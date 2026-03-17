---
name: complete-task
description: "Complete an in-progress task by running clean-code, staging, committing, and closing the bead. Use after /verify-task."
allowed-tools: "Read,Bash(bd:*),Bash(make:*),Bash(git:*),Bash(npm:*),Grep,Glob,Skill,AskUserQuestion"
version: "1.1.0"
author: "flurdy"
---

# Complete Task

Run clean-code, stage, commit, and close an in-progress task — the finalization phase of the development workflow.

## When to Use

- Code changes are verified and ready to commit
- After `/verify-task` has passed (or verification is not needed)
- Replacing manual Phase 3 (Commit and Close) steps

## Prerequisites

Run `/verify-task` before this skill to confirm requirements are met and test coverage is adequate. If you haven't verified yet, do that first.

## Usage

```
/complete-task              # Auto-detect in-progress bead
/complete-task <bead-id>    # Complete a specific bead
```

## Instructions

### 1. Identify the Task

Determine which bead is being completed:

```bash
# If bead ID provided, use it directly
bd show <bead-id>

# Otherwise, find the in-progress bead
bd list --status=in_progress
```

If multiple beads are in progress, ask the user which one to complete.
If no beads are in progress, ask the user what to do.

### 2. Run Clean Code

```bash
make clean-code
```

If clean-code fails:

- Fix auto-fixable issues
- Re-run to confirm zero warnings and zero errors
- If issues remain that change behavior, ask the user before fixing

### 3. Stage Changes

Stage only the files changed for this task:

```bash
git add <specific-files>
```

**Rules:**

- Never use `git add -A` or `git add .`
- Never stage root folders only (e.g., `git add src/`)
- Stage specific files or small subdirectories
- Exclude unrelated changes — if unrelated changes exist, leave them unstaged
- Exclude files that likely contain secrets (.env, credentials, etc.)

### 4. Commit

Create a commit using conventional commit format:

```bash
git commit -m "$(cat <<'EOF'
<type>: <concise description>
EOF
)"
```

**Commit message rules:**

- Use conventional commit prefix: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `perf:`, `test:`
- Infer the type from the bead type (feature → `feat:`, bug → `fix:`, task → contextual)
- Keep the message concise (1-2 sentences) focused on the "why"
- Do not push to remote

### 5. Close the Bead

Only after the commit succeeds:

```bash
bd close <bead-id> --reason="<brief summary of what was done>"
```

Never close a bead if the commit failed or changes are still uncommitted.

### 6. Check for Follow-Up Work

After closing:

- If implementation revealed new issues or TODOs, mention them to the user
- Suggest creating follow-up beads if appropriate (but don't auto-create)

### 7. Sync

```bash
bd sync
```

### 8. Report

Summarize what was done:

- Bead closed with ID and title
- Commit hash and message
- Files changed count
- Any follow-up items noted

## Handling Edge Cases

- **No in-progress beads**: Ask user if they want to complete uncommitted work without a bead, or create one first
- **Multiple in-progress beads**: List them and ask user to pick
- **Clean-code fails repeatedly**: After 2 attempts, ask user for guidance
- **No changes to commit**: Inform user there's nothing to commit; ask if the bead should still be closed
- **Unrelated unstaged changes**: Warn user about them; suggest creating a separate bead/commit
- **Commit hook fails**: Investigate the hook failure, fix the underlying issue, and create a new commit (never amend, never skip hooks)

## Rules

- Never use `--no-verify` or skip git hooks
- Never push to remote (leave that to the user or a separate skill)
- Never amend existing commits
- Never close a bead with uncommitted changes
- Always stage specific files, never bulk-add
- If any step fails, stop and inform the user rather than forcing through
