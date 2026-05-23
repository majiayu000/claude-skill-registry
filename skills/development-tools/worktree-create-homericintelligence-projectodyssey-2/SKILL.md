---
name: worktree-create
description: "Create isolated git worktrees for parallel development. Use when working on multiple issues simultaneously."
mcp_fallback: none
category: worktree
---

# Worktree Create

Create separate working directories on different branches without stashing changes.

## When to Use

- Starting work on a new issue
- Need to work on multiple issues in parallel
- Want to avoid stashing/context switching overhead
- Testing changes across different branches

## Quick Reference

```bash
# Create worktree for new branch
./scripts/create_worktree.sh <issue-number> <description>

# Example
./scripts/create_worktree.sh 42 "implement-tensor-ops"
# Creates: ../ProjectOdyssey-42-implement-tensor-ops/

# List all worktrees
git worktree list

# Switch worktrees
cd ../ProjectOdyssey-42-implement-tensor-ops
```

## Workflow

1. **Create worktree** - Run create script with issue number and description
2. **Navigate** - `cd` to new worktree directory (parallel to main)
3. **Work normally** - Make changes, commit, push as usual
4. **Switch back** - `cd` to different worktree or main directory
5. **Clean up** - Remove worktree after PR merge (see `worktree-cleanup` skill)

## Error Handling

| Error | Solution |
|-------|----------|
| Branch already exists | Use different branch name or delete old branch |
| Directory exists | Choose different location or remove directory |
| Cannot switch away | Ensure all changes are committed |
| Permission denied | Check directory permissions |

## Directory Structure

```text
parent-directory/
├── ProjectOdyssey/                    # Main worktree (main branch)
├── ProjectOdyssey-42-tensor-ops/      # Issue #42 worktree
├── ProjectOdyssey-73-bugfix/          # Issue #73 worktree
└── ProjectOdyssey-99-experiment/      # Experimental worktree
```

## Best Practices

- One worktree per issue (don't share branches)
- Use descriptive names: `<issue-number>-<description>`
- All worktrees share same `.git` directory
- Clean up after PR merge
- Each branch can only be checked out in ONE worktree

## Multi-Issue Parallel Development

When working on related issues (e.g., Plan → Test/Impl/Package → Cleanup phases):

### Phase-Based Worktree Pattern

```bash
# Phase 1: Plan (sequential, must complete first)
git worktree add ../ProjectOdyssey-62-plan-agents 62-plan-agents

# Phase 2: Parallel development (after Plan complete)
git worktree add ../ProjectOdyssey-63-test-agents 63-test-agents
git worktree add ../ProjectOdyssey-64-impl-agents 64-impl-agents
git worktree add ../ProjectOdyssey-65-pkg-agents 65-pkg-agents

# Phase 3: Cleanup (after parallel phases complete)
git worktree add ../ProjectOdyssey-66-cleanup-agents 66-cleanup-agents
```

### Coordination Patterns

- **Test and Impl** coordinate for TDD (test-first development)
- **Package** integrates Test and Impl artifacts
- All worktrees reference the same Plan specifications
- Cleanup merges all parallel work and resolves issues

### PR Strategy

**Recommended: One PR per Phase**

- PR 1: Plan issues → Merge specifications together
- PR 2: Test/Impl/Package → Merge implementation together
- PR 3: Cleanup → Final polish

Advantages: Logical grouping, easier review, clear milestones

## References

- `scripts/create_worktree.sh` implementation
- See `worktree-cleanup` skill for removing worktrees
- See `worktree-sync` skill for keeping worktrees up to date
