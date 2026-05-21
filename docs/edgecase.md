# Zomato-Cursor — Edge Cases & Expected Behavior

Catalog of **edge cases** for the restaurant recommendation system. Each entry defines the trigger, expected behavior, owning phase, and how to verify. Derived from [architecture.md](./architecture.md) (especially §6.4) and [implementationPlan.md](./implementationPlan.md).

**Severity**

| Level | Meaning |
|-------|---------|
| **P0** | Must handle correctly for phase sign-off |
| **P1** | Should handle; document if deferred |
| **P2** | Known limitation; acceptable for v1 portfolio |

---

## How to use this document

- During implementation: implement handling for **P0** cases in the phase listed under **Owner**.
- During phase eval: run cases tagged with that phase in the matching [eval/phase-N-eval.md](./eval/README.md) file.
- After Phase 6: full regression against **Integration** cases.

---

## 1. Data ingestion & preprocessing (Phase 1)

| ID | Edge case | Expected behavior | Owner | Severity |
|----|-----------|-------------------|-------|----------|
| D-01 | Hugging Face download fails (network, 503) | Ingest exits non-zero; clear error; suggest retry or use cached `data/processed/` if present | 1 | P0 |
| D-02 | Empty or corrupt Parquet on load | `RestaurantStore.is_loaded()` false; API returns 503 (§6.4.1) | 1, 4 | P0 |
| D-03 | `rate` missing or `"NEW"` / non-numeric | `rating` = null; row kept; excluded when `min_rating` filter applied | 1, 2 | P0 |
| D-04 | `rate` format `4.1/5` | Parsed to `4.1` float | 1 | P0 |
| D-05 | `approx_cost` missing or `"---"` | `cost_for_two` null; `budget_band` null; row excluded when budget filter applied | 1, 2 | P0 |
| D-06 | `approx_cost` at band boundary (400, 800 ₹) | Consistent band per config thresholds (document inclusive/exclusive rules in code) | 1 | P1 |
| D-07 | Duplicate `name` in same locality | Stable distinct `id` (hash of `url`); both rows can appear in candidates | 1 | P1 |
| D-08 | `name` is null | Row dropped at ingest | 1 | P0 |
| D-09 | `cuisines` empty or single token | Empty list or one-item list; cuisine filter excludes row | 1, 2 | P0 |
| D-10 | `reviews_list` very long (MB-scale) | Truncated to `MAX_REVIEW_CHARS` in `review_snippet` | 1, 3 | P0 |
| D-11 | Re-run ingest while API is running | Idempotent overwrite; API may need restart to reload (document in README) | 1, 6 | P1 |
| D-12 | `listed_in(city)` / `location` inconsistent casing | Normalized lowercase for matching; user input case-insensitive | 1, 2 | P0 |
| D-13 | Offline ingest when Parquet already exists | Skip HF download or optional `--force` flag | 1 | P2 |

---

## 2. Filtering & preferences (Phase 2)

| ID | Edge case | Expected behavior | Owner | Severity |
|----|-----------|-------------------|-------|----------|
| F-01 | Zero rows match all filters | `NoMatchResponse` with suggestions; **no LLM call** (§6.2 steps 19–22) | 2, 3 | P0 |
| F-02 | Location typo (`Banashankri`) | No match or partial match depending on substring rules; no crash | 2 | P1 |
| F-03 | Location matches `city` only (e.g. `Bangalore`) | All rows in that city eligible | 2 | P0 |
| F-04 | Location matches `location` only (e.g. `Banashankari`) | Subset in neighborhood | 2 | P0 |
| F-05 | Only `min_rating` set, no other filters | All rows with `rating >= min_rating` (and non-null rating) | 2 | P0 |
| F-06 | `min_rating` = 5.0 | Only perfect-rated rows; likely small set or no-match | 2 | P1 |
| F-07 | `min_rating` on rows with null rating | Those rows excluded | 2 | P0 |
| F-08 | Budget filter when `budget_band` is null | Row excluded from budget-filtered results | 2 | P0 |
| F-09 | Cuisine `"north indian"` vs dataset `"North Indian"` | Case-insensitive / normalized match | 2 | P0 |
| F-10 | Multi-cuisine restaurant; user asks one cuisine | Match if any cuisine token matches | 2 | P0 |
| F-11 | More than `MAX_CANDIDATES` matches | Return top N by rating, then votes | 2 | P0 |
| F-12 | Exactly one match | Single candidate passed to LLM (phase 3) | 2, 3 | P0 |
| F-13 | All optional filters omitted (location only) | Broad candidate set capped at N | 2 | P0 |
| F-14 | Whitespace-only `location` | Treated as invalid → 400 at API (phase 4) | 2, 4 | P0 |
| F-15 | `additional_preferences` only (no structured cuisine) | Passed to LLM only; does not affect hard filter | 2, 3 | P0 |

---

## 3. LLM pipeline (Phase 3)

| ID | Edge case | Expected behavior | Owner | Severity |
|----|-----------|-------------------|-------|----------|
| L-01 | LLM returns valid JSON, all ids grounded | Full `RecommendationResponse` up to `top_k` | 3 | P0 |
| L-02 | LLM invents `restaurant_id` not in candidates | Strip invalid entries; log warning (§6.4.2) | 3 | P0 |
| L-03 | All ids hallucinated after strip | Trigger `repair_prompt` if retry_budget > 0 | 3 | P0 |
| L-04 | JSON wrapped in markdown fences ` ```json ` | Parser strips fences before validate | 3 | P0 |
| L-05 | Malformed JSON (truncated, prose only) | Repair retry; then `ErrorResponse` / 502 | 3, 4 | P0 |
| L-06 | Valid JSON but missing required fields | Repair or partial accept per validator rules | 3 | P1 |
| L-07 | Duplicate ranks or gaps in rank numbers | Normalized to 1..k or re-sorted by rank field | 3 | P1 |
| L-08 | More recommendations than `top_k` | Truncate to `top_k` | 3 | P0 |
| L-09 | Fewer recommendations than `top_k` | Return fewer; no padding with fake venues | 3 | P0 |
| L-10 | `summary` field empty or omitted | Response still valid; UI hides or shows placeholder | 3, 5 | P1 |
| L-11 | LLM API timeout | `LLMError` → 502 retryable (§6.4.3) | 3, 4 | P0 |
| L-12 | Invalid / missing `LLM_API_KEY` | 502 with clear message; no stack trace to client | 3, 4 | P0 |
| L-13 | Rate limit (429) from provider | 502 retryable; optional backoff in client | 3 | P1 |
| L-14 | Candidate list = 1 restaurant | LLM still returns rank 1 + explanation | 3 | P0 |
| L-15 | `additional_preferences` contradicts data (e.g. "sushi" in Banashankari North Indian set) | LLM explains trade-off honestly; only lists candidate ids | 3 | P1 |
| L-16 | Prompt exceeds model context | Reduce snippets or candidates before call (§9.2) | 3 | P1 |
| L-17 | Repair retry succeeds after first failure | 200 with valid recommendations | 3 | P0 |
| L-18 | Repair retry still fails | 502 unprocessable LLM output | 3, 4 | P0 |
| L-19 | `get_by_ids` returns fewer rows than LLM ids (data bug) | Omit missing or 502; log error | 3 | P1 |

---

## 4. API & HTTP (Phase 4)

| ID | Edge case | Expected behavior | Owner | Severity |
|----|-----------|-------------------|-------|----------|
| A-01 | Missing `location` in body | 400 + field error | 4 | P0 |
| A-02 | `min_rating` = -1 or 6 | 400 validation error | 4 | P0 |
| A-03 | `top_k` = 0 or 100 | 400 or clamp to sane max (document choice) | 4 | P1 |
| A-04 | Empty JSON body | 400 | 4 | P0 |
| A-05 | Wrong Content-Type | 415 or 400 per FastAPI default | 4 | P2 |
| A-06 | Store not loaded at request time | 503 + "Run scripts/ingest.py" (§6.4.1) | 4, 5 | P0 |
| A-07 | Concurrent requests | No shared mutable state corruption; read-only store | 4 | P1 |
| A-08 | Very long `additional_preferences` (> 500 chars) | Truncate or 400 per config | 4 | P1 |
| A-09 | Control characters in free text | Sanitized before prompt (§10.3) | 4, 3 | P1 |
| A-10 | Health check when store down | `store_loaded: false` on `/health` | 4 | P0 |
| A-11 | `NoMatchResponse` from orchestrator | HTTP 200 (not 404) | 4 | P0 |
| A-12 | Orchestrator raises unexpected exception | 500 logged; generic message to client | 4 | P1 |

---

## 5. Presentation UI (Phase 5)

| ID | Edge case | Expected behavior | Owner | Severity |
|----|-----------|-------------------|-------|----------|
| U-01 | Submit with empty location | Client-side block or API 400 displayed | 5 | P0 |
| U-02 | API unreachable (connection refused) | Error state; not infinite spinner | 5 | P0 |
| U-03 | Long LLM latency (15s+) | Loading indicator remains; no double-submit | 5 | P0 |
| U-04 | 200 with empty `recommendations` array | Treat as edge error or no-match UX | 5 | P1 |
| U-05 | 503 on first load | Setup instructions visible | 5 | P0 |
| U-06 | User changes prefs and resubmits | New request; no stale cards | 5 | P0 |
| U-07 | `url` missing on restaurant | Card renders without link | 5 | P1 |
| U-08 | Very long explanation text | Card scrolls or truncates with expand | 5 | P2 |
| U-09 | API key in browser network tab | Must not appear (UI calls backend only) | 5 | P0 |

---

## 6. Configuration & environment (Phase 0–4)

| ID | Edge case | Expected behavior | Owner | Severity |
|----|-----------|-------------------|-------|----------|
| C-01 | No `.env` file | Defaults load; LLM fails at runtime with clear 502 unless key set | 0, 3 | P0 |
| C-02 | Invalid `DATA_PATH` | Store not loaded → 503 | 0, 4 | P0 |
| C-03 | `MAX_CANDIDATES` = 1 | At most one row to LLM | 0, 2 | P1 |
| C-04 | Custom budget thresholds change bands | Re-ingest not required; bands computed at ingest | 1 | P1 |

---

## 7. End-to-end integration (Phase 6)

| ID | Edge case | Expected behavior | Owner | Severity |
|----|-----------|-------------------|-------|----------|
| E-01 | Demo scenario A (Banashankari + North Indian + medium + 4.0) | 200 + ≥1 grounded recommendation | 6 | P0 |
| E-02 | Demo scenario C (over-constrained) | 200 `NoMatchResponse` + suggestions | 6 | P0 |
| E-03 | Demo scenario D (API without ingest) | 503 in UI | 6 | P0 |
| E-04 | Second request different city | Different results; no server restart | 6 | P0 |
| E-05 | `pytest` without network | All unit + mock integration pass | 6 | P0 |
| E-06 | Live LLM integration test | Passes when `LLM_API_KEY` set; skipped in CI | 6 | P1 |

---

## 8. Explicit non-goals (out of scope)

These are **not** edge cases to implement in v1:

| Scenario | Status |
|----------|--------|
| User accounts / saved searches | Out of scope |
| Real-time Zomato API | Out of scope |
| Maps / geolocation radius | Out of scope |
| Multi-city trip planning | Out of scope |
| Collaborative filtering | Out of scope |
| Training custom ranker | Out of scope |

---

## 9. Edge case → HTTP mapping (quick reference)

From architecture §6.4.3:

| Symptom | HTTP | Edge case IDs |
|---------|------|----------------|
| Bad request body | 400 | A-01–A-04, F-14 |
| Parquet / store missing | 503 | D-02, A-06, E-03 |
| No filter matches | 200 `NoMatchResponse` | F-01 |
| LLM / provider failure | 502 | L-05, L-11–L-12, L-18 |
| Success | 200 `RecommendationResponse` | L-01, E-01 |

---

## 10. Document references

- [architecture.md](./architecture.md) — §6.4 error flows  
- [implementationPlan.md](./implementationPlan.md) — phase ownership  
- [eval/README.md](./eval/README.md) — per-phase evaluation criteria  
