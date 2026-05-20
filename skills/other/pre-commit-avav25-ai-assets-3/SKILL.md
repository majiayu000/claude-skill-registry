---
name: pre-commit
description: Run the repository's quality gate before commit or PR by determining the relevant build, lint, and test commands and fixing obvious issues.
---

# Pre-commit

## Workflow

1. Read `AGENTS.md`, `TESTING.md`, and relevant service config.
2. Determine lint, build, and test commands for the changed area.
3. Run targeted checks first, then broader checks if needed.
4. Fix obvious failures and rerun.
5. Report what passed, what failed, and any remaining risk.