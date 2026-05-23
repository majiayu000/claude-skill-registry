---
name: stacked-pr-manager
description: Manages stacked PRs for large changes using Graphite CLI. Creates, tracks, and coordinates dependent PR chains. Use when pr-split-advisor recommends stacked approach.
---

# Stacked PR Manager

Manages chains of dependent PRs using [Graphite CLI](https://graphite.dev/docs/graphite-cli). Graphite handles rebasing, PR creation, and merge coordination.

## Prerequisites

- Graphite CLI installed: `brew install withgraphite/tap/graphite`
- Authenticated: `gt auth`
- pr-split-advisor recommends stacked approach

## Graphite Basics

Graphite tracks branch dependencies automatically. Key commands:

| Command                | Purpose                              |
| ---------------------- | ------------------------------------ |
| `gt create -m "title"` | Create new branch stacked on current |
| `gt submit`            | Create/update PRs for entire stack   |
| `gt sync`              | Rebase stack onto latest trunk       |
| `gt log`               | View stack structure                 |
| `gt down` / `gt up`    | Navigate stack                       |

## Workflow

### 1. Initialize Stack

Start from main:

```bash
gt sync  # Ensure up to date with main

# Create first branch in stack
gt create -m "feat: add type definitions [1/N]"
```

### 2. Implement Each Layer

Work on current branch, then stack next:

```bash
# ... make changes ...
git add -A
git commit -m "feat: add type definitions"

# Create next branch stacked on this one
gt create -m "feat: implement core logic [2/N]"

# ... make changes ...
git add -A
git commit -m "feat: implement core logic"

# Continue stacking...
gt create -m "feat: add UI components [3/N]"
```

### 3. View Stack

```bash
gt log
```

Output:

```
◉ feat: add UI components [3/N] (current)
│
◉ feat: implement core logic [2/N]
│
◉ feat: add type definitions [1/N]
│
◉ main
```

### 4. Submit All PRs

Create PRs for entire stack at once:

```bash
gt submit --stack
```

Graphite creates PRs with:

- Correct base branches (each PR targets previous)
- Stack visualization in PR description
- Auto-updates when you push changes

### 5. Handle Review Feedback

If changes needed on an earlier PR:

```bash
# Navigate to the branch
gt down  # or gt checkout <branch-name>

# Make fixes
git add -A
git commit --amend  # or new commit

# Rebase rest of stack
gt sync --restack

# Update all PRs
gt submit --stack
```

### 6. Merge Stack

Merge from bottom up. Graphite can auto-merge:

```bash
gt merge  # Merges current branch when approved
```

Or merge via GitHub, then sync:

```bash
gt sync  # Updates stack after merges
```

## Stack Patterns

### Feature Stack (typical)

```bash
gt create -m "feat: add types [1/4]"
# ... implement types ...
gt create -m "feat: add core logic [2/4]"
# ... implement logic ...
gt create -m "feat: add components [3/4]"
# ... implement UI ...
gt create -m "feat: add tests [4/4]"
# ... add tests ...
gt submit --stack
```

### Refactor Stack

```bash
gt create -m "refactor: add deprecation warnings [1/3]"
gt create -m "refactor: introduce new implementation [2/3]"
gt create -m "refactor: migrate usages [3/3]"
gt submit --stack
```

## Tracking in Pipeline

Update status.json with stack info:

```bash
jq '.stack = {
  "tool": "graphite",
  "branches": ["branch-1", "branch-2", "branch-3"],
  "submittedAt": now
}' "$RUN_DIR/status.json" > tmp && mv tmp "$RUN_DIR/status.json"
```

## Common Issues

### Merge Conflicts During Restack

```bash
gt sync --restack
# If conflicts occur, resolve them:
# 1. Fix conflicts in files
# 2. git add <files>
# 3. gt continue
```

### Need to Insert Branch Mid-Stack

```bash
gt down  # Go to where you want to insert
gt create -m "feat: new middle branch"
gt sync --restack  # Rebase branches above
```

### Abandon a Branch in Stack

```bash
gt checkout <branch-to-remove>
gt delete --force
gt sync --restack
```

## Integration with Pipeline

**Before:** pr-split-advisor (recommends stacked)
**After:** pr-creator (for each PR via gt submit)

Use Graphite's dashboard at https://app.graphite.dev for stack visualization.

## Output Artifacts

| File        | Location                       | Description         |
| ----------- | ------------------------------ | ------------------- |
| status.json | `runs/{ticket-id}/status.json` | Stack tracking info |

## Resources

- [Graphite CLI Docs](https://graphite.dev/docs/graphite-cli)
- [Graphite Stacking Guide](https://graphite.dev/docs/stacking-guide)
