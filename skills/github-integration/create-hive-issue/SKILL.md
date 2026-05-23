---
name: create-hive-issue
description: Create a GitHub issue with extra review and triage detail; use when a thorough or multi-perspective issue write-up is needed.
---

# Create Hive Issue

## Overview

Use mprocs to coordinate multiple workers for a deep issue write-up.

## Inputs

- Issue description

## Workflow

1. Verify `git` and `mprocs`.
2. Create `.hive/sessions/<session-id>` and `tasks.json`.
3. Write queen and worker prompts (scout, analysis, draft).
4. Launch mprocs and synthesize a final issue.

## tasks.json Template

```json
{
  "session": "{SESSION_ID}",
  "created": "{ISO_TIMESTAMP}",
  "status": "active",
  "thread_type": "Hive",
  "task_type": "create-hive-issue",
  "issue": {"description": "{ISSUE_DESC}"},
  "tasks": [
    {"id": "scout", "owner": "worker-1", "status": "pending"},
    {"id": "analysis", "owner": "worker-2", "status": "pending"},
    {"id": "draft", "owner": "worker-3", "status": "pending"}
  ]
}
```

## Worker Prompt Outline

```markdown
# Worker - Issue Scout
- Locate relevant files
- Summarize evidence

# Worker - Issue Analysis
- Identify scope and risks

# Worker - Issue Draft
- Write title and body
```

## mprocs Launch

```bash
mprocs --config .hive/mprocs.yaml
```

## Output

- Detailed GitHub issue with triage notes
