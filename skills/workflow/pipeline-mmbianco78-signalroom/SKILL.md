---
name: pipeline
description: Run dlt pipelines and Temporal workflows for SignalRoom. Use when syncing data sources, triggering workflows, checking pipeline status, or debugging data ingestion issues.
---

# Pipeline Operations

## Available Sources

| Source | Description | Schedule |
|--------|-------------|----------|
| `everflow` | Affiliate conversions/revenue | Hourly 7am-11pm ET |
| `redtrack` | Ad spend tracking | Hourly 7am-11pm ET |
| `s3_exports` | CSV files from S3 (Sticky.io) | Daily 6am ET |
| `posthog` | PostHog analytics | Stubbed |
| `mautic` | Mautic contacts/campaigns | Stubbed |
| `google_sheets` | Google Sheets data | Stubbed |

**API Reference**: See `docs/API_REFERENCE.md` for live docs, auth, and request/response examples.

## Run Pipeline Directly (Local Testing)

```bash
# Activate environment
source .venv/bin/activate

# Run a specific source
python scripts/run_pipeline.py everflow
python scripts/run_pipeline.py redtrack
python scripts/run_pipeline.py s3_exports

# Dry run (see what would happen)
python scripts/run_pipeline.py everflow --dry-run
```

## Trigger via Temporal (Production)

```bash
# Trigger and return immediately
python scripts/trigger_workflow.py everflow

# Trigger and wait for completion
python scripts/trigger_workflow.py everflow -w

# Trigger with notification on success
python scripts/trigger_workflow.py everflow -w --notify
```

## Check Pipeline Status

```bash
# View worker logs (local)
make logs-worker

# View Fly.io logs (production)
fly logs

# Temporal Cloud UI
# https://cloud.temporal.io/namespaces/signalroom-713.nzg5u/workflows
```

## Active Schedules

View in Temporal Cloud UI or:

```bash
python scripts/setup_schedules.py --list
```

Current schedules:
- `hourly-sync-everflow-redtrack` - Hourly 7am-11pm ET
- `daily-sync-s3` - Daily 6am ET

## Troubleshooting

**"Unknown source" error:**
Source not registered in `src/signalroom/pipelines/runner.py`

**Credentials error:**
Check `.env` has correct API keys

**Database connection failed:**
- Verify Supabase pooler settings (port 6543)
- User must be `postgres.{project_ref}`

**Activity timeout:**
Pipeline took >30 min. Filter resources or increase timeout.
