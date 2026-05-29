---
name: git-workspace-review
description: |

Triggers: staged, preflight, git, review, status
  Lightweight preflight checklist for verifying repo path, staged changes, and
  diffs before other workflows.

  Triggers: git status, preflight, workspace check, staged changes, diff review,
  git verification, repo state

  Use when: verifying workspace state before other git operations, checking
  staged changes, preflight checks before commits or PRs

  DO NOT use when: full commit workflow - use commit-messages instead.
  DO NOT use when: full PR preparation - use pr-prep.

  Use this skill as foundation for git workflows.
category: workspace-ops
tags: [git, preflight, status, diff, staged]
tools: [Bash, TodoWrite]
complexity: low
estimated_tokens: 500
dependencies:
  - sanctum:shared

# Claude Code 2.1.0+ lifecycle hooks
hooks:
  PreToolUse:
    - matcher: "Bash"
      command: |
        # Log git analysis commands
        if echo "$CLAUDE_TOOL_INPUT" | grep -qE "git (status|diff|log|show|branch)"; then
          echo "[skill:git-workspace-review] Git analysis initiated: $(date)" >> ${CLAUDE_CODE_TMPDIR:-/tmp}/skill-audit.log
        fi
      once: true  # Log once per skill invocation
  Stop:
    - command: |
        echo "[skill:git-workspace-review] === Analysis completed at $(date) ===" >> ${CLAUDE_CODE_TMPDIR:-/tmp}/skill-audit.log
---

# Git Workspace Review

## When to Use
Use this skill before any workflow that depends on understanding current changes (commit messages, PR prep, release notes, etc.).
Run once per session or whenever staged changes are updated.

## Required TodoWrite Items
1. `git-review:repo-confirmed`
2. `git-review:status-overview`
3. `git-review:code-quality-check`
4. `git-review:diff-stat`
5. `git-review:diff-details`

Mark each item as complete as you finish the corresponding step.

## Step 1: Confirm Repository (`repo-confirmed`)
- Run `pwd` to validate you are inside the correct repository.
- Run `git status -sb` to see the branch and short status.
- Capture the branch name and upstream information.

## Step 2: Review Status Overview (`status-overview`)
- Review the `git status -sb` output for staged vs. unstaged changes.
- Stage or unstage files as needed so downstream workflows operate on the intended diff.

## Step 3: Check Code Quality (`code-quality-check`)
- Run `make format && make lint` to validate code quality BEFORE committing
- If errors are found, fix them immediately
- **NEVER proceed to commit with `--no-verify`** - pre-commit hooks exist to enforce quality
- This proactive check prevents pre-commit hook failures later

## Step 4: Review Diff Statistics (`diff-stat`)
- Run `git diff --cached --stat` for staged changes (or `git diff --stat` if nothing is staged yet).
- Note the number of files touched and any hotspots (large insert/delete counts).

## Step 5: Review Detailed Diff (`diff-details`)
- Run `git diff --cached` to skim the actual changes.
- If working with unstaged work, use `git diff`.
- Capture key themes (e.g., "Makefile target adjustments," "New skill added").
- These notes feed downstream summaries.

## Exit Criteria
- `TodoWrite` items are completed.
- You understand which files and areas have changed and have staged the correct work.
- Downstream workflows (commit, PR, etc.) can now rely on this context without re-running Git commands.
## Troubleshooting

### Common Issues

If pre-commit hooks block you, fix the issues; do not use `--no-verify`. Run `make format` to resolve styling errors automatically. For lint failures, use `make lint` to pinpoint the cause. If merge conflicts arise, `git merge --abort` lets you retry safely.
