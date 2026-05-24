---
name: arxiv
description: >
  Search arXiv for papers and extract knowledge into memory.
  Use `search` to find papers, `learn` to extract knowledge.
allowed-tools: Bash, Read
triggers:
  - learn from arxiv
  - learn from this paper
  - extract knowledge from paper
  - find papers on
  - search arxiv
  - arxiv
metadata:
  short-description: arXiv paper search and knowledge extraction
---

# arXiv Skill

Search arXiv and extract knowledge into memory.

## Commands

| Command | Description |
|---------|-------------|
| `search` | Find papers (returns abstracts for triage) |
| `learn` | Extract knowledge into memory |

---

## `search` - Find Papers

```bash
./run.sh search -q "agent memory" -n 5
```

Returns papers with **full abstracts** for quick triage.

| Option | Description |
|--------|-------------|
| `-q` | Search query (required) |
| `-n` | Max results (default: 10) |
| `-c` | Category filter (e.g., cs.LG) |
| `-m` | Papers from last N months |
| `--smart` | LLM translates natural language query |

---

## `learn` - Extract Knowledge

```bash
./run.sh learn 2601.08058 --scope memory
```

Full pipeline: download → distill → interview → store → verify edges.

| Option | Description |
|--------|-------------|
| `--scope` | Memory scope (required) |
| `--context` | Domain focus for relevance |
| `--dry-run` | Preview without storing |
| `--skip-interview` | Auto-accept recommendations |

---

## Happy Path

```bash
# 1. Search - scan abstracts
./run.sh search -q "agent memory systems" -n 5

# 2. Learn - from relevant paper
./run.sh learn 2601.10702 --scope memory --context "agent systems"
```

That's it. Two commands.
