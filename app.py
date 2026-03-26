import streamlit as st
from graph import build_graph

# Build graph once
graph = build_graph()

st.set_page_config(page_title="GraphMind AI", layout="wide")

st.title("🧠 GraphMind AI Assistant")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input box
user_input = st.chat_input("Ask anything...")

if user_input:
    st.session_state.messages.append(("user", user_input))

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Run graph
    inputs = {"messages": [("user", user_input)]}

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        tool_placeholder = st.empty()

        final_response = ""

        for step in graph.stream(inputs, stream_mode="values"):
            message = step["messages"][-1]

            # ✅ Detect Tool Usage
            if hasattr(message, "tool_calls") and message.tool_calls:
                tool_name = message.tool_calls[0]["name"]
                tool_placeholder.info(f"🔧 Using Tool: {tool_name}")

            # ✅ Tool response
            elif message.type == "tool":
                tool_placeholder.success(f"✅ Tool finished: {message.name}")

            # ✅ Final AI response
            elif message.type == "ai":
                final_response = message.content
                response_placeholder.markdown(final_response)

    st.session_state.messages.append(("assistant", final_response))


# Show history nicely
st.divider()
st.subheader("💬 Chat History")

for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.write(msg)
