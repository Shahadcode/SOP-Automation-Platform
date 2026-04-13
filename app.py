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

# ================== CSS (FINAL CLEAN) ==================
st.markdown("""
<style>

/* ===== Base ===== */
.stApp {
    background-color: #EAF5F2;
}

/* Remove Streamlit junk */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background-color: #DCEFE8;
}

/* ===== Header ===== */
.hero {
    background: #0f766e;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
}

.hero-title {
    color: white;
    font-size: 28px;
    font-weight: 800;
    text-align: right;
    direction: rtl;
}

.hero-sub {
    color: #dff7f3;
    font-size: 14px;
    text-align: right;
    direction: rtl;
}

/* ===== Text ===== */
.rtl {
    direction: rtl;
    text-align: right;
}

/* ===== Inputs ===== */
div[data-baseweb="select"] > div {
    border-radius: 10px !important;
    border: 2px solid #0f766e !important;
}

div[data-baseweb="select"] span {
    direction: rtl !important;
    text-align: right !important;
}

/* ===== Radio FIX ===== */
div[data-testid="stRadio"] {
    direction: rtl;
}

div[data-testid="stRadio"] label {
    display: flex !important;
    flex-direction: row-reverse !important;
    justify-content: flex-end !important;
    gap: 8px;
    width: 100%;
}

div[data-testid="stRadio"] p {
    text-align: right !important;
    width: 100%;
}

/* ===== Buttons ===== */
.stButton button {
    background: #0f766e;
    color: white;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
}

/* ===== Cards ===== */
.card {
    background: #f8fafc;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #ddd;
    direction: rtl;
    text-align: right;
}

.success {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    padding: 10px;
    border-radius: 10px;
    direction: rtl;
    text-align: right;
}

/* Footer */
.footer {
    text-align: center;
    color: #777;
    font-size: 12px;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# ================== Helpers ==================
def read_uploaded_file(uploaded_file):
    if uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    if uploaded_file.name.endswith(".docx"):
        doc = Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

    return None


# ================== Sidebar ==================
with st.sidebar:
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=150)

    st.markdown("<div class='rtl'><b>التنقل</b></div>", unsafe_allow_html=True)

    page = st.radio("", ["إنشاء الإجراء", "معلومات النظام"])


# ================== Header ==================
def header(title, subtitle):
    c1, c2 = st.columns([6,1])

    with c1:
        st.markdown(f"""
        <div class="hero">
            <div class="hero-title">{title}</div>
            <div class="hero-sub">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        if os.path.exists("assets/logo.png"):
            st.image("assets/logo.png", width=110)


# ================== PAGE 1 ==================
if page == "إنشاء الإجراء":

    header("منصة أتمتة الإجراءات",
           "تحويل الإجراءات المكتوبة إلى نموذج SOP رسمي")

    col_left, col_right = st.columns([1,1.2])

    # ===== RIGHT (FORM) =====
    with col_right:

        st.markdown("<div class='rtl'><b>رفع بيانات الإجراء</b></div>", unsafe_allow_html=True)

        st.markdown("<div class='rtl'>رفع الإجراء</div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=["txt","docx"])

        st.markdown("<div class='rtl'>القسم</div>", unsafe_allow_html=True)
        department = st.selectbox("", ["المالية","العمليات","الامتثال"])

        st.markdown("<div class='rtl'>اللغة</div>", unsafe_allow_html=True)
        language = st.selectbox("", ["العربية"])

        st.markdown("<div class='rtl'>وضع العمل</div>", unsafe_allow_html=True)

        mode = st.radio(
            "",
            ["استخراج مباشر من النص", "إعادة صياغة احترافية"]
        )

        mode_value = "extract" if mode == "استخراج مباشر من النص" else "rewrite"

        generate = st.button("إنشاء الإجراء")

    # ===== LEFT (INFO) =====
    with col_left:

        st.markdown("<div class='rtl'><b>الحالة والتعليمات</b></div>", unsafe_allow_html=True)

        if uploaded_file:
            st.markdown("<div class='success'>تم رفع الملف بنجاح</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card'>اسم الملف: {uploaded_file.name}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='card'>يرجى رفع ملف</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class='card'>
        <b>ملاحظات:</b><br>
        • يدعم TXT و Word<br>
        • يتم إنشاء SOP عربي<br>
        • نفس قالب البنك
        </div>
        """, unsafe_allow_html=True)

    # ===== PROCESS =====
    if uploaded_file and generate:
        text = read_uploaded_file(uploaded_file)

        if text:
            try:
                data = generate_sop_data(
                    text=text,
                    department=department,
                    language=language,
                    mode=mode_value
                )

                file_path = create_sop_doc_from_template(data)

                st.success("تم إنشاء الملف")

                with open(file_path, "rb") as f:
                    st.download_button(
                        "تحميل",
                        f,
                        file_name="SOP.docx"
                    )

            except Exception as e:
                st.error(str(e))


# ================== PAGE 2 ==================
else:

    header("معلومات النظام","شرح النظام")

    st.markdown("""
    <div class='card'>
    هذه المنصة تقوم بتحويل الإجراءات إلى SOP.
    </div>
    """, unsafe_allow_html=True)


# ================== FOOTER ==================
st.markdown("<div class='footer'>Internal Use Only</div>", unsafe_allow_html=True)
