# Phase 5 Evaluation — Presentation UI

**Implementation plan:** [Phase 5](../implementationPlan.md#phase-5--presentation-ui)  
**Architecture:** §8.3, §6.2 steps 1–4, §6.4.1, §6.4.3

## Objective

User completes preference → result flow with correct UI states for all HTTP outcomes.

## Prerequisites

- [phase-4-eval.md](./phase-4-eval.md) — **Pass**
- API running on documented port
- Ingest completed (for success scenarios)

---

## Evaluation criteria

### P0 — Must pass

| # | Criterion | How to verify |
|---|-----------|---------------|
| 5.1 | Form collects location (required), budget, cuisine, min rating, notes, top_k | UI walkthrough |
| 5.2 | Submit shows loading state during API call | Visual |
| 5.3 | 200 success: cards show name, cuisines, rating, cost, explanation | Scenario A |
| 5.4 | 200 no-match: message + suggestions visible | Scenario C |
| 5.5 | 400: field errors shown (submit without location) | Manual |
| 5.6 | 502: user-friendly retry message | Mock or disconnect LLM |
| 5.7 | 503: setup message (API without ingest) | Scenario D |
| 5.8 | Second submit with different prefs updates results without app restart | Scenario B |
| 5.9 | No LLM API key in browser devtools network | Inspect requests |
| 5.10 | README documents two-terminal run (API + UI) | Doc review |

### P1 — Should pass

| # | Criterion | How to verify |
|---|-----------|---------------|
| 5.11 | Optional: Zomato `url` link on card | Click link |
| 5.12 | Optional: online_order / book_table badges | Card UI |
| 5.13 | API down → error state, not infinite spinner | Stop API, submit |
| 5.14 | Client blocks empty location before POST | UI test |

### P2 — Nice to have

| # | Criterion | How to verify |
|---|-----------|---------------|
| 5.15 | Long explanation truncated/expandable | UI polish |
| 5.16 | Autocomplete for cuisine from API | Optional endpoint |

---

## Demo scenarios (from implementation plan)

| Scenario | Steps | Expected UI |
|----------|-------|-------------|
| **A** | Banashankari, North Indian, medium, ≥4.0, “family friendly” | Success cards |
| **B** | Bangalore, Italian, high | Different cards |
| **C** | Over-constrained locality + cuisine + rating | No-match + suggestions |
| **D** | API started without ingest | 503 setup message |

---

## Manual checks

- [ ] Walk architecture §6.2 steps 1–4 (form → loading → result)
- [ ] No raw stack traces shown to user on errors

---

## Edge cases (this phase)

| ID | Case | Pass? |
|----|------|-------|
| U-01 | Empty location | ☐ |
| U-02 | API unreachable | ☐ |
| U-03 | Long LLM wait | ☐ |
| U-05 | 503 first load | ☐ |
| U-06 | Resubmit new prefs | ☐ |
| U-09 | No API key in browser | ☐ |

---

## Sign-off

| Field | Value |
|-------|-------|
| Evaluator | |
| Date | |
| Result | ☐ Pass ☐ Conditional ☐ Fail |
| Notes | |

**Next phase:** [phase-6-eval.md](./phase-6-eval.md)
