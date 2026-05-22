---
name: create-worktree
description: "Create a git worktree for agent isolation. ALWAYS resolves the repo root first to prevent nesting. Use this skill whenever spawning an agent that needs its own working directory."
---

# Create Worktree — Flat, Non-Nesting Worktree Creation

Creates a git worktree at `<repo-root>/.claude/worktrees/<name>`. Prevents the
nesting bug where a subagent creates a worktree inside its parent agent's worktree.

---

## UNBREAKABLE RULE: Resolve Repo Root First

**Every worktree MUST be created under the main repo root, never relative to CWD.**

A subagent running inside a worktree has its CWD set to that worktree. If it
creates `.claude/worktrees/` relative to CWD, the result is a nested path like:

```
<repo-root>/.claude/worktrees/agent-A/.claude/worktrees/agent-B   # WRONG
```

The correct path is always:

```
<repo-root>/.claude/worktrees/agent-B   # CORRECT
```

---

## Step 1 — Resolve the Repo Root

Use `git worktree list --porcelain` to find the main worktree (always the first
entry). This works correctly whether you are in the main repo or inside a worktree.

```bash
REPO_ROOT=$(git worktree list --porcelain | head -1 | sed 's/^worktree //')
```

**Verify the result does not contain `.claude/worktrees/`:**

```bash
if echo "$REPO_ROOT" | grep -q '\.claude/worktrees/'; then
  echo "ERROR: Resolved repo root is itself a worktree. This should not happen."
  echo "Resolved: $REPO_ROOT"
  exit 1
fi
```

---

## Step 2 — Define the Worktree Path

```bash
WORKTREE_DIR="$REPO_ROOT/.claude/worktrees/<name>"
```

Where `<name>` is a unique identifier for the agent session, e.g.:
- `agent-<random-id>` for generic agents
- `issue-<NUMBER>-<agent>` for issue-specific work (e.g., `issue-42-firemandecko`)

---

## Step 3 — Create the Worktree

```bash
# Ensure the parent directory exists
mkdir -p "$REPO_ROOT/.claude/worktrees"

# Create the worktree on the target branch
git worktree add "$WORKTREE_DIR" "<BRANCH>"
```

If the branch already exists remotely but not locally:

```bash
git worktree add "$WORKTREE_DIR" -b "<BRANCH>" origin/main
```

---

## Step 4 — Validate (Nesting Check)

After creation, verify the worktree path is flat (not nested):

```bash
# Count how many times .claude/worktrees/ appears in the path
NESTING_COUNT=$(echo "$WORKTREE_DIR" | grep -o '\.claude/worktrees/' | wc -l)

if [ "$NESTING_COUNT" -gt 1 ]; then
  echo "ERROR: Worktree is nested! Path: $WORKTREE_DIR"
  git worktree remove "$WORKTREE_DIR" --force
  exit 1
fi

echo "Worktree created at: $WORKTREE_DIR"
```

---

## Step 5 — Cleanup (After Agent Completes)

When the agent finishes its work (or the chain completes), remove the worktree:

```bash
REPO_ROOT=$(git worktree list --porcelain | head -1 | sed 's/^worktree //')
git worktree remove "$REPO_ROOT/.claude/worktrees/<name>" --force
```

To clean up ALL stale worktrees (e.g., after a batch run or crash recovery):

```bash
REPO_ROOT=$(git worktree list --porcelain | head -1 | sed 's/^worktree //')
git worktree prune
# Remove any remaining directories
rm -rf "$REPO_ROOT/.claude/worktrees/"*
```

---

## Full Script Reference

```bash
#!/usr/bin/env bash
set -euo pipefail

AGENT_NAME="${1:?Usage: create-worktree.sh <agent-name> <branch>}"
BRANCH="${2:?Usage: create-worktree.sh <agent-name> <branch>}"

# Step 1: Resolve repo root (never use CWD)
REPO_ROOT=$(git worktree list --porcelain | head -1 | sed 's/^worktree //')

# Guard: repo root must not be a worktree itself
if echo "$REPO_ROOT" | grep -q '\.claude/worktrees/'; then
  echo "FATAL: Repo root resolved to a worktree path: $REPO_ROOT" >&2
  exit 1
fi

# Step 2: Define path
WORKTREE_DIR="$REPO_ROOT/.claude/worktrees/$AGENT_NAME"

# Step 3: Create
mkdir -p "$REPO_ROOT/.claude/worktrees"
git worktree add "$WORKTREE_DIR" "$BRANCH"

# Step 4: Validate — no nesting
NESTING_COUNT=$(echo "$WORKTREE_DIR" | grep -o '\.claude/worktrees/' | wc -l)
if [ "$NESTING_COUNT" -gt 1 ]; then
  echo "FATAL: Nested worktree detected: $WORKTREE_DIR" >&2
  git worktree remove "$WORKTREE_DIR" --force
  exit 1
fi

echo "Worktree ready: $WORKTREE_DIR"
```

---

## Notes

- `.claude/worktrees/` is in `.gitignore` — worktree contents are never committed.
- The CLAUDE.md self-containment rule prohibits external files from referencing
  worktree paths. Worktrees are ephemeral.
- When using the Agent tool with `isolation: worktree`, Claude Code handles
  worktree creation internally. This skill documents the correct behavior that
  all agents and orchestrators must follow when creating worktrees manually.
