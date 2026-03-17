---
name: handoff
description: Prepare for context handoff when running low on context. Syncs docs and commits so a fresh agent can continue.
---

# Handoff Skill

Prepare for context handoff when running low on context. Updates documentation so a fresh agent can seamlessly continue the work.

## Usage

```
/handoff
```

Run this when:
- Context is getting long/full
- You're about to start a new session
- Switching to a different task and want to preserve state

## Workflow

### Step 1: Sync Documentation

First, run `/sync-docs` to ensure all documentation is current:
- Updates SITREP.md with current state
- Updates TODO.md with progress
- Updates HIVE-TEST-ANALYSIS.md if tests are running

### Step 2: Add Session Context

After sync-docs, enhance the docs with session-specific context:

**SITREP.md** - Add to "Current Activity":
- What was accomplished this session
- Any problems encountered
- Key decisions made and why

**TODO.md** - Ensure it has:
- Clear "Next Steps" for the incoming agent
- Any context the next agent needs that isn't obvious
- Specific, actionable first task

### Step 3: Update PROMPTLOG.md

Use the Task tool to run promptlog in a subagent:

```
Task tool with subagent_type="general-purpose", prompt="Run /promptlog to update PROMPTLOG.md"
```

Wait for completion before proceeding.

### Step 4: Commit All Changes

Stage and commit all documentation:

```bash
git add SITREP.md TODO.md HIVE-TEST-ANALYSIS.md PROMPTLOG.md
git commit -m "Update docs for session handoff

[Brief summary of session accomplishments]"
```

### Step 5: Report Handoff Summary

Output a summary for the user:

```
Handoff prepared:
- SITREP.md: [what was updated]
- TODO.md: [N] items, first task: [description]
- PROMPTLOG.md: Updated with [N] prompts
- Committed: [hash]

Next agent should run: /pickup
```

## For the Next Agent

The recommended way to continue work is:

```
/pickup
```

Or manually:

```
check @TODO.md and @SITREP.md and continue
```

## Related Skills

- `/sync-docs` - Update docs without full handoff
- `/pickup` - Resume work from previous session
- `/promptlog` - Update prompt history
- `/hive-progress` - Check test progress specifically
