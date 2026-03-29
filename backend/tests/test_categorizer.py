import pytest
from app.services.categorizer import TransactionCategorizer

class TestCategorization:
    """Test transaction categorization"""
    
    def test_food_detection(self):
        """Test food category detection"""
        category, auto_tagged = TransactionCategorizer.categorize("Lunch at McDonald's")
        assert category == "dining"
        assert auto_tagged == True
    
    def test_transport_detection(self):
        """Test transport category detection"""
        category, auto_tagged = TransactionCategorizer.categorize("Uber ride to office")
        assert category == "transportation"
    
    def test_entertainment_detection(self):
        """Test entertainment category detection"""
        category, auto_tagged = TransactionCategorizer.categorize("Netflix subscription")
        assert category == "entertainment"
    
    def test_salary_detection(self):
        """Test salary/income detection"""
        category, auto_tagged = TransactionCategorizer.categorize("Monthly salary deposit")
        assert category == "salary"
    
    def test_unknown_category(self):
        """Test unknown category defaults to 'other'"""
        category, auto_tagged = TransactionCategorizer.categorize("Random expense XYZ")
        assert category == "other"
    
    def test_case_insensitive(self):
        """Test that categorization is case-insensitive"""
        category1, _ = TransactionCategorizer.categorize("MCDONALD'S")
        category2, _ = TransactionCategorizer.categorize("mcdonald's")
        assert category1 == category2 == "dining"
