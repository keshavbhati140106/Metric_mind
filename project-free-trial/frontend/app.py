import streamlit as st
from streamlit_echarts import st_echarts
import sys
import os
import json
import re


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agentic-core')))

from agents.bi_agent import get_bi_agent

st.set_page_config(page_title="MetricMind BI", page_icon="📈", layout="wide")

st.title("MetricMind: Agentic Semantic BI Engine")
st.markdown("Ask natural language questions about your business metrics. The AI will translate them into governed semantic layer queries.")


with st.sidebar:
    st.markdown("### Settings")
    st.markdown("This is a free trial version. To prevent resource exhaustion, please provide your own API key. Your key is not saved anywhere.")
    user_api_key = st.text_input("Google Gemini API Key", type="password")
    st.markdown("[Get a free API key here](https://aistudio.google.com/app/apikey)")

if not user_api_key:
    st.warning("Please enter your Gemini API Key in the sidebar to start.")
    st.stop()

if "agent" not in st.session_state or st.session_state.get("current_api_key") != user_api_key:
    st.session_state.agent = get_bi_agent(api_key=user_api_key)
    st.session_state.current_api_key = user_api_key


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
                    ("system", '''You are MetricMind, an advanced BI assistant. Use the provided tools to query the Semantic Layer for data. Never write raw SQL. Only use the tools.
If the user asks for data that is best represented as a chart (like a time series or categorical breakdown), you MUST include an ECharts JSON configuration block in your response.
Wrap the JSON exactly in a markdown block like this:
```json
{
  "echarts_options": {
    "title": {"text": "Chart Title"},
    "tooltip": {},
    "xAxis": {"type": "category", "data": ["A", "B"]},
    "yAxis": {"type": "value"},
    "series": [{"data": [10, 20], "type": "bar"}]
  }
}
```
''')
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
                    
                echarts_options = None
                json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
                if json_match:
                    try:
                        parsed = json.loads(json_match.group(1))
                        if "echarts_options" in parsed:
                            echarts_options = parsed["echarts_options"]
                            response = response.replace(json_match.group(0), "").strip()
                    except Exception:
                        pass

                st.markdown(response)
                
                if echarts_options:
                    st_echarts(options=echarts_options, height="400px")
                    st.session_state.messages.append({"role": "assistant", "content": response, "echarts_options": echarts_options})
                else:
                    st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Error: {e}")
