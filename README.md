# Memory Module — Qdrant-Powered Persistent Memory

> **Person 3 Deliverable** | Technical & Coding Research Agent | Hack Geek Room Hackathon

---

## What This Does

This module gives the AI agent **long-term memory across sessions**. Without this, the agent forgets everything after every conversation. With this, the agent remembers:

- User preferences (e.g. "I prefer code examples")
- Past research sessions (what was asked and answered)
- Key facts extracted from previous research

---

## Architecture

```
User sends query
      ↓
retrieve(user_id, query)   ← pulls relevant memory from Qdrant
      ↓
Agent answers using memory context
      ↓
store(user_id, query, result)  ← saves new memory to Qdrant
      ↓
Next session → agent remembers everything
```

### Three Qdrant Collections

| Collection | What it stores | Example |
|---|---|---|
| `user_preferences` | How the user likes answers | "I prefer code examples" |
| `research_history` | Past queries and summaries | "What is RAG?" → summary |
| `key_facts` | Important facts from research | "LoRA reduces params by 90%" |

---

## File Structure

```
memory/
├── __init__.py         # Clean interface for Person 1 (agent orchestration)
├── qdrant_db.py        # Connects to Qdrant Cloud, creates collections + indexes
├── store.py            # Saves preferences, research history, key facts
└── retrieve.py         # Fetches relevant memory using semantic search
```

---

## How It Works (Semantic Search)

Unlike a normal database that matches exact words, this module uses **vector embeddings** to find memory by *meaning*.

```
"I prefer code examples"   →  [0.23, 0.87, 0.12 ...]  (384 numbers)
"Show me with code"        →  [0.21, 0.85, 0.14 ...]  (similar numbers!)
```

When the user asks something new, we find memories with *similar meaning* — even if the exact words are different. This is powered by `sentence-transformers/all-MiniLM-L6-v2`.

---

## Setup

### 1. Install dependencies

```bash
pip install qdrant-client sentence-transformers python-dotenv
```

### 2. Create `.env` file

```env
QDRANT_URL=https://your-cluster.qdrant.io:6333
QDRANT_API_KEY=your_api_key_here
```

> Never commit your `.env` file to GitHub. Add it to `.gitignore`.

### 3. Initialize Qdrant collections

```bash
python memory/qdrant_db.py
```

You should see:
```
[CREATED] user_preferences
[CREATED] research_history
[CREATED] key_facts
Qdrant is connected and ready!
```

---

## Usage (For Person 1 — Agent Orchestration)

Only 2 functions needed:

```python
from memory import retrieve, store

# STEP 1: Before agent answers — inject memory into context
context = retrieve("user123", query)
# Returns formatted string like:
# USER PREFERENCES:
#   - I prefer code examples
# PAST RESEARCH:
#   - Asked: what is RAG?
#     Summary: RAG is retrieval augmented generation

# STEP 2: After agent answers — save to memory
store("user123", query, {
    "summary": "RAG stands for Retrieval Augmented Generation...",
    "mode": "quick",           # or "deep"
    "preference": "I prefer code examples",   # optional
    "fact": "RAG reduces hallucinations",     # optional
    "topic": "RAG"                            # optional
})
```

---

## Usage (For Person 4 — Frontend)

### Show what the agent remembers

```python
from memory.retrieve import retrieve_preferences

prefs = retrieve_preferences("user123", "", limit=10)
# Returns: ["I prefer code examples", "No math-heavy explanations"]
```

### Clear user memory (forget button)

```python
from memory import clear

clear("user123")  # wipes all memory for this user
```

---

## Judging Criteria Coverage

| Criteria | Weight | How this module helps |
|---|---|---|
| Qdrant Usage | 10% | Core Qdrant Cloud integration with 3 collections |
| Memory Effectiveness | 10% | Semantic retrieval improves every answer |
| Architecture & Design | 15% | Clean separation of store / retrieve / connect |
| Production Readiness | 5% | .env config, error handling, no hardcoded keys |

**Total direct impact: ~40% of judging criteria**

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Qdrant Cloud | Vector database (free tier) |
| sentence-transformers | Text → vector embeddings |
| all-MiniLM-L6-v2 | Embedding model (384 dimensions) |
| python-dotenv | Secure config management |

---

## Key Design Decisions

**Why Qdrant over a regular database?**
Regular databases match exact words. Qdrant matches by *meaning*, so "show me with code" correctly retrieves the preference "I prefer code examples."

**Why 3 separate collections?**
Each stores different types of data with different retrieval patterns. Preferences are user-level. History is query-level. Facts are topic-level.

**Why all-MiniLM-L6-v2?**
Fast, lightweight (90MB), and accurate enough for this use case. Runs locally with no API cost.

---

*Built for Hack Geek Room AI Hackathon — Technical & Coding Research Agent*
