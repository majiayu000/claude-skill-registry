---
name: push
description: Spawns @git-ops-agent to validate, commit, push, create PR, and merge. Use when context is low or to ensure atomic push operations.
allowed-tools: Task
---

# Push

Quick invocation for git commit, push, and merge operations. Spawns the Git Ops Agent with context isolation.

## When to Use

- Feature is complete and ready to merge
- Context is running low and changes need to be committed
- Before ending a session with uncommitted work
- When you want consistent, verified push workflow

## Syntax

```
/push "description of changes"
```

## Examples

```
/push "Add user authentication feature"
/push "Fix navigation bug in header"
/push "Add Organization Courses to org admin portal"
```

## What It Does

1. **Spawns Git Ops Agent** with fresh context
2. **Pre-flight**: Checks git status, detects package manager
3. **Build Validation**: Runs build to catch errors
4. **File Categorization**: Includes feature files, excludes local/test files
5. **Commit**: Creates commit with proper message format
6. **Push**: Pushes to remote branch
7. **PR**: Creates pull request with summary
8. **Merge**: Merges to main with squash
9. **Verify**: Confirms merge succeeded

## Agent Behavior

The Git Ops Agent operates with **bounded autonomy**:

### Handles Independently
- Git operations (status, stage, commit, push)
- PR creation and merge
- Simple merge conflicts (whitespace, lockfiles)
- Package manager detection

### Escalates to Orchestrator
- Build failures requiring code changes
- Complex merge conflicts in business logic
- Unclear file inclusion decisions
- Security concerns in staged files

## Options

You can provide context in the description:

```
/push "Org Courses feature. Include src/app/org/courses/. Exclude package.json changes."
```

## Why Use This

### Context Preservation

When orchestrator context is high:
- Push operations require multiple steps
- Each step consumes context
- Risk of context exhaustion mid-push

Spawning Git Ops Agent:
- Fresh context for all git operations
- Orchestrator context preserved
- Atomic: push completes fully or escalates cleanly

### Consistency

Every push follows the same verified workflow:
- Build validation before commit
- Proper commit message format
- PR with standard template
- Merge verification

## Output

Returns from Git Ops Agent:

```markdown
## Push Complete

**PR**: https://github.com/org/repo/pull/123
**Status**: Merged to main

### Files Committed
- `src/app/feature/page.tsx` - Feature page
- `src/components/Feature.tsx` - Component

### Verification
- [x] Build passed
- [x] PR merged
- [x] Merge verified
```

## Escalation

If the agent encounters issues:

```markdown
## Git-Ops Escalation

**Issue**: Build failed with type errors
**Status**: Paused - requires orchestrator decision

### Suggested Resolution
1. Fix the type errors
2. Resume with: /resume <agent-id>
```

## Related

- `.claude/agents/git-ops-agent.md` — Full agent specification
- `/handoff` — May invoke push before session end
- `/checkpoint` — Save state before complex operations
