---
name: sit
description: "Use when a persisted `.univer` or `.unv` workbook needs `.sit` repo workflow: status, commit, history inspection, approval-backed sync, or origin pull recovery after workbook edits are saved."
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

Use `univer-cli` to create or edit workbook content. Use `sit` after workbook changes are saved and verified, or for the repo/sync/origin phase of a task that also includes workbook edits.

## Use when

- capturing persisted workbook changes into workbook-lane history
- inspecting repo state, diff, log, show, or blame output
- running the default approval-backed sync flow
- syncing local state with origin or recovering from origin refusal output

## Do not use when

- the workbook still needs to be edited, imported, exported, or structurally changed before repo/sync work can proceed
- the task is only about `univer-cli` workbook authoring
- you are about to invent Git-like commands that are not in the real command surface

## Core model

- local history is commit-based
- the public repo root for a workbook is `<file>.univer/.sit`
- the public tracked object is a workbook path, not an internal runtime id
- the current human gate truth is repo-local commit approval state
- `sit sync <file.univer>` is the default pull-first convergence path; it pulls first, then only continues origin advancement when the current HEAD commit is approved
- `sit pull origin <file.univer>` is the pull-only path
- recovery goes through existing `pull` surfaces
- `rebase origin` is not part of the command surface

## Default flow

1. Ensure workbook edits are already persisted and verified with `univer-cli`.
2. Run `sit status <univer-path>` when you need a quick lane summary.
3. Commit with `sit commit <univer-path> --message "..."`.
4. Inspect with `sit diff <univer-path>` or `sit log <univer-path>`.
5. Ensure approval is recorded in the current repo-local commit approval truth.
6. Run `sit sync <univer-path>` as pull-first convergence. It pulls first, then only continues origin advancement when the current HEAD commit is approved.

## Common routes

### Attach to an existing origin workbook

- `sit origin bind-existing <remote-workbook-id> <univer-path>` on a fresh local target path

### Pull remote changes only

- `sit pull origin <univer-path>`

Use pull-only mode when the task is to materialize or repair local state from remote origin, not to run the default approval-backed publish path.

## Quick reference

Use these exact commands when naming matters:

- `sit status [<univer-path>]`
- `sit diff <univer-path> [<revision>]`
- `sit log <univer-path> [--limit <n>]`
- `sit show <univer-path> [<revision>]`
- `sit blame <univer-path> --cell 'Sheet1!A1' [<revision>]`
- `sit commit <univer-path> --message "..."`
- `sit origin bind-existing <remote-workbook-id> <univer-path>`
- `sit pull origin <univer-path>`
- `sit pull origin --force-to-latest <univer-path>`
- `sit sync <univer-path>`

Current implementation note:

- `sit fetch origin <univer-path>` may still exist as internal / compatibility plumbing
- it is not part of the current public/default command teaching surface
- if you mention it, label it as implementation detail rather than the recommended user command

## Recovery cues

Use these when a `sit` happy path stops midway:

- local workbook is still dirty:
  `sit commit <univer-path> --message "..."`
- approval has not been recorded yet:
  record approval in repo-local commit approval truth
- remote state needs local materialization:
  `sit pull origin <univer-path>`
- pull repair is explicitly suggested:
  `sit pull origin --force-to-latest <univer-path>`
- `sit sync` says replay is not confirmed yet:
  rerun `sit sync <univer-path>`
- lineage is blocked:
  resolve the blocking condition before rerunning `sit sync <univer-path>` or `sit pull origin <univer-path>`

## Naming discipline

- use `commit <file.univer> --message`, not staging-first aliases
- use `sync`, not invented publish aliases
- use `pull origin`, not `sync`, when the intent is explicitly remote-to-local materialization
- treat `fetch origin` as internal/legacy wording unless the user is explicitly discussing current implementation internals
- do not ask for or simulate `rebase origin`
