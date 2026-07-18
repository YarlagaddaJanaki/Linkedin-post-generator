import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class LLMService:

    def __init__(self):

        self.groq = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

        self.gemini = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def get_llm(self, model_name):

        if model_name == "Gemini":
            return self.gemini

        return self.groq