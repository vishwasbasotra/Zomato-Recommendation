import os
import streamlit as st
import pandas as pd
from zomato_cursor.config import settings
from zomato_cursor.data.store import store
from zomato_cursor.models.preferences import UserPreferences
from zomato_cursor.services.orchestrator import recommend
from zomato_cursor.models.response import RecommendationResponse, NoMatchResponse, ErrorResponse

st.set_page_config(
    page_title="Zomato AI Recommendations",
    page_icon="🍽️",
    layout="wide"
)

@st.cache_resource
def load_and_prep_data():
    """Load the dataset and return the store."""
    if not settings.DATA_PATH.exists():
        st.info("Dataset not found locally. Running ingestion... (this takes ~10 seconds)")
        from scripts.ingest import main as run_ingest
        run_ingest()
        
    store.load(settings.DATA_PATH)
    return store

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .stButton>button {
        background-color: #cb202d;
        color: white;
        border: none;
        width: 100%;
        padding: 0.75rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #e23744;
        color: white;
        border: none;
    }
    .card {
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: rgba(255,255,255,0.05);
    }
    .badge {
        background: #10b981;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-right: 5px;
    }
    .badge-secondary {
        background: rgba(255,255,255,0.2);
    }
</style>
""", unsafe_allow_html=True)

st.title("🍽️ Zomato AI Recommendations")
st.markdown("Discover curated dining experiences using Gemini 2.5 Flash and the Zomato Bangalore Dataset.")

try:
    data_store = load_and_prep_data()
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# Build dropdown options
locations = sorted(data_store.df["location"].dropna().unique().tolist())
cuisines_set = set()
for c_list in data_store.df["cuisines"].dropna():
    for c in c_list:
        cuisines_set.add(c)
cuisines = ["Any"] + sorted(list(cuisines_set))

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Your Preferences")
    with st.form("recommendation_form"):
        location = st.selectbox("Location *", locations, index=locations.index("Banashankari") if "Banashankari" in locations else 0)
        cuisine = st.selectbox("Cuisine", cuisines, index=cuisines.index("North Indian") if "North Indian" in cuisines else 0)
        budget = st.selectbox("Budget", ["Any", "low", "medium", "high"], index=2)
        min_rating = st.slider("Minimum Rating", 0.0, 5.0, 4.0, 0.1)
        top_k = st.number_input("Number of Results", min_value=1, max_value=10, value=5)
        vibe = st.text_area("Vibe & Preferences", placeholder="e.g. Quiet ambiance, romantic, rooftop...")
        
        submitted = st.form_submit_button("Discover")

with col2:
    if submitted:
        if not settings.LLM_API_KEY and "LLM_API_KEY" not in os.environ:
            st.error("Error: LLM_API_KEY is not set in secrets or environment.")
            st.stop()
            
        with st.spinner("AI is analyzing Zomato reviews... (This takes about 10 seconds)"):
            prefs = UserPreferences(
                location=location,
                cuisine=cuisine if cuisine != "Any" else None,
                budget=budget if budget != "Any" else None,
                min_rating=min_rating,
                top_k=int(top_k),
                additional_preferences=vibe.strip() if vibe.strip() else None
            )
            
            resp = recommend(prefs)
            
        if isinstance(resp, ErrorResponse):
            st.error(f"**Error from AI Provider**: {resp.message}")
        elif isinstance(resp, NoMatchResponse):
            st.warning(resp.message)
            st.subheader("Suggestions:")
            for s in resp.suggestions:
                st.write(f"- {s}")
        elif isinstance(resp, RecommendationResponse):
            st.success(f"Found {len(resp.recommendations)} curated recommendations!")
            st.write(f"*{resp.summary}*")
            st.caption(f"Latency: {resp.meta['latency_ms']}ms | Processed {resp.meta['candidate_count']} candidates | Model: {resp.meta['llm_model']}")
            
            for r in resp.recommendations:
                # Build badges HTML
                badges = f'<span class="badge">★ {r.rating}</span>'
                if r.cost_for_two:
                    badges += f'<span class="badge badge-secondary">₹{r.cost_for_two} for two</span>'
                
                cuisines_str = ", ".join(r.cuisines[:3])
                
                # Card HTML
                st.markdown(f"""
                <div class="card">
                    <h3>#{r.rank} {r.name}</h3>
                    <div style="margin-bottom: 10px;">{badges} <span style="color: #94a3b8; font-size: 0.9rem;">{cuisines_str}</span></div>
                    <p style="margin-bottom: 15px; border-left: 3px solid #cb202d; padding-left: 10px;">
                        {r.explanation}
                    </p>
                    <p style="font-size: 0.85rem; color: #fda4af;"><strong>Highlights:</strong> {", ".join(r.match_highlights)}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("👈 Fill out your preferences and click Discover to get AI recommendations!")
