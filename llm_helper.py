from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-20b"
)

response = llm.invoke(
    "Two most important ingredients in samosa are?"
)

print(response.content)