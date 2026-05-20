---
name: health-report
description: Run a health check of the AI Harness system. Checks bot status, database, heartbeat tasks, and vault consistency.
user-invocable: true
argument-hint: "[full|quick|bot|heartbeat|vault|db]"
context: fork
agent: ops
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
model: sonnet
---

# Health Report

Run a health check of the AI Harness system.

## Live System State
!`ps aux | grep -E "(bot\.ts|heartbeat-runner|claude)" | grep -v grep 2>/dev/null || echo "(no processes)"`
!`launchctl list | grep com.aiharness 2>/dev/null || echo "(no launchd agents)"`
!`ls -lh bridges/discord/harness.db 2>/dev/null || echo "(no database)"`
!`tail -3 heartbeat-tasks/logs/*.log 2>/dev/null | head -20 || echo "(no logs)"`

## Check Modules

Parse `$ARGUMENTS` to determine scope. Default is `full` (all checks).

### Bot Check (`bot` or `full`)
1. Check if bot process is running: look for `bot.ts` in process list (from live state above)
2. Check PID file: `bridges/discord/.bot.pid` — does it exist? Is the PID alive?
3. Check database exists and is readable: `bridges/discord/harness.db`
4. Report: running/stopped, PID, uptime estimate

### Database Check (`db` or `full`)
1. Check `harness.db` exists and size
2. Run `sqlite3 harness.db "SELECT name FROM sqlite_master WHERE type='table'"` to verify schema
3. Check WAL file: `harness.db-wal` existence and size
4. Count rows in key tables: sessions, channel_configs, task_queue, dead_letter
5. Report: table counts, file size, WAL status

### Heartbeat Check (`heartbeat` or `full`)
1. List LaunchAgent plists: `~/Library/LaunchAgents/com.aiharness.heartbeat.*.plist`
2. For each, check if loaded in launchctl (from live state above)
3. Read state files: `heartbeat-tasks/*.state.json` — check last_run, consecutive_failures
4. Flag any tasks with consecutive_failures > 0
5. Report: task name, status (loaded/unloaded), last run, failures

### Vault Check (`vault` or `full`)
1. Count files in `vault/learnings/` by type prefix (LRN/ERR/FEAT)
2. Check for orphaned wikilinks: grep for `[[` references and verify targets exist
3. Check for entries missing required frontmatter fields
4. Count entries by status
5. Report: file counts, any issues found

### Truncation Check (`truncation` or `full`)
1. Read `context-log/truncation-stats.json` if it exists
2. Report: events by source, average % lost, critical count
3. Flag any sources with critical truncation events
4. Read last 10 lines of `context-log/truncation-events.jsonl` for recent events
5. Report: worst truncation sources, whether structure damage occurred

### Quick Check (`quick`)
Run only: bot process alive? Database exists? Any heartbeat failures? One-line summary.

## Output Format

```
=== AI Harness Health Report ===

Bot:       RUNNING (PID 12345)
Database:  OK (harness.db, 256KB, 5 tables)
Heartbeat: 2/2 tasks loaded, 0 failures
Vault:     42 learnings (38 resolved), 0 issues
Truncation: 15 events, 0 critical, avg 12% lost

Overall: HEALTHY
```

For issues, add a `⚠ Issues` section listing each problem and suggested fix.
