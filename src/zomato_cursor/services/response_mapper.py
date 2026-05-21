"""Maps validated LLM rankings to final DTOs."""

from typing import List, Dict, Any

from zomato_cursor.models.preferences import UserPreferences
from zomato_cursor.models.restaurant import Restaurant
from zomato_cursor.models.response import RecommendationResponse, FilterSummary, RankedRestaurant
from zomato_cursor.config import settings

class ResponseMapper:
    @staticmethod
    def to_dto(
        validated_rankings: List[Dict[str, Any]],
        candidates: List[Restaurant],
        prefs: UserPreferences,
        summary: str,
        latency_ms: int
    ) -> RecommendationResponse:
        
        # Build map for fast lookup
        cand_map = {c.id: c for c in candidates}
        
        ranked_restaurants = []
        for i, rank_data in enumerate(validated_rankings):
            rid = str(rank_data.get("restaurant_id"))
            cand = cand_map[rid]
            
            # Map into RankedRestaurant
            ranked = RankedRestaurant(
                **cand.model_dump(),
                rank=i + 1,
                explanation=rank_data.get("explanation", ""),
                match_highlights=rank_data.get("match_highlights", [])
            )
            ranked_restaurants.append(ranked)
            
        filter_summary = FilterSummary(
            location=prefs.location,
            budget=prefs.budget,
            cuisine=prefs.cuisine,
            min_rating=prefs.min_rating,
            candidates_found=len(candidates)
        )
        
        meta = {
            "candidate_count": len(candidates),
            "llm_model": settings.LLM_MODEL,
            "latency_ms": latency_ms
        }
        
        return RecommendationResponse(
            summary=summary if summary else None,
            filters_applied=filter_summary,
            recommendations=ranked_restaurants,
            meta=meta
        )
