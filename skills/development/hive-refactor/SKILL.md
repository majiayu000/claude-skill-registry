---
name: hive-refactor
description: Perform a large-scale refactor with staged work and validation; use when changes span many files or modules.
---

# Hive Refactor

## Overview

Use mprocs to coordinate a staged refactor across multiple workers.

## Inputs

- Refactor goal and scope

## Workflow

1. Verify `git` and `mprocs` are available.
2. Create `.hive/sessions/<session-id>`.
3. Write `tasks.json` with staged refactor tasks.
4. Write queen and worker prompts (analysis, implementation, tests, docs).
5. Launch mprocs.

## tasks.json Template

```json
{
  "session": "{SESSION_ID}",
  "created": "{ISO_TIMESTAMP}",
  "status": "active",
  "thread_type": "Hive",
  "task_type": "hive-refactor",
  "tasks": [
    {"id": "analysis", "owner": "queen", "status": "pending"},
    {"id": "impl-1", "owner": "worker-1", "status": "pending"},
    {"id": "impl-2", "owner": "worker-2", "status": "pending"},
    {"id": "tests", "owner": "worker-3", "status": "pending"}
  ]
}
```

## mprocs Launch

```bash
mprocs --config .hive/mprocs.yaml
```

## Output

- Refactor plan, changes, and validation status
