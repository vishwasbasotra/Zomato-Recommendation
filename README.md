# Zomato AI Engine 🍽️🔮

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-orange.svg)

> **Live Demo:** [https://zomato-recommendation-basotra.streamlit.app/](https://zomato-recommendation-basotra.streamlit.app/)

A futuristic, AI-powered dining concierge that recommends restaurants based on your specific "vibe" and natural language preferences. It analyzes over 50,000 real Zomato restaurant reviews using Google's **Gemini 2.5 Flash** LLM to curate the perfect dining experience for you.

## Features
- **Semantic Vibe Matching:** Don't just search for "Italian". Search for *"A quiet, romantic rooftop with jazz music and vegan options."*
- **Lightning Fast Data Pipeline:** Uses Parquet columnar storage for sub-millisecond filtering of 50k+ restaurants before passing context to the LLM.
- **Auto-Repairing LLM Orchestrator:** Validates the LLM's JSON output to prevent hallucinations, automatically prompting the LLM to self-correct if it makes a mistake.
- **Glassmorphic UI:** A beautifully designed dark-mode Streamlit interface using custom injected CSS and Tailwind-inspired aesthetics.

## Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vishwasbasotra/Zomato-Recommendation.git
   cd Zomato-Recommendation
   ```

2. **Set up the environment:**
   Create a `.env` file (copy from `.env.example`) and add your Gemini API Key:
   ```env
   LLM_API_KEY="your_actual_gemini_key_here"
   ```

3. **Install dependencies using `uv`:**
   ```bash
   uv pip install -e .
   ```

4. **Ingest the Dataset:**
   Downloads and processes the raw Zomato dataset into a highly-optimized Parquet file.
   ```bash
   python scripts/ingest.py
   ```

5. **Start the App:**
   ```bash
   streamlit run streamlit_app.py
   ```

---

