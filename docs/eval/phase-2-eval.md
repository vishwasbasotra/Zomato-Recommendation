# Phase 2 Evaluation — Domain Models & Filtering

**Implementation plan:** [Phase 2](../implementationPlan.md#phase-2--domain-models--filtering-no-llm)  
**Architecture:** §5, §4.2 `FilterService`, §6.2 steps 13–22

## Objective

Deterministic filtering and `NoMatchResponse` without any LLM dependency (architecture §6.2 steps 13–22).

## Prerequisites

- [phase-1-eval.md](./phase-1-eval.md) — **Pass**
- Processed Parquet available

---

## Evaluation criteria

### P0 — Must pass

| # | Criterion | How to verify |
|---|-----------|---------------|
| 2.1 | `Banashankari` + `North Indian` + `medium` + `min_rating=4.0` returns non-empty list | Script / test |
| 2.2 | Impossible filter combo returns `NoMatchResponse` (not exception) | Unit test |
| 2.3 | No-match path includes ≥2 actionable suggestions | Inspect response object |
| 2.4 | Every returned row satisfies all applied hard filters | Property test or assert |
| 2.5 | Result count ≤ `MAX_CANDIDATES` (default 25) | Test with broad location |
| 2.6 | Sort order: higher `rating` before lower; tie-break `votes` | Unit test |
| 2.7 | `pytest tests/test_filter_service.py` passes | CI / local |
| 2.8 | Pydantic models validate `UserPreferences` (location required) | Model test |

### P1 — Should pass

| # | Criterion | How to verify |
|---|-----------|---------------|
| 2.9 | Location-only query returns capped broad set | Test |
| 2.10 | Case-insensitive cuisine match | Test `"north indian"` |
| 2.11 | `filter_demo.py` runs (if implemented) | Manual |

### P2 — Nice to have

| # | Criterion | How to verify |
|---|-----------|---------------|
| 2.12 | Location alias table | Deferred documented |

---

## Automated checks

```bash
pytest tests/test_filter_service.py tests/test_preprocessor.py -v
```

---

## Manual checks

- [ ] Print top 3 candidates for demo prefs; fields look correct
- [ ] Confirm **no** LLM client imported in filter-only code path

---

## Edge cases (this phase)

| ID | Case | Pass? |
|----|------|-------|
| F-01 | Zero matches → NoMatch, no LLM | ☐ |
| F-03 | City-level location | ☐ |
| F-04 | Locality location | ☐ |
| F-07 | Null rating + min_rating | ☐ |
| F-08 | Null budget_band + budget filter | ☐ |
| F-09 | Cuisine case insensitivity | ☐ |
| F-11 | Cap at MAX_CANDIDATES | ☐ |
| F-12 | Single match | ☐ |
| F-13 | Location only | ☐ |
| F-15 | additional_preferences ignored by filter | ☐ |

---

## Sign-off

| Field | Value |
|-------|-------|
| Evaluator | |
| Date | |
| Result | ☐ Pass ☐ Conditional ☐ Fail |
| Notes | |

**Next phase:** [phase-3-eval.md](./phase-3-eval.md)
