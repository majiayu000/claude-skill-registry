---
name: context-management
version: 2.0.0
description: |
  Proactive context window management via token monitoring, intelligent extraction, and selective rehydration.
  Use when approaching token limits or needing to preserve essential context.
  Complements /transcripts and PreCompact hook with proactive optimization.
---

# Context Management Skill

## Purpose

This skill enables proactive management of Claude Code's context window through intelligent token monitoring, context extraction, and selective rehydration. Instead of reactive recovery after compaction, this skill helps users preserve essential context before hitting limits and restore it efficiently when needed.

## When to Use This Skill

- **Token monitoring**: Check current usage and get recommendations
- **Approaching limits**: Create snapshots at 70-85% usage
- **After compaction**: Restore essential context without full conversation
- **Long sessions**: Preserve key decisions and state proactively
- **Complex tasks**: Keep requirements and progress accessible
- **Context switching**: Save state when pausing work
- **Team handoffs**: Package context for others to continue

## Quick Start

### Check Token Status

```
User: Check my current token usage
```

I'll use the `context_manager` tool to check status:

```python
from context_manager import check_context_status

status = check_context_status(current_tokens=<current_count>)
# Returns: ContextStatus with usage percentage and recommendations
```

### Create a Snapshot

```
User: Create a context snapshot named "auth-implementation"
```

I'll use the `context_manager` tool to create a snapshot:

```python
from context_manager import create_context_snapshot

snapshot = create_context_snapshot(
    conversation_data=<conversation_history>,
    name="auth-implementation"
)
# Returns: ContextSnapshot with snapshot_id, file_path, and token_count
```

### Restore Context

```
User: Restore context from snapshot <snapshot_id> at essential level
```

I'll use the `context_manager` tool to rehydrate:

```python
from context_manager import rehydrate_from_snapshot

context = rehydrate_from_snapshot(
    snapshot_id="20251116_143522",
    level="essential"  # or "standard" or "comprehensive"
)
# Returns: Formatted context text ready to process
```

### List Snapshots

```
User: List my context snapshots
```

I'll use the `context_manager` tool to list snapshots:

```python
from context_manager import list_context_snapshots

snapshots = list_context_snapshots()
# Returns: List of snapshot metadata dicts
```

## Detail Levels

When rehydrating context, choose the appropriate detail level:

- **Essential** (smallest): Requirements + current state only (~250 tokens)
- **Standard** (balanced): + key decisions + open items (~800 tokens)
- **Comprehensive** (complete): + full decisions + tools used + metadata (~1,250 tokens)

Start with essential and upgrade if more context is needed.

## Actions

### Action: `status`

Check current token usage and get recommendations.

**Usage:**

```python
from context_manager import check_context_status

status = check_context_status(current_tokens=750000)
print(f"Usage: {status.percentage}%")
print(f"Status: {status.threshold_status}")
print(f"Recommendation: {status.recommendation}")
```

**Returns:**

- `ContextStatus` object with usage details
- `threshold_status`: 'ok', 'consider', 'recommended', or 'urgent'
- `recommendation`: Human-readable action suggestion

### Action: `snapshot`

Create intelligent context snapshot.

**Usage:**

```python
from context_manager import create_context_snapshot

snapshot = create_context_snapshot(
    conversation_data=messages,
    name="feature-name"  # Optional
)
print(f"Snapshot ID: {snapshot.snapshot_id}")
print(f"Token count: {snapshot.token_count}")
print(f"Saved to: {snapshot.file_path}")
```

**Returns:**

- `ContextSnapshot` object with metadata
- Snapshot saved to `.claude/runtime/context-snapshots/`

### Action: `rehydrate`

Restore context from snapshot at specified detail level.

**Usage:**

```python
from context_manager import rehydrate_from_snapshot

context = rehydrate_from_snapshot(
    snapshot_id="20251116_143522",
    level="standard"  # essential, standard, or comprehensive
)
print(context)  # Display restored context
```

**Returns:**

- Formatted markdown text with restored context
- Ready to process and continue work

### Action: `list`

List all available context snapshots.

**Usage:**

```python
from context_manager import list_context_snapshots

snapshots = list_context_snapshots()
for snapshot in snapshots:
    print(f"{snapshot['id']}: {snapshot['name']} ({snapshot['size']})")
```

**Returns:**

- List of snapshot metadata dicts
- Includes: id, name, timestamp, size, token_count

## Proactive Usage Workflow

### Step 1: Monitor Token Usage

Periodically check status during long sessions:

```python
status = check_context_status(current_tokens=current)

if status.threshold_status == 'consider':
    # Usage at 70%+ - consider creating snapshot
    print("Consider creating a snapshot soon")
elif status.threshold_status == 'recommended':
    # Usage at 85%+ - snapshot recommended
    create_context_snapshot(messages, name='current-work')
elif status.threshold_status == 'urgent':
    # Usage at 95%+ - create snapshot immediately
    create_context_snapshot(messages, name='urgent-backup')
```

### Step 2: Create Snapshot at Threshold

When 70-85% threshold reached, create a named snapshot:

```python
snapshot = create_context_snapshot(
    conversation_data=messages,
    name='descriptive-name'
)
# Save snapshot ID for later rehydration
```

### Step 3: Continue Working

After snapshot creation:

- Continue conversation naturally
- Let Claude Code compact if needed
- Use `/transcripts` for full history if desired
- PreCompact hook saves everything automatically

### Step 4: Rehydrate After Compaction

After compaction, restore essential context:

```python
# Start minimal
context = rehydrate_from_snapshot(
    snapshot_id='20251116_143522',
    level='essential'
)

# If more context needed, upgrade to standard
context = rehydrate_from_snapshot(
    snapshot_id='20251116_143522',
    level='standard'
)

# For complete context, use comprehensive
context = rehydrate_from_snapshot(
    snapshot_id='20251116_143522',
    level='comprehensive'
)
```

## Integration with Existing Systems

### vs. PreCompact Hook

**PreCompact Hook** (automatic safety net):

- Triggered by Claude Code before compaction
- Saves complete conversation transcript
- Automatic, no user action needed
- Full conversation export to markdown

**Context Skill** (proactive optimization):

- Triggered by user when monitoring indicates
- Saves intelligent context extraction
- User-initiated, deliberate choice
- Essential context only, not full dump

**Relationship**: Complementary, not competing. Hook = safety net, Skill = optimization.

### vs. /transcripts Command

**/transcripts** (reactive restoration):

- Restores full conversation after compaction
- Complete history, all messages
- Used when you need everything back
- Reactive recovery tool

**Context Skill** (proactive preservation):

- Preserves essential context before compaction
- Selective rehydration, not full history
- Used when you want efficient context
- Proactive optimization tool

**Relationship**: Transcripts for full recovery, skill for efficient management.

### Storage Locations

- **Snapshots**: `.claude/runtime/context-snapshots/` (JSON)
- **Transcripts**: `.claude/runtime/logs/<session_id>/CONVERSATION_TRANSCRIPT.md`
- **No conflicts**: Different directories, different purposes

## Automatic Management

Context management runs automatically via the post_tool_use hook:

- Monitors token usage every Nth tool use (adaptive frequency)
- Creates snapshots at thresholds (30%, 40%, 50% for 1M models)
- Detects compaction (token drop > 30%)
- Auto-rehydrates after compaction at appropriate level

This happens transparently without user intervention.

## Implementation

All context management functionality is provided by:

- **Tool**: `.claude/tools/amplihack/context_manager.py`
- **Hook Integration**: `.claude/tools/amplihack/context_automation_hook.py`
- **Hook System**: `.claude/tools/amplihack/hooks/tool_registry.py`

See tool documentation for complete API reference and implementation details.

## Common Patterns

### Pattern 1: Preventive Snapshotting

Check before long operation and create snapshot if needed:

```python
status = check_context_status(current_tokens=current)
if status.threshold_status in ['recommended', 'urgent']:
    create_context_snapshot(messages, name='before-refactoring')
```

### Pattern 2: Context Switching

Save state when pausing work on one feature to start another:

```python
# Pausing work on Feature A
create_context_snapshot(messages, name='feature-a-paused')

# [... work on Feature B ...]

# Resume Feature A later
context = rehydrate_from_snapshot('feature-a-snapshot-id', level='standard')
```

### Pattern 3: Team Handoff

Create comprehensive snapshot for teammate:

```python
snapshot = create_context_snapshot(
    messages,
    name='handoff-to-alice-api-work'
)
# Share snapshot ID with teammate
# Alice can rehydrate and continue work
```

## Philosophy Alignment

### Ruthless Simplicity

- Four single-purpose components in one tool
- On-demand invocation, no background processes
- Standard library only, no external dependencies
- Clear public API with convenience functions

### Single Responsibility

- ContextManager coordinates all operations
- Token monitoring, extraction, rehydration in one place
- No duplicate code or scattered logic

### Zero-BS Implementation

- No stubs or placeholders
- All functions work completely
- Real token estimation, not fake
- Actual file operations, not simulated

### Trust in Emergence

- User decides when to snapshot, not automatic (unless via hook)
- User chooses detail level, not system
- Proactive choice empowers the user

## Tips for Effective Context Management

1. **Monitor regularly**: Check status at natural breakpoints
2. **Snapshot strategically**: At 70-85% or before long operations
3. **Start minimal**: Use essential level first, upgrade if needed
4. **Name descriptively**: Use clear snapshot names for later reference
5. **List periodically**: Review and clean old snapshots
6. **Combine tools**: Use with /transcripts for full recovery option
7. **Trust emergence**: Don't over-snapshot, let context flow naturally

## Resources

- **Tool**: `.claude/tools/amplihack/context_manager.py`
- **Hook**: `.claude/tools/amplihack/context_automation_hook.py`
- **Philosophy**: `.claude/context/PHILOSOPHY.md`
- **Patterns**: `.claude/context/PATTERNS.md`

## Remember

This skill provides proactive context management through a clean, reusable tool. The tool can be called from skills, commands, and hooks. It complements existing tools (PreCompact hook, /transcripts) rather than replacing them. Use it to maintain clean, efficient context throughout long sessions.

**Key Takeaway**: Business logic lives in `context_manager.py`, this skill just tells you how to use it.
