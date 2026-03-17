---
name: perplexity
description: >
  Paid research assistant with real-time web search. Use when user asks "what's the latest",
  "current pricing for", "recent news about", "search the web for", "fact check this",
  "what's new in", or needs up-to-date information beyond training data.
allowed-tools: Bash, Read
triggers:
  - what's the latest
  - current pricing
  - recent news
  - search the web
  - fact check
  - what's new in
  - look up online
  - research this topic
  - paid search
metadata:
  short-description: AI research with web search

provides:
  - perplexity
composes:
  - dogpile
  - memory
  - task-monitor
---

# Perplexity Skill

AI-powered research assistant with real-time web search capabilities.

## Prerequisites

- `PERPLEXITY_API_KEY` in `.env` (get from https://www.perplexity.ai/settings/api)

## When to Use

- Current information (news, recent releases, pricing)
- Technical questions requiring up-to-date docs
- Fact-checking and verification
- Research questions needing multiple sources
- Comparisons (libraries, tools, approaches)

## Quick Start

```bash
# Simple query (quick answer)
python .pi/skills/perplexity/perplexity.py ask "What's new in Python 3.12?"

# With citations (JSON output)
python .pi/skills/perplexity/perplexity.py research "ArangoDB vs Neo4j for knowledge graphs"

# With specific model
python .pi/skills/perplexity/perplexity.py ask --model large "Best practices for Lean4 proofs"
```

## Commands at a Glance

| Command | What it does | Notes |
|---------|--------------|-------|
| `ask` | Fast answer with short citations preview | Matches the Typer command implemented in `perplexity.py ask` |
| `research` | Full answer + citations JSON | Equivalent to calling `_research()` and prints JSON unless `--no-json` |
| `models` | Lists available model aliases → API IDs | Useful when wiring the skill into other agents |

Every CLI example **must** include the subcommand (`ask`, `research`, or `models`) because the Typer app requires it; omitting the subcommand will raise a usage error. The shipped SKILL docs now mirror the exact runner arguments, so you can copy/paste them without edits.

## CLI Usage

Two commands: `ask` (quick answer) and `research` (with citations):

```bash
# Quick answer
python .pi/skills/perplexity/perplexity.py ask [OPTIONS] "your question"

# Research with citations (JSON output)
python .pi/skills/perplexity/perplexity.py research [OPTIONS] "your question"

Options:
  --model, -m     small|large|huge  (default: small, fast)
  --system, -s    Custom system prompt
  --json/--no-json  JSON output (research default: --json)
```

## Python API

```python
# Import the internal function
from perplexity import _research

# Research with citations
result = _research("What is BM25 scoring?", model="small")
print(result["answer"])
print(result["citations"])
```

Note: The CLI commands `ask` and `research` are the primary interface. For Python usage, use `_research()` directly.

## Shared Helpers

- `.pi/skills/dotenv_helper.py` is auto-imported so `.env` keys (e.g., `PERPLEXITY_API_KEY`) load without manual sourcing.
- `.pi/skills/json_utils.py` is available if you need to repair downstream JSON before writing it to files; the `research` command already emits valid JSON, so most callers can stream it directly.

## Models

| Model | API Name | Speed | Use Case |
|-------|----------|-------|----------|
| `small` | sonar | Fast | Quick lookups, simple questions |
| `large` | sonar-pro | Medium | Technical research, comparisons |
| `huge` | sonar-reasoning | Slow | Complex analysis, reasoning |

## Examples

### Technical Research
```bash
python .pi/skills/perplexity/perplexity.py ask "How to implement hybrid search with BM25 and vector similarity?"
```

### Current Information
```bash
python .pi/skills/perplexity/perplexity.py ask "Latest Anthropic Claude API changes 2024"
```

### Comparison
```bash
python .pi/skills/perplexity/perplexity.py ask --model large "sentence-transformers vs OpenAI embeddings for code search"
```

## vs Context7

| Perplexity | Context7 |
|------------|----------|
| General research | Library-specific docs |
| Real-time web search | Curated documentation |
| Any topic | Code libraries only |
| Synthesized answers | Raw doc snippets |

Use **Context7** for: specific library API syntax, exact function signatures
Use **Perplexity** for: research, comparisons, current information, general questions
