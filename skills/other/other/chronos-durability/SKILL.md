---
name: chronos-durability
description: Test AllSource Core event durability by writing events, restarting the container, and verifying all events survive. Proves WAL + Parquet persistence guarantees. Triggers on "test durability", "durability test", "restart test", "verify persistence", "crash recovery test", "prove events survive restart".
category: testing
color: blue
displayName: Chronos Durability Test
---

# Chronos Durability Test

Proves that events written to AllSource Core survive container restarts — the core durability guarantee of WAL + Parquet.

## When invoked:

1. Run the durability test script:
   ```bash
   bash tooling/durability-test/test-durability.sh
   ```

2. Analyze the output and report:
   - Whether all events were written successfully
   - Pre-restart storage state (WAL, Parquet if available)
   - Recovery time after restart
   - **Whether all events survived the restart** (the money test)
   - Post-restart storage state comparison

3. Use appropriate flags based on context:
   - `--target docker` (default) — local Docker stack (Core on port 3280)
   - `--target compose` — Docker compose with internal ports (Core on port 3900)
   - `--target fly` — Fly.io deployment
   - `--count N` — number of events to write (default: 10)
   - `--skip-restart` — write and verify only, no restart cycle
   - `--json` — machine-readable output

4. For quick smoke tests (no restart needed):
   ```bash
   bash tooling/durability-test/test-durability.sh --skip-restart
   ```

## Test Phases

| Phase | What's Checked |
|-------|---------------|
| **Pre-flight** | Core reachable, docker/fly CLI available, container exists |
| **Baseline** | Current event count via `/api/v1/stats` |
| **Write** | Ingest N events with unique `durability-test-{timestamp}` entity |
| **Verify Write** | Query back all events, confirm count matches |
| **Storage Check** | WAL status, storage stats, deep health (informational, may skip) |
| **Restart** | `docker restart` or `fly machines restart` |
| **Recovery** | Poll `/health` every 2s until back (timeout 60s) |
| **Verify Durability** | Query same events — ALL N must be present |
| **Investigation** | Post-restart stats, WAL status, deep health comparison |

## Common Failure Patterns

- **Events lost after restart**: Volume not mounted or WAL disabled. Check `ALLSOURCE_WAL_ENABLED=true` and Docker volume mounts.
- **Partial recovery**: WAL replay incomplete. May indicate crash during fsync interval. Check `ALLSOURCE_WAL_SYNC_INTERVAL_MS`.
- **Recovery timeout**: Container takes too long to start. Check Docker logs for WAL replay errors.
- **Ops endpoints skip**: `/api/v1/ops/*` endpoints may not exist in all Core versions. This is informational only, not a failure.

## Architecture Note

This test writes **directly to Core** (`POST /api/v1/events`) to eliminate the Query Service as a variable. Core IS the database — it has WAL (CRC32, fsync), Parquet (Snappy), and DashMap. Events are durable by design.
