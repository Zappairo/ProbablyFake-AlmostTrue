import streamlit as st
from transformers import pipeline
import requests
import urllib.parse
import os

MODEL_NAME = "hamzab/roberta-fake-news-classification"

@st.cache_resource
def get_fake_news_pipeline():
    return pipeline("text-classification", model=MODEL_NAME, tokenizer=MODEL_NAME)

# Récupération des clés API depuis les variables d'environnement ou secrets Streamlit
try:
    GOOGLE_FACTCHECK_API_KEY = st.secrets["GOOGLE_FACTCHECK_API_KEY"]
except:
    GOOGLE_FACTCHECK_API_KEY = os.getenv("GOOGLE_FACTCHECK_API_KEY")

try:
    NEWSAPI_KEY = st.secrets["NEWSAPI_KEY"]
except:
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

# Vérification que les clés API sont présentes
if not GOOGLE_FACTCHECK_API_KEY:
    st.warning("⚠️ Google Fact Check API key not found. Fact checking will be disabled.")
if not NEWSAPI_KEY:
    st.warning("⚠️ NewsAPI key not found. News search will be disabled.")

# Fonction pour interroger NewsAPI
def search_newsapi(query, api_key):
    base_url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": api_key,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 5
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("articles", [])
        else:
            return []
    except Exception:
        return []

# Fonction pour interroger Google Fact Check API
def search_fact_check(query, api_key):
    base_url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    params = {
        "query": query,
        "key": api_key
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("claims", [])
        else:
            return []
    except Exception:
        return []

def search_wikipedia(query):
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "srlimit": 5
    }
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json().get("query", {}).get("search", [])
        else:
            return []
    except Exception:
        return []

def ia_fake_news_score(text):
    try:
        clf = get_fake_news_pipeline()
        result = clf(text)[0]
        label = result["label"]
        score = result["score"]
        confidence_pct = score * 100
        
        if label == "LABEL_0":
            exp = f"The AI model estimates this text is likely fake news (confidence: {confidence_pct:.1f}%)."
            label_display = "Fake News"
        elif label == "LABEL_1":
            exp = f"The AI model estimates this text is likely reliable (confidence: {confidence_pct:.1f}%)."
            label_display = "Real News"
        else:
            exp = f"Label: {label} (confidence: {confidence_pct:.1f}%)"
            label_display = label
        return label_display, confidence_pct, exp
    except Exception as e:
        return "Error", 0, f"Error during analysis: {str(e)}"

if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "first_load" not in st.session_state:
    st.session_state.first_load = True

example_text = ("The moon landing was staged. ") # Example text for demonstration purposes

st.title("ProbablyFake AlmostTrue - an attempt to Detect Fake News")

# Affichage du champ texte : exemple seulement au premier chargement
if st.session_state.first_load and st.session_state.input_text == "":
    default_text = example_text
    st.session_state.input_text = example_text  # Synchroniser avec la session
else:
    default_text = st.session_state.input_text

text = st.text_area("Paste or enter text to analyze (English):", height=200, value=default_text, key="input_text_area", max_chars=500)

# Synchroniser automatiquement le texte avec la session à chaque changement
if text != st.session_state.input_text and not st.session_state.first_load:
    st.session_state.input_text = text

col1, col2 = st.columns([1,1])
analyze_clicked = col1.button("Analyze")
reset_clicked = col2.button("Reset")

if analyze_clicked:
    # Forcer la mise à jour du texte et nettoyer l'état précédent
    st.session_state.input_text = text
    st.session_state.show_results = True
    st.session_state.first_load = False
    # Forcer le rechargement pour s'assurer que l'état est propre
    st.rerun()
if reset_clicked:
    st.session_state.input_text = ""
    st.session_state.show_results = False
    st.session_state.first_load = False
    st.rerun()

if st.session_state.show_results:
    # S'assurer qu'on utilise le bon texte pour l'analyse
    current_text = st.session_state.input_text.strip()
    if current_text:
        st.subheader("AI Analysis (RoBERTa)")
        with st.spinner("AI analysis in progress..."):
            label_display, ia_confidence, ia_exp = ia_fake_news_score(current_text)
            st.metric("AI Result", label_display, delta=f"Confidence: {ia_confidence:.1f}%")
            st.write(ia_exp)
            st.info("ℹ️ This RoBERTa model is specifically trained for fake news detection on English texts. Ne pas essayer avec du texte en français les petits loulous !")

        st.subheader("Google Fact Check Results")
        if GOOGLE_FACTCHECK_API_KEY:
            claims = search_fact_check(current_text, GOOGLE_FACTCHECK_API_KEY)
            if claims:
                for claim in claims:
                    st.write(f"- **Claim:** {claim.get('text', 'N/A')}")
                    for review in claim.get('claimReview', []):
                        st.write(f"    - Source: [{review.get('publisher', {}).get('name', 'N/A')}]({review.get('url', '')})")
                        st.write(f"    - Rating: {review.get('textualRating', 'N/A')}")
            else:
                st.info("No fact check results found for this text.")
        else:
            st.info("Google Fact Check API key not configured. Please add it to access this feature.")

        st.subheader("Related News Articles (NewsAPI)")
        if NEWSAPI_KEY:
            articles = search_newsapi(current_text, NEWSAPI_KEY)
            if articles:
                for article in articles:
                    st.write(f"- [{article.get('title', 'N/A')}]({article.get('url', '')})")
                    st.write(f"    - Source: {article.get('source', {}).get('name', 'N/A')}")
                    st.write(f"    - Published: {article.get('publishedAt', 'N/A')}")
                    st.write(f"    - Description: {article.get('description', 'N/A')}")
            else:
                st.info("No related news articles found.")
        else:
            st.info("NewsAPI key not configured. Please add it to access this feature.")

        st.subheader(f"Wikipedia Search - More info about: {current_text[:50]}{'...' if len(current_text) > 50 else ''}")
        wiki_results = search_wikipedia(current_text)
        if wiki_results:
            for result in wiki_results:
                title = result.get('title', 'N/A')
                snippet = result.get('snippet', '').replace('<span class="searchmatch">', '').replace('</span>', '')
                pageid = result.get('pageid')
                url = f"https://en.wikipedia.org/?curid={pageid}" if pageid else ""
                st.write(f"- [{title}]({url})")
                st.write(f"    - {snippet} ...")
        else:
            st.info("No Wikipedia results found for this text.")
    else:
        st.info("Please enter text to analyze.")
