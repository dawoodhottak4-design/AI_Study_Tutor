import streamlit as st
from google import genai
from pypdf import PdfReader

st.set_page_config(page_title="AI Study Tutor", page_icon="📚", layout="wide")
st.title("📚 AI Study Tutor")

# API Key check
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Gemini API Key nahi mili!")
    st.stop()

# Initialize Client with New SDK
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    extracted_text = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"
    return extracted_text

input_type = st.radio("Input Mode Select Karein:", ["Text Entry", "PDF Document Upload"], horizontal=True)

context_text = ""
if input_type == "PDF Document Upload":
    uploaded_file = st.file_uploader("Apni PDF File Upload Karein", type=["pdf"])
    if uploaded_file is not None:
        with st.spinner("PDF reading..."):
            try:
                context_text = extract_text_from_pdf(uploaded_file)
                st.success(f"PDF successfully load ho gayi! ({len(context_text)} characters read)")
            except Exception as e:
                st.error(f"PDF error: {e}")
else:
    context_text = st.text_area("Apna question/text yahan paste karein:", height=150)

option = st.selectbox(
    "AI Tutor Se Kya Karwana Chahte Hain?",
    ["Summary & Main Points", "Key Concepts Explanation", "Generate Quiz (MCQs)", "Important Questions for Exam"]
)

if st.button("Generate Response", type="primary"):
    if not context_text.strip():
        st.warning("Pehle text ya PDF upload karein!")
    else:
        full_prompt = f"Role: Academic Tutor.\nTask: {option}\n\nContext:\n{context_text}"
        
        with st.spinner("Gemini AI response generate kar raha hai..."):
            try:
                # New SDK syntax
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=full_prompt,
                )
                st.markdown("### 📌 AI Tutor Output")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"API Error: {e}")
