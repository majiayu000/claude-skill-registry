---
name: type-design-analyzer
description: Use when asked to evaluate type design/invariants or explicitly asked to run the type-design-analyzer subagent.
---

# Type Design Analyzer Subagent

Use the `type-design-analyzer` agent card to handle this specialized task.

## Run

```bash
codex-subagent type-design-analyzer <<'EOF'
[Provide the task context, scope, and any issue/PR numbers.]
EOF
```

## Notes

- Include concrete scope and constraints in the context block.
- Fold the subagent output back into the main workflow.
