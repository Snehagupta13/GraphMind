# 🧠 Chatbot — LangGraph Powered Agent Framework

This project implements a modular, multi-tool AI chatbot using **LangGraph**, a powerful framework for building dynamic, stateful AI applications.

---

## 🚀 Features

- 🤖 **Multi-agent support** with LangGraph
- 🛠️ Modular tool system:
  - `gemma_tool.py`: Integrates with Google's Gemma LLM
  - `tavily_tool.py`: Web search using Tavily
  - `mcp_tools.py`: Custom tools for DICOM or medical processing
  - `time_tool.py`: Time-related utilities
  - `arxiv_tool.py`: Arxiv paper fetching
  - `llm.py`: LLM wrapper module
- 🔄 Stateful chat flows with `graph.py` and `state.py`
- 📦 Easily extendable with new tools
- 📂 Clean project structure with `.gitignore`, `requirements.txt`, and isolated `venv`

---

## 📁 Project Structure

chatbot/
│
├── main.py # Entry point to run the chatbot
├── graph.py # Builds the LangGraph computation graph
├── nodes.py # Defines the LangGraph nodes/agents
├── state.py # Handles state logic between steps
│
├── tools/ # Custom tools the chatbot uses
│ ├── gemma_tool.py
│ ├── tavily_tool.py
│ ├── mcp_tools.py
│ ├── time_tool.py
│ ├── arxiv_tool.py
│ └── llm.py
│
├── requirements.txt # Python dependencies
├── .env # Environment variables (API keys, secrets)
├── .gitignore # Git ignore rules
└── venv/ # Virtual environment (excluded in Git)


---

## 🛠️ Setup Instructions

### Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate


# Install Dependencies
pip install -r requirements.txt

# Set Environment Variables
Create a .env file and add your API keys:
TAVILY_API_KEY=your_key_here
GEMMA_API_KEY=your_key_here

# Run the Chatbot
python main.py
🙋‍♀️ Maintainer
Sneha Gupta
AI Developer @ Meril
GitHub: @Snehagupta13
