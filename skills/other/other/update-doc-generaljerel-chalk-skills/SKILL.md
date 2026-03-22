---
name: update-doc
description: Update an existing doc file in .chalk/docs/ when the user asks to update, edit, or revise documentation
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Edit
argument-hint: "[what to update and how]"
read-only: false
destructive: false
idempotent: true
open-world: false
user-invocable: true
tags: docs, documentation, update
capabilities: docs.update, chalk.docs.update
activation-intents: update doc, revise documentation, edit chalk doc
activation-events: user-prompt
activation-artifacts: .chalk/docs/**
risk-level: low
---

Update an existing documentation file in `.chalk/docs/`.

## Workflow

1. **Find the doc** — Search `.chalk/docs/` for the file matching `$ARGUMENTS`. Match by filename, path, or content. If ambiguous, list candidates and ask the user to clarify.
2. **Read current content** — Load the file to understand what exists.
3. **Apply changes** — Update the content per the user's request. Preserve existing structure and sections where possible. Don't remove content unless explicitly asked.
4. **Update the "Last updated" line** — Set to today's date with a brief change note describing what changed.
5. **Write the file** — Save back to the same path.
6. **Confirm** — Tell the user what was changed and the file path.

## Rules

- **Preserve structure** — Keep existing `#` and `##` headings intact unless the user asks to reorganize.
- **Update, don't rewrite** — Modify the specific sections relevant to the change. Don't rewrite unrelated content.
- **Last updated is required** — Always update the date line. Format: `Last updated: YYYY-MM-DD (<brief change note>)`.
- **No frontmatter** — Docs are plain markdown. Don't add YAML frontmatter.
- **Respect the vertical's tone** — Product docs are business-facing, AI docs are agent-facing reference-style, Engineering docs are technical and comprehensive.

## Finding Docs

Search strategies in order of preference:

1. **Exact path** — If the user provides a path like "ai/0_AI_PROFILE.md", use it directly.
2. **Filename match** — Glob for `**/[slug]*.md` in `.chalk/docs/`.
3. **Content search** — Grep for keywords in `.chalk/docs/**/*.md`.
4. **Vertical + topic** — If the user says "the engineering architecture doc", search `engineering/` for architecture-related filenames.
