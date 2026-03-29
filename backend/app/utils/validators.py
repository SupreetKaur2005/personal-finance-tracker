from typing import Dict, List, Tuple
from enum import Enum

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class ValidationError(Exception):
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__(f"Validation failed: {'; '.join(errors)}")

class TransactionValidator:
    """Comprehensive validation for transactions"""
    
    # Business rules
    INCOME_ONLY_CATEGORIES = ["salary", "bonus", "refund", "investment_returns"]
    EXPENSE_ONLY_CATEGORIES = ["rent", "utilities", "groceries", "transport", "dining", "entertainment", "healthcare", "shopping"]
    MIN_AMOUNT = 0.01
    MAX_AMOUNT = 1000000
    
    @staticmethod
    def validate_create_request(data: Dict) -> Tuple[bool, List[str]]:
        """Validate transaction creation request"""
        errors = []
        
        # Required fields
        if 'description' not in data or not str(data['description']).strip():
            errors.append("Description is required and cannot be empty")
        elif len(str(data['description'])) > 200:
            errors.append("Description cannot exceed 200 characters")
        
        if 'amount' not in data:
            errors.append("Amount is required")
        else:
            try:
                amount = float(data['amount'])
                if abs(amount) < TransactionValidator.MIN_AMOUNT:
                    errors.append(f"Amount must be at least {TransactionValidator.MIN_AMOUNT}")
                elif abs(amount) > TransactionValidator.MAX_AMOUNT:
                    errors.append(f"Amount cannot exceed {TransactionValidator.MAX_AMOUNT}")
            except (ValueError, TypeError):
                errors.append("Amount must be a valid number")
        
        type_val = data.get('transaction_type')
        if not type_val:
            errors.append("Transaction type is required")
        elif type_val not in [t.value for t in TransactionType]:
            errors.append(f"Transaction type must be one of: {[t.value for t in TransactionType]}")
        
        # Business rule validation
        category = data.get('category')
        if category:
            if category.lower() in TransactionValidator.INCOME_ONLY_CATEGORIES:
                if type_val == TransactionType.EXPENSE.value:
                    errors.append(f"Category '{category}' is only valid for income transactions")
            
            if category.lower() in TransactionValidator.EXPENSE_ONLY_CATEGORIES:
                if type_val == TransactionType.INCOME.value:
                    errors.append(f"Category '{category}' is only valid for expense transactions")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def normalize_transaction(data: Dict) -> Dict:
        """Normalize and sanitize transaction data"""
        normalized = data.copy()
        
        # Sanitize description
        if 'description' in normalized and normalized['description']:
            normalized['description'] = str(normalized['description']).strip()
        
        # Normalize amount sign based on type
        if 'amount' in normalized and 'transaction_type' in normalized:
            amount = float(normalized['amount'])
            if normalized['transaction_type'] == TransactionType.EXPENSE.value:
                normalized['amount'] = abs(amount) * -1.0
            else:
                normalized['amount'] = abs(amount)
        
        return normalized
