---
name: repository-hygiene-sweep
description: |-
  Use when cleaning repository branches, worktrees, gc state, large objects, and exclusion rules safely.
  Triggers:
skill_api_version: 1
user-invocable: false
hexagonal_role: supporting
practices:
- pragmatic-programmer
- twelve-factor
consumes: []
produces:
- repo-cleanup-report
context_rel: []
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: topic
metadata:
  tier: execution
  dependencies: []
  stability: stable
output_contract: A cleanup report (what was found, what was changed, what was deliberately skipped and why) plus a list of reversible recovery commands. No destructive operation runs without explicit, scoped confirmation.
---

# repository-hygiene-sweep — clean a repository without destroying useful work

Maintain a git repository: prune merged branches, compact storage, hunt large/dangling objects, and (only with explicit consent) rewrite history to remove accidental large files or secrets. The discipline is conservation — every step is reversible-first, and anything ambiguous is skipped, not guessed.

## ⚠️ Critical Constraints

- **Never run a destructive command without explicit, scoped confirmation.** Branch deletion, history rewrite, `reflog expire`, and `gc --prune=now` are the destructive set. Name exactly what will be destroyed and wait for a yes. **Why:** these are the operations that lose real work, and the user often does not realize what a branch or reflog entry was protecting.
- **Skip when in doubt — never guess.** If you cannot prove a branch is fully merged, a file is truly junk, or a repo is not shared, do nothing and report the ambiguity. **Why:** the cost of a wrong delete (lost work) vastly exceeds the cost of leaving a stale branch around.
- **Read-only first; mutate only after.** Run the diagnosis pass (counts, sizes, candidate lists) and present it before changing anything. **Why:** the user must see what they are approving.
  - WRONG: `git branch --merged | grep -v '\*' | xargs git branch -d`  (auto-deletes on a single guess)
  - CORRECT: list `git branch --merged main`, show it, get confirmation, then delete named branches one set at a time.
- **Never delete a branch that is not merged with `-D`.** Use `-d` (refuses to delete unmerged). **Why:** `-D` force-deletes branches that contain unique commits — the classic way to silently lose work.
  - WRONG: `git branch -D feature/x`
  - CORRECT: `git branch -d feature/x` and, if it refuses, investigate why instead of forcing.
- **Never rewrite published/shared history casually.** History rewrite (filter-repo, BFG) is acceptable only on a repo the owner confirms is unshared or whose collaborators have agreed to re-clone. **Why:** rewriting shared history breaks every other clone and can resurrect "deleted" data on the next push.
- **Always confirm a clean, backed-up state before any history rewrite.** Require a committed/clean working tree and a fresh mirror clone (`git clone --mirror`) as the backup. **Why:** history rewrite is the one operation with no in-repo undo once reflogs are expired.
- **A leaked secret is not "removed" by rewriting history alone.** Always advise rotating/revoking the secret too. **Why:** the secret may already be cloned, cached, or on a fork — rotation is the only real remediation.

## Why This Exists

Repositories accumulate cruft: dozens of merged feature branches, a `.git` directory bloated by an accidentally-committed binary, loose objects, and `.gitignore` files that let junk slip in. Cleaning them is routine but genuinely dangerous — the same commands that reclaim space (`gc --prune`, `branch -D`, history rewrite) are the ones that permanently destroy work. Agents are biased toward "looks done" and toward force-flags that make errors disappear; that bias is exactly wrong here. This skill exists to make the safe path the default path: diagnose, propose, confirm, act reversibly, and skip anything uncertain.

## Quick Start

```bash
# 1. Confirm where you are and that nothing is uncommitted (diagnosis is safe, read-only).
git rev-parse --is-inside-work-tree && git status --short

# 2. Run the full read-only diagnosis bundle.
bash {baseDir}/scripts/diagnose.sh        # branches, sizes, large blobs, dangling objects

# 3. Review the report, confirm specific actions, then mutate one category at a time.
```

`{baseDir}/scripts/diagnose.sh` is **Execute** — run it to gather the report. It changes nothing.

## Workflow

### Phase 1 — Diagnose (read-only, always first)
Establish ground truth before touching anything.

```bash
git status --short                                  # uncommitted work? (if yes, STOP — back up first)
git fetch --all --prune --dry-run                   # what would prune; preview only
git branch -vv --merged                             # branches fully merged into HEAD
git branch -vv --no-merged                          # branches with unique commits (DO NOT auto-delete)
git for-each-ref --sort=committerdate refs/heads --format='%(committerdate:short) %(refname:short)'
du -sh .git                                          # current repo storage footprint
git count-objects -vH                               # loose vs packed, size, dangling count
```

**Checkpoint:** if the working tree is dirty, or this is a shared repo and the user has not confirmed it, stop and report. Do not proceed to any mutation.

### Phase 2 — Prune branches (reversible)
Branch deletion is recoverable via reflog for a while, but treat it as consequential.

```bash
# Identify the integration branch explicitly (main/master/develop) — do not assume.
git branch --merged main | grep -vE '^\*| main$| master$| develop$'   # safe-to-delete candidates
```

- Present the candidate list. Delete only confirmed names, using `-d` (never `-D`).
- For remote-tracking cleanup of branches already deleted upstream: `git fetch --prune` (safe; only removes stale remote refs, not your local branches).
- Record each deleted branch's tip SHA in the report so it can be restored: `git branch <name> <sha>`.

**Checkpoint:** verify each deletion succeeded with `-d` (no force). If git refused, the branch had unique commits — leave it and flag it.

### Phase 3 — Compact storage (reversible vs destructive split)
```bash
git gc                          # safe: repacks, keeps reflog-reachable + recent loose objects
git repack -Ad                  # safe: consolidate packs
# DESTRUCTIVE — only after explicit confirmation:
# git reflog expire --expire=now --all && git gc --prune=now   # drops unreachable objects permanently
```

Run the safe `gc` by default. Only offer the prune-now path when the user explicitly wants to reclaim space from already-removed history AND understands it makes recovery impossible.

### Phase 4 — Find large / dangling objects (read-only)
See [references/large-objects.md](references/large-objects.md) for the blob-size ranking and dangling-object triage recipes.

**Checkpoint:** finding a large blob does not mean removing it. Confirm it is genuinely unwanted (not a needed asset) before considering Phase 5.

### Phase 5 — Remove large files / secrets from history (DESTRUCTIVE — gated)
This rewrites history. Do not enter this phase without: clean tree, confirmed unshared-or-agreed repo, and a `git clone --mirror` backup. Procedure, tool choice (git-filter-repo vs BFG), and the force-push/re-clone protocol are in [references/history-rewrite.md](references/history-rewrite.md).

### Phase 6 — .gitignore hygiene (low-risk)
```bash
git status --ignored --short                        # what is currently ignored
git ls-files --others --exclude-standard            # untracked, not ignored — should any be ignored?
git check-ignore -v <path>                           # explain why a path is/ignored
```

- Propose additions for build artifacts, dependency dirs, env/secret files, OS cruft. Do not blanket-ignore source.
- If a file is ALREADY tracked, adding it to `.gitignore` does nothing — note that it needs `git rm --cached` (a tracked-content change, confirm separately).

## Output Specification

Produce a report named `repo-cleanup-report.md` (or inline if small) with:
1. **Findings** — repo size, branch counts (merged/unmerged/stale), large blobs (size + path), dangling object count, .gitignore gaps.
2. **Actions taken** — each mutation, the exact command, and the result.
3. **Skipped (and why)** — every ambiguous item deliberately left alone.
4. **Recovery** — reversible commands (deleted branch SHAs, mirror-backup location).

## Quality Rubric

- No destructive command (`branch -D`, `gc --prune=now`, history rewrite, `reflog expire`) ran without a logged, explicit confirmation for that specific target.
- Every branch deletion used `-d`, and every deleted branch's tip SHA is recorded for restore.
- The report's "Skipped" section is non-empty whenever any candidate was ambiguous — the skill demonstrably chose caution over completeness.

## Examples

- **Routine pass:** Diagnose shows 18 merged branches, 1.2 GB `.git`, 40 loose objects. → List merged branches, confirm, `-d` delete; `git gc`; report 1.2 GB → 1.2 GB (size dominated by a large blob in history, surfaced in Phase 4 for a separate decision).
- **Bloat hunt:** `.git` is 4 GB. Phase 4 finds a 3.6 GB `dataset.zip` committed 200 commits back. → Confirm it is unwanted, confirm repo is solo + clean, mirror-backup, then `git filter-repo` per references/history-rewrite.md; advise force-push + collaborator re-clone.
- **Leaked key:** `.env` with a live API key was committed. → Rewrite history to drop it AND tell the user the key must be rotated immediately — rewriting alone does not secure it.

## Troubleshooting

| Symptom | Cause | Action |
|---|---|---|
| `git branch -d` refuses ("not fully merged") | Branch has unique commits | Do NOT use `-D`. Investigate the commits; keep the branch and flag it. |
| `.git` size unchanged after `gc` | Large objects still reachable from history/reflog | Confirm intent; only then Phase 5 history rewrite, not blind `--prune=now`. |
| `gc --prune=now` lost a stash/commit | Reflog was expired, removing the only ref | Recover from the mirror backup; this is why the backup is mandatory. |
| Force-push rejected after rewrite | Remote protects the branch / others pushed | Coordinate with collaborators; do not work around branch protections unilaterally. |
| Adding to `.gitignore` had no effect | File is already tracked | `git rm --cached <path>` (confirm separately), then commit. |

## See Also

| I need to… | Reference |
|---|---|
| Rank large blobs / triage dangling objects | [references/large-objects.md](references/large-objects.md) |
| Safely rewrite history to remove a file/secret | [references/history-rewrite.md](references/history-rewrite.md) |
