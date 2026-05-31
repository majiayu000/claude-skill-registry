---
name: claude-tracker-suite
description: "Manage Claude Code sessions — search by topic or ID, browse recent sessions with full metadata (tags, summaries, titles, cost), resume in Ghostty tabs, spawn interactive or headless sessions, monitor live sessions, and bootstrap new setups. Triggers on resume session, find session, list sessions, recent sessions, spawn session, session history, what was I working on, open in ghostty."
argument-hint: [query or --id <prefix>]
allowed-tools: Bash(claude-tracker*), Bash(node ~/.claude/skills/claude-tracker-suite/scripts/*), Bash(~/.claude/skills/claude-tracker-suite/scripts/*.sh), Bash(python3 ~/.claude/scripts/*), Read, Grep, Glob, Edit, Write, Skill
---

# Claude Session Management Suite

Search, browse, monitor, and manage Claude Code session history across all projects.

## Tools Overview

| Tool | Purpose |
|------|---------|
| `claude-tracker-search` | Search sessions by keyword or ID prefix (standalone script) |
| `open-sessions.js` | List top N sessions, open selected in cmux tabs/splits |
| `claude-tracker-resume` | Find and resume crashed/inactive sessions |
| `claude-tracker-alive` | Check which sessions have running processes |
| `claude-tracker-watch` | Daemon: auto-summarize new sessions, update active-projects.md |
| `claude-tracker` | List recent sessions with status badges (standalone script) |
| `new-session.sh` | Start a new session in Ghostty/VSCode/Cursor, with optional prompt or headless mode |
| `resume-session.sh` | Open a session in a cmux tab (optionally open project in VS Code/Cursor) |
| `detect-projects.js` | Scan sessions to find all projects, check CLAUDE.md coverage |
| `bootstrap-claude-setup.js` | Generate complete ~/.claude/ config for new machine |
| `update-active-projects.py` | Regenerate active-projects.md with enriched session data |
| `checkpoint-session.js` | Create/query named bookmarks within sessions |
| `quote-session.js` | Capture/search notable phrases with FTS5 |
| `tag-session.js` | Manual session tagging with provenance |
| `claude-tracker-recent` | Show last N sessions with full metadata (title, tags, summary, cost, model) |

## Standalone Scripts

Commands delegate to standalone Node.js scripts (avoids shell escaping issues with inline `node -e`):

| Script | Called By | Purpose |
|--------|-----------|---------|
| `scripts/search-sessions.js` | `/claude-tracker-search` | Keyword search or `--id` prefix lookup across all sessions |
| `scripts/open-sessions.js` | Direct invocation | List top N sessions, open in cmux tabs/splits with confirmation |
| `scripts/list-sessions.js` | `/claude-tracker` | List recent sessions with status badges |
| `scripts/new-session.sh` | `/spawn` | Start new interactive or prompt-driven session in Ghostty/VSCode/Cursor or headless |
| `scripts/resume-session.sh` | Direct invocation | Open session in cmux tab, optionally open project in VS Code/Cursor |
| `scripts/detect-projects.js` | Direct invocation | Project discovery and CLAUDE.md scaffolding |
| `scripts/bootstrap-claude-setup.js` | Direct invocation | New machine setup generator |
| `scripts/checkpoint-session.js` | `/checkpoint`, `/checkpoint-list` | Create and query session checkpoints |
| `scripts/quote-session.js` | `/quote`, `/quote-search` | Capture and search tagged phrases via FTS5 |
| `scripts/tag-session.js` | `/tag` | Manual session tagging with provenance |
| `scripts/recent-sessions.js` | `/claude-tracker-recent` | Last N sessions with title, tags, summary, model, cost |
| `~/.claude/scripts/ghostty-resume.sh` | Direct invocation | Open session in a new Ghostty tab |

All scripts use `~/.claude/lib/tracker-utils.js` for shared utilities (path decoding, session parsing, git remote detection) and `~/.claude/lib/tracker-db.js` for SQLite access (better-sqlite3, WAL mode).

## Quick Start

```bash
# Search by topic
claude-tracker-search "kothar mac mini"

# Lookup by session ID prefix (exact directory from JSONL ground truth)
node ~/.claude/skills/claude-tracker-suite/scripts/search-sessions.js --id d7b8f4dd

# Search by session name/slug only (fast — no JSONL body scan)
claude-tracker-search "thera" --name

# List top 10 sessions, open selected in cmux tabs
node ~/.claude/skills/claude-tracker-suite/scripts/open-sessions.js

# Open top 5 as vertical splits
node ~/.claude/skills/claude-tracker-suite/scripts/open-sessions.js --limit 5 --split right

# Check what's alive
claude-tracker-alive

# Resume crashed sessions in tmux
claude-tracker-resume --tmux

# Start auto-summarize daemon
claude-tracker-watch --daemon
```

## Search

```bash
claude-tracker-search "$ARGUMENTS"
```

**Search targets** (weighted ranking): Summary (3x), First prompt (2x), Project name (1x), Git branch (1x).

| Flag | Description |
|------|-------------|
| `--limit <n>` | Max results (default: 20) |
| `--id <prefix>` | Lookup by session ID prefix (8+ chars) |
| `--project <name>` | Filter by project name (substring) |
| `--since <duration>` | Recent only: `7d`, `24h`, `30m`, `2w` |
| `--json` | Machine-readable JSON output |
| `--name` | Search only session names, slugs, summaries—skips JSONL body scan (fast) |
| `--fzf` | Interactive selection via fzf (outputs resume command) |

## Resume Crashed Sessions

```bash
claude-tracker-resume                    # List crashed sessions with resume commands
claude-tracker-resume --tmux             # Resume all in tmux windows
claude-tracker-resume --zsh              # Resume all in Terminal.app tabs (macOS)
claude-tracker-resume --all              # Include non-VS Code sessions
claude-tracker-resume --dry-run          # Preview without acting
```

Smart fallback: if `--resume` fails on an expired session, automatically starts a fresh session in that project directory. Sessions older than 7 days show a STALE badge.

## Alive Detection

Check which sessions have running Claude processes:

```bash
claude-tracker-alive                     # Running + stale sessions overview
claude-tracker-alive --running           # Only sessions with active processes
claude-tracker-alive --stale             # Only sessions with no process
claude-tracker-alive --json              # Machine-readable output
```

Cross-references running `claude` PIDs (via `pgrep` + `lsof`) against recent session files. Sessions >3 days without a process show an OLD badge.

## Auto-Summarize Daemon

Watch for new sessions and auto-populate summary cache:

```bash
claude-tracker-watch --status            # Check if daemon is running
claude-tracker-watch --daemon            # Start in background
claude-tracker-watch --stop              # Stop running daemon
claude-tracker-watch --verbose           # Foreground with debug output
```

The daemon watches `~/.claude/projects/*/sessions-index.json` for changes. When new sessions appear, it caches summaries from Claude Code metadata and regenerates `active-projects.md`. See `references/daemon-setup.md` for launchd plist and lifecycle details.

## Recent Sessions (Full Metadata)

```bash
claude-tracker-recent                          # Last 10 sessions with full metadata
claude-tracker-recent --limit 20               # Last 20 sessions
claude-tracker-recent --json                   # Machine-readable JSON output
claude-tracker-recent --project myapp          # Filter by project
claude-tracker-recent --model opus             # Filter by model
claude-tracker-recent --since 7d               # Last 7 days only
```

Shows per session: title (custom or auto), summary, all tags (color-coded by type), project name, age, model, cost, turn count, git branch, session ID, and resume command. First result's resume command is auto-copied to clipboard.

## Session Listing

```bash
claude-tracker                           # All recent sessions
claude-tracker vscode                    # VS Code sessions only
```

When speculator is running, the session listing includes:
- **Header**: Ghostty tab count and window count alongside running/inactive/VS Code counts
- **TTY badges**: Purple `s000`–`s010` badge per session showing which Ghostty tab it occupies

## Detect Projects

```bash
node ~/.claude/skills/claude-tracker-suite/scripts/detect-projects.js                # List all
node ~/.claude/skills/claude-tracker-suite/scripts/detect-projects.js --suggest      # Suggest additions
node ~/.claude/skills/claude-tracker-suite/scripts/detect-projects.js --scaffold     # Create CLAUDE.md stubs
node ~/.claude/skills/claude-tracker-suite/scripts/detect-projects.js --since 30d    # Recent only
```

## Update Active Projects

```bash
python3 ~/.claude/scripts/update-active-projects.py              # Regenerate active-projects.md
python3 ~/.claude/scripts/update-active-projects.py --summarize  # Show sessions needing summaries
```

The generated table includes Model, Turns, and Cost columns from enriched session data (extracted from JSONL transcripts). Git worktree sessions show a tree emoji badge. Sessions without summaries are auto-named via one-shot `claude --model haiku` call.

## Bootstrap New Setup

Generate a complete `~/.claude/` configuration for a new machine:

```bash
node ~/.claude/skills/claude-tracker-suite/scripts/bootstrap-claude-setup.js --user "Name" --dry-run
node ~/.claude/skills/claude-tracker-suite/scripts/bootstrap-claude-setup.js --user "Name"
```

Creates directory structure, global CLAUDE.md, userModel template, agent_docs stubs, and project CLAUDE.md scaffolds. Follow up with `/claude-md-manager` to enrich generated files.

## Resume in New Terminal

Open a session in a new cmux tab, optionally opening the project in an editor:

```bash
# Resume in cmux tab (default — auto-detects project directory)
~/.claude/skills/claude-tracker-suite/scripts/resume-session.sh <session-id>

# Resume in cmux + open project in VS Code
~/.claude/skills/claude-tracker-suite/scripts/resume-session.sh <session-id> --vscode

# Resume in cmux + open project in Cursor
~/.claude/skills/claude-tracker-suite/scripts/resume-session.sh <session-id> --cursor

# Explicit project directory
~/.claude/skills/claude-tracker-suite/scripts/resume-session.sh <session-id> --project ~/Desktop/Programming
```

cmux owns the terminal lifecycle. Editor flags (`--vscode`, `--cursor`) only open the project in the editor — the session always resumes in cmux. Falls back to printing the resume command if cmux is not running.

## Resume in Ghostty Tab

Open a session in a new Ghostty tab (auto-detects project directory from SQLite or JSONL):

```bash
~/.claude/scripts/ghostty-resume.sh <session-id>
~/.claude/scripts/ghostty-resume.sh <session-id> --project ~/my-project
```

Uses the AppleScript clipboard-paste pattern for reliable command delivery. Launches Ghostty if not running. Search and recent-sessions output includes a `Ghostty:` line per result with the ready-to-run command.

## New Session / Spawn

Start a new Claude Code session in a terminal tab or headless:

```bash
# Interactive session in Ghostty (default)
~/.claude/skills/claude-tracker-suite/scripts/new-session.sh ~/my-project

# With a specific model
~/.claude/skills/claude-tracker-suite/scripts/new-session.sh ~/my-project --model opus

# Prompt-driven session in Ghostty tab
~/.claude/skills/claude-tracker-suite/scripts/new-session.sh ~/my-project --prompt "fix the login bug"

# Prompt-driven in VS Code terminal
~/.claude/skills/claude-tracker-suite/scripts/new-session.sh ~/my-project --vscode --prompt "fix the login bug"

# Headless — runs in current terminal, returns JSON
~/.claude/skills/claude-tracker-suite/scripts/new-session.sh ~/my-project --headless --prompt "summarize the README"

# Headless with specific model and output format
~/.claude/skills/claude-tracker-suite/scripts/new-session.sh ~/my-project --headless --prompt "fix tests" --model haiku --output-format text
```

Headless and prompt-driven modes use `claude -p` (the Agent SDK CLI). Note: `-p` is now officially part of the Claude Agent SDK—it uses SDK billing, not interactive session billing. Terminal modes use the clipboard-paste AppleScript pattern for reliable command delivery (handles special characters in prompts).

## Workflow: Find and Resume

1. `claude-tracker-search "topic"` — find matching sessions
2. `claude-tracker-recent` — browse last 10 sessions with full metadata
3. `claude --resume <session-id>` — resume in current terminal
4. `~/.claude/scripts/ghostty-resume.sh <session-id>` — resume in a new Ghostty tab
5. `open-sessions.js` — list top sessions, open selected in cmux tabs
6. Or `claude-tracker-resume --tmux` — auto-resume all crashed sessions

## Workflow: Open Sessions in cmux

List recent sessions and open them in cmux tabs or splits:

```bash
# List top 10, prompt for selection
node ~/.claude/skills/claude-tracker-suite/scripts/open-sessions.js

# Open as vertical splits
node ~/.claude/skills/claude-tracker-suite/scripts/open-sessions.js --split right

# Open all without confirmation
node ~/.claude/skills/claude-tracker-suite/scripts/open-sessions.js --yes

# JSON output for scripting
node ~/.claude/skills/claude-tracker-suite/scripts/open-sessions.js --json
```

Session directories are resolved from JSONL ground truth (`decodeProjectPath`), not from `active-projects.md`. Falls back to printing resume commands when cmux is unavailable.

For the full cmux CLI reference, see `references/cmux-commands.md`.

## Workflow: Monitor Active Work

1. `claude-tracker-alive` — see what's running vs stale
2. `claude-tracker-watch --daemon` — keep summaries auto-updated
3. Read `~/.claude/agent_docs/active-projects.md` — curated project overview

## SQLite Database (`tracker.db`)

Single SQLite database at `~/.claude/tracker.db` consolidates all session metadata, git tracking, tags, and three new capabilities: checkpoints, phase tracking, and tagged phrases.

**API module**: `~/.claude/lib/tracker-db.js` — synchronous better-sqlite3, WAL mode, singleton lazy-open.

```bash
# Query directly
sqlite3 ~/.claude/tracker.db "SELECT COUNT(*) FROM sessions;"
sqlite3 ~/.claude/tracker.db "SELECT phase, COUNT(*) FROM phases GROUP BY phase;"
sqlite3 ~/.claude/tracker.db "SELECT phrase, GROUP_CONCAT(tag) FROM tagged_phrases tp LEFT JOIN tagged_phrase_tags tpt ON tpt.phrase_id = tp.id GROUP BY tp.id ORDER BY tp.timestamp DESC LIMIT 10;"
```

**Migration** (idempotent): `node ~/.claude/scripts/migrate-to-sqlite.js`

### Checkpoints

Named bookmarks within sessions capturing label, git state, workflow phase, and modified files.

```bash
# Manual checkpoint
node ~/.claude/skills/claude-tracker-suite/scripts/checkpoint-session.js create "finished auth module"
node ~/.claude/skills/claude-tracker-suite/scripts/checkpoint-session.js create "pre-deploy" --summary "about to push"

# List checkpoints
node ~/.claude/skills/claude-tracker-suite/scripts/checkpoint-session.js list
node ~/.claude/skills/claude-tracker-suite/scripts/checkpoint-session.js list --phase implementing
node ~/.claude/skills/claude-tracker-suite/scripts/checkpoint-session.js list --limit 10
```

Auto-checkpoints are created on git commits (`git-track-post.sh`) and phase transitions (`phase-detect.py`).

### Phase Tracking

Automatic workflow phase detection via PostToolUse hook (`phase-detect.py`). Rolling window of last 10 tool calls, hysteresis to prevent flickering.

Phases: `exploring`, `planning`, `implementing`, `testing`, `reviewing`, `debugging`, `committing`, `deploying`.

```bash
# Query current phase for a session
sqlite3 ~/.claude/tracker.db "SELECT phase, started_at FROM phases WHERE session_id = 'abc...' AND ended_at IS NULL;"

# Phase history
sqlite3 ~/.claude/tracker.db "SELECT phase, started_at, ended_at, duration_ms FROM phases WHERE session_id = 'abc...' ORDER BY started_at;"

# Phase analytics
sqlite3 ~/.claude/tracker.db "SELECT phase, COUNT(*) as transitions, AVG(duration_ms)/1000 as avg_seconds FROM phases GROUP BY phase;"
```

### Tagged Phrases

Notable excerpts captured from sessions with tags, searchable via FTS5.

```bash
# Capture a phrase
node ~/.claude/skills/claude-tracker-suite/scripts/quote-session.js capture "assumptions are the enemy" --tags principle,design

# Search phrases (FTS5)
node ~/.claude/skills/claude-tracker-suite/scripts/quote-session.js search "assumptions"

# List by tag
node ~/.claude/skills/claude-tracker-suite/scripts/quote-session.js tag principle

# List recent phrases
node ~/.claude/skills/claude-tracker-suite/scripts/quote-session.js list --limit 20
```

Phrases are also auto-extracted by the `session-tags-infer.py` Stop hook during LLM inference.

## Related Systems

- **Git Tracking** — PreToolUse/PostToolUse hooks intercept git commands, tag sessions with repos they touch. Query via `tracker-utils.js` functions (`getSessionsForRepo`, `getReposForSession`, `getRecentCommits`). See `references/data-schemas.md` for hook files and index format.
- **Speculator** — Daemon at `~/.claude/scripts/speculator/` maps Ghostty tabs to sessions every 5 minutes. `list-sessions.js` uses `loadSpeculatorData()` and `getSessionTTY()` for TTY badges. Health check: `bash ~/.claude/scripts/speculator/status.sh`
- **Soul Registry** — Live session tracking with heartbeats and Slack bindings at `~/.claude/soul-sessions/registry.json`. View: `python3 ~/.claude/hooks/soul-registry.py list --md`. Activate: `/ensoul`. Bind to Slack: `/slack-sync #channel`.
- **Session Report** — `/session-report` generates a Markdown dashboard combining session status with git activity.

## References

For detailed schemas and infrastructure:

- `references/data-schemas.md` — Session index, summary cache, and JSONL transcript schemas; data source locations; shared library API
- `references/daemon-setup.md` — Watcher daemon lifecycle and launchd plist template
- `references/cmux-commands.md` — Complete cmux CLI reference: hierarchy, splits, tabs, input, browser, sidebar, notifications, keyboard shortcuts
