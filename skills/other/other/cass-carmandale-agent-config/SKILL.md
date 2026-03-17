---
name: cass
description: "Coding Agent Session Search - unified CLI/TUI to index and search local coding agent history from Claude Code, Codex, Gemini, Cursor, Aider, ChatGPT, Pi-Agent, Factory, and more. Purpose-built for AI agent consumption with robot mode."
---

# CASS - Coding Agent Session Search

Unified, high-performance CLI/TUI to index and search your local coding agent history. Aggregates sessions from **11 agents**: Codex, Claude Code, Gemini CLI, Cline, OpenCode, Amp, Cursor, ChatGPT, Aider, Pi-Agent, and Factory (Droid).

## CRITICAL: Robot Mode Required for AI Agents

**NEVER run bare `cass`** - it launches an interactive TUI that blocks your session!

```bash
# WRONG - blocks terminal
cass

# CORRECT - JSON output for agents
cass search "query" --robot
cass search "query" --json  # alias
```

**Always use `--robot` or `--json` flags for machine-readable output.**

---

## Quick Reference for AI Agents

### Pre-Flight Check

```bash
# Health check (exit 0=healthy, 1=unhealthy, <50ms)
cass health

# If unhealthy, rebuild index
cass index --full
```

### Essential Commands

```bash
# Search with JSON output
cass search "authentication error" --robot --limit 5

# Search with metadata (elapsed_ms, cache stats, freshness)
cass search "error" --robot --robot-meta

# Minimal payload (path, line, agent only)
cass search "bug" --robot --fields minimal

# View source at specific line
cass view /path/to/session.jsonl -n 42 --json

# Expand context around a line
cass expand /path/to/session.jsonl -n 42 -C 5 --json

# Capabilities discovery
cass capabilities --json

# Full API schema
cass introspect --json

# LLM-optimized documentation
cass robot-docs guide
cass robot-docs commands
cass robot-docs schemas
cass robot-docs examples
cass robot-docs exit-codes
```

---

## Why Use CASS

### Cross-Agent Knowledge Transfer

Your coding agents create scattered knowledge:
- Claude Code sessions in `~/.claude/projects`
- Codex sessions in `~/.codex/sessions`
- Cursor state in SQLite databases
- Aider history in markdown files

CASS **unifies all of this** into a single searchable index. When you're stuck on a problem, search across ALL your past agent sessions to find relevant solutions.

### Use Cases

```bash
# "I solved this before..."
cass search "TypeError: Cannot read property" --robot --days 30

# Cross-agent learning (what has ANY agent said about X?)
cass search "authentication" --robot --workspace /path/to/project

# Agent-to-agent handoff
cass search "database migration" --robot --fields summary

# Daily review
cass timeline --today --json
```

---

## Command Reference

### Indexing

```bash
# Full rebuild of DB and search index
cass index --full

# Incremental update (since last scan)
cass index

# Watch mode: auto-reindex on file changes
cass index --watch

# Force rebuild even if schema unchanged
cass index --full --force-rebuild

# Safe retries with idempotency key
cass index --full --idempotency-key "build-$(date +%Y%m%d)"

# JSON output with stats
cass index --full --json
```

### Search

```bash
# Basic search (JSON output required for agents!)
cass search "query" --robot

# With filters
cass search "error" --robot --agent claude --days 7
cass search "bug" --robot --workspace /path/to/project
cass search "panic" --robot --today

# Time filters
cass search "auth" --robot --since 2024-01-01 --until 2024-01-31
cass search "test" --robot --yesterday
cass search "fix" --robot --week

# Wildcards
cass search "auth*" --robot          # prefix: authentication, authorize
cass search "*tion" --robot          # suffix: authentication, exception
cass search "*config*" --robot       # substring: misconfigured

# Token budget management (critical for LLMs!)
cass search "error" --robot --fields minimal              # path, line, agent only
cass search "error" --robot --fields summary              # adds title, score
cass search "error" --robot --max-content-length 500      # truncate fields
cass search "error" --robot --max-tokens 2000             # soft budget (~4 chars/token)
cass search "error" --robot --limit 5                     # cap results

# Pagination (cursor-based)
cass search "TODO" --robot --robot-meta --limit 20
# Use _meta.next_cursor from response:
cass search "TODO" --robot --robot-meta --limit 20 --cursor "eyJ..."

# Match highlighting
cass search "authentication error" --robot --highlight

# Query analysis/debugging
cass search "auth*" --robot --explain    # parsed query, cost estimates
cass search "auth error" --robot --dry-run  # validate without executing

# Aggregations
cass search "error" --robot --aggregate agent,workspace,date

# Request correlation
cass search "bug" --robot --request-id "req-12345"

# Source filtering (for multi-machine setups)
cass search "auth" --robot --source laptop
cass search "error" --robot --source remote
```

### Session Analysis

```bash
# Export conversation to markdown/HTML/JSON
cass export /path/to/session.jsonl --format markdown -o conversation.md
cass export /path/to/session.jsonl --format html -o conversation.html
cass export /path/to/session.jsonl --format json --include-tools

# Expand context around a line (from search result)
cass expand /path/to/session.jsonl -n 42 -C 5 --json
# Shows 5 messages before and after line 42

# View source at line
cass view /path/to/session.jsonl -n 42 --json

# Activity timeline
cass timeline --today --json --group-by hour
cass timeline --days 7 --json --agent claude
cass timeline --since 7d --json

# Find related sessions for a file
cass context /path/to/source.ts --json
```

### Status & Diagnostics

```bash
# Quick health (<50ms)
cass health
cass health --json

# Full status snapshot
cass status --json
cass state --json  # alias

# Statistics
cass stats --json
cass stats --by-source  # for multi-machine

# Full diagnostics
cass diag --verbose
```

### Remote Sources (Multi-Machine Search)

Search across sessions from multiple machines via SSH/rsync:

```bash
# Add a remote machine
cass sources add user@laptop.local --preset macos-defaults
cass sources add dev@workstation --path ~/.claude/projects --path ~/.codex/sessions

# List sources
cass sources list --json

# Sync sessions
cass sources sync
cass sources sync --source laptop --verbose

# Check connectivity
cass sources doctor
cass sources doctor --source laptop --json

# Path mappings (rewrite remote paths to local)
cass sources mappings list laptop
cass sources mappings add laptop --from /home/user/projects --to /Users/me/projects
cass sources mappings test laptop /home/user/projects/myapp/src/main.rs

# Remove source
cass sources remove laptop --purge -y
```

Configuration stored in `~/.config/cass/sources.toml` (Linux) or `~/Library/Application Support/cass/sources.toml` (macOS).

### Shell Completions

```bash
cass completions bash > ~/.local/share/bash-completion/completions/cass
cass completions zsh > "${fpath[1]}/_cass"
cass completions fish > ~/.config/fish/completions/cass.fish
cass completions powershell >> $PROFILE
```

---

## Robot Mode Deep Dive

### Self-Documenting API

CASS teaches agents how to use itself:

```bash
# Quick capability check
cass capabilities --json
# Returns: features, connectors, limits

# Full API schema
cass introspect --json
# Returns: all commands, arguments, response shapes

# Topic-based docs (LLM-optimized)
cass robot-docs commands   # all commands and flags
cass robot-docs schemas    # response JSON schemas
cass robot-docs examples   # copy-paste invocations
cass robot-docs exit-codes # error handling
cass robot-docs guide      # quick-start walkthrough
```

### Forgiving Syntax (Agent-Friendly)

CASS auto-corrects common mistakes:

| What you type | What CASS understands |
|---------------|----------------------|
| `cass serach "error"` | `cass search "error"` (typo corrected) |
| `cass -robot -limit=5` | `cass --robot --limit=5` (single-dash fixed) |
| `cass --Robot --LIMIT 5` | `cass --robot --limit 5` (case normalized) |
| `cass find "auth"` | `cass search "auth"` (alias resolved) |
| `cass --limt 5` | `cass --limit 5` (Levenshtein <=2) |

**Command Aliases:**
- `find`, `query`, `q`, `lookup`, `grep` -> `search`
- `ls`, `list`, `info`, `summary` -> `stats`
- `st`, `state` -> `status`
- `reindex`, `idx`, `rebuild` -> `index`
- `show`, `get`, `read` -> `view`
- `docs`, `help-robot`, `robotdocs` -> `robot-docs`

### Output Formats

```bash
# Pretty-printed JSON (default)
cass search "error" --robot

# Streaming JSONL (header + one hit per line)
cass search "error" --robot-format jsonl

# Compact single-line JSON
cass search "error" --robot-format compact

# With performance metadata
cass search "error" --robot --robot-meta
```

**Design principle:** stdout = JSON only; diagnostics go to stderr.

### Token Budget Management

LLMs have context limits. Control output size:

| Flag | Effect |
|------|--------|
| `--fields minimal` | Only `source_path`, `line_number`, `agent` |
| `--fields summary` | Adds `title`, `score` |
| `--fields score,title,snippet` | Custom field selection |
| `--max-content-length 500` | Truncate long fields (UTF-8 safe) |
| `--max-tokens 2000` | Soft budget (~4 chars/token) |
| `--limit 5` | Cap number of results |

Truncated fields include `*_truncated: true` indicator.

### Structured Error Handling

Errors are JSON with actionable hints:

```json
{
  "error": {
    "code": 3,
    "kind": "index_missing",
    "message": "Search index not found",
    "hint": "Run 'cass index --full' to build the index",
    "retryable": false
  }
}
```

### Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Parse stdout |
| 1 | Health check failed | Run `cass index --full` |
| 2 | Usage error | Fix syntax (hint provided) |
| 3 | Index/DB missing | Run `cass index --full` |
| 4 | Network error | Check connectivity |
| 5 | Data corruption | Run `cass index --full --force-rebuild` |
| 6 | Incompatible version | Update cass |
| 7 | Lock/busy | Retry later |
| 8 | Partial result | Increase `--timeout` |
| 9 | Unknown error | Check `retryable` flag |

### Response Shapes

**Search Response:**
```json
{
  "query": "error",
  "limit": 10,
  "offset": 0,
  "count": 5,
  "total_matches": 42,
  "hits": [
    {
      "source_path": "/path/to/session.jsonl",
      "line_number": 123,
      "agent": "claude_code",
      "workspace": "/projects/myapp",
      "title": "Authentication debugging",
      "snippet": "The error occurs when...",
      "score": 0.85,
      "match_type": "exact",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "_meta": {
    "elapsed_ms": 12,
    "cache_hit": true,
    "wildcard_fallback": false,
    "next_cursor": "eyJ...",
    "index_freshness": { "stale": false, "age_seconds": 120 }
  }
}
```

**Status Response:**
```json
{
  "healthy": true,
  "recommended_action": null,
  "index": { "exists": true, "fresh": true, "age_seconds": 120 },
  "database": { "conversations": 500, "messages": 10000 },
  "pending": { "sessions": 0, "watch_active": true }
}
```

---

## Query Language

### Basic Queries

| Query | Matches |
|-------|---------|
| `error` | Messages containing "error" (case-insensitive) |
| `python error` | Both "python" AND "error" |
| `"authentication failed"` | Exact phrase |

### Wildcard Patterns

| Pattern | Type | Performance |
|---------|------|-------------|
| `auth*` | Prefix | Fast (edge n-grams) |
| `*tion` | Suffix | Slower (regex) |
| `*config*` | Substring | Slowest (regex) |

### Match Types

Results include `match_type`:

| Type | Meaning | Score Boost |
|------|---------|-------------|
| `exact` | Verbatim match | Highest |
| `prefix` | Via prefix expansion | High |
| `suffix` | Via suffix pattern | Medium |
| `substring` | Via substring pattern | Lower |
| `fuzzy` | Auto-fallback (sparse results) | Lowest |

### Auto-Fuzzy Fallback

When exact query returns <3 results, CASS automatically retries with wildcards:
- `auth` -> `*auth*`
- Results flagged with `wildcard_fallback: true`

---

## Supported Agents (11 Connectors)

| Agent | Location | Format |
|-------|----------|--------|
| **Claude Code** | `~/.claude/projects` | JSONL |
| **Codex** | `~/.codex/sessions` | JSONL (Rollout) |
| **Gemini CLI** | `~/.gemini/tmp` | JSON |
| **Cline** | VS Code global storage | Task directories |
| **OpenCode** | `.opencode` directories | SQLite |
| **Amp** | `~/.local/share/amp` + VS Code | Mixed |
| **Cursor** | `~/Library/Application Support/Cursor` | SQLite (state.vscdb) |
| **ChatGPT** | `~/Library/Application Support/com.openai.chat` | JSON (v1 unencrypted) |
| **Aider** | `~/.aider.chat.history.md` + per-project | Markdown |
| **Pi-Agent** | `~/.pi/agent/sessions` | JSONL with thinking |
| **Factory (Droid)** | `~/.factory/sessions` | JSONL by workspace |

**Note:** ChatGPT v2/v3 are AES-256-GCM encrypted (keychain access required). Legacy v1 unencrypted conversations are indexed automatically.

---

## TUI Features (for Humans)

Launch with `cass` (no flags):

### Keyboard Shortcuts

**Navigation:**
- `Up/Down`: Move selection
- `Left/Right`: Switch panes
- `Tab/Shift+Tab`: Cycle focus
- `Enter`: Open in `$EDITOR`
- `Space`: Full-screen detail view

**Filtering:**
- `F3`: Agent filter
- `F4`: Workspace filter
- `F5/F6`: Time filters
- `Shift+F5`: Cycle presets (24h/7d/30d/all)
- `Ctrl+Del`: Clear all filters

**Modes:**
- `F2`: Toggle dark/light theme
- `F7`: Context window size (S/M/L/XL)
- `F9`: Match mode (prefix/standard)
- `F12`: Ranking mode (recent/balanced/relevance/quality/newest/oldest)
- `Ctrl+B`: Toggle border style

**Actions:**
- `m`: Toggle selection
- `Ctrl+A`: Select all
- `Ctrl+Enter`: Add to queue
- `Ctrl+O`: Open all queued
- `y`: Copy path/content
- `/`: Find in detail pane
- `n/N`: Next/prev match
- `Ctrl+P`: Command palette
- `1-9`: Load saved view
- `Shift+1-9`: Save view to slot

**Source Filtering (multi-machine):**
- `F11`: Cycle source filter (all/local/remote)
- `Shift+F11`: Source selection menu

---

## Ranking Modes

Cycle with `F12` in TUI or use `--ranking` flag:

| Mode | Formula | Best For |
|------|---------|----------|
| **Recent Heavy** | `relevance*0.3 + recency*0.7` | "What was I working on?" |
| **Balanced** | `relevance*0.5 + recency*0.5` | General search |
| **Relevance** | `relevance*0.8 + recency*0.2` | "Best explanation of X" |
| **Match Quality** | Penalizes fuzzy matches | Precise technical searches |
| **Date Newest** | Pure chronological | Recent activity |
| **Date Oldest** | Reverse chronological | "When did I first..." |

---

## Optional Semantic Search

Local-only semantic search using MiniLM (no cloud):

**Required files** (place in data directory):
- `model.onnx`
- `tokenizer.json`
- `config.json`
- `special_tokens_map.json`
- `tokenizer_config.json`

Vector index stored as `vector_index/index-minilm-384.cvvi`.

CASS does NOT auto-download models; you must manually install them.

---

## Bookmarks

Save important results for later:

```bash
# Bookmarks stored in SQLite: ~/.local/share/coding-agent-search/bookmarks.db
```

In TUI: Press `b` to bookmark, add notes and tags.

Bookmark structure:
- `title`: Short description
- `source_path`, `line_number`, `agent`, `workspace`
- `note`: Your annotations
- `tags`: Comma-separated labels
- `snippet`: Extracted content

---

## Watch Mode

Real-time index updates:

```bash
cass index --watch
```

- **Debounce:** 2 seconds (wait for burst to settle)
- **Max wait:** 5 seconds (force flush during continuous activity)
- **Incremental:** Only re-scans modified files

TUI automatically starts watch mode in background.

---

## Performance Characteristics

| Operation | Latency |
|-----------|---------|
| Prefix search (cached) | 2-8ms |
| Prefix search (cold) | 40-60ms |
| Substring search | 80-200ms |
| Full reindex | 5-30s |
| Incremental reindex | 50-500ms |
| Health check | <50ms |

**Memory:** 70-140MB typical (50K messages)
**Disk:** ~600 bytes/message (including n-gram overhead)

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `CASS_DATA_DIR` | Override data directory |
| `CHATGPT_ENCRYPTION_KEY` | Base64 key for encrypted ChatGPT |
| `PI_CODING_AGENT_DIR` | Override Pi-Agent sessions path |
| `CASS_CACHE_SHARD_CAP` | Per-shard cache entries (default 256) |
| `CASS_CACHE_TOTAL_CAP` | Total cached hits (default 2048) |
| `CASS_DEBUG_CACHE_METRICS` | Enable cache debug logging |
| `CODING_AGENT_SEARCH_NO_UPDATE_PROMPT` | Skip update checks |

---

## Integration with CASS Memory (cm)

CASS provides **episodic memory** (raw sessions). CM extracts **procedural memory** (rules and playbooks):

```bash
# 1. CASS indexes raw sessions
cass index --full

# 2. Search for relevant past experience
cass search "authentication timeout" --robot --limit 10

# 3. CM reflects on sessions to extract rules
cm reflect
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "missing index" | `cass index --full` |
| Stale warning | Rerun index or enable watch |
| Empty results | Check `cass stats --json`, verify connectors detected |
| JSON parsing errors | Use `--robot-format compact` |
| Watch not triggering | Check `watch_state.json`, verify file event support |
| Reset TUI state | `cass tui --reset-state` or `Ctrl+Shift+Del` |

---

## Ready-to-Paste AGENTS.md Blurb

```
## cass - Coding Agent Session Search

Search all your agent histories (Claude, Codex, Cursor, Gemini, Aider, etc.) from a unified index.

**NEVER run bare `cass`** - it launches an interactive TUI. Always use `--robot` or `--json`.

### Quick Start
cass health                                    # Pre-flight check
cass search "auth error" --robot --limit 5     # Search
cass view /path/session.jsonl -n 42 --json     # View result
cass expand /path/session.jsonl -n 42 -C 3 --json  # Context

### Key Flags
| Flag | Purpose |
|------|---------|
| --robot / --json | Machine-readable output (required!) |
| --fields minimal | Reduce payload size |
| --limit N | Cap results |
| --agent NAME | Filter by agent |
| --days N | Recent N days |

stdout = JSON only, stderr = diagnostics. Exit 0 = success.
```

---

## Installation

```bash
# One-liner install
curl -fsSL https://raw.githubusercontent.com/Dicklesworthstone/coding_agent_session_search/main/install.sh \
  | bash -s -- --easy-mode --verify

# Windows
irm https://raw.githubusercontent.com/Dicklesworthstone/coding_agent_session_search/main/install.ps1 | iex
```
