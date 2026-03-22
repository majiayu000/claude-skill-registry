---
name: justdoit
description: "Manage tasks via the `justdoit` CLI (Google Tasks + Calendar): next view, list, search, complete/undo, and common workflows."
---

# justdoit CLI

`justdoit` is a CLI for Google Tasks + Calendar. This guide covers the most useful commands and flags so you can work without constantly checking `--help`.

## Daily view (Next)

- Show the "Next" view (overdue/today/this week/next week/backlog):
  - `justdoit next`
  - `justdoit next --ids`
  - `justdoit next --backlog=false` (hide backlog)

## List/search

- List by list/section:
  - `justdoit list --list <List>`
  - `justdoit list --list <List> --section <Section>`
  - `justdoit list --list <List> --section <Section> --all`

- Show IDs:
  - `justdoit list --list <List> --section <Section> --ids`
  - `justdoit search "<query>" --list <List> --ids`

## Complete / Undo

- Complete by ID:
  - `justdoit done <taskID> --list <List>`

- Complete by exact title (optional section):
  - `justdoit done --list <List> --title "<Exact title>" --section <Section>`

- Undo completion:
  - `justdoit undo <taskID> --list <List>`
  - `justdoit undo --list <List> --title "<Exact title>" --section <Section>`

## Tips

- Use `--ids` when you plan to complete or undo by ID.
- Use `--all` to include completed items where supported.
