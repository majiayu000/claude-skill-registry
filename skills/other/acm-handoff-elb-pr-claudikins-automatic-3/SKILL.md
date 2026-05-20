---
name: acm-handoff
description: Use when resuming work from a previous session that reached context threshold, or when a handoff summary exists. Reads handoff state and markdown to restore context, todos, and continue seamlessly.
---

# Context Handoff

This skill loads handoff content from a previous session that reached the context threshold.

## Instructions

When this skill is invoked:

1. **Check for structured state** at `.claude/claudikins-acm/handoff-state.json`
2. **Read the handoff markdown** at `.claude/claudikins-acm/handoff.md`
3. **Present both** to understand what was being worked on
4. **Restore todos** if active todos exist in the state
5. **Continue the work** from where it was left off

## File Locations

| File                                        | Purpose                      |
| ------------------------------------------- | ---------------------------- |
| `.claude/claudikins-acm/handoff-state.json` | Structured state (preferred) |
| `.claude/claudikins-acm/handoff.md`         | Human-readable summary       |

## Reading the State

The structured state JSON contains:

- `context.current_objective` - What was being worked on
- `context.active_todos` - Pending/in-progress todos to restore
- `context.key_files_modified` - Recently changed files
- `git.branch` - Git branch at handoff time
- `git.modified_files` - Uncommitted changes

## After Reading

1. **Restore todos** using TodoWrite if `active_todos` has entries
2. **Summarise** the previous session's state for the user
3. **Ask** if they want to continue from where they left off
4. **Clean up** the handoff files after successful restoration

## Cleanup

After successfully restoring context, offer to clean up:

```bash
rm -f .claude/claudikins-acm/handoff-state.json
rm -f .claude/claudikins-acm/handoff.md
```

## If No Handoff Exists

If neither file exists, inform the user:

- No handoff is currently active
- A handoff is created when context usage hits the threshold (default 60%)
- They can configure the threshold via /acm:config

---

_Claudikins Automatic Context Manager_
_To configure settings, use: /acm:config_
