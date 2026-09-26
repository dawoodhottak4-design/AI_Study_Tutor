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
st.write("PDF upload karein ya direct text likhein, Gemini AI aapko study material tayar kar ke dega.")

# 1. API Key Validation
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Gemini API Key nahi mili! App Settings -> Secrets mein GEMINI_API_KEY set karein.")
    st.stop()

# 2. Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# Function: PDF Text Extraction
def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    extracted_text = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"
    return extracted_text

# 3. User Input Selection (Text vs PDF)
input_type = st.radio("Input Mode Select Karein:", ["Text Entry", "PDF Document Upload"], horizontal=True)

context_text = ""

if input_type == "PDF Document Upload":
    uploaded_file = st.file_uploader("Apni PDF File Upload Karein", type=["pdf"])
    if uploaded_file is not None:
        with st.spinner("PDF reading chal rahi hai..."):
            try:
                context_text = extract_text_from_pdf(uploaded_file)
                st.success(f"PDF successfully load ho gayi! ({len(context_text)} characters read)")
            except Exception as e:
                st.error(f"PDF parhne mein masla hua: {e}")
else:
    context_text = st.text_area("Apna question ya text yahan paste karein:", height=150)

# 4. Action Options & Custom Prompt
st.markdown("---")
option = st.selectbox(
    "AI Tutor Se Kya Karwana Chahte Hain?",
    [
        "Summary & Main Points",
        "Key Concepts Explanation",
        "Generate Quiz (MCQs with Answers)",
        "Important Questions for Exam",
        "Custom Instruction"
    ]
)

custom_query = ""
if option == "Custom Instruction":
    custom_query = st.text_input("Apna specific question likhein (e.g., Explain page 2 in simple terms):")

# 5. Process & Generate
if st.button("Generate Response", type="primary"):
    if not context_text.strip():
        st.warning("Barah-e-karam pehle text likhein ya PDF upload karein!")
    else:
        # Prompt Formatting
        if option == "Custom Instruction":
            instruction = custom_query if custom_query.strip() else "Analyze this text."
        else:
            instruction = f"Provide: {option}"

        full_prompt = f"""
Role: You are an expert academic tutor and study assistant.
Task: {instruction}

Study Material / Context:
{context_text}
"""

        with st.spinner("Gemini AI document process kar raha hai..."):
            try:
                response = model.generate_content(full_prompt)
                
                st.markdown("### 📌 AI Tutor Output")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"API Error: {e}")
