import streamlit as st
from streamlit_echarts import st_echarts
import sys
import os
import json


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agentic-core')))

from agents.bi_agent import get_bi_agent

st.set_page_config(page_title="MetricMind BI", page_icon="📈", layout="wide")

st.title("MetricMind: Agentic Semantic BI Engine")
st.markdown("Ask natural language questions about your business metrics. The AI will translate them into governed semantic layer queries.")


if "agent" not in st.session_state:
    st.session_state.agent = get_bi_agent()


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "echarts_options" in message:
            st_echarts(options=message["echarts_options"], height="400px")


if prompt := st.chat_input("E.g., What is our total revenue for the last 30 days?"):

    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking and querying the semantic layer..."):
            try:

                formatted_messages = [
                    ("system", "You are MetricMind, an advanced BI assistant. Use the provided tools to query the Semantic Layer for data. Never write raw SQL. Only use the tools.")
                ]
                for m in st.session_state.messages[:-1]:
                    if m["role"] == "user":
                        formatted_messages.append(("user", m["content"]))
                    elif m["role"] == "assistant":
                        formatted_messages.append(("assistant", m["content"]))
                formatted_messages.append(("user", prompt))
                
                result = st.session_state.agent.invoke({"messages": formatted_messages})
                response_content = result["messages"][-1].content
                

                if isinstance(response_content, list):
                    text_parts = [block["text"] for block in response_content if isinstance(block, dict) and block.get("type") == "text" and "text" in block]
                    response = "\n".join(text_parts) if text_parts else str(response_content)
                else:
                    response = str(response_content)
                    
                st.markdown(response)
                

                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Error: {e}")

