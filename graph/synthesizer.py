# synthesizer.py
# STEP 3 in the graph.
# Reads all 3 files written by workers and merges into one final report.
#
# Input files:
#   search_results.txt  → raw web data
#   analysis.txt        → structured analysis
#   examples.txt        → real world cases
#
# Output: final_report (markdown string) saved in state

# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from tools.file_system import read_all_files
from graph.state import ResearchState
from dotenv import load_dotenv

load_dotenv()


def synthesizer_node(state: ResearchState) -> ResearchState:
    """
    LangGraph node — merges all agent outputs into one research report.
    """
    print("\n[Synthesizer] Merging all research into final report...")

    vfs = state.get("virtual_files", {})
    user_query = state.get("user_query", "")
    retry_count = state.get("retry_count", 0)

    all_content = read_all_files(vfs)

    prompt = f"""You are an expert research report writer.

Research Topic: {user_query}

You have the following research materials collected by specialist agents:

{all_content}

Write a comprehensive, well-structured research report using EXACTLY these sections:

# {user_query}

## Executive Summary
(2-3 sentences giving the overall answer)

## Key Findings
(5-7 bullet points with specific data, numbers, or facts)

## Detailed Analysis
(3-4 paragraphs diving deeper into the topic)

## Real-World Examples
(Use the 3 examples from the research materials, with company names and impact)

## Challenges & Limitations
(3-4 bullet points of problems or concerns)

## Future Outlook
(1-2 paragraphs about what is expected in the coming years)

## Conclusion
(2-3 sentences summarising the key takeaway)

Write in a professional, factual tone.
Use specific data and numbers from the research materials wherever possible.
Do NOT make up facts."""

    # llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.4)
    report = llm.invoke(prompt).content

    log = state.get("status_log", [])
    log.append(f"Synthesizer — report generated (attempt {retry_count + 1})")

    print("[Synthesizer] Report generated successfully.")

    return {
        **state,
        "final_report": report,
        "retry_count": retry_count + 1,
        "status_log": log
    }
