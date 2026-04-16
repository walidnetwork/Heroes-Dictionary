import streamlit as st
import base64
import os
import fitz  # PyMuPDF
from gtts import gTTS
import io
import re

# --- 1. إعدادات الصفحة (يجب أن تكون في البداية) ---
st.set_page_config(page_title="Alabtal AI Dictionary", layout="wide")

# --- 2. دالة النطق ---
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

# --- 4. المحرك الذكي للبحث واستخلاص الجمل والصفحات ---
def deep_search(pdf_path, word):
    results = []
    if not os.path.exists(pdf_path):
        return None
    
    try:
        doc = fitz.open(pdf_path)
        word_pattern = re.compile(re.escape(word), re.IGNORECASE)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            
            # تقسيم النص إلى جمل
            sentences = re.split(r'(?<=[.!?])\s+', text)
            for sentence in sentences:
                if word_pattern.search(sentence):
                    clean_sentence = sentence.replace('\n', ' ').strip()
                    
                    # الحصول على إحداثيات الكلمة لقص الصورة
                    inst = page.search_for(word)
                    img_data = None
                    if inst:
                        rect = inst[0]
                        # قص منطقة عرضية كاملة لإظهار السياق
                        clip = fitz.Rect(0, rect.y0 - 70, page.rect.width, rect.y1 + 120)
                        pix = page.get_pixmap(clip=clip, matrix=fitz.Matrix(1.5, 1.5))
                        img_data = pix.tobytes("png")
                    
                    results.append({
                        "page": page_num + 1,
                        "sentence": clean_sentence,
                        "image": img_data
                    })
                    if len(results) >= 8: break
            if len(results) >= 8: break
        return results
    except:
        return []

# --- 5. تصميم الواجهة (CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #1e3a8a, #0f172a); color: white; }
    .result-card { 
        background: rgba(255,255,255,0.1); 
        padding: 15px; 
        border-radius: 15px; 
        margin-bottom: 20px; 
        border-right: 6px solid #ef4444;
    }
    .sentence-text { font-size: 1.2rem; color: #fbbf24; font-weight: bold; }
    .page-tag { background: #ef4444; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; }
    .stTextInput input { background-color: white !important; color: black !important; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 10px; background: #ef4444; color: white; font-weight: bold; height: 45px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 6. نظام التنقل ---
if 'page' not in st.session_state: st.session_state.page = 'home'

# --- الصفحة الرئيسية (ترتيب إجباري) ---
if st.session_state.page == 'home':
    logo = get_base64('logo_animated.gif')
    if logo: st.markdown(f'<center><img src="data:image/gif;base64,{logo}" width="180"></center>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-family: Cairo;'>قاموس الأبطال</h1>", unsafe_allow_html=True)
    
    # الصفوف 1-3
    r1_c1, r1_c2, r1_c3 = st.columns(3)
    grades1 = [("g1", "الصف الأول"), ("g2", "الصف الثاني"), ("g3", "الصف الثالث")]
    for i, (gid, gname) in enumerate(grades1):
        with [r1_c1, r1_c2, r1_c3][i]:
            img = f"cover_{gid}.jpg"
            if os.path.exists(img): st.image(img, use_container_width=True)
            if st.button(f"دخول {gname}", key=gid):
                st.session_state.grade_id, st.session_state.page = gid, 'select_term'; st.rerun()

    # الصفوف 4-6
    r2_c1, r2_c2, r2_c3 = st.columns(3)
    grades2 = [("g4", "الصف الرابع"), ("g5", "الصف الخامس"), ("g6", "الصف السادس")]
    for i, (gid, gname) in enumerate(grades2):
        with [r2_c1, r2_c2, r2_c3][i]:
            img = f"cover_{gid}.jpg"
            if os.path.exists(img): st.image(img, use_container_width=True)
            if st.button(f"دخول {gname}", key=gid):
                st.session_state.grade_id, st.session_state.page = gid, 'select_term'; st.rerun()

# --- صفحة اختيار الترم ---
elif st.session_state.page == 'select_term':
    st.markdown("<h1 style='text-align:center;'>📚 اختر الترم الدراسي</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    gid = st.session_state.grade_id
    with col1:
        t1 = f"cover_{gid}_t1.jpg"
        if os.path.exists(t1): st.image(t1, use_container_width=True)
        if st.button("الترم الأول", key="t1_btn"):
            st.session_state.term, st.session_state.page = "t1", "search"; st.rerun()
    with col2:
        t2 = f"cover_{gid}_t2.jpg"
        if os.path.exists(t2): st.image(t2, use_container_width=True)
        if st.button("الترم الثاني", key="t2_btn"):
            st.session_state.term, st.session_state.page = "t2", "search"; st.rerun()
    if st.button("🔙 العودة للرئيسية"): st.session_state.page = 'home'; st.rerun()

# --- صفحة البحث والنتائج ---
elif st.session_state.page == 'search':
    st.markdown(f"<h2 style='text-align:center;'>🔍 محرك بحث {st.session_state.grade_id.upper()}</h2>", unsafe_allow_html=True)
    query = st.text_input("ادخل الكلمة الإنجليزية:")
    
    if query:
        pdf_file = f"{st.session_state.grade_id}_{st.session_state.term}.pdf"
        with st.spinner('بطلنا يفتش في صفحات الكتاب...'):
            data = deep_search(pdf_file, query)
            
            if data:
                for item in data:
                    with st.container():
                        st.markdown(f"""
                        <div class="result-card">
                            <span class="page-tag">Page {item['page']}</span>
                            <p class="sentence-text">{item['sentence']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # عرض الصورة والنطق
                        c_img, c_audio = st.columns([2, 1])
                        with c_img:
                            if item['image']: st.image(item['image'])
                        with c_audio:
                            st.write("🔊 نطق الجملة:")
                            audio = speak(item['sentence'])
                            if audio: st.audio(audio, format='audio/mp3')
                        st.write("---")
            elif data is None:
                st.error(f"ملف الكتاب {pdf_file} غير موجود.")
            else:
                st.warning("لم يتم العثور على الكلمة في هذا الكتاب.")

    if st.button("🔙 تغيير الصف أو الترم"): st.session_state.page = 'home'; st.rerun()
