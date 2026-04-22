---
name: sheet-git
description: Use when a persisted `agent-sheet` workspace needs versioning, review-session workflow, or hosted/origin sync through `sheet-git`, rather than direct workbook editing.
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

`sheet-git` is the Git-like control plane for persisted `agent-sheet` workspaces.

Use `agent-sheet` to create or edit workbook content. Use `sheet-git` after the workbook changes are already persisted and the task becomes versioning, review, or sync.

## Use when

- capturing persisted workbook changes into repo history
- inspecting repo state, diff, history, or blame
- creating or updating a review session
- publishing a review session to hosted review
- reading machine-readable review feedback
- syncing local state with origin

## Do not use when

- the workbook still needs to be edited, attached, or persisted
- the task is only about `agent-sheet` authoring workflows
- you are about to invent Git-like commands that are not in the real command surface

## Core model

- local history is commit-based
- local history is `commit`
- local review attempt is `review session`
- hosted thread reuse is decided by `push review`
- local durable truth is only `review session`
- there is no local `approve` command
- hosted review is separate from origin materialization
- recovery goes through the existing `fetch` / `pull` / `push origin --resume` surface
- `rebase origin` is not part of the current command surface

## Default flow

1. Ensure workbook edits are already persisted in `agent-sheet`.
2. Run `sheet-git status`.
3. Stage with `sheet-git stage --entry-id <id>` or `sheet-git stage --all`.
4. Inspect with `sheet-git diff`.
5. Commit with `sheet-git commit --message "..."`.
6. Create a review session with `sheet-git review create`.

## Common routes

### Start from an existing hosted repo

- `sheet-git clone <owner>/<repo> --base-url <base-url>`
- `sheet-git clone <host>/<owner>/<repo>`
- `sheet-git clone <review-url>`

Here `{owner}/{repo}` is the hosted review scope for this scenario. It does not need to be pre-created; if the scenario has no existing scope yet, choose stable values and reuse them consistently.

### Publish for review

- `sheet-git push review <session>`

### Read review feedback

- `sheet-git review status <session>`
- `sheet-git review comments <session>`

### Sync with origin

- `sheet-git fetch origin <entry-id>`
- `sheet-git pull origin <session-or-entry-id>`
- `sheet-git push origin <session>`
- `sheet-git push origin --skip-review-check <session>`
- `sheet-git push origin --resume <replay-run>`

By default, `sheet-git push origin <session>` checks hosted approval before replaying. Use `--skip-review-check` only when you need the explicit bypass path.

Follow refusal output literally. If `sheet-git` tells you the next safe command, use that instead of improvising.

## Primary commands

| Task | Command |
|---|---|
| initialize repo | `sheet-git init` |
| bind hosted review scope | `sheet-git remote add review [<base-url>] --owner <owner-id> --repo <repo-id>` |
| inspect state | `sheet-git status` |
| inspect diff | `sheet-git diff` |
| stage changes | `sheet-git stage --entry-id <id>` / `sheet-git stage --all` |
| commit | `sheet-git commit --message "..."` |
| inspect history | `sheet-git history [--limit <n>]` |
| inspect one revision | `sheet-git show [<commit-or-checkpoint>]` |
| create review session | `sheet-git review create` |
| inspect review session state | `sheet-git review status <session>` |
| publish to hosted review | `sheet-git push review <session>` |
| read review comments | `sheet-git review comments <session>` |
| preview origin materialization | `sheet-git push origin --dry-run <session>` |
| materialize to origin | `sheet-git push origin <session>` |
| bypass hosted review check | `sheet-git push origin --skip-review-check <session>` |
| resume interrupted replay | `sheet-git push origin --resume <replay-run>` |
| inspect remote-ahead state | `sheet-git fetch origin <entry-id>` |
| pull remote changes locally | `sheet-git pull origin <session-or-entry-id>` |
| bind an existing origin workbook | `sheet-git origin bind-existing <remote-workbook-id>` |
| inspect one cell | `sheet-git blame --entry-id <id> --cell 'Sheet1!A1' [<commit-or-checkpoint>]` |

## Naming discipline

- the command is `history`, not `log`
- the hosted handoff command is `push review`
- use `clone` and `remote add review` as documented; do not invent alternate names
- `--owner` / `--repo` define the hosted review scope for this scenario
- if the scenario has no pre-existing hosted scope, pick stable values and keep reusing them
- do not ask for or simulate `rebase origin`

## References

- [references/command-surface.md](references/command-surface.md): exact commands and naming
- [references/hosted-review.md](references/hosted-review.md): hosted review collaboration
- [references/recovery.md](references/recovery.md): refusal handling and recovery paths
