# main.py
# Run this file to test the full pipeline in terminal WITHOUT the UI.
# Good for testing before running the Streamlit app.
#
# Run with:  python main.py

import os
import sys
sys.path.insert(0, os.path.abspath("."))

from dotenv import load_dotenv
load_dotenv()

from graph.graph_builder import build_graph


def run_research(query: str):
    """Run the full ResearchForge pipeline for a given query."""

    print("\n" + "=" * 60)
    print(f"  ResearchForge")
    print(f"  Query: {query}")
    print("=" * 60)

    # Build the graph
    graph = build_graph()

    # Initial state
    initial_state = {
        "user_query":    query,
        "todos":         [],
        "virtual_files": {},
        "final_report":  None,
        "quality_score": None,
        "retry_count":   0,
        "status_log":    []
    }

    # Run the graph
    final_state = graph.invoke(initial_state)

    # Print results
    print("\n" + "=" * 60)
    print("  RESULTS")
    print("=" * 60)

    print("\n-- Agent Log --")
    for entry in final_state.get("status_log", []):
        print(f"  {entry}")

    print("\n-- Files Created --")
    for filename in final_state.get("virtual_files", {}).keys():
        print(f"  {filename}")

    score = final_state.get("quality_score", 0)
    retries = final_state.get("retry_count", 0)
    print(f"\n-- Quality Score: {score}/10  (attempts: {retries}) --")

    print("\n-- Final Report --\n")
    print(final_state.get("final_report", "No report generated."))

    # Save report to file
    report = final_state.get("final_report", "")
    if report:
        with open("output_report.md", "w", encoding="utf-8") as f:
            f.write(report)
        print("\n\nReport saved to output_report.md")

    return final_state


if __name__ == "__main__":
    # Change this query to test different topics
    query = "Research the impact of artificial intelligence on healthcare"
    run_research(query)
