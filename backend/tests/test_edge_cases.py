"""
Edge-case tests for the Personal Finance Tracker backend.

Covers three main areas:
  1. Duplicate detection window   — boundary conditions around the 30-minute window
  2. Invalid transaction type     — validator rejects bad/missing types
  3. Reclassification overrides   — manual category override logic
"""

from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from app.models.transaction import Transaction, TransactionStatus, TransactionStateError
from app.services.duplicate_detector import DuplicateDetector
from app.services.transaction_service import TransactionService
from app.utils.validators import TransactionValidator


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_txn(desc="Coffee", amount=5.0, txn_type="expense", minutes_ago=0):
    """Return a minimal transaction dict as used by DuplicateDetector."""
    ts = datetime.utcnow() - timedelta(minutes=minutes_ago)
    return {
        "description": desc,
        "amount": amount,
        "transaction_type": txn_type,
        "timestamp": ts.isoformat(),
    }


# ===========================================================================
# 1. DUPLICATE DETECTION WINDOW
# ===========================================================================

class TestDuplicateDetectionWindow:
    """Boundary tests around the 30-minute duplicate window."""

    def test_exact_duplicate_within_window(self):
        """Same description, amount, and type within 30 min → duplicate."""
        existing = [_make_txn(minutes_ago=0)]
        new = _make_txn(minutes_ago=0)
        is_dup, match = DuplicateDetector.is_duplicate(new, existing, time_window_minutes=30)
        assert is_dup is True
        assert match is not None

    def test_duplicate_at_window_boundary_is_caught(self):
        """Transaction submitted exactly at 29 minutes → still a duplicate."""
        existing = [_make_txn(minutes_ago=29)]
        new = _make_txn(minutes_ago=0)
        is_dup, _ = DuplicateDetector.is_duplicate(new, existing, time_window_minutes=30)
        assert is_dup is True

    def test_outside_window_not_duplicate(self):
        """Transaction submitted 31 minutes later → NOT a duplicate."""
        existing = [_make_txn(minutes_ago=31)]
        new = _make_txn(minutes_ago=0)
        is_dup, _ = DuplicateDetector.is_duplicate(new, existing, time_window_minutes=30)
        assert is_dup is False

    def test_exactly_at_window_edge_excluded(self):
        """Transaction submitted exactly 30 minutes later → NOT a duplicate (strict >)."""
        existing = [_make_txn(minutes_ago=30)]
        new = _make_txn(minutes_ago=0)
        is_dup, _ = DuplicateDetector.is_duplicate(new, existing, time_window_minutes=30)
        # time_diff == 30.0 > 30 → False; the implementation uses > so this is NOT a duplicate
        assert is_dup is False

    def test_custom_window_respected(self):
        """A larger custom window catches transactions that the default 30-min window would miss."""
        existing = [_make_txn(minutes_ago=45)]
        new = _make_txn(minutes_ago=0)

        is_dup_30, _ = DuplicateDetector.is_duplicate(new, existing, time_window_minutes=30)
        is_dup_60, _ = DuplicateDetector.is_duplicate(new, existing, time_window_minutes=60)

        assert is_dup_30 is False
        assert is_dup_60 is True

    def test_different_amount_outside_variance_not_dup(self):
        """Same description/time but amount differs by >5% → NOT a duplicate."""
        existing = [_make_txn(amount=10.0, minutes_ago=5)]
        new = _make_txn(amount=10.7, minutes_ago=0)  # 7% variance
        is_dup, _ = DuplicateDetector.is_duplicate(new, existing, time_window_minutes=30)
        assert is_dup is False

    def test_amount_within_variance_is_dup(self):
        """Amount difference ≤5% → duplicate (fuzzy amount match)."""
        existing = [_make_txn(amount=10.0, minutes_ago=5)]
        new = _make_txn(amount=10.4, minutes_ago=0)  # 4% variance
        is_dup, _ = DuplicateDetector.is_duplicate(new, existing, time_window_minutes=30)
        assert is_dup is True

    def test_different_type_not_dup(self):
        """Same description/amount/time but different type → NOT a duplicate."""
        existing = [_make_txn(txn_type="expense", minutes_ago=5)]
        new = _make_txn(txn_type="income", minutes_ago=0)
        is_dup, _ = DuplicateDetector.is_duplicate(new, existing, time_window_minutes=30)
        assert is_dup is False

    def test_fuzzy_description_match_within_threshold_is_dup(self):
        """Slightly different description that still meets similarity ≥0.75 → duplicate."""
        existing = [_make_txn(desc="Starbucks Coffee", minutes_ago=5)]
        new = _make_txn(desc="Starbucks Coffe", minutes_ago=0)  # typo, high similarity
        is_dup, _ = DuplicateDetector.is_duplicate(new, existing, time_window_minutes=30)
        assert is_dup is True

    def test_very_different_description_not_dup(self):
        """Descriptions with <75% similarity → NOT a duplicate even within window."""
        existing = [_make_txn(desc="Netflix Subscription", minutes_ago=5)]
        new = _make_txn(desc="Amazon Purchase", minutes_ago=0)
        is_dup, _ = DuplicateDetector.is_duplicate(new, existing, time_window_minutes=30)
        assert is_dup is False

    def test_empty_existing_list_never_duplicate(self):
        """No existing transactions → can never be a duplicate."""
        new = _make_txn()
        is_dup, match = DuplicateDetector.is_duplicate(new, [])
        assert is_dup is False
        assert match is None

    def test_find_duplicate_clusters(self):
        """find_duplicate_clusters groups identical transactions together."""
        t1 = _make_txn(desc="Netflix", minutes_ago=1)
        t2 = _make_txn(desc="Netflix", minutes_ago=2)  # same cluster
        t3 = _make_txn(desc="Rent", minutes_ago=3)       # different cluster

        clusters = DuplicateDetector.find_duplicate_clusters([t1, t2, t3])
        assert len(clusters) == 1
        assert len(clusters[0]) == 2

    def test_service_raises_on_duplicate(self, db_session):
        """TransactionService.create_transaction raises ValueError for duplicates."""
        service = TransactionService(db_session)
        data = {
            "description": "Duplicate Coffee",
            "amount": 4.50,
            "transaction_type": "expense",
        }
        service.create_transaction(data)

        with pytest.raises(ValueError, match="Duplicate transaction detected"):
            service.create_transaction(data)


# ===========================================================================
# 2. INVALID TRANSACTION TYPE
# ===========================================================================

class TestInvalidTransactionType:
    """Validator rejects bad or missing transaction_type values."""

    @pytest.mark.parametrize("bad_type", [
        "debit",
        "credit",
        "transfer",
        "INCOME",        # uppercase — not a valid enum value
        "EXPENSE",       # uppercase
        "Income",        # mixed case
        "",
        "  ",
        "null",
        "123",
        "!@#",
    ])
    def test_invalid_type_rejected(self, bad_type):
        """Any non-canonical type string should produce a validation error."""
        data = {
            "description": "Test transaction",
            "amount": 100.0,
            "transaction_type": bad_type,
        }
        is_valid, errors = TransactionValidator.validate_create_request(data)
        assert is_valid is False
        assert any("transaction type" in e.lower() for e in errors), errors

    def test_missing_type_rejected(self):
        """Omitting transaction_type entirely produces a validation error."""
        data = {"description": "No type", "amount": 50.0}
        is_valid, errors = TransactionValidator.validate_create_request(data)
        assert is_valid is False
        assert any("transaction type" in e.lower() for e in errors)

    def test_none_type_rejected(self):
        """Explicit None value for transaction_type produces a validation error."""
        data = {"description": "None type", "amount": 50.0, "transaction_type": None}
        is_valid, errors = TransactionValidator.validate_create_request(data)
        assert is_valid is False

    def test_valid_income_accepted(self):
        is_valid, errors = TransactionValidator.validate_create_request({
            "description": "Paycheck",
            "amount": 3000.0,
            "transaction_type": "income",
        })
        assert is_valid is True
        assert errors == []

    def test_valid_expense_accepted(self):
        is_valid, errors = TransactionValidator.validate_create_request({
            "description": "Electricity bill",
            "amount": 120.0,
            "transaction_type": "expense",
        })
        assert is_valid is True
        assert errors == []

    def test_service_raises_on_invalid_type(self, db_session):
        """TransactionService.create_transaction raises ValueError for invalid type."""
        service = TransactionService(db_session)
        with pytest.raises(ValueError, match="Validation failed"):
            service.create_transaction({
                "description": "Bad type txn",
                "amount": 50.0,
                "transaction_type": "transfer",
            })

    def test_income_only_category_with_expense_type_rejected(self):
        """Using an income-only category (e.g. 'salary') with 'expense' type → error."""
        data = {
            "description": "Salary payment",
            "amount": 5000.0,
            "transaction_type": "expense",
            "category": "salary",
        }
        is_valid, errors = TransactionValidator.validate_create_request(data)
        assert is_valid is False
        assert any("income" in e.lower() for e in errors)

    def test_expense_only_category_with_income_type_rejected(self):
        """Using an expense-only category (e.g. 'rent') with 'income' type → error."""
        data = {
            "description": "Rent received",
            "amount": 800.0,
            "transaction_type": "income",
            "category": "rent",
        }
        is_valid, errors = TransactionValidator.validate_create_request(data)
        assert is_valid is False
        assert any("expense" in e.lower() for e in errors)

    # Amount edge cases while we're validating the request structure
    def test_zero_amount_rejected(self):
        is_valid, errors = TransactionValidator.validate_create_request({
            "description": "Zero test",
            "amount": 0.0,
            "transaction_type": "expense",
        })
        assert is_valid is False

    def test_exceeds_max_amount_rejected(self):
        is_valid, errors = TransactionValidator.validate_create_request({
            "description": "Huge payment",
            "amount": 1_000_001.0,
            "transaction_type": "expense",
        })
        assert is_valid is False

    def test_negative_income_normalizes_to_positive(self):
        """normalize_transaction flips a negative income amount to positive."""
        normalized = TransactionValidator.normalize_transaction({
            "description": "salary",
            "amount": -3000.0,
            "transaction_type": "income",
        })
        assert normalized["amount"] == 3000.0

    def test_positive_expense_normalizes_to_negative(self):
        """normalize_transaction flips a positive expense amount to negative."""
        normalized = TransactionValidator.normalize_transaction({
            "description": "coffee",
            "amount": 5.0,
            "transaction_type": "expense",
        })
        assert normalized["amount"] == -5.0


# ===========================================================================
# 3. RECLASSIFICATION OVERRIDES
# ===========================================================================

class TestReclassificationOverrides:
    """Manual category override via reclassify_transaction."""

    def test_reclassify_changes_category(self, db_session):
        """Reclassifying a transaction updates its category."""
        service = TransactionService(db_session)
        txn = service.create_transaction({
            "description": "Amazon Purchase",
            "amount": 50.0,
            "transaction_type": "expense",
        })
        original_category = txn.category

        updated = service.reclassify_transaction(txn.id, "gifts")
        assert updated.category == "gifts"
        assert updated.category != original_category

    def test_reclassify_clears_auto_tagged_flag(self, db_session):
        """After manual reclassification auto_tagged must be False."""
        service = TransactionService(db_session)
        txn = service.create_transaction({
            "description": "Netflix Subscription",
            "amount": 15.0,
            "transaction_type": "expense",
        })
        assert txn.auto_tagged is True  # auto-categorized on creation

        updated = service.reclassify_transaction(txn.id, "personal_care")
        assert updated.auto_tagged is False

    def test_reclassify_nonexistent_transaction_raises(self, db_session):
        """Reclassifying a transaction that doesn't exist → ValueError."""
        service = TransactionService(db_session)
        with pytest.raises(ValueError, match="not found"):
            service.reclassify_transaction(99999, "food")

    def test_reclassify_pending_transaction_advances_status(self, db_session):
        """A PENDING transaction should be bumped to CATEGORIZED on reclassify."""
        service = TransactionService(db_session)

        # Insert a raw PENDING transaction directly (bypassing create_transaction)
        pending_txn = Transaction(
            description="Mystery charge",
            amount=-20.0,
            transaction_type="expense",
            category="other",
            auto_tagged=True,
            status=TransactionStatus.PENDING.value,
            timestamp=datetime.utcnow(),
        )
        db_session.add(pending_txn)
        db_session.commit()
        db_session.refresh(pending_txn)

        updated = service.reclassify_transaction(pending_txn.id, "dining")
        assert updated.status == TransactionStatus.CATEGORIZED.value

    def test_reclassify_verified_transaction_keeps_status(self, db_session):
        """Reclassifying a VERIFIED transaction must not change its status."""
        service = TransactionService(db_session)
        txn = service.create_transaction({
            "description": "Spotify",
            "amount": 10.0,
            "transaction_type": "expense",
        })
        # Advance to VERIFIED
        service.update_transaction_status(txn.id, TransactionStatus.VERIFIED.value)

        updated = service.reclassify_transaction(txn.id, "entertainment")
        # Status should remain VERIFIED (reclassify only bumps PENDING → CATEGORIZED)
        assert updated.status == TransactionStatus.VERIFIED.value
        assert updated.category == "entertainment"

    def test_reclassify_same_category_is_idempotent(self, db_session):
        """Re-applying the same category should succeed and keep auto_tagged=False."""
        service = TransactionService(db_session)
        txn = service.create_transaction({
            "description": "Grocery store",
            "amount": 60.0,
            "transaction_type": "expense",
        })

        first = service.reclassify_transaction(txn.id, "groceries")
        second = service.reclassify_transaction(first.id, "groceries")
        assert second.category == "groceries"
        assert second.auto_tagged is False

    def test_batch_reclassify_updates_all_matching(self, db_session):
        """batch_reclassify updates every transaction matching the filter criteria."""
        service = TransactionService(db_session)

        # Create several transactions in the same auto-categorized bucket
        for desc in ["Uber ride", "Lyft ride", "Taxi fare"]:
            service.create_transaction({
                "description": desc,
                "amount": 12.0,
                "transaction_type": "expense",
            })

        # All should land in "transportation"
        updated = service.batch_reclassify(
            filter_criteria={"old_category": "transportation"},
            new_category="commute",
        )
        assert len(updated) >= 1
        assert all(t.category == "commute" for t in updated)
        assert all(t.auto_tagged is False for t in updated)

    def test_batch_reclassify_empty_criteria_returns_all(self, db_session):
        """batch_reclassify with no useful filter still returns a list (not an error)."""
        service = TransactionService(db_session)
        service.create_transaction({
            "description": "Payday",
            "amount": 2000.0,
            "transaction_type": "income",
        })
        # Passing a non-existent old_category should return an empty list gracefully
        result = service.batch_reclassify(
            filter_criteria={"old_category": "nonexistent_cat_xyz"},
            new_category="other",
        )
        assert isinstance(result, list)
        assert len(result) == 0

    def test_reclassify_updates_updated_at_timestamp(self, db_session):
        """reclassify_transaction must refresh the updated_at timestamp."""
        service = TransactionService(db_session)
        txn = service.create_transaction({
            "description": "Magazine",
            "amount": 8.0,
            "transaction_type": "expense",
        })
        before = txn.updated_at  # may be None right after creation

        updated = service.reclassify_transaction(txn.id, "books")
        # updated_at should now be set (not None) and ≥ original
        assert updated.updated_at is not None
        if before is not None:
            assert updated.updated_at >= before
