import os
import streamlit as st
from docx import Document
from sop_engine import generate_sop_data
from doc_generator import create_sop_doc_from_template

st.set_page_config(
    page_title="منصة أتمتة الإجراءات",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    direction: rtl;
    text-align: right;
}

.stApp {
    background-color: #EAF5F2;
    direction: rtl;
    text-align: right;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* Sidebar */
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

/* Header */
.hero-box {
    background: #0f766e;
    border: 1px solid #0f766e;
    border-radius: 18px;
    padding: 22px 24px;
    margin-bottom: 18px;
}

.main-title {
    font-size: 30px;
    font-weight: 800;
    color: white;
    margin-bottom: 6px;
    text-align: right;
}

.main-subtitle {
    font-size: 15px;
    color: #dff7f3;
    margin-bottom: 0;
    text-align: right;
}

/* Text sections */
.plain-section-title {
    font-size: 20px;
    font-weight: 700;
    color: #134e4a;
    margin-bottom: 14px;
    margin-top: 8px;
    text-align: right;
}

.status-ok {
    background-color: #ecfdf5;
    color: #065f46;
    border: 1px solid #a7f3d0;
    padding: 12px 14px;
    border-radius: 12px;
    font-weight: 600;
    margin-bottom: 10px;
    text-align: right;
}

.status-note {
    background-color: #f8fafc;
    color: #334155;
    border: 1px solid #cbd5e1;
    padding: 12px 14px;
    border-radius: 12px;
    margin-top: 12px;
    text-align: right;
}

/* Force right alignment everywhere useful */
[data-testid="column"] {
    text-align: right !important;
}

label, p, span, div, h1, h2, h3, h4, h5, h6 {
    direction: rtl !important;
    text-align: right !important;
}

/* File uploader */
section[data-testid="stFileUploader"] {
    direction: rtl !important;
    text-align: right !important;
}

div[data-testid="stFileUploader"] section {
    background: #ffffff;
    border-radius: 14px;
    border: 2px dashed #0f766e;
    padding: 8px;
}

/* Select boxes */
div[data-baseweb="select"] {
    direction: rtl !important;
    text-align: right !important;
}

div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 2px solid #0f766e !important;
    border-radius: 12px !important;
    min-height: 46px !important;
    box-shadow: none !important;
    direction: rtl !important;
}

div[data-baseweb="select"] * {
    text-align: right !important;
    direction: rtl !important;
}

div[data-baseweb="select"] input {
    color: #0f172a !important;
    font-weight: 600 !important;
}

div[data-baseweb="select"] svg {
    color: #0f766e !important;
}

/* Buttons */
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

/* Footer */
.footer-note {
    text-align: center !important;
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

    page = st.radio(
        "التنقل",
        ["إنشاء الإجراء", "معلومات النظام"]
    )

if page == "إنشاء الإجراء":
    st.markdown("""
    <div class="hero-box">
        <div class="main-title">منصة أتمتة الإجراءات</div>
        <div class="main-subtitle">تحويل الإجراءات المكتوبة إلى نموذج SOP رسمي بنفس الصيغة المعتمدة في البنك.</div>
    </div>
    """, unsafe_allow_html=True)

    right, left = st.columns([1.1, 0.9], gap="large")

    with right:
        st.markdown('<div class="plain-section-title">رفع بيانات الإجراء</div>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader("رفع الإجراء", type=["txt", "docx"])

        department = st.selectbox(
            "القسم",
            ["المالية", "العمليات", "الامتثال", "إدارة المخاطر", "التدقيق الداخلي", "أخرى"]
        )

        language = st.selectbox(
            "اللغة",
            ["العربية"]
        )

        generate_btn = st.button("إنشاء الإجراء")

    with left:
        st.markdown('<div class="plain-section-title">الحالة والتعليمات</div>', unsafe_allow_html=True)

        if uploaded_file:
            st.markdown('<div class="status-ok">تم رفع الملف بنجاح.</div>', unsafe_allow_html=True)
            st.write(f"**اسم الملف:** {uploaded_file.name}")
        else:
            st.markdown('<div class="status-note">يرجى رفع ملف Word أو TXT للبدء.</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="status-note">
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
                    sop_data = generate_sop_data(text, department, language)
                    file_path = create_sop_doc_from_template(sop_data)

                    st.success("تم إنشاء ملف الإجراء بنجاح.")

                    with open(file_path, "rb") as f:
                        st.download_button(
                            "تحميل ملف الإجراء",
                            f,
                            file_name="Generated_SOP_Arabic.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                except Exception as e:
                    st.error(f"حدث خطأ أثناء إنشاء الملف: {str(e)}")
        else:
            st.error("تعذر قراءة الملف المرفوع.")

elif page == "معلومات النظام":
    st.markdown("""
    <div class="hero-box">
        <div class="main-title">معلومات النظام</div>
        <div class="main-subtitle">نظرة عامة على وظيفة المنصة وآلية الاستخدام.</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown('<div class="plain-section-title">ماذا تقوم به المنصة؟</div>', unsafe_allow_html=True)
        st.write("تقوم المنصة بتحويل الإجراءات المكتوبة إلى نموذج SOP رسمي باللغة العربية وبنفس الصيغة المعتمدة داخل البنك.")
        st.write("كما تقوم بتنسيق المحتوى داخل القالب المحدد، بما يشمل المقدمة، الأنظمة المشاركة، الهدف، منطق المطابقة، وخطوات الإجراء.")

    with c2:
        st.markdown('<div class="plain-section-title">كيفية الاستخدام</div>', unsafe_allow_html=True)
        st.write("1. قم برفع ملف الإجراء.")
        st.write("2. اختر القسم.")
        st.write("3. اضغط على زر إنشاء الإجراء.")
        st.write("4. قم بتحميل ملف الـ SOP الجاهز.")

st.markdown('<div class="footer-note">Internal Use Only - SOP Automation Platform</div>', unsafe_allow_html=True)
