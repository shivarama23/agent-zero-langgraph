import streamlit as st
from langchain.schema import HumanMessage, AIMessage
from langchain_core.messages.tool import ToolMessage

from utils.env import *
from supervisor.main import supervisor
from utils.messages import pretty_print_messages


st.set_page_config(page_title="LangGraph Chat")
st.title("🧠 Multi-Agent Chat")

# Initialize history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
with st.form("query_form", clear_on_submit=True):
    user_input = st.text_area("Ask me anything:", height=100)
    submitted  = st.form_submit_button("Send")

if submitted and user_input:
    # 1) Save the user's message
    st.session_state.history.append({"role": "user", "content": user_input})

    # 2) Stream new agent updates
    with st.spinner("Agents thinking..."):
        # Keep track of how many messages we've already shown
        last_shown = len(st.session_state.history)

        for update in supervisor.stream({"messages": st.session_state.history}):
            # Grab the full list of messages from supervisor
            print(update)
            all_msgs = list(update.values())[0]["messages"]

            # Only process any messages beyond what we've already added
            for msg_obj in all_msgs[last_shown:]:
                if isinstance(msg_obj, HumanMessage):
                    role = "user"
                elif isinstance(msg_obj, AIMessage):
                    role = "assistant"
                elif isinstance(msg_obj, ToolMessage):
                    role = "tool"
                else:
                    # fallback if new message types appear
                    role = "assistant"
                st.session_state.history.append({
                    "role": role,
                    "content": msg_obj.content
                })

            # Update the counter
            last_shown = len(all_msgs)

# 3) Render the chat history
for msg in st.session_state.history:
    st.chat_message(msg["role"]).markdown(msg["content"])
