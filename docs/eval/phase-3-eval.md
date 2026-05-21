# Phase 3 Evaluation — LLM Pipeline (Orchestrator)

**Implementation plan:** [Phase 3](../implementationPlan.md#phase-3--llm-pipeline-orchestrator-core)  
**Architecture:** §6.2 steps 23–48, §6.4.2, §6.5, §6.6, §9

## Objective

End-to-end `recommend()` via filter → prompt → LLM → validate → map, testable without HTTP.

## Prerequisites

- [phase-2-eval.md](./phase-2-eval.md) — **Pass**
- Mock LLM fixture in `tests/fixtures/`
- Optional: valid `LLM_API_KEY` for integration test

---

## Evaluation criteria

### P0 — Must pass

| # | Criterion | How to verify |
|---|-----------|---------------|
| 3.1 | Mock LLM → `RecommendationResponse` with `rank`, `explanation` | `test_orchestrator.py` |
| 3.2 | Filter empty → `NoMatchResponse`; mock LLM **not** called | Test spy / assert |
| 3.3 | Hallucinated `restaurant_id` stripped or repair invoked | `test_validator.py` + fixture |
| 3.4 | After strip, ≥1 valid id → partial success (not 502 at orchestrator level) | Test §6.4.2 |
| 3.5 | Invalid JSON → repair once → success or `ErrorResponse` | Test |
| 3.6 | `top_k` enforced in output | Test |
| 3.7 | `ResponseMapper` fills name, rating, cost from store | Inspect DTO |
| 3.8 | `meta` includes `candidate_count`, `llm_model`, `latency_ms` | Assert fields |
| 3.9 | `LLMError` raised on mock provider failure | Test |
| 3.10 | `pytest` passes without network (mock only) | `pytest -m "not integration"` |

### P1 — Should pass

| # | Criterion | How to verify |
|---|-----------|---------------|
| 3.11 | Markdown JSON fences parsed | Validator test |
| 3.12 | `repair_prompt` second call on empty validate | Test |
| 3.13 | Live integration: Banashankari prefs grounded | `@pytest.mark.integration` manual |
| 3.14 | Explanations mention user location or free text | Manual read one response |

### P2 — Nice to have

| # | Criterion | How to verify |
|---|-----------|---------------|
| 3.15 | Token trimming when many candidates | Log prompt size |
| 3.16 | Ollama / second provider adapter | Config switch |

---

## Automated checks

```bash
pytest tests/test_validator.py tests/test_orchestrator.py -v
pytest -m integration   # optional, requires API key
```

---

## Manual checks

```bash
python -c "
from zomato_cursor.models.preferences import UserPreferences
from zomato_cursor.services.orchestrator import recommend
prefs = UserPreferences(location='Banashankari', cuisine='North Indian', budget='medium', min_rating=4.0, top_k=5)
print(recommend(prefs))
"
```

- [ ] All `restaurant_id` in output exist in dataset
- [ ] No restaurant name in output that was not in candidate list

---

## Edge cases (this phase)

| ID | Case | Pass? |
|----|------|-------|
| L-01 | Valid grounded JSON | ☐ |
| L-02 | Hallucinated id stripped | ☐ |
| L-03 | All ids bad → repair | ☐ |
| L-04 | Markdown fences | ☐ |
| L-05 | Malformed JSON → 502 path | ☐ |
| L-08 | top_k truncate | ☐ |
| L-09 | Fewer than top_k results | ☐ |
| L-11 | Timeout → LLMError | ☐ |
| L-12 | Missing API key | ☐ |
| L-14 | Single candidate | ☐ |
| L-17 | Repair succeeds | ☐ |
| L-18 | Repair fails | ☐ |

---

## Sign-off

| Field | Value |
|-------|-------|
| Evaluator | |
| Date | |
| Result | ☐ Pass ☐ Conditional ☐ Fail |
| Notes | |

**Next phase:** [phase-4-eval.md](./phase-4-eval.md)
