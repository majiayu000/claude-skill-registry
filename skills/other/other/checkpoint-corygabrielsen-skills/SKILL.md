---
name: checkpoint
description: Swarm-safe git checkpoint workflow to validate, stage, commit, and optionally push work in any repo. Use when user says "checkpoint", "save", "commit", "stage and commit", or wants a safe, repeatable snapshot.
---

# Checkpoint

## Overview

Create a safe, repeatable checkpoint in any git repo. This workflow is swarm-safe: it acquires a lock, validates, stages selected files, commits with strict message rules, and optionally pushes.

## Principles

- Automate what is unambiguous; ask when it is not.
- Never switch branches or rewrite history unless explicitly instructed.
- Prefer explicit file selection; avoid "stage everything" by default.
- Abort if the working tree changes mid-run.

## Workflow (Swarm-Safe)

### 1) Acquire Lock

Use a repo-local lock so multiple agents do not collide.

- Lock path: `.git/.checkpoint.lock/`
- Create the lock with an atomic `mkdir`. If it exists, stop and report.
- Write `owner.txt` inside the lock with: user, host, pid, time, branch, worktree.
- Only break the lock if the user explicitly says "force".

If the lock is present, show `owner.txt` and stop. Do not proceed unless told to force.

### 2) Snapshot

- Record `git status -sb` and a diff summary.
- If on `master`, warn and ask for confirmation before continuing.
- If the working tree changes after this point, abort and report.

### 3) Validate

Run the repo's standard checks, but do not guess commands.

- Discover validation instructions from repo docs/config (README, CONTRIBUTING, build scripts, CI notes).
- If the repo does not specify validation steps, ask the user to choose or skip.
- If validation fails, fix and re-run before proceeding.

### 4) Stage

- Show the diff and ask which files to include.
- Stage only the files the user confirms (explicit paths only).
- Re-check `git status` and the diff. If anything changed unexpectedly, abort.

### 5) Commit

Ask for a commit message and enforce these rules (verbatim):

1. Subject <=42 chars (room for ` (#NNNN)` suffix -> 50 char limit)
2. Imperative mood ("Add feature" not "Added feature")
3. Capitalize subject, no period at end
4. Blank line between subject and body
5. Body: explain what and why, wrap at 72 chars
6. Use backticks around `filenames`, `paths`, and `code_symbols`

Use the heredoc pattern:

```bash
git commit -m "$(cat <<'EOF'
<Subject line - imperative, <=42 chars>

<Body - what and why, wrapped at 72 chars>
Use `backticks` around files, paths, symbols.
EOF
)"
```

If commit fails:

- No staged changes -> return to Stage
- Hook failure -> fix, re-stage, create a NEW commit (do not amend)
- Other error -> report and stop

### 6) Push (Optional)

- Ask whether to push unless the user explicitly requested it.
- If pushing: fetch first. If remote advanced or diverged, stop and ask.
- Push only the current branch.

### 7) Confirm and Release

- Summarize what happened (files staged, commit SHA, push status).
- Remove the lock directory only after completion.

## Notes

- No PR or Graphite steps in this skill.
- The lock directory is created by this workflow to prevent collisions; it is safe to remove only when no checkpoint is running.
