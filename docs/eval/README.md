# Phase Evaluation Guide

Use these documents to **sign off** each implementation phase before starting the next. Criteria align with [implementationPlan.md](../implementationPlan.md), [architecture.md](../architecture.md), and [edgecase.md](../edgecase.md).

## Evaluation process

1. Complete all tasks in the phase section of the implementation plan.
2. Run **automated checks** listed in the phase `eval.md`.
3. Run **manual checks** and relevant **edge cases** from [edgecase.md](../edgecase.md).
4. Mark the phase **Pass / Fail** using the sign-off checklist in each file.
5. Record date and evaluator (self-review or peer) in the checklist.

## Pass rules

| Result | Condition |
|--------|-----------|
| **Pass** | All **P0** criteria met; no blocking failures |
| **Conditional pass** | P0 met; P1 gaps documented as follow-ups before Phase 6 |
| **Fail** | Any P0 criterion unmet |

## Phase index

| Phase | Document | Primary focus |
|-------|----------|---------------|
| 0 | [phase-0-eval.md](./phase-0-eval.md) | Repo bootstrap, config |
| 1 | [phase-1-eval.md](./phase-1-eval.md) | Ingest, Parquet, store |
| 2 | [phase-2-eval.md](./phase-2-eval.md) | Filters, no-match |
| 3 | [phase-3-eval.md](./phase-3-eval.md) | LLM, validator, orchestrator |
| 4 | [phase-4-eval.md](./phase-4-eval.md) | FastAPI, HTTP codes |
| 5 | [phase-5-eval.md](./phase-5-eval.md) | UI flows |
| 6 | [phase-6-eval.md](./phase-6-eval.md) | Release, E2E, success criteria |

## Dependency chain

```text
phase-0-eval PASS → phase-1-eval → … → phase-6-eval PASS → project complete
```

Do not start phase **N+1** until phase **N** eval is **Pass**.
