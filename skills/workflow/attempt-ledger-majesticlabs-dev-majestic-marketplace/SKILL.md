---
name: attempt-ledger
description: Knowledge about attempt tracking and gating patterns for task execution
triggers:
  - relay
  - epic
  - task execution
  - attempt
  - gating
  - retry
---

# Attempt Ledger Pattern

## Purpose

The attempt ledger tracks execution attempts for tasks, enabling:

- **Retry with context:** Each attempt includes previous failure information
- **Gating:** Prevents infinite retry loops when tasks consistently fail
- **Progress persistence:** Resume execution after interruption
- **Receipt tracking:** Structured summaries instead of full transcripts

## Schema

```yaml
# .majestic/attempt-ledger.yml
version: 1
epic_id: "20260111-feature-name"
started_at: "2026-01-11T17:30:00Z"

settings:
  max_attempts_per_task: 3
  timeout_minutes: 15
  review:
    enabled: true
    provider: repoprompt  # repoprompt | gemini | none

task_status:
  T1: completed
  T2: in_progress
  T3: pending
  T4: blocked

attempts:
  T1:
    - id: 1
      started_at: "..."
      ended_at: "..."
      result: success
      receipt:
        summary: "Created migration and model"
        files_changed: [file1.rb, file2.rb]

  T2:
    - id: 1
      result: failure
      receipt:
        error_category: missing_dependency
        error_summary: "Database not migrated"
        suggestion: "Run db:migrate first"

gated_tasks:
  T5:
    reason: "max_attempts_exceeded"
    gated_at: "..."
```

## Gating Rules

Tasks are gated (blocked from retry) when:

| Condition | Gating Action |
|-----------|---------------|
| `attempts >= max_attempts` | Gate with `max_attempts_exceeded` |
| Same error repeated 2+ times | Gate with `repeated_failure` |
| Manual block by user | Gate with `user_blocked` |

## Receipt Structure

### Success Receipt

```yaml
receipt:
  summary: "Brief description of what was done"
  files_changed: [list, of, files]
  tests_passed: true
```

### Failure Receipt

```yaml
receipt:
  error_category: missing_dependency | code_error | test_failure | timeout
  error_summary: "What went wrong"
  approach_taken: "What was attempted"
  suggestion: "What to try differently"
```

## Task Status Flow

```
pending → in_progress → completed
                ↓
            failure → pending (retry)
                ↓
            max_attempts → gated
```

## Integration with Re-anchoring

Each fresh Claude instance receives:

1. **Git state:** Current branch, last commit, uncommitted changes
2. **Epic context:** Title, description, overall progress
3. **Task details:** Files, acceptance criteria, dependencies
4. **Previous receipts:** What was tried, what failed, why

This prevents context drift and ensures each attempt builds on prior learnings.

## Commands

| Command | Purpose |
|---------|---------|
| `/relay:init` | Create epic and ledger from blueprint |
| `/relay:status` | Show progress and gated tasks |
| `/relay:work` | Execute tasks with attempt tracking |

## Configuration

In `.agents.yml`:

```yaml
relay:
  max_attempts_per_task: 3
  timeout_minutes: 15
  review:
    enabled: true
    provider: none  # repoprompt | gemini | none
```

Override locally in `.agents.local.yml` (gitignored).
