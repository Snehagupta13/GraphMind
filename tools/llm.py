# llm_config.py

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tools.gemma_tool import gemma_chat
from tools.tavily_tool import tavily_search
from tools.arxiv_tool import search_arxiv
from tools.mcp_tools import run_agent_sync


# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Tool registry with all properly registered tools
TOOLS = [gemma_chat, tavily_search, search_arxiv, run_agent_sync]
tools_by_name = {tool.name: tool for tool in TOOLS}

# Bind tools to LLM
model = ChatGroq(
    temperature=0.3,
    api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192"
)
model = model.bind_tools(TOOLS)  
