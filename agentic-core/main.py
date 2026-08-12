from dotenv import load_dotenv
load_dotenv()

import sys
from agents.bi_agent import get_bi_agent

def main():
    print("Initializing MetricMind Agentic BI Engine...")
    agent = get_bi_agent()
    
    print("\nAgent initialized. Type 'exit' to quit.")
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            result = agent.invoke({"messages": [
                ("system", "You are MetricMind, an advanced BI assistant. Use the provided tools to query the Semantic Layer for data. Never write raw SQL. Only use the tools."),
                ("user", user_input)
            ]})
            response_content = result["messages"][-1].content
            
            if isinstance(response_content, list):
                text_parts = [block["text"] for block in response_content if isinstance(block, dict) and block.get("type") == "text" and "text" in block]
                response = "\n".join(text_parts) if text_parts else str(response_content)
            else:
                response = str(response_content)
                
            print(f"\nMetricMind: {response}")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
