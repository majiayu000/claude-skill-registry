---
name: checkpoint-workflow
description: Enforces incremental saving during complex tasks to prevent progress
  loss. Use this skill whenever working on multi-step tasks, creating multiple files,
  or doing work that takes more than 5 minutes. T
---

---
name: checkpoint-workflow
description: Enforces incremental saving during complex tasks to prevent progress loss. Use this skill whenever working on multi-step tasks, creating multiple files, or doing work that takes more than 5 minutes. Triggers on: file creation, documentation updates, code changes, workflow execution, any task with multiple steps.
---

# Checkpoint Workflow Skill

## Core Principle

**CHECKPOINT EARLY, CHECKPOINT OFTEN**

Never accumulate more than 5 minutes of unsaved work. Every significant unit of work must be persisted before moving to the next.

## Checkpoint Triggers

Create a checkpoint when:

1. After creating ANY file → commit immediately
2. After completing a subtask → update PROGRESS.md + commit
3. Before starting a new phase → save current state
4. Every 3-5 tool calls → update progress journal
5. Before complex operations → pre-operation snapshot

## Required Actions

### After Every 2-3 Files Created
```bash
git add <files>
git commit -m "checkpoint: <brief description>"
git push origin main
```

### Before and After Major Steps
Update `docs/claude-integration/PROGRESS.md`:
```markdown
### Completed Steps:
- [x] Step description (commit: abc123)

### Current State:
- Working on: [specific item]
- Next action: [what comes next]
```

### Commit Message Prefixes
- `checkpoint:` - Work in progress
- `wip:` - May not build/work
- `progress:` - Incremental progress
- `save:` - Explicit save point

## Recovery Protocol

On context loss or "continue" request:

1. Read `docs/claude-integration/PROGRESS.md`
2. Check `git log --oneline -10`
3. Check `/mnt/transcripts/[latest].txt`
4. Resume from documented "Next Actions"
5. Update PROGRESS.md before continuing

## Anti-Patterns to Avoid

❌ Creating 10 files then committing all at once
❌ Completing entire task before documenting
❌ Starting context-heavy operations without saving first
❌ Ignoring PROGRESS.md updates

## Sample Workflow

```
1. START TASK
   └─> Update PROGRESS.md: "Starting task X"
   └─> git commit -m "checkpoint: starting task X"

2. SUBTASK A (2-3 files)
   └─> Create files
   └─> git commit -m "checkpoint: completed subtask A"
   └─> Update PROGRESS.md

3. SUBTASK B (2-3 files)
   └─> Create files
   └─> git commit -m "checkpoint: completed subtask B"
   └─> Update PROGRESS.md

4. COMPLETE
   └─> git commit -m "feat: complete task X"
   └─> Update PROGRESS.md: "COMPLETE"
```
