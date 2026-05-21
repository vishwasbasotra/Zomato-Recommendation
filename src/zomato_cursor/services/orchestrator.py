"""Coordinates recommendation flow."""

import time
from typing import Union
from zomato_cursor.config import settings
from zomato_cursor.models.preferences import UserPreferences
from zomato_cursor.models.response import RecommendationResponse, NoMatchResponse, ErrorResponse
from zomato_cursor.services.filter_service import FilterService
from zomato_cursor.services.no_match_builder import build_no_match
from zomato_cursor.services.prompt_builder import PromptBuilder
from zomato_cursor.services.llm_client import LLMClient, LLMError
from zomato_cursor.services.output_validator import OutputValidator
from zomato_cursor.services.response_mapper import ResponseMapper

def recommend(prefs: UserPreferences, llm_client=None) -> Union[RecommendationResponse, NoMatchResponse, ErrorResponse]:
    candidates = FilterService.filter(prefs)
    if not candidates:
        return build_no_match(prefs)
        
    prompt = PromptBuilder.build(candidates, prefs)
    
    client = llm_client if llm_client else LLMClient()
    t0 = time.time()
    
    try:
        raw = client.complete(prompt)
    except LLMError as e:
        return ErrorResponse(code="LLM_FAILURE", message=str(e), retryable=e.retryable)
        
    valid_rankings, summary, err = OutputValidator.validate(raw, candidates, prefs.top_k)
    
    if err and settings.LLM_MAX_RETRIES > 0 and len(valid_rankings) == 0:
        repair = PromptBuilder.repair_prompt(raw, err)
        try:
            raw = client.complete(repair)
        except LLMError as e:
            return ErrorResponse(code="LLM_FAILURE", message=str(e), retryable=e.retryable)
            
        valid_rankings, summary, err = OutputValidator.validate(raw, candidates, prefs.top_k)
        
    if not valid_rankings:
        return ErrorResponse(code="VALIDATION_FAILURE", message=str(err), retryable=False)
        
    latency = int((time.time() - t0) * 1000)
    
    return ResponseMapper.to_dto(valid_rankings, candidates, prefs, summary, latency)
