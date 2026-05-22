---
name: git-worktree-manager
description: Manage git worktrees for efficient multi-branch development. Use when you need to create worktrees for feature branches, organize worktree directories, clean up unused worktrees, or implement worktree-based workflows.
---

# Git Worktree Manager

Manage git worktrees to enable efficient multi-branch development while keeping the main working directory clean.

## Purpose

Enable parallel development on multiple branches without switching contexts, allowing isolation and organization of work across multiple features, bugfixes, and experiments.

## When to Use

Use this skill when:
- **Creating Worktrees**: Setting up worktrees for new feature branches
- **Organizing Worktrees**: Structuring worktree directories for better management
- **Cleaning Up**: Removing unused or orphaned worktrees
- **Multi-Branch Development**: Working on multiple features simultaneously
- **Isolated Development**: Keeping experimental changes separate from main work
- **CI/CD Workflows**: Using worktrees for testing and deployment
- **Worktree Maintenance**: Listing, switching, and managing multiple worktrees

## Worktree Fundamentals

### What is a Git Worktree?

A git worktree is a linked working tree attached to the same repository. Each worktree allows you to:
- Check out different branches simultaneously
- Work on multiple features in parallel
- Keep main working directory clean
- Test changes without switching branches

### Directory Structure

Recommended organization:
```
project/
├── main-repo/          # Main working directory (default)
└── worktrees/          # All worktrees organized here
    ├── feature/feature-1/
    ├── bugfix/bug-2/
    ├── hotfix/critical-3/
    └── experiment/new-architecture/
```

### Naming Conventions

- **Branch-Based**: Name worktrees after their branches
- **Type Prefix**: Use prefixes for organization (feature/, bugfix/, hotfix/, experiment/)
- **Descriptive Names**: Clear, meaningful names that indicate purpose
- **No Special Characters**: Avoid spaces, special characters in names

## Core Operations

### 1. Create a Worktree

#### From Existing Branch
```bash
# Navigate to main repository
cd /path/to/project

# Create worktree from existing branch
git worktree add ../worktrees/feature-name feature-branch-name

# Verify creation
cd ../worktrees/feature-name
git status
```

#### Create New Branch
```bash
# Create worktree with new branch
git worktree add -b feature/new-feature ../worktrees/new-feature

# Switch to worktree
cd ../worktrees/new-feature
```

#### Detached HEAD Worktree
```bash
# Create worktree at specific commit
git worktree add ../worktrees/temp-checkout HEAD~5
```

### 2. List Worktrees

#### Basic Listing
```bash
# List all worktrees
git worktree list

# List with porcelain format (machine-readable)
git worktree list --porcelain
```

#### Detailed Status Check
```bash
# Check status of all worktrees
for wt in $(git worktree list --porcelain | grep worktree | sed 's/worktree //'); do
    echo "=== $wt ==="
    cd "$wt" && git status --short && git log --oneline -1
done
```

### 3. Navigate Between Worktrees

#### Quick Navigation
```bash
# Function to navigate to worktree
goto-worktree() {
    local wt=$1
    local project_root=$(git rev-parse --show-toplevel)
    local worktree_path="$project_root/../worktrees/$wt"
    
    if [ -d "$worktree_path" ]; then
        cd "$worktree_path"
        echo "Switched to worktree: $wt"
    else
        echo "Worktree not found: $wt"
    fi
}
```

#### Use with Projects
```bash
# In .bashrc or .zshrc
alias gwt='goto-worktree'

# Then use:
gwt feature-name
```

### 4. Manage Worktree Status

#### Lock and Unlock
```bash
# Lock a worktree (prevent operations)
git worktree lock ../worktrees/feature-name

# Unlock a worktree
git worktree unlock ../worktrees/feature-name

# Check locked status
git worktree list
```

#### Prune Worktrees
```bash
# Clean up worktree administrative data
git worktree prune

# Prune with verbose output
git worktree prune -v
```

## Worktree Cleanup

### Identify Unused Worktrees

#### Check for Orphaned Worktrees
```bash
# Find worktrees with deleted branches
git worktree list | while read path commit branch; do
    if ! git show-ref --verify --quiet "refs/heads/${branch#*/}"; then
        echo "Orphaned: $path ($branch)"
    fi
done
```

#### Check for Uncommitted Changes
```bash
# List worktrees with uncommitted changes
for wt in $(git worktree list --porcelain | grep worktree | sed 's/worktree //'); do
    if [ -n "$(cd "$wt" && git status --porcelain)" ]; then
        echo "Uncommitted changes: $wt"
    fi
done
```

### Safe Removal

#### Remove a Worktree
```bash
# Safe removal (if clean)
git worktree remove ../worktrees/feature-name

# Force removal (ignores uncommitted changes)
git worktree remove --force ../worktrees/feature-name
```

#### Remove Multiple Worktrees
```bash
# Remove all worktrees matching pattern
for wt in ../worktrees/feature-*; do
    git worktree remove "$wt"
done
```

## Workflow Integration

### Feature Development Workflow
```markdown
1. Create worktree for new feature
   ```bash
   git worktree add -b feature/new-ui ../worktrees/feature/new-ui
   ```

2. Develop feature in isolation
   ```bash
   cd ../worktrees/feature/new-ui
   # ... develop feature ...
   ```

3. Test changes locally
   ```bash
   cargo test
   ```

4. Commit and push to branch
   ```bash
   git add .
   git commit -m "Implement new UI"
   git push
   ```

5. Merge back to main
   ```bash
   cd /path/to/main-repo
   git checkout main
   git merge feature/new-ui
   ```

6. Clean up worktree
   ```bash
   git worktree remove ../worktrees/feature/new-ui
   ```
```

### Parallel Testing Workflow
```bash
# Test multiple branches simultaneously
for branch in feature/a feature/b feature/c; do
    git worktree add ../worktrees/$branch $branch
    cd ../worktrees/$branch
    cargo test &
done

# Wait for all tests to complete
wait
```

### Bugfix Workflow
```bash
# Create worktree for urgent bugfix
git worktree add -b hotfix/critical-issue ../worktrees/hotfix/critical-issue

# Fix and test in isolation
cd ../worktrees/hotfix/critical-issue
# ... fix bug ...

# Test thoroughly
cargo test

# Merge to release branch
git checkout release/v1.2
git merge hotfix/critical-issue

# Clean up
git worktree remove ../worktrees/hotfix/critical-issue
```

### CI/CD Integration
```yaml
# GitHub Actions workflow example
- name: Test with Worktrees
  run: |
    # Create worktree for testing
    git worktree add /tmp/ci-test $GITHUB_SHA
    
    # Run tests in worktree
    cd /tmp/ci-test
    cargo test --all
    
    # Clean up
    rm -rf /tmp/ci-test
```

### Code Review Workflow
```bash
# Create worktree for PR review
git worktree add ../worktrees/review/pr-123 origin/pr-123

# Review changes in isolation
cd ../worktrees/review/pr-123
# ... review code ...

# Run tests
cargo test

# Clean up after review
git worktree remove ../worktrees/review/pr-123
```

## Git Configuration

### Worktree-Specific Configuration
```bash
# Configure behavior in specific worktree
cd ../worktrees/feature-name

# Set up local Git config
git config user.name "Developer Name"
git config user.email "developer@example.com"

# Configure branch-specific settings
git config branch.feature-name.mergeoptions "no-ff"
```

### Aliases for Common Operations
```bash
# Add to ~/.gitconfig
[alias]
    wt-list = worktree list
    wt-add = "!f() { git worktree add ../worktrees/$1 ${2:--b $2}; }; f"
    wt-remove = "!f() { git worktree remove ../worktrees/$1; }; f"
    wt-prune = worktree prune
```

## Best Practices

### DO:
✓ Organize worktrees in dedicated directory (../worktrees/)
✓ Use descriptive branch names and worktree paths
✓ Clean up worktrees after merging or abandoning work
✓ Test in worktree before merging to main branch
✓ Use worktrees for isolated, parallel development
✓ Prune worktrees regularly to remove orphaned data
✓ Lock worktrees during automated operations
✓ Verify worktree status before major operations

### DON'T:
✗ Create worktrees in random locations
✗ Use worktrees as long-term storage (use branches instead)
✗ Leave worktrees with uncommitted changes indefinitely
✗ Forget to prune worktree administrative data
✗ Create worktrees with conflicting branches
✗ Mix worktree and non-worktree workflows without clear separation
✗ Remove worktrees without checking for uncommitted changes
✗ Use worktrees for unrelated changes (keep them focused)

## Advanced Patterns

### Main Branch Protection
```bash
# Keep main branch clean
# Never commit directly to main from worktree
# Always create feature branches from main
# Merge feature branches into main from main checkout

# Example safe workflow:
# 1. In main: create-feature-branch
# 2. In worktree: develop and test
# 3. In main: merge-feature-branch
# 4. Remove worktree
```

### Worktree Isolation
```bash
# Each worktree is isolated environment
# No shared state between worktrees
# Each worktree has its own .git/config
# Changes in worktree don't affect main until merged
```

### Stashing in Worktrees
```bash
# Stash works independently in each worktree
cd ../worktrees/feature-a
git stash save "WIP feature A"

cd ../worktrees/feature-b
git stash save "WIP feature B"
```

### Submodule Considerations
```bash
# Worktrees interact with submodules carefully
# Each worktree has its own submodule checkout
# Be aware of submodule init/update operations
```

## Troubleshooting

### Common Issues

#### Issue: Worktree Already Exists
```bash
# Error: fatal: 'worktrees/feature-name' already exists
# Solution: Remove existing worktree first
git worktree remove ../worktrees/feature-name
# Then recreate
git worktree add ../worktrees/feature-name feature-branch-name
```

#### Issue: Detached HEAD
```bash
# Worktree in detached HEAD state
# Solution: Check out appropriate branch
cd ../worktrees/feature-name
git checkout feature-branch-name
```

#### Issue: Merge Conflicts
```bash
# Conflicts when merging from worktree
# Solution: Resolve in worktree, then merge
cd ../worktrees/feature-name
git merge main
# Resolve conflicts
git commit
git checkout main
git merge feature-name
```

#### Issue: Large .git Directory
```bash
# Worktrees can bloat .git directory
# Solution: Use prune regularly
git worktree prune
# Consider using sparse checkout for large repos
```

## Tools and Commands Reference

### Quick Reference
```bash
# List all worktrees
git worktree list

# Create from branch
git worktree add ../worktrees/name branch-name

# Create with new branch
git worktree add -b new-branch ../worktrees/name

# Remove worktree
git worktree remove ../worktrees/name

# Force remove
git worktree remove --force ../worktrees/name

# Prune administrative data
git worktree prune

# Move a worktree
git worktree move ../worktrees/old-path ../worktrees/new-path

# Lock worktree
git worktree lock ../worktrees/name

# Unlock worktree
git worktree unlock ../worktrees/name
```

### Status Checking
```bash
# Check all worktree statuses
git worktree list

# Get detailed information
git worktree list --porcelain

# Find worktree for a branch
git worktree list | grep feature-branch-name
```

## Integration with Development Workflows

### With IDE
```bash
# VS Code: Add multiple workspace roots
# Settings -> Workspace -> Add Folder...
# Add: /path/to/project, /path/to/worktrees/*

# JetBrains: Configure multiple project roots
# File -> Open -> Add Directory to Project
```

### With Testing
```bash
# Parallel test execution
for branch in $(git branch -r | grep -v HEAD); do
    git worktree add /tmp/test-$branch $branch
    cd /tmp/test-$branch && cargo test
    rm -rf /tmp/test-$branch
done
```

### With CI/CD
```yaml
# GitHub Actions: Use worktrees for isolated testing
- name: Parallel Testing
  run: |
    for branch in test-1 test-2 test-3; do
      git worktree add /tmp/$branch origin/$branch
      cd /tmp/$branch && cargo test
      rm -rf /tmp/$branch
    done
```

## Maintenance

### Regular Cleanup Schedule
- **Daily**: Prune worktrees
- **Weekly**: Check for orphaned worktrees
- **Monthly**: Review and clean up old worktree directories

### Monitoring
```bash
# Monitor worktree usage
git worktree list | wc -l  # Count active worktrees

# Monitor disk usage
du -sh ../worktrees/

# Check for large .git directories
du -sh .git
```

### Backup Considerations
```bash
# Worktrees don't need separate backups
# All data is in shared git repository
# Main worktree is primary working directory
# Worktrees are temporary workspaces
```

## Summary

Git worktrees enable:
- **Parallel Development**: Multiple branches simultaneously
- **Isolation**: Clean main working directory
- **Flexibility**: Easy to create and remove workspaces
- **Organization**: Structured worktree management
- **Efficiency**: Faster context switching between features

Use worktrees for efficient, isolated multi-branch development while maintaining a clean main working directory.
