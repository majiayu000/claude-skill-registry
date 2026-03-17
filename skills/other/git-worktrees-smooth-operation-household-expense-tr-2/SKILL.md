---
name: git-worktrees
description: "Use when working on multiple features simultaneously. Creates isolated workspaces without branch switching, enabling parallel development."
---

# Git Worktrees

## Core Principle

Work on multiple features in parallel using git worktrees instead of constantly switching branches.

## When to Use This Skill

- Working on multiple features simultaneously
- Need to quickly switch context without stashing
- Want to run tests on one branch while working on another
- Comparing implementations across branches
- Client requests urgent fix while working on feature

## What Are Git Worktrees?

Git worktrees allow you to have multiple working directories for the same repository, each checked out to a different branch.

**Traditional way:**
```bash
git checkout feature-a
[work on feature-a]
git stash
git checkout feature-b
[work on feature-b]
git stash
git checkout feature-a
git stash pop
```

**With worktrees:**
```bash
# Both branches available simultaneously in different directories
cd ../project-feature-a    # Work on feature-a
cd ../project-feature-b    # Work on feature-b
cd ../project-hotfix        # Work on hotfix
```

## Benefits

✅ **No stashing**: Changes stay in their worktree
✅ **Parallel work**: Different features in different terminals
✅ **Independent testing**: Test one branch while coding another
✅ **Quick context switching**: Just `cd` to different directory
✅ **Clean state**: Each worktree is independent

## Git Worktree Basics

### Creating a Worktree

```bash
# Basic syntax
git worktree add <path> <branch>

# Create worktree for existing branch
git worktree add ../project-feature-x feature/feature-x

# Create worktree with new branch
git worktree add -b feature/new-feature ../project-new-feature main

# Create worktree from specific branch
git worktree add ../project-hotfix -b hotfix/security-patch main
```

### Listing Worktrees

```bash
# List all worktrees
git worktree list

# Output example:
# /path/to/project        abc123 [main]
# /path/to/project-auth   def456 [feature/authentication]
# /path/to/project-api    ghi789 [feature/api-refactor]
```

### Removing a Worktree

```bash
# After finishing work and merging the branch
git worktree remove ../project-feature-x

# Or if directory is already deleted
git worktree prune
```

### Moving Between Worktrees

```bash
# Just use cd
cd ../project-auth        # Work on authentication
cd ../project-api         # Work on API
cd ../project             # Back to main worktree
```

## Worktree Workflow Examples

### Example 1: Parallel Feature Development

**Scenario**: Working on authentication (long-term) and need to add quick bug fix

```bash
# Setup main project
cd ~/projects/myapp
git checkout main

# Create worktree for authentication feature
git worktree add -b feature/authentication ../myapp-auth main

# Start working on authentication
cd ../myapp-auth
[make changes, run tests, commit]

# Client reports urgent bug while you're working
# No need to stash! Just create worktree for fix
cd ~/projects/myapp
git worktree add -b fix/urgent-bug ../myapp-bugfix main

# Fix the bug in separate worktree
cd ../myapp-bugfix
[fix bug, test, commit, push]

# Create PR for bug fix
gh pr create --title "fix: resolve urgent bug"

# Bug fix merged, clean up
git worktree remove ../myapp-bugfix

# Continue working on authentication without interruption
cd ../myapp-auth
[continue work...]
```

### Example 2: Testing Across Branches

**Scenario**: Need to compare behavior between main and your feature branch

```bash
# Main worktree
cd ~/projects/myapp    # On main branch

# Feature worktree
git worktree add -b feature/new-api ../myapp-feature main
cd ../myapp-feature
[implement feature]

# Test your feature
./scripts/safe-test.sh npm test

# Compare with main branch behavior
cd ~/projects/myapp    # Main branch
./scripts/safe-test.sh npm test

# Run both simultaneously in different terminals
# Terminal 1: cd ~/projects/myapp && npm run dev
# Terminal 2: cd ../myapp-feature && npm run dev
# Compare on different ports
```

### Example 3: Code Review Workflow

**Scenario**: Reviewing a PR while working on your own feature

```bash
# Your work in progress
cd ~/projects/myapp-my-feature
[your work...]

# Colleague asks for code review on their PR
cd ~/projects/myapp
git fetch origin
git worktree add ../myapp-review-pr123 pr-123

# Review the code
cd ../myapp-review-pr123
[review code, run tests, check functionality]

# Add review comments
gh pr review 123 --comment -b "LGTM! Tested locally, works great."

# Clean up review worktree
cd ~/projects/myapp
git worktree remove ../myapp-review-pr123

# Back to your work without any disruption
cd ../myapp-my-feature
[continue working...]
```

## Worktree Organization Strategies

### Strategy 1: Sibling Directories

```
~/projects/
├── myapp/              # Main worktree (main branch)
├── myapp-auth/         # feature/authentication
├── myapp-api/          # feature/api-refactor
└── myapp-bugfix/       # fix/login-error
```

**Pros**: Easy to see all worktrees, simple paths
**Cons**: Clutters parent directory

### Strategy 2: Subdirectory Organization

```
~/projects/myapp/
├── .git/               # Main repo
├── main/               # Main branch worktree
├── worktrees/
│   ├── auth/          # feature/authentication
│   ├── api/           # feature/api-refactor
│   └── bugfix/        # fix/login-error
```

**Pros**: Organized, all in one place
**Cons**: Slightly longer paths

### Strategy 3: Feature-Based Structure

```
~/projects/myapp/
├── .git/
├── production/         # main branch
├── staging/            # staging branch
├── features/
│   ├── authentication/
│   ├── api-refactor/
│   └── user-profile/
└── fixes/
    ├── login-error/
    └── memory-leak/
```

**Pros**: Very organized, clear purpose
**Cons**: More complex setup

## Worktree Best Practices

### DO:
✅ Name worktree directories clearly (match branch name)
✅ Remove worktrees after branch is merged
✅ Run `git worktree prune` periodically
✅ Use worktrees for truly parallel work
✅ Keep worktrees in predictable locations

### DON'T:
❌ Create too many worktrees (keep it manageable)
❌ Leave stale worktrees around after branches merged
❌ Use worktrees for trivial branch switches
❌ Forget which worktree you're in (use git prompt)

## Worktree Cleanup

### Removing Merged Worktrees

```bash
# After feature is merged, remove worktree
git worktree remove ../myapp-feature

# Delete the merged branch
git branch -d feature/feature-name

# Prune any stale worktree references
git worktree prune
```

### Finding Stale Worktrees

```bash
# List all worktrees
git worktree list

# Check which branches are merged
git branch --merged

# Remove worktrees for merged branches
for worktree in $(git worktree list --porcelain | grep worktree | cut -d' ' -f2); do
    cd $worktree
    branch=$(git branch --show-current)
    if git branch --merged main | grep -q "$branch"; then
        echo "Removing merged worktree: $worktree"
        git worktree remove $worktree
    fi
done
```

## Integration with Skills

**Use with:**
- `dispatching-parallel-agents` - Run multiple agents in different worktrees
- `git-workflow` - Standard git practices apply in each worktree
- `executing-plans` - Execute different plans in parallel
- `code-review` - Review PRs in separate worktrees

**Workflow:**
1. Create worktree for feature: `git worktree add`
2. Work on feature: Use `brainstorming`, `writing-plans`, `executing-plans`
3. Test in worktree: Use `database-backup` for each worktree
4. Review in main worktree: Compare implementations
5. Merge and cleanup: Remove worktree

## Common Issues and Solutions

### Issue 1: Worktree Creation Fails

**Error**: `fatal: 'path' already exists`

**Solution**:
```bash
# Remove the directory first
rm -rf ../myapp-feature
git worktree add ../myapp-feature feature/feature-name

# Or use a different path
git worktree add ../myapp-feature-v2 feature/feature-name
```

### Issue 2: Branch Checked Out in Another Worktree

**Error**: `fatal: 'branch' is already checked out at 'path'`

**Solution**:
```bash
# A branch can only be checked out in one worktree at a time
# Either:
# 1. Remove the existing worktree
git worktree remove path/to/existing/worktree

# 2. Or create with different branch name
git worktree add -b feature/feature-name-v2 ../myapp-feature feature/feature-name
```

### Issue 3: Forgot Which Worktree You're In

**Solution**:
```bash
# Show current worktree path
pwd

# Show current branch
git branch --show-current

# Add to shell prompt (add to .bashrc or .zshrc)
parse_git_branch() {
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}
PS1="\w \$(parse_git_branch) $ "
```

### Issue 4: Stale Worktree References

**Error**: Worktree listed but directory doesn't exist

**Solution**:
```bash
# Prune stale references
git worktree prune -v

# Force remove if needed
git worktree remove --force path/to/worktree
```

## Advanced Worktree Usage

### Worktrees for CI/CD Testing

```bash
# Create worktree for CI testing
git worktree add ../myapp-ci-test feature/feature-name

# Run CI tests in isolation
cd ../myapp-ci-test
./scripts/safe-test.sh npm run ci-test

# Clean up
cd -
git worktree remove ../myapp-ci-test
```

### Worktrees for Deployment Branches

```bash
# Keep production and staging as worktrees
git worktree add ../myapp-production production
git worktree add ../myapp-staging staging

# Deploy from dedicated worktrees
cd ../myapp-production
git pull origin production
[run deployment script]

cd ../myapp-staging
git pull origin staging
[run staging deployment]
```

## Worktree Checklist

Before creating worktree:
- [ ] Do I really need parallel work? (worktrees add complexity)
- [ ] Have I chosen a clear, descriptive path?
- [ ] Is the base branch correct?

While working in worktree:
- [ ] Am I aware which worktree I'm in?
- [ ] Have I committed changes regularly?
- [ ] Am I using proper git workflow in this worktree?

After finishing work:
- [ ] Has the branch been merged?
- [ ] Have I removed the worktree?
- [ ] Have I deleted the merged branch?
- [ ] Have I run `git worktree prune`?

## Authority

**This skill is based on:**
- Git worktrees feature (since Git 2.5)
- Professional development: Parallel work is common
- Efficiency: Context switching is expensive
- Best practices from the Superpowers framework

**Social Proof**: Many professional developers use worktrees for parallel feature development.

## Your Commitment

Before using worktrees:
- [ ] I understand worktrees allow parallel work
- [ ] I will keep worktrees organized
- [ ] I will clean up merged worktrees
- [ ] I will not overuse worktrees (only when needed)

---

**Bottom Line**: Worktrees enable true parallel development. Use them when you need to work on multiple features simultaneously without constant branch switching. Clean up when done.
