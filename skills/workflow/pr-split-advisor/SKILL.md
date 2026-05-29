---
name: pr-split-advisor
description: 'Analyzes implementation plans and recommends PR splitting strategy. Use after a plan.md is approved to determine single PR, vertical slices, or stacked PRs approach.'
---

# PR Split Advisor

Analyzes an approved implementation plan and recommends whether to keep work as a single PR or split into multiple PRs using vertical slices or stacked PRs.

## When to Use

- After `plan-generator` produces an approved `plan.md`
- When starting implementation of a multi-file change
- When asked "should I split this into multiple PRs?"
- Before creating branches/worktrees for implementation

## Workflow

### 1. Load and Parse the Plan

Read `plan.md` from the run directory and extract:

- Files to modify (with estimated LoC changes)
- Files to create (with estimated LoC)
- Layers touched (components, stores, utils, types, tests)
- Dependencies between changes

```bash
# Find the plan
cat runs/{ticket-id}/plan.md
```

### 2. Analyze Scope

Calculate metrics:

| Metric              | How to Assess                                        |
| ------------------- | ---------------------------------------------------- |
| Total estimated LoC | Sum of all file estimates                            |
| File count          | Number of files affected                             |
| Layer count         | Distinct layers (component, store, util, type, test) |
| Coupling            | Can changes be tested independently?                 |

### 3. Apply Decision Rules

```
IF estimated LoC < 200:
  → Single PR (unless changes are completely unrelated)

IF estimated LoC 200-400 AND changes are tightly coupled:
  → Single PR (review burden is acceptable)

IF estimated LoC > 300 AND changes span multiple layers:
  → Consider splitting

IF changes have no dependencies on each other:
  → Vertical Slices (independent PRs, any merge order)

IF changes have logical dependencies (e.g., types → utils → components):
  → Stacked PRs (ordered merge using Graphite)
```

### 4. Generate Recommendation

Produce analysis in this format:

```markdown
# PR Split Analysis

## Scope Summary

- **Estimated LoC:** {number}
- **Files affected:** {count}
- **Layers touched:** {list}

## Recommendation: {Single PR / Vertical Slices / Stacked PRs}

### Rationale

{Why this approach fits the change}

## Proposed Split

### PR 1: {Title}

- **Scope:** {description}
- **Files:**
  - `path/to/file1.ts`
  - `path/to/file2.ts`
- **Dependencies:** None
- **Estimated LoC:** {number}

### PR 2: {Title}

- **Scope:** {description}
- **Files:**
  - `path/to/file3.ts`
- **Dependencies:** PR 1 (if stacked) / None (if vertical)
- **Estimated LoC:** {number}

## Setup Commands

{commands based on strategy}
```

### 5. Present Decision

Ask the user to confirm or override:

```
Based on analysis, I recommend: {strategy}

Options:
A) Accept recommendation and set up {strategy}
B) Use vertical slices instead
C) Use stacked PRs instead
D) Keep as single PR

Your choice:
```

### 6. Execute Setup

Based on chosen strategy:

#### Single PR

```bash
# No special setup needed
# Continue on current feature branch
git checkout -b feat/{ticket-id}-{feature-name}
```

#### Vertical Slices (Independent PRs)

```bash
# Create separate worktrees for each PR
wt-new {repo} pr1-{feature}
wt-new {repo} pr2-{feature}

# Or for cross-repo:
wt-multi-new {branch-prefix} {repo1} {repo2}
```

#### Stacked PRs (Dependent Chain)

```bash
# Check Graphite is installed
which gt || npm install -g @withgraphite/graphite-cli

# Initialize Graphite if needed
gt init

# Create first PR in stack
gt create -m "feat: {PR 1 title}"

# After PR 1 work, create next
gt create -m "feat: {PR 2 title}"

# Submit entire stack
gt submit
```

### 7. Update Plan

Add strategy section to `plan.md`:

```markdown
## PR Strategy

**Approach:** {Single PR / Vertical Slices / Stacked PRs}

### PRs

1. **{PR 1 title}** - {files list}
2. **{PR 2 title}** - {files list}

### Setup

{Commands used}
```

Update `status.json`:

```json
{
  "stage": "pr-strategy",
  "strategy": "vertical-slices",
  "prs": [
    { "id": 1, "title": "...", "branch": "pr1-..." },
    { "id": 2, "title": "...", "branch": "pr2-..." }
  ]
}
```

### 8. Output Next Steps

```markdown
## Setup Complete

**Strategy:** {chosen strategy}

### Next Steps

{For single PR:}

1. Continue to task generation
2. Implement tasks on branch: `{branch-name}`

{For vertical slices:}

1. Generate tasks for PR 1 first
2. Complete PR 1, then generate tasks for PR 2
3. PRs can be reviewed/merged independently

Worktrees created:

- `{path/to/pr1}` → PR 1
- `{path/to/pr2}` → PR 2

{For stacked PRs:}

1. Generate all tasks
2. Implement PR 1 changes first
3. Run `gt create` to checkpoint
4. Implement PR 2, then `gt create` again
5. Submit stack with `gt submit`
```

## Split Strategies

### Vertical Slices

Best for completely independent changes:

- Separate features
- Unrelated bug fixes
- Independent refactors

**Tools:** `wt-new`, `wt-multi-new` (git-worktree-utils)

### Stacked PRs

Best for dependent changes:

- Schema → API → UI flow
- Types → Utils → Components
- Base refactor → Feature implementation

**Tools:** Graphite CLI (`gt create`, `gt submit`, `gt sync`)

### When to Keep Single

- Under 200 LoC
- Highly coupled changes that break if split
- Simple, focused fixes
- Changes where context is lost if split

## Graphite Fallback

If Graphite isn't installed:

```
Graphite CLI not found. Options:

A) Install Graphite: `npm install -g @withgraphite/graphite-cli`
B) Use manual stacking:
   - Create branches: `git checkout -b pr-1 main`
   - Stack: `git checkout -b pr-2 pr-1`
   - Rebase when pr-1 changes: `git rebase pr-1 pr-2`
C) Switch to vertical slices (restructure to remove dependencies)
```

## Best Practices

- Default to single PR for small changes
- Prefer vertical slices over stacked when possible (easier to manage)
- Even 300 LoC may be fine if changes are simple/repetitive
- Consider reviewer context—don't split so much that reviews lose coherence
- Label stacked PRs: "[1/3] Schema changes", "[2/3] API layer"
