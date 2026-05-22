---
name: lint
description: Linting workflow rules for this workspace.
---

# Lint Skill

Use this skill when handling lint errors or running eslint.

## Linting

- When encountering lint errors, automatically fix them using `eslint --fix`
  before making manual changes.
- Run `eslint --fix` on the affected file(s) to resolve auto-fixable lint
  issues.
- If `eslint --fix` cannot solve a lint error, LEAVE IT TO ME. Do not attempt to
  manually fix it.
- NEVER use ESLint disable comments (e.g., `eslint-disable-next-line`,
  `eslint-disable`, etc.). Leave lint errors for the user to fix.
