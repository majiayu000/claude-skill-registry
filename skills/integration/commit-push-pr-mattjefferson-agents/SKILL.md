---
name: commit-push-pr
description: Commit staged/unstaged changes, push to remote, and create a PR if one doesn't exist. Use when asked to "ship it", "commit push pr", "open a pr", or finish a feature.
---

# Commit, Push, PR

Ship your changes in one workflow: commit, push, and open a PR if needed.

## Process

### 1. Assess the state

```bash
git status
git diff --stat
git log --oneline -5
```

Check what's staged, unstaged, and the recent commit history for message style.

### 2. Commit (safe staging)

**Critical**: Always use explicit file paths. Never use `.` or `-A` without a path.

```bash
# 1. Unstage everything first (prevents accidental inclusions)
git restore --staged :/

# 2. Stage only the specific files you want to commit
git add -A -- path/to/file1 path/to/file2

# 3. Verify what's staged
git diff --staged --stat

# 4. Commit with conventional message
git commit -m "$(cat <<'EOF'
<type>: <description>

<optional body>
EOF
)"
```

**Conventional Commit types**: `feat|fix|refactor|build|ci|chore|docs|style|perf|test`

**Handling deletions**: If a file was deleted, `git add -A -- <path>` still works to stage the deletion.

**Stale lock errors**: If commit fails with "Unable to create index.lock", remove it:
```bash
rm -f "$(git rev-parse --git-dir)/index.lock"
```

### 3. Push

```bash
# Check if branch has upstream
if git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
  git push
else
  git push -u origin HEAD
fi
```

### 4. Check if PR is needed

```bash
# Get current branch and default branch
current=$(git branch --show-current)
default=$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name')
```

**Skip PR creation if**:
- On the default branch (`main`/`master`) — just commit and push, done
- A PR already exists: `gh pr view --json url,state 2>/dev/null`

### 5. Create PR (if not on default branch)

Quick:
```bash
gh pr create --fill
```

With details:
```bash
gh pr create --title "<type>: <description>" --body "$(cat <<'EOF'
## Summary
- <bullet points>

## Test plan
- [ ] <verification steps>
EOF
)"
```

### 6. Report result

Output the PR URL when done.

## Guidelines

- **Never use `git add .` or `git add -A` without explicit paths** — this stages everything including secrets
- Never force push unless explicitly asked
- Don't commit `.env`, credentials, or secrets
- If the working tree is clean and there's nothing to commit, skip to push/PR
- Ask for confirmation if there are uncommitted changes that look unrelated to the task
