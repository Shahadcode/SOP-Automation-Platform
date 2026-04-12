import os
import streamlit as st
from docx import Document
from sop_engine import generate_sop_data
from doc_generator import create_sop_doc_from_template

st.set_page_config(
    page_title="منصة أتمتة الإجراءات",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp {
        background-color: #EAF5F2;
        direction: rtl;
    }

    header[data-testid="stHeader"],
    [data-testid="collapsedControl"],
    section[data-testid="stSidebar"] {
        display: none !important;
    }

    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }

    .hero-box {
        background: #0f766e;
        border: 1px solid #0f766e;
        border-radius: 0 0 18px 18px;
        padding: 22px 24px;
        margin: 0 0 20px 0;
        width: 100%;
        box-sizing: border-box;
        box-shadow: 0 6px 16px rgba(15, 118, 110, 0.16);
    }

    .main-title {
        font-size: 30px;
        font-weight: 800;
        color: white;
        margin-bottom: 6px;
    }

    .main-subtitle {
        font-size: 15px;
        color: #dff7f3;
        margin-bottom: 0;
    }

    .plain-section-title {
        font-size: 20px;
        font-weight: 700;
        color: #134e4a;
        margin-bottom: 14px;
        margin-top: 8px;
    }

    .status-ok {
        background-color: #ecfdf5;
        color: #065f46;
        border: 1px solid #a7f3d0;
        padding: 12px 14px;
        border-radius: 12px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .status-note {
        background-color: #f8fafc;
        color: #334155;
        border: 1px solid #cbd5e1;
        padding: 12px 14px;
        border-radius: 12px;
        margin-top: 12px;
    }

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

    .footer-note {
        text-align: center;
        color: #64748b;
        font-size: 12px;
        margin-top: 28px;
    }

    div[data-testid="stFileUploader"] section {
        background: #ffffff;
        border-radius: 14px;
        border: 2px dashed #0f766e;
        padding: 8px;
    }

    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 2px solid #0f766e !important;
        border-radius: 12px !important;
        min-height: 46px !important;
        box-shadow: none !important;
    }

    div[data-baseweb="select"] input {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="select"] svg {
        color: #0f766e !important;
    }

    /* LEFT PANEL ONLY */
    div[data-testid="column"]:first-child {
        background-color: #D7ECE5;
        border-left: 3px solid #9FCFC0;
        box-shadow: -6px 0 18px rgba(0, 0, 0, 0.10);
        padding: 0px 16px 24px 16px;
        min-height: 100vh;
    }

    /* make left panel content start lower to align with header */
    .logo-align-space {
        height: 22px;
    }

    .side-title {
        text-align: center;
        font-size: 20px;
        font-weight: 700;
        color: #134e4a;
        margin-top: 8px;
        margin-bottom: 4px;
    }

    .side-subtitle {
        text-align: center;
        font-size: 12px;
        color: #4b5563;
        margin-bottom: 24px;
    }

    .side-menu-title {
        font-size: 14px;
        font-weight: 700;
        color: #134e4a;
        margin-bottom: 10px;
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


left_panel, main_panel = st.columns([1, 4], gap="medium")

with left_panel:
    st.markdown('<div class="logo-align-space"></div>', unsafe_allow_html=True)

    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=170)

    st.markdown('<div class="side-title">منصة أتمتة الإجراءات</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-subtitle">First Iraqi Bank - Internal Tool</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-menu-title">التنقل</div>', unsafe_allow_html=True)

    page = st.radio(
        "",
        ["إنشاء الإجراء", "معلومات النظام"],
        label_visibility="collapsed"
    )

with main_panel:
    if page == "إنشاء الإجراء":
        st.markdown("""
        <div class="hero-box">
            <div class="main-title">منصة أتمتة الإجراءات</div>
            <div class="main-subtitle">تحويل الإجراءات المكتوبة إلى نموذج SOP رسمي بنفس الصيغة المعتمدة في البنك.</div>
        </div>
        """, unsafe_allow_html=True)

        left, right = st.columns([1.1, 0.9], gap="large")

        with left:
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

        with right:
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