---
name: commit
description:
  MUST invoke before creating any git commit. Provides commit message format and
  safety rules.
---

# Message guideline

## Title format

Use "component: Brief summary" format for the commit title.

Examples:

- "completions: Add support for keyword argument completion"
- "diagnostics: Fix false positive on unused variable"
- "ci: Update GitHub Actions workflow"

## Body

Provide a brief prose summary of the purpose of the changes made. Use backticks
for code elements (function names, variables, file paths, etc.).

## Line length

Ensure the maximum line length never exceeds 72 characters.

## GitHub references

When referencing external GitHub PRs or issues, use proper GitHub interlinking
format: "owner/repo#123"

## Footer

If you wrote code yourself, include a "Written by Claude" footer at the end of
the commit message. No emoji.

However, when simply asked to write a commit message (without having written the
code), there's no need to add that footer.

## Example

```
search: Cancel pending requests when UI components close

Add `SearchManager.cancelPendingRequests()` to allow components to
cancel their queued search requests when being destroyed. Apply this
to both `SemanticNoteFinder` and `RelatedNotesView` to prevent
unnecessary embedding requests after modals/views are closed.

Also extract `COMPONENT_ID` constants for consistent component
identification.
```

# Safety guideline

See the
["Git operations" section in CLAUDE.md](../../../CLAUDE.md#git-operations).
