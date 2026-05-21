"""Tests for the orchestrator."""

import json
import pytest
import pandas as pd

from zomato_cursor.models.preferences import UserPreferences
from zomato_cursor.models.response import RecommendationResponse, NoMatchResponse, ErrorResponse
from zomato_cursor.services.orchestrator import recommend
from zomato_cursor.services.llm_client import LLMError
from zomato_cursor.data.store import store

@pytest.fixture(autouse=True)
def mock_store():
    df = pd.DataFrame([
        {
            "id": "1", "name": "Fancy Indian", "city": "bangalore", "location": "banashankari",
            "address": "", "cuisines": ["North Indian", "Mughlai"], "rating": 4.5, "votes": 100,
            "cost_for_two": 600, "budget_band": "medium", "rest_type": "Casual",
            "dish_liked": "", "online_order": True, "book_table": True, "url": "", "review_snippet": ""
        }
    ])
    store.df = df
    yield
    store.df = None

class MockLLMClient:
    def __init__(self, response_text, raise_err=False):
        self.response_text = response_text
        self.raise_err = raise_err
        self.call_count = 0
        
    def complete(self, prompt: str) -> str:
        self.call_count += 1
        if self.raise_err:
            raise LLMError("Mock Error", retryable=True)
        return self.response_text

def test_orchestrator_success():
    prefs = UserPreferences(location="Banashankari", top_k=5)
    mock_resp = json.dumps({
        "summary": "Sum",
        "recommendations": [{"restaurant_id": "1", "rank": 1, "explanation": "exp"}]
    })
    client = MockLLMClient(mock_resp)
    
    resp = recommend(prefs, llm_client=client)
    assert isinstance(resp, RecommendationResponse)
    assert resp.meta["candidate_count"] == 1
    assert len(resp.recommendations) == 1
    assert resp.recommendations[0].id == "1"
    assert resp.recommendations[0].rank == 1

def test_orchestrator_no_match():
    prefs = UserPreferences(location="Delhi", top_k=5)
    client = MockLLMClient("")
    resp = recommend(prefs, llm_client=client)
    assert isinstance(resp, NoMatchResponse)
    assert client.call_count == 0

def test_orchestrator_repair():
    prefs = UserPreferences(location="Banashankari", top_k=5)
    
    class RepairMockClient:
        def __init__(self):
            self.call_count = 0
        def complete(self, prompt: str) -> str:
            self.call_count += 1
            if self.call_count == 1:
                return "Not json"
            return json.dumps({
                "summary": "Sum",
                "recommendations": [{"restaurant_id": "1", "rank": 1, "explanation": "exp"}]
            })

    client = RepairMockClient()
    resp = recommend(prefs, llm_client=client)
    assert isinstance(resp, RecommendationResponse)
    assert client.call_count == 2
    assert len(resp.recommendations) == 1

def test_orchestrator_llm_error():
    prefs = UserPreferences(location="Banashankari", top_k=5)
    client = MockLLMClient("", raise_err=True)
    
    resp = recommend(prefs, llm_client=client)
    assert isinstance(resp, ErrorResponse)
    assert resp.code == "LLM_FAILURE"
