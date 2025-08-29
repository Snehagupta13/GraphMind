import streamlit as st
from graph import build_graph

# Build your graph once
graph = build_graph()

# Initialize session state memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("RAG Chat with Streaming + Memory")

# User input
user_input = st.chat_input("Ask me something about Meril Life Science...")

if user_input:
    # Append user message to memory
    st.session_state.chat_history.append(("user", user_input))

    # Build the input payload (include memory)
    inputs = {"messages": st.session_state.chat_history}

    # Stream the response
    response_container = st.empty()
    full_response = ""

    for step in graph.stream(inputs, stream_mode="values"):
        message = step["messages"][-1]
        if isinstance(message, tuple):
            role, content = message
            if role == "assistant":
                full_response += content
                response_container.markdown(full_response)
        else:
            # LangChain/LangGraph messages often have pretty_print()
            try:
                content = message.pretty_repr() if hasattr(message, "pretty_repr") else str(message)
                full_response += content
                response_container.markdown(full_response)
            except:
                pass

    # Append assistant response to memory
    st.session_state.chat_history.append(("assistant", full_response))

# Display conversation history
st.subheader("Conversation history")
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 Assistant:** {msg}")
