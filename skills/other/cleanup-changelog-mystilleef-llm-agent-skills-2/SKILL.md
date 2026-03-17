---
name: cleanup-changelog
description: Format changelog and remove empty sections.
---

# Cleanup changelog

**`GOAL`**: fix formatting and remove empty sections in `CHANGELOG.md`.

**`WHEN`**: after generating or updating the changelog.

## Efficiency directives

- Optimize all operations for token and context efficiency
- Batch operations on file groups, avoid individual file processing
- Target only relevant files
- Reduce token usage

## Workflow

- Invoke the `fix-markdown` skill on `CHANGELOG.md`
- Run `scripts/remove-empty-headers.sh CHANGELOG.md`
- Invoke the `fix-markdown` skill on `CHANGELOG.md` again
- **`DONE`**

## Output

**Files modified:**

- `CHANGELOG.md` - Formatted and cleaned

**Status communication:**

- `SUCCESS` - Cleanup completed
- `ERROR` - Operation failed
