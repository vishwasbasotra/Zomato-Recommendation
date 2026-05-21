"""Canonical restaurant model."""

from typing import Optional
from pydantic import BaseModel

class Restaurant(BaseModel):
    id: str
    name: str
    city: str
    location: str
    address: str
    cuisines: list[str]
    rating: Optional[float] = None
    votes: int
    cost_for_two: Optional[int] = None
    budget_band: Optional[str] = None
    rest_type: str
    dish_liked: str
    online_order: bool
    book_table: bool
    url: str
    review_snippet: Optional[str] = None
