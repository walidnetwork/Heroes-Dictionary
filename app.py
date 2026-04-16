import streamlit as st
import time
import base64

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="Alabtal AI Dictionary",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. دالة تحويل الموارد لعملها برمجياً (Base64) ---
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception as e:
        return ""

# --- 3. تحسين الواجهة بـ CSS وتنسيق الألوان ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e40af 100%);
        color: white;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #ef4444, #b91c1c);
        color: white;
        font-weight: bold;
        border: none;
        height: 50px;
        font-size: 18px;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-5px);
        box-shadow: 0px 8px 20px rgba(239, 68, 68, 0.6);
        color: white;
    }
    h1, h2, h3, p {
        font-family: 'Cairo', sans-serif;
        text-align: center;
    }
    img {
        border-radius: 20px;
        box-shadow: 0px 15px 25px rgba(0,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# إدارة حالة التطبيق
if 'stage' not in st.session_state:
    st.session_state.stage = 'splash'

# --- المرحلة 1: شاشة الترحيب الاحترافية (Splash Screen) ---
if st.session_state.stage == 'splash':
    placeholder = st.empty()
    with placeholder.container():
        logo_b64 = get_base64('logo_animated.gif')
        audio_b64 = get_base64('start_theme.wav')
        
        st.markdown(f"""
            <div id="splash-container" style="display: flex; justify-content: center; align-items: center; height: 80vh; flex-direction: column; text-align: center;">
                <img src="data:image/gif;base64,{logo_b64}" width="320" style="margin-bottom: 30px;">
                <audio autoplay>
                    <source src="data:audio/wav;base64,{audio_b64}" type="audio/wav">
                </audio>
                <h2 class="fade-text">عالم الأبطال يرحب بك.. جاهز للتعلم؟</h2>
            </div>
            
            <style>
                @keyframes fadeInOut {{
                    0% {{ opacity: 0; }}
                    15% {{ opacity: 1; }}
                    85% {{ opacity: 1; }}
                    100% {{ opacity: 0; }}
                }}
                .fade-text {{
                    animation: fadeInOut 7s forwards;
                    color: #f8fafc;
                    font-family: Cairo;
                }
                #splash-container {{
                    animation: fadeInOut 7s forwards;
                }
            </style>
        """, unsafe_allow_html=True)
        
        # وقت الانتظار البرمجي (7.5 ثانية لضمان اكتمال الأنيميشن)
        time.sleep(7.5) 
        
    st.session_state.stage = 'select_grade'
    st.rerun()

# --- المرحلة 2: واجهة اختيار الصف الدراسي ---
elif st.session_state.stage == 'select_grade':
    st.markdown("<h1 style='margin-bottom: 30px;'>🦸‍♂️ اختر صفك الدراسي</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # قائمة الصفوف والملفات
    grades = [
        ("Grade 1", "cover_g1.jpg"), ("Grade 2", "cover_g2.jpg"), ("Grade 3", "cover_g3.jpg"),
        ("Grade 4", "cover_g4.jpg"), ("Grade 5", "cover_g5.jpg"), ("Grade 6", "cover_g6.jpg")
    ]
    
    for i, (g_name, g_img) in enumerate(grades):
        with [col1, col2, col3][i % 3]:
            st.image(g_img, use_container_width=True)
            if st.button(f"{g_name}", key=f"btn_{g_name}"):
                st.session_state.grade = g_name.replace(" ", "").upper()
                st.session_state.stage = 'select_term'
                st.rerun()

# --- المرحلة 3: واجهة اختيار الترم الدراسي ---
elif st.session_state.stage == 'select_term':
    st.markdown(f"<h1>📚 {st.session_state.grade} - اختر الترم</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        img_t1 = f"cover_{st.session_state.grade.lower()}_t1.jpg"
        st.image(img_t1, caption="الترم الأول", use_container_width=True)
        if st.button("الترم الأول", key="t1_btn"):
            st.session_state.term = "T1"
            st.session_state.stage = 'main_search'
            st.rerun()
            
    with col2:
        img_t2 = f"cover_{st.session_state.grade.lower()}_t2.png"
        st.image(img_t2, caption="الترم الثاني", use_container_width=True)
        if st.button("الترم الثاني", key="t2_btn"):
            st.session_state.term = "T2"
            st.session_state.stage = 'main_search'
            st.rerun()

# --- المرحلة 4: واجهة البحث النهائية ---
elif st.session_state.stage == 'main_search':
    current_cover = f"cover_{st.session_state.grade.lower()}_t1.jpg" if st.session_state.term == "T1" else f"cover_{st.session_state.grade.lower()}_t2.png"
    
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="data:image/png;base64,{get_base64(current_cover)}" width="140">
            <h3 style="margin-top: 10px;">منهج {st.session_state.grade} - {st.session_state.term}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.title("🔍 محرك بحث الأبطال")
    
    query = st.text_input("ادخل الكلمة بالإنجليزية:", placeholder="e.g. Science")
    
    if query:
        st.info(f"جاري البحث عن '{query}'...")

    if st.button("🔙 العودة لاختيار الصفوف"):
        st.session_state.stage = 'select_grade'
        st.rerun()
