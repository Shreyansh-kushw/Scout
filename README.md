# 🕵️‍♂️ Scout: Autonomous AI Research Agent

> Deep, iterative research powered by agentic AI — grounded in sources, not hallucinations.

[![Live Demo](https://img.shields.io/badge/Live_Demo-Visit_Now-blue?style=for-the-badge)](https://scout-xz2j.onrender.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

![Python](https://img.shields.io/badge/Language-Python_3.12+-3776AB?style=flat-square&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-FF6B35?style=flat-square)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/LLM-Groq_(Llama--3)-F55036?style=flat-square)
![Gemini](https://img.shields.io/badge/LLM-Gemini_2.5_Flash-4285F4?style=flat-square&logo=google&logoColor=white)
![Tavily](https://img.shields.io/badge/Search-Tavily_API-6C63FF?style=flat-square)

Scout is an autonomous research agent that performs deep, iterative information retrieval and synthesis using agentic workflows. It solves the problem of surface-level LLM hallucinations by grounding every response in multiple cycles of search and evaluation, ensuring high-fidelity reports for complex queries. From an engineering perspective, Scout is built as a stateful cyclic graph using LangGraph, enabling controlled iteration, precise state management, and hybrid model orchestration.

---

## ⚙️ How It Works

Scout operates as a directed acyclic graph (with conditional loops) that manages the research lifecycle:

```text
       START
         |
[ Decompose Query ] <-----------+
         |                      |
  [ Search Query ]              | (Conditional Loop:
         |                      |  If Gaps Found & Iterations < 4)
  [ Evaluate Info ] ------------+
         |
[ Synthesize Response ]
         |
        END
```

### 🧩 Node Roles
- **Decompose Query**: Breaks the initial high-level question into a set of focused, searchable sub-queries.
- **Search Query**: Executes parallel searches via the Tavily API and applies strict heuristic filters to ensure content quality and relevance.
- **Evaluate Info**: Analyzes the current knowledge base to identify information gaps or missing context required to fully answer the original prompt.
- **Synthesize Response**: Aggregates all filtered search results and metadata into a structured, comprehensive markdown report.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Orchestration** | LangGraph | State machine management and cyclic agent workflow. |
| **LLM Framework** | LangChain | Abstraction layer for model interaction and prompt management. |
| **Language Models** | Groq (Llama-3) | High-speed, low-latency reasoning for decomposition and evaluation. |
| **Language Models** | Gemini 2.5 Flash | Large context window and high reasoning capability for synthesis. |
| **Search Engine** | Tavily API | Specialized AI-search for high-quality, clean content retrieval. |
| **API Framework** | FastAPI | Asynchronous RESTful interface for the research agent. |
| **Environment** | uv / Pydantic Settings | Dependency management and type-safe configuration. |

---

## 📁 Project Structure

```text
Scout/
├── app/
│   ├── agent/                 # Core agent logic
│   │   ├── nodes/             # LangGraph node implementations
│   │   │   ├── decompose.py   # Query breakdown logic
│   │   │   ├── evaluate.py    # Gap analysis and quality control
│   │   │   ├── search.py      # Tavily search execution and filtering
│   │   │   └── synthesise.py  # Final report generation
│   │   ├── __init__.py        # Graph construction and agent export
│   │   ├── models.py          # LLM initialization and provider config
│   │   └── state.py           # TypedDict defining the graph state
│   ├── schemas/               # Pydantic models for API I/O
│   └── utils/                 # Prompts and configuration management
├── main.py                    # FastAPI entry point
├── pyproject.toml             # Project metadata and dependencies
└── .env.example               # Template for environment variables
```

---

## 🚀 Setup

### 📋 Prerequisites
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) installed
- API keys for Groq, Google AI (Gemini), and Tavily

### 📥 Installation

1. Clone the repository and navigate to the root:
   ```bash
   git clone <repo-url>
   cd Scout
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Initialize the environment:
   ```bash
   cp .env.example .env
   ```

4. Fill in your API keys in `.env`, then start the server:
   ```bash
   uvicorn main:app --reload
   ```

*The API will be available at [http://localhost:8000](http://localhost:8000).*

### 📄 .env.example
```env
# Models
EVALUATION_QUERY_MODEL="llama3-70b-8192"
SYNTHESIS_MODEL="gemini-2.5-flash"

# API Keys
GROQ_API_KEY="your_groq_key"
GEMINI_API_KEY="your_gemini_key"
TAVILY_API_KEY="your_tavily_key"
```

---

## 📡 API

### `GET /research`
**Purpose**: Triggers the full research agent workflow for a given question.

**Request Parameters**:
- `question` (query, string): The research topic or question.

**Response Schema (`ResearchResponse`)**:

| Field | Type | Description |
| :--- | :--- | :--- |
| `question` | `string` | The original input question. |
| `queries` | `list[str]` | All search queries generated during the process. |
| `iterations` | `int` | Number of research cycles completed. |
| `sources` | `list[{title, url}]` | Cited sources used in the report. |
| `report` | `string` | The final synthesized markdown report. |

**Example Curl**:
```bash
curl -G "https://scout-xz2j.onrender.com/research" \
     --data-urlencode "question=What are the latest breakthroughs in solid-state battery technology for 2026?"
```

---

## 📖 Example

**Query**
> What has lead to the recent crackdown of the U.S. government on Anthropic?

**Response**

The U.S. government's recent crackdown on Anthropic, primarily occurring in 2026, stemmed from a multi-faceted dispute concerning national security, control over advanced AI capabilities, and Anthropic's policy on technology use [2][7][15][16][18][27].

## Reasons for the Crackdown

### Refusal to Waive "Red Lines"
A primary catalyst for the government's action was Anthropic CEO Dario Amodei's refusal to comply with demands from Defense Secretary Pete Hegseth [2][10]. Hegseth pressured Amodei to remove "red lines" that restricted the use of Anthropic's AI model, Claude, for **mass domestic surveillance** and **fully autonomous weapons systems** [2][16]. Anthropic had maintained these safeguards since signing a contract with the Pentagon in 2025, specifically to prevent its technology from being used for mass surveillance [10].

> Full response and sources: [`examples/anthropic-2026.md`](examples/anthropic-2026.md)

---

## 🚀 Deployment

Scout is deployed on [Render](https://render.com). To deploy your own instance:

1. Push your repository to GitHub.
2. Create a new **Web Service** on Render and connect the repo.
3. Set the **Start Command** to:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
4. Add the following **Environment Variables** in the Render dashboard:

   | Key | Value |
   | :--- | :--- |
   | `EVALUATION_QUERY_MODEL` | `llama3-70b-8192` |
   | `SYNTHESIS_MODEL` | `gemini-2.5-flash` |
   | `GROQ_API_KEY` | `your_groq_key` |
   | `GEMINI_API_KEY` | `your_gemini_key` |
   | `TAVILY_API_KEY` | `your_tavily_key` |

5. Deploy — Render will build and serve the API automatically.

> **Note:** Render free-tier instances spin down after inactivity. The first request after a cold start may take 30–60 seconds.

---

## 🛠️ Engineering Notes

1. **Heuristic Search Filtering**: In `search.py`, the agent applies a specific set of filters to Tavily results. It excludes content that is too short (<100 chars), too long (>3000 chars), or contains specific mathematical/encoding artifacts (e.g., `⊤`, `∫`, `−D/2`). This prevents the synthesis model from being overwhelmed by noise or low-quality scraped data.
2. **State Reducer Pattern**: The `ResearchState` uses `Annotated[list[str], operator.add]` for the `queries` and `search_results` fields. This ensures that every node execution appends to the history rather than overwriting it, which is critical for the `Evaluate Info` node to have a complete view of the research history.
3. **JSON Parsing Resilience**: The `Evaluate Info` node frequently handles raw string output from LLMs that should be JSON. The implementation includes a `try-except` block around `json.loads(gaps)` to prevent graph crashes during malformed model responses, providing a more robust execution loop.

---

## 📐 Design Decisions

1. **LangGraph over Raw LangChain Agents**: The team chose LangGraph to gain explicit control over the agent's iterative loop. Unlike standard autonomous agents that can "spin" indefinitely, LangGraph allows for hard-coded iteration limits (max 4 cycles) and predictable state transitions.
2. **Hybrid Model Orchestration**: Scout uses Groq for high-speed, low-cost utility tasks (decomposition/evaluation) and Gemini 2.5 Flash for the final synthesis. This balances latency and cost with the need for a large context window and high reasoning capability for the final report.
3. **Pydantic Settings for Configuration**: Instead of basic `os.getenv`, the project uses `pydantic-settings` to enforce type validation on environment variables at startup. This prevents runtime failures due to missing or incorrectly typed API keys or model names.