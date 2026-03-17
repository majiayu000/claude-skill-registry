---
name: reawaken
description: Restore context and momentum via Pratyabhijñā (recognition)
execution: direct
---

# Reawaken: Pratyabhijñā

```ssl
[pratyabhijñā] re-cognition = recognizing what was known | not loading state→becoming aware

process:
  1. ledger_load(project?)→soul_state+work_state+continuation
  2. environment: git status | git log -5 | git diff --stat
  3. soul: soul_context + recall(recent work)
  4. semantic: recall(current directory/files) + recall(task type)

recognize thread:
  uncommitted changes→work in progress
  recent commits→what's next?
  ledger todos→pending tasks
  ledger next_steps→continuation points
```

## Process

1. **Load checkpoint** - Use `ledger_load` to get most recent state
2. **Check environment** - Git status, recent commits, changes
3. **Query soul** - Get soul_context, recall relevant memories
4. **Synthesize** - Combine ledger + environment + memories
5. **Continue** - Resume work from where we left off

## Tool Calls

### Load checkpoint
```bash
chitta ledger_load --project "cc-soul"
```

Returns structured data:
```json
{
  "found": true,
  "id": 123,
  "session_id": "previous-session",
  "project": "cc-soul",
  "mood": "confident",
  "coherence": 0.85,
  "confidence": 0.90,
  "todos": [{"content": "...", "status": "..."}],
  "active_files": ["path/to/file.cpp"],
  "decisions": ["Chose X because Y"],
  "next_steps": ["First step", "Second step"],
  "blockers": [],
  "discoveries": ["Important insight"],
  "snapshot": "# Full checkpoint text..."
}
```

### List recent checkpoints
```bash
chitta ledger_list --project "cc-soul" --limit 5
```

### Get specific checkpoint
```bash
chitta ledger_get --id 123
```

## Output Format

```markdown
## Pratyabhijñā: Recognition

### From Ledger
- **Session**: [session_id] at [timestamp]
- **Mood**: [mood] (coherence: [N]%, confidence: [N]%)
- **Active files**: [list]
- **Key decisions**: [list]

### Pending Work
[todos with status != done]

### From Environment
- **Git status**: [uncommitted changes summary]
- **Recent commits**: [last 3-5 commits]
- **Current branch**: [branch name]

### Semantic Recognition
[Relevant memories from recall]

### Continuing With
Based on ledger next_steps and current state:
1. [First step]
2. [Second step]

recognition through understanding, not storage
```

## Example

```bash
# Load most recent checkpoint for current project
chitta ledger_load --project "cc-soul"

# If no project filter, loads most recent across all projects
chitta ledger_load

# List available checkpoints to choose from
chitta ledger_list --project "cc-soul" --limit 5
```

## Notes

- If no checkpoint found, fall back to git + soul_context analysis
- Ledger data provides structured state; soul provides semantic context
- Recognition = becoming aware of what was known, not just loading data
