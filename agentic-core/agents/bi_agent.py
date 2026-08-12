import os
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.cube_tools import query_cube_metric, list_available_metrics

import json

def _run_query_tool(query_json_str: str) -> str:
    try:
        query_dict = json.loads(query_json_str)
        measures = query_dict.get("measures", [])
        dimensions = query_dict.get("dimensions", [])
        time_dimensions = query_dict.get("timeDimensions", [])
        filters = query_dict.get("filters", [])
        
        result = query_cube_metric(measures, dimensions, time_dimensions, filters)
        return json.dumps(result)
    except Exception as e:
        return f"Error executing query: {str(e)}"

def _run_meta_tool(args: str) -> str:
    result = list_available_metrics()
    return json.dumps(result)

def get_bi_agent():
    llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)
    
    tools = [
        Tool(
            name="query_cube_semantic_layer",
            func=_run_query_tool,
            description="""Useful for executing queries against the Cube Semantic Layer. 
            The input must be a valid JSON string with the following keys:
            - measures: list of strings (e.g. ['transactions.total_revenue'])
            - dimensions: list of strings (e.g. ['customers.tier'])
            - timeDimensions: list of dicts (e.g. [{"dimension": "transactions.transaction_date", "dateRange": "Last 30 days", "granularity": "day"}])
            - filters: list of dicts
            Always use this tool to get data; DO NOT write raw SQL.
            """
        ),
        Tool(
            name="list_available_metrics",
            func=_run_meta_tool,
            description="Useful for finding out what measures and dimensions are available in the Semantic Layer before querying."
        )
    ]
    agent = create_react_agent(llm, tools)
    return agent
