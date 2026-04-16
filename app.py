import streamlit as st
import base64
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Alabtal AI Dictionary", layout="wide")

# --- 2. دالة جلب الصور ---
def get_base64(bin_file):
    if os.path.exists(bin_file):
        try:
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()
        except: return ""
    return ""

# --- 3. تصميم الواجهة المحسن للرؤية ---
st.markdown("""
    <style>
    /* خلفية متدرجة احترافية */
    .stApp {
        background: linear-gradient(to bottom, #1e3a8a, #0f172a);
        color: white;
    }
    
    /* توضيح النصوص التي تظهر فوق مربعات الإدخال */
    label {
        color: #f1f5f9 !important; /* لون أبيض مائل للزرقة خفيف */
        font-size: 1.2rem !important;
        font-weight: bold !important;
        font-family: 'Cairo', sans-serif;
    }

    /* تحسين شكل مربع البحث نفسه */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #0f172a !important;
        border-radius: 10px !important;
        font-weight: bold;
    }

    /* تحسين العناوين */
    h1, h2, h3 {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    .main-header { text-align: center; padding: 10px; }
    .logo-img { width: 180px; margin-bottom: 10px; }
    
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: #ef4444;
        color: white;
        font-weight: bold;
        height: 45px;
        border: none;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    
    /* إخفاء القوائم غير الضرورية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. نظام التنقل ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    logo_data = get_base64('logo_animated.gif')
    if logo_data:
        st.markdown(f'<div class="main-header"><img src="data:image/gif;base64,{logo_data}" class="logo-img"></div>', unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; font-family: Cairo;'>قاموس الأبطال للغة الإنجليزية</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    grades = [
        ("Grade 1", "cover_g1.jpg"), ("Grade 2", "cover_g2.jpg"), ("Grade 3", "cover_g3.jpg"),
        ("Grade 4", "cover_g4.jpg"), ("Grade 5", "cover_g5.jpg"), ("Grade 6", "cover_g6.jpg")
    ]

    for i, (name, img_path) in enumerate(grades):
        with [col1, col2, col3][i % 3]:
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            if st.button(f"دخول {name}", key=name):
                st.session_state.grade = name.replace(" ", "").lower()
                st.session_state.page = 'select_term'
                st.rerun()

# --- صفحة اختيار الترم ---
elif st.session_state.page == 'select_term':
    st.markdown(f"<h2 style='text-align:center;'>📚 منهج {st.session_state.grade.upper()}</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    
    with c1:
        t1_img = f"cover_{st.session_state.grade}_t1.jpg"
        if os.path.exists(t1_img): st.image(t1_img, use_container_width=True)
        if st.button("الترم الأول", key="t1"):
            st.session_state.term, st.session_state.page = "t1", "search"
            st.rerun()

    with c2:
        t2_img = f"cover_{st.session_state.grade}_t2.png"
        if os.path.exists(t2_img): st.image(t2_img, use_container_width=True)
        if st.button("الترم الثاني", key="t2"):
            st.session_state.term, st.session_state.page = "t2", "search"
            st.rerun()
    
    if st.button("🔙 العودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()

# --- صفحة البحث المحدثة ---
elif st.session_state.page == 'search':
    st.markdown(f"<h2 style='text-align:center;'>🔍 محرك بحث {st.session_state.grade.upper()} - {st.session_state.term.upper()}</h2>", unsafe_allow_html=True)
    
    # مربع البحث مع تسمية واضحة جداً
    query = st.text_input("أدخل الكلمة الإنجليزية التي تبحث عنها:")
    
    if query:
        st.markdown(f"<p style='color: #fbbf24; font-size: 1.5rem;'>جاري البحث عن: {query}...</p>", unsafe_allow_html=True)
        
    if st.button("🔙 تغيير الصف"):
        st.session_state.page = 'home'
        st.rerun()
