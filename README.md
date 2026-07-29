# MetricMind: Agentic Semantic BI Engine

An advanced, enterprise-grade Data Analytics architecture designed to bridge the gap between Generative AI and strict corporate data governance.

## Architecture Overview
Giving an LLM raw access to a data warehouse often results in hallucinated joins and rogue SQL. MetricMind solves this by utilizing a modern Agentic Semantic BI approach:
- **Semantic Layer (Cube.dev / dbt):** Centralizes mathematical definitions of business metrics as code.
- **Agentic Orchestrator (LangChain / Llama 3):** Translates natural language into governed semantic API calls.
- **Data Lakehouse (Snowflake):** The underlying storage and compute engine.
- **Conversational BI Interface (Next.js & ECharts):** A custom UI rendering natural language alongside interactive data visualizations.

## Project Structure
- `/data-warehouse` - dbt models and mock data ingestion schemas.
- `/semantic-layer` - Cube.dev configuration and metric definitions.
- `/agentic-core` - LangChain reasoning, prompts, and tool orchestration.
- `/frontend` - Next.js conversational UI and dynamic charting.