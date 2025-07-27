import os
import re
from langchain_groq import ChatGroq
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from extractor import extract_text, chunk_text
from pylatexenc.latexwalker import LatexWalker

# Filter question-like lines
def filter_question_like_text(text):
    question_lines = []
    for line in text.split("\n"):
        if re.match(r"^\d+\.|^Q\d+|^\(\w+\)", line.strip()):
            question_lines.append(line)
    return "\n".join(question_lines)

# Validate LaTeX output
def validate_latex(latex_str):
    try:
        LatexWalker(latex_str)
        return True
    except:
        return False

# Build FAISS vector store and save
def build_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(chunks, embeddings)
    vectorstore.save_local("faiss_index")
    return vectorstore

# Load FAISS vector store safely
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

# Main function for optimized question extraction
def extract_questions_latex(pdf_path, chapter_query):
    # Step 1: Extract and chunk text
    text = extract_text(pdf_path)
    chunks = chunk_text(text)

    # Step 2: Build vectorstore if not already created
    if not os.path.exists("faiss_index"):
        build_vectorstore(chunks)

    # Step 3: Retrieve relevant content for chapter/topic
    retriever = load_vectorstore().as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(f"Chapter {chapter_query} questions only")
    raw_text = " ".join([doc.page_content for doc in docs])
    filtered_text = filter_question_like_text(raw_text)

    # Step 4: Initialize Groq LLaMA3 model
    llm = ChatGroq(model="llama3-70b-8192", temperature=0)

    # Step 5: Single optimized prompt (extraction + LaTeX formatting)
    prompt_template = PromptTemplate(
        input_variables=["text"],
        template="""
From the text below, extract ONLY the questions (ignore theory, solutions, definitions).
Return them in LaTeX format.

Rules:
- Wrap all questions in \\begin{{enumerate}} ... \\end{{enumerate}}.
- Use \\frac{{}}{{}} for fractions, \\sqrt{{}} for roots, etc.
- Keep sub-parts (a), (b) inside nested enumerate environments.
- Do NOT add commentary or extra text.

Text:
{text}

Output in LaTeX:
"""
    )

    latex_output = llm.predict(prompt_template.format(text=filtered_text))

    # Validate LaTeX structure
    if not validate_latex(latex_output):
        latex_output = "\\begin{enumerate}\n" + latex_output + "\n\\end{enumerate}"

    return latex_output
