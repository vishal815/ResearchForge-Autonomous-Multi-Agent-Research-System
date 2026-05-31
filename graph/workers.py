# workers.py
# STEP 2 in the graph — 3 specialist agents run here.
#
# search_agent   → searches the web with Tavily, saves search_results.txt
# analysis_agent → reads search_results.txt, writes structured analysis.txt
# examples_agent → finds real company examples, saves examples.txt
#
# All 3 are called inside workers_node() one after another.

# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from tools.search_tool import search_web
from tools.file_system import write_file, read_file
from graph.state import ResearchState
from dotenv import load_dotenv

load_dotenv()

# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.4)


# ── Agent 1: Search ───────────────────────────────────────────────────────────

def run_search_agent(state: dict) -> dict:
    """
    Finds the search_agent TODO, runs web search, saves to search_results.txt
    """
    print("\n  [Search Agent] Searching the web...")

    todos = state.get("todos", [])
    my_todo = next((t for t in todos if t["assigned_to"] == "search_agent"), None)

    if not my_todo:
        print("  [Search Agent] No task found. Skipping.")
        return state

    print(f"  [Search Agent] Task: {my_todo['task']}")

    results = search_web(my_todo["task"], max_results=5)

    vfs = state.get("virtual_files", {})
    vfs = write_file(vfs, "search_results.txt", results)

    for t in todos:
        if t["assigned_to"] == "search_agent":
            t["status"] = "done"

    log = state.get("status_log", [])
    log.append("Search Agent — web search completed")

    print("  [Search Agent] Done. Saved to search_results.txt")

    return {**state, "virtual_files": vfs, "todos": todos, "status_log": log}


# ── Agent 2: Analysis ─────────────────────────────────────────────────────────

def run_analysis_agent(state: dict) -> dict:
    """
    Reads search_results.txt, sends to Gemini for analysis, saves analysis.txt
    """
    print("\n  [Analysis Agent] Analysing search results...")

    todos = state.get("todos", [])
    my_todo = next((t for t in todos if t["assigned_to"] == "analysis_agent"), None)

    if not my_todo:
        print("  [Analysis Agent] No task found. Skipping.")
        return state

    vfs = state.get("virtual_files", {})
    search_results = read_file(vfs, "search_results.txt")

    if not search_results:
        search_results = "No search results available. Use your general knowledge."

    user_query = state.get("user_query", "")

    prompt = f"""You are a research analysis expert.

Topic: {user_query}

Based on the search results below, write a structured analysis:

{search_results[:3000]}

Your analysis MUST include these 4 sections:

## Key Findings
(5 bullet points with specific facts or numbers)

## Main Themes
(What are the 2-3 big ideas?)

## Challenges and Concerns
(3 bullet points)

## Future Outlook
(1 short paragraph about what comes next)

Be specific. Use data from the search results where possible."""

    response = llm.invoke(prompt)
    analysis = response.content

    vfs = write_file(vfs, "analysis.txt", analysis)

    for t in todos:
        if t["assigned_to"] == "analysis_agent":
            t["status"] = "done"

    log = state.get("status_log", [])
    log.append("Analysis Agent — structured analysis completed")

    print("  [Analysis Agent] Done. Saved to analysis.txt")

    return {**state, "virtual_files": vfs, "todos": todos, "status_log": log}


# ── Agent 3: Examples ─────────────────────────────────────────────────────────

def run_examples_agent(state: dict) -> dict:
    """
    Searches for real world case studies and saves to examples.txt
    """
    print("\n  [Examples Agent] Finding real-world examples...")

    todos = state.get("todos", [])
    my_todo = next((t for t in todos if t["assigned_to"] == "examples_agent"), None)

    if not my_todo:
        print("  [Examples Agent] No task found. Skipping.")
        return state

    user_query = state.get("user_query", "")

    search_query = f"real world examples case studies companies {user_query}"
    raw = search_web(search_query, max_results=4)

    prompt = f"""You are a research examples specialist.

Topic: {user_query}

Based on this information:
{raw[:2500]}

Provide exactly 3 real-world examples in this EXACT format:

EXAMPLE 1: [Real Company or Project Name]
What they do: [1-2 sentences describing what they built or did]
Impact: [specific measurable result or outcome]

EXAMPLE 2: [Real Company or Project Name]
What they do: [1-2 sentences]
Impact: [specific result]

EXAMPLE 3: [Real Company or Project Name]
What they do: [1-2 sentences]
Impact: [specific result]

Only use real, verifiable examples. Include actual company names."""

    response = llm.invoke(prompt)
    examples = response.content

    vfs = state.get("virtual_files", {})
    vfs = write_file(vfs, "examples.txt", examples)

    for t in todos:
        if t["assigned_to"] == "examples_agent":
            t["status"] = "done"

    log = state.get("status_log", [])
    log.append("Examples Agent — real-world cases found")

    print("  [Examples Agent] Done. Saved to examples.txt")

    return {**state, "virtual_files": vfs, "todos": todos, "status_log": log}


# ── Combined Workers Node ─────────────────────────────────────────────────────

def workers_node(state: ResearchState) -> ResearchState:
    """
    LangGraph node that runs all 3 agents in sequence.
    Each agent reads from and writes to the shared state.
    """
    print("\n[Workers] Starting all 3 agents...")

    state = run_search_agent(state)
    state = run_analysis_agent(state)
    state = run_examples_agent(state)

    print("\n[Workers] All 3 agents completed.")
    return state
