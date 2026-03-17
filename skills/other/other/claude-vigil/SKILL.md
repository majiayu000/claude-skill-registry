---
name: claude-vigil
description: File checkpoint and recovery — auto-quicksaves before destructive commands, manual checkpoints for safe rollback
triggers: [PreToolUse]
---

# Vigil Plugin

File recovery. Saves checkpoints before dangerous operations, diffs changes, restores files safely.

## Hooks

| Hook | When | Action |
|------|------|--------|
| **PreToolUse(Bash)** | Destructive command detected | Auto-quicksaves affected files (rm, mv, git reset, etc.) |

Token cost: 0 on safe commands, ~30-50 on destructive. The regex matches: `rm`, `rmdir`, `mv`, `sed -i`, `perl -i`, `git checkout/reset/clean/restore`, output redirects.

## Commands

| Command | Description |
|---------|-------------|
| `/save-vigil <name> [files]` | Create a named file checkpoint |
| `/restore-vigil [name]` | Restore files from a checkpoint |

## Workflows

### Checkpoint (standalone)

1. `vigil_save(name: "before-refactor", files: ["src/auth.ts", "src/middleware.ts"])`
2. Make changes safely
3. If something breaks: `vigil_restore(name: "before-refactor")`

### Checkpoint (with siblings)

1. `vigil_save(name: "before-refactor", files: [...])`
2. If **praetorian** active: also `praetorian_compact(type: "decisions", ...)` to save the reasoning
3. Make changes — both files and context are now protected
4. If something breaks:
   - `vigil_restore(name: "before-refactor")` — restore files
   - `praetorian_restore("before-refactor")` — restore context

### Recovery (standalone)

1. `vigil_list()` — see available checkpoints
2. `vigil_diff(name: "checkpoint")` — preview what would change
3. `vigil_restore(name: "checkpoint")` — restore files
4. Optionally: `vigil_delete(name: "checkpoint")` — clean up

### Recovery (with siblings)

1. `vigil_list()` — see available checkpoints
2. `vigil_diff(name: "checkpoint")` — preview changes
3. If **historian** active: `find_file_context("filename")` to understand what changed and why
4. `vigil_restore(name: "checkpoint")` — restore files
5. If **praetorian** active: restore matching compaction for context

## Sibling Synergy

| Sibling | Value | How |
|---------|-------|-----|
| **Praetorian** | Context saved alongside files | Pair vigil checkpoints with praetorian compactions for full state recovery |
| **Historian** | File change context from history | `find_file_context()` explains what happened between checkpoint and now |

## MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `vigil_save` | Create named checkpoint (SHA-256 + gzip dedup) |
| `vigil_list` | List available checkpoints with metadata |
| `vigil_diff` | Preview changes since checkpoint |
| `vigil_restore` | Restore files from checkpoint |
| `vigil_delete` | Remove a checkpoint and free storage |

## Storage

Content-addressable at `.claude/vigil/`. 3 named slots + 1 rotating `~quicksave`.

## Requires

```
claude mcp add vigil -- npx claude-vigil-mcp
```
