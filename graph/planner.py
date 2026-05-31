# planner.py
# STEP 1 in the graph.
# Receives the user query, sends it to Gemini, gets back 3 TODO tasks.
#
# Example:
#   Input:  "Research impact of AI on healthcare"
#   Output: 3 todos assigned to search_agent, analysis_agent, examples_agent

# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from graph.state import ResearchState
from dotenv import load_dotenv

load_dotenv()


def parse_todos(llm_response: str) -> list:
    """
    Converts LLM text into a list of todo dicts.
    Expects lines like:  TASK 1 | search_agent | Search for AI healthcare news
    """
    todos = []
    lines = llm_response.strip().split("\n")

    for line in lines:
        line = line.strip()
        if not line or "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3:
            todos.append({
                "id": len(todos) + 1,
                "task": parts[2],
                "status": "pending",
                "assigned_to": parts[1]
            })

    return todos


def planner_node(state: ResearchState) -> ResearchState:
    """
    LangGraph node — breaks the user query into 3 TODO tasks.
    Saves todos into the shared state.
    """
    print("\n[Planner] Breaking query into tasks...")

    user_query = state["user_query"]

    # llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.4)

    prompt = f"""You are a research planning agent.

A user wants to research: "{user_query}"

Create exactly 3 research sub-tasks for this query.
Assign each task to one of these agents:
- search_agent     : finds raw information from the web
- analysis_agent   : analyses and summarises findings
- examples_agent   : finds real world examples and case studies

Respond in this EXACT format (nothing else):
TASK 1 | search_agent | <specific search task>
TASK 2 | analysis_agent | <specific analysis task>
TASK 3 | examples_agent | <specific examples task>

Use the actual topic in each task. Be specific."""

    response = llm.invoke(prompt)
    todos = parse_todos(response.content)

    # Fallback if parsing fails
    if not todos:
        todos = [
            {"id": 1, "task": f"Search web for {user_query}", "status": "pending", "assigned_to": "search_agent"},
            {"id": 2, "task": f"Analyse findings about {user_query}", "status": "pending", "assigned_to": "analysis_agent"},
            {"id": 3, "task": f"Find real examples of {user_query}", "status": "pending", "assigned_to": "examples_agent"},
        ]

    log = state.get("status_log", [])
    log.append(f"Planner created {len(todos)} tasks")

    print(f"[Planner] Created {len(todos)} TODOs:")
    for t in todos:
        print(f"  -> [{t['assigned_to']}] {t['task']}")

    return {
        **state,
        "todos": todos,
        "virtual_files": {},
        "retry_count": 0,
        "status_log": log
    }
