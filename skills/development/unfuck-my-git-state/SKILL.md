---
name: unfuck-my-git-state
description: Diagnose and recover broken Git state and worktree metadata with a staged, low-risk recovery flow. Use when Git reports detached or contradictory HEAD state, phantom worktree locks, orphaned worktree entries, missing refs, 0000000000000000000000000000000000000000 hashes, or branch operations fail with errors like already checked out, unknown revision, not a valid object name, or cannot lock ref.
---

# unfuck-my-git-state

Recover a repo without making the blast radius worse.

## Core Rules

1. Snapshot first. Do not "just try stuff."
2. Prefer non-destructive fixes before force operations.
3. Treat `.git/` as production data until backup is taken.
4. Use `git symbolic-ref` before manually editing `.git/HEAD`.
5. After each fix, run verification before proceeding.

## Fast Workflow

1. Capture diagnostics:
```bash
bash scripts/snapshot_git_state.sh .
```
2. Route by symptom using `references/symptom-map.md`.
3. Generate non-destructive command plan:
```bash
bash scripts/guided_repair_plan.sh --repo .
```
4. Apply the smallest matching playbook.
5. Run `references/recovery-checklist.md` verification gate.
6. Escalate only if the gate fails.

For explicit routing:
```bash
bash scripts/guided_repair_plan.sh --list
bash scripts/guided_repair_plan.sh --symptom phantom-branch-lock
```

## Regression Harness

Use disposable simulation tests before changing script logic:

```bash
bash scripts/regression_harness.sh
```

Run one scenario:

```bash
bash scripts/regression_harness.sh --scenario orphaned-worktree
```

## Playbook A: Orphaned Worktree Metadata

Symptoms:
- `git worktree list` shows a path that no longer exists.
- Worktree entries include invalid or zero hashes.

Steps:
```bash
git worktree list --porcelain
git worktree prune -v
git worktree list --porcelain
```
If stale entries remain, back up `.git/` and remove the specific stale folder under `.git/worktrees/<name>`, then rerun prune.

## Playbook B: Phantom Branch Lock

Symptoms:
- `git branch -d` or `git branch -D` fails with "already used by worktree".
- `git worktree list` seems to disagree with branch ownership.

Steps:
```bash
git worktree list --porcelain
```
Find the worktree using that branch, switch that worktree to another branch or detach HEAD there, then retry the branch operation in the main repo.

## Playbook C: Detached or Contradictory HEAD

Symptoms:
- `git status` says detached HEAD unexpectedly.
- `git branch --show-current` and `git symbolic-ref -q HEAD` disagree.

Steps:
```bash
git symbolic-ref -q HEAD || true
git reflog --date=iso -n 20
git switch <known-good-branch>
```
If branch context is unknown, create a rescue branch from current commit:
```bash
git switch -c rescue/$(date +%Y%m%d-%H%M%S)
```
Then reconnect to the intended branch after investigation.

## Playbook D: Missing or Broken Refs

Symptoms:
- `unknown revision`, `not a valid object name`, or `cannot lock ref`.

Steps:
```bash
git fetch --all --prune
git show-ref --verify refs/remotes/origin/<branch>
git branch -f <branch> origin/<branch>
git switch <branch>
```
Use `reflog` to recover local-only commits before forcing branch pointers.

## Last Resort: Manual HEAD Repair

Only after backup of `.git/`.

Preferred:
```bash
git show-ref --verify refs/heads/<branch>
git symbolic-ref HEAD refs/heads/<branch>
```
Fallback when `symbolic-ref` cannot be used:
```bash
echo "ref: refs/heads/<branch>" > .git/HEAD
```
Immediately run the verification gate.

## Verification Gate (Must Pass)

Run checks in `references/recovery-checklist.md`. Minimum bar:
- `git status` exits cleanly with no fatal errors.
- `git symbolic-ref -q HEAD` matches intended branch.
- `git worktree list --porcelain` has no missing paths and no zero hashes.
- `git fsck --no-reflogs --full` has no new critical errors.

## Escalation Path

1. Archive `.git`:
```bash
tar -czf git-metadata-backup-$(date +%Y%m%d-%H%M%S).tar.gz .git
```
2. Clone fresh from remote.
3. Recover unpushed work with reflog and cherry-pick from old clone.
4. Document failure mode and add guardrails to automation.

## Automation Hooks

When building worktree tooling (iMi, scripts, bots), enforce:
- preflight snapshot and state validation
- post-operation verification gate
- hard stop on HEAD/ref inconsistency
- explicit user confirmation before destructive commands

## Resources

- Symptom router: `references/symptom-map.md`
- Verification checklist: `references/recovery-checklist.md`
- Diagnostic snapshot script: `scripts/snapshot_git_state.sh`
- Guided plan generator: `scripts/guided_repair_plan.sh`
- Disposable regression harness: `scripts/regression_harness.sh`
