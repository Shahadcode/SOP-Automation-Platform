import streamlit as st
import os
from sop_engine import generate_sop_data
from doc_generator import create_sop_doc_from_template

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="منصة أتمتة الإجراءات",
    layout="wide"
)

# =============================
# GLOBAL CSS (RTL FIX + DESIGN)
# =============================
st.markdown("""
<style>

/* ===== RTL FIX ===== */
html, body, .stApp {
    direction: rtl;
    text-align: right;
}

/* ===== MAIN CONTAINER ===== */
.block-container {
    padding-top: 2rem;
}

/* ===== HEADER ===== */
.header {
    background: #1f7a6f;
    padding: 25px 30px;
    border-radius: 20px;
    color: white;
    position: relative;
}

.header h1 {
    margin: 0;
    font-size: 28px;
}

.header p {
    margin-top: 5px;
    font-size: 14px;
    opacity: 0.9;
}

/* ===== LOGO ===== */
.header img {
    position: absolute;
    left: 20px;
    top: 20px;
    height: 50px;
}

/* ===== CARDS ===== */
.card {
    background: #ffffff;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #e6e6e6;
}

/* ===== INPUT ALIGNMENT ===== */
.stSelectbox, .stRadio, .stFileUploader {
    direction: rtl !important;
    text-align: right !important;
}

/* ===== RADIO FIX (IMPORTANT) ===== */
div[data-testid="stRadio"] {
    direction: rtl !important;
}

div[data-testid="stRadio"] label {
    display: flex !important;
    flex-direction: row-reverse !important;
    justify-content: flex-start !important;
    align-items: center !important;
    gap: 10px;
    text-align: right !important;
    width: 100%;
}

/* ===== BUTTON ===== */
.stButton button {
    background: #1f7a6f;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# =============================
# HEADER
# =============================
st.markdown(f"""
<div class="header">
    <h1>منصة أتمتة الإجراءات</h1>
    <p>تحويل الإجراءات المكتوبة إلى نموذج SOP رسمي بنفس الصيغة المعتمدة في البنك</p>
    <img src="assets/logo.png">
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =============================
# LAYOUT
# =============================
col1, col2 = st.columns([2, 1])

# =============================
# RIGHT SIDE (UPLOAD & FORM)
# =============================
with col1:
    st.markdown("### رفع بيانات الإجراء")

    uploaded_file = st.file_uploader("رفع الإجراء", type=["txt", "docx"])

    department = st.selectbox("القسم", ["المالية", "العمليات", "تقنية المعلومات"])

    language = st.selectbox("اللغة", ["العربية"])

    st.markdown("### وضع العمل")

    mode = st.radio(
        "",
        ["استخراج مباشر من النص", "إعادة صياغة احترافية"],
        label_visibility="collapsed"
    )

    st.info("سيتم الاعتماد على نص المستند المرفوع كما هو قدر الإمكان، مع أقل قدر ممكن من الاختصار أو إعادة الصياغة.")

    if st.button("إنشاء الإجراء"):

        if uploaded_file is not None:
            try:
                text = uploaded_file.read().decode("utf-8", errors="ignore")

                sop_data = generate_sop_data(text, department)

                output_file = create_sop_doc_from_template(sop_data)

                with open(output_file, "rb") as file:
                    st.download_button(
                        "تحميل الملف",
                        file,
                        file_name=os.path.basename(output_file)
                    )

                st.success("تم إنشاء الملف بنجاح")

            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")

        else:
            st.warning("يرجى رفع ملف أولاً")

# =============================
# LEFT SIDE (INFO)
# =============================
with col2:
    st.markdown("### الحالة والتعليمات")

    st.info("يرجى رفع ملف Word أو TXT للبدء.")

    st.markdown("""
    ### ملاحظات مهمة:
    - يدعم النظام ملفات TXT و Word
    - يتم إنشاء الإجراء باللغة العربية الرسمية
    - يتم إخراج النتيجة بنفس نموذج SOP المعتمد
    - يفضل أن يكون النص واضحاً ومكتوباً بشكل منظم
    """)

# =============================
# FOOTER
# =============================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("Internal Use Only - SOP Automation Platform")
