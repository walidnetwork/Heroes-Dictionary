import streamlit as st
import base64
import os
import fitz  # PyMuPDF
from gtts import gTTS
import io
import re

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Alabtal AI Dictionary", layout="wide")

# --- 2. دالة النطق الذكي ---
def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp.getvalue()
    except:
        return None

# --- 3. دالة جلب الصور ---
def get_base64(bin_file):
    if os.path.exists(bin_file):
        try:
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()
        except: return ""
    return ""

# --- 4. المحرك الذكي للبحث والاستخلاص ---
def deep_search(pdf_path, word):
    results = []
    if not os.path.exists(pdf_path):
        return None
    
    doc = fitz.open(pdf_path)
    word_pattern = re.compile(re.escape(word), re.IGNORECASE)
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        
        # البحث عن الجمل التي تحتوي على الكلمة
        sentences = re.split(r'(?<=[.!?])\s+', text)
        for sentence in sentences:
            if word_pattern.search(sentence):
                clean_sentence = sentence.replace('\n', ' ').strip()
                
                # الحصول على مكان الكلمة لقص الصورة (Context Image)
                inst = page.search_for(word)
                img_data = None
                if inst:
                    # قص منطقة واسعة حول الكلمة لإظهار التصميم والصورة
                    rect = inst[0]
                    clip = fitz.Rect(0, rect.y0 - 60, page.rect.width, rect.y1 + 100)
                    pix = page.get_pixmap(clip=clip, matrix=fitz.Matrix(1.5, 1.5))
                    img_data = pix.tobytes("png")
                
                results.append({
                    "page": page_num + 1,
                    "sentence": clean_sentence,
                    "image": img_data
                })
                if len(results) >= 10: break # حد أقصى 10 نتائج للسرعة
        if len(results) >= 10: break
    return results

# --- 5. تنسيق الواجهة (CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #1e3a8a, #0f172a); color: white; }
    .result-card { 
        background: rgba(255,255,255,0.08); 
        padding: 20px; 
        border-radius: 20px; 
        margin-bottom: 25px; 
        border-right: 5px solid #ef4444;
    }
    .sentence-text { font-size: 1.3rem; color: #fbbf24; font-weight: bold; margin-bottom: 10px; }
    .page-label { background: #ef4444; padding: 2px 10px; border-radius: 5px; font-size: 0.8rem; }
    .stTextInput input { background-color: white !important; color: black !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 6. نظام التنقل والصفحات ---
if 'page' not in st.session_state: st.session_state.page = 'home'

if st.session_state.page == 'home':
    # عرض اللوجو والصفوف (كما في الكود السابق)
    logo = get_base64('logo_animated.gif')
    if logo: st.markdown(f'<center><img src="data:image/gif;base64,{logo}" width="180"></center>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>قاموس الأبطال</h1>", unsafe_allow_html=True)
    
    # شبكة الصفوف
    c1, c2, c3 = st.columns(3)
    for i, g in enumerate(["g1", "g2", "g3"]):
        with [c1, c2, c3][i]:
            if st.button(f"الصف {i+1}", key=g):
                st.session_state.grade_id, st.session_state.page = g, 'select_term'; st.rerun()
    c4, c5, c6 = st.columns(3)
    for i, g in enumerate(["g4", "g5", "g6"]):
        with [c4, col5, col6][i]: # ملاحظة: تأكد من تعريف col5, col6 أو استبدالها بـ c5, c6
             if st.button(f"الصف {i+4}", key=g):
                st.session_state.grade_id, st.session_state.page = g, 'select_term'; st.rerun()

elif st.session_state.page == 'select_term':
    st.markdown("<h1 style='text-align:center;'>📚 اختر الترم</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    gid = st.session_state.grade_id
    with col1:
        if st.button("الترم الأول"): st.session_state.term, st.session_state.page = "t1", "search"; st.rerun()
    with col2:
        if st.button("الترم الثاني"): st.session_state.term, st.session_state.page = "t2", "search"; st.rerun()

# --- صفحة البحث والنتائج المتطورة ---
elif st.session_state.page == 'search':
    st.markdown(f"<h2 style='text-align:center;'>🔍 محرك البحث الذكي</h2>", unsafe_allow_html=True)
    query = st.text_input("ابحث عن كلمة إنجليزية:")
    
    if query:
        pdf_file = f"{st.session_state.grade_id}_{st.session_state.term}.pdf"
        with st.spinner('بطلنا يحلل كتاب المدرسة الآن...'):
            data = deep_search(pdf_file, query)
            
            if data:
                st.info(f"وجدنا '{query}' في {len(data)} موضعاً مختلفاً:")
                for item in data:
                    with st.container():
                        st.markdown(f"""
                        <div class="result-card">
                            <span class="page-label">Page: {item['page']}</span>
                            <p class="sentence-text">{item['sentence']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_img, col_spk = st.columns([3, 1])
                        with col_img:
                            if item['image']: st.image(item['image'], caption="صورة من الكتاب")
                        with col_spk:
                            st.write("🔊 اسمع الجملة")
                            audio = speak(item['sentence'])
                            if audio: st.audio(audio, format='audio/mp3')
            elif data is None:
                st.error("ملف الكتاب غير موجود على السيرفر.")
            else:
                st.warning("الكلمة غير موجودة في هذا الكتاب.")

    if st.button("🔙 عودة للرئيسية"): st.session_state.page = 'home'; st.rerun()
