# components.py
# Reusable Streamlit UI building blocks.
# Each function draws one section of the app.

import streamlit as st


def render_header():
    st.markdown("""
        <div style='text-align:center; padding: 2rem 0 1rem 0;'>
            <h1 style='font-size:2.6rem; font-weight:800; margin:0;'>
                🔬 ResearchForge
            </h1>
            <p style='color:#6b7280; font-size:1.05rem; margin-top:0.4rem;'>
                Autonomous Research Agent &nbsp;·&nbsp; LangGraph + Gemini + Tavily
            </p>
        </div>
    """, unsafe_allow_html=True)


def render_how_it_works():
    st.markdown("### How it works")
    cols = st.columns(5)
    steps = [
        ("🧠", "Planner",      "Breaks your query into 3 tasks"),
        ("🔍", "Search",       "Finds web articles via Tavily"),
        ("📊", "Analysis",     "Summarises key findings"),
        ("🌍", "Examples",     "Finds real company cases"),
        ("✍️", "Synthesizer",  "Writes the final report"),
    ]
    for col, (icon, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
                <div style='text-align:center; padding:1rem 0.5rem;
                            background:#f9fafb; border-radius:10px;
                            border:1px solid #e5e7eb;'>
                    <div style='font-size:1.8rem;'>{icon}</div>
                    <div style='font-weight:600; margin:0.3rem 0;'>{title}</div>
                    <div style='font-size:0.78rem; color:#6b7280;'>{desc}</div>
                </div>
            """, unsafe_allow_html=True)


def render_agent_status(status_log: list, todos: list):
    st.markdown("### 🤖 Agent Activity")

    color_map = {
        "planner":     "#7c3aed",
        "search":      "#2563eb",
        "analysis":    "#0891b2",
        "examples":    "#059669",
        "synthesizer": "#d97706",
        "quality":     "#dc2626",
    }

    for entry in status_log:
        color = "#6b7280"
        for keyword, c in color_map.items():
            if keyword in entry.lower():
                color = c
                break
        st.markdown(f"""
            <div style='padding:0.45rem 1rem; margin:0.2rem 0;
                        border-left:4px solid {color};
                        background:#f9fafb; border-radius:0 6px 6px 0;
                        font-size:0.88rem;'>
                ✓ {entry}
            </div>
        """, unsafe_allow_html=True)

    if todos:
        st.markdown("**Task Checklist:**")
        for todo in todos:
            icon = "✅" if todo["status"] == "done" else "⏳"
            st.markdown(f"{icon} `{todo['assigned_to']}` — {todo['task']}")


def render_virtual_files(virtual_files: dict):
    st.markdown("### 📁 Agent Output Files")

    icons = {
        "search_results.txt": "🔍",
        "analysis.txt":       "📊",
        "examples.txt":       "🌍"
    }

    for filename, content in virtual_files.items():
        icon = icons.get(filename, "📄")
        with st.expander(f"{icon}  {filename}  ({len(content)} chars)"):
            st.text(content[:2000] + ("..." if len(content) > 2000 else ""))


def render_quality_badge(score):
    if score is None:
        return
    if score >= 8:
        color, label = "#059669", "Excellent"
    elif score >= 7:
        color, label = "#2563eb", "Good"
    elif score >= 5:
        color, label = "#d97706", "Fair"
    else:
        color, label = "#dc2626", "Low"

    st.markdown(f"""
        <div style='display:inline-flex; align-items:center; gap:0.5rem;
                    padding:0.4rem 1.2rem; border-radius:20px;
                    background:{color}18; border:1px solid {color};
                    margin-bottom:1rem;'>
            <span style='color:{color}; font-weight:600; font-size:0.95rem;'>
                ✅ Quality Score: {score}/10 — {label}
            </span>
        </div>
    """, unsafe_allow_html=True)


def render_report(report: str):
    st.markdown("### 📄 Final Research Report")
    st.markdown(report)
    st.divider()
    st.download_button(
        label="⬇️ Download Report as Markdown",
        data=report,
        file_name="research_report.md",
        mime="text/markdown",
        use_container_width=True
    )
