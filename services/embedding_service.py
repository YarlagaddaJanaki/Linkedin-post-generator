import os

import streamlit as st
from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer

# Force CPU loading on Windows to avoid meta-device / GPU issues.
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model: SentenceTransformer):
        self._model = model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        vectors = self._model.encode(
            texts,
            show_progress_bar=False,
            convert_to_numpy=True,
        )
        return vectors.tolist()

    def embed_query(self, text: str) -> list[float]:
        vector = self._model.encode(
            text,
            show_progress_bar=False,
            convert_to_numpy=True,
        )
        return vector.tolist()


@st.cache_resource(show_spinner="Loading embedding model...")
def get_embedding_model() -> SentenceTransformerEmbeddings:
    model = SentenceTransformer(
        MODEL_NAME,
        device="cpu",
        model_kwargs={"low_cpu_mem_usage": False},
    )
    return SentenceTransformerEmbeddings(model)
