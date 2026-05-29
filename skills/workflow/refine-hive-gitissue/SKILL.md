---
name: refine-hive-gitissue
description: Refine a GitHub issue with extra validation and triage detail; use for high-impact issues or cross-team work.
---

# Refine Hive Git Issue

## Overview

Use mprocs to refine an existing issue with validation and triage details.

## Inputs

- Issue text or link

## Workflow

1. Verify `git` and `mprocs`.
2. Create `.hive/sessions/<session-id>` and `tasks.json`.
3. Write queen and worker prompts (validation, rewrite, triage).
4. Launch mprocs.

## tasks.json Template

```json
{
  "session": "{SESSION_ID}",
  "created": "{ISO_TIMESTAMP}",
  "status": "active",
  "thread_type": "Hive",
  "task_type": "refine-hive-gitissue",
  "issue": {"text": "{ISSUE_TEXT}"}
}
```

## mprocs Launch

```bash
mprocs --config .hive/mprocs.yaml
```

## Output

- Refined issue with validation notes and recommended labels
