---
name: ralph-memory-sync
description: Sync buffered memories to Cognee. Use when agent-memory reconnects or to force sync pending entries.
triggers:
  - /ralph.memory-sync
  - sync memories
  - sync buffer
---

# /ralph.memory-sync

Synchronize locally buffered memories to Cognee (agent-memory).

## When to Use

- After Cognee reconnects following outage
- Before session end to ensure all memories persisted
- When pending buffer grows large
- After fixing failed sync entries

## Process

1. **Check Cognee Availability**

   Run `/ralph.preflight` to verify Cognee is accessible.

   If Cognee unavailable, abort sync with message.

2. **Count Pending Entries**

   ```bash
   pending=$(ls .ralph/memory-buffer/pending/*.json 2>/dev/null | wc -l)
   failed=$(ls .ralph/memory-buffer/failed/*.json 2>/dev/null | wc -l)
   echo "Pending: $pending, Failed: $failed"
   ```

3. **Sync Pending Entries**

   For each file in `.ralph/memory-buffer/pending/`:

   a. Read entry content
   b. Send to Cognee via agent-memory
   c. On success: move to `synced/`
   d. On failure: increment retry count
   e. After 3 failures: move to `failed/`

4. **Report Results**

## Output: Success

```
RALPH WIGGUM MEMORY SYNC
========================

Cognee Status: Connected
Buffer Status:
  - Pending: 15 entries
  - Failed: 0 entries

Syncing...
  [1/15] decision-abc123 -> synced
  [2/15] session-def456 -> synced
  ...
  [15/15] decision-xyz789 -> synced

Results:
  - Synced: 15
  - Failed: 0
  - Remaining: 0

All memories synchronized successfully.
```

## Output: Partial Failure

```
RALPH WIGGUM MEMORY SYNC
========================

Cognee Status: Connected
Buffer Status:
  - Pending: 15 entries
  - Failed: 2 entries

Syncing...
  [1/15] decision-abc123 -> synced
  [2/15] session-def456 -> FAILED (retry 1/3)
  [3/15] decision-ghi789 -> synced
  ...

Results:
  - Synced: 13
  - Failed: 2 (moved to failed/)
  - Remaining: 0

WARN: 2 entries failed after max retries.
Review: .ralph/memory-buffer/failed/
```

## Output: Cognee Unavailable

```
RALPH WIGGUM MEMORY SYNC
========================

Cognee Status: UNAVAILABLE
  Reason: COGNEE_API_KEY not set

Cannot sync memories. Options:
  1. Set COGNEE_API_KEY and retry
  2. Run 'agent-memory health' to diagnose
  3. Entries remain safely in local buffer

Pending entries preserved in:
  .ralph/memory-buffer/pending/
```

## Buffer Entry Format

Each entry in `.ralph/memory-buffer/pending/`:

```json
{
  "id": "decision-abc123",
  "type": "decision",
  "dataset": "sessions",
  "timestamp": "2026-01-16T14:30:00Z",
  "content": {
    "decision": "Use polling instead of sleep in tests",
    "rationale": "Constitution principle V requires K8s-native patterns",
    "task_id": "T001",
    "alternatives": ["time.sleep()", "asyncio.sleep()"]
  },
  "sync_attempts": 0
}
```

## Handling Failed Entries

For entries in `.ralph/memory-buffer/failed/`:

1. **Review the entry** to understand why it failed
2. **Fix if possible** (e.g., correct malformed JSON)
3. **Move back to pending** to retry:
   ```bash
   mv .ralph/memory-buffer/failed/entry.json .ralph/memory-buffer/pending/
   ```
4. **Run sync again**: `/ralph.memory-sync`

Or discard if no longer needed:
```bash
rm .ralph/memory-buffer/failed/entry.json
```

## Auto-Sync Triggers

Memory sync is automatically triggered:

| Event | Trigger |
|-------|---------|
| Session start | If `sync_on_session_start: true` |
| Cognee reconnects | If `auto_sync_on_reconnect: true` |
| `/ralph.cleanup` | Final sync before worktree removal |

## Configuration

From `.ralph/config.yaml`:

```yaml
resilience:
  memory_buffer:
    enabled: true
    buffer_dir: ".ralph/memory-buffer"
    max_retry_attempts: 3
    auto_sync_on_reconnect: true
    sync_on_session_start: true
    synced_retention_hours: 24
```

## Force Sync Script

For programmatic use:

```bash
# Sync all pending
python -c "
from pathlib import Path
import json

pending = Path('.ralph/memory-buffer/pending')
for f in pending.glob('*.json'):
    entry = json.loads(f.read_text())
    print(f'Would sync: {entry[\"id\"]}')
"
```

## Related Commands

- `/ralph.memory-status` - Check buffer status without syncing
- `/ralph.preflight` - Verify Cognee connectivity
- `/ralph.resume` - Resume with synced context
