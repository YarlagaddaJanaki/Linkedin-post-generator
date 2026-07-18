# 🚀 AI-Powered LinkedIn Post Generator

An AI-powered Streamlit application that generates personalized LinkedIn posts using Large Language Models (LLMs). The application supports Retrieval-Augmented Generation (RAG) by analyzing uploaded resume PDFs to create context-aware and personalized LinkedIn posts.

---

## ✨ Features

- 🤖 Generate LinkedIn posts using **Groq Llama 3.3** and **Google Gemini**
- 📄 Upload your resume (PDF) for personalized post generation
- 🔍 Retrieval-Augmented Generation (RAG) using ChromaDB
- ✂️ Automatic text chunking for efficient document processing
- 🧠 Semantic search using Sentence Transformers embeddings
- 🎯 Customize:
  - Topic
  - Tone
  - Audience
  - Language
  - Post Length
- 🔗 Automatically opens LinkedIn's post creation page with the generated content
- 📋 One-click copy generated post

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Groq API (Llama 3.3)
- Google Gemini
- ChromaDB
- Sentence Transformers
- Hugging Face
- PyPDF
- Retrieval-Augmented Generation (RAG)

---

## 📂 Project Structure

```
linkedin-post-generator/
│
├── data/
├── prompts/
├── services/
│   ├── embedding_service.py
│   ├── llm_service.py
│   └── pdf_service.py
│
├── utils/
│   └── chunking.py
│
├── vectorstore/
│   └── chroma_service.py
│
├── main.py
├── post_generator.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/YarlagaddaJanaki/Linkedin-post-generator.git
```

Navigate to the project

```bash
cd Linkedin-post-generator
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
```

Run the application

```bash
streamlit run main.py
```

---

## 🚀 How It Works

1. Upload your resume (optional).
2. Resume text is extracted and split into chunks.
3. Chunks are converted into vector embeddings using Sentence Transformers.
4. Embeddings are stored in ChromaDB.
5. Relevant resume information is retrieved using semantic search.
6. LangChain combines the retrieved context with your prompt.
7. Groq Llama 3.3 or Google Gemini generates a personalized LinkedIn post.
8. Click **Open in LinkedIn** to automatically navigate to LinkedIn's post creation page.

---

## 📸 Demo
<img width="1916" height="861" alt="image" src="https://github.com/user-attachments/assets/d4902d39-7ee4-4c94-9204-3058574e1275" />
<img width="1917" height="865" alt="image" src="https://github.com/user-attachments/assets/afc6f5f5-6e92-46cd-ae79-a77e4dec626b" />







---

## 🔮 Future Enhancements

- Support multiple document uploads
- Add more LLM providers
- Save generated post history
- Export posts to PDF or DOCX
- Multiple LinkedIn post templates

---

## 👩‍💻 Author

**Janaki Yarlagadda**

- GitHub: https://github.com/YarlagaddaJanaki
- LinkedIn:https://www.linkedin.com/in/yarlagadda-janaki-5618b0303/

---

⭐ If you found this project useful, consider giving it a star!
