---
name: ship
description: Commit, push, create PR, then after approval check CI and merge. Use when work is done and ready to ship.
user-invocable: true
---

# Ship

Finalize the current feature branch: commit, push, create a PR, wait for approval, check CI, and merge.

## Step 1: Verify branch

Run `git branch --show-current` and confirm you are NOT on `main` or `master`. If you are, STOP and tell the user to check out a feature branch first.

```bash
git branch --show-current
```

If the branch is `main` or `master`, abort with:
> "You are on `main`. Please check out a feature branch before shipping."

## Step 2: Check for changes

Run `git status` and `git diff --stat` to see what needs to be committed.

- If there are no staged or unstaged changes and no untracked files, skip to Step 4 (push).
- If there are changes, proceed to Step 3.

```bash
git status
git diff --stat
```

## Step 3: Commit

1. Run `git diff` (staged + unstaged) to understand all changes.
2. Run `git log --oneline -5` to match the repo's commit message style.
3. Stage relevant files (use specific file names, never `git add -A`). Do NOT stage files that look like secrets (`.env`, credentials).
4. Write a concise commit message summarizing the changes.
5. Commit using a HEREDOC:

```bash
git commit -m "$(cat <<'EOF'
feat: <description>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

## Step 4: Push

Push the branch to origin. Use `-u` if this is the first push.

```bash
git push -u origin $(git branch --show-current)
```

## Step 5: Create PR

Check if a PR already exists for this branch:

```bash
gh pr view --json number,title,url 2>&1
```

- If a PR already exists, skip to Step 6.
- If no PR exists, create one:

1. Run `git log --oneline main..HEAD` to understand all commits on this branch.
2. Run `git diff main...HEAD --stat` for a change summary.
3. Create the PR:

```bash
gh pr create --title "<short title>" --body "$(cat <<'EOF'
## Summary
<bullet points summarizing changes>

## Test plan
<checklist of testing steps>

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

4. Report the PR URL to the user.

## Step 6: Wait for approval

Tell the user:
> "PR is ready for review: <URL>. Let me know when it's approved and I'll check CI and merge."

**STOP HERE.** Do NOT proceed until the user explicitly says to merge or confirms approval.

## Step 7: Check CI status

After user confirmation, check the CI status:

```bash
gh pr checks $(gh pr view --json number -q .number)
```

- If all checks pass, proceed to Step 8.
- If checks are failing, report the failures and offer to investigate with `/fix-ci`.
- If checks are still running, wait 30 seconds and check again (up to 3 retries).

## Step 8: Merge

Merge the PR using squash merge:

```bash
gh pr merge --squash --delete-branch
```

After successful merge, clean up any associated worktree:

```bash
BRANCH=$(gh pr view --json headRefName -q .headRefName 2>/dev/null || echo "")
if [ -n "$BRANCH" ]; then
  git worktree list | grep "$BRANCH" | awk '{print $1}' | while read wt; do
    [ -n "$wt" ] && git worktree remove "$wt" --force 2>/dev/null || true
  done
fi
git worktree prune
```

Report success:
> "PR merged and branch cleaned up."

## Safety rules

- NEVER force push
- NEVER merge without user confirmation
- NEVER merge if CI is failing
- NEVER commit `.env`, credentials, or secrets
- NEVER push to `main` directly
