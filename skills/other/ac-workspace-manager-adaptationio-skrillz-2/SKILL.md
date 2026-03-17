---
name: ac-workspace-manager
description: Manage git worktrees for isolated development. Use when creating isolated workspaces, managing parallel development, handling worktree lifecycle, or merging completed work.
---

# AC Workspace Manager

Manage git worktrees for isolated autonomous development.

## Purpose

Provides workspace isolation using git worktrees, enabling parallel development and safe rollback without affecting the main branch.

## Quick Start

```python
from scripts.workspace_manager import WorkspaceManager

manager = WorkspaceManager(project_dir)
worktree = await manager.create_worktree("feature-auth")
await manager.merge_completed(worktree)
```

## Worktree Strategy

```
main branch (stable)
│
├── .worktrees/
│   ├── build-001/  ← Isolated worktree
│   ├── build-002/  ← Another build
│   └── build-003/  ← Parallel work
│
└── project files
```

## Workflow

1. **Create**: New worktree from main branch
2. **Develop**: All changes in isolated workspace
3. **Review**: Review changes before merge
4. **Merge**: Merge back to main
5. **Cleanup**: Remove worktree

## API

```python
# Create new worktree
worktree = await manager.create_worktree("build-001")

# Get current worktree
current = await manager.get_current_worktree()

# List all worktrees
worktrees = await manager.list_worktrees()

# Merge completed work
await manager.merge_completed(worktree)

# Cleanup worktree
await manager.cleanup_worktree(worktree)
```

## Integration

- Used by: `ac-session-manager` for session isolation
- Uses: `ac-checkpoint-manager` for rollback points

## API Reference

See `scripts/workspace_manager.py` for full implementation.
