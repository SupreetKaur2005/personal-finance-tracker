import pytest
from app.services.categorizer import SmartCategorizer

def test_smart_categorizer_food():
    categorizer = SmartCategorizer()
    cat, conf = categorizer.categorize("McDonald's Lunch")
    assert cat == "dining"
    assert conf > 0.0

def test_smart_categorizer_transport():
    categorizer = SmartCategorizer()
    cat, conf = categorizer.categorize("Uber Ride")
    assert cat == "transportation"
    assert conf > 0.0

def test_smart_categorizer_fallback():
    categorizer = SmartCategorizer()
    cat, conf = categorizer.categorize("Unknown Vendor 12345")
    assert cat == "other"
    assert conf == 0.0

def test_smart_categorizer_rent():
    categorizer = SmartCategorizer()
    cat, conf = categorizer.categorize("Apartment Rent Payment")
    assert cat == "rent"
