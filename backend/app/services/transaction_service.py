from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.models.transaction import Transaction, TransactionStatus, TransactionStateError
from app.schemas.transaction_schema import TransactionCreate
from app.services.categorizer import SmartCategorizer
from app.services.duplicate_detector import DuplicateDetector
from app.utils.validators import TransactionValidator
from app.core.logging_config import LoggerSetup

logger = LoggerSetup.setup()

class TransactionService:
    """Business logic for transactions"""
    
    def __init__(self, db: Session):
        self.db = db
        self.categorizer = SmartCategorizer()
    
    def create_transaction(self, data: dict) -> Transaction:
        """
        Create a new transaction with:
        1. Validation
        2. Amount normalization
        3. Auto-categorization (ML-like)
        4. Duplicate detection (Fuzzy Math)
        """
        logger.info("Creating transaction started", extra={
            "amount": data.get('amount'),
            "type": data.get('transaction_type'),
            "description": data.get('description')
        })
        
        # Step 1: Validate
        is_valid, errors = TransactionValidator.validate_create_request(data)
        if not is_valid:
            logger.error("Validation failed", extra={"errors": errors, "input": data})
            raise ValueError(f"Validation failed: {'; '.join(errors)}")
        
        # Step 2: Normalize amount
        normalized_data = TransactionValidator.normalize_transaction(data)
        
        # Step 3: Auto-categorize
        # Get categorization with confidence
        if data.get('category'):
            category = data['category']
            auto_tagged = False
        else:
            category, confidence = self.categorizer.categorize(normalized_data['description'])
            auto_tagged = confidence > 0.0 # Standard fallback means high confidence if it matches a pattern
        
        # Step 4: Check for duplicates
        # Fetch recent transactions for duplicate check
        cutoff_time = datetime.utcnow() - datetime.timedelta(minutes=30) if 'timedelta' in globals() else datetime.utcnow()
        recent_txns = self.db.query(Transaction).filter(
            Transaction.created_at >= (datetime.utcnow() - __import__('datetime').timedelta(minutes=30))
        ).all()
        existing_dicts = [txn.to_dict() for txn in recent_txns]
        
        is_dup, dup_match = DuplicateDetector.is_duplicate(
            {**normalized_data, "timestamp": datetime.utcnow()},
            existing_dicts,
            time_window_minutes=30
        )
        
        if is_dup:
            logger.warning("Duplicate transaction detected", extra={"duplicate_of": dup_match['id']})
            raise ValueError(
                f"Duplicate transaction detected. "
                f"Similar transaction from {dup_match['timestamp']}"
            )
        
        # Step 5: Create transaction
        timestamp_val = data.get('timestamp')
        if not timestamp_val:
            timestamp_val = datetime.utcnow()
        elif isinstance(timestamp_val, str):
            timestamp_val = datetime.fromisoformat(timestamp_val.replace('Z', '+00:00'))

        transaction = Transaction(
            description=normalized_data['description'],
            amount=normalized_data['amount'],
            transaction_type=normalized_data['transaction_type'],
            category=category,
            auto_tagged=auto_tagged,
            status=TransactionStatus.CATEGORIZED.value,
            timestamp=timestamp_val
        )
        
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        
        logger.info("Transaction created successfully", extra={
            "transaction_id": transaction.id,
            "category": transaction.category,
            "auto_tagged": transaction.auto_tagged,
            "status": transaction.status
        })
        
        return transaction

    def update_transaction_status(self, transaction_id: int, new_status: str, changed_by: str = "system") -> Transaction:
        """Update a transaction's status via state machine"""
        transaction = self.db.query(Transaction).get(transaction_id)
        if not transaction:
            raise ValueError(f"Transaction {transaction_id} not found")
        
        try:
            transaction.transition_to(new_status, changed_by)
            self.db.commit()
            self.db.refresh(transaction)
            logger.info("Transaction status updated", extra={
                "transaction_id": transaction_id,
                "new_status": new_status
            })
            return transaction
        except TransactionStateError as e:
            logger.warning("Invalid state transition", extra={"error": str(e), "transaction_id": transaction_id})
            raise e
    
    def get_monthly_summary(self, year: int = None, month: int = None) -> dict:
        query = self.db.query(
            func.strftime('%Y-%m', Transaction.timestamp).label('month'),
            Transaction.transaction_type,
            Transaction.category,
            func.sum(Transaction.amount).label('total'),
            func.count(Transaction.id).label('count')
        ).filter(
            Transaction.is_duplicate == False
        )
        
        if year and month:
            query = query.filter(
                func.strftime('%Y', Transaction.timestamp) == str(year),
                func.strftime('%m', Transaction.timestamp) == f"{month:02d}"
            )
        
        results = query.group_by(
            func.strftime('%Y-%m', Transaction.timestamp),
            Transaction.transaction_type,
            Transaction.category
        ).all()
        
        summary = {}
        for month_str, trans_type, category, total, count in results:
            if not month_str:
                continue
            if month_str not in summary:
                summary[month_str] = {
                    "income_total": 0,
                    "expense_total": 0,
                    "by_category": {}
                }
            
            if trans_type == "income":
                summary[month_str]["income_total"] += total
            else:
                summary[month_str]["expense_total"] += abs(total)
            
            if category not in summary[month_str]["by_category"]:
                summary[month_str]["by_category"][category] = 0
            
            if trans_type == "expense":
                summary[month_str]["by_category"][category] += abs(total)
            else:
                summary[month_str]["by_category"][category] += total
        
        for month_str in summary:
            summary[month_str]["net"] = (
                summary[month_str]["income_total"] - 
                summary[month_str]["expense_total"]
            )
        
        return summary
    
    def reclassify_transaction(self, transaction_id: int, new_category: str) -> Transaction:
        """Manually override category for a transaction"""
        transaction = self.db.query(Transaction).get(transaction_id)
        if not transaction:
            raise ValueError(f"Transaction {transaction_id} not found")
        
        transaction.category = new_category
        transaction.auto_tagged = False  # Mark as manually categorized
        transaction.updated_at = datetime.utcnow()
        
        # If categorized, bump the state
        if transaction.status == TransactionStatus.PENDING.value:
            transaction.transition_to(TransactionStatus.CATEGORIZED.value, "system_reclassify")
            
        self.db.commit()
        self.db.refresh(transaction)
        
        logger.info("Transaction reclassified", extra={
            "transaction_id": transaction_id,
            "new_category": new_category
        })
        return transaction
    
    def batch_reclassify(self, filter_criteria: dict, new_category: str) -> list:
        """Bulk reclassify matching criteria"""
        query = self.db.query(Transaction)
        for key, value in filter_criteria.items():
            if key == "old_category":
                query = query.filter(Transaction.category == value)
            elif hasattr(Transaction, key):
                query = query.filter(getattr(Transaction, key) == value)
                
        matching = query.all()
        updated = []
        for txn in matching:
            txn.category = new_category
            txn.auto_tagged = False
            txn.updated_at = datetime.utcnow()
            updated.append(txn)
            
        self.db.commit()
        logger.info("Batch reclassify completed", extra={
            "count": len(updated),
            "new_category": new_category
        })
        return updated
    
    def list_transactions(self, skip: int = 0, limit: int = 100) -> list:
        return self.db.query(Transaction).filter(
            Transaction.is_duplicate == False
        ).order_by(
            Transaction.timestamp.desc()
        ).offset(skip).limit(limit).all()
    
    def delete_transaction(self, transaction_id: int) -> bool:
        transaction = self.db.query(Transaction).get(transaction_id)
        if not transaction:
            raise ValueError(f"Transaction {transaction_id} not found")
        
        self.db.delete(transaction)
        self.db.commit()
        return True
