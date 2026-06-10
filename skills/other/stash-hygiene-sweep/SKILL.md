---
name: stash-hygiene-sweep
description: |-
  Use when auditing git stashes, deciding keep/drop/apply/archive, and clearing confirmed stale entries.
  Triggers:
practices:
- defensive-programming
- code-complete
hexagonal_role: supporting
consumes: []
produces: []
context_rel: []
skill_api_version: 1
context:
  window: isolated
  intent:
    mode: none
metadata:
  tier: execution
  stability: experimental
  dependencies: []
output_contract: 'stdout: per-stash keep/drop verdict table; side effect: stashes applied/archived to refs/stash-archive, only confirmed-redundant stashes dropped'
user-invocable: false
---
# stash-hygiene-sweep — audit and clear a git-stash backlog without losing work

> **Purpose:** Turn a long, scary `git stash list` into a reviewed, intentional
> decision per stash. Inspect every stash, classify keep vs. drop, apply or
> archive the keepers, and drop **only** what is provably redundant.

## ⚠️ Critical Constraints

- **`git stash drop` and `git stash clear` are destructive and have no undo via
  porcelain.** A dropped stash's commit lingers in the reflog/`fsck` for a while
  but is unreachable, GC-able, and a nightmare to recover. **Why:** the whole
  point of this skill is to never silently lose work — treat every drop as
  permanent.
  ```bash
  # WRONG — nukes every stash, zero review, unrecoverable in practice
  git stash clear
  # CORRECT — review each, archive keepers, drop only the confirmed-redundant one
  git stash show -p stash@{2} | less   # inspect first
  git stash drop stash@{2}             # only after a recorded keep/drop verdict
  ```
- **Never `drop` a stash you have not inspected with `git stash show -p`.**
  **Why:** an unreviewed stash is unknown work; dropping unknown work is the
  exact failure this skill exists to prevent.
- **Skip-when-in-doubt is the default verdict, and it means ARCHIVE, not drop.**
  If you cannot prove a stash is redundant (already merged / empty / a confirmed
  duplicate), do **not** drop it. Branch it to `refs/stash-archive/*` and leave
  the original stash in place for the human. **Why:** archiving is reversible;
  dropping is not. When unsure, choose the reversible move every time.
- **Never run on a dirty tree mid-decision without recording it.** `stash apply`
  can conflict with uncommitted changes. **Why:** a failed apply can leave the
  working tree half-merged and confuse the audit.
  ```bash
  # WRONG — applying a stash onto a dirty tree, may conflict and corrupt state
  git stash apply stash@{0}
  # CORRECT — confirm clean tree (or stash current work first), then apply
  git status --porcelain   # must be empty before applying a keeper
  ```
- **Stash indices renumber on every drop.** `stash@{3}` becomes `stash@{2}` after
  you drop `stash@{0}`. **Why:** dropping by stale index deletes the WRONG stash.
  Resolve each stash to its immutable commit SHA up front and operate by SHA, or
  drop strictly highest-index-first.

## Why This Exists

A git stash backlog is one of the highest-anxiety cleanup tasks: the list is
opaque (`WIP on main: ...` tells you almost nothing), the verbs are destructive
and effectively un-undoable, and the indices shift under you as you delete. The
naive moves — `git stash clear`, or dropping by remembered index — silently
destroy work. This skill replaces "clear it all and hope" with a per-stash,
evidence-first audit whose default verdict is the reversible one.

## Quick Start

```bash
# 1. Snapshot the backlog with stable identities (SHA), never just indices
git stash list --format='%gd %H %ci %gs'

# 2. Inspect ONE stash before any verdict
git stash show -p 'stash@{0}'        # full diff
git stash show --stat 'stash@{0}'    # files touched, quick scan

# 3. Archive a keeper to a branch (reversible), then it's safe to drop later
git branch "stash-archive/$(date +%Y%m%d)-wip-0" 'stash@{0}'

# 4. Drop ONLY a stash with a recorded "redundant" verdict, highest index first
git stash drop 'stash@{0}'
```

## Workflow

### Phase 1 — Snapshot (immutable identities)
Capture the backlog keyed by commit SHA, not just `stash@{N}`, because indices
renumber as you drop.

```bash
git stash list --format='%gd | %H | %ci | %gs'
```

Record the table. Each row: index, SHA, date, subject. The SHA is the stable
handle for the rest of the run.

**Checkpoint:** if the list is empty, report "no stashes" and stop. If `git
status --porcelain` is non-empty, note that the tree is dirty — keepers cannot be
applied until it is clean, but inspection and archiving are still safe.

### Phase 2 — Inspect each stash
For every stash, gather enough to classify it. Never skip this step.

```bash
git stash show -p "$SHA"             # works by SHA too; full diff
git stash show --stat "$SHA"         # files + line counts
git log --oneline -1 "$SHA"          # the stash's WIP commit subject
```

Classify each into exactly one bucket:

- **REDUNDANT** — provably safe to drop. Proof required, e.g.:
  - Empty diff: `git stash show -p "$SHA"` produces no output.
  - Already merged: every hunk is present on the current branch
    (`git stash show -p "$SHA" | git apply --check -R -` succeeds → the changes
    already exist in the tree).
  - Confirmed duplicate of another stash with identical diff (compare patches).
- **KEEP** — has unique, possibly-useful changes. Will be archived.
- **UNSURE** — cannot prove redundant. **Treat as KEEP** (skip-when-in-doubt).

### Phase 3 — Archive keepers (reversible)
Before dropping anything, make every KEEP/UNSURE recoverable. Branch the stash
commit so it survives independent of the stash stack.

```bash
git branch "stash-archive/$(date +%Y%m%d)-${SLUG}" "$SHA"
# or, to also preserve it as a stash-namespaced ref:
git update-ref "refs/stash-archive/${SLUG}" "$SHA"
```

Optionally apply a keeper into the working tree (only on a clean tree):

```bash
git status --porcelain   # MUST be empty
git stash apply "$SHA"   # apply; resolve conflicts; do NOT auto-drop
```

**Checkpoint:** confirm each archive ref exists (`git branch --list
'stash-archive/*'`) before proceeding to any drop.

### Phase 4 — Drop only the confirmed-redundant
Drop strictly highest-index-first so renumbering never points you at the wrong
stash. Drop **only** stashes with a recorded REDUNDANT verdict from Phase 2.

```bash
# Re-resolve indices NOW (they may have shifted); drop highest index first
git stash list --format='%gd %H'
git stash drop 'stash@{N}'   # N = highest redundant index, repeat descending
```

**Never** use `git stash clear`. If the human explicitly asks to wipe
everything, refuse the bulk verb and instead archive all stashes to branches
first, then drop individually.

## Output Specification

Emit a verdict table to stdout before taking any destructive action, then a
summary. Suggested artifact filename if persisted: `stash-audit-<date>.md`.

```
| idx | sha7    | date       | subject              | verdict   | action          |
|-----|---------|------------|----------------------|-----------|-----------------|
| 0   | a1b2c3d | 2026-05-01 | WIP on main: hotfix  | KEEP      | archived→branch |
| 1   | e4f5g6h | 2026-04-22 | WIP on feat: spike   | REDUNDANT | dropped         |
| 2   | i7j8k9l | 2026-03-10 | WIP on main          | UNSURE    | archived (kept) |

Summary: 3 stashes reviewed · 2 archived · 1 dropped (redundant) · 0 lost.
```

## Quality Rubric

- **No unreviewed drop:** every dropped stash has a recorded REDUNDANT verdict
  backed by an inspection command output — verifiable in the audit table.
- **Every non-redundant stash is recoverable:** for each KEEP/UNSURE there is a
  `stash-archive/*` ref (`git branch --list 'stash-archive/*'` shows it).
- **No `git stash clear` was run, and drops were highest-index-first:** the
  command log shows individual `git stash drop` calls in descending index order.

## Examples

**Backlog of 5, two empties, three real:**
Snapshot → inspect all five → two have empty diffs (REDUNDANT) → three have
unique changes (KEEP) → branch the three to `stash-archive/*` → drop the two
empties highest-index-first → report "5 reviewed, 3 archived, 2 dropped, 0 lost".

**Human says "just clear them all":**
Refuse the bulk verb. Archive all stashes to `stash-archive/*` branches first,
report what was preserved, then offer to drop individually only after
confirmation. Reversibility is preserved either way.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `stash drop` deleted the wrong stash | dropped by stale index after a prior drop renumbered the stack | recover from reflog `git fsck --no-reflogs --unreachable \| grep commit`; thereafter operate by SHA or highest-index-first |
| `stash apply` reports conflicts | applied onto a dirty/divergent tree | abort, ensure `git status --porcelain` is empty, retry; resolve conflicts manually |
| Can't tell if a stash is already merged | opaque `WIP on ...` subject | `git stash show -p "$SHA" \| git apply --check -R -` — success means changes already in tree (REDUNDANT) |
| Lost a dropped stash | porcelain has no undo | `git fsck --unreachable --no-reflogs` to find dangling commits, then `git branch rescue <sha>` quickly before GC |

## See Also

- `git stash show`, `git stash apply`, `git stash branch`, `git reflog` — the
  underlying porcelain this skill orchestrates safely.
