"""User preferences model."""

from typing import Literal, Optional
from pydantic import BaseModel, Field

class UserPreferences(BaseModel):
    location: str = Field(..., description="City or locality")
    budget: Optional[Literal["low", "medium", "high"]] = None
    cuisine: Optional[str] = None
    min_rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    additional_preferences: Optional[str] = None
    top_k: int = Field(5, ge=1)
