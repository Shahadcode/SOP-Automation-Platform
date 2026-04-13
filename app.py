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
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 15px;
    color: #dff7f3;
    margin-bottom: 0;
    text-align: right;
    direction: rtl;
    line-height: 1.6;
}

/* ===== Text blocks ===== */
.rtl-title {
    font-size: 20px;
    font-weight: 700;
    color: #134e4a;
    margin-bottom: 14px;
    margin-top: 8px;
    text-align: right;
    direction: rtl;
}

.rtl-label {
    font-size: 15px;
    font-weight: 600;
    color: #134e4a;
    margin-bottom: 6px;
    margin-top: 12px;
    text-align: right;
    direction: rtl;
}

.info-card {
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 14px;
    padding: 18px;
    text-align: right;
    direction: rtl;
    line-height: 1.9;
}

.success-card {
    background-color: #ecfdf5;
    color: #065f46;
    border: 1px solid #a7f3d0;
    border-radius: 12px;
    padding: 12px 14px;
    font-weight: 600;
    margin-bottom: 10px;
    text-align: right;
    direction: rtl;
}

/* ===== Markdown text alignment ===== */
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li,
div[data-testid="stMarkdownContainer"] strong {
    text-align: right !important;
    direction: rtl !important;
}

/* ===== File uploader ===== */
div[data-testid="stFileUploader"] section {
    background: #ffffff;
    border-radius: 14px;
    border: 2px dashed #0f766e;
    padding: 10px;
}

div[data-testid="stFileUploader"] * {
    direction: rtl !important;
    text-align: right !important;
}

/* ===== Select boxes ===== */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 2px solid #0f766e !important;
    border-radius: 12px !important;
    min-height: 46px !important;
    box-shadow: none !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] input,
div[data-baseweb="select"] svg {
    direction: rtl !important;
    text-align: right !important;
}

/* ===== Radio buttons ===== */
div[data-testid="stRadio"] {
    direction: rtl !important;
}

div[data-testid="stRadio"] label {
    display: flex !important;
    flex-direction: row-reverse !important;
    justify-content: flex-end !important;
    gap: 8px !important;
    width: 100% !important;
}

div[data-testid="stRadio"] p {
    text-align: right !important;
    direction: rtl !important;
    width: 100% !important;
    margin: 0 !important;
}

/* ===== Alerts ===== */
[data-testid="stAlert"] {
    direction: rtl !important;
    text-align: right !important;
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

.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #115e59;
    color: white;
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


with st.sidebar:
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=180)

    st.markdown('<div class="sidebar-title">منصة أتمتة الإجراءات</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">First Iraqi Bank - Internal Tool</div>', unsafe_allow_html=True)

    page = st.radio("التنقل", ["إنشاء الإجراء", "معلومات النظام"])


def render_header(title: str, subtitle: str):
    c_text, c_logo = st.columns([6, 1], gap="small")
    with c_text:
        st.markdown(
            f"""
            <div class="hero-box">
                <div class="hero-title">{title}</div>
                <div class="hero-subtitle">{subtitle}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c_logo:
        if os.path.exists("assets/logo.png"):
            st.image("assets/logo.png", width=120)


if page == "إنشاء الإجراء":
    render_header(
        "منصة أتمتة الإجراءات",
        "تحويل الإجراءات المكتوبة إلى نموذج SOP رسمي بنفس الصيغة المعتمدة في البنك."
    )

    col_info, col_form = st.columns([0.9, 1.1], gap="large")

    with col_form:
        st.markdown('<div class="rtl-title">رفع بيانات الإجراء</div>', unsafe_allow_html=True)

        st.markdown('<div class="rtl-label">رفع الإجراء</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "رفع الإجراء",
            type=["txt", "docx"],
            label_visibility="collapsed",
        )

        st.markdown('<div class="rtl-label">القسم</div>', unsafe_allow_html=True)
        department = st.selectbox(
            "القسم",
            ["المالية", "العمليات", "الامتثال", "إدارة المخاطر", "التدقيق الداخلي", "أخرى"],
            label_visibility="collapsed",
        )

        st.markdown('<div class="rtl-label">اللغة</div>', unsafe_allow_html=True)
        language = st.selectbox(
            "اللغة",
            ["العربية"],
            label_visibility="collapsed",
        )

        st.markdown('<div class="rtl-label">وضع العمل</div>', unsafe_allow_html=True)
        mode = st.radio(
            "وضع العمل",
            ["استخراج مباشر من النص", "إعادة صياغة احترافية"],
            label_visibility="collapsed",
        )

        if mode == "استخراج مباشر من النص":
            st.info("سيتم الاعتماد على نص المستند المرفوع قدر الإمكان، مع أقل قدر ممكن من الاختصار أو إعادة الصياغة.")
            mode_value = "extract"
        else:
            st.info("سيتم تحسين الصياغة وتنظيم المحتوى بشكل مهني مع الحفاظ على المعنى الأساسي.")
            mode_value = "rewrite"

        generate_btn = st.button("إنشاء الإجراء")

    with col_info:
        st.markdown('<div class="rtl-title">الحالة والتعليمات</div>', unsafe_allow_html=True)

        if uploaded_file:
            st.markdown('<div class="success-card">تم رفع الملف بنجاح.</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="info-card"><b>اسم الملف:</b> {uploaded_file.name}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<div class="info-card">يرجى رفع ملف Word أو TXT للبدء.</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card" style="margin-top:14px;">
        <b>ملاحظات مهمة:</b><br><br>
        • يدعم النظام ملفات Word و TXT<br>
        • يتم إنشاء الإجراء باللغة العربية الرسمية<br>
        • يتم إخراج النتيجة بنفس نموذج الـ SOP المعتمد<br>
        • يفضل أن يكون النص المرفوع واضحاً ومكتوباً بشكل منظم
        </div>
        """, unsafe_allow_html=True)

    if uploaded_file and generate_btn:
        text = read_uploaded_file(uploaded_file)

        if text:
            with st.spinner("جاري إنشاء الإجراء..."):
                try:
                    sop_data = generate_sop_data(
                        text=text,
                        department=department,
                        language=language,
                        mode=mode_value,
                    )
                    file_path = create_sop_doc_from_template(sop_data)

                    st.success("تم إنشاء ملف الإجراء بنجاح.")

                    with open(file_path, "rb") as f:
                        st.download_button(
                            "تحميل ملف الإجراء",
                            f,
                            file_name="Generated_SOP_Arabic.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        )
                except Exception as e:
                    st.error(f"حدث خطأ أثناء إنشاء الملف: {str(e)}")
        else:
            st.error("تعذر قراءة الملف المرفوع.")

elif page == "معلومات النظام":
    render_header(
        "معلومات النظام",
        "نظرة عامة على وظيفة المنصة وآلية الاستخدام."
    )

    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown('<div class="rtl-title">ماذا تقوم به المنصة؟</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="info-card">تقوم المنصة بتحويل الإجراءات المكتوبة إلى نموذج SOP رسمي باللغة العربية وبنفس الصيغة المعتمدة داخل البنك.<br><br>كما تقوم بتنسيق المحتوى داخل القالب المحدد، بما يشمل المقدمة، الأنظمة المشاركة، الهدف، منطق المطابقة، وخطوات الإجراء.</div>',
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown('<div class="rtl-title">كيفية الاستخدام</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="info-card">1. قم برفع ملف الإجراء.<br>2. اختر القسم.<br>3. اختر وضع العمل المناسب.<br>4. اضغط على زر إنشاء الإجراء.<br>5. قم بتحميل ملف الـ SOP الجاهز.</div>',
            unsafe_allow_html=True,
        )

st.markdown('<div class="footer-note">Internal Use Only - SOP Automation Platform</div>', unsafe_allow_html=True)
