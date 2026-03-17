---
name: code-architect
description: Use when asked for an architecture blueprint or explicitly asked to run the code-architect subagent.
---

# Code Architect Subagent

Use the `code-architect` agent card to handle this specialized task.

## Run

```bash
codex-subagent code-architect <<'EOF'
[Provide the task context, scope, and any issue/PR numbers.]
EOF
```

## Notes

- Include concrete scope and constraints in the context block.
- Fold the subagent output back into the main workflow.
