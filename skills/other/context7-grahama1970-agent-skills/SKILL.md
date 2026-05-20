---
name: context7
description: >
  Fetch up-to-date library documentation from Context7 API. Use when user asks
  "how do I use this library", "show me docs for", "library documentation",
  "API reference for", or needs current documentation for any code library.
allowed-tools: Bash, Read
triggers:
  - library documentation
  - show me docs for
  - API reference
  - how to use this library
  - latest docs for
  - context7 lookup
metadata:
  short-description: Library documentation lookup via Context7

provides:
  - context7
composes:
  - memory
  - task-monitor
---

# Context7 Documentation Lookup Skill

Fetch up-to-date library documentation from Context7 API for ANY code library.

## Prerequisites

- `CONTEXT7_API_KEY` environment variable set (check `.env`)

## Quick Start

```bash
# Step 1: Find the library ID
python .pi/skills/context7/context7.py search <library-name> "<your-query>"

# Step 2: Get documentation context
python .pi/skills/context7/context7.py context <library-id> "<your-query>" --tokens 5000
```

## Commands at a Glance

| Command | Description | Example |
|---------|-------------|---------|
| `search` | Rank repositories by relevance to your query | `python .pi/skills/context7/context7.py search arangodb "bm25 search"` |
| `context` | Download reranked doc chunks for a specific library ID | `python .pi/skills/context7/context7.py context /arangodb/arangodb "vector search"` |
| `find` | Convenience multi-library search across common stacks | `python .pi/skills/context7/context7.py find "binary search"` |

These are the only supported subcommands; invoking the script without one will show Typer’s usage error. The table mirrors the exact signatures implemented in `context7.py`, so copy/paste examples will work as-is.

## API Endpoints

### 1. Search for ANY Library

Find libraries by name with LLM-powered ranking. Works with ANY library on GitHub:

```bash
# Search for any library - just change the libraryName
curl -s -X GET "https://context7.com/api/v2/libs/search?libraryName=<YOUR-LIBRARY>&query=<your-query>" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY" | jq '.results[:3]'

# Examples for different libraries:
curl -s "https://context7.com/api/v2/libs/search?libraryName=pandas&query=dataframe+merge" ...
curl -s "https://context7.com/api/v2/libs/search?libraryName=tensorflow&query=keras+model" ...
curl -s "https://context7.com/api/v2/libs/search?libraryName=django&query=orm+query" ...
```

Response includes library IDs like `/owner/repo` that you use in the context endpoint.

### 2. Get Documentation Context (PRIMARY)

Retrieve LLM-reranked documentation snippets for a query:

```bash
# Get ArangoDB BM25 documentation
curl -s -X GET "https://context7.com/api/v2/context?libraryId=/arangodb/arangodb&query=bm25+search+arangosearch&tokens=5000" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"

# Get Lean4 tactic documentation
curl -s -X GET "https://context7.com/api/v2/context?libraryId=/leanprover/lean4&query=simp+tactic&tokens=3000" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"

# Get sentence-transformers embedding docs
curl -s -X GET "https://context7.com/api/v2/context?libraryId=/UKPLab/sentence-transformers&query=encode+embeddings+cosine&tokens=3000" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

Parameters:
- `libraryId`: Library ID from search (e.g., `/arangodb/arangodb`)
- `query`: Natural language query
- `tokens`: Max tokens to return (default ~5000)

## Common Library IDs

Use `python context7.py search <name> "<query>"` to find ANY library's ID.

| Library | Library ID |
|---------|------------|
| ArangoDB | `/arangodb/arangodb` |
| Lean 4 | `/leanprover/lean4` |
| sentence-transformers | `/UKPLab/sentence-transformers` |
| PyTorch | `/pytorch/pytorch` |
| TensorFlow | `/tensorflow/tensorflow` |
| Pandas | `/pandas-dev/pandas` |
| NumPy | `/numpy/numpy` |
| Django | `/django/django` |
| Flask | `/pallets/flask` |
| FastAPI | `/tiangolo/fastapi` |
| Next.js | `/vercel/next.js` |
| React | `/facebook/react` |
| Vue.js | `/vuejs/vue` |
| Svelte | `/sveltejs/svelte` |
| Express | `/expressjs/express` |
| Rust std | `/rust-lang/rust` |
| Go std | `/golang/go` |

## Usage Examples

### Get ArangoDB AQL syntax for vector search
```bash
CONTEXT7_API_KEY=$(grep CONTEXT7_API_KEY .env | cut -d= -f2) \
curl -s "https://context7.com/api/v2/context?libraryId=/arangodb/arangodb&query=cosine+similarity+vector+search&tokens=3000" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

### Get Lean4 proof tactics
```bash
CONTEXT7_API_KEY=$(grep CONTEXT7_API_KEY .env | cut -d= -f2) \
curl -s "https://context7.com/api/v2/context?libraryId=/leanprover/lean4&query=omega+tactic+natural+numbers&tokens=3000" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

## Python Usage

The CLI surface is the preferred interface. If you embed it elsewhere, import
the Typer app or the helper functions directly:

```python
from .context7 import app, _search_libs, _get_context

result = _search_libs("arangodb", "bm25 search")
docs = _get_context("/arangodb/arangodb", "bm25 arangosearch scoring")
```

This matches the shipped code (`context7.py`).

## Shared Helpers

- `.pi/skills/dotenv_helper.py` loads `.env` automatically so `CONTEXT7_API_KEY` is present even when skills run via `uvx`.
- `.pi/skills/json_utils.py` can be imported to repair JSON before forwarding it to downstream tooling if you extend the skill; the built-in CLI already prints valid JSON.

## When to Use

1. When you need current documentation for a library
2. When official docs may have changed since training cutoff
3. When implementing features using unfamiliar APIs
4. To verify correct syntax for AQL, Lean4, or other DSLs
