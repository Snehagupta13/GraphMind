# graph.py

from langgraph.graph import StateGraph, END
from state import AgentState
from nodes import call_model, tool_node, should_continue

def build_graph():
    # Create the graph with state type
    workflow = StateGraph(AgentState)

    # Add LLM + tool nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    # Set entrypoint
    workflow.set_entry_point("agent")

    # Conditional logic: should we use tools?
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END,
        }
    )

    # After using tools, loop back to the agent
    workflow.add_edge("tools", "agent")
    

    # Compile and return graph
    graph = workflow.compile()

    from IPython.display import Image, display

    try:
        
        display(graph.get_graph().draw_mermaid())
    except Exception:
        # This requires some extra dependencies and is optional
        pass
    return graph
graph = build_graph()


