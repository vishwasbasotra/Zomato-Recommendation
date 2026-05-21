# Phase 1 Evaluation — Data Ingestion & Preprocessing

**Implementation plan:** [Phase 1](../implementationPlan.md#phase-1--data-ingestion--preprocessing)  
**Architecture:** §4.2, §6.3, §7, §14

## Objective

Produce reliable processed data and a loadable `RestaurantStore` per the ingest sequence (architecture §6.3).

## Prerequisites

- [phase-0-eval.md](./phase-0-eval.md) — **Pass**
- Network access for first Hugging Face download (or pre-cached Parquet)

---

## Evaluation criteria

### P0 — Must pass

| # | Criterion | How to verify |
|---|-----------|---------------|
| 1.1 | `python scripts/ingest.py` exits 0 | Run CLI |
| 1.2 | `metadata.json` reports row count ≈ 51k (±5%) | Read metadata |
| 1.3 | Parquet contains all canonical columns (architecture §4.2) | Schema inspect |
| 1.4 | `RestaurantStore.load()` completes in &lt; 2s | Timed one-liner |
| 1.5 | `is_loaded()` true after load; false before | Unit test or script |
| 1.6 | `get_by_ids([valid_id])` returns matching row | Unit test |
| 1.7 | Re-run ingest overwrites files idempotently | Run twice, same schema |
| 1.8 | Unit tests pass for rate, cost, budget_band parsers | `pytest tests/test_preprocessor.py` |

### P1 — Should pass

| # | Criterion | How to verify |
|---|-----------|---------------|
| 1.9 | Rows with null `name` dropped | Count diff raw vs processed |
| 1.10 | `review_snippet` length ≤ `MAX_REVIEW_CHARS` | Sample max length |
| 1.11 | `id` stable across re-ingest for same `url` | Re-ingest compare |

### P2 — Nice to have

| # | Criterion | How to verify |
|---|-----------|---------------|
| 1.12 | `--force` or offline skip for HF | CLI flag documented |

---

## Automated checks

```bash
python scripts/ingest.py
pytest tests/test_preprocessor.py -v
python -c "from zomato_cursor.data.store import RestaurantStore; import time; t=time.time(); s=RestaurantStore.load(); print(len(s.df), time.time()-t, s.is_loaded())"
```

---

## Manual checks

- [ ] Spot-check one row: `rating`, `budget_band`, `cuisines` list sensible
- [ ] `rate` like `4.1/5` parsed correctly in sample
- [ ] Log output includes row count and output path

---

## Edge cases (this phase)

| ID | Case | Pass? |
|----|------|-------|
| D-01 | HF download fail | ☐ |
| D-03 | Missing / invalid rate | ☐ |
| D-04 | `4.1/5` format | ☐ |
| D-05 | Missing cost | ☐ |
| D-08 | Null name dropped | ☐ |
| D-10 | Long reviews truncated | ☐ |
| D-12 | City/location normalization | ☐ |
| C-02 | Invalid DATA_PATH → not loaded | ☐ |

---

## Sign-off

| Field | Value |
|-------|-------|
| Evaluator | |
| Date | |
| Result | ☐ Pass ☐ Conditional ☐ Fail |
| Notes | |

**Next phase:** [phase-2-eval.md](./phase-2-eval.md)
