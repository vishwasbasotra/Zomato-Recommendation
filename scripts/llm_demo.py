"""Demo script for Phase 3 LLM integration."""

from zomato_cursor.config import settings
from zomato_cursor.data.store import store
from zomato_cursor.models.preferences import UserPreferences
from zomato_cursor.services.orchestrator import recommend

def main():
    print(f"Loading data from {settings.DATA_PATH}...")
    store.load(settings.DATA_PATH)
    
    prefs = UserPreferences(
        location="Banashankari",
        cuisine="North Indian",
        budget="medium",
        min_rating=4.0,
        additional_preferences="I want a place with a quiet ambiance if possible.",
        top_k=2
    )
    
    print("\nRequesting recommendations for:")
    print(prefs.model_dump())
    print(f"\nUsing Model: {settings.LLM_MODEL}")
    print("Calling LLM (this may take a few seconds)...")
    
    resp = recommend(prefs)
    
    print("\n--- RESULTS ---")
    if hasattr(resp, "recommendations"):
        print(f"Summary: {resp.summary}")
        print(f"Latency: {resp.meta['latency_ms']}ms")
        print(f"Candidates processed: {resp.meta['candidate_count']}")
        print()
        for r in resp.recommendations:
            print(f"#{r.rank} {r.name} (Rating: {r.rating})")
            print(f"Explanation: {r.explanation}")
            print(f"Highlights: {r.match_highlights}")
            print()
    else:
        print(f"Response: {resp}")

if __name__ == "__main__":
    main()
