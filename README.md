# 📘 RD Sharma Question Extractor (LaTeX)

## ✅ Overview  
This project implements a **Retrieval-Augmented Generation (RAG) pipeline** using **LLMs (Groq LLaMA3)** to automatically extract **questions only** from **RD Sharma Class 12 Mathematics book** and return them in **LaTeX format**.  

The system supports:  
✔ **Chapter & Topic-based extraction**  
✔ **Preserves mathematical structure** (`\frac{}{}`, `\sqrt{}` etc.)  
✔ Outputs in **LaTeX enumerated format**  

---

## ✅ Features
- **Input:** PDF file + Chapter/Sub-topic name (e.g., `30.3 Conditional Probability`)
- **Processing:**
  - PDF parsing → text extraction
  - Chunking for efficient retrieval
  - Embedding-based semantic search using FAISS
  - LLaMA3 model for extraction and LaTeX formatting
- **Output:** Structured LaTeX-formatted questions
- **Interface:** Streamlit Web App + CLI/Notebook Demo

---

## ✅ Architecture
### **Pipeline Flow**

User Input (PDF + Chapter)

↓

PDF Parsing (pdfplumber)

↓

Text Chunking (LangChain)

↓

Embeddings (HuggingFace MiniLM)

↓

FAISS Vector Store

↓

LLM (Groq LLaMA3) → Extraction + LaTeX Formatting

↓

Streamlit UI Output (.tex Download)


---

## ✅ Tech Stack
- **Language:** Python
- **LLM:** Groq LLaMA3 (`llama3-70b-8192`)
- **RAG Framework:** LangChain
- **Embeddings:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
- **Vector Store:** FAISS
- **UI:** Streamlit
- **PDF Parser:** pdfplumber

---

## ✅ Setup Instructions

### **1. Clone Repository**
```bash
git clone <repo-url>
cd project

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt

GROQ_API_KEY=your_groq_api_key_here

streamlit run app.py

From the text below, extract ONLY the questions (ignore theory, solutions, definitions).
Return them in LaTeX format.

Rules:
- Wrap all questions in \begin{enumerate}...\end{enumerate}.
- Use \frac{}{} for fractions, \sqrt{} for roots.
- Keep sub-parts (a), (b) inside nested enumerate environments.
- Do NOT add commentary or extra text.

Text:
{text}

Output in LaTeX:



