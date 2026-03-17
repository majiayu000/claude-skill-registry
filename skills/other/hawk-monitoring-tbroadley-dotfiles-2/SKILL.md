---
name: monitoring
description: Monitor Hawk job status, view logs, and diagnose issues. Use when the user wants to check job progress, view error logs, debug a failing job, or generate a monitoring report for a Hawk evaluation run.
---

# Hawk Job Monitoring

Monitor running or completed Hawk jobs using the `hawk logs` command or `hawk status` subcommands.

## Job ID

The `JOB_ID` parameter is the **eval_set_id** or **scan_run_id** from when the job was submitted.

**JOB_ID is optional.** If omitted, uses the last eval set ID that was used or received.

## Available Commands

### 1. View Logs (Shorthand)

The `hawk logs` command shows logs:

```bash
hawk logs                             # Show last 100 logs (all types)
hawk logs <JOB_ID>                    # Show last 100 logs for job
hawk logs -n 50                       # Show last 50 lines
```

**Options:**
- `-n, --lines N` - Number of lines to show (default: 100)

**Note:** Do NOT use the `-f/--follow` flag - it blocks indefinitely and is intended for interactive terminal use only.

### 2. View status

Generate a full monitoring report with logs, metrics, and other details:

```bash
hawk status                           # Use last job ID
hawk status <JOB_ID>                  # Print report to stdout
hawk status <JOB_ID> > report.json      # Save to file
```

**Options:**
- `--hours {hours}` - Fetch logs from last N hours (default: 24 hours)

## Common Workflows

### Check job progress
```bash
hawk logs
```

### Generate full report for analysis
```bash
hawk status > report.status
```
