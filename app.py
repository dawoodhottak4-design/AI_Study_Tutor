import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="AI Study Tutor", page_icon="📚")

st.title("📚 AI Study Tutor")

# Fetch API key directly from Streamlit Cloud Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ API Key nahi mili! Streamlit Cloud Settings -> Secrets mein GEMINI_API_KEY add karein.")
    st.stop()

# Configure Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# App UI
user_query = st.text_area("Apna question ya topic yahan likhein:", height=150)

if st.button("Generate Study Notes", type="primary"):
    if user_query.strip():
        with st.spinner("AI response generate ho raha hai..."):
            try:
                response = model.generate_content(user_query)
                st.markdown("### Answer / Study Material")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Pehle koi topic ya question likhein.")
