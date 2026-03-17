---
name: conversation-fork
description: Fork the current conversation to safely explore an alternative approach without losing current progress
disable-model-invocation: true
---

# Conversation Fork

Create a safe divergence point to explore an alternative approach without losing current progress.

## When to Run

- "I'm not sure whether to do X or Y — let me try both"
- Before a risky refactor that might not pan out
- When the user wants to explore an alternative design
- After a plan is agreed but before major implementation begins

## Arguments

- First argument: fork name (short, kebab-case, e.g. `auth-approach-b`)
- `--worktree`: use heavy fork (new git worktree + branch) instead of light fork (git stash)

## Strategy Selection

| Strategy | When | Cost |
|----------|------|------|
| Light fork (default) | Experimenting, < 1 day of work, same branch OK | Low |
| Heavy fork (`--worktree`) | Long-lived parallel track, needs own CI, separate PR | High |

## Light Fork (Default)

Creates a stash snapshot and documents both approaches in a FORK file.

### Steps

1. Capture state:
```bash
FORK_NAME="<name>"
BRANCH=$(git branch --show-current)
SHA=$(git rev-parse --short HEAD)
DATE=$(date +%Y-%m-%d)
```

2. Stash current work (preserves staged + unstaged + untracked):
```bash
git stash push -m "fork/$FORK_NAME" --include-untracked
```

3. Write fork document at `docs/plans/FORK-${FORK_NAME}.md`:

```markdown
# Fork: <NAME>

**Created:** <DATE>
**Branch:** <BRANCH>
**Commit:** <SHA>

## Context

<One paragraph: why we forked here, what decision point this represents>

## Approach A (Stashed / Original Path)

**Status:** Stashed as `fork/<NAME>`
**What it does:** <Description of the current approach>
**Resume:** `git stash apply stash^{/fork/<NAME>}`

## Approach B (Current / Exploration)

**Status:** Working from <SHA>
**What it will do:** <Description of the alternative>
**Resume:** Continue working (this is the active branch)

## Recent Context

<output of: git log --oneline -5>

## Decision Criteria

- Choose A if: <condition>
- Choose B if: <condition>
- Merge both if: <condition>

## Resume Instructions

To return to Approach A:
\`\`\`bash
git stash apply stash^{/fork/<NAME>}
\`\`\`

To abandon Approach B and restore A:
\`\`\`bash
git checkout -- .
git stash pop
\`\`\`
```

## Heavy Fork (`--worktree`)

Creates a full git worktree at a new branch for true parallel development.

### Steps

1. Capture state (same as light fork).

2. Create worktree at current HEAD:
```bash
WORKTREE_PATH="$HOME/worktrees/property-tracker/fork-${FORK_NAME}"
git worktree add "$WORKTREE_PATH" -b "fork/$FORK_NAME"
```

3. Copy env:
```bash
cp .env.local "$WORKTREE_PATH/.env.local" 2>/dev/null || true
```

4. Write fork document to **both** worktrees (`docs/plans/FORK-${FORK_NAME}.md`):

```markdown
# Fork: <NAME>

**Created:** <DATE>
**Origin Branch:** <BRANCH>
**Origin Commit:** <SHA>

## Approach A (Origin)

**Path:** <original worktree path>
**Branch:** <BRANCH>
**Resume:** Work here, this worktree is untouched

## Approach B (Exploration)

**Path:** <WORKTREE_PATH>
**Branch:** `fork/<NAME>`
**Resume:** `cd <WORKTREE_PATH>`

## Recent Context

<output of: git log --oneline -5>

## Cleanup

When done exploring, remove the worktree:
\`\`\`bash
git worktree remove <WORKTREE_PATH>
git branch -d fork/<NAME>
\`\`\`
Or keep it and open a separate PR from `fork/<NAME>`.
```

## After Forking

1. **Light fork:** You're on a clean working tree at the same SHA. Implement Approach B. Return to A with `git stash apply`.
2. **Heavy fork:** Switch to the new worktree path. Both tracks run independently.

In either case, `docs/plans/FORK-<name>.md` records the decision context for future reference.

## Examples

```
/conversation-fork auth-approach-b
/conversation-fork db-indexing-strategy --worktree
/conversation-fork no-orm-experiment --worktree
```
