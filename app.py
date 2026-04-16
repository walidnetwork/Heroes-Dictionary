import streamlit as st
import time
import base64
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Alabtal AI Dictionary", layout="centered", initial_sidebar_state="collapsed")

# --- 2. دالة تحويل الموارد لعملها برمجياً (Base64) ---
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
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e40af 100%); color: white; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(90deg, #ef4444, #b91c1c); color: white; font-weight: bold; height: 50px; }
    h1, h2, h3, p { font-family: 'Cairo', sans-serif; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

if 'stage' not in st.session_state:
    st.session_state.stage = 'splash'

# --- المرحلة 1: شاشة الترحيب ---
if st.session_state.stage == 'splash':
    placeholder = st.empty()
    with placeholder.container():
        logo_data = get_base64('logo_animated.gif')
        audio_data = get_base64('start_theme.wav')
        st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; height: 80vh; flex-direction: column; text-align: center;">
                {"<img src='data:image/gif;base64," + logo_data + "' width='300'>" if logo_data else "<h2>Alabtal Dictionary</h2>"}
                {"<audio autoplay><source src='data:audio/wav;base64," + audio_data + "' type='audio/wav'></audio>" if audio_data else ""}
                <h2 style='margin-top:20px; color:white;'>مرحباً بك يا بطل...</h2>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(5)
    st.session_state.stage = 'select_grade'
    st.rerun()

# --- المرحلة 2: اختيار الصف ---
elif st.session_state.stage == 'select_grade':
    st.markdown("<h1>🦸‍♂️ اختر صفك الدراسي</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    grades_list = [("Grade 1", "cover_g1.jpg"), ("Grade 2", "cover_g2.jpg"), ("Grade 3", "cover_g3.jpg"),
                   ("Grade 4", "cover_g4.jpg"), ("Grade 5", "cover_g5.jpg"), ("Grade 6", "cover_g6.jpg")]
    
    for i, (name, img_file) in enumerate(grades_list):
        with [col1, col2, col3][i % 3]:
            if os.path.exists(img_file): st.image(img_file, use_container_width=True)
            if st.button(name, key=name):
                st.session_state.grade = name.replace(" ", "").lower() # تصبح g1, g2...
                st.session_state.stage = 'select_term'
                st.rerun()

# --- المرحلة 3: اختيار الترم ---
elif st.session_state.stage == 'select_term':
    st.markdown(f"<h1>📚 {st.session_state.grade.upper()} - اختر الترم</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    
    with c1:
        t1_img = f"cover_{st.session_state.grade}_t1.jpg"
        if os.path.exists(t1_img): st.image(t1_img)
        if st.button("الترم الأول", key="t1"):
            st.session_state.term = "t1"
            st.session_state.stage = 'main_search'
            st.rerun()
            
    with c2:
        t2_img = f"cover_{st.session_state.grade}_t2.png"
        if os.path.exists(t2_img): st.image(t2_img)
        if st.button("الترم الثاني", key="t2"):
            st.session_state.term = "t2"
            st.session_state.stage = 'main_search'
            st.rerun()

# --- المرحلة 4: واجهة البحث المرتبطة بالـ PDF ---
elif st.session_state.stage == 'main_search':
    # تحديد اسم ملف الـ PDF بناءً على الاختيارات
    # مثال: g5_t1.pdf
    pdf_file_name = f"{st.session_state.grade}_{st.session_state.term}.pdf"
    
    st.markdown(f"<h3>منهج {st.session_state.grade.upper()} - {st.session_state.term.upper()}</h3>", unsafe_allow_html=True)
    st.title("🔍 ابحث عن الكلمة")
    
    query = st.text_input("اكتب الكلمة بالإنجليزية:")
    
    if query:
        if os.path.exists(pdf_file_name):
            st.success(f"جاري البحث عن '{query}' داخل ملف {pdf_file_name}...")
            # هنا سنضع لاحقاً دالة استخراج الصور والنطق من هذا الملف تحديداً
        else:
            st.error(f"عذراً يا بطل، ملف الـ PDF ({pdf_file_name}) غير موجود حالياً.")

    if st.button("🔙 عودة للقائمة الرئيسية"):
        st.session_state.stage = 'select_grade'
        st.rerun()
