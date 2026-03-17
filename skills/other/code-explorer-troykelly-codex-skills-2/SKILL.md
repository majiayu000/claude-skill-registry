---
name: code-explorer
description: Use when asked to trace existing codepaths or explicitly asked to run the code-explorer subagent.
---

# Code Explorer Subagent

Use the `code-explorer` agent card to handle this specialized task.

## Run

```bash
codex-subagent code-explorer <<'EOF'
[Provide the task context, scope, and any issue/PR numbers.]
EOF
```

## Notes

- Include concrete scope and constraints in the context block.
- Fold the subagent output back into the main workflow.
