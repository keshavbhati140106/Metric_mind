import os
import requests
from dotenv import load_dotenv

load_dotenv()

CUBE_API_URL = os.getenv("CUBE_API_URL")
CUBE_API_TOKEN = os.getenv("CUBE_API_TOKEN")

def query_cube_metric(measures: list, dimensions: list = None, time_dimensions: list = None, filters: list = None) -> dict:
    
    if not CUBE_API_URL or not CUBE_API_TOKEN:
        return {"error": "CUBE_API_URL or CUBE_API_TOKEN is missing in the environment."}
    
    headers = {
        "Authorization": CUBE_API_TOKEN,
        "Content-Type": "application/json"
    }
    
    query = {
        "measures": measures,
        "dimensions": dimensions or [],
        "timeDimensions": time_dimensions or [],
        "filters": filters or []
    }
    
    try:
        response = requests.post(f"{CUBE_API_URL}/load", headers=headers, json={"query": query})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "response": response.text if response else None}

def list_available_metrics() -> dict:

    if not CUBE_API_URL or not CUBE_API_TOKEN:
        return {"error": "CUBE_API_URL or CUBE_API_TOKEN is missing in the environment."}
    
    headers = {
        "Authorization": CUBE_API_TOKEN,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{CUBE_API_URL}/meta", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
