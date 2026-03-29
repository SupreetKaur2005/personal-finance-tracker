from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.transaction_schema import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
    StatusUpdateRequest,
    SuggestCategoryRequest,
    BatchReclassifyRequest
)
from app.models.transaction import TransactionStateError
from app.services.transaction_service import TransactionService
from app.services.analytics_service import AnalyticsService
from app.services.categorizer import SmartCategorizer
from app.utils.validators import TransactionValidator
from typing import List
import csv
from io import StringIO

router = APIRouter(prefix="/transactions", tags=["transactions"])

def get_transaction_service(db: Session = Depends(get_db)):
    return TransactionService(db)

def get_analytics_service(db: Session = Depends(get_db)):
    return AnalyticsService(db)

@router.post("", response_model=TransactionResponse, status_code=201)
async def create_transaction(
    transaction: TransactionCreate,
    service: TransactionService = Depends(get_transaction_service)
):
    try:
        # Convert Pydantic model to dict for service layer unified validation
        result = service.create_transaction(transaction.dict())
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[TransactionResponse])
async def list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: TransactionService = Depends(get_transaction_service)
):
    return service.list_transactions(skip, limit)

@router.get("/summary", response_model=dict)
async def get_summary(
    year: int = Query(None),
    month: int = Query(None, ge=1, le=12),
    service: TransactionService = Depends(get_transaction_service)
):
    summary = service.get_monthly_summary(year, month)
    return {
        "status": "success",
        "data": summary,
        "filters": {"year": year, "month": month}
    }

@router.post("/suggest-category", response_model=dict)
async def suggest_category(request: SuggestCategoryRequest):
    """Real-time category suggestions via ML-ready categorizer"""
    categorizer = SmartCategorizer()
    suggestions = categorizer.suggest_categories(request.description)
    return {
        "status": "success",
        "suggestions": suggestions
    }

@router.get("/analytics/insights", response_model=dict)
async def get_financial_insights(
    service: AnalyticsService = Depends(get_analytics_service)
):
    """Get comprehensive financial insights"""
    return {
        "status": "success",
        "data": {
            "trends": service.get_spending_trends(),
            "categories": service.get_category_insights(),
            "patterns": service.get_spending_patterns(),
            "budget_alerts": service.get_budget_alerts({
                "groceries": 500,
                "dining": 300,
                "transport": 200
            })
        }
    }

@router.post("/batch/import")
async def bulk_import_transactions(
    file: UploadFile = File(...),
    service: TransactionService = Depends(get_transaction_service)
):
    """
    Import multiple transactions from CSV.
    CSV format: date, description, amount, type
    """
    try:
        content = await file.read()
        csv_reader = csv.DictReader(StringIO(content.decode()))
        
        imported = []
        errors = []
        
        for row_num, row in enumerate(csv_reader, start=2):
            try:
                # Clean header formatting mapping
                transaction = {
                    'description': row.get('description', ''),
                    'amount': float(row.get('amount', 0)),
                    'transaction_type': row.get('type', 'expense').lower()
                }
                
                # Check mapping format
                if 'date' in row and row['date']:
                    transaction['timestamp'] = row['date']
                    
                is_valid, validation_errors = TransactionValidator.validate_create_request(transaction)
                if not is_valid:
                    errors.append({"row": row_num, "errors": validation_errors})
                    continue
                
                result = service.create_transaction(transaction)
                imported.append(result)
                
            except Exception as e:
                errors.append({"row": row_num, "error": str(e)})
        
        return {
            "status": "success",
            "imported_count": len(imported),
            "error_count": len(errors),
            "errors": errors if errors else None,
            "data": [t.to_dict() for t in imported]
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Import failed: {str(e)}")

@router.patch("/batch/reclassify")
async def batch_reclassify(
    reclassify_request: BatchReclassifyRequest,
    service: TransactionService = Depends(get_transaction_service)
):
    """Bulk reclassify transactions that match criteria."""
    updated = service.batch_reclassify(
        filter_criteria=reclassify_request.filter,
        new_category=reclassify_request.new_category
    )
    
    return {
        "status": "success",
        "updated_count": len(updated),
        "data": [t.to_dict() for t in updated]
    }

@router.patch("/{transaction_id}/status")
async def update_transaction_status(
    transaction_id: int,
    status_update: StatusUpdateRequest,
    service: TransactionService = Depends(get_transaction_service)
):
    """
    Update transaction status with state machine validation.
    
    Valid transitions:
    PENDING -> CATEGORIZED, ARCHIVED
    CATEGORIZED -> VERIFIED, PENDING, ARCHIVED
    VERIFIED -> RECONCILED, CATEGORIZED, ARCHIVED
    RECONCILED -> ARCHIVED
    """
    try:
        result = service.update_transaction_status(
            transaction_id,
            status_update.new_status,
            changed_by=status_update.user_id
        )
        return {
            "status": "success",
            "data": result.to_dict(),
            "message": f"Transaction moved to {status_update.new_status}"
        }
    except TransactionStateError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{transaction_id}/reclassify", response_model=TransactionResponse)
async def reclassify_transaction(
    transaction_id: int,
    update: TransactionUpdate,
    service: TransactionService = Depends(get_transaction_service)
):
    try:
        result = service.reclassify_transaction(transaction_id, update.category)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction(
    transaction_id: int,
    service: TransactionService = Depends(get_transaction_service)
):
    try:
        service.delete_transaction(transaction_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
