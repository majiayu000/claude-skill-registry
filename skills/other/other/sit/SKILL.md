---
name: sit
description: "Use when a persisted `.univer` or `.unv` workbook needs `.sit` repo workflow: status, add/reset, diff/log/show/blame/checkpoints, commits, review sessions, hosted review feedback, `push review`, or origin fetch/pull/push recovery after workbook edits are saved."
metadata:
  openclaw:
    os:
      - linux
      - macos
    requires:
      bins:
        - sit
      anyBins:
        - univer
        - unv
    install:
      - kind: none
    links:
      repository: https://github.com/dream-num/skills
      documentation: https://github.com/dream-num/skills
---

# sit

`sit` is the canonical Git-shaped control plane for persisted Univer workbooks.

Use `univer-cli` to create or edit workbook content. Use `sit` after workbook changes are saved and verified, or for the repo/review/origin phase of a task that also includes workbook edits.

## Use when

- capturing persisted workbook changes into repo history
- inspecting repo state, diff, log, show, checkpoint, or blame output
- creating or updating a local review session
- publishing a review session to hosted review
- reading machine-readable hosted review feedback
- syncing local state with origin or recovering from origin refusal output

## Do not use when

- the workbook still needs to be edited, imported, exported, or structurally changed before repo/review work can proceed
- the task is only about `univer-cli` workbook authoring
- you are about to invent Git-like commands that are not in the real command surface

## Core model

- local history is commit-based
- the public repo root is `.sit`
- the public tracked object is a workbook path, not an internal runtime id
- local review attempt is a `review session`
- hosted thread reuse is decided by `push review`
- local durable truth is still the local `review session`
- hosted review is separate from origin materialization
- there is no local `approve` command
- recovery goes through existing `fetch` / `pull` / `push origin --resume` surfaces
- `rebase origin` is not part of the command surface

## Default flow

1. Ensure workbook edits are already persisted and verified with `univer-cli`.
2. If the repo does not exist yet, run `sit init`.
3. Run `sit status`.
4. Capture changes with `sit add <univer-path>` or `sit add --all`.
5. Inspect with `sit diff`.
6. Commit with `sit commit --message "..."`.
7. Create a review session with `sit review create`.

## Common routes

### Start from an existing hosted repo

- `sit clone <owner>/<repo> --base-url <base-url>`
- `sit clone <host>/<owner>/<repo>`
- `sit clone <review-url>`

Here `{owner}/{repo}` is the hosted review scope for this scenario. It does not need to be pre-created; if the scenario has no existing scope yet, choose stable values and reuse them consistently.

### Publish for review

- `sit remote add review [<base-url>] --owner <owner-id> --repo <repo-id>`
- `sit push review <session>`

### Read review feedback

- `sit review status <session>`
- `sit review comments <session>`

### Sync with origin

- `sit fetch origin <univer-path>`
- `sit pull origin <session-or-univer-path>`
- `sit pull origin --force-to-latest <session-or-univer-path>`
- `sit push origin --dry-run <session>`
- `sit push origin --explain <session>`
- `sit push origin <session>`
- `sit push origin --skip-review-check <session>`
- `sit push origin --resume <replay-run>`

By default, `sit push origin <session>` checks hosted approval before replaying. Use `--skip-review-check` only when you need the explicit bypass path.

Follow refusal output literally. If `sit` tells you the next safe command, use that instead of improvising.

## Naming discipline

- use `log`, not `history`
- use `add`, not `stage`
- use `push review`, not invented publish aliases
- use `remote add review` for hosted review scope
- do not ask for or simulate `rebase origin`

## Read next

- [references/command-surface.md](references/command-surface.md): exact commands and naming
- [references/hosted-review.md](references/hosted-review.md): hosted review collaboration
- [references/recovery.md](references/recovery.md): refusal handling and recovery paths
