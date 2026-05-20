---
description: System health monitoring - check DB, Redis, Sentry, Vercel Blob, and SLA status
---

## User Input

```text
$ARGUMENTS
```

Options: `detailed` for comprehensive report, empty for quick status

## Task

Check system health across all services and report status.

### Steps

1. **Check Database (Neon DB)**:
   ```bash
   cd backend
   python -c "
   from src.lib.database import engine
   try:
       with engine.connect() as conn:
           result = conn.execute('SELECT 1')
           print('✅ Database: Connected')
   except Exception as e:
       print(f'❌ Database: {e}')
   "
   ```

2. **Check Redis**:
   ```bash
   python -c "
   from src.lib.redis_client import redis_client
   try:
       redis_client.ping()
       print('✅ Redis: Connected')
   except Exception as e:
       print(f'❌ Redis: {e}')
   "
   ```

3. **Check Vercel Blob Storage**:
   ```bash
   curl -s https://blob.vercel-storage.com/ \
     -H "Authorization: Bearer ${BLOB_READ_WRITE_TOKEN}" | \
     grep -q "blobs" && echo "✅ Vercel Blob: Connected" || echo "❌ Vercel Blob: Failed"
   ```

4. **Check Storage Usage** (detailed mode):
   ```bash
   # Get total blob size
   python -c "
   import os
   # Calculate blob storage usage
   # Target: Stay below 4GB (80% of 5GB free tier)
   "
   ```

5. **Check Sentry Status**:
   ```bash
   curl -s "https://sentry.io/api/0/projects/" \
     -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN}" | \
     grep -q "id" && echo "✅ Sentry: Connected" || echo "⚠️ Sentry: Check auth"
   ```

6. **Check Recent Errors** (from Sentry):
   ```bash
   # List last 10 errors from past 24h
   python -c "
   import sentry_sdk
   # Query recent errors
   "
   ```

7. **Check SLA Breaches**:
   ```bash
   python -c "
   from src.models.manual_resolution import ManualResolution
   from src.lib.database import SessionLocal
   from datetime import datetime

   db = SessionLocal()
   breaches = db.query(ManualResolution).filter(
       ManualResolution.sla_deadline < datetime.utcnow(),
       ManualResolution.status == 'pending'
   ).count()

   if breaches > 0:
       print(f'⚠️ SLA Breaches: {breaches} pending cases past deadline')
   else:
       print('✅ SLA: No breaches')
   "
   ```

8. **Output Summary**:
   ```
   ✅ System Health Report
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Timestamp: 2025-12-30 12:34:56 UTC

   Services:
   ✅ Database (Neon DB): Connected
   ✅ Redis: Connected (latency: 12ms)
   ✅ Vercel Blob: Connected
   ✅ Sentry: Connected

   Storage:
   📊 Vercel Blob: 2.1 GB / 5 GB (42% used)
   ⚠️ Approaching 80% threshold at 4GB

   Errors (Last 24h):
   📊 Total Errors: 12
   🔴 Critical: 0
   🟡 Warning: 3
   🔵 Info: 9

   SLA Status:
   ✅ No SLA breaches
   📊 Manual resolution queue: 2 pending cases
   📊 Oldest case: 45 minutes

   Recommendations:
   [List any issues or warnings]
   ```

## Example Usage

```bash
/monitor           # Quick status check
/monitor detailed  # Comprehensive report with metrics
```

## Exit Criteria

- All services checked and status reported
- Storage usage calculated
- Recent errors retrieved
- SLA status verified
