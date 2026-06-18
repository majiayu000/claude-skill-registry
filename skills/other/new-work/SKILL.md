---
name: new-work
description: "Create and manage todo tracking documents for features, bugs, and multi-step tasks. Use when starting new work that benefits from a persistent record of decisions, progress, and context."
disable-model-invocation: true
metadata:
  author: Garrick Aden-Buie (@gadenbuie)
  version: "1.0"
license: MIT
---

# New Work

Todo notes track work items as markdown files with YAML front matter capturing status, context, and progress.

## Storage Location

Use `_dev/todos/` if it exists in the repository root; otherwise ask the user where to store todo notes before creating anything. It contains two subdirectories: `pending/` (active) and `done/` (finished).

## File Naming

`YYYY-MM-DD_short-kebab-slug.md`, e.g. `2026-02-18_add-oauth-support.md`.

## File Contents

YAML front matter plus a markdown body. Only `status` is required.

```markdown
---
status: pending   # pending | in progress | review | blocked | done
issue: https://github.com/org/repo/issues/123   # optional
pr: https://github.com/org/repo/pull/456        # optional
---

# Title

Overview of what this is about and why it matters.

## Key Files

- `src/relevant-file.ts` — what it does
- `src/other-file.ts:functionName()` — why it matters

## Work Items

- [ ] First thing to do
- [ ] Second thing to do

## Design Decisions

Context, constraints, or choices worth capturing.

## Decision Log

<!--
### YYYY-MM-DD — Short Decision Title
**Decision:** What was decided?
**Rationale:** Why?
-->
```

## Lifecycle

- **Create:** make `pending/` if needed, create the date-prefixed file with `status: pending`, and write enough context to resume later.
- **In progress:** update `status`; add `issue`/`pr` links when they exist; check off Work Items (`- [ ]` → `- [x]`); record significant decisions in the Decision Log.
- **Complete:** set `status: done` and `mv` the file from `pending/` to `done/`.

## Keeping the Document Current

Treat the todo as a living record for the rest of the session. Update it after any decision, newly discovered problem or requirement, issue raised/resolved, significant implementation work, or commit. When in doubt, update it.

When you form a plan — whether in response to a user request or on your own initiative — write it to the todo document rather than presenting it only in chat. The document is the persistent record; the chat is not.

To resume in a future session, use `/working-on <path-to-todo>` — same live-document behavior without re-creating the file.