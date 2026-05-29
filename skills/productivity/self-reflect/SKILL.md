---
name: self-reflect
description: "Track personal productivity across GitHub and coding agents. Generates a web dashboard with contribution metrics, repo creation trends, and agent session history. Use when the user wants to analyze their coding output or review past agent conversations."
---

# Self Reflect

A personal productivity tracking tool that aggregates data from GitHub contributions and AI coding agent sessions (Claude Code, Cursor) into a single dashboard.

## Purpose

This skill helps developers understand their productivity patterns by:
- Visualizing GitHub contribution trends over time
- Tracking repositories created and contributed to
- Browsing historical conversations with coding agents (Claude Code, Cursor)
- Seeing which projects and branches you've worked on across agents

## Quick Start

```bash
cd skills/self-reflect

# Install dependencies
npm install

# Collect all data (GitHub + agent sessions)
node scripts/cli.js sync

# Start the dashboard
node scripts/cli.js serve
```

Then open http://localhost:3000 in your browser.

## CLI Commands

### `sync`
Collect all data sources at once (GitHub + agents) and backup to the data repo.

```bash
node scripts/cli.js sync
```

If the `self-reflect-data` repo is cloned as a sibling directory, sync will also:
- Copy `agents/sessions.json` and `github/contributions.json` to the data repo
- Backup all Claude project files (`CLAUDE.md`, `settings.json`, `sessions-index.json`)
- Backup all Claude session conversation files (`.jsonl`) - the raw chat data
- Backup all Cursor session transcript files (`.txt`)
- Backup the global `~/.claude/CLAUDE.md`

### `collect github`
Fetch GitHub contribution data using the `gh` CLI.

```bash
node scripts/cli.js collect github
node scripts/cli.js collect github --from 2024-01-01 --to 2024-12-31
```

Options:
- `--from YYYY-MM-DD` - Start date (default: 1 year ago)
- `--to YYYY-MM-DD` - End date (default: today)
- `--user USERNAME` - GitHub username (default: authenticated user)

**Requirement:** GitHub CLI (`gh`) must be installed and authenticated.

### `collect agents`
Collect session data from Claude Code and Cursor.

```bash
node scripts/cli.js collect agents
```

This scans:
- `~/.claude/projects/*/sessions-index.json` - Claude Code session metadata
- `~/.cursor/` - Cursor session data (if available)

### `serve`
Start the local dashboard server.

```bash
node scripts/cli.js serve
node scripts/cli.js serve --port 8080
```

Options:
- `--port PORT` - Port number (default: 3000, auto-increments if busy)

## Dashboard Features

### Main View
- **Stats row**: Total contributions, commits, PRs, issues, repos, agent sessions
- **Charts**: Contribution trends, repos created over time, session activity
- **Repos by commits**: Which repositories you've contributed to most
- **Agent sessions**: Clickable list of past agent conversations

### Session Viewer Modal
- **Conversation display**: User messages, assistant responses, tool calls
- **Session sidebar**: Quick navigation between sessions (right side)
- **Tick mark navigation**: Quick jump to user messages (top-right corner)
- **Keyboard shortcuts**:
  - `j`/`k` or arrows - Navigate between user messages
  - `[`/`]` - Switch between sessions
  - `Escape` - Close modal

### Filters
- **Time range**: 24h, 7d, 30d, 1y
- **Orchestrator filter**: Filter sessions by source (conductor, cli, cursor, claude-worktree)

## Data Storage

### Local Storage
Data is stored in the `data/` directory (gitignored):

```
data/
├── github/
│   └── contributions.json   # GitHub API response with contributions
└── agents/
    └── sessions.json        # Aggregated session metadata
```

Session conversations are read directly from:
- Claude Code: `~/.claude/projects/*/{sessionId}.jsonl`
- Cursor: `~/.cursor/` (conversation files)

### Data Repo Backup
For persistent backup, clone `seflless/self-reflect-data` to `~/dev/`:

```bash
gh repo clone seflless/self-reflect-data ~/dev/self-reflect-data
```

When you run `sync`, it will copy data to:
```
~/dev/self-reflect-data/
├── CLAUDE.md                    # Global ~/.claude/CLAUDE.md backup
├── agents/sessions.json         # Session metadata
├── github/contributions.json    # GitHub data
├── claude-projects/             # Claude Code project backups
│   └── {project-name}/
│       ├── CLAUDE.md            # Project-specific instructions
│       ├── settings.json        # Project settings
│       ├── sessions-index.json  # Session metadata
│       └── sessions/            # Raw conversation data
│           └── {sessionId}.jsonl
└── cursor-projects/             # Cursor project backups
    └── {project-name}/
        └── agent-transcripts/
            └── {sessionId}.txt
```

## Architecture

```
skills/self-reflect/
├── SKILL.md              # This file - skill definition and docs
├── package.json          # Dependencies (marked for markdown rendering)
├── scripts/
│   ├── cli.js            # Main CLI entry point + HTTP server
│   ├── github-collector.js   # GitHub data collection via gh CLI
│   └── agents-collector.js   # Agent session scanning
├── web/
│   └── index.html        # Single-file dashboard (HTML + CSS + JS)
└── data/                 # Collected data (gitignored)
```

### Key Technical Details

**Session loading**: Conversations are loaded on-demand when clicking a session (not pre-loaded). The server reads the JSONL file and parses messages, tool calls, and results.

**Tool call parsing**: Claude Code stores tool calls as `tool_use` blocks with matching `tool_result` blocks. The CLI does a two-pass parse: first collecting results by ID, then building the message stream.

**Repo name extraction**: The `getRepoName()` function extracts meaningful folder names from project paths, skipping common directories like `Users`, `workspaces`, `.agents`.

## Next Steps / Roadmap

### High Priority
- [ ] Add Cursor session support (currently only Claude Code works)
- [ ] Add session search/filter in the modal
- [ ] Show token usage per session if available in the JSONL

### Nice to Have
- [ ] Export conversation as markdown
- [ ] Compare productivity across time periods
- [ ] Add user benchmarks (compare against other developers)
- [ ] Heatmap visualization for contribution calendar
- [ ] Auto-refresh when new sessions are created

### Known Issues
- Large sessions (1000+ messages) may be slow to load
- Tool call results can be very long - consider truncating more aggressively
- Branch name may be outdated if it changed during the session

## Development

To work on this skill:

1. Start the server in watch mode (manual restart needed for now):
   ```bash
   node scripts/cli.js serve
   ```

2. Edit `web/index.html` - it's a single file with inline CSS and JS

3. Refresh browser to see changes

4. The `data/` directory is gitignored - run `sync` to populate it on a fresh clone
