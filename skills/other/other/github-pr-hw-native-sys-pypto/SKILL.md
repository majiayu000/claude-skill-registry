---
name: github-pr
description: Create a GitHub pull request after committing, rebasing, and pushing changes. Use when the user asks to create a PR, submit changes for review, or open a pull request.
---

# PyPTO GitHub Pull Request Workflow

## Prerequisites

⚠️ **MANDATORY**: Use the `/git-commit` skill to commit all changes. This runs the full code review, testing, and linting workflow. Do not commit directly.

## Workflow Steps

1. Check for existing PR (exit if found)
2. Fetch upstream changes
3. Rebase onto upstream/main
4. Resolve conflicts if needed
5. Push to fork with `--force-with-lease`
6. Create PR using gh CLI

## Step 1: Check for Existing PR

```bash
BRANCH_NAME=$(git branch --show-current)
gh pr list --head "$BRANCH_NAME" --state open
```

**If PR exists**: Display with `gh pr view` and exit immediately.

## Step 2: Fetch Upstream

```bash
git remote add upstream https://github.com/hw-native-sys/pypto.git  # If needed
git fetch upstream
```

## Step 3: Rebase

```bash
git rebase upstream/main  # Or user-specified branch
```

**On conflicts**:

```bash
git status                     # View conflicts
# Edit files, remove markers
git add path/to/resolved/file
git rebase --continue
# If stuck: git rebase --abort
```

## Step 4: Push

```bash
# First push
git push --set-upstream origin BRANCH_NAME

# After rebase (use --force-with-lease, NOT --force)
git push --force-with-lease origin BRANCH_NAME
```

⚠️ **Use `--force-with-lease`** - safer than `--force`, fails if remote has unexpected changes.

## Step 5: Create PR

**Check gh CLI**:

```bash
gh auth status
```

**If gh NOT available**: Report to user and provide manual URL: `https://github.com/hw-native-sys/pypto/compare/main...BRANCH_NAME`

**If gh available**:

```bash
gh pr create \
  --title "Brief description of changes" \
  --body "$(cat <<'EOF'
## Summary
- Key change 1
- Key change 2

## Testing
- [ ] All tests pass
- [ ] Code review completed
- [ ] Documentation updated

## Related Issues
Fixes #ISSUE_NUMBER (if applicable)
EOF
)"
```

**PR Title/Body**: Auto-extracted from commit messages since upstream/main.

**Important**:

- ❌ Do NOT add footers like "🤖 Generated with Claude Code" or similar branding
- ✅ Keep PR descriptions professional and focused on technical content only

## Common Issues

| Issue | Solution |
| ----- | -------- |
| PR already exists | `gh pr view` then exit |
| Merge conflicts | Resolve, `git add`, `git rebase --continue` |
| Push rejected | `git push --force-with-lease` |
| gh not authenticated | Tell user to run `gh auth login` |
| Wrong upstream branch | Use `git rebase upstream/BRANCH` |

## Checklist

- [ ] No existing PR for branch (exit if found)
- [ ] Changes committed via git-commit
- [ ] Fetched upstream and rebased successfully
- [ ] Conflicts resolved
- [ ] Pushed with `--force-with-lease`
- [ ] PR created with clear title/body

## Remember

- Always rebase before creating PR
- Use `--force-with-lease`, not `--force`
- Don't auto-install gh CLI - let user do it
