---
name: atuin-memory
description: Check, store, and retrieve project memories from atuin kv. Use when starting work on a project, recalling previous context, storing plans or specs, or when the user mentions memory, atuin, or project context.
allowed-tools:
  - Bash(atuin *)
  - Bash(git rev-parse *)
  - Bash(git branch *)
  - Bash(basename *)
  - Bash(pwd)
  - Bash(cat *)
  - Bash(echo *)
  - Bash(grep *)
  - Bash(head *)
  - Read
---

# Project Memory with Atuin

Store and retrieve project context using atuin kv to persist across sessions.

## Project Detection

Reuse these variables in all commands:

```bash
PROJECT=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || basename "$PWD")
BRANCH=$(git branch --show-current 2>/dev/null)
BRANCH=${BRANCH:-main}
```

## Before Starting Work

```bash
echo "=== $PROJECT ($BRANCH) ==="

# Discover what memories exist for this project
atuin kv list --namespace "project-metadata" | grep -F "$PROJECT-" || echo "(no memories found)"
```

Then retrieve relevant memories:

```bash
# Empty output means memory doesn't exist
atuin kv get --namespace "project-metadata" "$PROJECT-$BRANCH-plan"
atuin kv get --namespace "project-metadata" "$PROJECT-$BRANCH-spec"
atuin kv get --namespace "project-metadata" "$PROJECT-$BRANCH-todo"
```

## Acting on Retrieved Memories

<memory-actions>
  <on-retrieval>
    - Check if stored plan/spec/todo still matches git state and current goals
    - Briefly summarize what you found so user can correct misunderstandings
    - Raise blockers, gaps, or open questions before proceeding—don't assume, ask
    - Pick up from first incomplete todo item; if none exist, start fresh
  </on-retrieval>
  <on-completion>
    - Update stored state after completing work so next session can resume cleanly
  </on-completion>
</memory-actions>

## Storing Memories

For multi-line content, write to a temp file first to avoid shell escaping issues:

```bash
# 1. Write content to temp file
# 2. Store from temp file
atuin kv set --namespace "project-metadata" --key "$PROJECT-$BRANCH-plan" "$(cat /tmp/plan.md)"

# 3. Verify storage succeeded
atuin kv get --namespace "project-metadata" "$PROJECT-$BRANCH-plan" | head -5
```

For short single-line values, store directly:

```bash
atuin kv set --namespace "project-metadata" --key "$PROJECT-$BRANCH-status" "in-progress"
```

## Key Naming

| Key Pattern | Purpose |
|-------------|---------|
| `{project}-{branch}-plan` | Implementation plans |
| `{project}-{branch}-spec` | Specifications/designs |
| `{project}-{branch}-todo` | Task state |
| `{project}-{branch}-session-$(date +%Y-%m-%d)` | Session summaries (use current date) |

## Deleting Memories

```bash
# Delete a specific key
atuin kv delete --namespace "project-metadata" "$PROJECT-$BRANCH-plan"

# Verify deletion (should return empty)
atuin kv get --namespace "project-metadata" "$PROJECT-$BRANCH-plan"
```

## Quick Reference

**Argument syntax is inconsistent across subcommands — pay attention to positional vs flag arguments:**

| Operation | Command | Notes |
|-----------|---------|-------|
| List all | `atuin kv list --namespace "project-metadata"` | |
| Get | `atuin kv get --namespace "project-metadata" "key"` | KEY is **positional** |
| Set | `atuin kv set --namespace "project-metadata" --key "key" "value"` | KEY is **`--key` flag**, VALUE is **positional** |
| Delete | `atuin kv delete --namespace "project-metadata" "key"` | KEY is **positional** (not `--key`) |

<constraints>
  - Store artifacts in atuin, not local markdown files
  - Use /tmp for any temporary files needed during storage
  - Never commit metadata files to git
</constraints>
