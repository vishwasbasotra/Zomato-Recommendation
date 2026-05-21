"""API response models."""

from typing import Optional, Any
from pydantic import BaseModel
from zomato_cursor.models.restaurant import Restaurant

class FilterSummary(BaseModel):
    location: str
    budget: Optional[str] = None
    cuisine: Optional[str] = None
    min_rating: Optional[float] = None
    candidates_found: int

class NoMatchResponse(BaseModel):
    message: str
    suggestions: list[str]
    filters_applied: FilterSummary

class ErrorResponse(BaseModel):
    code: str
    message: str
    retryable: bool

class RankedRestaurant(Restaurant):
    rank: int
    explanation: str
    match_highlights: Optional[list[str]] = None

class RecommendationResponse(BaseModel):
    summary: Optional[str] = None
    filters_applied: FilterSummary
    recommendations: list[RankedRestaurant]
    meta: dict[str, Any]
