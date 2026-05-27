---
name: do
description: 'Manifest executor. Iterates through Deliverables satisfying Acceptance Criteria, then verifies all ACs and Global Invariants pass. Use when you have a manifest from /define.'
user-invocable: true
---

# /do - Manifest Executor

## Goal

Execute a Manifest: satisfy all Deliverables' Acceptance Criteria, then verify everything passes (including Global Invariants).

**Why quality execution matters**: The manifest front-loaded the thinking—criteria are already defined. Your job is implementation that passes verification on first attempt. Every verification failure is rework.

## Input

`$ARGUMENTS` = manifest file path (REQUIRED)

If no arguments: Output error "Usage: /do <manifest-file-path>"

## Principles

1. **ACs define success, not the path** - Work toward acceptance criteria however makes sense. The manifest says WHAT, you decide HOW.

2. **Target failures specifically** - On verification failure, fix the specific failing criterion. Don't restart from scratch. Don't touch passing criteria.

3. **Respect tradeoffs** - When values conflict, check the manifest's "Tradeoffs & Preferences" section and apply.

## Constraints

**Must call /verify** - Can't declare done without verification. When all deliverables addressed:
```
Skill("vibe-experimental:verify", "/tmp/manifest-{ts}.md /tmp/do-log-{ts}.md")
```

## Todo Discipline

**Create todo list immediately** based on manifest structure—deliverables and their ACs. Use `D{N}:` prefix. Adapt to THIS manifest's complexity.

**Required elements:**
- Log file creation (`/tmp/do-log-{timestamp}.md`)
- `→log` after implementation steps (externalizes progress)
- `(expand: ...)` when sub-tasks will emerge during implementation
- `Refresh: read full log` before calling /verify
- Acceptance criteria on each todo ("; done when X")

**Update todos after every substantive action**—no batching completions.

## Log Discipline

**Create execution log** - Write to `/tmp/do-log-{timestamp}.md`. This is your working memory.

**Write as you go** - After each significant action, update the log. Don't wait until the end.

**Refresh before /verify** - Read the full log to restore context before verification.

## What to Do

**Read the manifest** - Extract intent, global invariants, deliverables with their ACs, tradeoffs.

**Work through deliverables** - For each, satisfy its acceptance criteria. Log your work.

**Call /verify** - When all deliverables addressed, verify everything passes.

**Handle failures** - Fix specific failing criteria, call /verify again. Loop until pass.

**Escalate when stuck** - If you've tried 3+ approaches on a criterion and can't satisfy it:
```
Skill("vibe-experimental:escalate", "[criterion ID] blocking after 3 attempts")
```

## Log Structure

```markdown
# Execution Log

Manifest: [path]
Started: [timestamp]

## Intent
**Goal:** [from manifest]

## Deliverable 1: [Name]

### AC-1.1: [description]
- Approach: [what you tried]
- Result: [outcome]

### Status: [COMPLETE/IN PROGRESS]

## Verification Attempts

### Attempt 1
- Results: [summary]
- Action: [what to fix]
```

## Flow

```
1. Read manifest
2. Create todos + log
3. For each deliverable: work toward ACs, log progress
4. Call /verify
5. If failures: fix specific criteria, /verify again
6. All pass: /verify calls /done
```
