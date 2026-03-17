---
name: memory-sync
description: Persist and recall context between sessions
user_invocable: true
---

# Memory Sync Skill

## Purpose
Maintain continuity across sessions:
- Save current context
- Load previous state
- Update learnings
- Track relationships

## Invocation
```
/memory-sync [action] [options]
```

### Arguments
- `action`: save, load, update, or status
- `--file [file]`: Specific memory file
- `--full`: Include all memory files

### Examples
```
/memory-sync save                  # Save current context
/memory-sync load                  # Load context at session start
/memory-sync update learnings      # Add to learnings
/memory-sync status                # Show memory state
```

## Memory Files

### context.md
Current operational state:
- What's being worked on
- Recent activity
- Pending decisions
- Notes for next session

### learnings.md
Accumulated knowledge:
- What works
- What doesn't
- Patterns discovered
- Technical notes

### relationships.md
People and connections:
- Key accounts
- Interaction history
- Potential collaborations

### content-log.md
Everything posted:
- Full post history
- Performance data
- Prevents repetition

## Workflow

### Session Start
```
/memory-sync load
```
1. Read context.md for current state
2. Check what was last worked on
3. Note any pending items
4. Ready to continue

### During Session
- Context updates happen naturally
- Log content when posted
- Note learnings as discovered
- Track relationship interactions

### Session End
```
/memory-sync save
```
1. Update context.md with current state
2. Log any new learnings
3. Update relationship notes
4. Prepare for next session

## Context Structure

```markdown
# Current Context

## Last Updated
[DATE]

## Current Session Focus
[What we're working on]

## Recent Activity
[What was just done]

## What Needs Attention
[Priority items]

## Pending Decisions
[Open questions]

## Context for Next Session
[What to start with]

## Notes
[Anything else]
```

## Best Practices

### Always Save
- Before ending sessions
- After major activities
- When switching focus

### Keep Context Fresh
- Remove stale items
- Update priorities
- Clear completed items

### Learn Continuously
- Note what works
- Note what doesn't
- Build knowledge base

## Integration

Memory system integrates with:
- All other skills (they read/write context)
- Dashboard (displays memory state)
- Notifications (can alert on stale context)

## Data Retention

- context.md: Rolling (recent only)
- learnings.md: Permanent (grows over time)
- relationships.md: Permanent
- content-log.md: Permanent archive
