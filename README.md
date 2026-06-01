# 🔬 ResearchForge

<img width="1536" height="1024" alt="ChatGPT Image May 31, 2026, 03_12_43 AM" src="https://github.com/user-attachments/assets/a5fe5c25-b012-4015-beb3-7c4914cc4d5b" />

### Autonomous Multi-Agent Research System · Powered by LangGraph + Gemini + Tavily

> **Give it a topic. Get a full research report.**
> ResearchForge uses a team of AI agents that plan, search, analyse, find examples, write, and self-check — all automatically.

### 🔗 Open Live Application

**👉 https://huggingface.co/spaces/Visal9252/Autonomous_Multi-Agent_Research_System**

No installation required. Just enter a research topic and watch the AI agents work.

---

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-latest-purple)](https://langchain-ai.github.io/langgraph/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5--flash-orange?logo=google)](https://aistudio.google.com)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?logo=streamlit)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📌 Table of Contents

1. [What is ResearchForge?](#-what-is-researchforge)
2. [How It Works — Real Example](#-how-it-works--real-example)
3. [Core Concepts Explained](#-core-concepts-explained)
4. [Architecture](#-architecture)
5. [Folder Structure](#-folder-structure)
6. [Getting API Keys (Free)](#-getting-api-keys-free)
7. [Installation & Setup](#-installation--setup)
8. [Running the Project](#-running-the-project)
9. [Download Report as PDF](#-download-report-as-pdf)
10. [Running project demo Video](#-output-demo-video-of-project)
11. [Concepts Covered](#-concepts-covered)
12. [Troubleshooting](#-troubleshooting)
13. [Contributing](#-contributing)

---

## 🤔 What is ResearchForge?

ResearchForge is a **multi-agent AI research system** that takes one research question from you and automatically:

1. **Plans** the research by breaking your query into subtasks
2. **Searches** the web for real, current information
3. **Analyses** the information and finds key insights
4. **Finds** real-world company examples and case studies
5. **Writes** a complete structured research report
6. **Scores** its own report and retries if quality is low
7. **Delivers** the report through a clean web UI with a PDF download

**This is not a simple chatbot.** It is an autonomous pipeline of specialised AI agents working together — the same architectural pattern used in production AI systems at companies like Anthropic, Google DeepMind, and OpenAI.

### Who is this for?

| Audience | How to use it |
|----------|--------------|
| 🎓 **Students** | Research papers, assignment preparation, topic deep-dives |
| 💼 **Professionals** | Market research, technology evaluation, competitor analysis |
| 🧑‍💻 **Developers** | Learn LangGraph, multi-agent systems, and agentic AI patterns |
| 🏢 **Interns / Freshers** | Portfolio project that demonstrates real AI engineering skills |

---

## ⚡ How It Works — Real Example

Let's trace what happens when you type:

> **"Research the impact of AI on healthcare"**

```
Step 1 — YOU TYPE THE QUERY
        ↓
Step 2 — PLANNER NODE (Gemini LLM)
         Reads your query and creates 3 tasks:
         TODO 1 → search_agent   : "Search for AI healthcare applications 2024"
         TODO 2 → analysis_agent : "Analyse key findings and themes in AI healthcare"
         TODO 3 → examples_agent : "Find real company examples like IBM Watson, DeepMind"
        ↓
Step 3 — WORKERS NODE (3 agents run one after another)

         [Search Agent]
         → Calls Tavily API → gets 5 real web articles
         → Saves to virtual file: search_results.txt

         [Analysis Agent]
         → Reads search_results.txt
         → Sends to Gemini: "Summarise key findings, themes, challenges"
         → Saves structured analysis to: analysis.txt

         [Examples Agent]
         → Searches specifically for company case studies
         → Gemini formats 3 real examples
         → Saves to: examples.txt
        ↓
Step 4 — SYNTHESIZER NODE
         → Reads all 3 files together
         → Asks Gemini to write a full report with:
           Executive Summary, Key Findings, Analysis,
           Real Examples, Challenges, Future Outlook, Conclusion
        ↓
Step 5 — QUALITY GATE NODE
         → Gemini scores the report from 0 to 10
         → Score ≥ 7 → Send to UI as final report ✅
         → Score < 7 → Go back to Synthesizer and retry (max 2 retries)
        ↓
Step 6 — FINAL REPORT shown in Streamlit UI
         → Download as Markdown or PDF
```

**The whole process takes about 30–60 seconds.**

---

## 🧠 Core Concepts Explained

### What is an AI Agent?
An AI agent is an LLM (like Gemini) that can **decide what action to take** based on its current situation. Unlike a simple chatbot that only replies, an agent can call tools, save data, read files, and loop until a goal is achieved.

### What is LangGraph?
LangGraph is a Python library for building **stateful, multi-step AI workflows**. You define:
- **Nodes** — individual steps (planner, workers, synthesizer)
- **Edges** — connections between steps
- **State** — shared memory passed between all nodes

Think of it like a flowchart where each box is an AI agent and the arrows are the flow of information.

### What is a Virtual File System?
Instead of saving files to your actual hard drive, ResearchForge uses a Python dictionary inside LangGraph's state to simulate a file system. Each agent "writes a file" (saves to the dict) and other agents can "read" it later.

```python
# Writing a file (inside state dict)
virtual_files["search_results.txt"] = "AI is used in hospitals for..."

# Reading a file
content = virtual_files["search_results.txt"]
```

### What is the Quality Gate?
After the synthesizer writes a report, the quality gate node asks Gemini: *"Score this report from 0–10."* If the score is below 7, the whole synthesizer step runs again with a note to improve. This makes the system **self-correcting**.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INPUT                           │
│              "Research AI impact on healthcare"             │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    PLANNER NODE                             │
│   Gemini LLM reads query → creates 3 TODO tasks            │
│   Saves: todos[] in LangGraph State                         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    WORKERS NODE                             │
│                                                             │
│   ┌─────────────────┐  ┌────────────────┐  ┌────────────┐  │
│   │  Search Agent   │  │ Analysis Agent │  │  Examples  │  │
│   │                 │  │                │  │   Agent    │  │
│   │ Tavily API call │  │ Gemini summary │  │ Web search │  │
│   │ → 5 articles    │  │ → key insights │  │ + Gemini   │  │
│   │                 │  │                │  │ formatting │  │
│   └────────┬────────┘  └───────┬────────┘  └─────┬──────┘  │
│            │                   │                  │         │
│            ▼                   ▼                  ▼         │
│   search_results.txt      analysis.txt       examples.txt   │
│              (Virtual File System in LangGraph State)        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  SYNTHESIZER NODE                           │
│   Reads all 3 virtual files                                 │
│   Gemini writes structured 7-section report                 │
│   Saves: final_report in state                              │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  QUALITY GATE NODE                          │
│   Gemini scores report (0–10)                               │
│   Score ≥ 7  ──────────────────────────────────► END ✅     │
│   Score < 7  ──────────────► back to Synthesizer (retry)   │
│   Max 2 retries                                             │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT UI                             │
│   • Agent activity log (live status)                        │
│   • Task checklist (TODOs)                                  │
│   • Expandable agent output files                           │
│   • Quality score badge                                     │
│   • Full formatted report                                   │
│   • Download as Markdown or PDF                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Folder Structure

```
researchforge/
│
├── graph/                         ← LangGraph agent nodes
│   ├── __init__.py
│   ├── state.py                   ← Shared memory schema (TypedDict)
│   ├── planner.py                 ← Node 1: Breaks query into TODOs
│   ├── workers.py                 ← Node 2: 3 specialist agents
│   ├── synthesizer.py             ← Node 3: Merges outputs into report
│   ├── quality_gate.py            ← Node 4: Scores + retry logic
│   └── graph_builder.py           ← Wires all nodes into one graph
│
├── tools/                         ← Utility functions used by agents
│   ├── __init__.py
│   ├── search_tool.py             ← Tavily web search wrapper
│   └── file_system.py             ← Virtual FS: read/write/list files
│
├── ui/                            ← Streamlit frontend
│   ├── app.py                     ← Main UI entry point
│   └── components.py              ← Reusable UI sections
│
├── main.py                        ← Terminal test runner (no UI)
├── requirements.txt               ← All Python dependencies
├── .env                           ← API keys (never commit this)
├── .gitignore                     ← Excludes .env, .venv, cache
└── README.md                      ← This file
```

### What each key file does

| File | Role | Analogy |
|------|------|---------|
| `state.py` | Defines the shared memory | A whiteboard every agent reads & writes |
| `planner.py` | Creates the task list | A project manager assigning work |
| `workers.py` | Runs the 3 agents | 3 specialists doing their jobs |
| `synthesizer.py` | Writes the report | An editor assembling everything |
| `quality_gate.py` | Reviews and scores | A QA reviewer checking output |
| `graph_builder.py` | Connects all nodes | Plugging cables into a circuit board |
| `search_tool.py` | Calls Tavily search | A web browser for the agent |
| `file_system.py` | Virtual file read/write | A shared Google Drive for agents |
| `app.py` | Streamlit UI | The front door of the application |

## 🔑 Getting API Keys (Free)

You need at least **one LLM API key** to run the project. For the best experience, **Groq** is recommended because it offers faster responses and a much more generous free tier than Gemini.

---

### 1. Google Gemini API Key ✅ Required · Free

Gemini is the default LLM that powers all reasoning in the project.

**Steps:**

1. Go to **https://aistudio.google.com**
2. Sign in with your Google account
3. Click **"Get API Key"**
4. Click **"Create API Key"**
5. Copy the generated key (`AIzaSy...`)

**Free Tier Limits:**

* 15 requests per minute
* 1,500 requests per day
* 1 million tokens per day

> ⚠️ If you receive a `429 RESOURCE_EXHAUSTED` error, you have reached Gemini's free-tier limits.

---

### 2. Tavily Search API Key ✅ Recommended · Free

Tavily provides real-time web search capabilities for ResearchForge.

**Steps:**

1. Go to **https://app.tavily.com**
2. Sign up using Google or email
3. Open your Dashboard
4. Copy the API key (`tvly-...`)

**Free Tier:**

* 1,000 searches/month

> Without Tavily, the agents can still work, but reports will rely on model knowledge instead of live web data.

---

### 3. Groq API Key ⭐ Recommended · Free

Groq is currently the best free alternative to Gemini and works exceptionally well with LangGraph-based multi-agent systems.

#### Why Groq?

* ⚡ Ultra-fast inference
* 🆓 Generous free tier
* 🚀 Excellent for LangGraph workflows
* 🔥 Fewer rate-limit issues than Gemini
* 💰 No billing required for getting started

#### Steps

1. Go to **https://console.groq.com**
2. Sign up with Google, GitHub, or email
3. Open **API Keys**
4. Click **Create API Key**
5. Copy your API key (`gsk_...`)

#### Free Tier

* Up to **14,400 requests/day**
* Suitable for demos, testing, portfolio projects, and hackathons

#### Install

```bash
uv pip install langchain-groq
```

#### Add to `.env`

```env
GROQ_API_KEY=your_key_here
```

#### Replace Gemini in All Graph Files

Update these files:

* `planner.py`
* `workers.py`
* `synthesizer.py`
* `quality_gate.py`

Remove:

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.4
)
```

Add:

```python
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.4
)
```

#### Recommended Model

```python
model="llama-3.3-70b-versatile"
```

Alternative models:

```python
model="deepseek-r1-distill-llama-70b"
model="qwen/qwen3-32b"
```

---

### 4. LangSmith API Key 🔍 Optional · Free (Tracing & Debugging)

LangSmith allows you to visualize every step in the agent workflow, making it extremely useful for debugging and learning how LangGraph works internally.

**Steps:**

1. Go to **https://smith.langchain.com**
2. Sign up for free
3. Open **Settings → API Keys**
4. Create a new API key

Example:

```text
lsv2_xxxxxxxxxxxxxxxxx
```

Add to `.env`:

```env
LANGCHAIN_API_KEY=your_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=researchforge
```

---

### Alternative Free LLM Options

#### Option A — OpenRouter

```python
from langchain_community.chat_models import ChatOpenAI

llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)
```

#### Option B — Hugging Face Inference API

```python
from langchain_community.llms import HuggingFaceHub

llm = HuggingFaceHub(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_KEY")
)
```

### Recommended Provider Order

1. 🥇 Groq (Best Free Option)
2. 🥈 Gemini
3. 🥉 OpenRouter
4. 🎖 Hugging Face


---

### ⚙️ Installation & Setup

### Prerequisites
- Python 3.11 or higher → [Download](https://python.org/downloads)
- Git → [Download](https://git-scm.com)
- VS Code (recommended) → [Download](https://code.visualstudio.com)

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/vishal815/ResearchForge-Autonomous-Multi-Agent-Research-System.git
cd researchforge
```

Or download the ZIP and extract it, then:
```bash
cd researchforge
```

---

### Step 2 — Install uv (Fast Package Manager)

```bash
pip install uv
```

Verify it worked:
```bash
uv --version
```

---

### Step 3 — Create Virtual Environment

```bash
uv venv
```

This creates a `.venv` folder — an isolated Python environment just for this project.

---

### Step 4 — Activate the Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac / Linux:**
```bash
source .venv/bin/activate
```

You will see `(researchforge)` appear at the start of your terminal line. This means the environment is active.

> ⚠️ You must activate the environment every time you open a new terminal.

---

### Step 5 — Install Dependencies

```bash
uv pip install -r requirements.txt
```

This installs: `langgraph`, `langchain`, `langchain-google-genai`, `tavily-python`, `streamlit`, `python-dotenv`, `langsmith`, `fpdf2`

---

### Step 6 — Create Your `.env` File

Create a file named `.env` in the root of the project (same level as `main.py`):

```bash
# Windows
type nul > .env

# Mac / Linux
touch .env
```

Open `.env` in VS Code and add your keys:

```env
# Required
GOOGLE_API_KEY=your_gemini_key_here

# Optional but recommended
GROQ_API_KEY=your_key_here
or
TAVILY_API_KEY=your_tavily_key_here

# Optional — for LangSmith tracing
LANGCHAIN_API_KEY=your_langsmith_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=researchforge
```

> 🔒 The `.env` file is already in `.gitignore` — it will never be pushed to GitHub.

---

## ▶️ Running the Project

### Option A — Terminal Mode (test first)

Run this to test the full pipeline without the UI:

```bash
python main.py
```

You will see each agent printing its status in the terminal. At the end, a report is saved to `output_report.md`.

**Expected output:**
```
============================================================
  ResearchForge
  Query: Research the impact of artificial intelligence on healthcare
============================================================

[Planner] Breaking query into tasks...
[Planner] Created 3 TODOs

[Workers] Starting all 3 agents...
  [Search Agent] Searching the web...
  [Search Agent] Done. Saved to search_results.txt
  [Analysis Agent] Analysing search results...
  [Analysis Agent] Done. Saved to analysis.txt
  [Examples Agent] Finding real-world examples...
  [Examples Agent] Done. Saved to examples.txt

[Synthesizer] Merging all research into final report...
[Synthesizer] Report generated successfully.

[Quality Gate] Scoring the report...
[Quality Gate] Score = 8.5/10
[Quality Gate] Report accepted.

Report saved to output_report.md
```

---

### Option B — Streamlit Web UI

```bash
streamlit run ui/app.py
```

Your browser opens automatically at `http://localhost:8501`

**What you see in the UI:**
- A text input box to enter your research topic
- Example query buttons in the sidebar
- Live agent activity log (what each agent is doing)
- Task checklist showing TODO progress
- Expandable panels showing each agent's raw output file
- Quality score badge
- The final formatted research report
- Download button for Markdown and PDF

---

## 📄 Download Report as PDF

ResearchForge generates reports in Markdown format.

The PDF download button appears automatically in the UI after a report is generated. The PDF includes:
- Project title and date
- All report sections with proper formatting
- Clean, readable font (uses built-in PDF fonts for compatibility)

---

## 🎬 Output Demo Video of Project

![ResearchForge Demo](

https://github.com/user-attachments/assets/f34f0e95-37ac-49f8-8243-ed7055c4b31d

)

### What the demo shows

* 🔎 User enters a research topic
* 🧠 Planner Agent creates research tasks
* 🔍 Search Agent gathers web information
* 📊 Analysis Agent extracts insights
* 🌍 Examples Agent finds real-world case studies
* ✍️ Synthesizer Agent writes the final report
* ✅ Quality Gate reviews and scores the report
* 📄 Final research report generated
* 📥 PDF download available


## 📚 Concepts Covered

This project is a practical implementation of several important AI engineering concepts:

| Concept | Where it appears | Why it matters |
|---------|-----------------|----------------|
| **Agentic AI** | Every node in the graph | Agents decide actions autonomously |
| **LangGraph StateGraph** | `graph_builder.py` | Stateful multi-step orchestration |
| **Shared State Management** | `state.py` | How agents share information |
| **Tool Use** | `search_tool.py` | Agents calling external APIs |
| **Virtual File System** | `file_system.py` | Context offloading across steps |
| **ReAct Pattern** | `workers.py` | Reason → Act → Observe loop |
| **LLM-as-Judge** | `quality_gate.py` | Self-evaluation and quality control |
| **Conditional Edges** | `graph_builder.py` | Dynamic routing based on conditions |
| **Retry Logic** | `quality_gate.py` | Automatic self-correction |
| **Prompt Engineering** | Every node | Structured prompts for consistent output |
| **Multi-Agent Systems** | Full pipeline | Specialised agents for specialised tasks |
| **Supervisor Pattern** | Planner → Workers | One agent orchestrating others |

---

## 🔧 Troubleshooting

### `404 NOT_FOUND` — Model not found
Your model name is wrong. Use exactly:
```python
model="gemini-2.5-flash"
```

### `429 RESOURCE_EXHAUSTED` — Rate limit hit
You hit Gemini's free tier per-minute limit. Wait 60 seconds and try again. For production use, add billing to your Google Cloud project.

### `ModuleNotFoundError`
Your virtual environment is not activated. Run:
```bash
# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

Then install again:
```bash
uv pip install -r requirements.txt
```

### Search agent returns "Search failed"
Your `TAVILY_API_KEY` is missing or wrong. The project will still work — agents will use Gemini's knowledge instead of live web data.

### Streamlit UI does not open
Make sure you run from the project root folder:
```bash
# Must be in researchforge/ folder
streamlit run ui/app.py
```

### `GOOGLE_API_KEY` not loading
Check that your `.env` file is in the root of the project (same folder as `main.py`), not inside `graph/` or any subfolder.

---

## 🤝 Contributing

Contributions welcome! Here are ideas to extend the project:

- [ ] Add a `citation_agent` that formats academic references
- [ ] Add LangSmith evaluation dashboard integration
- [ ] Add support for uploading a PDF as research context
- [ ] Add memory across sessions using LangGraph checkpointing
- [ ] Deploy to Streamlit Cloud or Render
- [ ] Add OpenRouter / Hugging Face as model selector in UI

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

## 🙏 Acknowledgements

- [LangGraph](https://langchain-ai.github.io/langgraph/) — agent orchestration framework
- [Google Gemini](https://aistudio.google.com) — LLM powering all reasoning
- [Tavily](https://tavily.com) — real-time web search API
- [Streamlit](https://streamlit.io) — Python web UI framework
- [LangSmith](https://smith.langchain.com) — agent tracing and evaluation

---

<div align="center">

**Keep Learing and keep Growing.**


*If this helped you learn something, give it a ⭐ on GitHub!*
**Vishal Lazurs**

</div>
