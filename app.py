import streamlit as st
from graph import build_graph

# ------------------- CONFIG -------------------
st.set_page_config(
    page_title="GraphMind AI",
    page_icon="🧠",
    layout="wide"
)

# ------------------- CUSTOM CSS -------------------
st.markdown("""
<style>
/* Background */
.main {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

/* Chat bubbles */
.stChatMessage {
    border-radius: 15px;
    padding: 10px;
    margin-bottom: 10px;
}

/* User bubble */
[data-testid="stChatMessage"][data-testid*="user"] {
    background-color: #1d4ed8;
    color: white;
}

/* Assistant bubble */
[data-testid="stChatMessage"][data-testid*="assistant"] {
    background-color: #334155;
    color: white;
}

/* Tool box */
.tool-box {
    background: #0ea5e9;
    padding: 10px;
    border-radius: 10px;
    color: white;
    font-weight: bold;
}

/* Title */
h1 {
    text-align: center;
    font-size: 2.5rem;
}
</style>
""", unsafe_allow_html=True)

# ------------------- SIDEBAR -------------------
with st.sidebar:
    st.title("⚙️ Settings")

    st.markdown("### 🎛 Controls")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3)

    st.markdown("### 📊 Info")
    st.info("GraphMind AI\n\nLangGraph + Tools + Groq")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ------------------- GRAPH -------------------
graph = build_graph()

# ------------------- HEADER -------------------
st.title("🧠 GraphMind AI Assistant")
st.caption("⚡ Powered by LangGraph + Tool Calling")

# ------------------- CHAT HISTORY -------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------- INPUT -------------------
user_input = st.chat_input("Ask anything...")

# ------------------- PROCESS -------------------
if user_input:
    st.session_state.messages.append(("user", user_input))

    with st.chat_message("user"):
        st.markdown(f"**🧑 You:** {user_input}")

    inputs = {"messages": [("user", user_input)]}

    with st.chat_message("assistant"):

        response_placeholder = st.empty()
        tool_placeholder = st.empty()
        progress_bar = st.progress(0)

        final_response = ""
        step_count = 0

        for step in graph.stream(inputs, stream_mode="values"):
            step_count += 1
            progress_bar.progress(min(step_count * 20, 100))

            message = step["messages"][-1]

            # 🔧 TOOL CALL DETECT
            if hasattr(message, "tool_calls") and message.tool_calls:
                tool_name = message.tool_calls[0]["name"]

                tool_placeholder.markdown(
                    f'<div class="tool-box">🔧 Using Tool: {tool_name}</div>',
                    unsafe_allow_html=True
                )

            # ✅ TOOL DONE
            elif message.type == "tool":
                tool_placeholder.success(f"✅ Tool finished: {message.name}")

            # 🤖 FINAL RESPONSE
            elif message.type == "ai":
                final_response = message.content
                response_placeholder.markdown(
                    f"**🤖 AI Response:**\n\n{final_response}"
                )

        progress_bar.empty()

    st.session_state.messages.append(("assistant", final_response))

# ------------------- HISTORY -------------------
st.divider()
st.subheader("💬 Chat History")

for role, msg in st.session_state.messages:
    with st.chat_message(role):
        if role == "user":
            st.markdown(f"**🧑 You:** {msg}")
        else:
            st.markdown(f"**🤖 AI:** {msg}")
