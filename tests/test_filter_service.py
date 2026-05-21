"""Tests for FilterService and NoMatch generation."""

import pandas as pd
import pytest

from zomato_cursor.config import settings
from zomato_cursor.data.store import store
from zomato_cursor.models.preferences import UserPreferences
from zomato_cursor.services.filter_service import FilterService
from zomato_cursor.services.no_match_builder import build_no_match

@pytest.fixture(autouse=True)
def mock_store():
    """Inject a dummy dataset into the store for testing."""
    df = pd.DataFrame([
        {
            "id": "1", "name": "Fancy Indian", "city": "bangalore", "location": "banashankari",
            "address": "", "cuisines": ["North Indian", "Mughlai"], "rating": 4.5, "votes": 100,
            "cost_for_two": 600, "budget_band": "medium", "rest_type": "Casual",
            "dish_liked": "", "online_order": True, "book_table": True, "url": "", "review_snippet": ""
        },
        {
            "id": "2", "name": "Cheap Italian", "city": "bangalore", "location": "indiranagar",
            "address": "", "cuisines": ["Italian", "Pizza"], "rating": 3.5, "votes": 50,
            "cost_for_two": 300, "budget_band": "low", "rest_type": "Cafe",
            "dish_liked": "", "online_order": False, "book_table": False, "url": "", "review_snippet": ""
        },
        {
            "id": "3", "name": "Expensive Indian", "city": "bangalore", "location": "banashankari",
            "address": "", "cuisines": ["North Indian", "South Indian"], "rating": 4.8, "votes": 500,
            "cost_for_two": 1500, "budget_band": "high", "rest_type": "Fine Dining",
            "dish_liked": "", "online_order": True, "book_table": True, "url": "", "review_snippet": ""
        },
        {
            "id": "4", "name": "Bad Indian", "city": "bangalore", "location": "banashankari",
            "address": "", "cuisines": ["North Indian"], "rating": 2.5, "votes": 10,
            "cost_for_two": 500, "budget_band": "medium", "rest_type": "Casual",
            "dish_liked": "", "online_order": True, "book_table": False, "url": "", "review_snippet": ""
        },
        {
            "id": "5", "name": "Missing Rating", "city": "bangalore", "location": "banashankari",
            "address": "", "cuisines": ["North Indian"], "rating": None, "votes": 0,
            "cost_for_two": 500, "budget_band": "medium", "rest_type": "Casual",
            "dish_liked": "", "online_order": False, "book_table": False, "url": "", "review_snippet": ""
        }
    ])
    store.df = df
    yield
    store.df = None

def test_exact_match_banashankari_north_indian_medium_4_0():
    prefs = UserPreferences(
        location="Banashankari",
        cuisine="North Indian",
        budget="medium",
        min_rating=4.0
    )
    results = FilterService.filter(prefs)
    assert len(results) == 1
    assert results[0].id == "1"
    assert results[0].name == "Fancy Indian"

def test_no_match():
    prefs = UserPreferences(
        location="Banashankari",
        cuisine="Italian",  # No Italian in Banashankari in our mock
        budget="low"
    )
    results = FilterService.filter(prefs)
    assert len(results) == 0

def test_rating_sort_and_nulls():
    prefs = UserPreferences(
        location="Banashankari",
        cuisine="North Indian"
    )
    results = FilterService.filter(prefs)
    # IDs should be 3 (4.8), 1 (4.5), 4 (2.5), 5 (None)
    assert len(results) == 4
    assert results[0].id == "3"
    assert results[1].id == "1"
    assert results[2].id == "4"
    assert results[3].id == "5"

def test_min_rating_drops_nulls():
    prefs = UserPreferences(
        location="Banashankari",
        min_rating=3.0
    )
    results = FilterService.filter(prefs)
    # 3 and 1 match. 4 is 2.5, 5 is None.
    assert len(results) == 2
    assert set([r.id for r in results]) == {"1", "3"}

def test_max_candidates_cap(monkeypatch):
    monkeypatch.setattr(settings, "MAX_CANDIDATES", 2)
    prefs = UserPreferences(location="Bangalore")
    results = FilterService.filter(prefs)
    assert len(results) == 2

def test_no_match_builder():
    prefs = UserPreferences(location="Indiranagar", min_rating=4.5)
    nm = build_no_match(prefs)
    assert len(nm.suggestions) >= 1
    assert nm.filters_applied.location == "Indiranagar"
