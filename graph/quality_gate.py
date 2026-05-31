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



def quality_gate_node(state: ResearchState) -> ResearchState:
    print("\n[Quality Gate] Scoring the report...")

    report = state.get("final_report", "")

    if not report or len(report) < 100:
        print("[Quality Gate] Report too short. Score = 3.0")
        return {**state, "quality_score": 3.0}

    # llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.4)

    prompt = f"""You are reviewing a research report written by an AI system.

Score it from 0 to 10 using these generous criteria:

- 8-10 : Has clear sections, multiple facts, real examples, good length
- 6-7  : Has most sections, some facts, decent length
- 4-5  : Has some structure, covers the topic reasonably
- 2-3  : Very short or mostly vague
- 0-1  : Empty or completely off-topic

Be generous. If the report covers the topic with reasonable detail, score it 7 or above.
Reply with ONLY a single number like: 7 or 8.5
No explanation. No text. Just the number.

REPORT (first 2000 chars):
{report[:2000]}"""

    try:
        response = llm.invoke(prompt)
        raw = response.content.strip()
        match = re.search(r'\d+(\.\d+)?', raw)
        score = float(match.group()) if match else 6.0
        score = min(10.0, max(0.0, score))
    except Exception:
        score = 6.0  # default pass score if LLM fails

    log = state.get("status_log", [])
    log.append(f"Quality Gate — score: {score}/10")

    print(f"[Quality Gate] Score = {score}/10")

    return {**state, "quality_score": score, "status_log": log}


def should_retry(state: ResearchState) -> str:
    """
    Pass threshold is 5.0 — realistic for free-tier models.
    Max 2 retries to avoid burning API quota.
    """
    score = state.get("quality_score", 0)
    retry_count = state.get("retry_count", 0)

    if score < 5.0 and retry_count < 2:
        print(f"[Quality Gate] Score {score} < 5. Retrying ({retry_count}/2 used)...")
        return "retry"
    else:
        print(f"[Quality Gate] Accepted. Score = {score}")
        return "done"
