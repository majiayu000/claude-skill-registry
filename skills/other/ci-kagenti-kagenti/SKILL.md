---
name: ci
description: CI pipeline monitoring, status checks, and PR validation workflows
---

```mermaid
flowchart TD
    PR([PR / Push]) --> CI{"/ci"}
    CI -->|Check status| STATUS["ci:status"]:::ci
    CI -->|Monitor running| MON["ci:monitoring"]:::ci
    CI -->|Failed, investigate| RCACI["rca:ci"]:::rca
    CI -->|Failed, fix + rerun| TDDCI["tdd:ci"]:::tdd

    STATUS --> RESULT{Result?}
    RESULT -->|All pass| DONE([Merge])
    RESULT -->|Failed| RCACI
    MON -->|Completed| STATUS

    RCACI --> ROOT[Root Cause]
    ROOT --> TDDCI
    TDDCI -->|CI passes| DONE

    classDef ci fill:#2196F3,stroke:#333,color:white
    classDef rca fill:#FF5722,stroke:#333,color:white
    classDef tdd fill:#4CAF50,stroke:#333,color:white
```

> Follow this diagram as the workflow.

# CI Skills

CI pipeline skills for monitoring and managing GitHub Actions workflows.

## Auto-Select Sub-Skill

When this skill is invoked, determine the right sub-skill based on context:

```
What do you need?
    │
    ├─ Check current PR status (what passed/failed?)
    │   → Use `ci:status`
    │
    ├─ Monitor a running CI job (wait for it to finish)
    │   → Use `ci:monitoring`
    │
    ├─ CI failed and need to investigate
    │   → Use `rca:ci` (root cause analysis from logs)
    │
    └─ CI failed and need to fix + re-run
        → Use `tdd:ci` (commit, push, iterate)
```

## Available Skills

| Skill | Purpose | When |
|-------|---------|------|
| `ci:status` | Check PR checks, failures, test results | Before/after pushing |
| `ci:monitoring` | Monitor running jobs, create tasks for results | After pushing, waiting |

## Quick Status Check

```bash
gh pr checks
```

## Related Skills

- `rca:ci` - Investigate CI failures
- `tdd:ci` - Fix and re-run CI iteratively
- `ci:status` - Detailed check status
- `ci:monitoring` - Wait for running jobs
