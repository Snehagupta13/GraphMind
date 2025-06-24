# gemma_tool.py

from langchain_groq import ChatGroq
from langchain.tools import tool
from dotenv import load_dotenv
import os
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Create Groq client using Gemma
llm = ChatGroq(model_name="gemma2-9b-it", temperature=0.3)

@tool
def gemma_chat(prompt: str) -> str:
    """Use gemma2-9b-it via Groq to generate a response from a given prompt."""
    print(f"💬 Prompt to Groq Gemma: {prompt}")
    return llm.invoke(prompt)
