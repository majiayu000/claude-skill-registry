---
name: swarm-coordination
description: Coordinate multi-agent swarm workflows. Use when working in parallel with other agents, managing shared resources, or orchestrating distributed tasks. Covers conflict prevention, handoffs, and state synchronization.
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Swarm Coordination

## Overview

This skill provides protocols and patterns for consistent, conflict-free multi-agent development. Follow these guidelines when working alongside other Claude Code agents in the same codebase.

## Core Principles

1. **Beads as Source of Truth**: All work items tracked via `bd` commands
2. **File Locking**: Hooks automatically manage file locks - respect them
3. **Session Isolation**: Each agent has a unique session ID for tracking
4. **Clean Handoffs**: Always leave state that another agent can continue

## Workflows

### Starting Work

- [ ] **Check Beads**: Run `bd ready` to find unblocked issues
- [ ] **Claim Work**: Update issue status: `bd update <id> --status in_progress`
- [ ] **Check Conflicts**: Review `.claude/hooks/.file-tracker.log` for recent edits
- [ ] **Coordinate**: If another agent is active, coordinate via Beads comments

### During Work

- [ ] **Atomic Changes**: Make small, complete changes that don't leave broken state
- [ ] **Frequent Commits**: Commit often to reduce merge conflicts
- [ ] **Update Progress**: Add comments to Beads issues for visibility
- [ ] **Respect Locks**: If a file is locked, wait or work on something else

### Completing Work

- [ ] **Run Tests**: Verify changes don't break existing functionality
- [ ] **Close Issue**: `bd close <id> --reason "Completed: <description>"`
- [ ] **Sync Beads**: `bd sync` to share updates with other agents
- [ ] **Clean State**: Commit all changes, leave no uncommitted work

## Conflict Prevention

### File Lock Protocol

Hooks automatically acquire/release locks. If you encounter a lock:

```bash
# Check who holds the lock
cat .claude/hooks/.locks/<filename>.lock

# Lock automatically expires after 60 seconds
# If urgent, coordinate via Beads or wait
```

### Merge Conflict Strategy

1. Pull frequently: Keep your branch up to date
2. Small PRs: Easier to merge than large changes
3. Coordinate: Use Beads to claim files/features before editing
4. Resolve quickly: Address conflicts immediately when detected

## Communication Patterns

### Handoff Message

When ending a session with incomplete work:

```bash
# Create handoff for next agent
echo '{"message": "Continue implementing auth middleware. Tests passing but needs error handling in src/auth.ts:45"}' > .claude/hooks/.state/handoff.json
```

### Issue Comments (via Beads)

```bash
# Add context for other agents
bd comment <issue-id> "Implemented base class. Needs: validation, tests, docs"
```

## Multi-Agent Patterns

### Queen-Worker Pattern

For complex tasks, one agent orchestrates while others execute:

1. **Queen**: Plans, decomposes, assigns via Beads
2. **Workers**: Claim issues, implement, report completion
3. **Sync Point**: All workers sync before final integration

### Parallel Streams

For independent features:

1. Create separate Beads issues for each stream
2. Each agent claims one stream
3. Avoid editing same files across streams
4. Merge streams at defined integration points

## State Files

| File | Purpose |
|------|---------|
| `.claude/hooks/.state/session_*.json` | Active agent sessions |
| `.claude/hooks/.state/handoff.json` | Handoff messages between sessions |
| `.claude/hooks/.locks/*.lock` | File edit locks |
| `.claude/hooks/.file-tracker.log` | Recent file modifications |

## Best Practices

1. **Check Before Edit**: Always verify no active locks on target files
2. **Complete Units**: Finish logical units of work before switching
3. **Document Intent**: Use Beads issues to declare what you're working on
4. **Test Locally**: Run tests before pushing to catch issues early
5. **Sync Often**: Keep Beads and git in sync with other agents

## Emergency Procedures

### Deadlock Detection

If agents are waiting on each other:

```bash
# Check active sessions
ls -la .claude/hooks/.state/session_*.json

# Check active locks
ls -la .claude/hooks/.locks/

# Force release stale locks (use with caution)
find .claude/hooks/.locks -mmin +5 -delete
```

### Recovery from Conflict

1. Save current work to a new branch
2. Sync with main: `git fetch && git rebase origin/main`
3. Resolve conflicts file by file
4. Update Beads: `bd sync`
5. Continue work

## Integration with Beads

```bash
# View all open work
bd list --status open

# Get ready (unblocked) items
bd ready --sort hybrid

# Claim an issue
bd update <id> --status in_progress --assignee claude

# Add dependency
bd dep add <blocking-id> <blocked-id> --type blocks

# Complete work
bd close <id> --reason "Implemented feature X"

# Sync state
bd sync
```
