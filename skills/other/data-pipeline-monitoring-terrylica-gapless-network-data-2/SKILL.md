---
name: data-pipeline-monitoring
description: Monitor and troubleshoot dual-pipeline data collection systems on GCP. This skill should be used when checking pipeline health, viewing logs, diagnosing failures, or monitoring long-running operations for data collection workflows. Supports Cloud Run Jobs (batch pipelines) and VM systemd services (real-time streams).
---

# Data Pipeline Monitoring

Monitor and operate dual-pipeline data collection systems deployed on Google Cloud Platform.

## Purpose

Provide systematic workflows for:

1. **Health checking** - Verify both batch and real-time pipelines are operational
2. **Log viewing** - Access logs from Cloud Run Jobs and VM systemd services
3. **Troubleshooting** - Diagnose and recover from common failure modes
4. **Progress monitoring** - Track long-running operations like historical backfills
5. **Service management** - Restart services, update configurations, deploy fixes

## When to Use This Skill

Invoke this skill when the user mentions any of:

- "Check if the pipeline is running"
- "View logs for [service/job]"
- "Why is [pipeline] failing"
- "Monitor the backfill progress"
- "Restart the collector service"
- "Verify both pipelines are healthy"
- "Check for errors in the last hour"
- "Show me the latest execution status"

This skill applies to dual-pipeline architectures where:
- **Batch pipeline** runs on Cloud Run Jobs (scheduled executions)
- **Real-time pipeline** runs on VM with systemd service (continuous streaming)

## Core Workflows

### Workflow 1: Health Check Both Pipelines

Use the provided health check script for automated status verification:

```bash
python3 scripts/check_pipeline_health.py \
  --gcp-project PROJECT_ID \
  --cloud-run-job JOB_NAME \
  --region REGION \
  --vm-name VM_NAME \
  --vm-zone ZONE \
  --systemd-service SERVICE_NAME
```

**Output**: Status report showing OK/WARNING/CRITICAL for each component

**Manual verification** (if script unavailable):

1. Check batch pipeline last execution:
   ```bash
   gcloud run jobs executions list \
     --job JOB_NAME \
     --region REGION \
     --project PROJECT_ID \
     --limit 1 \
     --format "value(metadata.name,status.conditions[0].type)"
   ```

2. Check real-time pipeline service status:
   ```bash
   gcloud compute ssh VM_NAME \
     --zone ZONE \
     --project PROJECT_ID \
     --command='sudo systemctl is-active SERVICE_NAME'
   ```

**Expected**: Batch shows `Completed`, real-time shows `active`

### Workflow 2: View Logs

Use the provided log viewer script for unified log access:

```bash
# Cloud Run Job logs
bash scripts/view_logs.sh \
  --type cloud-run \
  --project PROJECT_ID \
  --job JOB_NAME \
  --region REGION \
  --lines 50

# VM systemd service logs
bash scripts/view_logs.sh \
  --type systemd \
  --project PROJECT_ID \
  --vm VM_NAME \
  --zone ZONE \
  --service SERVICE_NAME \
  --lines 50 \
  --follow
```

**Common filters**:
- `--filter "ERROR"` - Show only errors
- `--filter "Block [0-9]+"` - Show block collection progress
- `--follow` or `-f` - Real-time log streaming

**Manual commands** (see `references/gcp-monitoring-patterns.md` for complete patterns):

For Cloud Run:
```bash
gcloud logging read \
  "resource.type=cloud_run_job AND resource.labels.job_name=JOB_NAME" \
  --limit 50 \
  --project PROJECT_ID
```

For VM systemd:
```bash
gcloud compute ssh VM_NAME \
  --zone ZONE \
  --project PROJECT_ID \
  --command='sudo journalctl -u SERVICE_NAME -n 50'
```

### Workflow 3: Troubleshoot Failures

**Step 1**: Identify the failing component

Run health check (Workflow 1) to determine which pipeline is failing.

**Step 2**: View recent logs

Run log viewer (Workflow 2) for the failing component, focusing on ERROR severity.

**Step 3**: Consult troubleshooting guide

Read `references/troubleshooting-guide.md` for common failure modes matching the error symptoms.

**Common failure patterns**:

- **gRPC metadata validation error** → Secret Manager credentials have trailing newlines, apply `.strip()`
- **Cloud Run "Failed" status** → Check logs for timeout, OOM, or permission errors
- **systemd service "inactive/failed"** → Check logs for Python tracebacks or missing dependencies
- **No data collection** → Verify API connectivity, rate limits, database access

**Step 4**: Apply recovery procedure

Execute the recovery commands from the troubleshooting guide.

**Step 5**: Verify resolution

Re-run health check to confirm both pipelines return to OK status.

### Workflow 4: Monitor Long-Running Operations

For operations like historical backfills that run for hours:

**Start operation in background**:
```bash
gcloud compute ssh VM_NAME \
  --zone ZONE \
  --project PROJECT_ID \
  --command='
    cd ~/workdir
    nohup python3 script.py > progress.log 2>&1 &
    echo "Started with PID: $!"
  '
```

**Check progress** (repeat periodically):
```bash
gcloud compute ssh VM_NAME \
  --zone ZONE \
  --project PROJECT_ID \
  --command='tail -50 ~/workdir/progress.log'
```

**Check if process still running**:
```bash
gcloud compute ssh VM_NAME \
  --zone ZONE \
  --project PROJECT_ID \
  --command='ps aux | grep script.py | grep -v grep'
```

### Workflow 5: Restart Failed Services

**For Cloud Run Jobs**:

Manually trigger a new execution:
```bash
gcloud run jobs execute JOB_NAME \
  --region REGION \
  --project PROJECT_ID
```

**For VM systemd services**:

Restart the service:
```bash
gcloud compute ssh VM_NAME \
  --zone ZONE \
  --project PROJECT_ID \
  --command='sudo systemctl restart SERVICE_NAME'
```

Wait 5 seconds, then verify:
```bash
gcloud compute ssh VM_NAME \
  --zone ZONE \
  --project PROJECT_ID \
  --command='sudo systemctl status SERVICE_NAME --no-pager'
```

### Workflow 6: Deploy Code Fixes

When code changes are needed to resolve issues:

**Step 1**: Update the code locally (use Edit tool)

**Step 2**: Copy updated file to VM:
```bash
gcloud compute scp LOCAL_FILE VM_NAME:REMOTE_PATH \
  --zone ZONE \
  --project PROJECT_ID
```

**Step 3**: Restart service to apply changes:
```bash
gcloud compute ssh VM_NAME \
  --zone ZONE \
  --project PROJECT_ID \
  --command='sudo systemctl restart SERVICE_NAME'
```

**Step 4**: Verify fix by checking logs:
```bash
gcloud compute ssh VM_NAME \
  --zone ZONE \
  --project PROJECT_ID \
  --command='sudo journalctl -u SERVICE_NAME -n 20 --no-pager'
```

## Bundled Resources

### Scripts

**`scripts/check_pipeline_health.py`** - Automated health check for both pipelines
- Returns OK/WARNING/CRITICAL status for each component
- Supports JSON output for programmatic use
- Exits with code 1 if any CRITICAL failures detected

**`scripts/view_logs.sh`** - Unified log viewer for Cloud Run and systemd
- Supports real-time following (`--follow`)
- Supports regex filtering (`--filter "PATTERN"`)
- Handles both Cloud Run Jobs and VM systemd services

### References

**`references/gcp-monitoring-patterns.md`** - Complete command reference
- Load this when user needs specific gcloud commands
- Contains patterns for Cloud Run Jobs, VM systemd services, Secret Manager, Cloud Scheduler
- Includes dual-pipeline monitoring patterns

**`references/troubleshooting-guide.md`** - Failure diagnosis and recovery
- Load this when user reports errors or pipeline failures
- Contains common failure modes with symptoms, causes, and recovery procedures
- Includes diagnostic script for escalation scenarios

## Configuration

To use the scripts, provide these parameters:

**GCP Configuration**:
- `PROJECT_ID` - GCP project ID
- `REGION` - Cloud Run region (e.g., `us-east1`)

**Batch Pipeline**:
- `JOB_NAME` - Cloud Run Job name

**Real-Time Pipeline**:
- `VM_NAME` - VM instance name
- `ZONE` - VM zone (e.g., `us-east1-b`)
- `SERVICE_NAME` - systemd service name

**Example values** from MotherDuck integration:
```
PROJECT_ID=eonlabs-ethereum-bq
REGION=us-east1
JOB_NAME=eth-md-updater
VM_NAME=eth-realtime-collector
ZONE=us-east1-b
SERVICE_NAME=eth-collector
```

## Best Practices

1. **Always check health before investigating** - Run health check first to determine scope
2. **Use scripts for repetitive tasks** - Leverage provided scripts instead of manual commands
3. **Follow progressive troubleshooting** - Start with logs, then consult troubleshooting guide
4. **Verify fixes after applying** - Re-run health check to confirm resolution
5. **Monitor both pipelines together** - Dual pipelines are designed to complement each other

## Integration with Project Documentation

This skill complements project-specific documentation:

- **Architecture docs** - Explain dual-pipeline design rationale
- **Deployment guides** - Cover initial setup and configuration
- **This skill** - Focus on operational monitoring and troubleshooting

Load project documentation when needed for context, but use this skill's workflows for operational tasks.

## Cross-Reference: Data Completeness Verification

**Important**: This skill monitors pipeline health (whether pipelines are running), NOT data completeness.

For verifying actual data in ClickHouse (block counts, historical data presence):
- Use the **historical-backfill-execution** skill
- Run `scripts/clickhouse/verify_blocks.py` for database state verification

**Common scenario**: Pipeline health checks show OK, but historical data is missing. This happens because:
- Cloud Run hourly sync only loads last 2 hours (NOT historical)
- VM real-time collector only captures new blocks (NOT historical)
- Historical backfill requires separate one-time execution

See `historical-backfill-execution` skill for backfill operations and troubleshooting missing data.
