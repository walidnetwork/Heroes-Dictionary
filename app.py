import streamlit as st
import time
import base64
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Alabtal AI Dictionary", layout="centered", initial_sidebar_state="collapsed")

# --- 2. دالة آمنة لتحويل الملفات (تتجنب توقف التطبيق) ---
def get_base64(bin_file):
    if os.path.exists(bin_file):
        try:
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()
        except:
            return ""
    return ""

# --- 3. تصميم الواجهة (CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e40af 100%); color: white; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(90deg, #ef4444, #b91c1c); color: white; font-weight: bold; height: 50px; }
    h1, h2, h3, p { font-family: 'Cairo', sans-serif; text-align: center; }
    img { border-radius: 15px; box-shadow: 0px 10px 20px rgba(0,0,0,0.3); }
    </style>
    """, unsafe_allow_html=True)

if 'stage' not in st.session_state:
    st.session_state.stage = 'splash'

# --- المرحلة 1: شاشة الترحيب ---
if st.session_state.stage == 'splash':
    placeholder = st.empty()
    with placeholder.container():
        # التأكد من أسماء الملفات كما في GitHub
        logo_data = get_base64('logo_animated.gif')
        audio_data = get_base64('start_theme.wav')
        
        html_code = f"""
            <div style="display: flex; justify-content: center; align-items: center; height: 80vh; flex-direction: column; text-align: center;">
                {"<img src='data:image/gif;base64," + logo_data + "' width='300'>" if logo_data else "<h2>Heroes Dictionary</h2>"}
                {"<audio autoplay><source src='data:audio/wav;base64," + audio_data + "' type='audio/wav'></audio>" if audio_data else ""}
                <h2 style='margin-top:20px; color:white;'>جاري التحميل يا بطل...</h2>
            </div>
        """
        st.markdown(html_code, unsafe_allow_html=True)
        time.sleep(6)
    st.session_state.stage = 'select_grade'
    st.rerun()

# --- المرحلة 2: اختيار الصف ---
elif st.session_state.stage == 'select_grade':
    st.markdown("<h1>🦸‍♂️ اختر صفك الدراسي</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    # مصفوفة الصفوف
    grades_list = [
        ("Grade 1", "cover_g1.jpg"), ("Grade 2", "cover_g2.jpg"), ("Grade 3", "cover_g3.jpg"),
        ("Grade 4", "cover_g4.jpg"), ("Grade 5", "cover_g5.jpg"), ("Grade 6", "cover_g6.jpg")
    ]
    
    for i, (name, img_file) in enumerate(grades_list):
        with [col1, col2, col3][i % 3]:
            if os.path.exists(img_file):
                st.image(img_file, use_container_width=True)
            else:
                st.warning(f"Missing: {name}")
            
            if st.button(name, key=name):
                st.session_state.grade = name.replace(" ", "").upper()
                st.session_state.stage = 'select_term'
                st.rerun()

# --- المرحلة 3: اختيار الترم ---
elif st.session_state.stage == 'select_term':
    st.markdown(f"<h1>📚 {st.session_state.grade} - اختر الترم</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    
    # ترم 1 (JPG)
    t1_img = f"cover_{st.session_state.grade.lower()}_t1.jpg"
    with c1:
        if os.path.exists(t1_img): st.image(t1_img)
        if st.button("الترم الأول"):
            st.session_state.term, st.session_state.stage = "T1", "main_search"
            st.rerun()
            
    # ترم 2 (PNG)
    t2_img = f"cover_{st.session_state.grade.lower()}_t2.png"
    with c2:
        if os.path.exists(t2_img): st.image(t2_img)
        if st.button("الترم الثاني"):
            st.session_state.term, st.session_state.stage = "T2", "main_search"
            st.rerun()

# --- المرحلة 4: البحث ---
elif st.session_state.stage == 'main_search':
    st.title("🔍 ابحث عن كلمتك")
    st.write(f"منهج {st.session_state.grade} - {st.session_state.term}")
    query = st.text_input("اكتب الكلمة:")
    if st.button("🔙 عودة"):
        st.session_state.stage = 'select_grade'
        st.rerun()
