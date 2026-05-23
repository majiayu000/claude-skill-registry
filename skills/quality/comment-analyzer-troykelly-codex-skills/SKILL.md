---
name: comment-analyzer
description: Use when asked to review code comments for accuracy/quality or explicitly asked to run the comment-analyzer subagent.
---

# Comment Analyzer Subagent

Use the `comment-analyzer` agent card to handle this specialized task.

## Run

```bash
codex-subagent comment-analyzer <<'EOF'
[Provide the task context, scope, and any issue/PR numbers.]
EOF
```

## Notes

- Include concrete scope and constraints in the context block.
- Fold the subagent output back into the main workflow.
