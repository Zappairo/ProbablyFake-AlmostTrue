import streamlit as st
import re
from transformers import pipeline

def simple_fake_news_score(text):
    scoreSimpleRules = 0
    explanations = []
    # Rule 1: sensational words
    sensational_words = ["incredible", "shocking", "revealed", "urgent", "scandal", "impossible", "secret", "breaking", "exclusive", "Aliens",]
    found = [w for w in sensational_words if w in text.lower()]
    if found:
        scoreSimpleRules += 40
        explanations.append(f"Sensational words detected: {', '.join(found)}")
    # Rule 2: absence of reliable sources
    if not re.search(r"source|Reuters|AFP|BBC|CNN|NY Times|Associated Press", text, re.IGNORECASE):
        scoreSimpleRules += 30
        explanations.append("No reliable sources detected in the text.")
    # Rule 3: excessive capitals
    if sum(1 for c in text if c.isupper()) > len(text) * 0.2:
        scoreSimpleRules += 20
        explanations.append("Excessive use of capital letters, alarmist tone.")
    # Score max 100
    scoreSimpleRules = min(scoreSimpleRules, 100)
    return scoreSimpleRules, explanations

MODEL_NAME = "hamzab/roberta-fake-news-classification"

@st.cache_resource
def get_fake_news_pipeline():
    return pipeline("text-classification", model=MODEL_NAME, tokenizer=MODEL_NAME)

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

example_text = ("Breaking: Scientists have discovered that aliens from Mars have been secretly living among us for decades. "
                "This incredible information was revealed by an anonymous source, but no evidence has been provided. "
                "Experts claim this is an unprecedented scandal in modern history and could have far-reaching implications in the 9/11 attacks, the elections of Donald Trump, and the reason behind the COVID-19 pandemic.")

st.title("ProbablyFake AlmostTrue - an attempt to Detect Fake News")
text = st.text_area("Paste or enter text to analyze (English):", height=200, value=st.session_state.input_text or example_text, key="input_text_area")

col1, col2 = st.columns([1,1])
analyze_clicked = col1.button("Analyze")
reset_clicked = col2.button("Reset")

if analyze_clicked:
    st.session_state.input_text = text
    st.session_state.show_results = True
if reset_clicked:
    st.session_state.input_text = ""
    st.session_state.show_results = False
    st.rerun()

if st.session_state.show_results:
    if st.session_state.input_text.strip():
        st.subheader("AI Analysis (RoBERTa)")
        with st.spinner("AI analysis in progress..."):
            label_display, ia_confidence, ia_exp = ia_fake_news_score(st.session_state.input_text)
            st.metric("AI Result", label_display, delta=f"Confidence: {ia_confidence:.1f}%")
            st.write(ia_exp)
            st.info("ℹ️ This RoBERTa model is specifically trained for fake news detection on English texts. Ne pas essayer avec du texte en français les petits loulous !")

        scoreSimpleRules, explanations = simple_fake_news_score(st.session_state.input_text)
        st.write(f"**Simple Rules Analysis: Score {scoreSimpleRules}/100 (the higher the score, the more likely it is to be real news)**")
        for exp in explanations:
            st.write(f"- {exp}")
    else:
        st.info("Please enter text to analyze.")
