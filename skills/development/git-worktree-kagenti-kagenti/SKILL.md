---
name: git:worktree
description: Create and manage git worktrees for parallel development and testing
---

# Git Worktree Skill

Manage git worktrees for parallel development workflows.

## When to Use

- Need to work on multiple branches simultaneously
- Testing features in isolation
- Reviewing PRs without switching branches
- Running CI-like tests locally

## Quick Start

### Create Worktree

```bash
# New branch from main
git worktree add .worktrees/<name> -b <branch-name> main

# Existing branch
git worktree add .worktrees/<name> <existing-branch>

# Specific commit
git worktree add .worktrees/<name> <commit-sha>
```

### List Worktrees

```bash
git worktree list
```

### Remove Worktree

```bash
# Normal remove
git worktree remove .worktrees/<name>

# Force remove (discards changes)
git worktree remove --force .worktrees/<name>

# Prune stale references
git worktree prune
```

## Recommended Workflow

### 1. Create Feature Worktree

```bash
# Create worktree for new feature
git worktree add .worktrees/feature-auth -b feature-auth main
cd .worktrees/feature-auth
```

### 2. Work in Worktree

```bash
# Make changes, commit, push
git add .
git commit -m "Add auth feature"
git push -u origin feature-auth
```

### 3. Deploy and Test from Worktree

```bash
# Source environment
source ~/.kagenti-hypershift-env.sh

# Deploy from worktree to cluster
KUBECONFIG=$HOSTED_KUBECONFIG ./deployments/ansible/run-install.sh --env ocp

# Or use local-setup scripts
./.github/scripts/local-setup/kind-full-test.sh --skip-cluster-destroy
```

### 4. Clean Up

```bash
# Return to main
cd /path/to/main/repo

# Remove worktree
git worktree remove .worktrees/feature-auth

# Delete branch if merged
git branch -d feature-auth
```

## Directory Structure

Keep worktrees organized:

```
kagenti/                    # Main worktree (main branch)
├── .worktrees/             # Feature worktrees
│   ├── feature-auth/       # Auth feature
│   ├── fix-keycloak/       # Bug fix
│   └── pr-review-123/      # PR review
└── ...
```

Add to `.git/info/exclude`:
```
.worktrees/
```

## Using with TODO Docs

Point worktree work to a TODO document in the main repo:

```bash
# Create worktree for TODO item
git worktree add .worktrees/todo-phoenix -b todo-phoenix main
cd .worktrees/todo-phoenix

# Reference TODO from main repo
cat /path/to/main/repo/docs/TODO_PHOENIX.md

# Implement based on TODO
# ...

# Test deployment
./.github/scripts/local-setup/hypershift-full-test.sh --skip-cluster-destroy
```

## Using with HyperShift

Test worktree code on HyperShift clusters:

```bash
# Create worktree
git worktree add .worktrees/my-feature -b my-feature main
cd .worktrees/my-feature

# Source environment (shared kubeconfig)
source ~/.kagenti-hypershift-env.sh

# Deploy to existing cluster
KUBECONFIG=$HOSTED_KUBECONFIG ./deployments/ansible/run-install.sh --env ocp

# Or create new cluster with this code
./.github/scripts/local-setup/hypershift-full-test.sh --skip-cluster-destroy
```

## Using with Kind

Test worktree code on local Kind cluster:

```bash
# Create worktree
git worktree add .worktrees/my-feature -b my-feature main
cd .worktrees/my-feature

# Full test cycle
./.github/scripts/local-setup/kind-full-test.sh --skip-cluster-destroy

# Access UI
./.github/scripts/kind/access-ui.sh
```

## Best Practices

1. **Use .worktrees/ directory**: Keep worktrees in one place
2. **Name descriptively**: `feature-auth`, `fix-keycloak`, `pr-123`
3. **Share kubeconfigs**: Store in `$HOME`, not in worktree
4. **Clean up regularly**: Remove merged worktrees
5. **Prune stale refs**: Run `git worktree prune` periodically

## Troubleshooting

### Branch already checked out

```bash
# Find which worktree has the branch
git worktree list | grep <branch-name>
```

### Worktree already exists

```bash
# Remove existing worktree
git worktree remove .worktrees/<name>
# Or force if changes exist
git worktree remove --force .worktrees/<name>
```

### Stale worktree references

```bash
# Prune after manually deleting worktree directories
git worktree prune
```

## Related Skills

- **tdd:ci**: CI-driven TDD workflow (auto-creates worktree from upstream/main for GH issues/PRs)
- **kind:cluster**: Local Kind cluster management
- **hypershift:cluster**: HyperShift cluster management
- **kagenti:operator**: Deploy Kagenti platform
