import streamlit as st
import pandas as pd
import base64
from gtts import gTTS
import io
import os
import fitz  # PyMuPDF
import re

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Heroes Dictionary", page_icon="🦸‍♂️", layout="wide")

# --- 2. دالات المساعدة ---
def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

def speak(text):
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

def advanced_search(pdf_path, word):
    extracted_sentences = []
    full_pages = []
    if not os.path.exists(pdf_path):
        return [], []
    
    try:
        doc = fitz.open(pdf_path)
        word_pattern = re.compile(rf'\b{re.escape(word)}\b', re.IGNORECASE)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            
            if word_pattern.search(text):
                # 1. استخراج الصفحات (مهم جداً إضافتها أولاً)
                pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
                img_data = pix.tobytes("png")
                full_pages.append({"num": page_num + 1, "image": img_data})

                # 2. استخراج الجمل
                lines = text.split('\n')
                for line in lines:
                    clean_line = line.strip()
                    if word_pattern.search(clean_line) and len(clean_line) > 3:
                        # تمييز الكلمة باللون الأحمر
                        display_text = re.sub(word_pattern, f"<b style='color:#ef4444;'>{word}</b>", clean_line)
                        if clean_line not in [s['raw'] for s in extracted_sentences]:
                            extracted_sentences.append({
                                "display": display_text,
                                "raw": clean_line,
                                "page": page_num + 1
                            })
        doc.close()
    except Exception as e:
        st.error(f"خطأ في قراءة الكتاب: {e}")
        
    return extracted_sentences, full_pages

# --- 3. واجهة المستخدم والتصميم ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stappviewcontainer"] {
        direction: rtl; text-align: right; font-family: 'Cairo', sans-serif;
        background-color: #1e293b; color: white;
    }
    .stButton>button { width: 100%; border-radius: 12px; background: #ef4444; color: white; font-weight: bold; height: 3em; }
    .section-header { border-right: 5px solid #ef4444; padding-right: 15px; margin: 25px 0; color: #f1f5f9; }
    .sentence-box { background: #334155; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #ef4444; }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق التنقل ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- 5. الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown("<h1 style='text-align:center;'>🦸‍♂️ قاموس الأبطال</h1>", unsafe_allow_html=True)
    logo = get_base64('logo.png')
    if logo:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo}" width="200"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        query = st.text_input("🔍 ابحث عن كلمة", placeholder="اكتب الكلمة هنا...").strip()
        if query:
            st.session_state.search_word = query
            st.session_state.page = 'results'
            st.rerun()

# --- 6. صفحة النتائج ---
elif st.session_state.page == 'results':
    word = st.session_state.search_word
    st.markdown(f"<h2 style='text-align:center;'>🔍 نتائج البحث عن: {word}</h2>", unsafe_allow_html=True)
    
    sentences, pages = advanced_search('book.pdf', word)
    
    # 🔊 النطق
    st.markdown(f"<h3 class='section-header'>🔊 نطق الكلمة: {word}</h3>", unsafe_allow_html=True)
    st.audio(speak(word))
    
    # 📝 عرض الجمل
    if sentences:
        st.markdown("<h3 class='section-header'>📝 جمل من الكتاب</h3>", unsafe_allow_html=True)
        for s in sentences[:8]:
            st.markdown(f"<div class='sentence-box'>📄 {s['display']}</div>", unsafe_allow_html=True)
            if st.button(f"🔊 استمع للجملة", key=f"voice_{s['raw']}"):
                st.audio(speak(s['raw']))
    
    # 📖 عرض الصفحات
    if pages:
        st.markdown("<h3 class='section-header'>📖 صفحات من الكتاب</h3>", unsafe_allow_html=True)
        for p in pages:
            st.image(p['image'], caption=f"صفحة {p['num']}", use_container_width=True)
    
    if not sentences and not pages:
        st.warning(f"عذراً يا بطل، لم نجد '{word}' في الكتاب.")

    if st.button("🔙 عودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()

# --- 7. التذييل ---
st.markdown("<br><hr>", unsafe_allow_html=True)
p_img = get_base64('personal_photo.jpg')
if p_img:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/jpeg;base64,{p_img}" style="width:100px; border-radius:50%; border:2px solid #ef4444;"></div>', unsafe_allow_html=True)
st.markdown("<div style='text-align:center;'>Created by Mr. Walid Elhagary</div>", unsafe_allow_html=True)
