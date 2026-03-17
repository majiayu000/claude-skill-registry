---
name: gemini
description: Gemini CLI for one-shot Q&A, summaries, and generation. Integrates with NotebookLM for deep research. Use when asked to search the web, research topics, generate content, or query NotebookLM sources.
---

# Gemini Skill

## Overview

Use Google Gemini subscription for all AI and web search needs. **No separate API keys required** - uses your Google account.

## Primary Tool: `gemini` CLI

The official Gemini CLI is installed at `/opt/homebrew/bin/gemini`.

### Web Search (One-Shot)

```bash
gemini "What is the weather forecast for King, NC?"
gemini "Latest news about Epic EHR"
gemini "Research competitive landscape for X"
```

### JSON Output (for scripting)

```bash
gemini "your query" --output-format json
```

### Interactive Mode

```bash
gemini -i "Start researching topic X"
```

## NotebookLM Integration

For deep research with source synthesis:

```bash
# Quick search (adds sources to notebook)
nlm source add-research "your query" --notebook <id>

# Deep research (adds sources to notebook)
nlm source add-research "your query" --notebook <id> --mode deep

# Query notebook sources
nlm ask -n <id> --new "your question"
```

## When to Use What

| Task | Tool |
|------|------|
| Quick web search | `gemini "query"` |
| One-shot Q&A | `gemini "question"` |
| Deep research with sources | `nlm source add-research --mode deep` |
| Query documents/sources | `nlm ask -n <id>` |
| Generate podcast | `nlm generate audio` |

## No API Keys Needed

Your Gemini subscription handles:
- Web search
- Text generation
- NotebookLM features
- All Gemini models

**Do NOT use:**
- Brave Search API (unnecessary cost)
- Separate Gemini API keys
- Other web search services

## Authentication

Both tools use your Google account:
- `gemini`: Auto-authenticates via cached credentials
- `nlm`: Requires `nlm login` (browser-based, ~20 min sessions)

## Files

- System CLI: `/opt/homebrew/bin/gemini`
- NotebookLM CLI: `/opt/homebrew/bin/nlm`
- Custom wrapper: `skills/gemini/gemini_cli.py` (optional, wraps both)
