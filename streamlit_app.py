import os
import streamlit as st
import random
from zomato_cursor.config import settings
from zomato_cursor.data.store import store
from zomato_cursor.models.preferences import UserPreferences
from zomato_cursor.services.orchestrator import recommend
from zomato_cursor.models.response import RecommendationResponse, NoMatchResponse, ErrorResponse

st.set_page_config(
    page_title="Zomato AI Engine",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS Injection for Dark/Glassmorphic Theme ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap');

    /* Base Theme Overrides */
    .stApp {
        background-color: #1e0f0e;
        color: #fadcd9;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Background Blobs */
    .gradient-blob {
        position: fixed;
        filter: blur(120px);
        z-index: -1;
        border-radius: 50%;
        opacity: 0.4;
        pointer-events: none;
    }
    .blob-crimson { background: #cb202d; width: 500px; height: 500px; top: -100px; right: -100px; }
    .blob-navy { background: #1e1b4b; width: 600px; height: 600px; bottom: -200px; left: -200px; }

    /* Streamlit Widget Overrides */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 24px;
    }
    
    .stButton>button {
        background-color: #cb202d !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem !important;
        font-weight: bold !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background-color: #e23744 !important;
        transform: scale(1.02);
    }
    
    /* Custom Result Card Styles (Raw CSS replacement for Tailwind) */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 24px;
        transition: transform 0.3s ease;
    }
    .glass-card:hover {
        transform: scale(1.01);
    }
    .card-img-container {
        position: relative;
        height: 250px;
        overflow: hidden;
    }
    .card-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .card-img-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(to top, #1e0f0e 10%, transparent 80%);
    }
    .card-badges-top {
        position: absolute;
        top: 16px;
        left: 16px;
        display: flex;
        gap: 8px;
    }
    .badge-rank {
        background: linear-gradient(to bottom right, #cb202d, #68000d);
        color: white;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 14px;
    }
    .badge-rating {
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(8px);
        color: #ffb3af;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 14px;
    }
    .card-header-bottom {
        position: absolute;
        bottom: 16px;
        left: 24px;
        right: 24px;
    }
    .card-title {
        font-size: 28px;
        font-weight: 700;
        color: white;
        margin: 0 0 4px 0;
        font-family: 'Outfit', sans-serif;
    }
    .card-subtitle {
        display: flex;
        gap: 8px;
        color: #e4bdbb;
        font-size: 14px;
    }
    .card-body {
        padding: 24px;
    }
    .neural-rationale {
        background: rgba(203, 32, 45, 0.05);
        border: 1px solid rgba(203, 32, 45, 0.1);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
    }
    .neural-title {
        color: #ffb3af;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 12px;
        margin-bottom: 8px;
    }
    .neural-text {
        color: #fadcd9;
        font-style: italic;
        font-size: 14px;
        line-height: 1.6;
        margin: 0;
    }
    .card-highlights {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    .highlight-pill {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        color: #e4bdbb;
    }
</style>
<div class="gradient-blob blob-crimson"></div>
<div class="gradient-blob blob-navy"></div>
""", unsafe_allow_html=True)

# Unsplash fallback images
FALLBACK_IMAGES = [
    "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1550966841-3ee71a39f0d7?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1552566626-52f8b828add9?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?auto=format&fit=crop&w=800&q=80"
]

@st.cache_resource
def load_and_prep_data():
    if not settings.DATA_PATH.exists():
        from scripts.ingest import main as run_ingest
        run_ingest()
    store.load(settings.DATA_PATH)
    return store

# Header
st.markdown("<h1 style='color: #ffb3af; font-family: Outfit; margin-bottom: 0;'>Zomato AI Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #e4bdbb; margin-top: 0; margin-bottom: 30px;'>Futuristic Dining Concierge</p>", unsafe_allow_html=True)

try:
    data_store = load_and_prep_data()
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

locations = sorted(data_store.df["location"].dropna().unique().tolist())
cuisines_set = set()
for c_list in data_store.df["cuisines"].dropna():
    for c in c_list:
        cuisines_set.add(c)
cuisines = ["Any"] + sorted(list(cuisines_set))

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("<h3 style='color: #ffb3af; font-family: Outfit;'>Set Your Vibe</h3>", unsafe_allow_html=True)
    with st.form("preference-form"):
        location = st.selectbox("LOCATION *", locations, index=locations.index("Banashankari") if "Banashankari" in locations else 0)
        cuisine = st.selectbox("CUISINE", cuisines, index=cuisines.index("North Indian") if "North Indian" in cuisines else 0)
        
        c1, c2 = st.columns(2)
        with c1:
            budget = st.selectbox("BUDGET", ["Any", "low", "medium", "high"], index=2)
        with c2:
            top_k = st.number_input("RESULTS", min_value=1, max_value=10, value=5)
            
        min_rating = st.slider("MIN RATING", 0.0, 5.0, 4.0, 0.1)
        vibe = st.text_area("SPECIFIC VIBE", placeholder="e.g. 'Rooftop with jazz music and vegan options'", height=100)
        
        submitted = st.form_submit_button("✨ Discover")

with col2:
    if submitted:
        if not settings.LLM_API_KEY and "LLM_API_KEY" not in os.environ:
            st.error("Error: LLM_API_KEY is not set.")
            st.stop()
            
        with st.spinner("AI is analyzing thousands of Zomato reviews..."):
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
            st.warning("No Match Found")
            st.write(resp.message)
            for s in resp.suggestions:
                st.write(f"- {s}")
        elif isinstance(resp, RecommendationResponse):
            st.markdown(f"<h2 style='color: #ffb3af; font-family: Outfit;'>Top Curated Matches</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #e4bdbb; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 24px;'>Based on your neural profile • {len(resp.recommendations)} Discoveries</p>", unsafe_allow_html=True)
            
            for i, r in enumerate(resp.recommendations):
                cuisines_str = " • ".join(r.cuisines[:3])
                cost_str = f"₹{r.cost_for_two} for two" if r.cost_for_two else ""
                hl_html = "".join([f"<span class='highlight-pill'>{h}</span>" for h in r.match_highlights])
                bg_img = FALLBACK_IMAGES[i % len(FALLBACK_IMAGES)]
                
                card_html = f"""
                <div class="glass-card">
                    <div class="card-img-container">
                        <img src="{bg_img}" class="card-img">
                        <div class="card-img-overlay"></div>
                        <div class="card-badges-top">
                            <span class="badge-rank">#{r.rank} AI PICK</span>
                            <span class="badge-rating">★ {r.rating}</span>
                        </div>
                        <div class="card-header-bottom">
                            <h3 class="card-title">{r.name}</h3>
                            <div class="card-subtitle">
                                <span>{cuisines_str}</span>
                                <span>•</span>
                                <span style="color: #ffb3af; font-weight: bold;">{cost_str}</span>
                            </div>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="neural-rationale">
                            <div class="neural-title">🧠 Neural Rationale</div>
                            <p class="neural-text">"{r.explanation}"</p>
                        </div>
                        <div class="card-highlights">
                            {hl_html}
                        </div>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
    else:
        # Welcome State
        st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; text-align: center; padding: 48px; background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; margin-top: 20px;">
            <div style="font-size: 64px; margin-bottom: 24px;">🔮</div>
            <h2 style="color: #ffb3af; font-family: Outfit; font-size: 36px; margin-bottom: 16px;">Gourmet AI Ready</h2>
            <p style="color: #e4bdbb; font-size: 18px; max-width: 400px; line-height: 1.5;">
                Fill out your preferences to the left and let our neural engine curate your perfect dining experience.
            </p>
        </div>
        """, unsafe_allow_html=True)
