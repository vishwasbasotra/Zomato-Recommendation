"""In-memory data store for the restaurant dataset."""

import pandas as pd
from pathlib import Path
from typing import Optional

class RestaurantStore:
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        
    def load(self, parquet_path: str | Path) -> "RestaurantStore":
        """Load Parquet dataset into memory."""
        self.df = pd.read_parquet(parquet_path)
        return self
        
    def is_loaded(self) -> bool:
        """Check if dataset is loaded."""
        return self.df is not None

    def assert_loaded(self) -> None:
        """Raise error if store not loaded."""
        if not self.is_loaded():
            raise RuntimeError("RestaurantStore not loaded. Run scripts/ingest.py first.")

    def get_by_ids(self, ids: list[str]) -> pd.DataFrame:
        """Retrieve full rows for a list of ids, keeping the requested order."""
        self.assert_loaded()
        subset = self.df[self.df["id"].isin(ids)].set_index("id")
        return subset.reindex(ids).dropna(how="all").reset_index()

# Global singleton to be used across the app
store = RestaurantStore()
