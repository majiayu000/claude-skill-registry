---

name: vibekanban
description: "Vibe Kanban orchestration platform for AI coding agents: workspaces, sessions, task management, code review, git worktrees, multi-agent support. Keywords: Vibe Kanban, AI agents, Claude Code, Codex, Gemini, kanban board, git worktree, code review, MCP server, workspaces, sessions."
version: "0.0.167"
release_date: "2026-02-01"

# Vibe Kanban

Orchestration platform for AI coding agents. Plan, review, and manage AI-generated code in isolated git worktrees.

## Quick Navigation

| Topic                         | Reference                                               |
| ----------------------------- | ------------------------------------------------------- |
| Installation & Setup          | [getting-started.md](references/getting-started.md)     |
| **Workspaces (Beta)**         | [workspaces.md](references/workspaces.md)               |
| Projects, Tasks, Review       | [core-features.md](references/core-features.md)         |
| Subtasks, Attempts, Conflicts | [advanced-features.md](references/advanced-features.md) |
| Settings, Agents, Tags        | [configuration.md](references/configuration.md)         |
| GitHub, Azure, VSCode, MCP    | [integrations.md](references/integrations.md)           |
| Common Issues                 | [troubleshooting.md](references/troubleshooting.md)     |
| Best Practices                | [vibe-guide.md](references/vibe-guide.md)               |

## Quick Start

### Install & Run

```bash
npx vibe-kanban
```

Opens browser automatically. Use `PORT=8080 npx vibe-kanban` for fixed port.

### Prerequisites

- Node.js LTS
- Authenticated coding agent (Claude Code, Codex, Gemini, etc.)
- GitHub CLI (`gh`) for PR integration

### First Steps

1. Authenticate with a coding agent externally
2. Run `npx vibe-kanban`
3. Complete setup dialogs
4. Create project from existing git repo
5. Add tasks and start executing

## Two UI Modes

### Classic Kanban (Tasks)

Traditional board with columns: To do → In Progress → In Review → Done

### Workspaces (Beta) — NEW

Modern interface with:

- **Sessions**: Multiple conversation threads per workspace
- **Command Bar**: `Cmd/Ctrl + K` for all actions
- **Workspace Notes**: Document requirements and decisions
- **Multi-repo support**: Work across multiple repositories
- **Integrated Terminal**: PTY-backed terminal with shell support
- **Session Dropdown**: Agent icons displayed next to session titles

Switch between modes via Command Bar → "Open in Old UI"

## Core Concepts

### Git Worktrees

Each task/workspace runs in an **isolated git worktree**:

- Agents can't interfere with each other
- Safe from main branch changes
- Automatic cleanup after completion

### Task Flow (Classic)

```
To do → In Progress → In Review → Done
```

- **To do**: Task created
- **In Progress**: Agent executing
- **In Review**: Agent finished, awaiting review
- **Done**: Merged or PR merged

### Task Attempts

One task can have multiple attempts:

- Different agent
- Different branch
- Fresh conversation context

## Supported Agents

| Agent          | Variants              |
| -------------- | --------------------- |
| Claude Code    | DEFAULT, PLAN, ROUTER |
| Codex          | DEFAULT, HIGH         |
| Gemini         | DEFAULT, FLASH        |
| GitHub Copilot | DEFAULT               |
| Amp            | DEFAULT               |
| Cursor Agent   | DEFAULT               |
| OpenCode       | DEFAULT               |
| Qwen Code      | DEFAULT               |
| Droid          | DEFAULT               |
| Antigravity    | DEFAULT               |

Select agent when creating task attempt or workspace session.

## Project Configuration

### Setup Scripts

Run before agent execution (e.g., `npm install`, `cargo build`).

### Dev Server Scripts

Start dev server for preview (e.g., `npm run dev`).

### Cleanup Scripts

Run after agent finishes (e.g., `npm run format`).

### Copy Files

Files to copy from main project to worktree (e.g., `.env`).

## Task Creation

```
Press C or click + to create task
```

Options:

- **Create Task**: Add to board only
- **Create & Start**: Add and immediately execute with default agent

### Task Tags

Reusable snippets via `@mention`:

- Type `@` in description
- Select tag from dropdown
- Content inserted at cursor

Task description editor supports markdown paste and preserves inline code formatting.

## Code Review

1. Task moves to "In Review" when agent finishes
2. Click Diff icon to view changes
3. Click `+` on any line to add comment
4. Submit all comments together
5. Task returns to "In Progress" for fixes

## Git Operations

| Action    | Description                       |
| --------- | --------------------------------- |
| Merge     | Merge to target branch            |
| Create PR | Open PR on GitHub/Azure           |
| Rebase    | Update with target branch changes |
| Push      | Push additional changes to PR     |

## Preview Mode

Test web apps without leaving Vibe Kanban:

1. Configure dev server script in project settings
2. Click "Start Dev Server" in Preview tab
3. View app in embedded iframe
4. Install `vibe-kanban-web-companion` for component selection

## Keyboard Shortcuts

| Key              | Action                              |
| ---------------- | ----------------------------------- |
| `C`              | Create task                         |
| `⌘/Ctrl + Enter` | Submit/Send message                 |
| `k/j`            | Navigate up/down in column          |
| `h/l`            | Navigate left/right between columns |
| `Enter`          | Open task                           |
| `⌘/Ctrl + S`     | Focus search                        |

## MCP Integration

### Add MCP Servers to Agents

Settings → MCP Servers → Select agent → Add servers

### Vibe Kanban MCP Server

Expose Vibe Kanban to external MCP clients:

```json
{
  "mcpServers": {
    "vibe_kanban": {
      "command": "npx",
      "args": ["-y", "vibe-kanban@latest", "--mcp"]
    }
  }
}
```

MCP tools: `list_projects`, `list_tasks`, `create_task`, `start_task_attempt`

## Critical Safety Note

Vibe Kanban runs agents with `--dangerously-skip-permissions`/`--yolo` by default for autonomous operation. Each task runs in isolated worktree, but agents can still perform system-level actions. Review work and keep backups.

## Critical Prohibitions

- Do not skip agent authentication before first use
- Do not ignore worktree isolation benefits
- Do not forget to configure setup/cleanup scripts for dependencies
- Do not mix multiple agents on same task without new attempts
- Do not ignore rebase conflicts — resolve or abort

## Links

- Official docs: https://www.vibekanban.com/docs
- Vibe Guide: https://www.vibekanban.com/vibe-guide
- GitHub: https://github.com/BloopAI/vibe-kanban
