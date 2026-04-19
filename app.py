import streamlit as st
import base64
from gtts import gTTS
import io
import os
import fitz  # PyMuPDF
import re

# --- 1. إعدادات الهوية ---
st.set_page_config(
    page_title="ALABTAL SEARCH ENGINE", 
    page_icon="logo.png",
    layout="wide"
)

# --- 2. دوال البحث والنطق المستقرة ---
def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return None

@st.cache_data(show_spinner=False)
def speak_clean(text):
    clean_text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
    tts = gTTS(text=clean_text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()

def advanced_search(pdf_path, word):
    extracted_sentences, full_pages = [], []
    if not os.path.exists(pdf_path): return [], []
    try:
        doc = fitz.open(pdf_path)
