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
version: 1.3.5
---

# Git Workspace Review

## Usage

Use this skill before workflows that depend on repository state, such as commit message generation, PR preparation, or release notes. Run it once per session or whenever staged changes are modified.

## Required Progress Tracking

1. `git-review:repo-confirmed`
2. `git-review:status-overview`
3. `git-review:code-quality-check`
4. `git-review:diff-stat`
5. `git-review:diff-details`

Mark each item as complete as you finish the corresponding step.

## Step 1: Confirm Repository (`repo-confirmed`)

Run `pwd` to confirm you are in the correct repository directory. Execute `git status -sb` to view the current branch and short status, then capture the branch name and upstream information.

## Step 2: Review Status Overview (`status-overview`)

Analyze the `git status -sb` output for staged and unstaged changes. Stage or unstage files so that subsequent workflows operate on the intended diff.

## Step 3: Check Code Quality (`code-quality-check`)

Run `make format && make lint` to validate code quality before committing. Fix any errors immediately. Do not bypass pre-commit hooks with `--no-verify`. This check identifies issues early and avoids late-stage pipeline failures.

## Step 4: Review Diff Statistics (`diff-stat`)

Run `git diff --cached --stat` for staged changes (or `git diff --stat` for unstaged work). Note the number of files modified and identify hotspots with large insertion or deletion counts.

## Step 5: Review Detailed Diff (`diff-details`)

Run `git diff --cached` to examine the actual changes. For unstaged work, use `git diff`. Identify key themes, such as Makefile adjustments or new skill additions, to provide context for downstream summaries.

## Exit Criteria

Complete all progress tracking items. You should have a clear understanding of modified files and areas, and the correct work should be staged. Subsequent workflows can then rely on this context without re-executing git commands.

## Troubleshooting

If pre-commit hooks block a commit, resolve the reported issues instead of using `--no-verify`. Run `make format` to fix styling errors automatically and use `make lint` to isolate logical failures. If merge conflicts occur, use `git merge --abort` to return to a clean state before retrying.
