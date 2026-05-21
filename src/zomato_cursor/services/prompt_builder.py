"""Builds prompts for the LLM."""

import json
from typing import List
from zomato_cursor.models.preferences import UserPreferences
from zomato_cursor.models.restaurant import Restaurant

class PromptBuilder:
    @staticmethod
    def build(candidates: List[Restaurant], prefs: UserPreferences) -> str:
        candidates_json = []
        for c in candidates:
            candidates_json.append({
                "id": c.id,
                "name": c.name,
                "cuisines": c.cuisines,
                "rating": c.rating,
                "cost_for_two": c.cost_for_two,
                "location": c.location,
                "votes": c.votes,
                "snippet": c.review_snippet
            })
            
        prompt = f"""You are a restaurant recommendation assistant for Indian cities.
Rules: (1) Only recommend restaurants from the provided candidate list. (2) Do not invent names, ratings, or prices. (3) If none fit well, say so honestly and rank the best available matches. (4) Output valid JSON only, using the exact schema below. Do not use markdown fences (```json).

JSON Output Schema:
{{
  "summary": "One short paragraph overview.",
  "recommendations": [
    {{
      "restaurant_id": "string — must exactly match a candidate id",
      "rank": 1,
      "explanation": "Why this fits the user's stated preferences.",
      "match_highlights": ["highlight 1", "highlight 2"]
    }}
  ]
}}

USER CONTEXT:
Location: {prefs.location}
Budget: {prefs.budget or 'Any'}
Cuisine: {prefs.cuisine or 'Any'}
Min Rating: {prefs.min_rating or 'Any'}
Additional Notes: {prefs.additional_preferences or 'None'}
Rank top {prefs.top_k} recommendations.

CANDIDATE RESTAURANTS:
{json.dumps(candidates_json, indent=2)}
"""
        return prompt

    @staticmethod
    def repair_prompt(raw_response: str, validation_errors: str) -> str:
        """Create a repair prompt when validation fails."""
        return f"""The previous JSON response was invalid or contained hallucinated restaurant IDs.
Please fix the JSON and return ONLY valid JSON matching the schema, and strictly use the provided candidate IDs.

Errors:
{validation_errors}

Previous output:
{raw_response}
"""
