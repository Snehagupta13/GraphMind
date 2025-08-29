from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Tuple, Optional
from graph import build_graph  # your LangGraph workflow

app = FastAPI(title="GraphMind Chat")

# Build the graph once at startup
graph = build_graph()

# In-memory conversation storage (per session_id)
# 👉 In production, replace with Redis/DB
memory_store = {}


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    response: str
    history: List[Tuple[str, str]]


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Standard endpoint: send user message, get assistant reply.
    """
    session_id = req.session_id
    user_msg = req.message

    # Initialize memory if new session
    if session_id not in memory_store:
        memory_store[session_id] = []

    # Append user message
    memory_store[session_id].append(("user", user_msg))

    # Run LangGraph with memory
    inputs = {"messages": memory_store[session_id]}
    response = ""
    for step in graph.stream(inputs, stream_mode="values"):
        msg = step["messages"][-1]
        if isinstance(msg, tuple):
            role, content = msg
            if role == "assistant":
                response = content

    # Append assistant reply to memory
    memory_store[session_id].append(("assistant", response))

    return ChatResponse(
        session_id=session_id,
        response=response,
        history=memory_store[session_id]
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
