---
name: git-branchless
description: Enforce idiomatic git-branchless during planning and executing tasks — detached-HEAD-first work, in-memory rebase via `git move`, event-log recovery via `git undo`, deferred branch creation, speculative-merge `git sync` for base updates. Use when planning or executing multi-commit work, history rewrites, stack edits, rebase/reorder, fixup insertion mid-stack, stacked-PR publishing, or recovery from bad git ops; or when the user mentions branchless, smartlog, `git move`, or `git undo`. Silently inert if branchless is not initialized for the current repo.
---

# Git-branchless

Branchless treats commits as checkpoints, detached HEAD as the default
work mode, and branches as publishing artifacts. This skill enforces that
mental model and routes every common git workflow to its branchless
equivalent. Reference docs:

- `references/commands.md` — every command, flag, revset, config key.
- `references/recipes.md` — concrete sequences + decision rubric.
- `references/recovery.md` — undo, restack, hide, snapshot, GC semantics.

---

## Pre-flight gate [LOAD-BEARING]

Before applying any rule below, confirm branchless is initialized for the
current repository. Run:

```
test -d "$(git rev-parse --git-common-dir)/branchless" && git config --get branchless.core.mainBranch
```

(Resolving the git-common-dir handles linked worktrees, where `.git` is a
file rather than a directory and branchless state lives in the main repo's
git dir.)

| Result | Skill behavior |
|--------|----------------|
| Both succeed | Skill is active. Apply the rules below. Acknowledge with one line: `git-branchless active — main=<value>`. |
| Either fails | Skill is **silently inert**. Emit one line: `git-branchless not initialized; skill inactive`. Yield to plain git. Do **not** suggest `git branchless init` unless the user explicitly asks how to enable. |

The inert path is intentional. This skill does not nag and does not refuse
legitimate work in repos where branchless was never adopted.

---

## Always / Never (operation-class framing)

Each rule names an **operation class**, not a command. Plain-git commands
are fine when they fall outside the class.

| Class | Always | Never |
|-------|--------|-------|
| **Stack edits** (reorder, fixup, squash, split) | `git move`, `git move -F`, `git reword`, and `git split` where available `[v0.11.0+]` (use the Recipe 4 workaround on older versions). | `git rebase -i` to drive stack edits. |
| **Base updates** (rebase a stack onto fresh main) | `git sync --pull` (or `git move -b 'stack()' -d origin/main`). Read the skip summary. | `git pull --rebase` against a stack. |
| **Undoing committed history** | `git undo -i`. | `git reset --hard <SHA>` against any commit you have already made. |
| **Discarding local work in progress** | `git hide -r <tip>` (recoverable). | `git branch -D` or `git reset --hard` purely to wipe. |
| **Branch creation for ephemeral work** | Detached HEAD until publish; commit immediately, branch later. | `git checkout -b feature/X` before the first commit exists. |
| **Publishing** | Branch the tip then `git push -u`, or `git submit -c` on supported forges. | Force-push as a way to "fix" your local history. |

Edge cases that are still legitimate (do not block these):

- `git reset --soft HEAD~` against staging when nothing has been committed yet.
- `git rebase --onto` for a one-off, non-interactive upstream sync in a repo where branchless is not initialized (the skill is inert there anyway).
- `git checkout -b` when the work is genuinely about to be pushed.

---

## Workflow phases

```
Init   → git branchless init  (one-time per repo)
Work   → git switch --detach origin/main → edit → git commit (or git record)
Refine → git move | git move --fixup | git amend | git reword | git split [v0.11.0+]
Sync   → git sync --pull       (re-base onto fresh main; read skip summary)
Verify → git test run --exec '<cmd>' 'stack()'  (revset is positional)
Publish→ git branch <name> <tip> && git push -u origin <name>
        (or git submit -c on Phabricator; treat GitHub forge as experimental)
Recover→ git undo -i           (event-log walk replaces reflog spelunking)
```

Restack is mostly automatic. After `git amend`, `git reword`, `git move`,
or `git split`, descendants are auto-restacked in-memory. Run
`git restack` manually only when the smartlog warns about abandoned
subtrees (`✕` ancestors).

---

## Decision rubric (quick lookup)

| Goal | Command sequence |
|------|------------------|
| Insert a fixup mid-stack | `git commit --fixup <target>` then `git move -s HEAD -d <target> --fixup` |
| Reorder commits | `git move -s <src> -d <dest>` |
| Squash two commits | `git move -s <child> -d <parent> --fixup` |
| Split a commit | `git split <commit>` `[v0.11.0+]` (or workaround in `recipes.md` Recipe 4) |
| Rebase stack onto main | `git sync --pull` |
| Find first failing commit | `git test run --search binary --exec '<cmd>' 'stack()'` |
| Recover lost work | `git undo -i` |
| Discard a local experiment | `git hide -r <tip>` |
| Publish | `git branch <name> <tip>` then `git push -u`, or `git submit -c` |

Full recipes with rationale: `references/recipes.md`.

---

## Hand-off

- **`atomic-commit`** is the per-commit-grouping concern. Pair this skill
  with `atomic-commit` when the task is "commit my changes" — branchless
  handles workflow, atomic-commit handles per-change boundaries.
- **`git-guardrails-claude-code`** is the complementary block-list hook.
  This skill teaches the branchless idioms; that skill enforces a hard
  block on `git push --force`, `git reset --hard`, and similar. They
  coexist — the hook surfaces a refusal, this skill surfaces the right
  alternative.
- **`fix`** drives iterative repair via per-iteration commits + revert
  protocol. `fix` already uses `git revert HEAD --no-edit` (event-log-friendly)
  rather than `git reset --hard`; this skill is consistent with that.

ODIN-baseline agents already have an abridged branchless cheat-sheet in
their style block. This skill is the canonical, deeper reference for both
ODIN and non-ODIN agents — it does not depend on the baseline being loaded.

---

## Self-skepticism notes

Things this skill is **uncertain** about and treats accordingly:

- `git split` and its modes (`--detach`, `--discard`, `--before`) are
  documented for `[v0.11.0+]`. The locally installed version may be older.
  Recipes include a pre-`v0.11.0` workaround.
- `git submit --forge github` is **experimental** in v0.9.0. Stack
  reordering can lose PR ancestry. Default to manual branch + `git push`
  for GitHub work; reserve `git submit` for Phabricator.
- The event log is per-repository and per-clone. `git undo` cannot reach
  state from a different clone or a different machine.
- Speculative-merge skips during `git sync` and `git move` are silent
  unless you read the summary line. The skill reminds you to read it,
  but cannot enforce it without running the command.

When the skill recommends a flag and the local version rejects it, fall
back to the closest documented alternative in `references/commands.md`
and tell the user which version-gated feature was unavailable.
