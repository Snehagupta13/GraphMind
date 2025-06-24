import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from typing import Union
from langchain.tools import tool

# 1. Load environment variables before anything else
load_dotenv()

# 2. Retrieve environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NOTION_MCP_TOKEN = os.getenv("NOTION_MCP_TOKEN")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# 3. Validate required keys
if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY in .env")
if not NOTION_MCP_TOKEN:
    raise ValueError("Missing NOTION_MCP_TOKEN in .env")
if not TAVILY_API_KEY:
    raise ValueError("Missing TAVILY_API_KEY in .env")

# 4. Main function to run Scout agent
async def run_scout_agent(user_input: str) -> Union[str, dict]:
    # Initialize MCP client
    client = MultiServerMCPClient({
        "tavily-mcp": {
            "command": "npx",
            "args": ["-y", "tavily-mcp@0.2.4"],
            "transport": "stdio",
            "env": {
                "TAVILY_API_KEY": TAVILY_API_KEY
            }
        }
    })
    # Load tools from MCP
    tools = await client.get_tools()

    # Create and bind LLM
    llm = ChatGroq(
        temperature=0.3,
        api_key=GROQ_API_KEY,
        model_name="deepseek-r1-distill-llama-70b"
    ).bind_tools(tools)

    # Create ReAct-style agent
    agent_executor = create_react_agent(llm, tools)

    # Run the agent with user input
    result = await agent_executor.ainvoke({
        "messages": [
            SystemMessage(content="You are Scout. Use the tools to answer the user's question."),
            {"role": "user", "content": user_input}
        ]
    }, config={"recursion_limit": 50})

    return result

# 5. Synchronous wrapper for external usage
@tool
def run_agent_sync(user_input: str) -> Union[str, dict]:
    """Runs the Scout agent synchronously with the given user input."""
    import asyncio
    return asyncio.run(run_scout_agent(user_input))

