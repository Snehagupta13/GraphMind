from langchain.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import os

# Load variables from .env into the environment
load_dotenv()

# Now the TAVILY_API_KEY will be picked up from the environment
client = TavilyClient()

@tool
def tavily_search(query: str) -> str:
    """Uses Tavily API to perform a web search and return a summary of top results."""
    results = client.search(query=query, search_depth="advanced", max_results=5)
    response = ""
    for i, result in enumerate(results["results"]):
        response += f"{i+1}. {result['title']} ({result['url']})\nSnippet: {result['content']}\n\n"
    return response.strip()
