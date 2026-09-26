import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# Page Config
st.set_page_config(
    page_title="AI Study Tutor",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Study Tutor")
st.write("Apni PDF upload karein aur uske andar se koi bhi question poochhein!")

# 1. API Key Check
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Gemini API Key nahi mili! App Settings -> Secrets mein GEMINI_API_KEY set karein.")
    st.stop()

# 2. Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# Using gemini-2.0-flash or gemini-1.5-flash
model = genai.GenerativeModel("gemini-2.0-flash")

# Function: PDF Text Extraction
def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    extracted_text = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"
    return extracted_text

# 3. PDF Upload Section
uploaded_file = st.file_uploader("📂 Apni PDF File (Notes/Book) Upload Karein:", type=["pdf"])

pdf_text = ""
if uploaded_file is not None:
    with st.spinner("PDF parhi ja rahi hai..."):
        try:
            pdf_text = extract_text_from_pdf(uploaded_file)
            st.success(f"✅ PDF successfully load ho gayi! ({len(pdf_text)} characters read)")
        except Exception as e:
            st.error(f"❌ PDF read karne mein masla hua: {e}")

st.markdown("---")

# 4. Specific Question Input Box
user_question = st.text_area(
    "❓ Apna Question yahan paste / type karein:",
    placeholder="E.g., What was the administrative division in India under the British rule? Explain...",
    height=120
)

# 5. Search / Generate Response
if st.button("Answer From PDF Notes 🎯", type="primary"):
    if not pdf_text.strip():
        st.warning("⚠️ Pehle PDF file upload karein!")
    elif not user_question.strip():
        st.warning("⚠️ Pehle apna question type karein!")
    else:
        # Strict Prompt to restrict Gemini to the provided PDF context
        strict_prompt = f"""
You are a strict academic study assistant.

INSTRUCTIONS:
1. Answer the user's question using ONLY the provided Study Material below.
2. If the answer is directly found in the Study Material, explain it clearly based on that content.
3. If the answer is NOT mentioned or cannot be inferred from the provided Study Material, state clearly: "Is question ka jawab aap ki uploaded PDF notes mein maujood nahi hai." Do not invent information outside the PDF.

---
STUDY MATERIAL / PDF CONTENT:
{pdf_text}

---
USER QUESTION:
{user_question}
"""

        with st.spinner("Gemini AI aap ke PDF notes mein se jawab dhoond raha hai..."):
            try:
                response = model.generate_content(strict_prompt)
                
                st.markdown("### 📌 Jawab (Based on PDF Notes)")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"API Error: {e}")
                
