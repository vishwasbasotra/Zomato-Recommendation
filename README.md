# Zomato-Cursor

AI-powered restaurant recommendation inspired by Zomato. Combines structured filtering over a real Hugging Face dataset with an LLM for ranked, explained suggestions.

## Documentation

| Document | Description |
|----------|-------------|
| [docs/problemStatement.md](docs/problemStatement.md) | Product context, objectives, success criteria |
| [docs/architecture.md](docs/architecture.md) | System design, components, sequence diagrams |
| [docs/implementationPlan.md](docs/implementationPlan.md) | Phase-wise build plan |
| [docs/edgecase.md](docs/edgecase.md) | Edge cases and expected behavior |
| [docs/eval/README.md](docs/eval/README.md) | Per-phase evaluation criteria |

## Requirements

- Python 3.11+
- (Later phases) Hugging Face access for dataset ingest
- (Later phases) LLM API key in `.env`

## Setup

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
# source .venv/bin/activate

pip install -e ".[dev]"
```

Copy environment template and add secrets locally (never commit `.env`):

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # macOS / Linux
```

Verify configuration:

```bash
python -c "from zomato_cursor.config import settings; print(settings.DATA_PATH)"
```

## Run API (stub — full stack from Phase 4+)

```bash
uvicorn zomato_cursor.api.main:app --reload --port 8000
```

Health check: http://localhost:8000/api/v1/health

## Development

```bash
pytest
ruff check src tests
```

## Implementation status

| Phase | Status |
|-------|--------|
| 0 — Bootstrap | Complete |
| 1 — Data pipeline | Pending |
| 2 — Filtering | Pending |
| 3 — LLM | Pending |
| 4 — API | Pending |
| 5 — UI | Pending |
| 6 — Release | Pending |

## License

Portfolio / learning project.
