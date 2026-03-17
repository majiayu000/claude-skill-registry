---
name: end
description: Finalize session by creating detailed log and syncing to cloud
version: 1.2.0
---

# End Session

## Quick Finalization Workflow

1. **Collect session info**: Prompt user for session summary (topic, projects touched, key activities, decisions, blockers)

2. **Capture performance metrics**: Get actual values automatically:
   - Run: `python3 ~/.claude/get-context-metrics.py` to get: tokens|raw%|ctx(u)%|overhead
   - Parse output: `95641|47.8|59.8|12.0` means:
     - Context: 95,641 tokens
     - Tokens %: 47.8%
     - Context Window %: 59.8%
     - Overhead: 12.0 percentage points

3. **Generate daily log entry**: Create structured log in `~/.claude-memory/providers/claude/logs/daily/YYYY.MM.DD.md` with:
   - Session timestamp + topic
   - Projects touched
   - Activities realized
   - Performance metrics (see format below)
   - Next steps
   - Decisions/insights

4. **Update session state**: Modify `~/.claude-memory/providers/claude/session-state.md` with current focus and pending tasks

5. **Update integration timeline**: Append to `~/.claude-memory/integration/provider-activities.md` and `.quick.md`

6. **Sync to cloud**: Try pushing logs to cloud. On error, logs stay local only. (Cloud path in `~/.claude-memory/.config.json` - don't read, just try sync)

7. **Confirmation**: Show user what was logged and sync status

## Performance Metrics Format

```markdown
**Context Window**: [ctx(u)]% (real usage including Anthropic overhead)
**Tokens**: [used]/200,000 ([raw]%)
**Overhead**: [difference] percentage points
```

**Example**:
```markdown
**Context Window**: 59.8% (real usage)
**Tokens**: 95,641/200,000 (47.8%)
**Overhead**: 12.0 percentage points
```

**Why both matter**:
- **Context Window %** = What matters for hitting limits (includes system overhead)
- **Tokens %** = Conversation size (useful for comparing sessions)
- **Overhead** = Anthropic's cost (tools, prompts, cache, etc.)

## Key Principle

**Logs saved locally first, cloud sync is best-effort.** Session finalization never blocks on cloud errors.

---

See existing daily logs for format examples.
