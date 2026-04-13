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

st.markdown(
    """
<style>
/* ===== Base ===== */
html, body, [class*="css"] {
    direction: rtl;
}

.stApp {
    background-color: #EAF5F2;
}

.block-container {
    padding-top: 0.6rem !important;
    padding-bottom: 1rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 100% !important;
}

/* ===== Hide Streamlit chrome ===== */
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0rem !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

#MainMenu {
    visibility: hidden !important;
}

footer {
    visibility: hidden !important;
}

[data-testid="collapsedControl"] {
    display: none !important;
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background-color: #DCEFE8 !important;
    border-left: 2px solid #B9DDD2 !important;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.2rem !important;
}

.sidebar-title {
    font-size: 20px;
    font-weight: 700;
    color: #134e4a;
    text-align: center;
    margin-top: 8px;
    margin-bottom: 4px;
}

.sidebar-subtitle {
    font-size: 12px;
    color: #4b5563;
    text-align: center;
    margin-bottom: 20px;
}

/* ===== Hero ===== */
.hero-box {
    background: #0f766e;
    border-radius: 18px;
    padding: 22px 28px;
    margin-bottom: 24px;
    box-shadow: 0 8px 18px rgba(15, 118, 110, 0.18);
}

.main-title {
    font-size: 30px;
    font-weight: 800;
    color: white;
    text-align: right;
    margin-bottom: 8px;
    line-height: 1.2;
}

.main-subtitle {
    font-size: 15px;
    color: #dff7f3;
    text-align: right;
    line-height: 1.5;
}

/* ===== General text alignment ===== */
h1, h2, h3, h4, h5, h6, p, label, div, span {
    text-align: right;
}

[data-testid="column"] {
    text-align: right;
}

/* ===== Section titles ===== */
.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #134e4a;
    margin-bottom: 14px;
    margin-top: 8px;
    text-align: right;
}

/* ===== Cards ===== */
.info-card {
    background-color: #f7fbfa;
    border: 1px solid #cbd5e1;
    border-radius: 14px;
    padding: 18px;
}

.success-card {
    background-color: #ecfdf5;
    color: #065f46;
    border: 1px solid #a7f3d0;
    border-radius: 12px;
    padding: 12px 14px;
    font-weight: 600;
    margin-bottom: 10px;
}

/* ===== File uploader ===== */
div[data-testid="stFileUploader"] section {
    background: #ffffff;
    border-radius: 14px;
    border: 2px dashed #0f766e;
    padding: 10px;
    direction: rtl !important;
}

/* ===== Select boxes ===== */
div[data-baseweb="select"] {
    direction: rtl !important;
}

div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 2px solid #0f766e !important;
    border-radius: 12px !important;
    min-height: 46px !important;
    box-shadow: none !important;
}

div[data-baseweb="select"] * {
    text-align: right !important;
    direction: rtl !important;
}

/* ===== Radio ===== */
div[role="radiogroup"] {
    direction: rtl;
    text-align: right;
}

/* ===== Buttons ===== */
.stButton > button {
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
    color: white;
}

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

/* ===== Footer ===== */
.footer-note {
    text-align: center !important;
    color: #64748b;
    font-size: 12px;
    margin-top: 28px;
}
</style>
""",
    unsafe_allow_html=True,
)


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
        st.image(logo_path, width=170)

    st.markdown('<div class="sidebar-title">منصة أتمتة الإجراءات</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-subtitle">First Iraqi Bank - Internal Tool</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "التنقل",
        ["إنشاء الإجراء", "معلومات النظام"],
    )

if page == "إنشاء الإجراء":
    st.markdown(
        """
    <div class="hero-box">
        <div class="main-title">منصة أتمتة الإجراءات</div>
        <div class="main-subtitle">تحويل الإجراءات المكتوبة إلى نموذج SOP رسمي بنفس الصيغة المعتمدة في البنك.</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_right, col_left = st.columns([1.2, 0.8], gap="large")

    with col_right:
        st.markdown('<div class="section-title">رفع بيانات الإجراء</div>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader("رفع الإجراء", type=["txt", "docx"])

        department = st.selectbox(
            "القسم",
            ["المالية", "العمليات", "الامتثال", "إدارة المخاطر", "التدقيق الداخلي", "أخرى"],
        )

        language = st.selectbox("اللغة", ["العربية"])

        mode = st.radio(
            "وضع العمل",
            ["استخراج مباشر من النص", "إعادة صياغة احترافية"],
            horizontal=False,
        )

        if mode == "استخراج مباشر من النص":
            st.info("سيتم الاعتماد على نص المستند المرفوع قدر الإمكان، مع أقل قدر ممكن من الاختصار أو إعادة الصياغة.")
            mode_value = "extract"
        else:
            st.info("سيتم تحسين الصياغة وتنظيم المحتوى بشكل مهني مع الحفاظ على المعنى الأساسي.")
            mode_value = "rewrite"

        generate_btn = st.button("إنشاء الإجراء")

    with col_left:
        st.markdown('<div class="section-title">الحالة والتعليمات</div>', unsafe_allow_html=True)

        if uploaded_file:
            st.markdown('<div class="success-card">تم رفع الملف بنجاح.</div>', unsafe_allow_html=True)
            st.write(f"**اسم الملف:** {uploaded_file.name}")
        else:
            st.markdown(
                '<div class="info-card">يرجى رفع ملف Word أو TXT للبدء.</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            """
        <div class="info-card" style="margin-top:14px;">
        <b>ملاحظات مهمة:</b><br><br>
        • يدعم النظام ملفات Word و TXT<br>
        • يتم إنشاء الإجراء باللغة العربية الرسمية<br>
        • يتم إخراج النتيجة بنفس نموذج الـ SOP المعتمد<br>
        • يفضل أن يكون النص المرفوع واضحاً ومكتوباً بشكل منظم
        </div>
        """,
            unsafe_allow_html=True,
        )

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
    st.markdown(
        """
    <div class="hero-box">
        <div class="main-title">معلومات النظام</div>
        <div class="main-subtitle">نظرة عامة على وظيفة المنصة وآلية الاستخدام.</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown('<div class="section-title">ماذا تقوم به المنصة؟</div>', unsafe_allow_html=True)
        st.write("تقوم المنصة بتحويل الإجراءات المكتوبة إلى نموذج SOP رسمي باللغة العربية وبنفس الصيغة المعتمدة داخل البنك.")
        st.write("كما تقوم بتنسيق المحتوى داخل القالب المحدد، بما يشمل المقدمة، الأنظمة المشاركة، الهدف، منطق المطابقة، وخطوات الإجراء.")

    with c2:
        st.markdown('<div class="section-title">كيفية الاستخدام</div>', unsafe_allow_html=True)
        st.write("1. قم برفع ملف الإجراء.")
        st.write("2. اختر القسم.")
        st.write("3. اختر وضع العمل المناسب.")
        st.write("4. اضغط على زر إنشاء الإجراء.")
        st.write("5. قم بتحميل ملف الـ SOP الجاهز.")

st.markdown('<div class="footer-note">Internal Use Only - SOP Automation Platform</div>', unsafe_allow_html=True)
