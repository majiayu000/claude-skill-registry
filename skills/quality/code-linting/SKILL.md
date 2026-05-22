---
name: code-linting
description: Run linters according to repository guidelines. Use immediately after creating or modifying code, or before committing changes.
---

# Code Linting

Run all appropriate linters according to repository guidelines.

## When to Use This Skill

Use this skill:
- Immediately after creating new source code files
- Immediately after modifying existing code (functions, classes, imports, etc.)
- Immediately after completing a feature, refactor, or bug fix
- Before staging files for commit
- When build/compilation succeeds but linting hasn't been checked
- Proactively, whenever code changes are made

**Don't use:**
- When you've already run linting and it passed

## Linter Discovery

First look for linting commands in the following order:

1. Directives to AI agents (`CLAUDE.md`, `.cursorrules`, `.ai-rules`,
   `AGENTS.md`, `AGENT.md`, `GEMINI.md`, and similar)
2. Repository documentation (`README.md`, `docs/`, etc.)
3. Package configuration (`package.json`, `Makefile`, `pyproject.toml`, etc.)
4. Standard linter patterns for the project type

If no linting guidelines are found or they are unclear, ask the user
for clarification.

## Common Linter Commands

```bash
# JavaScript/TypeScript
npm run lint
yarn run lint
pnpm run lint
npx eslint .

# Python
ruff check .
pylint .
flake8 .
black --check .
make lint

# Shell
shellcheck .

# Multiple/Generic
npm run format
yarn run format
pnpm run format
```

## Linting Process

For each linter found:

1. If it has an auto-fix mode (e.g., `prettier`, `eslint --fix`, `black`, `ruff check --fix`), run that first
2. Run the linter in check mode to see if there are any remaining issues
3. If issues can't be fixed automatically, report them clearly

## Important Rules

**CRITICAL: Do NOT ignore unfixed issues!**

- All linting issues MUST be resolved before considering the task complete
- The only exception is if the user explicitly gives permission to defer resolution
- Document any issues that couldn't be auto-fixed for the user to review

## Output

Report results organized by:

1. **Auto-fixed issues**: What was automatically corrected
2. **Remaining issues**: Issues requiring manual attention (list each with file, line, and description)
3. **Recommendation**: What the developer should do next

If all linting passes, simply confirm: "All linters passed."
