from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Index
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum
from app.core.database import Base

class TransactionStatus(str, Enum):
    """Transaction lifecycle states"""
    PENDING = "pending"
    CATEGORIZED = "categorized"
    VERIFIED = "verified"
    RECONCILED = "reconciled"
    ARCHIVED = "archived"

class TransactionStateError(Exception):
    """Raised when invalid state transition attempted"""
    pass

class Transaction(Base):
    """Transaction model"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Core fields
    description = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(10), nullable=False)  # 'income' or 'expense'
    
    # Category fields
    category = Column(String(50), nullable=False, default="uncategorized")
    auto_tagged = Column(Boolean, default=True)  # Was category auto-detected?
    status = Column(String(20), default=TransactionStatus.PENDING.value)
    
    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Audit trail
    status_changed_at = Column(DateTime)
    status_changed_by = Column(String(100))  # user_id or "system"
    
    # Duplicate tracking (retaining from previous functionality for the overall structure)
    is_duplicate = Column(Boolean, default=False)
    duplicate_of = Column(Integer, nullable=True)  # ID of original transaction
    
    # Strategic indexes for common queries
    __table_args__ = (
        Index('idx_timestamp', 'timestamp'),
        Index('idx_category_timestamp', 'category', 'timestamp'),
        Index('idx_duplicate_check', 'description', 'amount', 'timestamp'),
        Index('idx_status', 'status'),
        Index('idx_type_category_month', 'transaction_type', 'category', 'timestamp'),
        Index('idx_created_at', 'created_at'),
    )
    
    @staticmethod
    def get_valid_transitions(current_status: str) -> list:
        """Define valid state transitions"""
        transitions = {
            TransactionStatus.PENDING.value: [
                TransactionStatus.CATEGORIZED.value,
                TransactionStatus.ARCHIVED.value
            ],
            TransactionStatus.CATEGORIZED.value: [
                TransactionStatus.VERIFIED.value,
                TransactionStatus.PENDING.value,  # Allow going back to correct
                TransactionStatus.ARCHIVED.value
            ],
            TransactionStatus.VERIFIED.value: [
                TransactionStatus.RECONCILED.value,
                TransactionStatus.CATEGORIZED.value,
                TransactionStatus.ARCHIVED.value
            ],
            TransactionStatus.RECONCILED.value: [
                TransactionStatus.ARCHIVED.value
            ],
            TransactionStatus.ARCHIVED.value: []  # Terminal state
        }
        return transitions.get(current_status, [])
    
    def transition_to(self, new_status: str, changed_by: str = "system"):
        """Change status with validation"""
        valid_transitions = self.get_valid_transitions(self.status)
        
        if new_status not in valid_transitions:
            raise TransactionStateError(
                f"Cannot transition from {self.status} to {new_status}. "
                f"Valid transitions: {valid_transitions}"
            )
        
        self.status = new_status
        self.status_changed_at = datetime.utcnow()
        self.status_changed_by = changed_by

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'amount': self.amount,
            'transaction_type': self.transaction_type,
            'category': self.category,
            'auto_tagged': self.auto_tagged,
            'status': self.status,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_duplicate': self.is_duplicate,
        }
