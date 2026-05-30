# app.py — Main Streamlit UI
# Run from project root with:  streamlit run ui/app.py

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from graph.graph_builder import build_graph
from ui.components import (
    render_header,
    render_how_it_works,
    render_agent_status,
    render_virtual_files,
    render_quality_badge,
    render_report
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchForge",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ About")
    st.markdown("""
    **ResearchForge** is a multi-agent AI system built with:
    - 🔗 **LangGraph** — agent orchestration
    - 🤖 **Gemini 1.5 Flash** — LLM reasoning
    - 🌐 **Tavily** — web search
    - 📊 **LangSmith** — tracing
    """)
    st.divider()

    st.markdown("### 💡 Try These Queries")
    example_queries = [
        "Impact of AI on healthcare",
        "Future of renewable energy",
        "Blockchain in finance",
        "Rise of electric vehicles",
        "Quantum computing applications",
        "AI in education",
        "5G technology impact",
    ]
    for ex in example_queries:
        if st.button(f"📌 {ex}", use_container_width=True, key=f"btn_{ex}"):
            st.session_state["query_input"] = ex

    st.divider()
    st.markdown("### 🔗 Links")
    st.markdown("[GitHub Repo](#) · [LangSmith Traces](#)")

# ── Header ────────────────────────────────────────────────────────────────────
render_header()

# ── How it works ──────────────────────────────────────────────────────────────
with st.expander("ℹ️ How does this work?", expanded=False):
    render_how_it_works()

st.divider()

# ── Input section ─────────────────────────────────────────────────────────────
st.markdown("### 🔎 Enter Your Research Topic")

col_input, col_btn = st.columns([4, 1])

with col_input:
    query = st.text_input(
        label="query",
        placeholder="e.g. Impact of AI on healthcare",
        key="query_input",
        label_visibility="collapsed"
    )

with col_btn:
    run = st.button("🚀 Research", use_container_width=True, type="primary")

# ── Run pipeline ──────────────────────────────────────────────────────────────
if run and query.strip():

    st.divider()

    left_col, right_col = st.columns([1, 2])

    with st.spinner("🤖 Agents are working... this takes ~30-60 seconds"):

        graph = build_graph()

        initial_state = {
            "user_query":    query.strip(),
            "todos":         [],
            "virtual_files": {},
            "final_report":  None,
            "quality_score": None,
            "retry_count":   0,
            "status_log":    []
        }

        final_state = graph.invoke(initial_state)

    # Show results
    with left_col:
        render_agent_status(
            final_state.get("status_log", []),
            final_state.get("todos", [])
        )
        st.divider()
        render_virtual_files(final_state.get("virtual_files", {}))

    with right_col:
        render_quality_badge(final_state.get("quality_score"))
        render_report(final_state.get("final_report", "No report generated."))

elif run and not query.strip():
    st.warning("⚠️ Please enter a research topic first.")

else:
    # Empty state shown before first run
    st.markdown("""
        <div style='text-align:center; padding:5rem 0 3rem 0; color:#9ca3af;'>
            <div style='font-size:4rem;'>🔬</div>
            <p style='font-size:1.2rem; font-weight:500; color:#6b7280; margin-top:1rem;'>
                Enter a topic above and click <strong>🚀 Research</strong>
            </p>
            <p style='font-size:0.9rem;'>
                The AI agents will search, analyse, find examples, and write a full report.
            </p>
        </div>
    """, unsafe_allow_html=True)
