---
name: deps
description: Visualize and analyze issue dependencies in Linear. Finds blocking chains, circular dependencies, and critical path items.
---

# Deps Skill - Dependency Analysis

You are an expert at analyzing and visualizing software project dependencies.

## When to Use

Use this skill when:
- Understanding what's blocking an issue
- Planning work order
- Identifying circular dependencies
- Finding critical path items

## Process

1. **Visualize Dependencies**
   ```bash
   linear deps ENG-100
   linear deps --team ENG
   ```

2. **Analyze Blocking Chains**
   - Find longest blocking chains
   - Identify bottleneck issues
   - Locate circular dependencies

3. **Recommend Actions**

## Dependency Types

| Type | Meaning | Example |
|------|---------|---------|
| blocks | A must complete before B | Auth blocks Login UI |
| blocked_by | B cannot start until A done | Login UI blocked by Auth |
| related | Informational link | Two related features |
| duplicate | Same issue | Close one, reference other |

## Visualization Output

```
DEPENDENCY GRAPH: ENG-100
════════════════════════════════════════
ENG-100 User Authentication Epic
├─ ENG-101 Login flow [In Progress]
│  ├─ ENG-103 OAuth integration [Todo]
│  │     → blocks: ENG-105
│  └─ ENG-104 Session management [Todo]
├─ ENG-102 Logout flow [Blocked]
│     ← blocked by: ENG-101
└─ ENG-105 Token refresh [Blocked]
      ← blocked by: ENG-103
────────────────────────────────────────
5 issues, 4 dependencies, 0 cycles
```

## Analysis Areas

### Blocking Chains
Issues that block many other issues are critical:
```
Critical blocker: ENG-101
  → blocks 3 issues directly
  → blocks 5 issues transitively
```

### Circular Dependencies
Cycles prevent any issue from completing:
```
⚠ Circular dependency detected:
  ENG-201 → ENG-202 → ENG-203 → ENG-201
```

### Critical Path
Longest dependency chain determines minimum completion time:
```
Critical path (4 issues):
  ENG-100 → ENG-101 → ENG-103 → ENG-105
Minimum time: 4 issue completion times
```

### Orphaned Dependencies
Issues referencing non-existent or closed issues:
```
⚠ Orphaned dependencies:
  ENG-150 blocked by ENG-099 (closed)
```

## Commands Used

```bash
# Single issue dependencies (issue ID doesn't require team context)
linear deps ENG-100

# Team-wide dependencies (requires team context from 'linear init')
linear deps --team ENG

# Check what blocks an issue
linear issues blocked-by ENG-100

# Check what an issue blocks
linear issues blocking ENG-100

# Create a dependency
linear issues update ENG-102 --blocked-by ENG-101

# Create multiple dependencies (comma-separated)
linear issues update ENG-102 --blocked-by ENG-101,ENG-103

# Remove a dependency (update with empty)
linear issues update ENG-102 --blocked-by ""
```

## Key Learnings

- **Issue identifiers (ENG-123) don't require team context** - work without `linear init`
- **Team-wide analysis requires team context** - use `linear init` or `--team` flag
- Dependencies are detected automatically and shown in ASCII graph format
- Circular dependencies are detected and highlighted with warnings

## Action Recommendations

Based on analysis, recommend:

1. **Unblock critical path** - Prioritize blockers
2. **Break cycles** - Remove unnecessary dependencies
3. **Parallelize** - Find work that can happen concurrently
4. **Update stale deps** - Clean up outdated relationships

## Best Practices

1. **Keep dependencies minimal** - Only add necessary ones
2. **Use blocks, not blocked_by** - Clearer mental model
3. **Review regularly** - Dependencies become stale
4. **Document non-obvious deps** - Add comments explaining why
