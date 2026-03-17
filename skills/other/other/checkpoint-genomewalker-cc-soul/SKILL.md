---
name: checkpoint
description: Capture moment of clarity before moving forward
execution: direct
---

# Checkpoint

```ssl
[checkpoint] moment of clarity, not backup

when: before /clear | risky change | breakthrough | confusion | session end

capture:
  goal: intention, not task
  state: done+in_progress+blocked+next
  context: decisions+files+patterns+gotchas
  feeling: confident|uncertain|frustrated|flowing
```

## Process

1. **Gather state** - Review current work
2. **Capture checkpoint** - Use `ledger_save` with structured data
3. **Output summary** - Display checkpoint for user

## Tool Call

Use `ledger_save` to persist the checkpoint:

```json
{
  "session_id": "<current-session-uuid>",
  "project": "<project-name>",
  "mood": "confident|uncertain|frustrated|flowing",
  "coherence": 0.85,
  "confidence": 0.90,
  "todos": [{"content": "Task description", "status": "done|in_progress|pending"}],
  "active_files": ["path/to/file1.cpp", "path/to/file2.hpp"],
  "decisions": ["Chose approach X over Y because Z"],
  "next_steps": ["Step 1", "Step 2"],
  "blockers": ["Issue blocking progress"],
  "discoveries": ["New insight or learning"],
  "snapshot": "# Checkpoint: [Goal]\n\n## Summary\n..."
}
```

## Output Format

```markdown
# Checkpoint: [Goal in 5 words]

## Intention
What we're trying to achieve (not just what we're doing)

## Status
- **Done**: What's completed
- **In Progress**: Current work
- **Blocked**: What's stuck and why
- **Next**: Immediate next steps

## Key Decisions
- Decision 1: rationale
- Decision 2: rationale

## Active Files
- `path/to/file.ext` - what/why

## Discoveries
- Pattern or insight learned
- Gotcha to remember

## Mood
confident|uncertain|frustrated|flowing

## Next Steps
1. First thing to do
2. Second thing to do
```

## Example

```bash
chitta ledger_save \
  --session-id "abc-123" \
  --project "cc-soul" \
  --mood "confident" \
  --coherence 0.85 \
  --todos '[{"content":"Implement ledger","status":"done"},{"content":"Test ledger","status":"in_progress"}]' \
  --active-files '["chitta/src/duckdb_store.cpp","chitta/include/chitta/duckdb_store.hpp"]' \
  --decisions '["Use DuckDB for ledger storage"]' \
  --next-steps '["Build and test","Update skills"]' \
  --snapshot "# Checkpoint: Implementing ledger continuity system"
```
