# Streamlit Deployment Plan

This document outlines the strategy for deploying the Zomato AI Recommendation Engine to **Streamlit Community Cloud**.

## 1. Architectural Approach
Since Streamlit is a Python-based full-stack framework, we have two deployment options:
1. **Frontend-Only (Client/Server)**: Streamlit acts purely as a frontend calling our existing FastAPI backend (which would need to be hosted elsewhere, like Render or AWS).
2. **Monolithic (Recommended)**: We bypass FastAPI entirely. We create a `streamlit_app.py` that directly imports the `orchestrator.recommend()` function and loads the `RestaurantStore` into memory. Streamlit Community Cloud handles both the UI and the backend logic in one place.

**Decision**: We will proceed with the **Monolithic** approach for simplicity and zero-cost hosting.

## 2. Data Management (The Parquet File)
Our `restaurants.parquet` file is generated locally via `ingest.py` and is relatively large (~20MB). Streamlit Community Cloud pulls directly from GitHub.
- **Option A (Git LFS)**: Commit the `restaurants.parquet` to GitHub using Git Large File Storage (LFS).
- **Option B (On-the-fly Ingestion)**: Have the Streamlit app download the raw HuggingFace dataset and convert it to Parquet on startup using Streamlit's `@st.cache_resource`.

**Decision**: **Option B** is preferred as it avoids GitHub LFS quota limits and keeps the repository lightweight.

## 3. Required Code Changes

To transition to Streamlit, we will need to create a new file `streamlit_app.py` at the root of the project.

### `streamlit_app.py` (Draft Structure)
```python
import streamlit as st
import os
from zomato_cursor.data.store import store
from zomato_cursor.models.preferences import UserPreferences
from zomato_cursor.services.orchestrator import recommend

# 1. Page Config
st.set_page_config(page_title="Zomato AI", layout="centered")

# 2. Data Loading (Cached)
@st.cache_resource
def load_data():
    if not os.path.exists("data/processed/restaurants.parquet"):
        # Run the ingest script logic here if missing
        pass
    store.load("data/processed/restaurants.parquet")
    return store

store = load_data()

# 3. UI Forms
st.title("Zomato AI - Curated Dining")
with st.form("recommendation_form"):
    location = st.selectbox("Location", store.df["location"].dropna().unique())
    cuisine = st.selectbox("Cuisine", ["Any"] + [...])
    budget = st.selectbox("Budget", ["low", "medium", "high"])
    min_rating = st.slider("Min Rating", 0.0, 5.0, 4.0)
    vibe = st.text_area("Vibe & Preferences")
    
    submitted = st.form_submit_button("Discover")

# 4. Action
if submitted:
    with st.spinner("Analyzing Zomato reviews..."):
        prefs = UserPreferences(
            location=location,
            cuisine=cuisine if cuisine != "Any" else None,
            budget=budget,
            min_rating=min_rating,
            additional_preferences=vibe
        )
        response = recommend(prefs)
        # Render response cards...
```

## 4. Dependencies
We will need to add `streamlit` to our dependencies in `pyproject.toml`:
```toml
dependencies = [
    # ... existing dependencies
    "streamlit>=1.30.0",
]
```

## 5. Environment Secrets
In the Streamlit Community Cloud dashboard, we will need to configure the following secrets (under **Settings > Secrets**):
```toml
LLM_PROVIDER="gemini"
LLM_MODEL="gemini-2.5-flash"
LLM_API_KEY="your_actual_gemini_key_here"
```

## 6. Deployment Steps
1. Build and test `streamlit_app.py` locally (`streamlit run streamlit_app.py`).
2. Commit and push the code to a public GitHub repository.
3. Log in to [share.streamlit.io](https://share.streamlit.io).
4. Click **New app**.
5. Select the GitHub repository, branch, and set the Main file path to `streamlit_app.py`.
6. Click **Advanced Settings** and paste the secrets.
7. Click **Deploy!**
