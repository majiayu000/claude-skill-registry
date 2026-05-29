---
name: troubleshoot
description: Read-only diagnostics and troubleshooting for SignalRoom. Use when debugging issues, checking system health, analyzing logs, or verifying connections. This skill restricts modifications to prevent accidental changes during investigation.
allowed-tools: Read, Grep, Glob, Bash
---

# Troubleshooting & Diagnostics

## Quick Health Checks

### 1. Fly.io Worker Status

```bash
fly status
fly logs --app signalroom-worker
```

### 2. Temporal Connection

```bash
python scripts/test_temporal_connection.py
```

### 3. Supabase Connection

```bash
python -c "
from signalroom.common import settings
print(f'Host: {settings.supabase_db_host}')
print(f'Port: {settings.supabase_db_port}')
print(f'User: {settings.supabase_db_user}')
"
```

### 4. Recent Pipeline Runs

```sql
SELECT load_id, schema_name, status, inserted_at
FROM s3_exports._dlt_loads
ORDER BY inserted_at DESC LIMIT 5;
```

## Common Error Patterns

### Database Errors

| Error | Cause | Check |
|-------|-------|-------|
| "password authentication failed" | Wrong user format | User should be `postgres.{project_ref}` |
| "connection refused" | Wrong host/port | Pooler: port 6543, Direct: port 5432 |
| "too many connections" | Connection leak | Use pooler, check for unclosed connections |
| "relation does not exist" | Table not created | Check schema name, run pipeline first |

### Temporal Errors

| Error | Cause | Check |
|-------|-------|-------|
| "No worker available" | Worker not running | `fly status`, `fly logs` |
| "Activity timed out" | Pipeline too slow | Check activity duration, add heartbeats |
| "RestrictedWorkflowAccessError" | Sandbox blocking imports | Use `UnsandboxedWorkflowRunner` |
| "asyncio.run() cannot be called" | Nested event loop | Use `await` directly in activities |

### Pipeline Errors

| Error | Cause | Check |
|-------|-------|-------|
| "Unknown source" | Source not registered | Check `SOURCES` dict in runner.py |
| "Primary key violation" | Duplicate data with merge | Check source data, primary key definition |
| "Column type mismatch" | Schema evolution conflict | Check dlt schema, may need table drop |

## Log Analysis

### Fly.io Logs

```bash
# Recent logs
fly logs

# Follow logs
fly logs -f

# Filter by level
fly logs | grep -i error
```

### Local Worker Logs

```bash
make logs-worker
```

### Structured Log Fields

```json
{
  "event": "pipeline_completed",
  "source": "everflow",
  "load_id": "1705312345",
  "row_counts": {"daily_stats": 523}
}
```

Search by event:
```bash
fly logs | grep "pipeline_failed"
fly logs | grep "activity_failed"
```

## Verification Commands

### Verify Environment

```bash
# Check required env vars are set
python -c "
from signalroom.common import settings
required = ['supabase_db_host', 'supabase_db_password', 'temporal_address']
for var in required:
    val = getattr(settings, var, None)
    status = '✓' if val else '✗'
    print(f'{status} {var}')
"
```

### Verify Imports

```bash
python -c "from signalroom.workers.main import main; print('OK')"
```

### Verify Temporal Activities

```bash
python -c "
from signalroom.temporal.activities import run_pipeline_activity
print('Activities import OK')
"
```

### Verify dlt Sources

```bash
python -c "
from signalroom.pipelines.runner import SOURCES
print('Registered sources:', list(SOURCES.keys()))
"
```

## Database Diagnostics

### Check Table Exists

```sql
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_name = 'daily_stats';
```

### Check Recent Data

```sql
-- Everflow
SELECT date, COUNT(*) as rows
FROM everflow.daily_stats
GROUP BY date ORDER BY date DESC LIMIT 7;

-- Redtrack
SELECT date, COUNT(*) as rows
FROM redtrack.daily_spend
GROUP BY date ORDER BY date DESC LIMIT 7;
```

### Check dlt Load History

```sql
SELECT
    load_id,
    inserted_at,
    status
FROM everflow._dlt_loads
ORDER BY inserted_at DESC LIMIT 10;
```

## Temporal UI Diagnostics

**URL**: https://cloud.temporal.io/namespaces/signalroom-713.nzg5u/workflows

### Check Workflow Status

1. Open workflow by ID
2. Look at "Event History"
3. Find failed activity
4. Expand to see error details

### Check Pending Activities

1. Go to workflow detail
2. Look for "Pending Activities" section
3. Check if worker is processing

## Network Diagnostics

### DNS Resolution

```bash
nslookup aws-0-us-east-1.pooler.supabase.com
nslookup ap-northeast-1.aws.api.temporal.io
```

### Port Connectivity

```bash
nc -zv aws-0-us-east-1.pooler.supabase.com 6543
```

## Recovery Procedures

### Restart Fly.io Worker

```bash
fly apps restart signalroom-worker
```

### Clear Stuck Pipeline State

```bash
dlt pipeline {pipeline_name} drop-pending-packages
```

### Revert Recent Changes

```bash
git log --oneline -5
git revert <commit>
```

## When to Escalate

If you cannot resolve after:
1. Checking logs for specific error
2. Verifying connections
3. Testing locally
4. Reviewing recent changes

Document findings and escalate with:
- Exact error message
- Relevant log snippets
- What you've tried
- Timeline of when it started

## References

- **API Reference**: `docs/API_REFERENCE.md` — Live docs, auth, request/response examples
- **Source Details**: `docs/SOURCES.md` — Schema, queries, implementation notes
- **Data Patterns**: `docs/DATA_ORGANIZATION.md` — Client data structure
