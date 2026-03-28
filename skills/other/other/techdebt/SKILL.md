---
name: phx:techdebt
description: Analyze Elixir/Phoenix project for technical debt, duplicate code, and refactoring opportunities. Use when the user mentions code quality concerns, cleanup, refactor, credo issues, or asks about what to improve. Also use before major feature work to identify areas that need attention first.
effort: medium
---

# Technical Debt Detection

Find and eliminate duplicate code patterns, anti-patterns, and refactoring opportunities in Elixir/Phoenix projects.

## Iron Laws - Never Violate These

1. **Search before refactoring** - Understand full scope of duplication before extracting
2. **Three strikes rule** - Extract shared code only after 3+ duplications
3. **Prefer composition** - Use behaviours and protocols over inheritance-style abstractions
4. **Test coverage first** - Ensure tests exist before refactoring duplicated code

## Analysis Checklist

### 1. Run Credo for Automated Detection

```bash
mix credo --strict
```

Focus on:

- Design issues (duplication, complexity)
- Consistency issues (naming, patterns)
- Refactoring opportunities

### 2. Find Duplicate Ecto Query Patterns

```bash
# Repeated Repo calls
grep -r "Repo.get!\|Repo.get\|Repo.one" lib/ --include="*.ex"

# Duplicate query patterns
grep -r "from.*in.*where" lib/ --include="*.ex"
```

### 3. Find Duplicate Validation Logic

```bash
# Changeset patterns
grep -r "def changeset" lib/ --include="*.ex" | wc -l

# Repeated validations
grep -r "validate_required\|validate_format" lib/ --include="*.ex"
```

### 4. Find Copy-Pasted Controller Actions

```bash
# Similar action patterns
grep -r "def create\|def update\|def delete" lib/*_web/ --include="*.ex"
```

## Common Duplication Patterns

| Pattern | Symptom | Solution |
|---------|---------|----------|
| Repeated queries | Same `Repo.get` in multiple contexts | Create shared query module |
| Duplicate validations | Same `validate_*` calls | Extract to shared changeset |
| Similar controllers | Copy-pasted CRUD actions | Use Phoenix generators consistently |
| Repeated transforms | Same `Enum.map` patterns | Extract to domain module |

## Reporting Format

For each duplication found, report:

1. **Location**: File paths and line numbers
2. **Pattern**: What code is duplicated
3. **Extraction**: Suggested shared function/module
4. **Effort**: Low/Medium/High to fix

## Usage

Run `/phx:techdebt` to analyze the codebase and generate a prioritized report of technical debt with specific remediation steps.
