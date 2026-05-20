---
name: context7-tools
type: complex
depth: base
user-invocable: false
description: >-
  Queries version-specific library documentation from Context7. Use when fetching API references, code examples,
  or conceptual guides for npm/PyPI packages. Resolves library IDs, retrieves docs by topic. Not for web search.
---

# [H1][CONTEXT7-TOOLS]
>**Dictum:** *Three commands mirror MCP capabilities plus unified convenience.*

<br>

Query Context7 library documentation. Matches MCP tool structure (resolve-library-id, query-docs).

[IMPORTANT] Context7 pulls up-to-date, version-specific documentation from source. Supports private documents (early access). Community-driven library coverage.

---
## [1][COMMANDS]

| [CMD]   | [ARGS]                 | [RETURNS]                       |
| ------- | ---------------------- | ------------------------------- |
| resolve | `<library> [query]`    | Top 5 matching IDs with scores  |
| docs    | `<library-id> <query>` | Documentation filtered by query |
| lookup  | `<library> <query>`    | Resolve + docs in one call      |

---
## [2][USAGE]

```bash
# Resolve library -> see options
uv run .claude/skills/context7-tools/scripts/context7.py resolve effect

# Resolve with query filter
uv run .claude/skills/context7-tools/scripts/context7.py resolve react "server components"

# Fetch docs for specific ID
uv run .claude/skills/context7-tools/scripts/context7.py docs /effect-ts/effect "Services"

# Unified: resolve + docs
uv run .claude/skills/context7-tools/scripts/context7.py lookup react "hooks"

# Unified: with version-specific query
uv run .claude/skills/context7-tools/scripts/context7.py lookup vite "v7 migration guide"
```

---
## [3][ARGUMENTS]

**resolve**: `<library> [query]`
- `library` — Library name to search (required, e.g., `effect`, `react`, `vite`)
- `query` — Optional query to narrow results

**docs**: `<library-id> <query>`
- `library-id` — Context7 library ID (required, e.g., `/effect-ts/effect`)
- `query` — Documentation topic to retrieve (required)

**lookup**: `<library> <query>`
- `library` — Library name (required)
- `query` — Topic to fetch docs for (required)

---
## [4][SELECTION_LOGIC]

`lookup` auto-selects library by: VIP status -> highest benchmark score.

Use `resolve` first when disambiguation needed (e.g., multiple React packages).

---
## [5][OUTPUT]

Commands return JSON or plain text.

| [INDEX] | [CMD]     | [RESPONSE]                                            |
| :-----: | --------- | ----------------------------------------------------- |
|   [1]   | `resolve` | JSON array: `[{id, title, score, vip}]`               |
|   [2]   | `docs`    | Plain text documentation prefixed with `[library-id]` |
|   [3]   | `lookup`  | Plain text documentation (same as docs)               |

---
## [6][ENVIRONMENT]

| [VAR]              | [REQUIRED] | [DESCRIPTION]                  |
| ------------------ | ---------- | ------------------------------ |
| `CONTEXT7_API_KEY` | No         | Optional bearer token for auth |

---
## [7][ERROR_HANDLING]

- HTTP errors print `[ERROR] <status>: <body>` and exit 1
- Connection errors print `[ERROR] <message>` and exit 1
- No library found: `[ERROR] No library found for '<query>'` and exit 1
