"""Preprocess raw restaurant dataset into a canonical schema."""

import hashlib
import pandas as pd
from typing import Optional
from zomato_cursor.config import settings

def parse_rate(rate_str: str) -> Optional[float]:
    """Parse '4.1/5' or 'NEW' or '-' into float or None."""
    if pd.isna(rate_str) or not isinstance(rate_str, str):
        return None
    rate_str = rate_str.strip().upper()
    if rate_str in ("NEW", "-", ""):
        return None
    try:
        # e.g., "4.1/5"
        val = rate_str.split('/')[0].strip()
        return float(val)
    except ValueError:
        return None

def parse_cost(cost_str: str) -> Optional[int]:
    """Parse '800' or '1,200' into integer."""
    if pd.isna(cost_str) or not isinstance(cost_str, str):
        return None
    cost_str = cost_str.strip().replace(",", "")
    try:
        return int(cost_str)
    except ValueError:
        return None

def get_budget_band(cost: Optional[int]) -> Optional[str]:
    """Map cost to 'low', 'medium', or 'high' based on config."""
    if cost is None:
        return None
    if cost <= settings.BUDGET_LOW_MAX:
        return "low"
    elif cost <= settings.BUDGET_MEDIUM_MAX:
        return "medium"
    return "high"

def parse_boolean(val: str) -> bool:
    """Parse 'Yes'/'No' to boolean."""
    if pd.isna(val) or not isinstance(val, str):
        return False
    return val.strip().lower() == "yes"

def parse_cuisines(cuisine_str: str) -> list[str]:
    """Parse 'North Indian, Mughlai, Chinese' into list."""
    if pd.isna(cuisine_str) or not isinstance(cuisine_str, str):
        return []
    return [c.strip() for c in cuisine_str.split(",") if c.strip()]

def generate_id(url: str, index: int) -> str:
    """Generate a stable id from url or fallback to index."""
    if pd.isna(url) or not isinstance(url, str):
        return f"idx_{index}"
    return hashlib.md5(url.strip().encode("utf-8")).hexdigest()

def truncate_review(review_list_str: str) -> Optional[str]:
    """Truncate the reviews_list to MAX_REVIEW_CHARS."""
    if pd.isna(review_list_str) or not isinstance(review_list_str, str):
        return None
    return review_list_str[:settings.MAX_REVIEW_CHARS]

def preprocess_dataset(hf_dataset) -> pd.DataFrame:
    """Convert Hugging Face dataset to canonical pandas DataFrame."""
    df = hf_dataset.to_pandas()
    
    # 1. Drop rows with null name
    df = df.dropna(subset=["name"])
    
    # 2. Extract and transform columns
    canonical = []
    
    for i, row in df.iterrows():
        cost = parse_cost(row.get("approx_cost(for two people)"))
        
        canonical.append({
            "id": generate_id(row.get("url"), i),
            "name": str(row["name"]).strip(),
            "city": str(row.get("listed_in(city)", "")).strip().lower(),
            "location": str(row.get("location", "")).strip().lower(),
            "address": str(row.get("address", "")).strip(),
            "cuisines": parse_cuisines(row.get("cuisines")),
            "rating": parse_rate(row.get("rate")),
            "votes": int(row.get("votes", 0)) if pd.notna(row.get("votes")) else 0,
            "cost_for_two": cost,
            "budget_band": get_budget_band(cost),
            "rest_type": str(row.get("rest_type", "")).strip(),
            "dish_liked": str(row.get("dish_liked", "")).strip() if pd.notna(row.get("dish_liked")) else "",
            "online_order": parse_boolean(row.get("online_order")),
            "book_table": parse_boolean(row.get("book_table")),
            "url": str(row.get("url", "")).strip(),
            "review_snippet": truncate_review(row.get("reviews_list"))
        })
        
    return pd.DataFrame(canonical)
