---
name: worktree-management
description: Git worktree management for parallel dotfiles development. Use when user mentions "create worktree", "switch worktree", "delete worktree", "list worktrees", "feature branch", "parallel development", or worktree operations.
---

# Git Worktree Management

git worktreeを使用した並列開発環境の管理。

## Architecture

Each worktree gets isolated Docker resources:

```
workspace/
├── dotfiles/              # main branch
│   └── Container: dotfiles-dotfiles
├── dotfiles-feature-xyz/  # feature/xyz branch
│   └── Container: dotfiles-dotfiles-feature-xyz
└── dotfiles-fix-bug/      # fix/bug branch
    └── Container: dotfiles-dotfiles-fix-bug
```

## Common Operations

### Create New Worktree

```bash
# From dotfiles directory
git worktree add ../dotfiles-feature-xyz feature/xyz

# Move to new worktree
cd ../dotfiles-feature-xyz

# Build Docker environment
make build
make shell
```

### Create from Existing Branch

```bash
git worktree add ../dotfiles-existing existing-branch
```

### List Worktrees

```bash
git worktree list
```

### Delete Worktree

```bash
# Clean Docker resources first
cd ../dotfiles-feature-xyz
make clean

# Remove worktree
cd ../dotfiles
git worktree remove ../dotfiles-feature-xyz

# Force remove if needed
git worktree remove --force ../dotfiles-feature-xyz
```

### Switch Between Worktrees

Simply change directory:

```bash
cd ../dotfiles-feature-xyz
make shell  # Enter this worktree's container
```

## Naming Convention

Use descriptive names:

```bash
# Good
git worktree add ../dotfiles-feature-vim-config feature/vim-config
git worktree add ../dotfiles-fix-tmux-colors fix/tmux-colors

# Bad
git worktree add ../test test-branch
```

## Cleanup

### Remove Single Worktree

```bash
cd worktree-dir
make clean                    # Remove Docker resources
cd ..
git worktree remove worktree-dir
```

### Check All Containers

```bash
make list  # Works from any worktree
```

### Remove All Docker Resources

```bash
make clean-all  # Removes all dotfiles containers
```

## Troubleshooting

### Cannot Delete Worktree

```bash
git worktree remove --force ../worktree-dir
# Or manually:
rm -rf ../worktree-dir
git worktree prune
```

### Branch Already Checked Out

Each branch can only be checked out in one worktree. Use a different branch or remove the existing worktree first.
