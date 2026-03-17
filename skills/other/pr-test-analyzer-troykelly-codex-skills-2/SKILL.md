---
name: pr-test-analyzer
description: Use when asked to evaluate PR test coverage or explicitly asked to run the pr-test-analyzer subagent.
---

# Pr Test Analyzer Subagent

Use the `pr-test-analyzer` agent card to handle this specialized task.

## Run

```bash
codex-subagent pr-test-analyzer <<'EOF'
[Provide the task context, scope, and any issue/PR numbers.]
EOF
```

## Notes

- Include concrete scope and constraints in the context block.
- Fold the subagent output back into the main workflow.
