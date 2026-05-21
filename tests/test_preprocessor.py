"""Tests for preprocessing logic."""

from zomato_cursor.data.preprocessor import parse_rate, parse_cost, get_budget_band, parse_cuisines, parse_boolean

def test_parse_rate():
    assert parse_rate("4.1/5") == 4.1
    assert parse_rate("NEW") is None
    assert parse_rate("-") is None
    assert parse_rate(None) is None
    assert parse_rate("  4.5 /5 ") == 4.5
    assert parse_rate(float('nan')) is None

def test_parse_cost():
    assert parse_cost("800") == 800
    assert parse_cost("1,200") == 1200
    assert parse_cost("---") is None
    assert parse_cost(None) is None

def test_get_budget_band():
    assert get_budget_band(300) == "low"
    assert get_budget_band(400) == "low"
    assert get_budget_band(500) == "medium"
    assert get_budget_band(800) == "medium"
    assert get_budget_band(1000) == "high"
    assert get_budget_band(None) is None

def test_parse_cuisines():
    assert parse_cuisines("North Indian, Chinese") == ["North Indian", "Chinese"]
    assert parse_cuisines(None) == []
    assert parse_cuisines("  Cafe  ") == ["Cafe"]

def test_parse_boolean():
    assert parse_boolean("Yes") is True
    assert parse_boolean("No") is False
    assert parse_boolean("yes ") is True
    assert parse_boolean(None) is False
