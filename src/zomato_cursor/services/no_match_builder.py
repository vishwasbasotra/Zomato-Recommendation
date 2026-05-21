"""Builder for generating NoMatchResponse."""

from zomato_cursor.models.preferences import UserPreferences
from zomato_cursor.models.response import NoMatchResponse, FilterSummary

def build_no_match(prefs: UserPreferences) -> NoMatchResponse:
    """Generate a NoMatchResponse based on the provided user preferences."""
    suggestions = []
    
    if prefs.min_rating is not None and prefs.min_rating > 3.0:
        suggestions.append(f"Try lowering the minimum rating from {prefs.min_rating}.")
        
    if prefs.budget:
        suggestions.append(f"Consider broadening your budget preference (currently set to '{prefs.budget}').")
        
    if prefs.cuisine:
        suggestions.append(f"There might not be many '{prefs.cuisine}' places in {prefs.location}. Try a different cuisine.")
        
    suggestions.append(f"Expand the search location beyond '{prefs.location}'.")
    
    suggestions = suggestions[:3]

    summary = FilterSummary(
        location=prefs.location,
        budget=prefs.budget,
        cuisine=prefs.cuisine,
        min_rating=prefs.min_rating,
        candidates_found=0
    )
    
    return NoMatchResponse(
        message="We couldn't find any restaurants matching all your criteria.",
        suggestions=suggestions,
        filters_applied=summary
    )
