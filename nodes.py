# llm_nodes.py

import json
from langchain_core.messages import ToolMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from state import AgentState
from tools.llm import model, tools_by_name


# llm_nodes.py
from langchain_core.messages import BaseMessage


# Call the LLM
def call_model(state: AgentState, config: RunnableConfig):
    system_prompt = SystemMessage(
        "You are a helpful AI assistant. Please respond clearly and concisely."
    )
    response = model.invoke([system_prompt] + state["messages"], config)
    return {"messages": [response]}

# Run the tool that was called
def tool_node(state: AgentState):
    outputs = []
    for tool_call in state["messages"][-1].tool_calls:
        result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
        
        # Ensure result is serializable
        if isinstance(result, BaseMessage):  # like AIMessage, etc.
            result = result.content  # or use str(result) if needed

        outputs.append(
            ToolMessage(
                content=json.dumps(result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}


# Conditional edge
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    return "continue" if last_message.tool_calls else "end"
