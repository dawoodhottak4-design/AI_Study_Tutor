import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(
    page_title="AI Study Tutor",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Study Tutor")
st.write("Apna topic ya question dein, Gemini AI aapko detail mein samjhaye ga.")

# 1. Check & Fetch API Key from Streamlit Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Gemini API Key nahi mili! App Settings -> Secrets mein GEMINI_API_KEY set karein.")
    st.stop()

# 2. Configure Gemini API
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 3. Initialize Model (Fastest & Efficient Model for Study Assistance)
model = genai.GenerativeModel("gemini-1.5-flash")

# 4. User Inputs
option = st.selectbox(
    "Kya karna chahte hain?",
    ["Concept Explain Karein", "Short Notes Banaein", "Quiz Questions (MCQs)", "Summary"]
)

user_text = st.text_area("Apna question ya syllabus text yahan enter karein:", height=150)

# 5. Generate Button
if st.button("Generate Response", type="primary"):
    if not user_text.strip():
        st.warning("Barah-e-karam pehle koi text ya question likhein!")
    else:
        # Prompt Crafting
        prompt = f"Role: You are an expert academic tutor.\nTask: Provide response for option: {option}\nContent: {user_text}"
        
        with st.spinner("Gemini AI jawab tayar kar raha hai..."):
            try:
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.subheader("📌 AI Tutor Response")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"API Error: {e}")
