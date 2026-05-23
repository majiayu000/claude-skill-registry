---
name: github-pr-merge
description: Merges GitHub Pull Requests after validating pre-merge checklist. Use when user wants to merge PR, close PR, finalize PR, complete merge, approve and merge, or execute merge. Runs pre-merge validation (tests, lint, CI, comments), confirms with user, merges with proper format, handles post-merge cleanup.
---

# GitHub PR Merge

Merges Pull Requests after validating pre-merge checklist and handling post-merge cleanup.

## Quick Start

```bash
# 1. Get PR info
PR=$(gh pr view --json number -q '.number')
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')

# 2. Run pre-merge checklist
make test && make lint && gh pr checks $PR

# 3. Verify all comments replied
gh api repos/$REPO/pulls/$PR/comments --jq '[.[] | select(.in_reply_to_id == null)] | length'

# 4. Merge with concise message (--delete-branch auto-deletes remote)
gh pr merge $PR --merge --delete-branch --body "- Change 1
- Change 2

Reviews: N/N addressed
Tests: X passed (Y% cov)
Refs: Task N"

# 5. Post-merge cleanup (local only, remote already deleted)
git checkout develop && git pull && git branch -d feature/<name>
```

## Pre-Merge Checklist

**ALWAYS verify before merging:**

| Check | Command | Required |
|-------|---------|----------|
| Tests passing | `make test` | Yes |
| Linting passing | `make lint` or `make check` | Yes |
| CI checks green | `gh pr checks $PR` | Yes |
| All comments replied | Verify only, don't reply | Yes |
| No unresolved threads | Review PR page | Yes |

## Core Workflow

### 1. Identify PR

```bash
PR=$(gh pr view --json number -q '.number')
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
echo "PR #$PR in $REPO"
```

### 2. Check Comments Status

```bash
# Count original comments (not replies)
ORIGINALS=$(gh api repos/$REPO/pulls/$PR/comments --jq '[.[] | select(.in_reply_to_id == null)] | length')

# Count comments that have at least one reply
REPLIED=$(gh api repos/$REPO/pulls/$PR/comments --jq '
  [.[] | select(.in_reply_to_id)] | [.[].in_reply_to_id] | unique | length
')

echo "Original comments: $ORIGINALS, With replies: $REPLIED"

# Find unreplied comment IDs
UNREPLIED=$(gh api repos/$REPO/pulls/$PR/comments --jq '
  [.[] | select(.in_reply_to_id) | .in_reply_to_id] as $replied_ids |
  [.[] | select(.in_reply_to_id == null) | select(.id | IN($replied_ids[]) | not) | .id]
')
echo "Unreplied: $UNREPLIED"
```

All original comments should have at least one reply.

**If unreplied comments exist:**
- DO NOT reply from this skill
- STOP the merge process
- Inform user: "Found unreplied comments: [IDs]. Run github-pr-review first."
- Show which comment IDs are missing replies

### 3. Run Validation

```bash
# Activate venv if Python project
source venv/bin/activate 2>/dev/null

# Run tests
make test

# Run linting
make lint  # or: make check

# Check CI status
gh pr checks $PR
```

**All checks MUST pass before proceeding.**

### 4. Show PR Summary

```bash
gh pr view $PR --json title,body,commits,changedFiles --jq '
  "Title: \(.title)\nCommits: \(.commits | length)\nFiles: \(.changedFiles)"
'
```

### 5. Confirm with User

**ALWAYS ask before merging:**
```
Pre-merge checklist verified:
- Tests: passing
- Lint: passing
- CI: green
- Comments: all replied

Ready to merge PR #X. Proceed?
```

### 6. Execute Merge

```bash
gh pr merge $PR --merge --delete-branch --body "$(cat <<'EOF'
- Key change 1
- Key change 2
- Key change 3

Reviews: N/N addressed
Tests: X passed (Y% cov)
Refs: Task N, Req M
EOF
)"
```

**Merge strategy**: Always use `--merge` (merge commit), never squash or rebase per project guidelines.

**Note**: `--delete-branch` automatically deletes the remote branch after merge.

### 7. Post-Merge Cleanup

```bash
# Switch to develop and update (--delete-branch already deleted local+remote)
git checkout develop
git pull origin develop
```

**Note**: If you didn't use `--delete-branch`, manually delete:
```bash
git branch -d feature/<branch-name>           # local
git push origin --delete feature/<branch-name> # remote
```

## Merge Message Format

**Concise format** (recommended for clean git log):

```
- Key change 1 (what was added/fixed)
- Key change 2
- Key change 3

Reviews: 7/7 addressed (Gemini 5, Codex 2)
Tests: 628 passed (88% cov)
Refs: Task 8, Req 14-15
```

**Guidelines**:
- 3-5 bullet points max for changes
- One line for reviews summary
- One line for test results
- One line for task/requirement references
- No headers (##), no verbose sections
- Total: ~10 lines max

## Important Rules

- **ALWAYS** run full pre-merge checklist before merging
- **ALWAYS** verify all review comments have replies
- **ALWAYS** confirm with user before executing merge
- **ALWAYS** use merge commit (--merge), never squash/rebase
- **ALWAYS** delete feature branch after successful merge
- **NEVER** merge with failing tests or lint
- **NEVER** merge with unresolved CI checks
- **NEVER** skip user confirmation
- **NEVER** reply to PR comments from this skill - use github-pr-review instead
- **STOP** merge if unreplied comments exist and direct user to review skill

## Error Handling

**Tests failing**: Stop and inform user. Do not merge.

**Lint errors**: Stop and inform user. Do not merge.

**CI checks pending**: Wait or inform user. Do not merge.

**Unreplied comments**: List unreplied comment IDs. DO NOT reply from this skill.
Tell user: "Found N unreplied comments: [IDs]. Run github-pr-review to address them before merge."

**Branch protection**: If merge fails due to protection rules, inform user of required approvals.

## Related Skills

- **github-pr-review** - For resolving review comments before merge
- **github-pr-creation** - For creating PRs (this skill handles the merge)
- **git-commit** - For commit message format during PR work

## When to use this skill

Merges GitHub Pull Requests after validating pre-merge checklist. Use when user wants to merge PR, close PR, finalize PR, complete merge, approve and merge, or execute merge. Runs pre-merge validation (tests, lint, CI, comments), confirms with user, merges with proper format, handles post-merge cleanup.

## How to use this skill

Refer to the instructions above or standard agent usage for this skill type.
