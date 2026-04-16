import streamlit as st
import base64
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Alabtal AI Dictionary", layout="wide")

# --- 2. دالة جلب الصور بأمان ---
def get_base64(bin_file):
    if os.path.exists(bin_file):
        try:
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()
        except: return ""
    return ""

# --- 3. تصميم الواجهة (CSS) لتحسين الرؤية والترتيب ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #1e3a8a, #0f172a);
        color: white;
    }
    label {
        color: #f1f5f9 !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        font-family: 'Cairo', sans-serif;
    }
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #000 !important;
        border-radius: 10px !important;
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
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. نظام التنقل ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- الصفحة الرئيسية (بترتيب الصفوف الصحيح) ---
if st.session_state.page == 'home':
    logo_data = get_base64('logo_animated.gif')
    if logo_data:
        st.markdown(f'<div class="main-header"><img src="data:image/gif;base64,{logo_data}" class="logo-img"></div>', unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; font-family: Cairo;'>قاموس الأبطال للغة الإنجليزية</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>اختر صفك الدراسي لتبدأ</p>", unsafe_allow_html=True)

    # الترتيب الصحيح للصفوف (1-2-3 ثم 4-5-6)
    grades = [
        ("Grade 1", "cover_g1.jpg"), ("Grade 2", "cover_g2.jpg"), ("Grade 3", "cover_g3.jpg"),
        ("Grade 4", "cover_g4.jpg"), ("Grade 5", "cover_g5.jpg"), ("Grade 6", "cover_g6.jpg")
    ]

    # إنشاء الصفوف البرمجية
    row1 = st.columns(3)
    row2 = st.columns(3)
    
    all_columns = row1 + row2 # دمجهم لسهولة التوزيع

    for i, (name, img_path) in enumerate(grades):
        with all_columns[i]:
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.info(f"كتاب {name}")
            
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
    
    st.write("---")
    if st.button("🔙 العودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()

# --- صفحة البحث ---
elif st.session_state.page == 'search':
    st.markdown(f"<h3 style='text-align:center;'>🔍 محرك بحث {st.session_state.grade.upper()} - {st.session_state.term.upper()}</h3>", unsafe_allow_html=True)
    
    query = st.text_input("أدخل الكلمة الإنجليزية التي تبحث عنها:")
    if query:
        st.markdown(f"<p style='color: #fbbf24; text-align:center;'>جاري البحث عن: {query}...</p>", unsafe_allow_html=True)
        
    if st.button("🔙 تغيير الصف"):
        st.session_state.page = 'home'
        st.rerun()
