---
name: code-simplifier
description: Use when asked to simplify recently changed code without changing behavior or explicitly asked to run the code-simplifier subagent.
---

# Code Simplifier Subagent

Use the `code-simplifier` agent card to handle this specialized task.

## Run

```bash
codex-subagent code-simplifier <<'EOF'
[Provide the task context, scope, and any issue/PR numbers.]
EOF
```

## Notes

- Include concrete scope and constraints in the context block.
- Fold the subagent output back into the main workflow.
