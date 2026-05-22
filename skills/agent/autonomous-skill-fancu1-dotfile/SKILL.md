---
name: autonomous-skill
description: 'Use when user wants to execute long-running tasks that require multiple sessions to complete. This skill manages task decomposition, progress tracking, and autonomous execution using Codex non-interactive mode with auto-continuation. Trigger phrases include autonomous, long-running task, multi-session, 自主执行, 长时任务, autonomous skill.'
---

# Autonomous Skill - Long-Running Task Execution

Execute complex, long-running tasks across multiple sessions using a dual-agent pattern (Initializer + Executor) with automatic session continuation via Codex non-interactive mode.

## Quick Start

Use the `run-session.sh` script to manage autonomous tasks:

```bash
# Start a new autonomous task
~/.codex/skills/autonomous-skill/scripts/run-session.sh "Build a REST API for todo app"

# Continue an existing task
~/.codex/skills/autonomous-skill/scripts/run-session.sh --task-name build-rest-api-todo --continue

# List all tasks and their progress
~/.codex/skills/autonomous-skill/scripts/run-session.sh --list

# Show help
~/.codex/skills/autonomous-skill/scripts/run-session.sh --help
```

## Directory Structure

All task data is stored in `.autonomous/<task-name>/` under the project root:

```text
project-root/
└── .autonomous/
    ├── build-rest-api/
    │   ├── task_list.md        # Master task checklist
    │   ├── progress.md         # Session-by-session notes
    │   ├── session.id          # Last Codex session ID for resumption
    │   └── session.log         # JSON Lines output from sessions
    ├── refactor-auth/
    │   ├── task_list.md
    │   ├── progress.md
    │   └── session.id
    └── ...
```

This allows multiple autonomous tasks to run in parallel without conflicts.

## Script Options

```text
Usage:
  run-session.sh "task description"           Start new task (auto-generates name)
  run-session.sh --task-name <name> --continue Continue specific task
  run-session.sh --list                        List all tasks
  run-session.sh --help                        Show help

Options:
  --task-name <name>       Specify task name explicitly
  --continue, -c           Continue existing task
  --no-auto-continue       Don't auto-continue after session
  --max-sessions N         Limit to N sessions
  --list                   List all existing tasks
  --resume-last            Resume the most recent Codex session
  --network                Enable network access (uses danger-full-access sandbox)
```

## Workflow Overview

```text
User Request → Generate Task Name → Create .autonomous/<task-name>/ → Execute Codex Sessions
                                                                            ↓
                                                                    ┌───────────────┐
                                                                    │ task_list.md  │
                                                                    │ exists?       │
                                                                    └───────┬───────┘
                                                                            │
                                                    ┌───────────────────────┴───────────────────────┐
                                                    │ NO                                        YES │
                                                    ▼                                              ▼
                                            ┌───────────────┐                            ┌───────────────┐
                                            │  INITIALIZER  │                            │   EXECUTOR    │
                                            │  - Analyze    │                            │  - Read state │
                                            │  - Break down │                            │  - Next task  │
                                            │  - Create     │                            │  - Implement  │
                                            │    task_list  │                            │  - Mark done  │
                                            └───────────────┘                            └───────────────┘
                                                                            │
                                                                            ▼
                                                                    ┌───────────────┐
                                                                    │ All complete? │
                                                                    └───────┬───────┘
                                                                            │
                                                            ┌───────────────┴───────────────┐
                                                            │ NO                        YES │
                                                            ▼                              ▼
                                                    Auto-continue               Exit with success
                                                    (3 sec delay)
```

## Usage Examples

### Example 1: Start New Task

```bash
~/.codex/skills/autonomous-skill/scripts/run-session.sh "Build a REST API for todo app"
```

Output:
```text
ℹ Generated task name: build-rest-api-todo
==========================================
  SESSION 1 - build-rest-api-todo
==========================================

==========================================
  INITIALIZER SESSION
==========================================
Task: Build a REST API for todo app
Task Name: build-rest-api-todo
Task Directory: .autonomous/build-rest-api-todo

[Codex creates task_list.md with 25 tasks...]

✓ Initializer session complete
ℹ Session ID saved: 550e8400-e29b-41d4-a716-446655440000

=== Progress: 0/25 ===

Continuing in 3 seconds... (Press Ctrl+C to pause)
```

### Example 2: Continue Existing Task

```bash
~/.codex/skills/autonomous-skill/scripts/run-session.sh --task-name build-rest-api-todo --continue
```

### Example 3: Resume with Session Context

```bash
# Resume the Codex session (preserves conversation context)
~/.codex/skills/autonomous-skill/scripts/run-session.sh --task-name build-rest-api-todo --continue --resume-last
```

### Example 4: List All Tasks

```bash
~/.codex/skills/autonomous-skill/scripts/run-session.sh --list
```

Output:
```text
==========================================
  AUTONOMOUS TASKS
==========================================
  ✓ build-rest-api-todo (25/25 - 100% complete) [session: 550e8400...]
  ○ refactor-auth (12/30 - 40%) [session: 661f9511...]
  ? incomplete-task (no task_list.md)
```

### Example 5: With Network Access

```bash
# Enable network access for tasks that need API calls
~/.codex/skills/autonomous-skill/scripts/run-session.sh --network "Fetch data from GitHub API and analyze"
```

## Key Files

For each task in `.autonomous/<task-name>/`:

| File | Purpose |
|------|---------|
| `task_list.md` | Master task list with checkbox progress |
| `progress.md` | Session-by-session progress notes |
| `session.id` | Last Codex session ID for resumption |
| `session.log` | JSON Lines output from Codex sessions |

## Important Notes

1. **Task Isolation**: Each task has its own directory, no conflicts
2. **Task Naming**: Auto-generated from description (lowercase, hyphens, max 30 chars)
3. **Task List is Sacred**: Never delete or modify task descriptions, only mark `[x]`
4. **One Task at a Time per Session**: Focus on completing tasks thoroughly
5. **Auto-Continue**: Sessions auto-continue with 3s delay; Ctrl+C to pause
6. **Session Resumption**: Use `--resume-last` to preserve Codex conversation context
7. **Network Mode**: `--network` uses `--dangerously-bypass-approvals-and-sandbox`; only use in an isolated environment
8. **Git Hygiene**: Consider adding `.autonomous/` to `.gitignore` to avoid committing logs

## Codex CLI Reference

The script uses these Codex commands internally:

```bash
# Non-interactive execution with file edits (fully autonomous)
# --full-auto: autonomous execution with workspace-write sandbox
codex exec --full-auto --json "prompt"

# Resume previous session
codex exec --full-auto --json resume <SESSION_ID> "prompt"

# Full access (file edits + network) - use with caution!
codex exec --dangerously-bypass-approvals-and-sandbox --json "prompt"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Task not found | Run `--list` to see existing tasks |
| Multiple tasks | Specify task name with `--task-name` |
| Session stuck | Check `session.log` in task directory |
| Need to restart | Delete task directory and start fresh |
| Resume failed | Remove `session.id` to start fresh session |
| Codex not found | Install Codex CLI: `npm install -g @openai/codex` |
