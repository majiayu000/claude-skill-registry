---
name: phx:techdebt
description: Analyze Elixir/Phoenix technical debt — duplicates, refactoring opportunities, credo issues. Use when asked about code quality, cleanup, or what to improve.
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

Run `mix credo --strict`.

Focus on:

- Design issues (duplication, complexity)
- Consistency issues (naming, patterns)
- Refactoring opportunities

### 2. Find Duplicate Ecto Query Patterns

Use Grep to search for repeated Repo calls (`Repo.get!`, `Repo.get`, `Repo.one`) in `lib/**/*.ex`.
Use Grep to find duplicate query patterns (`from.*in.*where`) in `lib/**/*.ex`.

### 3. Find Duplicate Validation Logic

Use Grep with `output_mode: "count"` to count `def changeset` occurrences in `lib/**/*.ex`.
Use Grep to find repeated validations (`validate_required`, `validate_format`) in `lib/**/*.ex`.

### 4. Find Copy-Pasted Controller Actions

Use Grep to find similar action patterns (`def create`, `def update`, `def delete`) in `lib/*_web/**/*.ex`.

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
