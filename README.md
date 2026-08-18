# MetricMind: Agentic Semantic BI Engine

It is AI of modern times, it proves it via combining many tech at once and doing truly what a AI should do. It is a logically verified model interaction based system which is best at it's place when it comes to semantic layer integrations and natural language interaction.

## Architecture Overview
Giving an LLM raw access to a data warehouse often results in hallucinated joins and rogue SQL. MetricMind solves this by utilizing a modern Agentic Semantic BI approach:
- **Semantic Layer (Cube.dev / dbt):** Centralizes mathematical definitions of business metrics as code.
- **Agentic Orchestrator (LangChain / Llama 3):** Translates natural language into governed semantic API calls.
- **Data Lakehouse (Snowflake):** The underlying storage and compute engine.
- **Conversational BI Interface :** I used a stremlit for thsi project

## Project Structure
- `/data-warehouse` - dbt models and mock data ingestion schemas.
- `/semantic-layer` - Cube.dev configuration and metric definitions.
- `/agentic-core` - LangChain reasoning, prompts, and tool orchestration.
- `/frontend` - used streamlit

## BYOK ( Bring Your Own Key ) 
As the deployment is based on Gemini API key so it is obvious that the project has only limited resources.  So  to  avoid  "Resource  Exhausted" error and also to make it open for everyone. I built  a  BYOK(bring  your  own  key)  version  in which you can paste your google AI studio API key and run the metric-mind engine.
refer my Project-freetrial folder in github.
