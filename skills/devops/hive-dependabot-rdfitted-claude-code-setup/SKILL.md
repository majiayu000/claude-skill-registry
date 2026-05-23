---
name: hive-dependabot
description: Triage and resolve multiple Dependabot updates in batch; use when there are many dependency PRs.
---

# Hive Dependabot

## Overview

Use mprocs to coordinate a queen and workers to resolve multiple Dependabot updates.

## Inputs

- List of Dependabot PRs or update descriptions

## Workflow

1. Verify `git` and `mprocs` are available.
2. Create `.hive/sessions/<session-id>`.
3. Write `tasks.json` with one task per PR.
4. Write queen and worker prompts focused on dependency updates.
5. Launch mprocs.

## tasks.json Template

```json
{
  "session": "{SESSION_ID}",
  "created": "{ISO_TIMESTAMP}",
  "status": "active",
  "thread_type": "Hive",
  "task_type": "hive-dependabot",
  "prs": ["{PR_1}", "{PR_2}"]
}
```

## Worker Prompt Outline

```markdown
# Worker - Dependabot Update
- Apply dependency bump
- Regenerate lockfiles
- Fix conflicts
- Run tests
- Report results
```

## mprocs Launch

```bash
mprocs --config .hive/mprocs.yaml
```

## Output

- Per-PR update summaries and test results
