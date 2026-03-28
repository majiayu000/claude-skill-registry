---
name: subagent-dev
description: Use when executing a multi-task plan where each task is independent, or when the user wants parallel or isolated task execution with review.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, Agent
argument-hint: "[plan reference or task list]"
---

Execute a plan using subagent-driven development for: **$ARGUMENTS**

## Iron Law

> **The controller coordinates. Subagents implement. Never mix roles.**

The controller agent (you) MUST NOT write production code directly. You dispatch subagents for each task, review their work, and coordinate the overall plan.

## Architecture

```
Controller (you)
  ├── Read the plan
  ├── For each task:
  │   ├── Dispatch Implementer subagent (fresh context)
  │   ├── Dispatch Spec Reviewer subagent
  │   ├── Dispatch Quality Reviewer subagent
  │   └── Handle status (DONE / CONCERNS / BLOCKED)
  └── Verify all tests pass at the end
```

## Steps

### 1. Load the Plan

Read `task_plan.md` or the user's task list. Extract all tasks with:
- Task description
- Files involved
- Dependencies (what must complete first)
- Acceptance criteria

### 2. Execute Each Task

For each task (respecting dependency order):

#### A. Dispatch Implementer

Launch a subagent with Agent tool:
```
Prompt: "Implement [task description].
Files to modify: [list]
Pattern to follow: [reference file]
Acceptance criteria: [criteria]
Run tests after implementation."
```

Use `model: "sonnet"` for mechanical tasks, `model: "opus"` for complex architecture.

#### B. Check Implementer Status

The implementer should report one of:

| Status | Meaning | Action |
|--------|---------|--------|
| **DONE** | Task complete, tests pass | Proceed to review |
| **DONE_WITH_CONCERNS** | Complete but has questions | Review concerns, decide if acceptable |
| **NEEDS_CONTEXT** | Missing information to proceed | Provide context, re-dispatch |
| **BLOCKED** | Cannot complete (dependency, bug) | Log blocker, skip to next task |

#### C. Two-Stage Review

**Stage 1 — Spec Compliance** (must pass first):
- Does the implementation match the task description?
- Are all acceptance criteria met?
- Were the correct files modified?

**Stage 2 — Code Quality** (only after Stage 1 passes):
- Does it follow existing codebase patterns?
- Are there security issues?
- Is the code clean and maintainable?

If either review fails, send feedback to a new implementer subagent for fixes.

### 3. Verify Everything

After all tasks are done:

```bash
# Run full test suite
[test command]

# Check for uncommitted changes
git status
```

### 4. Report

```
## Subagent Execution Report

### Tasks Completed: X/Y
| Task | Status | Implementer | Review |
|------|--------|-------------|--------|
| [task] | DONE | Pass | Pass |

### Files Changed
- [file list]

### Concerns Raised
- [any DONE_WITH_CONCERNS items]

### Blocked Items
- [any BLOCKED items with reasons]
```

## Anti-Rationalization

| Excuse | Rebuttal |
|--------|----------|
| "This task is too small for a subagent" | Small tasks are the BEST use of subagents — they get clean context |
| "I'll just make this quick fix myself" | You are the controller. Controllers don't write code. |
| "The review is overkill for this change" | Every change gets reviewed. No exceptions. |
| "I'll review everything at the end" | Review after EACH task. Catching issues early is 10x cheaper. |
| "The tests were passing before my changes" | Verify. Don't assume. Run them. |

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
