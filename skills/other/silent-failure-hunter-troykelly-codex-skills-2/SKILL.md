---
name: silent-failure-hunter
description: Use when asked to detect silent failures/weak error handling or explicitly asked to run the silent-failure-hunter subagent.
---

# Silent Failure Hunter Subagent

Use the `silent-failure-hunter` agent card to handle this specialized task.

## Run

```bash
codex-subagent silent-failure-hunter <<'EOF'
[Provide the task context, scope, and any issue/PR numbers.]
EOF
```

## Notes

- Include concrete scope and constraints in the context block.
- Fold the subagent output back into the main workflow.
