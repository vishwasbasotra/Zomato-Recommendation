"""Validates LLM output against candidate IDs and JSON constraints."""

import json
from typing import List, Dict, Any, Tuple, Optional
from zomato_cursor.models.restaurant import Restaurant

class OutputValidator:
    @staticmethod
    def validate(raw_response: str, candidates: List[Restaurant], top_k: int) -> Tuple[List[Dict[str, Any]], str, Optional[str]]:
        """
        Parses JSON, grounds IDs, enforces top_k.
        Returns:
            (valid_rankings, summary_text, validation_error_message).
            If validation_error_message is not None, there were fatal/repairable errors.
        """
        text = raw_response.strip()
        
        # Strip markdown fences if present
        if text.startswith("```"):
            lines = text.split("\n")
            if len(lines) >= 2:
                # Find start
                if lines[0].startswith("```"):
                    lines = lines[1:]
                # Find end
                if lines[-1].strip() == "```":
                    lines = lines[:-1]
                text = "\n".join(lines).strip()

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            return [], "", f"Invalid JSON: {str(e)}"
            
        if not isinstance(data, dict):
            return [], "", "Root must be a JSON object"
            
        recs = data.get("recommendations", [])
        if not isinstance(recs, list):
            return [], "", "'recommendations' must be a list"
            
        summary = data.get("summary", "")
        
        candidate_ids = {c.id for c in candidates}
        valid_recs = []
        
        for r in recs:
            rid = str(r.get("restaurant_id", ""))
            if rid in candidate_ids:
                valid_recs.append(r)
                
        if not valid_recs:
            return [], "", "No valid grounded restaurant IDs found in output."
            
        # Return warning if some hallucinated IDs were stripped
        err = None
        if len(valid_recs) < len(recs):
            err = "Some hallucinated IDs were stripped."
            
        # Enforce top_k
        valid_recs = valid_recs[:top_k]
        
        return valid_recs, summary, err
