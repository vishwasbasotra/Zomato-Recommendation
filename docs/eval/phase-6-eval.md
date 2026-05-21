# Phase 6 Evaluation — Quality & Release Readiness

**Implementation plan:** [Phase 6](../implementationPlan.md#phase-6--quality-documentation--release-readiness)  
**Architecture:** §11.3, §13, §17  
**Problem statement:** Success criteria §139–146, scope §150–163

## Objective

Project meets all product success criteria, handles documented edge cases, and is demonstrable as a portfolio release.

## Prerequisites

- [phase-5-eval.md](./phase-5-eval.md) — **Pass**
- All prior phase evals **Pass**

---

## Evaluation criteria

### P0 — Problem statement success criteria

| # | Success criterion | Verification |
|---|-------------------|--------------|
| SC-1 | Enter preferences in one flow without editing data files | Phase 5 scenario A |
| SC-2 | Only dataset restaurants matching hard filters, or explicit no-match | Phase 2 tests + Phase 3 validator + manual id check |
| SC-3 | Ranked recommendations with explanations referencing inputs | Scenario A manual read |
| SC-4 | Re-run with different prefs without redeploy / re-ingest | Scenario B without restart |

### P0 — Technical quality

| # | Criterion | How to verify |
|---|-----------|---------------|
| 6.1 | `pytest` full unit suite passes (no network) | `pytest -m "not integration"` |
| 6.2 | README: ingest → API → UI complete path | Follow as new user |
| 6.3 | Links to all docs: problem statement, architecture, plan, edge cases, eval | README review |
| 6.4 | Demo scenarios A, B, C, D pass | Checklist below |
| 6.5 | All **P0** edge cases in [edgecase.md](../edgecase.md) addressed or documented | Review §1–7 tables |
| 6.6 | `problemStatement.md` repository status updated | Doc review |

### P1 — Should pass

| # | Criterion | How to verify |
|---|-----------|---------------|
| 6.7 | `ruff` / format clean | CI or local |
| 6.8 | GitHub Actions CI on push (optional) | Green build |
| 6.9 | `@pytest.mark.integration` documented for live LLM | README |
| 6.10 | Docker Compose runs (optional) | `docker compose up` |

### P2 — Nice to have

| # | Criterion | How to verify |
|---|-----------|---------------|
| 6.11 | Screenshots in README | Files present |
| 6.12 | Sample `.env` filled for local demo | Template only, not committed |

---

## Out of scope verification (must be true)

| Item | Confirmed |
|------|-----------|
| No user accounts / history | ☐ |
| No Zomato live API / scraping | ☐ |
| No maps / payments / delivery | ☐ |
| No custom ML model training | ☐ |

---

## End-to-end demo checklist

| Step | Action | Pass? |
|------|--------|-------|
| 1 | `python scripts/ingest.py` | ☐ |
| 2 | Start API | ☐ |
| 3 | Start UI | ☐ |
| 4 | Scenario A — success | ☐ |
| 5 | Scenario B — different results | ☐ |
| 6 | Scenario C — no-match | ☐ |
| 7 | Scenario D — 503 without data | ☐ |

---

## Integration edge cases

| ID | Case | Pass? |
|----|------|-------|
| E-01 | Demo A | ☐ |
| E-02 | Demo C | ☐ |
| E-03 | Demo D | ☐ |
| E-04 | Second city request | ☐ |
| E-05 | pytest offline | ☐ |
| E-06 | Live LLM optional | ☐ |

---

## Phase eval rollup

| Phase | Eval doc | Result |
|-------|----------|--------|
| 0 | [phase-0-eval.md](./phase-0-eval.md) | ☐ Pass |
| 1 | [phase-1-eval.md](./phase-1-eval.md) | ☐ Pass |
| 2 | [phase-2-eval.md](./phase-2-eval.md) | ☐ Pass |
| 3 | [phase-3-eval.md](./phase-3-eval.md) | ☐ Pass |
| 4 | [phase-4-eval.md](./phase-4-eval.md) | ☐ Pass |
| 5 | [phase-5-eval.md](./phase-5-eval.md) | ☐ Pass |
| 6 | This document | ☐ Pass |

---

## Sign-off (project complete)

| Field | Value |
|-------|-------|
| Evaluator | |
| Date | |
| Result | ☐ Pass ☐ Conditional ☐ Fail |
| Notes | |

**Project status:** ☐ Ready for portfolio / demo ☐ Needs follow-up
