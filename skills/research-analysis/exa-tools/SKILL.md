---
name: exa-tools
type: complex
depth: base
user-invocable: false
description: >-
  Executes semantic web search via Exa AI Python CLI. Use when searching for
  current information, code examples, API documentation, finding similar pages,
  or generating AI answers with citations. Supports fast/deep/neural search.
---

# [H1][EXA-TOOLS]
>**Dictum:** *Semantic search surfaces relevant content.*

<br>

Execute Exa AI search queries via Python CLI. API key auto-injected via 1Password.

[IMPORTANT] Exa 2.0 introduced three search tiers: `fast` (sub-350ms), `auto` (balanced), `deep` (agentic, highest quality). Default: `auto`.

---
## [1][COMMANDS]

| [CMD]        | [ARGS]                 | [RETURNS]                        |
| ------------ | ---------------------- | -------------------------------- |
| search       | `<query> [type] [num]` | Web results with text content    |
| code         | `<query> [num]`        | GitHub code context              |
| find-similar | `<url> [num]`          | Pages similar to given URL       |
| answer       | `<query>`              | AI-generated answer with sources |

---
## [2][USAGE]

```bash
# Web search (default: auto type, 8 results)
uv run .claude/skills/exa-tools/scripts/exa.py search "Vite 7 new features"

# Neural search for concepts
uv run .claude/skills/exa-tools/scripts/exa.py search "Effect-TS best practices" neural

# Fast search for quick lookups
uv run .claude/skills/exa-tools/scripts/exa.py search "React 19 release notes" fast 15

# Deep search for highest quality
uv run .claude/skills/exa-tools/scripts/exa.py search "Nx workspace optimization" deep

# Code context search (GitHub)
uv run .claude/skills/exa-tools/scripts/exa.py code "React useState hook examples"

# Code search with custom results
uv run .claude/skills/exa-tools/scripts/exa.py code "Effect pipe examples" 20

# Find similar pages
uv run .claude/skills/exa-tools/scripts/exa.py find-similar "https://effect.website/docs/guides/essentials/pipeline"

# AI answer with citations
uv run .claude/skills/exa-tools/scripts/exa.py answer "What are the breaking changes in Vite 7?"
```

---
## [3][ARGUMENTS]

**search**: `<query> [type] [num]`
- `query` — Search query (required)
- `type` — Search type: `auto`, `neural`, `keyword`, `fast`, `deep` (default: `auto`)
- `num` — Number of results (default: `8`)

**code**: `<query> [num]`
- `query` — Code search query (required)
- `num` — Number of results (default: `10`)

**find-similar**: `<url> [num]`
- `url` — Source URL to find similar pages for (required)
- `num` — Number of results (default: `10`)

**answer**: `<query>`
- `query` — Question to answer with web sources (required)

---
## [4][OUTPUT]

Commands return: `{"status": "success|error", ...}`.

| [INDEX] | [CMD]          | [RESPONSE]                   |
| :-----: | -------------- | ---------------------------- |
|   [1]   | `search`       | `{query, results[]}`         |
|   [2]   | `code`         | `{query, context[]}`         |
|   [3]   | `find-similar` | `{url, results[]}`           |
|   [4]   | `answer`       | `{query, answer, sources[]}` |

---
## [5][ENVIRONMENT]

| [VAR]         | [REQUIRED] | [DESCRIPTION]                    |
| ------------- | ---------- | -------------------------------- |
| `EXA_API_KEY` | Yes        | Exa API key (1Password injected) |

---
## [6][ERROR_HANDLING]

- HTTP errors print `[ERROR] <status>: <body>` and exit 1
- Rate limit (429): retry after `Retry-After` header value
- Invalid API key: `[ERROR] 401: Unauthorized`
- Empty results: returns `{"status": "success", "results": []}` (not an error)
