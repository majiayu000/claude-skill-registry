---
name: sheet-git
description: Spreadsheet repo control and hosted review/origin collaboration for persisted `agent-sheet` workspaces. Use when needs to stage workbook entries, create commits or proposal-shaped review units, inspect proposal state, publish to hosted review, pull machine-readable review comments, or coordinate `push/fetch/pull` against origin. Do not use it for direct workbook editing.
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

Current authority split:

- `proposal` is the Git-shaped local handle and read model
- hosted review truth is a review session
- origin execution truth is a replay run
- `pull origin` absorbs replay/recovery; `rebase origin` is not part of the current surface

Use `agent-sheet` to create, edit, attach, and persist workbook content.
Use `sheet-git` when the task becomes:

- binding a local repo to one hosted review scope
- choosing the correct hosted `{owner}/{repo}` scope inside one shared hosted review instance
- cloning an existing hosted review repo into a fresh local workspace
- capturing persisted local workbook changes into repo history
- creating and tracking proposals
- handing proposals to hosted review
- pulling machine-readable review feedback
- materializing reviewed changes to origin
- recovering collaborative drift with `fetch` and `pull`

## Hard boundaries

- Operate on persisted local entry files only.
- Start from `agent-sheet` if the workbook content itself still needs to change.
- Treat `push review` as handoff only. It publishes to hosted review; it does not approve.
- Treat `proposal comments` as the agent-facing review surface. It returns JSON packets, and the default read is now a continuity view: current revision plus unresolved carried-forward threads from the same review session.
- Treat `push origin` as the real origin materialization step.
- Treat `push origin --resume <replay-run>` as replay continuation, not a separate merge system.
- Treat hosted web as an approve-only human review surface. The main human routes are `/` for the simple home page, `/owners/{owner}/repos/{repo}/reviews` for the scoped list, and `/owners/{owner}/repos/{repo}/reviews/sessions/{reviewId}` for review detail.
- Follow refusal output literally. `fetch origin`, `pull origin`, and `push origin` already emit the next safe command when collaboration state is blocked.
- Treat `draft-replay-required` as the preserved-draft path: `pull origin` should keep Alice local draft and replay it onto the newer remote base when the shape is safe.
- Treat `--force-to-latest` as an explicit escape hatch, not the default answer for transformable local draft.
- In the common gold-user-story case of `remote ahead + local unsynced commits 0`, ordinary `pull origin` is the main path even if `status` still shows staging constraints.

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

When `fetch origin` reports:

- `remote ahead yes`
- `local unsynced commits 0`
- `pull readiness ready`

prefer plain:

- `sheet-git pull origin <entry-id>`

Do not escalate to `--force-to-latest` unless the refusal path or recovery state explicitly requires it.

## Highest-signal playbooks

### Local capture

- `sheet-git remote add review <base-url> --owner <owner-id> --repo <repo-id>` when the repo should publish to hosted review
- `sheet-git init`
- `sheet-git stage --entry-id <id>` or `sheet-git stage --all`
- `sheet-git commit --message "..."`
- `sheet-git proposal create`

Stage behavior:

- `stage` auto-flushes live dirty local workbook state when it is safe
- `stage` also attempts to auto-reconcile simple persisted drift into a replayable local batch
- if it still refuses, treat that as “the current workbook state could not be reconstructed as a replayable local change”, not as a signal that pull is necessarily blocked

### Start from an existing hosted repo

- `sheet-git clone <owner>/<repo> --base-url <base-url>`
- or `sheet-git clone <host>/<owner>/<repo>` for browser-copied host shorthand
- or `sheet-git clone <review-url>`
- this creates a fresh local workspace, binds the hosted scope, and restores the latest materialized entries
- if the hosted repo exists but has no materialized origin workbook yet, `clone` still binds the hosted scope but cannot hydrate workbook content yet

### Publish to Bob

- `sheet-git push review <proposal>`
- Bob sees the same proposal in hosted inbox as `needs-review`
- follow-up local commits should be republished through the same proposal id, not a new proposal

Read [references/hosted-review.md](references/hosted-review.md) when the task involves Alice/Bob handoff, follow-up revisions, or materialization waiting state.

### Pull review feedback

- `sheet-git proposal comments <proposal>`
- default output is JSON review packet with continuity semantics
- current revision threads stay marked as current, and unresolved old threads stay visible as carried-forward items
- selection-based comments may include `selectionAttachment`
- revise locally, commit again, then `sheet-git push review <same proposal>`

### Materialize to origin

- `sheet-git push origin --dry-run <proposal>`
- `sheet-git push origin --explain <proposal>`
- `sheet-git push origin <proposal>`
- `sheet-git push origin --resume <replay-run>`
- `sheet-git fetch origin <entry-id>`
- `sheet-git pull origin <proposal-or-entry-id>`

Hosted gate rule:

- do not assume you must run `proposal status` before `push origin`
- `push origin` now refreshes hosted approval state on the main path

Read [references/recovery.md](references/recovery.md) when `fetch`, `pull`, or `push` refuses and emits a next step.

## Quick routes

| Task | Command |
|---|---|
| clone an existing hosted repo | `sheet-git clone <owner>/<repo> [<path>] --base-url <base-url>` |
| clone from host shorthand | `sheet-git clone <host>/<owner>/<repo> [<path>]` |
| initialize repo | `sheet-git init` |
| bind hosted review scope | `sheet-git remote add review <base-url> --owner <owner-id> --repo <repo-id>` |
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
| resume a replay run | `sheet-git push origin --resume <replay-run>` |
| see remote-ahead state | `sheet-git fetch origin <entry-id>` |
| materialize remote changes locally | `sheet-git pull origin <proposal-or-entry-id>` |
| force destructive local repair | `sheet-git pull origin --force-to-latest <proposal-or-entry-id>` |
| blame one cell | `sheet-git blame --entry-id <id> --cell 'Sheet1!A1' [<commit>]` |
| inspect history | `sheet-git history [--limit <n>]` |
| inspect one revision | `sheet-git show [<commit>]` |

For exact command semantics and output expectations, read [references/command-surface.md](references/command-surface.md).

## Output discipline

- Prefer `status` or `proposal status` before making claims.
- Treat semantic summaries as the default review surface.
- Drop to raw cell diff or blame only when the summary is not enough.
- When reporting a blocked state, include the exact refusal text and the suggested next command.
- In multi-repo situations, always report the hosted scope as `{owner}/{repo}`, not just the proposal id.
- Treat `status` / `diff` staging-constraint output as capture/staging context, not automatically as a veto on safe `pull origin`.
