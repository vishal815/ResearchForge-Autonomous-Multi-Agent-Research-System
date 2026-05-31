# quality_gate.py
# STEP 4 in the graph.
# Scores the final report 0-10. If score < 7 and retries < 2, sends back to synthesizer.
#
# This is what makes the system self-correcting.
# should_retry() is the router function LangGraph uses to decide next step.

# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from graph.state import ResearchState
from dotenv import load_dotenv
import re

load_dotenv()


def quality_gate_node(state: ResearchState) -> ResearchState:
    """
    Scores the final report.
    Adds quality_score to state.
    """
    print("\n[Quality Gate] Scoring the report...")

    report = state.get("final_report", "")

    if not report:
        print("[Quality Gate] No report found. Score = 0")
        return {**state, "quality_score": 0.0}

    # llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.4)

    prompt = f"""You are a strict research quality reviewer.

Score the report below on a scale of 0 to 10 based on:
- Does it directly answer the research topic?
- Is it well structured with clear sections?
- Does it include specific facts, numbers, or data?
- Does it include real company or project examples?
- Is it detailed enough (not too short or vague)?

Reply with ONLY a single number between 0 and 10. Nothing else. No text.

REPORT:
{report[:3000]}"""

    response = llm.invoke(prompt)
    raw = response.content.strip()

    match = re.search(r'\d+(\.\d+)?', raw)
    score = float(match.group()) if match else 5.0
    score = min(10.0, max(0.0, score))

    log = state.get("status_log", [])
    log.append(f"Quality Gate — score: {score}/10")

    print(f"[Quality Gate] Score = {score}/10")

    return {**state, "quality_score": score, "status_log": log}


def should_retry(state: ResearchState) -> str:
    """
    Router function called by LangGraph after quality_gate_node.
    Returns "retry" → goes back to synthesizer
    Returns "done"  → ends the graph
    """
    score = state.get("quality_score", 0)
    retry_count = state.get("retry_count", 0)

    if score < 7.0 and retry_count < 2:
        print(f"[Quality Gate] Score {score} < 7. Retrying... ({retry_count}/2 retries used)")
        return "retry"
    else:
        print(f"[Quality Gate] Report accepted with score {score}.")
        return "done"
