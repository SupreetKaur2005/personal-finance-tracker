import time
from finance_sdk.api.transactions_api import TransactionsApi
from finance_sdk.api_client import ApiClient
from finance_sdk.configuration import Configuration

print("="*50)
print("Personal Finance Tracker SDK Demonstration")
print("="*50)

# 1. Initialize API Client to hit localhost
configuration = Configuration(host="http://localhost:8000")
client = ApiClient(configuration)
api_instance = TransactionsApi(client)

try:
    print("\n[1] Fetching Monthly Summary Aggregations...")
    # NOTE: OpenAPI generated methods sometimes rename typical endpoints
    summary_response = api_instance.get_summary_transactions_summary_get()
    
    print("\n✅ Successfully retrieved SDK Data!")
    print(f"Response Status: {summary_response.status}")
    print(f"Available Months: {list(summary_response.data.keys())}")
    
    # Print the most recent month if it exists
    if summary_response.data:
        latest_month = sorted(summary_response.data.keys())[-1]
        data = summary_response.data[latest_month]
        print(f"\n📊 Summary for {latest_month}:")
        print(f"   => Total Income:  ${data.income_total:.2f}")
        print(f"   => Total Expense: ${data.expense_total:.2f}")
        print(f"   => Net Cashflow:  ${data.net:.2f}")
        print(f"   => Primary Spending Category: {max(data.by_category, key=data.by_category.get)}")

except Exception as e:
    print(f"❌ Failed to reach the backend API via SDK. Is the server running on port 8000?")
    print(f"Exception details: {e}")
