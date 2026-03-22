---
name: check-compliance
description: Run full compliance checks before and after changes
category: Code Quality
---

# Skill: check-compliance

## What I do

I ensure all code changes meet project standards for quality, security, and licensing before they reach the repository. I enforce a "verify before you commit" discipline that prevents broken builds and security regressions.

## When to use me

- Before staging changes for a new commit
- After finishing a feature or bug fix to verify integration
- When a pre-commit hook fails and requires manual investigation
- To ensure local environments match CI/CD gate requirements

## Core principles

1. **Local verification first** — Never rely on CI to catch basic formatting or linting errors.
2. **Comprehensive coverage** — Checks must include linting, formatting, unit tests, and security scans.
3. **Fail fast** — Stop the commit process immediately if any check fails.
4. **No bypass** — Avoid --no-verify unless in an extreme emergency with stakeholder approval.

## Patterns & examples

**Compliance check sequence:**
1. **Linting**: Static analysis to catch syntax and logic errors (e.g. eslint, golangci-lint).
2. **Formatting**: Ensure consistent code style (e.g. prettier, gofmt).
3. **Security**: Scan for secrets and vulnerable dependencies (e.g. gitleaks, npm audit).
4. **Testing**: Run the local test suite to ensure no regressions.

**Standard Makefile implementation:**
```makefile
check-compliance:
	@echo "Running compliance checks..."
	@npm run lint
	@npm run format:check
	@npm test
	@gitleaks detect --source .
```

**Pre-commit hook configuration (.pre-commit-config.yaml):**
```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
-   repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
    -   id: gitleaks
```

## Anti-patterns to avoid

- ❌ **Committing with failures** — Fixing "later" leads to broken main branches and technical debt.
- ❌ **Inconsistent local/CI checks** — If it passes locally but fails in CI, the local checks are incomplete.
- ❌ **Manual-only checks** — If checks aren't automated via a command or hook, they won't be run consistently.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Code-Quality/Check Compliance.md`

## Related skills

- `static-analysis` — Deep analysis of code quality and logic
- `dependency-management` — Scanning for vulnerable third-party packages
- `security` — Secure coding practices and input validation
- `bdd-workflow` — Running behavioural tests as part of compliance
