---
name: sheet-git
description: Spreadsheet repo control and hosted review/origin collaboration for persisted `agent-sheet` workspaces. Use when needs to stage workbook entries, create commits or proposals, inspect proposal state, publish a proposal to hosted review, pull machine-readable review comments, or coordinate `push/fetch/pull/rebase` against origin. Do not use it for direct workbook editing.
metadata:
  openclaw:
    os:
      - linux
      - macos
    requires:
      bins:
        - sheet-git
        - agent-sheet
    install:
      - kind: none
    links:
      repository: https://github.com/dream-num/skills
      documentation: https://github.com/dream-num/skills
---

# sheet-git

`sheet-git` is the repo, review, and origin control plane that sits beside `agent-sheet`.

Use `agent-sheet` to create, edit, attach, and persist workbook content.
Use `sheet-git` when the task becomes:

- capturing persisted local workbook changes into repo history
- creating and tracking proposals
- handing proposals to hosted review
- pulling machine-readable review feedback
- materializing reviewed changes to origin
- recovering collaborative drift with `fetch`, `pull`, and `rebase`

## Hard boundaries

- Operate on persisted local entry files only.
- Start from `agent-sheet` if the workbook content itself still needs to change.
- Treat `push review` as handoff only. It publishes to hosted review; it does not approve.
- Treat `proposal comments` as the agent-facing review surface. It returns JSON packets.
- Treat `push origin` as the real origin materialization step.
- Treat hosted web `Merge` as review closure plus a materialization handoff. Alice may still need `sheet-git push origin <proposal>` unless a daemon claims the request.
- Follow refusal output literally. `pull origin`, `push origin`, and `rebase origin` already emit the next safe command when collaboration state is blocked.

## First path

1. Verify workbook edits are already persisted with `agent-sheet`.
2. Run `sheet-git status`.
3. Stage with `sheet-git stage --entry-id <id>` or `sheet-git stage --all`.
4. Inspect with `sheet-git diff`.
5. Commit with `sheet-git commit --message "..."`.
6. Create a proposal with `sheet-git proposal create`.

If the task is already in review or origin sync, do not guess. Read the current state first:

- `sheet-git proposal status <proposal>`
- `sheet-git proposal comments <proposal>`
- `sheet-git fetch origin <entry-id>`

## Highest-signal playbooks

### Local capture

- `sheet-git init`
- `sheet-git stage --entry-id <id>` or `sheet-git stage --all`
- `sheet-git commit --message "..."`
- `sheet-git proposal create`

### Publish to Bob

- `sheet-git push review <proposal>`
- Bob sees the same proposal in hosted inbox as `needs-review`
- follow-up local commits should be republished through the same proposal id, not a new proposal

Read [references/hosted-review.md](references/hosted-review.md) when the task involves Alice/Bob handoff, follow-up revisions, or materialization waiting state.

### Pull review feedback

- `sheet-git proposal comments <proposal>`
- default output is JSON review packet
- selection-based comments may include `selectionAttachment`
- revise locally, commit again, then `sheet-git push review <same proposal>`

### Materialize to origin

- `sheet-git push origin --dry-run <proposal>`
- `sheet-git push origin --explain <proposal>`
- `sheet-git push origin <proposal>`
- `sheet-git pull origin <proposal-or-entry-id>`
- `sheet-git fetch origin <entry-id>`
- `sheet-git rebase origin <entry-id>`

Read [references/recovery.md](references/recovery.md) when `pull`, `push`, or `rebase` refuses and emits a next step.

## Quick routes

| Task | Command |
|---|---|
| initialize repo | `sheet-git init` |
| stage one workbook | `sheet-git stage --entry-id <id>` |
| stage all capturable workbooks | `sheet-git stage --all` |
| inspect repo state | `sheet-git status` |
| inspect staged or commit diff | `sheet-git diff` |
| create commit | `sheet-git commit --message "..."` |
| create proposal | `sheet-git proposal create` |
| list proposals | `sheet-git proposal list` |
| inspect one proposal | `sheet-git proposal show <proposal>` |
| inspect proposal review/origin state | `sheet-git proposal status <proposal>` |
| publish to hosted review | `sheet-git push review <proposal>` |
| pull machine-readable review comments | `sheet-git proposal comments <proposal>` |
| approve from CLI | `sheet-git proposal approve <proposal> [--actor <name>]` |
| preview origin materialization | `sheet-git push origin --dry-run <proposal>` |
| explain origin blockers | `sheet-git push origin --explain <proposal>` |
| materialize to origin | `sheet-git push origin <proposal>` |
| resume a merge run | `sheet-git push origin --resume <merge-run>` |
| materialize remote changes locally | `sheet-git pull origin <proposal-or-entry-id>` |
| force local materialization repair | `sheet-git pull origin --force-to-latest <proposal-or-entry-id>` |
| see remote-ahead state | `sheet-git fetch origin <entry-id>` |
| rebase local work on remote | `sheet-git rebase origin <entry-id>` |
| blame one cell | `sheet-git blame --entry-id <id> --cell 'Sheet1!A1' [<commit>]` |
| inspect history | `sheet-git history [--limit <n>]` |
| inspect one revision | `sheet-git show [<commit>]` |

For exact command semantics and output expectations, read [references/command-surface.md](references/command-surface.md).

## Output discipline

- Prefer `status` or `proposal status` before making claims.
- Treat semantic summaries as the default review surface.
- Drop to raw cell diff or blame only when the summary is not enough.
- When reporting a blocked state, include the exact refusal text and the suggested next command.
