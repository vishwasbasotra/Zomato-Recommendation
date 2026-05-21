"""Quick script to manually test filtering against real dataset."""

from zomato_cursor.config import settings
from zomato_cursor.data.store import store
from zomato_cursor.models.preferences import UserPreferences
from zomato_cursor.services.filter_service import FilterService
from zomato_cursor.services.no_match_builder import build_no_match

def main():
    store.load(settings.DATA_PATH)
    
    prefs = UserPreferences(
        location="Banashankari",
        cuisine="North Indian",
        budget="medium",
        min_rating=4.0
    )
    
    print("Testing preferences:", prefs.model_dump())
    
    candidates = FilterService.filter(prefs)
    if not candidates:
        print("\nNo match found!")
        no_match = build_no_match(prefs)
        print("Message:", no_match.message)
        print("Suggestions:", no_match.suggestions)
        return
        
    print(f"\nFound {len(candidates)} candidates.")
    print("Top 3:")
    for c in candidates[:3]:
        print(f"- {c.name} (Rating: {c.rating}, Budget: {c.budget_band})")

if __name__ == "__main__":
    main()
