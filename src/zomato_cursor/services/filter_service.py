"""Service for applying deterministic hard filters to restaurants."""

from typing import List
import pandas as pd

from zomato_cursor.config import settings
from zomato_cursor.data.store import store
from zomato_cursor.models.preferences import UserPreferences
from zomato_cursor.models.restaurant import Restaurant

class FilterService:
    @staticmethod
    def filter(prefs: UserPreferences) -> List[Restaurant]:
        """Apply hard constraints and return up to MAX_CANDIDATES."""
        store.assert_loaded()
        df = store.df
        
        # Location filter (case-insensitive substring match on city OR location)
        loc = prefs.location.lower().strip()
        mask_loc = df["city"].str.contains(loc, case=False, na=False) | df["location"].str.contains(loc, case=False, na=False)
        
        mask_all = mask_loc
        
        # Minimum rating filter
        if prefs.min_rating is not None:
            mask_rating = df["rating"].notna() & (df["rating"] >= prefs.min_rating)
            mask_all = mask_all & mask_rating
            
        # Budget band filter
        if prefs.budget:
            mask_budget = df["budget_band"] == prefs.budget
            mask_all = mask_all & mask_budget
            
        # Cuisine filter (any token match, case-insensitive)
        if prefs.cuisine:
            c_target = prefs.cuisine.lower().strip()
            mask_cuisine = df["cuisines"].apply(
                lambda c_list: any(c_target in str(c).lower() for c in c_list) if hasattr(c_list, '__iter__') and not isinstance(c_list, str) else False
            )
            mask_all = mask_all & mask_cuisine
            
        subset = df[mask_all].copy()
        
        if subset.empty:
            return []
            
        # Sort by rating DESC, votes DESC
        # na_position="last" ensures missing ratings sort to the bottom
        subset = subset.sort_values(by=["rating", "votes"], ascending=[False, False], na_position="last")
        
        # Cap candidates
        subset = subset.head(settings.MAX_CANDIDATES)
        
        # Convert to list of Restaurant models
        records = subset.to_dict(orient="records")
        return [Restaurant(**r) for r in records]
