---
name: claude-tracker-suite
description: "Claude Code session management suite: search sessions by topic/ID, resume crashed sessions, spawn new sessions (interactive or headless), monitor live sessions, detect projects, auto-summarize new sessions, and bootstrap new setups. This skill should be used when searching past sessions, checking running sessions, resuming work, spawning new sessions, or bootstrapping a new machine."
argument-hint: [query or --id <prefix>]
allowed-tools: Bash(claude-tracker*), Bash(node ~/.claude/skills/claude-tracker-suite/scripts/*), Bash(~/.claude/skills/claude-tracker-suite/scripts/*.sh), Bash(python3 ~/.claude/scripts/*), Read, Grep, Glob, Edit, Write, Skill
---

# Claude Session Management Suite

Search, browse, monitor, and manage Claude Code session history across all projects.

## Tools Overview

| Tool | Purpose |
|------|---------|
| `claude-tracker-search` | Search sessions by keyword (standalone script) |
| `claude-tracker-resume` | Find and resume crashed/inactive sessions |
| `claude-tracker-alive` | Check which sessions have running processes |
| `claude-tracker-watch` | Daemon: auto-summarize new sessions, update active-projects.md |
| `claude-tracker` | List recent sessions with status badges (standalone script) |
| `new-session.sh` | Start a new session in Ghostty/VSCode/Cursor, with optional prompt or headless mode |
| `resume-in-vscode.sh` | Open a session in a new VS Code (or Cursor) terminal via AppleScript |
| `detect-projects.js` | Scan sessions to find all projects, check CLAUDE.md coverage |
| `bootstrap-claude-setup.js` | Generate complete ~/.claude/ config for new machine |
| `update-active-projects.py` | Regenerate active-projects.md with enriched session data |

## Standalone Scripts

Commands delegate to standalone Node.js scripts (avoids shell escaping issues with inline `node -e`):

| Script | Called By | Purpose |
|--------|-----------|---------|
| `scripts/search-sessions.js` | `/claude-tracker-search` | Keyword search across all sessions (8K lines/file, noise-filtered) |
| `scripts/list-sessions.js` | `/claude-tracker` | List recent sessions with status badges |
| `scripts/new-session.sh` | `/spawn` | Start new interactive or prompt-driven session in Ghostty/VSCode/Cursor or headless |
| `scripts/resume-in-vscode.sh` | Direct invocation | Open session in new VS Code/Cursor terminal (macOS AppleScript) |
| `scripts/detect-projects.js` | Direct invocation | Project discovery and CLAUDE.md scaffolding |
| `scripts/bootstrap-claude-setup.js` | Direct invocation | New machine setup generator |

All scripts use `~/.claude/lib/tracker-utils.js` for shared utilities (path decoding, session parsing, git remote detection).

## Quick Start

```bash
# Search by topic
claude-tracker-search "kothar mac mini"

# Interactive search with fzf
claude-tracker-search "kothar" --fzf

# Search by session ID prefix
claude-tracker-search --id 1da2b718

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

## Session Listing

```bash
claude-tracker                           # All recent sessions
claude-tracker vscode                    # VS Code sessions only
```

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

Open a session in a new Ghostty tab, VS Code terminal, or Cursor terminal (macOS AppleScript):

```bash
# Resume session in Ghostty (default)
~/.claude/skills/claude-tracker-suite/scripts/resume-in-vscode.sh <session-id>

# Resume in VS Code terminal
~/.claude/skills/claude-tracker-suite/scripts/resume-in-vscode.sh <session-id> --vscode

# Resume in Cursor terminal
~/.claude/skills/claude-tracker-suite/scripts/resume-in-vscode.sh <session-id> --cursor

# cd to a project first, then resume
~/.claude/skills/claude-tracker-suite/scripts/resume-in-vscode.sh <session-id> --project ~/Desktop/Programming
```

System aliases: `code` → Cursor, `vscode` → VS Code. Ghostty is the default target.

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
2. `claude --resume <session-id>` — resume in current terminal
3. `resume-in-vscode.sh <session-id>` — resume in new VS Code terminal
4. Or `claude-tracker-resume --tmux` — auto-resume all crashed sessions

## Workflow: Monitor Active Work

1. `claude-tracker-alive` — see what's running vs stale
2. `claude-tracker-watch --daemon` — keep summaries auto-updated
3. Read `~/.claude/agent_docs/active-projects.md` — curated project overview

## Related: Git Tracking

Git-aware session tracking via PreToolUse/PostToolUse hooks intercepts all git commands and tags sessions with repos they touch. Enables cross-directory session discovery.

| File | Purpose |
|------|---------|
| `~/.claude/hooks/git-track.sh` | PreToolUse hook — logs git commands to JSONL |
| `~/.claude/hooks/git-track-post.sh` | PostToolUse hook — captures commit hashes |
| `~/.claude/hooks/git-track-rebuild.py` | Builds bidirectional index at SessionEnd |
| `~/.claude/git-tracking.jsonl` | Append-only event log (hot path) |
| `~/.claude/git-tracking-index.json` | Bidirectional session <-> repo index |

Query functions in `tracker-utils.js`:
- `loadGitTracking()` — load the index
- `getSessionsForRepo(path)` — find sessions that touched a repo
- `getReposForSession(sid)` — find repos a session touched
- `getRecentCommits({hours, repoPath})` — recent commits across sessions
- `getRecentGitEvents({hours})` — raw event timeline

The `/session-report` command generates a Markdown dashboard combining session status with git activity.

## Related: Soul Registry

The soul registry (`~/.claude/hooks/soul-registry.py`) tracks **live** sessions with heartbeats, topics, and Slack channel bindings. It complements the tracker suite:

| | Tracker Suite | Soul Registry |
|--|---------------|---------------|
| **Scope** | All sessions, all time | Active sessions only |
| **Data source** | JSONL transcripts, sessions-index.json | `~/.claude/soul-sessions/registry.json` |
| **Updates** | After session ends (summaries) | Real-time (heartbeat every turn) |
| **Purpose** | Search, resume, project detection | Cross-session awareness, Slack binding |

To view the live registry: `python3 ~/.claude/hooks/soul-registry.py list --md`

To activate Claudicle identity in a session: `/ensoul` (opt-in per session). To bind a session to Slack: `/slack-sync #channel`.

## References

For detailed schemas and infrastructure:

- `references/data-schemas.md` — Session index, summary cache, and JSONL transcript schemas; data source locations; shared library API
- `references/daemon-setup.md` — Watcher daemon lifecycle and launchd plist template
