"""Phase 0: configuration defaults."""

from zomato_cursor.config import Settings, settings


def test_settings_singleton_loads_without_env_file() -> None:
    assert settings.LLM_PROVIDER == "gemini"
    assert settings.MAX_CANDIDATES == 10
    assert settings.TOP_K_DEFAULT == 5


def test_data_path_default() -> None:
    path = str(settings.DATA_PATH).replace("\\", "/")
    assert path.endswith("data/processed/restaurants.parquet")


def test_budget_thresholds() -> None:
    assert settings.BUDGET_LOW_MAX == 400
    assert settings.BUDGET_MEDIUM_MAX == 800


def test_settings_instantiation_with_defaults() -> None:
    s = Settings(_env_file=None)
    assert s.MAX_REVIEW_CHARS == 200
    assert s.MAX_ADDITIONAL_PREF_CHARS == 500
