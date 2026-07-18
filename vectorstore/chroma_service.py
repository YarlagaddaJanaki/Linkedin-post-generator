import streamlit as st
from langchain_chroma import Chroma

from services.embedding_service import get_embedding_model


@st.cache_resource(show_spinner="Loading vector store...")
def get_chroma_service():
    return Chroma(
        collection_name="linkedin_posts",
        embedding_function=get_embedding_model(),
        persist_directory="./chroma_db",
    )


class ChromaService:

    def __init__(self, db):
        self.db = db

    def add_documents(self, chunks):
        self.db.add_texts(chunks)

    def similarity_search(self, query, k=3):
        return self.db.similarity_search(query, k=k)
