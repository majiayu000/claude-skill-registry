---
name: codex-log-guard
description: Automatically diagnose excessive Codex local SQLite diagnostic log writes and give a concrete fix plan. Use when a user asks whether Codex is writing too much to disk, mentions logs_2.sqlite, logs_2.sqlite-wal, block_log_inserts, SSD/TBW wear from Codex logs, or wants Codex log write issues checked, explained, stopped, cleaned up, verified, or restored.
---

# Codex Log Guard

## Overview

Automatically diagnose Codex persistent diagnostic logging from local evidence, then give a concise conclusion and the safest next action. Do not make the user choose from a command menu.

## Default Flow

When the user asks to "check", "看看", "诊断", or asks whether the local machine is affected:

1. Inspect all candidate live database files and schemas:
   - `~/.codex/logs_2.sqlite`
   - `~/.codex/sqlite/logs_2.sqlite`
2. Identify which candidate database is currently held by Codex processes.
3. Check whether `block_log_inserts` already exists on each candidate with a `logs` table.
4. Measure whether `logs` is still being written using `COUNT(*), MIN(id), MAX(id)` samples.
   Treat `MAX(id)` or `MIN(id)` movement with stable `COUNT(*)` as active churn, not necessarily disk growth.
4. Inspect low-level log volume with `TRACE`/`DEBUG` counts and top noisy targets.
5. Check which Codex processes currently hold each candidate database.
6. Return a diagnosis with:
   - current state: healthy / protected / affected historically / actively writing / actively growing on disk / missing database / blocked
   - evidence: file sizes, trigger state, row/min-id/max-id samples, level distribution, active path
   - recommended next action: do nothing / install trigger / cleanup later / cleanup now / restore logging
7. Do not ask the user which command to run. Choose the diagnosis path from the evidence.

When the user asks to "处理", "修一下", "止血", or explicitly approves mitigation:

1. Install `block_log_inserts` first.
2. Verify that `COUNT(*), MAX(id)` stops growing.
3. If disk space should be reclaimed, create a SQLite `.backup`, then delete log rows, vacuum, and truncate WAL.
4. Report the backup path and final file sizes.

When the user asks to restore diagnostics:

1. Drop `block_log_inserts`.
2. Sample `COUNT(*), MAX(id)` to confirm logging resumes or stays quiet.

## Evidence Commands

Run direct shell/SQLite commands. Use only the needed subset for the user's request; do not paste a menu back to the user.

Inspect files:

```bash
for db in ~/.codex/logs_2.sqlite ~/.codex/sqlite/logs_2.sqlite; do
  ls -lh "$db"* 2>/dev/null
  du -h "$db"* 2>/dev/null
done
```

Check schema and trigger:

```bash
db=~/.codex/logs_2.sqlite
sqlite3 "$db" ".tables"
sqlite3 "$db" "PRAGMA table_info(logs);"
sqlite3 "$db" "SELECT name, tbl_name, sql FROM sqlite_master WHERE type='trigger' AND name='block_log_inserts';"
```

Sample writes and growth:

```bash
db=~/.codex/logs_2.sqlite
for i in 1 2 3; do
  date '+%F %T'
  sqlite3 "$db" "SELECT COUNT(*) AS rows, MIN(id) AS min_id, MAX(id) AS max_id FROM logs;"
  stat -f '%N %z bytes mtime=%Sm' "$db" "$db-wal" "$db-shm" 2>/dev/null
  sleep 10
done
```

Inspect levels and noisy targets:

```bash
db=~/.codex/logs_2.sqlite
sqlite3 "$db" "SELECT level, COUNT(*) AS n, ROUND(SUM(estimated_bytes)/1024.0/1024.0, 1) AS estimated_mib FROM logs GROUP BY level ORDER BY n DESC;"
sqlite3 "$db" "SELECT target, level, COUNT(*) AS n, ROUND(SUM(estimated_bytes)/1024.0/1024.0, 1) AS estimated_mib FROM logs GROUP BY target, level ORDER BY n DESC LIMIT 15;"
```

Check open processes:

```bash
lsof ~/.codex/logs_2.sqlite ~/.codex/logs_2.sqlite-wal ~/.codex/logs_2.sqlite-shm \
     ~/.codex/sqlite/logs_2.sqlite ~/.codex/sqlite/logs_2.sqlite-wal ~/.codex/sqlite/logs_2.sqlite-shm 2>/dev/null
```

Install protection:

```bash
db=~/.codex/logs_2.sqlite
sqlite3 "$db" "PRAGMA busy_timeout=10000; CREATE TRIGGER IF NOT EXISTS block_log_inserts BEFORE INSERT ON logs BEGIN SELECT RAISE(IGNORE); END;"
```

Clean up after protection:

```bash
db="$HOME/.codex/logs_2.sqlite"
backup="$db.bak.$(date +%Y%m%d-%H%M%S)"
sqlite3 "$db" ".backup '$backup'"
sqlite3 "$db" "PRAGMA busy_timeout=10000; PRAGMA wal_checkpoint(TRUNCATE); DELETE FROM logs; VACUUM; PRAGMA wal_checkpoint(TRUNCATE);"
echo "$backup"
```

Restore persistent logging:

```bash
db=~/.codex/logs_2.sqlite
sqlite3 "$db" "DROP TRIGGER IF EXISTS block_log_inserts;"
```

## Diagnosis Rules

- Missing all candidate `logs_2.sqlite` files: healthy/not applicable unless the user expects Codex to have run.
- If multiple candidates exist, call out the active path from `lsof`; do not assume the top-level path is the only live database.
- Trigger present and `COUNT/MIN(id)/MAX(id)` stable: protected.
- Trigger absent and `MIN(id)` or `MAX(id)` moves: affected and actively writing.
- If row ids move but file sizes do not materially increase, say "actively writing/churning" rather than "actively growing on disk".
- Trigger absent, database large, high `TRACE`/`DEBUG`, but no sample movement: affected historically; recommend protection, cleanup optional.
- Main DB or WAL above hundreds of MB: recommend cleanup after installing protection if the active path is affected.
- WAL mtime or tiny WAL growth alone is not enough; use row/max-id samples.
- If `logs` is absent or schema differs, stop and report that the known workaround is not safely applicable.

## Safety Rules

- Run read-only diagnosis before write operations unless the user explicitly asks for a specific command.
- Do not claim the issue is fixed from file size alone; verify with `COUNT(*), MAX(id)` sampling.
- Treat `cleanup` as reversible only through its timestamped backup. Mention the backup path in the final answer.
- Do not delete backups automatically.
- If SQLite reports lock or corruption errors, stop and report the exact error. Do not kill Codex processes unless the user explicitly asks.
- This skill only manages Codex local SQLite diagnostic logs (`~/.codex/logs_2.sqlite*` and `~/.codex/sqlite/logs_2.sqlite*`); it does not manage conversation archives, repo files, credentials, or remote telemetry.

## Answer Shape

Keep the user-facing answer short:

1. One-line conclusion.
2. Key evidence in 3-5 bullets.
3. Recommended action and whether it was already applied.
4. Backup path only if cleanup ran.
