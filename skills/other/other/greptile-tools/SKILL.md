---
name: greptile-tools
type: complex
depth: base
user-invocable: false
description: >-
  Executes natural language codebase queries against indexed repositories via Greptile API. Use when investigating code architecture, locating implementations, understanding feature workflows, or searching cross-repository patterns requiring semantic code graph traversal.
---

# [H1][GREPTILE-TOOLS]
>**Dictum:** *Codebase context enables precise answers.*

<br>

Query indexed repositories via Greptile API v2. Defaults to current repo.

[IMPORTANT] Repository must be indexed before querying. Check `status` first. Supports natural language queries against a comprehensive code graph with file/function/class references.

---
## [1][COMMANDS]

| [CMD]  | [ARGS]                | [PURPOSE]                           |
| ------ | --------------------- | ----------------------------------- |
| index  | --                    | Trigger repository indexing         |
| status | --                    | Check indexing progress/completion  |
| query  | `<question> [genius]` | Natural language codebase Q&A       |
| search | `<question>`          | Code search (files only, no answer) |

---
## [2][USAGE]

```bash
# Check indexing status (run first)
uv run .claude/skills/greptile-tools/scripts/greptile.py status

# Trigger repository indexing
uv run .claude/skills/greptile-tools/scripts/greptile.py index

# Natural language query
uv run .claude/skills/greptile-tools/scripts/greptile.py query "How does authentication work?"

# Deep analysis with genius mode
uv run .claude/skills/greptile-tools/scripts/greptile.py query "Explain Effect pipeline patterns" genius

# Code search (files/functions only, no generated answer)
uv run .claude/skills/greptile-tools/scripts/greptile.py search "rate limiting implementation"
```

---
## [3][ARGUMENTS]

**index**: (no arguments)
- Triggers indexing on default repo (bsamiee/Parametric_Portal)
- Set `reload=True` to force re-index

**status**: (no arguments)
- Returns indexing status, files processed count, SHA, readiness

**query**: `<question> [genius]`
- `question` — Natural language query (required)
- `genius` — Pass literal `genius` for deep analysis mode (slower, more thorough)
- Returns: answer text + source file references with line ranges

**search**: `<question>`
- `question` — Natural language code search (required)
- Returns: matching files/functions/classes (no generated answer)

---
## [4][OUTPUT]

Commands return: `{"status": "success|error", ...}`.

| [INDEX] | [CMD]    | [RESPONSE]                                   |
| :-----: | -------- | -------------------------------------------- |
|   [1]   | `index`  | `{repo, message}`                            |
|   [2]   | `status` | `{repo, indexing, sha, progress, ready}`     |
|   [3]   | `query`  | `{query, answer, sources: [{file, lines}]}`  |
|   [4]   | `search` | `{query, results: [{file, lines, summary}]}` |

Error responses include `retryable: bool` for transient failures (5xx, 429).

---
## [5][ENVIRONMENT]

| [VAR]            | [REQUIRED] | [DESCRIPTION]                                |
| ---------------- | ---------- | -------------------------------------------- |
| `GREPTILE_TOKEN` | Yes        | Greptile API bearer token                    |
| `GITHUB_TOKEN`   | Yes        | GitHub token for repo access (or `GH_TOKEN`) |

---
## [6][ERROR_HANDLING]

- HTTP errors print `[ERROR] <status>: <body>` and exit 1
- Missing token: `[ERROR] GREPTILE_TOKEN environment variable not set` and exit 1
- Repository not indexed: `[ERROR] Repository not indexed`; run `index` command first
- Rate limit (429): retry after `Retry-After` header value
- `query` returns `retryable: bool` for transient failures (5xx, 429)
