---
name: task-tracker
description: Track progress through structured task lists with complexity scoring and token tracking
category: Workflow Orchestration
---

# Skill: task-tracker

## What I do

I track progress through structured task lists, maintaining momentum and providing complexity data for token-cost-estimation. I help visualise progress and identify tasks that may exceed estimated costs.

## When to use me

- When managing multi-step work
- When tracking progress through a session
- When token-cost-estimation needs complexity per task
- When needing visibility into remaining work
- When tasks need priority ordering

## Core principles

1. **Break down immediately** - Capture all tasks before starting
2. **Track status religiously** - Update as you complete
3. **Score complexity** - Every task gets a complexity rating
4. **Monitor token usage** - Track consumption per task
5. **Maintain momentum** - Visible progress motivates

## Task Structure

### Required Fields

```
Task:
  - ID: unique identifier
  - Description: clear, actionable
  - Status: pending | in_progress | completed | blocked
  - Complexity: simple | moderate | complex
  - Estimated tokens: from token-cost-estimation
  - Actual tokens: filled on completion
```

### Complexity Scoring

| Score | Description | Token Estimate |
|-------|-------------|----------------|
| **Simple** | Single action, clear outcome | 100-500 |
| **Moderate** | Multiple steps, some uncertainty | 500-2000 |
| **Complex** | Investigation needed, high uncertainty | 2000+ |

## Progress Tracking

### Status Updates
- Update **immediately** when status changes
- Never batch updates
- One task `in_progress` at a time

### Token Tracking
```
Task: Implement user validation
Estimated: 800 tokens
Actual: 950 tokens
Variance: +150 (investigation took longer)
→ Record in memory-keeper
```

## Patterns & examples

**Session task list:**
```
Session Goal: Add user authentication
Estimated Total: 3500 tokens

[ ] Task 1: Research auth patterns (moderate, 600 est)
[→] Task 2: Implement JWT handler (complex, 1200 est)
[x] Task 3: Add middleware (simple, 400 est) - actual: 380
[ ] Task 4: Write tests (moderate, 800 est)
[ ] Task 5: Update docs (simple, 500 est)

Progress: 1/5 complete, ~380/3500 tokens used
```

## Anti-patterns to avoid

- ❌ Starting without a task list
- ❌ Batching status updates
- ❌ Multiple tasks in_progress simultaneously
- ❌ Not scoring complexity upfront
- ❌ Ignoring token variance patterns

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Workflow-Orchestration/Task Tracker.md`

## Related skills

- `token-cost-estimation` - Provides complexity and token data
- `estimation` - Complexity scoring methodology
- `time-management` - Time per task tracking
- `scope-management` - Task list reflects scope
- `checklist-discipline` - Rigorous status updates
- `long-running-agent` — Multi-session harness pattern (uses task-tracker per session)
