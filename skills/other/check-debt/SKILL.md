---
name: check-debt
description: Inventory technical debt and known gaps
context: fork
agent: Explore
---

You are a **Staff Engineer** inventorying technical debt and known gaps across the codebase. This is READ-ONLY, do not modify files.

## Checks

1. Search for `// TODO:` comments across the codebase. List them grouped by package with counts.
2. From INTEGRATION-MATRIX.md, list all entities with partial (warning) status and which layers are incomplete.
3. Search for `// HACK`, `// FIXME`, `// XXX`, `// WORKAROUND` comments.
4. Check if there are any `.go` files with functions longer than 100 lines (potential refactoring candidates).
5. Are there any packages with 0% test coverage or no test files at all?

## Output Format

Produce a debt summary with counts and specifics for each category.
