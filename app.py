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

# --- 3. تصميم الواجهة (CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #1e3a8a, #0f172a); color: white; }
    label { color: #f1f5f9 !important; font-weight: bold !important; font-family: 'Cairo', sans-serif; }
    .stTextInput input { background-color: rgba(255, 255, 255, 0.9) !important; color: #000 !important; border-radius: 10px !important; }
    .main-header { text-align: center; padding: 10px; }
    .logo-img { width: 180px; margin-bottom: 10px; }
    .stButton>button { width: 100%; border-radius: 10px; background: #ef4444; color: white; font-weight: bold; height: 50px; border: none; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    logo_data = get_base64('logo_animated.gif')
    if logo_data:
        st.markdown(f'<div class="main-header"><img src="data:image/gif;base64,{logo_data}" class="logo-img"></div>', unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; font-family: Cairo;'>قاموس الأبطال للغة الإنجليزية</h1>", unsafe_allow_html=True)
    
    grades = [
        ("Grade 1", "cover_g1.jpg"), ("Grade 2", "cover_g2.jpg"), ("Grade 3", "cover_g3.jpg"),
        ("Grade 4", "cover_g4.jpg"), ("Grade 5", "cover_g5.jpg"), ("Grade 6", "cover_g6.jpg")
    ]

    cols = st.columns(3)
    for i, (name, img_path) in enumerate(grades):
        with cols[i % 3]:
            # التحقق من وجود غلاف الصف
            if not os.path.exists(img_path): img_path = img_path.replace(".jpg", ".png")
            if os.path.exists(img_path): st.image(img_path, use_container_width=True)
            
            if st.button(f"دخول {name}", key=name):
                # هنا نحفظ g1, g2 إلخ لتستخدم في أسماء الملفات
                st.session_state.grade_id = name.replace("Grade ", "g").lower() 
                st.session_state.page = 'select_term'
                st.rerun()

# --- صفحة اختيار الترم ---
elif st.session_state.page == 'select_term':
    gid = st.session_state.grade_id # g1, g2...
    st.markdown(f"<h2 style='text-align:center; font-family: Cairo;'>📚 اختر الترم - {gid.upper()}</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # البحث عن غلاف الترم 1 بأسماء مثل cover_g1_t1.jpg
        t1_name = f"cover_{gid}_t1.jpg"
        if not os.path.exists(t1_name): t1_name = f"cover_{gid}_t1.png"
        
        if os.path.exists(t1_name):
            st.image(t1_name, caption="الترم الأول", use_container_width=True)
        else:
            st.warning(f"⚠️ مفقود: {t1_name}")
        
        if st.button("تصفح الترم الأول", key="t1"):
            st.session_state.term, st.session_state.page = "t1", "search"
            st.rerun()

    with col2:
        # البحث عن غلاف الترم 2 بأسماء مثل cover_g1_t2.jpg
        t2_name = f"cover_{gid}_t2.jpg"
        if not os.path.exists(t2_name): t2_name = f"cover_{gid}_t2.png"
        
        if os.path.exists(t2_name):
            st.image(t2_name, caption="الترم الثاني", use_container_width=True)
        else:
            st.warning(f"⚠️ مفقود: {t2_name}")
            
        if st.button("تصفح الترم الثاني", key="t2"):
            st.session_state.term, st.session_state.page = "t2", "search"
            st.rerun()
    
    if st.button("🔙 العودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()

# --- صفحة البحث ---
elif st.session_state.page == 'search':
    st.title("🔍 محرك البحث")
    st.write(f"الصف: {st.session_state.grade_id.upper()} | الترم: {st.session_state.term.upper()}")
    if st.button("🔙 عودة"):
        st.session_state.page = 'home'
        st.rerun()
