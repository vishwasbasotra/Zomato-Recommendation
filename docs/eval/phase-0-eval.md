# Phase 0 Evaluation — Project Bootstrap

**Implementation plan:** [Phase 0](../implementationPlan.md#phase-0--project-bootstrap)  
**Architecture:** §1, §8.1, §10.1, §12

## Objective

Confirm the repository is installable, correctly structured, and configurable without secrets.

## Prerequisites

- Python 3.11+ installed  
- Git clone of project  

---

## Evaluation criteria

### P0 — Must pass

| # | Criterion | How to verify |
|---|-----------|---------------|
| 0.1 | Directory layout matches architecture §12 | Inspect `src/zomato_cursor/`, `scripts/`, `tests/`, `ui/`, `data/processed/` (gitignored ok) |
| 0.2 | `pip install -e .` succeeds | Run in clean venv |
| 0.3 | `from zomato_cursor.config import settings` works without `.env` | Python one-liner |
| 0.4 | `.env.example` documents all vars from architecture §10.1 | Manual diff vs `config.py` |
| 0.5 | `.gitignore` excludes `.env`, `data/processed/`, `.venv` | File review |
| 0.6 | No API keys or secrets in tracked files | `git grep` for `sk-`, keys |
| 0.7 | `README.md` links to problem statement, architecture, implementation plan | Open README |

### P1 — Should pass

| # | Criterion | How to verify |
|---|-----------|---------------|
| 0.8 | `ruff` or linter configured | `ruff check` runs |
| 0.9 | `pytest` discovers `tests/` | `pytest --collect-only` |

### P2 — Nice to have

| # | Criterion | How to verify |
|---|-----------|---------------|
| 0.10 | Pre-commit or editorconfig | Optional file present |

---

## Automated checks

```bash
pip install -e .
python -c "from zomato_cursor.config import settings; print(settings.DATA_PATH)"
pytest --collect-only
ruff check src/   # if configured
```

---

## Manual checks

- [ ] Default `DATA_PATH` points to `data/processed/restaurants.parquet`
- [ ] Budget thresholds and `MAX_CANDIDATES` readable from settings
- [ ] Import path documented for future `uvicorn zomato_cursor.api.main:app`

---

## Edge cases (this phase)

| ID | Case | Expected |
|----|------|----------|
| C-01 | No `.env` | Defaults load (see [edgecase.md](../edgecase.md)) |

---

## Sign-off

| Field | Value |
|-------|-------|
| Evaluator | Agent / implementation |
| Date | 2026-05-21 |
| Result | ☑ Pass ☐ Conditional ☐ Fail |
| Notes | `pip install -e ".[dev]"`, pytest (4 tests), ruff clean |

**Next phase:** [phase-1-eval.md](./phase-1-eval.md) — blocked until **Pass**.
