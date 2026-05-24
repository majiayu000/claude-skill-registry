---
name: worktree-coordination
description: Manage multiple Claude Code instances across git worktrees. Check status, claim/release file locks, sync decisions, and prevent conflicts. Use when coordinating multiple worktrees or Claude instances.
context: none
version: 1.0.0
author: SkillForge
tags: [coordination, worktree, multi-instance, locking, parallel-development, 2026]
user-invocable: true
---

# Worktree Coordination Skill

## Commands

### /worktree-status
Show status of all active Claude Code instances.

**Usage:** `/worktree-status [--json] [--clean]`

**Actions:**
1. Run `cc-worktree-status` to see all active instances
2. Check for stale instances (no heartbeat > 5 min)
3. View file locks across all instances

**Output includes:**
- Instance ID and branch
- Current task (if set)
- Health status (ACTIVE/STALE)
- Files locked by each instance

### /worktree-claim <file-path>
Explicitly lock a file for this instance.

**Usage:** `/worktree-claim src/auth/login.ts`

**Actions:**
1. Check if file is already locked
2. If locked by another instance, show who holds it
3. If available, acquire lock

### /worktree-release <file-path>
Release lock on a file.

**Usage:** `/worktree-release src/auth/login.ts`

### /worktree-sync
Sync shared context and check for conflicts.

**Usage:** `/worktree-sync [--check-conflicts] [--pull-decisions]`

**Actions:**
1. `--check-conflicts`: Run merge-tree against other active branches
2. `--pull-decisions`: Show recent architectural decisions from other instances

### /worktree-decision <decision>
Log an architectural decision visible to all instances.

**Usage:** `/worktree-decision "Using Passport.js for OAuth" --rationale "Better middleware support"`

## Automatic Behaviors

### File Lock Check (PreToolUse Hook)
Before any Write or Edit operation:
1. Check if file is locked by another instance
2. If locked → BLOCK with details about lock holder
3. If unlocked → Acquire lock and proceed

### Heartbeat (Lifecycle Hook)
Every 30 seconds:
1. Update this instance's heartbeat timestamp
2. Clean up stale instances (no heartbeat > 5 min)
3. Release orphaned locks

### Cleanup (Stop Hook)
When Claude Code exits:
1. Release all file locks held by this instance
2. Unregister from coordination registry

## File Lock States

```
┌─────────────────────────────────────────────────────────┐
│  FILE: src/auth/oauth.ts                                │
├─────────────────────────────────────────────────────────┤
│  Status: LOCKED                                         │
│  Holder: cc-auth-a1b2c3                                 │
│  Branch: feature/user-authentication                    │
│  Task:   Implementing OAuth2 login flow                 │
│  Since:  2 minutes ago                                  │
├─────────────────────────────────────────────────────────┤
│  Action: Wait for release or use /worktree-release     │
└─────────────────────────────────────────────────────────┘
```

## Registry Schema

Located at `.claude/coordination/registry.json`:

```json
{
  "instances": {
    "cc-auth-a1b2c3": {
      "worktree": "/Users/dev/worktrees/feature-auth",
      "branch": "feature/user-authentication",
      "task": "Implementing OAuth2",
      "files_locked": ["src/auth/oauth.ts"],
      "started": "2026-01-08T14:30:00Z",
      "last_heartbeat": "2026-01-08T14:45:32Z"
    }
  },
  "file_locks": {
    "src/auth/oauth.ts": {
      "instance_id": "cc-auth-a1b2c3",
      "acquired_at": "2026-01-08T14:35:00Z",
      "reason": "edit"
    }
  },
  "decisions_log": [
    {
      "id": "dec-001",
      "instance_id": "cc-auth-a1b2c3",
      "decision": "Use Passport.js for OAuth",
      "rationale": "Better middleware support",
      "timestamp": "2026-01-08T14:40:00Z"
    }
  ]
}
```

## CLI Commands

Available in `bin/`:

```bash
# Create new coordinated worktree
cc-worktree-new <feature-name> [--base <branch>]

# Check status of all worktrees
cc-worktree-status [--json] [--clean]

# Sync context and check conflicts
cc-worktree-sync [--check-conflicts] [--pull-decisions]
```

## Best Practices

1. **One task per worktree** - Each Claude Code instance should focus on one feature/task
2. **Claim files early** - Use `/worktree-claim` before starting work on shared files
3. **Log decisions** - Use `/worktree-decision` for choices that affect other instances
4. **Check conflicts** - Run `cc-worktree-sync --check-conflicts` before committing
5. **Clean up** - Exit Claude Code properly to release locks (Ctrl+C or /exit)

## Troubleshooting

### "File is locked by another instance"
1. Check who holds it: `/worktree-status`
2. If instance is STALE: `cc-worktree-status --clean`
3. If legitimately held: Coordinate with other instance or work on different files

### "Instance not registered"
The heartbeat hook will auto-register on first tool use. If issues persist:
1. Check `.claude-local/instance-id.txt` exists
2. Verify `.claude/coordination/` is symlinked correctly

## Related Skills

- `git-workflow` - Git workflow patterns used within each coordinated worktree
- `commit` - Create commits with proper conventional format in each worktree
- `stacked-prs` - Manage dependent PRs that may span multiple worktrees
- `architecture-decision-record` - Document decisions shared via /worktree-decision

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Lock granularity | File-level | Balances conflict prevention with parallel work flexibility |
| Stale detection | 5 min heartbeat timeout | Long enough for normal pauses, short enough for quick cleanup |
| Registry location | .claude/coordination/ | Shared across worktrees via symlink, version-controlled |
| Lock acquisition | Automatic on Write/Edit | Prevents accidental conflicts without manual intervention |
| Decision sharing | Centralized log | All instances see architectural decisions in real-time |

## Capability Details

### status-check
**Keywords:** worktree, status, instances, active, who
**Solves:**
- How to see all active Claude Code instances
- Check which files are locked
- Find stale instances

### file-locking
**Keywords:** lock, claim, release, conflict, blocked
**Solves:**
- How to prevent file conflicts between instances
- Claim a file before editing
- Release a lock when done

### decision-sync
**Keywords:** decision, sync, share, coordinate
**Solves:**
- Share architectural decisions across instances
- See what other instances decided
- Coordinate approach between worktrees

### conflict-prevention
**Keywords:** conflict, merge, overlap, collision
**Solves:**
- Check for merge conflicts before committing
- Avoid overlapping work
- Coordinate parallel development
