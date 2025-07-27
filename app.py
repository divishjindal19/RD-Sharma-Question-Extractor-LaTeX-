import streamlit as st
from rag import extract_questions_latex
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="RD Sharma Question Extractor", layout="wide")
st.title("📘 RD Sharma Question Extractor (LaTeX)")

uploaded = st.file_uploader("Upload RD Sharma Class 12 PDF", type=["pdf"])
chapter_input = st.text_input("Enter Chapter or Sub-topic (e.g., '30.3 Conditional Probability')")

if uploaded and chapter_input:
    if st.button("Extract Questions"):
        with st.spinner("Extracting questions... Please wait..."):
            with open("uploaded.pdf", "wb") as f:
                f.write(uploaded.getbuffer())

            latex_output = extract_questions_latex("uploaded.pdf", chapter_input)

        st.subheader("✅ Extracted Questions in LaTeX")
        st.code(latex_output, language="latex")
        st.download_button("Download as .tex", latex_output, file_name="questions.tex", mime="text/plain")
