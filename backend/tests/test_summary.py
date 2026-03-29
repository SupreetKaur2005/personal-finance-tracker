import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app.core.database import Base
from app.models.transaction import Transaction
from app.services.transaction_service import TransactionService

# Setup an in-memory db for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_monthly_summary_aggregation(db):
    service = TransactionService(db)
    
    # Insert dummy transactions
    t1 = Transaction(description="Salary", amount=1000, transaction_type="income", category="salary", timestamp=datetime(2025, 1, 15))
    t2 = Transaction(description="Rent", amount=-800, transaction_type="expense", category="rent", timestamp=datetime(2025, 1, 16))
    t3 = Transaction(description="Groceries", amount=-100, transaction_type="expense", category="food", timestamp=datetime(2025, 1, 17))
    t4 = Transaction(description="Next Month Rent", amount=-800, transaction_type="expense", category="rent", timestamp=datetime(2025, 2, 1))

    db.add_all([t1, t2, t3, t4])
    db.commit()

    # Get summary
    summary = service.get_monthly_summary()
    jan = "2025-01"
    feb = "2025-02"

    assert jan in summary
    assert feb in summary

    assert summary[jan]["income_total"] == 1000
    assert summary[jan]["expense_total"] == 900
    assert summary[jan]["net"] == 100
    assert summary[jan]["by_category"]["rent"] == 800
    assert summary[jan]["by_category"]["food"] == 100

    assert summary[feb]["expense_total"] == 800
    assert summary[feb]["by_category"]["rent"] == 800
