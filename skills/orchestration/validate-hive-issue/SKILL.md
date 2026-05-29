---
name: validate-hive-issue
description: Validate a GitHub issue with deeper cross-checking and risk assessment; use for high-impact issues.
---

# Validate Hive Issue

## Overview

Use mprocs to validate an issue with multiple workers and a queen synthesis.

## Inputs

- Issue text or link

## Workflow

1. Verify `git` and `mprocs`.
2. Create `.hive/sessions/<session-id>` and `tasks.json`.
3. Write queen and worker prompts (repro check, code scan, risk analysis).
4. Launch mprocs.

## tasks.json Template

```json
{
  "session": "{SESSION_ID}",
  "created": "{ISO_TIMESTAMP}",
  "status": "active",
  "thread_type": "Hive",
  "task_type": "validate-hive-issue",
  "issue": {"text": "{ISSUE_TEXT}"}
}
```

## mprocs Launch

```bash
mprocs --config .hive/mprocs.yaml
```

## Output

- Validation report with evidence and risk notes
