---
name: changelog-observer
description: Track development session events in a daily markdown changelog, including file changes, test results, and key decisions.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
user-invocable: true
---

# Changelog Observer

Track session context in `.changelog/session-YYYY-MM-DD.md`.

## Log target

- Use `.changelog/session-YYYY-MM-DD.md` for the current local date.
- Create `.changelog/` and the session file if they do not exist.
- If the session file is new, initialize it from [template.md](template.md).
- Append new entries in chronological order.

## What to log

- `file-change`: after creating, editing, or deleting project files.
- `test-result`: after running tests, checks, or validation commands.
- `decision`: after making an implementation or architecture decision worth preserving.

## Entry rules

- Keep each description short and specific.
- List only directly affected files.
- Use `none` when no files were changed.
- Do not rewrite earlier entries unless they are incorrect.

## Template

Use the markdown structure in [template.md](template.md) for each appended entry.
