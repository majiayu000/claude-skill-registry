---
name: thor-db
description: Analyze THOR's SQLite database (thor10.db/thor11.db) for performance tuning, scan timing, resume state, and delta comparisons. Use when investigating slow scans, debugging performance, or understanding what THOR tracked.
---

# THOR DB Skill

THOR maintains an SQLite database for timing telemetry, scan resume state, and delta comparisons between scans.

## What ThorDB Covers

- **Performance telemetry** – Timing data for rules, modules, and scan elements
- **Scan resume state** – Markers to continue interrupted scans
- **Delta comparison** – Compare current vs previous module results for `--diff` mode

## Quick Commands

Disable ThorDB:
```bash
# v11
thor64.exe --exclude-component ThorDB -p C:\

# v10
thor64.exe --nothordb -p C:\
```

Override location (v11):
```bash
thor64.exe --thordb-path /custom/path/ -p C:\
```

Find the database:
```bash
# Windows admin
dir C:\ProgramData\thor\thor*.db

# Linux root
ls -la /var/lib/thor/thor*.db

# Linux user
ls -la ~/.local/state/thor/thor*.db
```

Open with SQLite:
```bash
sqlite3 /var/lib/thor/thor10.db
```

## Use Cases

### Performance Analysis

When THOR is slow, check what's taking time:
```sql
-- Top time sinks overall
SELECT category, element, count, duration/1e9 AS seconds
FROM times ORDER BY duration DESC LIMIT 20;
```

### Identifying Slow Rules

Find rules or elements with high average time:
```sql
SELECT category, element, count,
       (duration*1.0/count)/1e9 AS avg_seconds
FROM times WHERE count >= 5
ORDER BY (duration*1.0/count) DESC LIMIT 20;
```

### Resume Investigation

Check resume markers and scan metadata:
```sql
SELECT key, value FROM tbl ORDER BY key;
```

## Resume Behavior

Resume requires ThorDB to be enabled and command line arguments to match.

### THOR v11 Resume Flags

```bash
# Resume if state exists, otherwise run full scan
thor64.exe --resume-scan -p C:\

# Resume only if state exists, fail otherwise
thor64.exe --resume-only -p C:\
```

To clear resume state: run THOR once without `--resume-scan`.

### THOR v10 Resume Flags

```bash
# Enable resume tracking (required since v10.5)
thor64.exe --resume -p C:\
```

Since THOR 10.5, resume state is not tracked by default due to performance implications. Start scans with `--resume` to enable resume capability.

To clear resume state: run THOR once without `--resume`.

## References

- [Database Locations](reference/locations.md) - Where to find ThorDB
- [Schema Reference](reference/schema.md) - Tables and columns
- [Useful Queries](reference/queries.md) - Analysis queries

## Scripts

- [thor_db_top_times.py](scripts/thor_db_top_times.py) - Top time consumers
- [thor_db_export_csv.py](scripts/thor_db_export_csv.py) - Export to CSV/JSON
- [thor_db_slow_rules_hint.py](scripts/thor_db_slow_rules_hint.py) - Tuning hints

## Detecting DB Name

THOR 10 uses `thor10.db`, THOR 11 uses `thor11.db`. Older deployments may show `thor.db`.

```bash
# Check binary strings
strings ./thor-linux-64 | grep -E 'thor[0-9]+\.db'

# Or trace file opens during scan
strace -f -e openat ./thor-linux-64 --quick -p /tmp 2>&1 | grep -E 'thor[0-9]+\.db'
```
