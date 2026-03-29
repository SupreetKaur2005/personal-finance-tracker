from datetime import datetime, timedelta
import pytest
from app.services.transaction_service import TransactionService
from app.models.transaction import Transaction, TransactionStatus

def test_create_transaction_success(db_session):
    service = TransactionService(db_session)
    data = {
        "description": "Amazon Purchase",
        "amount": -50.25,
        "transaction_type": "expense",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    txn = service.create_transaction(data)
    
    assert txn.id is not None
    assert txn.description == "Amazon Purchase"
    assert txn.amount == -50.25  # Should be normalized to negative
    assert txn.transaction_type == "expense"
    assert txn.status == TransactionStatus.CATEGORIZED.value
    assert txn.category == "shopping"  # Assuming 'Amazon' categorizes to shopping
    assert txn.auto_tagged is True

def test_duplicate_transaction_detection(db_session):
    service = TransactionService(db_session)
    data = {
        "description": "Starbucks Coffee",
        "amount": 5.50,
        "transaction_type": "expense",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # First creation should succeed
    txn1 = service.create_transaction(data)
    assert txn1.id is not None
    
    # Second creation within 30 mins should fail as duplicate
    with pytest.raises(ValueError, match="Duplicate transaction detected"):
        service.create_transaction(data)

def test_transaction_state_transitions(db_session):
    service = TransactionService(db_session)
    data = {
        "description": "Monthly Salary",
        "amount": 5000.00,
        "transaction_type": "income"
    }
    
    txn = service.create_transaction(data)
    assert txn.status == TransactionStatus.CATEGORIZED.value
    
    # Transition to VERIFIED
    updated_txn = service.update_transaction_status(txn.id, TransactionStatus.VERIFIED.value)
    assert updated_txn.status == TransactionStatus.VERIFIED.value
    
    # Invalid transition (e.g. going from VERIFIED directly to PENDING) should fail. wait, PENDING may not be valid from VERIFIED.
    # From transaction.py: VERIFIED -> RECONCILED, CATEGORIZED, ARCHIVED
    with pytest.raises(Exception):
        service.update_transaction_status(txn.id, TransactionStatus.PENDING.value)

def test_monthly_summary(db_session):
    service = TransactionService(db_session)
    
    # Create test transactions
    now = datetime.utcnow()
    service.create_transaction({
        "description": "Salary", "amount": 2000.0, "transaction_type": "income", "timestamp": now.isoformat()
    })
    service.create_transaction({
        "description": "Rent", "amount": -1000.0, "transaction_type": "expense", "timestamp": now.isoformat()
    })
    service.create_transaction({
        "description": "Groceries", "amount": -200.0, "transaction_type": "expense", "timestamp": now.isoformat()
    })
    
    summary = service.get_monthly_summary(year=now.year, month=now.month)
    month_key = f"{now.year}-{now.month:02d}"
    
    assert month_key in summary
    assert summary[month_key]["income_total"] == 2000.0
    assert summary[month_key]["expense_total"] == 1200.0
    assert summary[month_key]["net"] == 800.0
    assert summary[month_key]["by_category"]["rent"] == 1000.0
