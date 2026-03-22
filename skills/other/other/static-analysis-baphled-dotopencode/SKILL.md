---
name: static-analysis
description: Static code analysis tools and patterns
category: Code Quality
---

# Skill: static-analysis

## What I do

I provide guidance on static code analysis tools and patterns across multiple languages. I help detect bugs, code smells, security vulnerabilities, and style violations without executing code, ensuring issues are caught early in the development cycle.

## When to use me

- Before committing code (pre-commit hooks)
- During code review to automate style/convention checks
- Setting up CI/CD pipelines with quality gates
- Investigating code quality or complexity issues

## Core principles

1. **Fast Feedback** - Run tools that provide immediate results without execution.
2. **Prevent, Don't Detect** - Catch issues locally before they reach the team/repo.
3. **Automate Everything** - Integrate into IDE, pre-commit hooks, and CI pipelines.
4. **Configuration as Code** - Store tool configs (e.g., `.golangci.yml`) in version control.
5. **Progressive Enforcement** - Start with basic rules and gradually tighten them.

## Analysis Categories & Tools

| Category | Purpose | Tools (Go/Ruby/TS) |
|----------|---------|-------------------|
| **Formatting** | Consistent style | `gofmt` / `rubocop` / `prettier` |
| **Linting** | Idioms & conventions | `golangci-lint` / `rubocop` / `eslint` |
| **Bugs** | Logic errors | `staticcheck` / `reek` / `tsc` |
| **Security** | Vulnerabilities | `gosec` / `brakeman` / `npm audit` |
| **Complexity** | Maintainability | `gocyclo` / `flog` / `complexity (eslint)` |
| **Duplication** | DRY violations | `dupl` / `flay` / `jscpd` |

## Integration Patterns

- **IDE:** Real-time feedback and auto-fix on save.
- **Pre-commit:** Local gate preventing commits with lint errors.
- **CI/CD:** Team gate ensuring all merged code meets quality standards.

## Handling False Positives

- **Inline:** Use specific comments (e.g., `//nolint:errcheck`, `# rubocop:disable`) with justification.
- **Exclusion:** Update configuration files to exclude specific files or rules if justified.

## Anti-patterns to avoid

- ❌ **Disabling without understanding** - Learn the rule's purpose before silencing it.
- ❌ **Ignoring legacy violations** - Technical debt grows if not addressed incrementally.
- ❌ **No CI enforcement** - Local checks are easily bypassed or forgotten.
- ❌ **Too many tools** - Overwhelming noise leads to the team ignoring results.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Code-Quality/Static Analysis.md`

## Related skills

- `clean-code` - The standards that static analysis enforces
- `check-compliance` - Running the full suite of checks
- `fix-architecture` - Remediating architectural violations detected
- `security` - Deep-dive security analysis
