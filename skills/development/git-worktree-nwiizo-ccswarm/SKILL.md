# Git Worktree Workflow

Multi-step workflow for parallel development using git worktrees.

## Overview

Git worktree allows working on multiple branches simultaneously. Each worktree is an independent working directory with its own branch.

## Setup Workflow

### 1. Create Feature Worktree
```bash
git worktree add ../ccswarm-feature-<name> feature/<description>
```

### 2. Create Bug Fix Worktree
```bash
git worktree add ../ccswarm-bugfix-<name> hotfix/<description>
```

### 3. Create Experiment Worktree
```bash
git worktree add ../ccswarm-experiment-<name> experiment/<description>
```

## Recommended Structure

```
github.com/nwiizo/
├── ccswarm/                  # Main repository (master)
├── ccswarm-feature-*/        # Feature worktrees
├── ccswarm-bugfix-*/         # Bug fix worktrees
├── ccswarm-hotfix-*/         # Hotfix worktrees
└── ccswarm-experiment-*/     # Experimental worktrees
```

## Management Commands

```bash
# List all worktrees
git worktree list

# Remove worktree after merging
git worktree remove ../ccswarm-feature-<name>

# Prune stale worktree information
git worktree prune
```

## Agent Integration

Each agent can work in its own worktree:

```bash
# Frontend agent
git worktree add ../ccswarm-frontend feature/ui-redesign

# Backend agent
git worktree add ../ccswarm-backend feature/api-enhancement

# DevOps agent
git worktree add ../ccswarm-devops feature/ci-cd-improvement
```

## Best Practices

1. One worktree per feature/bug
2. Use naming convention: `ccswarm-<type>-<description>`
3. Clean up after merging
4. Run `git worktree prune` periodically
5. Run tests in different worktrees simultaneously
