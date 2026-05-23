---
name: implement
description: Use when executing an implementation plan — dispatches subagent per task with self-review, verification along the way, and commits
---

# Implement

Execute a plan by dispatching a fresh subagent per task. Each subagent implements, tests, self-reviews, and commits. No heavy review gates per task — the full review happens after all tasks complete (see `dodi-dev:review`).

## Process

1. Read the plan, extract all tasks with full text
2. For each task sequentially:
   a. Dispatch implementer subagent with full task text + context (see implementer-prompt.md)
   b. Handle subagent status (see below)
   c. Mark task complete
3. After all tasks: invoke `dodi-dev:review`

**Never dispatch multiple implementers in parallel** — they'll conflict.

## Model Selection

- **Mechanical tasks** (1-2 files, clear spec): use a fast model
- **Integration tasks** (multi-file, pattern matching): use standard model
- **Architecture/judgment tasks**: use most capable model

## Handling Implementer Status

| Status | Action |
|--------|--------|
| **DONE** | Mark complete, next task |
| **DONE_WITH_CONCERNS** | Read concerns. If correctness issue, address first. If observation, note and proceed |
| **NEEDS_CONTEXT** | Provide missing context, re-dispatch |
| **BLOCKED** | Assess: provide more context, use more capable model, break task smaller, or escalate to human |

Never ignore an escalation or retry without changes.

## Verification Along the Way

After each subagent completes, verify its claims before moving on:
- Check `git diff` or `git log` to confirm changes were actually made
- If the task included tests, confirm they actually ran and passed
- Don't trust "tests pass" without evidence
