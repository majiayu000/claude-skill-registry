---
name: Sessions
description: "Claude Code session search, resume, and index repair. USE WHEN find session, search sessions, resume old session, fix session index, repair sessions, session history, broken resume."
---

# Sessions

Search, browse, and resume Claude Code sessions. Repair the sessions-index.json when the built-in `/resume` picker is broken.

## Workflow Routing

| Workflow | Trigger | Section |
|----------|---------|---------|
| **Search** | "find session", "search sessions", "session about X" | [Search](#search) |
| **Repair** | "fix session index", "repair sessions", "resume is broken" | [Repair Index](#repair-index) |
| **Browse** | "list sessions", "recent sessions", "session history" | [Browse](#browse) |

## Tools

| Tool | Location | Purpose |
|------|----------|---------|
| `recall` | `/opt/homebrew/bin/recall` | Full-text TUI search across .jsonl session files |
| `repair-sessions-index.py` | `Hooks/repair-sessions-index.py` | Rebuild sessions-index.json from .jsonl metadata |

### Prerequisites

```bash
# recall — install if missing
brew install zippoxer/tap/recall

# repair script — ships with the repo
python3 Hooks/repair-sessions-index.py --help
```

## Search

Use `recall` to find sessions by content. This bypasses sessions-index.json entirely — searches .jsonl files directly.

### Interactive (TUI)

Tell the user to run `recall` directly in their terminal — the TUI requires direct terminal access:

```
recall                    # open TUI, type to search, Enter to resume
recall "forge-tlp"        # TUI with initial query
```

### Programmatic (from within a session)

```bash
recall search "forge-tlp"              # JSON — matching sessions
recall read <session-id>               # JSON — full conversation transcript
```

### Intent-to-command mapping

| User says | Command |
|-----------|---------|
| "find the session where we worked on X" | `recall search "X"` |
| "what sessions mention forge-tlp" | `recall search "forge-tlp"` |
| "read session abc123" | `recall read abc123` |

## Repair Index

Rebuilds sessions-index.json by reading actual .jsonl transcript files. Fixes:
- Missing sessions (not in index)
- Stale metadata (`firstPrompt: "No prompt"`, empty summaries)
- Deleted index file (creates from scratch)

### Usage

```bash
# All projects
python3 Hooks/repair-sessions-index.py

# Specific project
python3 Hooks/repair-sessions-index.py ~/.claude/projects/-Users-N4M3Z-Data
```

### When to run

- `claude --resume` shows blank/unnamed sessions
- sessions-index.json is missing or corrupt
- After Claude Code updates that break session indexing
- Upstream bug: [anthropics/claude-code#25032](https://github.com/anthropics/claude-code/issues/25032)

### What it does

1. Scans all .jsonl files in the project directory
2. Extracts firstPrompt, messageCount, created/modified timestamps from each transcript
3. Adds missing sessions to the index
4. Updates existing entries that have stale `firstPrompt: "No prompt"`
5. Backs up existing index before writing

## Browse

### Recent sessions (JSON)

```bash
recall list                             # recent sessions across all projects
```

### Resume by keyword (bypasses picker)

```bash
claude --resume "some words from the session"
```

### Resume by ID

```bash
# List session files for this project
ls ~/.claude/projects/-Users-N4M3Z-Data/*.jsonl | head -20

# Resume specific session
claude --resume <session-uuid>
```

### Reindex recall's own index

```bash
recall --reindex                        # clear and rebuild recall's search index
```

## Constraints

- `recall` TUI requires direct terminal access — cannot be run inside a Claude Code session via Bash tool
- `recall search` and `recall list` work programmatically (JSON output)
- The repair script only fixes metadata in sessions-index.json — it cannot recover deleted .jsonl files
- Sessions-index.json is architecturally vestigial since Claude Code v2.1.31 — the built-in picker may ignore it in future versions
- The repair script is a workaround, not a permanent fix — upstream resolution tracked in [#25032](https://github.com/anthropics/claude-code/issues/25032)
