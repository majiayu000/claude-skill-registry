---
name: auto
description: |
  Autonomous AI coding loop (Ralph Wiggum methodology). Use when running AI agents
  in unattended/autonomous mode to independently select and complete tasks from a
  structured task list (prd.json). Enables AFK development across multiple context windows.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: workflow
---

# Autonomous AI Coding Loop

Enable unattended AI-driven development using the Ralph Wiggum methodology.

**Use When**: Running AI agents autonomously, AFK development, batch task execution
**4D Phase**: Develop (autonomous execution of generated tasks)

---

## Overview

The autonomous loop runs AI agents in a cycle, where each iteration:
1. Starts with fresh context (no conversation history dependency)
2. Reads project state from files (prd.json, progress.md, CLAUDE.md)
3. Selects and implements one task
4. Commits changes and updates state
5. Documents learnings for future iterations

Continuity is maintained through **persistent files**, not conversation history.

---

## Core Principles

### 1. Fresh Context Per Iteration
Each cycle begins with a clean AI context window. The AI agent reconstructs
understanding from: git history, prd.json (task state), progress.md (learnings),
and CLAUDE.md/AGENTS.md (project guardrails).

### 2. Right-Sized Decomposition
Tasks must be completable within a single context window. Break large features
into focused, atomic steps. If a task is too big, split it before starting.

### 3. Feedback-Driven Quality
Automated checks (tests, linting, type checking) serve as guardrails:
- Quality checks must pass before committing
- Failed checks provide feedback for the next attempt
- Pre-commit hooks catch regressions

### 4. Knowledge Persistence
Learnings accumulate in `progress.md` across iterations:
- Architectural decisions
- Gotchas and edge cases
- Patterns discovered
- Error resolutions

### 5. Agent-Driven Prioritization
The AI agent chooses which task to work on based on:
- Priority level (critical > high > medium > low)
- Dependency resolution (prerequisites must be complete)
- Task ID ordering (lower IDs first when priority is equal)

---

## Workflow

### Option A: PRD-Based Setup (Planned Work)

```bash
# 1. Create PRD and task breakdown (existing Samuel workflow)
# Use .claude/skills/create-prd/SKILL.md
# Use .claude/skills/generate-tasks/SKILL.md

# 2. Initialize autonomous loop
samuel auto init --prd .claude/tasks/0001-prd-feature.md

# 3. Review generated files
cat .claude/auto/prd.json      # Task list in JSON
cat .claude/auto/prompt.md     # Iteration prompt
```

### Option B: Pilot Mode (Zero Setup)

```bash
# Fully autonomous — no PRD or task files needed
samuel auto pilot

# Customize iterations, focus, and discovery frequency
samuel auto pilot --iterations 20 --focus testing
samuel auto pilot --discover-interval 3 --max-tasks 5

# Dry run to preview without executing
samuel auto pilot --dry-run

# Skip confirmation
samuel auto pilot --yes
```

Pilot mode automatically discovers improvement opportunities (test gaps,
code quality issues, security concerns, documentation gaps) and generates
atomic tasks, then implements them in alternating discovery/implementation
iterations.

### Running the Loop

```bash
# Start the loop (will prompt for confirmation)
samuel auto start

# Start with custom iteration count
samuel auto start --iterations 20

# Skip confirmation
samuel auto start --yes

# Dry run (see what would happen)
samuel auto start --dry-run
```

### Monitoring

```bash
# Check progress
samuel auto status

# View recent learnings
tail -20 .claude/auto/progress.md

# List all tasks
samuel auto task list
```

### Manual Intervention

```bash
# Mark a task as completed manually
samuel auto task complete 1.1

# Skip a task
samuel auto task skip 2.3

# Reset a task to pending
samuel auto task reset 1.1

# Add a new task
samuel auto task add "3.0" "New parent task"
```

---

## Per-Iteration Protocol

When operating in autonomous mode, follow these steps exactly:

### Step 1: Read Context
```
1. Read CLAUDE.md (or AGENTS.md) for project guardrails
2. Read .claude/auto/progress.md for learnings from prior iterations
3. Read .claude/auto/prd.json to find tasks and current state
```

### Step 2: Select Task
```
1. Find tasks with status "pending"
2. Filter out tasks whose depends_on items are not "completed" or "skipped"
3. Sort by priority: critical > high > medium > low
4. If priorities match, prefer lower task IDs
5. Select the top task
```

### Step 3: Implement
```
1. Update task status to "in_progress" in prd.json
2. Follow project guardrails from CLAUDE.md
3. Write tests alongside code
4. Keep changes atomic -- one task per iteration
5. Respect file size limits (functions ≤50 lines, files ≤300 lines)
```

### Step 4: Quality Check
```
1. Run all commands listed in prd.json config.quality_checks
2. All checks must pass before committing
3. If a check fails, fix the issue and retry
4. If unfixable, mark task as "blocked" and document why
```

### Step 5: Commit
```
1. Stage only files related to this task
2. Use conventional commit format: type(scope): task ID - description
3. Example: feat(auth): task 1.1 - create user schema
```

### Step 6: Update State
```
1. Set task status to "completed" in prd.json
2. Record commit SHA in task's commit_sha field
3. Record iteration number in task's iteration field
4. Update progress.completed_tasks count
```

### Step 7: Document Learnings
```
Append to .claude/auto/progress.md:
[timestamp] [iteration:N] [task:ID] COMPLETED: what was done
[timestamp] [iteration:N] [task:ID] LEARNING: any insights or gotchas
```

---

## prd.json Format

```json
{
  "version": "1.0",
  "project": {
    "name": "project-name",
    "description": "Project description",
    "source_prd": ".claude/tasks/0001-prd-feature.md",
    "created_at": "2026-02-11T10:00:00Z",
    "updated_at": "2026-02-11T12:00:00Z"
  },
  "config": {
    "max_iterations": 50,
    "quality_checks": ["go test ./...", "go vet ./..."],
    "ai_tool": "claude",
    "ai_prompt_file": ".claude/auto/prompt.md",
    "sandbox": "none"
  },
  "tasks": [
    {
      "id": "1.0",
      "title": "Database Setup",
      "status": "completed",
      "priority": "critical",
      "complexity": "medium",
      "depends_on": [],
      "commit_sha": "abc1234",
      "iteration": 1
    },
    {
      "id": "1.1",
      "title": "Create user schema",
      "status": "pending",
      "priority": "high",
      "parent_id": "1.0",
      "depends_on": ["1.0"]
    }
  ],
  "progress": {
    "total_tasks": 10,
    "completed_tasks": 3,
    "status": "running"
  }
}
```

### Task Statuses
- **pending**: Not yet started (available for selection)
- **in_progress**: Currently being worked on
- **completed**: Successfully finished with commit
- **skipped**: Deliberately skipped (counts as "done" for dependencies)
- **blocked**: Cannot proceed (needs human intervention)

---

## progress.md Format

Append-only log with structured entries:

```
[2026-02-11T10:30:00Z] [iteration:1] [task:1.0] STARTED: Database setup
[2026-02-11T10:35:00Z] [iteration:1] [task:1.0] COMPLETED: Created schema
[2026-02-11T10:35:00Z] [iteration:1] [task:1.0] LEARNING: Use explicit indexes
[2026-02-11T10:36:00Z] [iteration:1] QUALITY_CHECK: go test ./... PASSED
[2026-02-11T10:36:00Z] [iteration:1] COMMIT: abc1234 "feat(db): task 1.0"
[2026-02-11T10:40:00Z] [iteration:2] [task:1.1] ERROR: FK constraint wrong
```

Entry types: STARTED, COMPLETED, ERROR, LEARNING, QUALITY_CHECK, COMMIT

---

## Tips for Success

1. **Start supervised, then go AFK**: Run a few iterations manually to verify
   the prompt and quality checks work correctly. Then let it run unattended.

2. **Prioritize risky tasks**: Have the AI tackle architectural decisions and
   integration points first. Reserve human oversight for critical foundations.

3. **Define quality level**: Specify whether code is prototype, production, or
   library quality so the agent matches appropriate standards.

4. **Take small steps**: Break work into focused tasks. Each should produce one
   commit. Smaller tasks = better feedback loops.

5. **Use quality gates**: Tests, linting, and type checking catch regressions
   before they compound across iterations.

6. **Review progress.md**: The learnings journal accumulates valuable insights.
   Read it periodically to catch issues early.

---

## Error Recovery

When the AI agent encounters errors:

1. **Within iteration**: Try to fix within the current iteration
2. **Mark as blocked**: If unfixable, set status to "blocked" with description
3. **Document in progress.md**: Append error details as LEARNING entry
4. **Fresh context helps**: The next iteration starts clean and may succeed
   where the previous one got stuck

When the loop itself fails:
```bash
samuel auto status              # Check what happened
samuel auto task list           # See task states
samuel auto task reset 1.1      # Reset a stuck task
samuel auto start               # Resume the loop
```

---

## Integration with 4D Methodology

The auto loop extends the existing COMPLEX mode workflow:

```
Standard COMPLEX Mode:
  create-prd → generate-tasks → manual implementation (HITL)

With Auto Loop (PRD-based):
  create-prd → generate-tasks → samuel auto init → samuel auto start (autonomous)

With Pilot Mode (zero setup):
  samuel auto pilot (discovers and implements autonomously)
```

The human can re-enter the loop at any point by stopping the process and returning
to manual task-by-task implementation.
