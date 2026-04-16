import streamlit as st
import base64
import os
import fitz  # PyMuPDF
from gtts import gTTS
import io
import re

# --- 1. إعدادات الصفحة والهوية ---
st.set_page_config(
    page_title="ALABTAL DICTIONARY",
    page_icon="logo_animated.gif",
    layout="wide"
)

# --- 2. دالة النطق ---
def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp.getvalue()
    except: return None

# --- 3. دالة جلب الصور ---
def get_base64(bin_file):
    if os.path.exists(bin_file):
        try:
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()
        except: return ""
    return ""

# --- 4. محرك البحث الذكي (استخراج جمل + صفحات كاملة) ---
def advanced_search(pdf_path, word):
    extracted_sentences = []
    full_pages = []
    
    if not os.path.exists(pdf_path): return None, None
    
    try:
        doc = fitz.open(pdf_path)
        word_pattern = re.compile(re.escape(word), re.IGNORECASE)
        
        found_pages_indices = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            
            if word_pattern.search(text):
                # 1. استخراج الجمل منفصلة
                sentences = re.split(r'(?<=[.!?])\s+', text)
                for sentence in sentences:
                    if word_pattern.search(sentence):
                        clean_s = sentence.replace('\n', ' ').strip()
                        if clean_s not in [s['text'] for s in extracted_sentences]:
                            extracted_sentences.append({"text": clean_s, "page": page_num + 1})

                # 2. حفظ الصفحة كاملة كصورة
                if page_num not in found_pages_indices:
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # جودة عالية
                    full_pages.append({"num": page_num + 1, "image": pix.tobytes("png")})
                    found_pages_indices.append(page_num)
                    
            if len(full_pages) >= 5: break # تحديد النتائج للسرعة
            
        return extracted_sentences, full_pages
    except: return [], []

# --- 5. تصميم الواجهة (CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #1e3a8a, #0f172a); color: white; }
    .sentence-card { 
        background: white; 
        color: #0f172a; 
        padding: 20px; 
        border-radius: 15px; 
        margin-bottom: 10px; 
        border-left: 8px solid #ef4444;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    .sentence-text { font-size: 1.4rem; font-weight: bold; margin-bottom: 5px; }
    .page-info { color: #64748b; font-size: 0.9rem; }
    .section-title { border-bottom: 2px solid #ef4444; padding-bottom: 10px; margin-top: 30px; margin-bottom: 20px; font-family: 'Cairo'; }
    .stTextInput input { background-color: white !important; color: black !important; font-weight: bold; border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 10px; background: #ef4444; color: white; font-weight: bold; height: 50px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 6. نظام التنقل ---
if 'page' not in st.session_state: st.session_state.page = 'home'

# --- الصفحة الرئيسية واختيار الترم (نفس الهيكل السابق المستقر) ---
if st.session_state.page == 'home':
    logo = get_base64('logo_animated.gif')
    if logo: st.markdown(f'<center><img src="data:image/gif;base64,{logo}" width="200"></center>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-family: Cairo;'>قاموس الأبطال</h1>", unsafe_allow_html=True)
    for row in [["g1", "g2", "g3"], ["g4", "g5", "g6"]]:
        cols = st.columns(3)
        for i, gid in enumerate(row):
            with cols[i]:
                img = f"cover_{gid}.jpg"
                if os.path.exists(img): st.image(img, use_container_width=True)
                if st.button(f"دخول الصف {gid[1]}", key=gid):
                    st.session_state.grade_id, st.session_state.page = gid, 'select_term'; st.rerun()

elif st.session_state.page == 'select_term':
    st.markdown("<h1 style='text-align:center; font-family: Cairo;'>📚 اختر الترم الدراسي</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    gid = st.session_state.grade_id
    for i, t in enumerate(["t1", "t2"]):
        with [col1, col2][i]:
            img = f"cover_{gid}_{t}.jpg"
            if os.path.exists(img): st.image(img, use_container_width=True)
            if st.button(f"تصفح الترم {'الأول' if t=='t1' else 'الثاني'}", key=t):
                st.session_state.term, st.session_state.page = t, 'search'; st.rerun()
    if st.button("🔙 عودة"): st.session_state.page = 'home'; st.rerun()

# --- صفحة البحث والنتائج الجديدة ---
elif st.session_state.page == 'search':
    st.markdown(f"<h2 style='text-align:center;'>🔍 محرك بحث الأبطال</h2>", unsafe_allow_html=True)
    query = st.text_input("ادخل الكلمة (English):")
    
    if query:
        # 1. نطق الكلمة الأساسية
        st.markdown(f"### 🔊 نطق الكلمة: {query}")
        q_audio = speak(query)
        if q_audio: st.audio(q_audio)
        
        pdf_file = f"{st.session_state.grade_id}_{st.session_state.term}.pdf"
        with st.spinner('بطلنا يحلل كتاب المدرسة...'):
            sentences, pages = advanced_search(pdf_file, query)
            
            if sentences:
                # 2. عرض الجمل المستخلصة
                st.markdown("<h3 class='section-title'>📝 جمل من المنهج</h3>", unsafe_allow_html=True)
                for s in sentences:
                    st.markdown(f"""
                    <div class="sentence-card">
                        <p class="sentence-text">{s['text']}</p>
                        <p class="page-info">ذكرت في صفحة: {s['page']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.write("🔊 استمع للجملة:")
                    s_audio = speak(s['text'])
                    if s_audio: st.audio(s_audio)
                
                # 3. عرض الصفحات كاملة
                st.markdown("<h3 class='section-title'>📖 صفحات الكتاب كاملة</h3>", unsafe_allow_html=True)
                for p in pages:
                    st.markdown(f"**الصفحة رقم: {p['num']}**")
                    st.image(p['image'], use_container_width=True)
                    st.write("---")
            else:
                st.warning("لم نجد نتائج للكلمة المطلوبة.")

    if st.button("🔙 عودة للرئيسية"): st.session_state.page = 'home'; st.rerun()

# --- التذييل (Footer) ---
st.markdown("---")
f_col1, f_col2, f_col3 = st.columns([1, 2, 1])
with f_col2:
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    p_img = get_base64('personal_photo.jpg')
    if p_img: st.markdown(f'<img src="data:image/jpeg;base64,{p_img}" style="width:100px; border-radius:50%; border:3px solid #ef4444;">', unsafe_allow_html=True)
    st.markdown("### Created by Mr. Walid")
    st.markdown("[![Facebook](https://img.shields.io/badge/Facebook-Follow%20Us-blue?style=for-the-badge&logo=facebook)](https://www.facebook.com/your-page-link)")
    st.markdown("</div>", unsafe_allow_html=True)
