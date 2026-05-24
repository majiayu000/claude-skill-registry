---
name: agent-orchestrate
description:
  Multi-agent task orchestration for Claude Code. When given multiple tasks to execute, use this
  skill to spawn parallel worker agents through Sibyl's MetaOrchestrator instead of Claude Code's
  built-in Task tool. This enables true multi-process execution with budget controls, quality gates,
  and coordination.
allowed-tools: Bash, Read, Grep, Glob
---

# Agent Orchestration

**CRITICAL: This skill teaches you how to dispatch tasks to multiple worker agents.**

When you're asked to work on multiple tasks, or to "dispatch agents", "parallelize work", or
"orchestrate" - use **Sibyl's MetaOrchestrator** via the CLI, NOT Claude Code's built-in Task tool.

## Why This Matters

Claude Code's built-in `Task` tool spawns inline subagents within YOUR process. This is useful for
research, but NOT for parallel task execution because:

- Subagents run sequentially, not in parallel
- No budget controls or quality gates
- No coordination between workers
- Context bloat as results accumulate

**Sibyl's MetaOrchestrator** spawns separate Claude processes that:

- Run truly in parallel (up to N concurrent)
- Have isolated worktrees (no git conflicts)
- Go through implement → review → rework loops
- Track budget and can pause when limits hit
- Report progress through the message bus

---

## Quick Start

```bash
# One-liner: dispatch all todo tasks with 3 parallel agents
sibyl agent dispatch --status todo --strategy parallel --max 3

# With budget limit
sibyl agent dispatch --status todo --budget 25.00 --gates lint,test

# Specific tasks
sibyl agent dispatch task_abc123 task_def456 --strategy parallel
```

---

## The Dispatch Command

`sibyl agent dispatch` is the high-level command that handles everything:

```bash
sibyl agent dispatch [TASK_IDS...] [OPTIONS]

Options:
  --status, -s    Filter tasks by status (todo, doing, blocked)
  --priority      Filter tasks by priority
  --strategy      Execution strategy: parallel, sequential, priority
  --max, -m       Max concurrent agents (default: 3)
  --budget, -b    Budget limit in USD
  --gates, -g     Quality gates (comma-separated: lint,test,typecheck)
  --dry-run       Show what would be dispatched
  --project, -p   Project ID (auto-resolves from cwd)
```

### Examples

```bash
# Dispatch all todo tasks
sibyl agent dispatch --status todo

# Dispatch high-priority tasks only
sibyl agent dispatch --status todo --priority high,critical

# Parallel with 4 workers and $50 budget
sibyl agent dispatch --status todo --strategy parallel --max 4 --budget 50.00

# Sequential with quality gates
sibyl agent dispatch task_abc --strategy sequential --gates lint,test,typecheck

# Dry run first
sibyl agent dispatch --status todo --dry-run
```

---

## Lower-Level Commands

For fine-grained control, use the `sibyl agent orchestrate` subcommands:

```bash
# Initialize orchestrator
sibyl agent orchestrate init

# Queue specific tasks
sibyl agent orchestrate queue task_abc123 task_def456

# Set strategy
sibyl agent orchestrate strategy parallel --max 4

# Set budget
sibyl agent orchestrate budget 50.00 --alert 0.8

# Start processing
sibyl agent orchestrate start --gates lint,test

# Monitor progress
sibyl agent orchestrate status

# Pause/resume
sibyl agent orchestrate pause
sibyl agent orchestrate resume
```

---

## Strategies

| Strategy     | Behavior                              | Use When                      |
| ------------ | ------------------------------------- | ----------------------------- |
| `parallel`   | Run up to N tasks concurrently        | Independent tasks, need speed |
| `sequential` | One task at a time                    | Dependent tasks, shared state |
| `priority`   | One at a time, highest priority first | Mixed urgency, limited budget |

---

## Quality Gates

Quality gates run after each implementation cycle:

- `lint` - Run linter (ruff, eslint, etc.)
- `test` - Run test suite
- `typecheck` - Run type checker (pyright, tsc)

If any gate fails, the worker enters a rework cycle (up to 3 attempts).

```bash
sibyl agent dispatch --status todo --gates lint,test,typecheck
```

---

## Monitoring

```bash
# Check orchestration status
sibyl agent orchestrate status

# Output shows:
#   - Queue size and active workers
#   - Completed/failed counts
#   - Budget utilization
#   - Rework cycles
```

---

## Workflow: Orchestrating a Sprint

```bash
# 1. See what's available
sibyl task list --status todo

# 2. Preview what would be dispatched
sibyl agent dispatch --status todo --dry-run

# 3. Launch with controls
sibyl agent dispatch --status todo \
  --strategy parallel \
  --max 3 \
  --budget 30.00 \
  --gates lint,test

# 4. Monitor progress
sibyl agent orchestrate status

# 5. Pause if needed
sibyl agent orchestrate pause
```

---

## When to Use What

**Use Sibyl orchestration (`sibyl agent dispatch`) when:**

- You need multiple implementation tasks done in parallel
- Tasks are independent and can run concurrently
- You want budget controls and quality gates
- You're orchestrating a sprint or batch of work

**Use Claude Code's built-in Task tool when:**

- Researching or exploring code (reading files, searching)
- Asking specialized agents questions
- Delegating subtasks within a single implementation

**Key insight:** These are complementary, not exclusive!

Worker agents spawned by Sibyl orchestration are **encouraged** to use their built-in Task tool for
research, exploration, and subtask delegation. The hierarchy is:

```
MetaOrchestrator (Sibyl)
├── Spawns parallel worker agents for independent TASKS
│
Worker Agent 1                    Worker Agent 2
├── Uses Task tool for research   ├── Uses Task tool for research
├── Spawns subagents as needed    ├── Spawns subagents as needed
└── Implements assigned task      └── Implements assigned task
```

The rule is simple:

- **Cross-task parallelism** → Sibyl orchestration (separate processes, isolated worktrees)
- **Within-task work** → Built-in Task tool (subagents, research, exploration)

---

## Architecture

```
MetaOrchestrator (Tier 1)
├── Manages sprint/project-level coordination
├── Maintains task queue
├── Spawns TaskOrchestrators per strategy
└── Tracks budget and metrics

TaskOrchestrator (Tier 2)
├── Manages single task lifecycle
├── Runs implement → review → rework loop
├── Enforces quality gates
└── Reports to MetaOrchestrator

Worker Agent (Tier 3)
├── Actual Claude process
├── Has isolated git worktree
├── Implements the code
└── Communicates via message bus
```

---

## Troubleshooting

**"No tasks to dispatch"**

- Ensure you have tasks with matching status/priority
- Check project context: `sibyl context`
- Try `--dry-run` to see what matches

**"No orchestrator or project specified"**

- Link your directory to a project: `sibyl project link <project_id>`
- Or specify explicitly: `--project proj_abc123`

**Budget exhausted**

- Check status: `sibyl agent orchestrate status`
- Increase budget: `sibyl agent orchestrate budget 100.00`
- Resume: `sibyl agent orchestrate resume`
