"""Tests for the OutputValidator."""

import json
from zomato_cursor.models.restaurant import Restaurant
from zomato_cursor.services.output_validator import OutputValidator

def test_valid_json():
    candidates = [Restaurant(id="1", name="A", city="C", location="L", address="", cuisines=[], votes=0, rest_type="", dish_liked="", online_order=False, book_table=False, url="")]
    raw = json.dumps({
        "summary": "Sum",
        "recommendations": [{"restaurant_id": "1", "rank": 1, "explanation": "exp"}]
    })
    
    valid, summary, err = OutputValidator.validate(raw, candidates, 5)
    assert not err
    assert len(valid) == 1
    assert valid[0]["restaurant_id"] == "1"

def test_hallucinated_id():
    candidates = [Restaurant(id="1", name="A", city="C", location="L", address="", cuisines=[], votes=0, rest_type="", dish_liked="", online_order=False, book_table=False, url="")]
    raw = json.dumps({
        "summary": "Sum",
        "recommendations": [{"restaurant_id": "999", "rank": 1, "explanation": "exp"}]
    })
    
    valid, summary, err = OutputValidator.validate(raw, candidates, 5)
    assert len(valid) == 0
    assert err == "No valid grounded restaurant IDs found in output."

def test_markdown_fences():
    candidates = [Restaurant(id="1", name="A", city="C", location="L", address="", cuisines=[], votes=0, rest_type="", dish_liked="", online_order=False, book_table=False, url="")]
    raw = "```json\n" + json.dumps({
        "summary": "Sum",
        "recommendations": [{"restaurant_id": "1", "rank": 1, "explanation": "exp"}]
    }) + "\n```"
    
    valid, summary, err = OutputValidator.validate(raw, candidates, 5)
    assert not err
    assert len(valid) == 1

def test_invalid_json():
    candidates = []
    raw = "Hello world this is not json"
    valid, summary, err = OutputValidator.validate(raw, candidates, 5)
    assert len(valid) == 0
    assert "Invalid JSON" in err

def test_top_k():
    candidates = [
        Restaurant(id="1", name="A", city="C", location="L", address="", cuisines=[], votes=0, rest_type="", dish_liked="", online_order=False, book_table=False, url=""),
        Restaurant(id="2", name="B", city="C", location="L", address="", cuisines=[], votes=0, rest_type="", dish_liked="", online_order=False, book_table=False, url="")
    ]
    raw = json.dumps({
        "summary": "Sum",
        "recommendations": [
            {"restaurant_id": "1", "rank": 1, "explanation": "exp"},
            {"restaurant_id": "2", "rank": 2, "explanation": "exp"}
        ]
    })
    
    valid, summary, err = OutputValidator.validate(raw, candidates, 1)
    assert not err
    assert len(valid) == 1
    assert valid[0]["restaurant_id"] == "1"
