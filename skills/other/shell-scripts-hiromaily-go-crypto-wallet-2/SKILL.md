---
name: shell-scripts
description: Shell script development workflow. Use when modifying files in scripts/ directory or any *.sh files.
---

# Shell Scripts Workflow

Workflow for shell script changes.

## Prerequisites

- **Use `git-workflow` Skill** for branch, commit, and PR workflow.
- **Refer to `.claude/rules/shell-script.md`** for detailed best practices (SSOT).

## Applicable Files

| Path | Description |
|------|-------------|
| `scripts/` | All shell scripts |
| `*.sh` | Shell scripts anywhere |

## Workflow

### 1. Make Changes

Edit shell scripts following the rules in `.claude/rules/shell-script.md`.

### 2. Verify (from rules/shell-script.md)

```bash
make shfmt
shellcheck scripts/{script}.sh  # if installed
```

### 3. Self-Review Checklist

- [ ] Script is executable (`chmod +x`)
- [ ] Has shebang line (`#!/usr/bin/env bash`)
- [ ] Uses strict mode (`set -euo pipefail`)
- [ ] Variables are quoted
- [ ] All comments and messages are in English

## Related

- `.claude/rules/shell-script.md` - Shell rules (SSOT)
- `git-workflow` - Branch, commit, PR workflow
