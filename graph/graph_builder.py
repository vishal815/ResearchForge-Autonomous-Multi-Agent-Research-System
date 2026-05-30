# graph_builder.py
# Connects all nodes into one complete LangGraph pipeline.
#
# Flow:
#   planner → workers → synthesizer → quality_gate
#                            ↑               |
#                            |__ retry _______|  (if score < 7)
#                                            |
#                                           END  (if score >= 7)

from langgraph.graph import StateGraph, END
from graph.state import ResearchState
from graph.planner import planner_node
from graph.workers import workers_node
from graph.synthesizer import synthesizer_node
from graph.quality_gate import quality_gate_node, should_retry


def build_graph():
    """
    Builds and compiles the full LangGraph.
    Returns a runnable graph object.
    """

    graph = StateGraph(ResearchState)

    # Add all 4 nodes
    graph.add_node("planner",       planner_node)
    graph.add_node("workers",       workers_node)
    graph.add_node("synthesizer",   synthesizer_node)
    graph.add_node("quality_gate",  quality_gate_node)

    # Connect nodes in order
    graph.set_entry_point("planner")
    graph.add_edge("planner",      "workers")
    graph.add_edge("workers",      "synthesizer")
    graph.add_edge("synthesizer",  "quality_gate")

    # Conditional edge after quality gate
    graph.add_conditional_edges(
        "quality_gate",
        should_retry,
        {
            "retry": "synthesizer",   # score too low → retry
            "done":  END              # score good    → finish
        }
    )

    return graph.compile()
