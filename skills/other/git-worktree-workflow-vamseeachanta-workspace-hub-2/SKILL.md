---
name: git-worktree-workflow
description: Use git worktrees for parallel Claude Code workflows. Run multiple Claude instances on different features simultaneously without merge conflicts. Use for parallel development, multi-branch testing, and subagent workflows.
version: 1.1.0
last_updated: 2026-01-02
category: development
related_skills:
  - repo-sync
  - sparc-workflow
  - agent-orchestration
  - swarm-worker
---

# Git Worktree Workflow Skill

> Version: 1.1.0
> Created: 2025-12-30
> Last Updated: 2026-01-02
> Category: Development

## Overview

Git worktrees allow you to have multiple working directories from a single repository, enabling parallel development workflows with Claude Code. This is essential for running multiple Claude instances on different tasks simultaneously.

## Quick Start

```bash
# 1. Create worktree for new feature branch
git worktree add -b feature-api ../project-api main

# 2. Run Claude in worktree
cd ../project-api && claude "Implement the feature"

# 3. After completion, merge and cleanup
cd ../project
git merge feature-api
git worktree remove ../project-api
git branch -d feature-api
```

## When to Use

- Running multiple Claude agents on different features
- Testing changes while continuing development
- Code review with live comparison
- Parallel bug fixes across branches
- Subagent verification workflows
- A/B implementation comparisons
- CI/CD parallel job execution

## Concepts

### What is a Worktree?

```
Main repo: /project (on main branch)
Worktree 1: /project-feature-a (on feature-a branch)
Worktree 2: /project-feature-b (on feature-b branch)
Worktree 3: /project-hotfix (on hotfix branch)
```

All share the same `.git` directory but have independent working directories.

## Basic Commands

### Create a Worktree

```bash
# Create worktree for existing branch
git worktree add ../project-feature feature-branch

# Create worktree with new branch
git worktree add -b new-feature ../project-new-feature main

# Create worktree for detached HEAD (testing)
git worktree add --detach ../project-test HEAD
```

### List Worktrees

```bash
git worktree list
# Output:
# /project           abc1234 [main]
# /project-feature   def5678 [feature-a]
# /project-hotfix    ghi9012 [hotfix-123]
```

### Remove Worktree

```bash
# Remove after merging
git worktree remove ../project-feature

# Force remove (discards changes)
git worktree remove --force ../project-abandoned

# Prune stale worktrees
git worktree prune
```

## Parallel Claude Workflows

### Pattern 1: Feature + Review

Run development and review in parallel:

```bash
# Terminal 1: Development Claude
cd /project-feature
claude "Implement the new authentication module"

# Terminal 2: Review Claude
cd /project
claude "Review the authentication changes in feature-auth branch"
```

### Pattern 2: Multi-Feature Development

Work on multiple features simultaneously:

```bash
# Setup worktrees
git worktree add -b feature-api ../project-api main
git worktree add -b feature-ui ../project-ui main
git worktree add -b feature-tests ../project-tests main

# Run Claude in each (separate terminals)
cd ../project-api && claude "Build REST API endpoints"
cd ../project-ui && claude "Create React components"
cd ../project-tests && claude "Write integration tests"
```

### Pattern 3: Subagent Verification

Main Claude spawns verification in separate worktree:

```bash
# Main Claude working in /project
# Creates verification worktree:
git worktree add --detach ../project-verify HEAD

# Spawns subagent to verify:
cd ../project-verify && claude -p "Verify the implementation works correctly"
```

### Pattern 4: A/B Implementation

Compare two approaches:

```bash
# Create two worktrees from same point
git worktree add -b approach-a ../project-a main
git worktree add -b approach-b ../project-b main

# Different Claude instances try different solutions
cd ../project-a && claude "Implement caching using Redis"
cd ../project-b && claude "Implement caching using Memcached"

# Compare results
diff -r ../project-a/src ../project-b/src
```

## Best Practices

### Do

1. Use descriptive naming convention: `<project>-<purpose>`
2. Create worktrees in sibling directories (not inside project)
3. Commit or stash changes before removing worktrees
4. Prune stale worktrees regularly
5. Document active worktrees in team communication
6. Clean up merged worktrees promptly

### Don't

1. Create worktrees inside the main project directory
2. Leave uncommitted changes in worktrees before removal
3. Forget to merge/push changes from worktrees
4. Create excessive worktrees (manage actively)
5. Use worktrees for long-lived branches (use separate clones)
6. Skip the cleanup step after merging

### Naming Convention

```bash
# Pattern: <project>-<purpose>
../project-feature-auth      # Feature work
../project-hotfix-123        # Bug fix
../project-review            # Code review
../project-test              # Testing
../project-experiment        # Experiments
```

### Workspace Organization

```
/workspace/
├── project/                 # Main development
├── project-feature-a/       # Active features
├── project-feature-b/
├── project-review/          # Review worktree
└── project-archive/         # Completed features (before cleanup)
```

### Cleanup Script

```bash
#!/bin/bash
# cleanup-worktrees.sh

# Remove merged branches
git branch --merged main | grep -v main | while read branch; do
    worktree=$(git worktree list | grep "$branch" | awk '{print $1}')
    if [ -n "$worktree" ]; then
        echo "Removing worktree: $worktree"
        git worktree remove "$worktree"
    fi
done

# Prune stale references
git worktree prune
```

## Integration with Claude Code

### CLAUDE.md Configuration

Add to project CLAUDE.md:

```markdown
## Worktree Workflow

When running parallel tasks:
1. Create worktree: `git worktree add -b <branch> ../<project>-<purpose> main`
2. Work in isolated directory
3. Commit changes normally
4. Return to main and merge
5. Remove worktree: `git worktree remove ../<worktree>`
```

### Headless Mode in Worktrees

```bash
# Automate worktree operations
WORKTREE="../project-auto-$(date +%s)"
git worktree add -b auto-task "$WORKTREE" main

cd "$WORKTREE"
claude -p "Complete the task in task.md" --output result.md

# Collect results
cp result.md ../results/
git worktree remove "$WORKTREE"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Branch already checked out | Branch exists in another worktree | Remove existing worktree or use different branch |
| Cannot remove worktree | Uncommitted changes present | Commit, stash, or force remove |
| Permission errors | Directory not writable | `chmod -R u+w <worktree>` then remove |
| Stale worktree references | Worktree directory deleted manually | Run `git worktree prune` |
| Lock file exists | Previous operation interrupted | Remove `.git/worktrees/<name>/locked` file |
| Path already exists | Directory exists at target path | Choose different path or remove existing directory |

## Advanced: CI/CD Integration

### GitHub Actions Parallel Jobs

```yaml
jobs:
  parallel-claude:
    strategy:
      matrix:
        task: [lint, test, security]
    steps:
      - uses: actions/checkout@v4

      - name: Create worktree
        run: |
          git worktree add -b ${{ matrix.task }} ../work-${{ matrix.task }}

      - name: Run Claude task
        run: |
          cd ../work-${{ matrix.task }}
          claude -p "Run ${{ matrix.task }} analysis"
```

## Execution Checklist

| Step | Command | Verification |
|------|---------|--------------|
| Create worktree | `git worktree add -b <branch> <path> main` | `git worktree list` shows new entry |
| Navigate to worktree | `cd <path>` | `pwd` shows worktree path |
| Run Claude task | `claude "<task>"` | Task completes successfully |
| Commit changes | `git add . && git commit -m "message"` | `git log` shows commit |
| Return to main | `cd <main-project>` | `pwd` shows main path |
| Merge changes | `git merge <branch>` | `git log` shows merge |
| Remove worktree | `git worktree remove <path>` | `git worktree list` excludes entry |
| Delete branch | `git branch -d <branch>` | `git branch` excludes branch |
| Prune stale | `git worktree prune` | No stale references remain |

## Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Worktree Creation Time | <5s | Time to create new worktree |
| Parallel Efficiency | >80% | CPU utilization across worktrees |
| Cleanup Rate | 100% | Worktrees removed after merge |
| Branch Isolation | 100% | No cross-worktree conflicts |
| Merge Success Rate | >95% | Clean merges without conflicts |

## Related Skills

- [repo-sync](../repo-sync/SKILL.md) - Manage multiple repositories
- [sparc-workflow](../sparc-workflow/SKILL.md) - Systematic development process
- [agent-orchestration](../agent-orchestration/SKILL.md) - Multi-agent coordination

---

## Version History

- **1.1.0** (2026-01-02): Added Quick Start, Error Handling table, Metrics, Execution Checklist, Best Practices Do/Don't, updated frontmatter with version/category/related_skills
- **1.0.0** (2025-12-30): Initial release based on Claude Code best practices
