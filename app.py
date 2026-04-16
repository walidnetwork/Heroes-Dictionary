import streamlit as st
import base64
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Alabtal AI Dictionary", layout="wide", initial_sidebar_state="collapsed")

# --- 2. دالة جلب الصور ---
def get_base64(bin_file):
    if os.path.exists(bin_file):
        try:
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()
        except: return ""
    return ""

# --- 3. تصميم واجهة الأبطال (بدون بهتان) ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(to bottom, #1e3a8a, #0f172a); /* تدرج أزرق ملكي */
        color: white;
    }}
    .main-header {{
        text-align: center;
        padding: 20px;
    }}
    .logo-img {{
        width: 200px;
        filter: drop-shadow(0px 0px 10px rgba(255,255,255,0.3));
    }}
    .grade-card {{
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: 0.3s;
    }
    .stButton>button {{
        width: 100%;
        border-radius: 10px;
        background: #ef4444; /* الأحمر الناري */
        color: white;
        font-weight: bold;
        border: none;
        height: 45px;
    }
    </style>
    """, unsafe_allow_html=True)

# إدارة الحالة (Navigation)
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- الصفحة الرئيسية (اختيار الصفوف) ---
if st.session_state.page == 'home':
    # عرض اللوجو في الأعلى (ثابت)
    logo_data = get_base64('logo_animated.gif') # سيعمل كصورة ثابتة أو متحركة حسب الملف
    st.markdown(f"""
        <div class="main-header">
            <img src="data:image/gif;base64,{logo_data}" class="logo-img">
            <h1 style='font-family: Cairo;'>قاموس الأبطال للغة الإنجليزية</h1>
            <p>اختر صفك الدراسي لتبدأ رحلة التعلم</p>
        </div>
    """, unsafe_allow_html=True)

    # عرض الصفوف
    col1, col2, col3 = st.columns(3)
    grades = [
        ("Grade 1", "cover_g1.jpg"), ("Grade 2", "cover_g2.jpg"), ("Grade 3", "cover_g3.jpg"),
        ("Grade 4", "cover_g4.jpg"), ("Grade 5", "cover_g5.jpg"), ("Grade 6", "cover_g6.jpg")
    ]

    for i, (name, img) in enumerate(grades):
        with [col1, col2, col3][i % 3]:
            if os.path.exists(img):
                st.image(img, use_container_width=True)
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
        if st.button("الترم الأول"):
            st.session_state.term, st.session_state.page = "t1", "search"
            st.rerun()

    with c2:
        t2_img = f"cover_{st.session_state.grade}_t2.png"
        if os.path.exists(t2_img): st.image(t2_img, use_container_width=True)
        if st.button("الترم الثاني"):
            st.session_state.term, st.session_state.page = "t2", "search"
            st.rerun()
    
    if st.button("🔙 عودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()

# --- صفحة البحث ---
elif st.session_state.page == 'search':
    st.title("🔍 محرك البحث")
    st.write(f"الصف: {st.session_state.grade.upper()} | الترم: {st.session_state.term.upper()}")
    
    query = st.text_input("اكتب الكلمة بالإنجليزية:")
    if st.button("🔙 تغيير الصف"):
        st.session_state.page = 'home'
        st.rerun()
