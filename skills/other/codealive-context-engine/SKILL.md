---
name: codealive-context-engine
description: Semantic code search and AI-powered codebase Q&A across indexed repositories. Use when understanding code beyond local files, exploring dependencies, discovering cross-project patterns, planning features, debugging, or onboarding. Queries like "How does X work?", "Show me Y patterns", "How is library Z used?". Provides search (fast, returns file locations) and chat-with-codebase (slower, costs more, but returns synthesized answers).
---

# CodeAlive Context Engine

Semantic code intelligence across your entire code ecosystem — current project, organizational repos, dependencies, and any indexed codebase.

## Table of Contents

- [Tools Overview](#tools-overview)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Tool Reference](#tool-reference)
- [Data Sources](#data-sources)
- [Configuration](#configuration)

## Tools Overview

| Tool | Script | Speed | Cost | Best For |
|------|--------|-------|------|----------|
| **List Data Sources** | `datasources.py` | Instant | Free | Discovering indexed repos and workspaces |
| **Search** | `search.py` | Fast | Low | Finding code locations, file paths, snippets |
| **Chat with Codebase** | `chat.py` | Slow | High | Synthesized answers, architectural explanations |
| **Explore** | `explore.py` | Slow | High | Multi-step discovery workflows |

**Cost guidance:** Search is lightweight and should be the default starting point. Chat with Codebase invokes an LLM on the server side, making it significantly more expensive per call — use it when you need a synthesized, ready-to-use answer rather than raw search results.

## When to Use

**Use this skill for semantic understanding:**
- "How is authentication implemented?"
- "Show me error handling patterns across services"
- "How does this library work internally?"
- "Find similar features to guide my implementation"

**Use local file tools instead for:**
- Finding specific files by name or pattern
- Exact keyword search in the current directory
- Reading known file paths
- Searching uncommitted changes

## Quick Start

### 1. Discover what's indexed

```bash
python scripts/datasources.py
```

### 2. Search for code (fast, cheap)

```bash
python scripts/search.py "JWT token validation" my-backend
python scripts/search.py "error handling patterns" workspace:platform-team --mode deep
```

### 3. Chat with codebase (slower, richer answers)

```bash
python scripts/chat.py "Explain the authentication flow" my-backend
python scripts/chat.py "What about security considerations?" --continue CONV_ID
```

### 4. Multi-step exploration

```bash
python scripts/explore.py "understand:user authentication" my-backend
python scripts/explore.py "debug:slow database queries" my-service
```

## Tool Reference

### `datasources.py` — List Data Sources

```bash
python scripts/datasources.py              # Ready-to-use sources
python scripts/datasources.py --all        # All (including processing)
python scripts/datasources.py --json       # JSON output
```

### `search.py` — Semantic Code Search

Returns file paths, line numbers, and code snippets. Fast and cheap.

```bash
python scripts/search.py <query> <data_sources...> [options]
```

| Option | Description |
|--------|-------------|
| `--mode auto` | Default. Intelligent semantic search — use 80% of the time |
| `--mode fast` | Quick lexical search for known terms |
| `--mode deep` | Exhaustive search for complex cross-cutting queries. Resource-intensive |
| `--include-content` | Include full file content (use for external repos you can't Read locally) |

**Content inclusion rule:** Use `--include-content` only for repositories outside your working directory. For the current repo, get paths from search and then read files directly for latest content.

### `chat.py` — Chat with Codebase

Sends your question to an AI consultant that has full context of the indexed codebase. Returns synthesized, ready-to-use answers. Supports conversation continuity for follow-ups.

**This is more expensive than search** because it runs an LLM inference on the server side. Prefer search when you just need to locate code. Use chat when you need explanations, comparisons, or architectural analysis.

```bash
python scripts/chat.py <question> <data_sources...> [options]
```

| Option | Description |
|--------|-------------|
| `--continue <id>` | Continue a previous conversation (saves context and cost) |

**Conversation continuity:** Every response includes a `conversation_id`. Pass it with `--continue` for follow-up questions — this preserves context and is cheaper than starting fresh.

### `explore.py` — Smart Exploration

Combines search and chat-with-codebase in multi-step workflows. Useful for complex investigations.

```bash
python scripts/explore.py <mode:query> <data_sources...>
```

| Mode | Purpose |
|------|---------|
| `understand:<topic>` | Search + explanation |
| `dependency:<library>` | Library usage and internals |
| `pattern:<pattern>` | Cross-project pattern discovery |
| `implement:<feature>` | Find similar features for guidance |
| `debug:<issue>` | Trace symptom to root cause |

## Data Sources

**Repository** — single codebase, for targeted searches:
```bash
python scripts/search.py "query" my-backend-api
```

**Workspace** — multiple repos, for cross-project patterns:
```bash
python scripts/search.py "query" workspace:backend-team
```

**Multiple repositories:**
```bash
python scripts/search.py "query" repo-a repo-b repo-c
```

## Configuration

### Prerequisites

- Python 3.8+ (no third-party packages required — uses only stdlib)

### API Key Setup

The skill needs a CodeAlive API key. Resolution order:

1. `CODEALIVE_API_KEY` environment variable
2. OS credential store (macOS Keychain / Linux secret-tool / Windows Credential Manager)

**Environment variable (all platforms):**
```bash
export CODEALIVE_API_KEY="your_key_here"
```

**macOS Keychain:**
```bash
security add-generic-password -a "$USER" -s "codealive-api-key" -w "YOUR_API_KEY"
```

**Linux (freedesktop secret-tool):**
```bash
secret-tool store --label="CodeAlive API Key" service codealive-api-key
```

**Windows Credential Manager:**
```cmd
cmdkey /generic:codealive-api-key /user:codealive /pass:"YOUR_API_KEY"
```

**Base URL** (optional, defaults to `https://app.codealive.ai`):
```bash
export CODEALIVE_BASE_URL="https://your-instance.example.com"
```

Get API keys at: https://app.codealive.ai/settings/api-keys

## Detailed Guides

For advanced usage, see reference files:
- **[Query Patterns](references/query-patterns.md)** — effective query writing, anti-patterns, language-specific examples
- **[Workflows](references/workflows.md)** — step-by-step workflows for onboarding, debugging, feature planning, and more
