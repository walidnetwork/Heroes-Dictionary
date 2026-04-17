import streamlit as st
import pandas as pd
import base64
from gtts import gTTS
import io
import os
import fitz  # PyMuPDF
from PIL import Image

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
    results = []
    pages_to_show = []
    word_lower = word.lower()
    
    if os.path.exists(pdf_path):
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            lines = text.split('\n')
            
            # البحث عن الجمل
            for line in lines:
                if word_lower in line.lower():
                    results.append({'raw': line.strip(), 'page': page_num + 1})
            
            # البحث عن الصفحات الكاملة
            if word_lower in text.lower():
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_data = pix.tobytes("png")
                pages_to_show.append({'num': page_num + 1, 'image': img_data})
        doc.close()
    return results, pages_to_show

# --- 3. تحميل البيانات ---
@st.cache_data
def load_data():
    df = pd.read_excel('words.xlsx')
    return df

try:
    df = load_data()
except:
    st.error("يرجى التأكد من وجود ملف words.xlsx")
    st.stop()

# --- 4. واجهة المستخدم والتصميم (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stappviewcontainer"] {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: #1e293b;
        color: white;
    }
    .main-title { color: #f8fafc; text-align: center; margin-bottom: 20px; font-size: 3rem; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3em; background: #ef4444; color: white; border: none; font-weight: bold; }
    .section-header { border-right: 5px solid #ef4444; padding-right: 15px; margin: 20px 0; color: #f1f5f9; }
    </style>
""", unsafe_allow_html=True)

# --- 5. منطق التنقل ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- 6. الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown("<h1 class='main-title'>🦸‍♂️ قاموس الأبطال</h1>", unsafe_allow_html=True)
    
    # شعار الأبطال
    logo = get_base64('logo.png')
    if logo:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo}" width="250"></div>', unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align:center;'>ALABTAL DICTIONARY</h3>", unsafe_allow_html=True)
    
    search_col1, search_col2, search_col3 = st.columns([1, 2, 1])
    with search_col2:
        query = st.text_input("🔍 ابحث عن كلمة (مثلاً: Beach)", placeholder="ادخل الكلمة هنا...").strip()
        if query:
            st.session_state.search_word = query
            st.session_state.page = 'results'
            st.rerun()

# --- 7. صفحة النتائج ---
elif st.session_state.page == 'results':
    word = st.session_state.search_word
    st.markdown(f"<h1 style='text-align:center;'>🔍 محرك بحث الأبطال</h1>", unsafe_allow_html=True)
    st.write(f"### نتائج البحث عن: **{word}**")
    
    sentences, pages = advanced_search('book.pdf', word)
    
    if sentences or pages:
        # نطق الكلمة
        st.markdown(f"<h3 class='section-header'>🔊 نطق الكلمة: {word}</h3>", unsafe_allow_html=True)
        s_audio = speak(word)
        st.audio(s_audio)
        
        # عرض الجمل
        if sentences:
            st.markdown("<h3 class='section-header'>📝 جمل تحتوي على الكلمة</h3>", unsafe_allow_html=True)
            for s in sentences[:5]:
                st.info(f"📄 {s['raw']}")
                if st.button(f"🔊 استمع للجملة", key=f"btn_{s['raw']}"):
                    st.audio(speak(s['raw']))
        
        # عرض الصفحات
        if pages:
            st.markdown("<h3 class='section-header'>📖 صفحات الكتاب كاملة</h3>", unsafe_allow_html=True)
            for p in pages:
                st.image(p['image'], caption=f"صفحة رقم {p['num']}", use_container_width=True)
        
        if st.button("🔙 عودة"):
            st.session_state.page = 'home'
            st.rerun()
    else:
        st.warning("⚠️ لم نجد نتائج لهذه الكلمة")
        if st.button("🔙 عودة"):
            st.session_state.page = 'home'
            st.rerun()

# --- 8. التذييل (Footer) ---
st.markdown("<br><br>", unsafe_allow_html=True)
f_c1, f_c2, f_c3 = st.columns([1, 2, 1])
with f_c2:
    st.markdown("<div style='text-align:center; border-top: 1px solid #475569; padding-top: 20px;'>", unsafe_allow_html=True)
    p_img = get_base64('personal_photo.jpg')
    if p_img:
        st.markdown(f'<img src="data:image/jpeg;base64,{p_img}" style="width:110px; border-radius:50%; border:3px solid #ef4444;">', unsafe_allow_html=True)
    st.markdown("### Created by Mr. Walid Elhagary")
    st.markdown("[![Facebook](https://img.shields.io/badge/Facebook-Follow%20Our%20Series-blue?style=for-the-badge&logo=facebook)](https://www.facebook.com/share/15fGv6mC8C/)")
    st.markdown("</div>", unsafe_allow_html=True)
