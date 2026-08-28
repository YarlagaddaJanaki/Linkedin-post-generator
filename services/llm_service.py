import os
import streamlit as st

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class LLMService:

    def __init__(self):

        try:
            groq_api_key = st.secrets["GROQ_API_KEY"]
        except:
            groq_api_key = os.getenv("GROQ_API_KEY")

        try:
            google_api_key = st.secrets["GOOGLE_API_KEY"]
        except:
            google_api_key = os.getenv("GOOGLE_API_KEY")

        self.groq = ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0.7,
            groq_api_key=groq_api_key
        )

        self.gemini = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            google_api_key=google_api_key
        )

    def get_llm(self, model_name):

        if model_name == "Gemini":
            return self.gemini

        if model_name == "Groq":
            return self.groq

        return self.gemini