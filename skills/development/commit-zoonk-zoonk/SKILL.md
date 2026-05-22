---
name: commit
description: Guidelines for writing commit messages and PR descriptions
---

# Commit Messages

## Format

```
type(scope): short message
```

## Types

- `feat` - new feature
- `fix` - bug fix
- `refactor` - code refactoring
- `chore` - maintenance tasks (deps, config, tooling)

## Scopes

Always use the app or package name as scope:

**Apps**: `admin`, `auth`, `editor`, `evals`, `main`

**Packages**: `ai`, `auth`, `core`, `db`, `e2e`, `error-reporter`, `mailer`, `next`, `testing`, `tsconfig`, `ui`, `utils`

**Inferred scopes** (when change doesn't fit an app/package):

- `agents` - CLAUDE.md, AGENTS.md, `.claude/` folder
- `ci` - GitHub workflows, CI/CD configuration
- `deps` - dependency updates across multiple packages
- `data` - data layer changes spanning multiple packages

## Examples

```
feat(main): add lesson page
fix(editor): always use custom lesson kind
refactor(db): use enum for step kind
chore(deps): update vercel ai sdk
chore(agents): add commit skill
fix(ci): update node version in workflow
```

## Rules

- Use lowercase for entire message
- No period at the end
- Keep message under 72 characters
- Use imperative mood ("add" not "added")

## Author

Always set the AI agent as the commit author:

```bash
git commit -m "feat(main): add lesson page" --author="Claude Opus 4.5 <noreply@anthropic.com>"
```

# PR Descriptions

Keep descriptions brief. Focus on what changed. No need to list verification commands run.
