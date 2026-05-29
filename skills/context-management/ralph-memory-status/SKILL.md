---
name: ralph-memory-status
description: Show memory buffer status including pending, synced, and failed entry counts. Quick health check without syncing.
triggers:
  - /ralph.memory-status
  - memory status
  - buffer status
---

# /ralph.memory-status

Display the status of the memory write-ahead buffer without syncing.

## When to Use

- Quick check of buffer health
- Before starting a new session
- To monitor buffer growth during work
- To check if sync is needed

## Process

1. **Count Entries in Each Directory**

   ```bash
   pending=$(ls .ralph/memory-buffer/pending/*.json 2>/dev/null | wc -l)
   synced=$(ls .ralph/memory-buffer/synced/*.json 2>/dev/null | wc -l)
   failed=$(ls .ralph/memory-buffer/failed/*.json 2>/dev/null | wc -l)
   ```

2. **Check Cognee Connectivity**

   Quick health check (no full sync).

3. **Report Status**

## Output: Healthy

```
RALPH WIGGUM MEMORY STATUS
==========================

Buffer Location: .ralph/memory-buffer/

Entry Counts:
  - Pending: 0
  - Synced (cached): 5
  - Failed: 0

Cognee Status: Connected
  API: https://api.cognee.ai
  Response: 142ms

Last Sync: 2026-01-16T14:30:00Z (15 minutes ago)

Status: HEALTHY - Buffer empty, ready for use
```

## Output: Pending Entries

```
RALPH WIGGUM MEMORY STATUS
==========================

Buffer Location: .ralph/memory-buffer/

Entry Counts:
  - Pending: 12
  - Synced (cached): 5
  - Failed: 0

Pending Entries:
  1. 2026-01-16T14:30:00-decision-abc123.json (decision)
  2. 2026-01-16T14:32:00-session-def456.json (session)
  3. 2026-01-16T14:35:00-decision-ghi789.json (decision)
  ... (9 more)

Cognee Status: Connected

Status: WARN - 12 entries pending sync
Action: Run /ralph.memory-sync to synchronize
```

## Output: Failed Entries

```
RALPH WIGGUM MEMORY STATUS
==========================

Buffer Location: .ralph/memory-buffer/

Entry Counts:
  - Pending: 3
  - Synced (cached): 5
  - Failed: 2

FAILED ENTRIES (need attention):
  1. 2026-01-16T12:00:00-decision-xyz123.json
     Error: Invalid JSON structure
  2. 2026-01-16T12:30:00-session-abc789.json
     Error: Cognee rejected (schema mismatch)

Cognee Status: Connected

Status: WARN - 2 failed entries need review
Action: Review .ralph/memory-buffer/failed/ and fix or discard
```

## Output: Cognee Unavailable

```
RALPH WIGGUM MEMORY STATUS
==========================

Buffer Location: .ralph/memory-buffer/

Entry Counts:
  - Pending: 8
  - Synced (cached): 5
  - Failed: 0

Cognee Status: UNAVAILABLE
  Reason: Connection timeout

Status: DEGRADED
  - New memories will buffer locally
  - Existing pending entries preserved
  - Sync when Cognee reconnects

Action: Check Cognee connectivity, then /ralph.memory-sync
```

## Quick Status Check (Bash)

For scripts or quick checks:

```bash
# One-liner status
echo "Pending: $(ls .ralph/memory-buffer/pending/*.json 2>/dev/null | wc -l | tr -d ' '), Failed: $(ls .ralph/memory-buffer/failed/*.json 2>/dev/null | wc -l | tr -d ' ')"
```

## Entry Details

To inspect a specific entry:

```bash
cat .ralph/memory-buffer/pending/2026-01-16T14-30-00-decision-abc123.json | python -m json.tool
```

## Buffer Size Thresholds

| Pending Count | Status | Action |
|---------------|--------|--------|
| 0-10 | HEALTHY | Normal operation |
| 11-50 | WARN | Consider syncing soon |
| 51+ | ALERT | Sync recommended |

| Failed Count | Status | Action |
|--------------|--------|--------|
| 0 | HEALTHY | No issues |
| 1-5 | WARN | Review when convenient |
| 6+ | ALERT | Immediate review needed |

## Cleanup Synced Entries

Synced entries are kept for verification but can be cleaned:

```bash
# Remove synced entries older than 24 hours
find .ralph/memory-buffer/synced -name "*.json" -mtime +1 -delete
```

## Configuration

From `.ralph/config.yaml`:

```yaml
resilience:
  memory_buffer:
    synced_retention_hours: 24  # Auto-clean synced after 24h
```

## Related Commands

- `/ralph.memory-sync` - Sync pending entries to Cognee
- `/ralph.preflight` - Full pre-flight check
- `/ralph.resume` - Resume session with memory context
