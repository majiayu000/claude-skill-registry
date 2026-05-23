---
name: resolve-hive-issue
description: Resolve a GitHub issue with structured task breakdown and validation; use for complex or multi-area fixes.
---

# Resolve Hive Issue

## Overview

Use mprocs to coordinate analysis, implementation, simplification, and testing for a complex issue.

## Inputs

- Issue text or link

## Workflow

1. Verify `git` and `mprocs`.
2. Create `.hive/sessions/<session-id>` and `tasks.json`.
3. Write queen and worker prompts (analysis, implementation, simplification, tests).
4. Launch mprocs.

## tasks.json Template

```json
{
  "session": "{SESSION_ID}",
  "created": "{ISO_TIMESTAMP}",
  "status": "active",
  "thread_type": "Hive",
  "task_type": "resolve-hive-issue",
  "issue": {"text": "{ISSUE_TEXT}"},
  "tasks": [
    {"id": "analysis", "owner": "worker-1", "status": "pending"},
    {"id": "impl", "owner": "worker-2", "status": "pending"},
    {"id": "simplify", "owner": "worker-3", "status": "pending"},
    {"id": "tests", "owner": "worker-4", "status": "pending"}
  ]
}
```

## mprocs Launch

```bash
mprocs --config .hive/mprocs.yaml
```

## Output

- Fix summary, tests run, and remaining risks
