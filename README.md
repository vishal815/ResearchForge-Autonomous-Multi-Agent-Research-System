# 🔬 ResearchForge

Autonomous AI Research Agent built with LangGraph, Google Gemini, and Tavily.

Enter any research topic → AI agents research, analyse, find examples → get a full structured report.

## Architecture
```
User Query → Planner → Workers (Search + Analysis + Examples) → Synthesizer → Quality Gate → Report
```

## Tech Stack
- LangGraph · LangChain · Google Gemini 1.5 Flash · Tavily · Streamlit · LangSmith

## Setup
```bash
pip install uv
uv venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
uv pip install -r requirements.txt
```

Add keys to `.env`:
```
GOOGLE_API_KEY=...
TAVILY_API_KEY=...
LANGCHAIN_API_KEY=...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=researchforge
```

## Run
```bash
# Test in terminal first
python main.py

# Full UI
streamlit run ui/app.py
```
