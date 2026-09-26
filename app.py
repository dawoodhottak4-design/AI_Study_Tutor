import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# Page Configuration
st.set_page_config(
    page_title="AI Study Tutor",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Study Tutor")
st.write("PDF upload karein, custom questions poochhein ya preset study options select karein!")

# 1. API Key Setup
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Gemini API Key nahi mili! App Settings -> Secrets mein GEMINI_API_KEY set karein.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

# Function: Full PDF Text Extraction
def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    extracted_text = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"
    return extracted_text

# 2. File Upload Section
uploaded_file = st.file_uploader("📂 Apni PDF File Upload Karein:", type=["pdf"])

pdf_text = ""
if uploaded_file is not None:
    with st.spinner("Pori PDF file parhi ja rahi hai..."):
        try:
            pdf_text = extract_text_from_pdf(uploaded_file)
            st.success(f"✅ PDF successfully load ho gayi! (Total {len(pdf_text)} characters processed)")
        except Exception as e:
            st.error(f"❌ PDF parhne mein masla hua: {e}")

st.markdown("---")

# 3. Select Task / Option
task_mode = st.selectbox(
    "🎯 Application Option Select Karein:",
    [
        "Specific Question Answer Extract Karna (Custom Question)",
        "Summary & Executive Notes",
        "Generate Multiple Choice Questions (MCQs Quiz with Answers)",
        "Key Terms & Definitions Extraction",
        "Important Exam Questions & Flashcards"
    ]
)

# 4. Dynamic Options Based on Choice
user_question = ""
answer_style = ""

if task_mode == "Specific Question Answer Extract Karna (Custom Question)":
    user_question = st.text_area(
        "❓ Apna Question yahan type / paste karein:",
        placeholder="E.g., What was the administrative division of India under British rule? Explain in detail.",
        height=120
    )
    answer_style = st.radio(
        "⚙️ Answer Extraction Mode Select Karein:",
        [
            "Strictly PDF Only (Jawab sirf PDF ke andar se ho)",
            "Detailed Explanation (PDF context + Clear Academic explanation)",
            "Short & Concise Bullet Points"
        ],
        horizontal=True
    )

# 5. Generate Button & Logic
if st.button("Generate Answer / Response 🚀", type="primary"):
    if not pdf_text.strip():
        st.warning("⚠️ Pehle PDF file upload karein!")
    elif task_mode == "Specific Question Answer Extract Karna (Custom Question)" and not user_question.strip():
        st.warning("⚠️ Pehle apna question enter karein!")
    else:
        # Prompt Crafting
        if task_mode == "Specific Question Answer Extract Karna (Custom Question)":
            if "Strictly PDF Only" in answer_style:
                system_instruction = (
                    "Answer the question strictly using ONLY the provided PDF text. "
                    "If the answer is not mentioned in the text, explicitly state: "
                    "'Is question ka jawab aap ki uploaded PDF notes mein maujood nahi hai.'"
                )
            elif "Short & Concise" in answer_style:
                system_instruction = "Extract the key answer from the PDF text and present it in clear, short bullet points."
            else:
                system_instruction = "Provide a detailed, well-structured academic explanation based on the PDF content."

            full_prompt = f"""
Role: Professional Academic Tutor.
Task: {system_instruction}

---
PDF CONTENT / STUDY MATERIAL:
{pdf_text}

---
USER QUESTION:
{user_question}
"""
        else:
            # Preset Options Logic
            full_prompt = f"""
Role: Professional Academic Tutor.
Task: Perform the following action on the provided PDF text: '{task_mode}'.

---
PDF CONTENT / STUDY MATERIAL:
{pdf_text}
"""

        with st.spinner("AI pori PDF ko analyze kar ke jawab tayar kar raha hai..."):
            try:
                response = model.generate_content(full_prompt)
                st.markdown("### 📌 Output Result")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"API Error: {e}")
