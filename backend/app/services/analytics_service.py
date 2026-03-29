from typing import Dict, List
from datetime import datetime, timedelta
from sqlalchemy import func
from app.models.transaction import Transaction

class AnalyticsService:
    """Generate financial insights"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    def get_spending_trends(self, months: int = 6) -> Dict:
        """Analyze spending trends over time"""
        cutoff_date = datetime.utcnow() - timedelta(days=30*months)
        
        expenses = self.db.query(
            func.strftime('%Y-%m', Transaction.timestamp).label('month'),
            func.sum(func.abs(Transaction.amount)).label('total')
        ).filter(
            Transaction.transaction_type == 'expense',
            Transaction.timestamp >= cutoff_date
        ).group_by('month').order_by('month').all()
        
        months_data = [float(e[1]) for e in expenses]
        monthly_dict = {str(e[0]): float(e[1]) for e in expenses}
        
        return {
            "monthly_totals": monthly_dict,
            "average": sum(months_data) / len(months_data) if months_data else 0,
            "max_month": max(months_data) if months_data else 0,
            "min_month": min(months_data) if months_data else 0,
            "trend": "increasing" if len(months_data) > 1 and months_data[-1] > months_data[0] else "decreasing"
        }
    
    def get_category_insights(self) -> List[Dict]:
        """Get insights per category for the current month"""
        this_month = datetime.utcnow().strftime('%Y-%m')
        
        categories = self.db.query(
            Transaction.category,
            func.sum(func.abs(Transaction.amount)).label('total'),
            func.count(Transaction.id).label('count')
        ).filter(
            Transaction.transaction_type == 'expense',
            func.strftime('%Y-%m', Transaction.timestamp) == this_month
        ).group_by(Transaction.category).all()
        
        return [
            {
                "category": cat,
                "total_spent": float(total),
                "transaction_count": count,
                "average_per_transaction": float(total / count) if count else 0
            }
            for cat, total, count in categories
        ]
    
    def get_budget_alerts(self, category_budgets: Dict) -> List[Dict]:
        """Alert if spending exceeds budgets"""
        insights = self.get_category_insights()
        alerts = []
        
        for insight in insights:
            category = insight['category']
            spent = insight['total_spent']
            budget = category_budgets.get(category, float('inf'))
            
            if spent > budget:
                alerts.append({
                    "category": category,
                    "budget": budget,
                    "spent": spent,
                    "overspent": spent - budget,
                    "percentage": (spent / budget * 100) if budget else 0,
                    "severity": "critical" if spent > budget * 1.5 else "warning"
                })
        
        return alerts
    
    def get_spending_patterns(self) -> Dict:
        """Identify spending patterns based on day of week"""
        # Day of week analysis SQLite %w returns string 0-6 (0 is Sunday)
        dow_query = self.db.query(
            func.strftime('%w', Transaction.timestamp).label('dow'),
            func.sum(func.abs(Transaction.amount)).label('total')
        ).filter(
            Transaction.transaction_type == 'expense'
        ).group_by('dow').all()
        
        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        dow_pattern = {}
        for d in dow_query:
            if d[0] is not None:
                dow_pattern[days[int(d[0])]] = float(d[1])
        
        return {
            "day_of_week_pattern": dow_pattern,
            "highest_spending_day": max(dow_pattern, key=dow_pattern.get) if dow_pattern else None,
            "lowest_spending_day": min(dow_pattern, key=dow_pattern.get) if dow_pattern else None
        }
