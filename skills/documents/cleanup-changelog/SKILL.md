---
name: cleanup-changelog
description:
  Use the `fix-markdown` skill to clean up CHANGELOG.md, then remove
  headers with empty sections. Use after the agent has finished
  generating or updating the changelog.
---

# Cleanup changelog

**`GOAL`**: fix lint, formatting, and prose issues in `CHANGELOG.md`.

**`WHEN`**: use after the agent has finished generating or updating the
changelog.

## Remove empty headers script

Run the `scripts/remove-empty-headers.sh` script against `CHANGELOG.md`
to remove headers with empty sections.

## Workflow

- Use the `fix-markdown` skill to fix `CHANGELOG.md`
- Run the script to remove headers with empty sections in `CHANGELOG.md`
- Run `fix-markdown` skill again to ensure proper formatting
- **`DONE`**
