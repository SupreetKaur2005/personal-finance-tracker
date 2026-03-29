"""
Example SDK usage - demonstrates API calls programmatically
"""
import sys
import os

# Add SDK to path (when auto-generated)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sdk'))

import argparse
from datetime import datetime, timedelta

def demo_with_requests():
    """Demo using requests library (simpler for initial testing)"""
    import requests
    
    BASE_URL = "http://127.0.0.1:8000"
    
    print("📱 Personal Finance Tracker - SDK Demo\n")
    
    # Create a transaction
    print("1️⃣  Creating a transaction...")
    transaction_data = {
        "description": "Lunch at McDonald's",
        "amount": 15.50,
        "transaction_type": "expense"
    }
    
    response = requests.post(f"{BASE_URL}/transactions", json=transaction_data)
    if response.status_code == 201:
        transaction = response.json()
        print(f"✅ Transaction created: {transaction}")
        tx_id = transaction['id']
    else:
        print(f"❌ Failed: {response.text}")
        return
    
    # List transactions
    print("\n2️⃣  Listing transactions...")
    response = requests.get(f"{BASE_URL}/transactions")
    transactions = response.json()
    print(f"✅ Found {len(transactions)} transactions")
    for tx in transactions:
        print(f"  - {tx['description']}: ${tx['amount']} ({tx['category']})")
    
    # Get summary
    print("\n3️⃣  Getting monthly summary...")
    today = datetime.now()
    response = requests.get(
        f"{BASE_URL}/transactions/summary",
        params={"year": today.year, "month": today.month}
    )
    summary = response.json()
    print(f"✅ Summary: {summary}")
    
    # Reclassify
    print(f"\n4️⃣  Reclassifying transaction {tx_id}...")
    response = requests.patch(
        f"{BASE_URL}/transactions/{tx_id}/reclassify",
        json={"category": "food"}
    )
    if response.status_code == 200:
        print(f"✅ Reclassified successfully")
    
    print("\n✅ SDK Demo completed!")

def demo_with_generated_sdk():
    """Demo using auto-generated SDK"""
    try:
        from finance_sdk import ApiClient, Configuration
        from finance_sdk.api.transactions_api import TransactionsApi
        from finance_sdk.models.transaction_create import TransactionCreate
        
        print("🔧 Using generated SDK...\n")
        
        configuration = Configuration(host="http://127.0.0.1:8000")
        client = ApiClient(configuration)
        api = TransactionsApi(client)
        
        print("1️⃣  Creating a transaction...")
        txn_create = TransactionCreate(
            description="Uber Ride to Airport",
            amount=45.0,
            transaction_type="expense",
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        created_txn = api.create_transaction_transactions_post(txn_create)
        print(f"✅ Transaction created with ID: {created_txn.id}")
        
        print("\n2️⃣  Listing transactions...")
        transactions = api.list_transactions_transactions_get()
        print(f"✅ Found {len(transactions)} transactions")
        
        print("\n3️⃣  Getting summary...")
        summary_response = api.get_summary_transactions_summary_get()
        print(f"✅ Summary retrieved successfully")
        
    except ImportError as e:
        print("⚠️  Generated SDK not found or failed to import. Run generate_sdk.py first.")
        print(f"Error: {e}")
        print("Falling back to requests library library demo...\n")
        demo_with_requests()
    except Exception as e:
        print(f"❌ Failed to reach the backend API via SDK. Is the server running on port 8000?")
        print(f"Exception details: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Finance Tracker SDK Demo")
    parser.add_argument("--sdk", action="store_true", help="Use generated SDK")
    args = parser.parse_args()
    
    if args.sdk:
        demo_with_generated_sdk()
    else:
        demo_with_requests()
