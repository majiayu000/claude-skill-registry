---
name: git-workflow
description: >
  Git operations and pull request workflows. Create PRs, rebase branches,
  resolve conflicts, merge to upstream. Use when ready to create PR or
  when working with git branches and upstream.
---

# Git Workflow

## Committing Work

```bash
cd ~/Code/community-patterns

git add patterns/$GITHUB_USER/pattern.tsx
git commit -m "Add pattern: description"
git push origin main
```

## Getting Updates (Already done in Step 1)

```bash
git fetch upstream
git pull --rebase upstream main
git push origin main
```

## Sharing Work Upstream (Creating Pull Requests)

**IMPORTANT: Wait for user to tell you to create a PR.** Don't push or create PRs automatically.

**Before creating any PR, you MUST update from main and rebase your branch:**

### Step 0: Update and Rebase Before Creating PR

**Use cached repository type from workspace config:**

```bash
# Read IS_FORK from .claude-workspace (set during Step 2)
IS_FORK=$(grep "^is_fork=" .claude-workspace | cut -d= -f2)

# Determine which remote to use
if [ "$IS_FORK" = "true" ]; then
  echo "Working on fork - will fetch from upstream"
  MAIN_REMOTE="upstream"
else
  echo "Working on main repo - will fetch from origin"
  MAIN_REMOTE="origin"
fi
```

**Then fetch latest main and rebase your branch:**

```bash
# Fetch latest main
git fetch $MAIN_REMOTE

# Rebase current branch on top of main
git rebase $MAIN_REMOTE/main

# If rebase succeeds, push (force-with-lease if on feature branch)
if [ "$(git branch --show-current)" != "main" ]; then
  git push origin $(git branch --show-current) --force-with-lease
else
  git push origin main
fi
```

**If rebase has conflicts:**
1. Show conflict files: `git status`
2. Help resolve conflicts
3. Continue: `git rebase --continue`
4. Then push

**Why this matters:**
- Ensures your PR is based on the latest main
- Avoids merge conflicts during PR review
- Makes PR review easier

---

### If User Has Their Own Fork (Most Common)

When user wants to contribute patterns from their fork to upstream:

**Step 1: Ensure changes are committed and pushed to their fork**
```bash
cd ~/Code/community-patterns
git status  # Verify all changes are committed
git push origin main
```

**Step 2: Update and rebase (see Step 0 above)**

**Step 3: Create pull request to upstream**
```bash
gh pr create \
  --repo jkomoros/community-patterns \
  --title "Add: pattern name" \
  --body "$(cat <<'EOF'
## Summary
- Brief description of the pattern
- Key features
- Use cases

## Testing
- [x] Pattern compiles without errors
- [x] Tested in browser at http://localhost:8000
- [x] All features working as expected

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### If Working Directly on jkomoros/community-patterns

**CRITICAL: When working directly on the upstream repository, you MUST use branches and PRs. Direct pushes to main are NOT allowed.**

**Step 1: Create feature branch**
```bash
cd ~/Code/community-patterns
git checkout -b username/feature-name
```

**Step 2: Commit and push branch**
```bash
git add patterns/$GITHUB_USER/
git commit -m "Add: pattern name"
git push origin username/feature-name
```

**Step 3: Update and rebase (see Step 0 above)**

**Step 4: Create pull request**
```bash
gh pr create \
  --title "Add: pattern name" \
  --body "$(cat <<'EOF'
## Summary
- Brief description

## Testing
- [x] Tested and working

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Step 5: Merge with rebase (when approved)**
```bash
gh pr merge PR_NUMBER --rebase --delete-branch
```

### Important Notes

- **Always wait for user permission** before creating PRs
- **All PRs are merged with `--rebase`** (NOT `--squash` or `--merge`)
- This preserves individual commit history
- Commit frequently locally, but only create PR when user asks
- PRs will be reviewed before merging to upstream
- After merge, everyone gets your patterns automatically on next update
