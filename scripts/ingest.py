"""Ingestion script to load, preprocess, and save the dataset."""

import json
import time
import argparse
from pathlib import Path

from zomato_cursor.config import settings
from zomato_cursor.data.loader import load_raw_dataset
from zomato_cursor.data.preprocessor import preprocess_dataset

def main():
    parser = argparse.ArgumentParser(description="Ingest Zomato dataset")
    parser.add_argument("--force", action="store_true", help="Force re-download even if parquet exists")
    args = parser.parse_args()

    out_path = Path(settings.DATA_PATH)
    meta_path = out_path.parent / "metadata.json"

    if out_path.exists() and not args.force:
        print(f"Dataset already exists at {out_path}. Re-ingesting anyway (idempotent)...")
        # Ingest overwrites idempotently. Could skip with logic here if desired.

    out_path.parent.mkdir(parents=True, exist_ok=True)

    print("Loading raw dataset from Hugging Face...")
    t0 = time.time()
    raw_ds = load_raw_dataset()
    print(f"Loaded {len(raw_ds)} raw rows in {time.time() - t0:.2f}s.")

    print("Preprocessing data...")
    t1 = time.time()
    df = preprocess_dataset(raw_ds)
    print(f"Preprocessed {len(df)} rows in {time.time() - t1:.2f}s.")

    print(f"Saving to {out_path}...")
    df.to_parquet(out_path, index=False)

    metadata = {
        "processed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "row_count": len(df),
    }
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Success! {len(df)} rows saved to {out_path}")
    print(f"Metadata saved to {meta_path}")

if __name__ == "__main__":
    main()
