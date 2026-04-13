import os
import streamlit as st
from docx import Document
from sop_engine import generate_sop_data
from doc_generator import create_sop_doc_from_template

st.set_page_config(
    page_title="منصة أتمتة الإجراءات",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>

/* ===== Base ===== */
.stApp {
    background-color: #EAF5F2;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 100% !important;
}

/* ===== Hide Streamlit chrome ===== */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent !important;}
[data-testid="stToolbar"] {display: none !important;}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background-color: #DCEFE8 !important;
    border-left: 2px solid #B9DDD2 !important;
    box-shadow: -4px 0 14px rgba(0,0,0,0.06) !important;
}

.sidebar-title {
    font-size: 20px;
    font-weight: 700;
    color: #134e4a;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 4px;
}

.sidebar-subtitle {
    font-size: 12px;
    color: #4b5563;
    text-align: center;
    margin-bottom: 20px;
}

/* ===== Header ===== */
.hero-box {
    background: #0f766e;
    border-radius: 18px;
    padding: 22px 24px;
    margin-bottom: 18px;
    box-shadow: 0 8px 18px rgba(15, 118, 110, 0.18);
}

.hero-title {
    font-size: 30px;
    font-weight: 800;
    color: white;
    margin-bottom: 8px;
    text-align: right;
    direction: rtl;
}

.hero-subtitle {
    font-size: 15px;
    color: #dff7f3;
    margin-bottom: 0;
    text-align: right;
    direction: rtl;
}

/* ===== RTL TEXT ===== */
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li,
div[data-testid="stMarkdownContainer"] strong {
    text-align: right !important;
    direction: rtl !important;
}

/* ===== Inputs ===== */
div[data-testid="stFileUploader"] *,
div[data-baseweb="select"] *,
[data-testid="stAlert"] {
    direction: rtl !important;
    text-align: right !important;
}

/* ===== RADIO FIX (THIS IS THE ONLY CHANGE) ===== */
div[data-testid="stRadio"] {
    direction: rtl !important;
    text-align: right !important;
    width: 100% !important;
}

div[data-testid="stRadio"] [role="radiogroup"] {
    direction: rtl !important;
    text-align: right !important;
    width: 100% !important;
}

div[data-testid="stRadio"] [role="radiogroup"] label {
    display: flex !important;
    flex-direction: row-reverse !important; /* circle RIGHT */
    justify-content: flex-start !important;
    align-items: center !important;
    gap: 10px !important;
    width: 100% !important;
    margin-bottom: 10px !important;
}

div[data-testid="stRadio"] [role="radiogroup"] p {
    margin: 0 !important;
    width: 100% !important;
    text-align: right !important;
    direction: rtl !important;
}

/* ===== Buttons ===== */
.stButton > button,
.stDownloadButton > button {
    width: 100%;
    background-color: #0f766e;
    color: white;
    border: none;
    border-radius: 12px;
    height: 48px;
    font-size: 16px;
    font-weight: 700;
}

.stButton > button:hover {
    background-color: #115e59;
}

/* ===== Footer ===== */
.footer-note {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    margin-top: 28px;
}

</style>
""", unsafe_allow_html=True)


def read_uploaded_file(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    if file_name.endswith(".docx"):
        doc = Document(uploaded_file)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)

    return None


# ===== Sidebar =====
with st.sidebar:
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=180)

    st.markdown('<div class="sidebar-title">منصة أتمتة الإجراءات</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">First Iraqi Bank - Internal Tool</div>', unsafe_allow_html=True)

    page = st.radio("التنقل", ["إنشاء الإجراء", "معلومات النظام"])


def render_header(title, subtitle):
    c_text, c_logo = st.columns([6, 1])
    with c_text:
        st.markdown(f"""
        <div class="hero-box">
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)

    with c_logo:
        if os.path.exists("assets/logo.png"):
            st.image("assets/logo.png", width=120)


# ===== MAIN PAGE =====
if page == "إنشاء الإجراء":
    render_header(
        "منصة أتمتة الإجراءات",
        "تحويل الإجراءات المكتوبة إلى نموذج SOP رسمي بنفس الصيغة المعتمدة في البنك."
    )

    col_info, col_form = st.columns([0.9, 1.1])

    with col_form:
        st.markdown("### رفع بيانات الإجراء")

        uploaded_file = st.file_uploader("رفع الإجراء", type=["txt", "docx"])

        department = st.selectbox("القسم", ["المالية", "العمليات", "الامتثال"])

        language = st.selectbox("اللغة", ["العربية"])

        st.markdown("### وضع العمل")

        # ✅ FIXED RADIO
        mode = st.radio(
            "",
            ["استخراج مباشر من النص", "إعادة صياغة احترافية"],
            label_visibility="collapsed",
            horizontal=False,
        )

        if mode == "استخراج مباشر من النص":
            st.info("سيتم الاعتماد على النص كما هو")
            mode_value = "extract"
        else:
            st.info("سيتم إعادة الصياغة بشكل احترافي")
            mode_value = "rewrite"

        if st.button("إنشاء الإجراء"):

            if uploaded_file:
                text = read_uploaded_file(uploaded_file)

                if text:
                    sop_data = generate_sop_data(text, department, language, mode_value)
                    file_path = create_sop_doc_from_template(sop_data)

                    with open(file_path, "rb") as f:
                        st.download_button(
                            "تحميل الملف",
                            f,
                            file_name="SOP.docx"
                        )
                else:
                    st.error("فشل قراءة الملف")

    with col_info:
        st.markdown("### الحالة والتعليمات")

        if uploaded_file:
            st.success("تم رفع الملف بنجاح")
        else:
            st.info("يرجى رفع ملف")

# ===== FOOTER =====
st.markdown('<div class="footer-note">Internal Use Only - SOP Automation Platform</div>', unsafe_allow_html=True)
