from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, Dict

class TransactionCreate(BaseModel):
    """Schema for creating a transaction"""
    description: str = Field(..., min_length=3, max_length=255)
    amount: float = Field(..., gt=0)  # Must be positive
    transaction_type: str = Field(..., pattern="^(income|expense)$")
    category: Optional[str] = Field(None)
    timestamp: Optional[datetime] = Field(None)
    
    @validator('description')
    def description_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Description cannot be empty')
        return v.strip()

class TransactionUpdate(BaseModel):
    """Schema for updating a transaction"""
    category: str = Field(..., min_length=2)

class StatusUpdateRequest(BaseModel):
    """Schema for updating transaction status"""
    new_status: str
    user_id: str = "system"

class BatchReclassifyRequest(BaseModel):
    """Schema for batch reclassification"""
    filter: Dict[str, str]  # e.g., {"old_category": "other"}
    new_category: str

class SuggestCategoryRequest(BaseModel):
    """Schema for returning category recommendations"""
    description: str = Field(..., min_length=3)

class TransactionResponse(BaseModel):
    """Schema for transaction response"""
    id: int
    description: str
    amount: float
    transaction_type: str
    category: str
    status: str
    auto_tagged: bool
    timestamp: Optional[datetime]
    created_at: datetime
    is_duplicate: bool
    
    class Config:
        from_attributes = True

class TransactionSummary(BaseModel):
    """Schema for summary response"""
    month: str  # "2024-03"
    income_total: float
    expense_total: float
    net: float
    by_category: dict  # {"Food": 150.00, "Rent": 1000.00}
