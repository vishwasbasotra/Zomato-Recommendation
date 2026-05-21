# Phase 4 Evaluation — REST API & Startup

**Implementation plan:** [Phase 4](../implementationPlan.md#phase-4--rest-api-request-validation--startup)  
**Architecture:** §6.2 (5–12), §6.3, §6.4, §8.2, §10.2, §10.4

## Objective

HTTP API implements full §6.4.3 response table and §6.3 startup lifecycle.

## Prerequisites

- [phase-3-eval.md](./phase-3-eval.md) — **Pass**
- Mock LLM wired for tests (or dependency override)

---

## Evaluation criteria

### P0 — Must pass (architecture §6.4.3)

| # | Condition | HTTP | Automated test |
|---|-----------|------|----------------|
| 4.1 | Invalid body (missing location) | 400 | `test_api` |
| 4.2 | Store not loaded | 503 | `test_api` |
| 4.3 | Zero filter matches | 200 `NoMatchResponse` | `test_api` |
| 4.4 | LLM / provider failure | 502 | Mock `LLMError` |
| 4.5 | Unprocessable LLM after retry | 502 | Mock orchestrator |
| 4.6 | Success | 200 `RecommendationResponse` | Mock fixture |
| 4.7 | `GET /api/v1/health` returns `store_loaded` | 200 | `test_api` |
| 4.8 | Lifespan loads store when Parquet exists | Integration | Start uvicorn |
| 4.9 | `request_id` or correlation in logs | Manual / log assert | |
| 4.10 | OpenAPI `/docs` loads | Manual browser | |

### P1 — Should pass

| # | Criterion | How to verify |
|---|-----------|---------------|
| 4.11 | `min_rating` out of range → 400 | Test |
| 4.12 | curl example from implementation plan works | Copy-paste |
| 4.13 | Concurrent 5 requests without error | Simple load script |
| 4.14 | Long `additional_preferences` handled | Test truncate/400 |

### P2 — Nice to have

| # | Criterion | How to verify |
|---|-----------|---------------|
| 4.15 | `GET /api/v1/cuisines` | Optional route |
| 4.16 | `GET /api/v1/metadata` | Optional route |

---

## Automated checks

```bash
pytest tests/test_api.py -v
uvicorn zomato_cursor.api.main:app --port 8000 &
curl -s http://localhost:8000/api/v1/health
curl -s -X POST http://localhost:8000/api/v1/recommendations -H "Content-Type: application/json" -d "{\"location\":\"Banashankari\",\"budget\":\"medium\",\"cuisine\":\"North Indian\",\"min_rating\":4.0}"
```

---

## Manual checks

- [ ] Startup without Parquet: health shows `store_loaded: false`; POST → 503
- [ ] After ingest + restart: POST → 200
- [ ] Response JSON matches Pydantic models in OpenAPI

---

## Edge cases (this phase)

| ID | Case | Pass? |
|----|------|-------|
| A-01 | Missing location | ☐ |
| A-02 | Bad min_rating | ☐ |
| A-04 | Empty body | ☐ |
| A-06 | Store not loaded | ☐ |
| A-10 | Health reflects store | ☐ |
| A-11 | No-match is 200 | ☐ |
| D-02 | Corrupt Parquet | ☐ |
| C-01 | No .env | ☐ |

---

## Sign-off

| Field | Value |
|-------|-------|
| Evaluator | |
| Date | |
| Result | ☐ Pass ☐ Conditional ☐ Fail |
| Notes | |

**Next phase:** [phase-5-eval.md](./phase-5-eval.md)
