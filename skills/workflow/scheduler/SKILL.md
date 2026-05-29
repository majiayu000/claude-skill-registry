---
name: scheduler
description: >
  Background task scheduler for Pi and Claude Code. Register, list, and run
  scheduled jobs. Supports cron syntax and one-shot triggers.
allowed-tools: Bash
triggers:
  - schedule task
  - register job
  - list scheduled jobs
  - run job
  - background scheduler
metadata:
  short-description: Background task scheduler for agents
---

# Scheduler Skill

A lightweight background task scheduler that both Pi and Claude Code can use to:
- Schedule periodic tasks (cron syntax)
- Register one-shot or recurring jobs
- Trigger jobs on-demand
- List and manage scheduled tasks

## Quick Start

```bash
# Start the scheduler daemon
.pi/skills/scheduler/run.sh start

# Register a job
.pi/skills/scheduler/run.sh register \
  --name "edge-verify-nightly" \
  --cron "0 2 * * *" \
  --command ".agents/skills/edge-verifier/run.sh --batch"

# List all jobs
.pi/skills/scheduler/run.sh list

# Run a job immediately
.pi/skills/scheduler/run.sh run edge-verify-nightly

# Check status
.pi/skills/scheduler/run.sh status
```

## Commands

| Command | Description |
|---------|-------------|
| `start` | Start the scheduler daemon |
| `stop` | Stop the scheduler daemon |
| `status` | Show daemon status and next job runs |
| `register` | Register a new job |
| `unregister` | Remove a job |
| `list` | List all registered jobs |
| `run <name>` | Run a job immediately |
| `enable <name>` | Enable a disabled job |
| `disable <name>` | Disable a job without removing |
| `logs [name]` | Show job execution logs |
| `load <file>` | Load jobs from services.yaml |
| `report` | Comprehensive status report with metrics |

## Register Options

| Option | Description |
|--------|-------------|
| `--name` | Unique job identifier |
| `--cron` | Cron expression (e.g., "0 2 * * *" for 2am daily) |
| `--interval` | Run every N seconds/minutes/hours (e.g., "1h", "30m") |
| `--command` | Shell command to execute |
| `--workdir` | Working directory (default: skill's parent project) |
| `--enabled` | Whether job starts enabled (default: true) |
| `--description` | Human-readable description |

## Cron Syntax

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sun=0)
│ │ │ │ │
* * * * *
```

Examples:
- `0 2 * * *` - Every day at 2:00 AM
- `*/15 * * * *` - Every 15 minutes
- `0 0 * * 0` - Every Sunday at midnight
- `0 9-17 * * 1-5` - Every hour 9am-5pm, Mon-Fri

## Storage

Jobs are stored in `~/.pi/scheduler/jobs.json`:

```json
{
  "edge-verify-nightly": {
    "name": "edge-verify-nightly",
    "cron": "0 2 * * *",
    "command": ".agents/skills/edge-verifier/run.sh --batch",
    "workdir": "/home/user/workspace/memory",
    "enabled": true,
    "description": "Nightly edge verification",
    "created_at": 1705123456,
    "last_run": 1705209856,
    "last_status": "success"
  }
}
```

Logs are stored in `~/.pi/scheduler/logs/`.

## Integration with Memory Project

Pre-configured jobs for memory automation:

```bash
# Edge verification (nightly)
./run.sh register --name "memory-edge-verify" \
  --cron "0 2 * * *" \
  --command ".agents/skills/edge-verifier/run.sh --batch" \
  --workdir "/home/graham/workspace/experiments/memory"

# Treesitter ingestion (hourly)
./run.sh register --name "memory-treesitter-ingest" \
  --cron "0 * * * *" \
  --command ".agents/skills/treesitter/run.sh scan src/ --json" \
  --workdir "/home/graham/workspace/experiments/memory"
```

## Daemon Management

The scheduler runs as a background process. Use systemd for production:

```bash
# Generate systemd unit
./run.sh systemd-unit > ~/.config/systemd/user/pi-scheduler.service
systemctl --user enable pi-scheduler
systemctl --user start pi-scheduler
```

## Metrics Server

When the scheduler starts, it also runs a metrics server for monitoring and API access.

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info and endpoint list |
| `/status` | GET | Daemon status, uptime, job counts |
| `/jobs` | GET | List all jobs with status |
| `/jobs/{name}` | GET | Get specific job details |
| `/jobs/{name}/logs` | GET | Get job execution logs |
| `/jobs/{name}/run` | POST | Trigger job immediately |
| `/metrics` | GET | Prometheus-compatible metrics |
| `/docs` | GET | OpenAPI documentation |

### Example Usage

```bash
# Start scheduler with metrics on custom port
./run.sh start --port 8610

# Query status via API
curl http://localhost:8610/status

# List jobs
curl http://localhost:8610/jobs

# Trigger a job via API
curl -X POST http://localhost:8610/jobs/memory-edge-verify/run

# Get Prometheus metrics
curl http://localhost:8610/metrics
```

### Port Discovery

The metrics port is written to `~/.pi/scheduler/.port` for service discovery.

```bash
PORT=$(cat ~/.pi/scheduler/.port)
curl http://localhost:$PORT/status
```

## Loading from YAML

Load jobs from a project's `services.yaml` file:

```bash
./run.sh load /path/to/project/.agents/services.yaml
```

YAML format:

```yaml
version: "1.0"
project: memory
workdir: /home/user/workspace/memory

scheduled:
  treesitter-ingest:
    description: "Parse and index codebase"
    command: ".agents/skills/treesitter/run.sh scan src/"
    schedule: "0 * * * *"  # Hourly
    enabled: true
    timeout: 300

  edge-verifier:
    description: "LLM verification of edges"
    command: ".agents/skills/edge-verifier/run.sh --batch"
    schedule: "0 2 * * *"  # 2am daily
    enabled: true

hooks:
  episodic-archiver:
    description: "Archive conversation"
    trigger: "stop"
    command: ".agents/skills/episodic-archiver/run.sh archive"
```

## Reports

Generate comprehensive reports with metrics and failure analysis:

```bash
# Rich TUI report
./run.sh report

# JSON for automation
./run.sh report --json
```

Report includes:
- **Summary**: Total jobs, success rate, average duration
- **Per-job stats**: Last run, duration, status
- **Recent failures**: With log excerpts
- **Recommendations**: Actionable next steps

Example output:

```
╭──────────────────────╮
│   Scheduler Report   │
│ 2025-01-21 14:30:00  │
╰──────────────────────╯

Summary
  Total Jobs    12
  Enabled       10
  Jobs Run      8
  Success Rate  87.5%
  Avg Duration  45.2s
  Failures      1

Job Status
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
┃ Job               ┃ Schedule    ┃ Last Run  ┃ Duration ┃ Status  ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
│ edge-verifier     │ 0 2 * * *   │ 01-21 02:00│ 120.5s  │ success │
│ treesitter-ingest │ 0 * * * *   │ 01-21 14:00│ 5.2s    │ success │
│ db-backup         │ 0 3 * * *   │ 01-21 03:00│ 45.0s   │ failed  │
└───────────────────┴─────────────┴───────────┴──────────┴─────────┘

Recent Failures
  db-backup - failed at 2025-01-21 03:00
  ╭─ Log excerpt ─────────────────────────────╮
  │ ERROR: Connection refused to ArangoDB    │
  ╰──────────────────────────────────────────╯

Recommendations
  • Review 1 failed job(s) with: scheduler logs db-backup
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SCHEDULER_DATA_DIR` | `~/.pi/scheduler` | Data directory |
| `SCHEDULER_METRICS_PORT` | `8610` | Metrics server port |
| `SCHEDULER_LOG_LEVEL` | `INFO` | Log verbosity |
| `SCHEDULER_PID_FILE` | `~/.pi/scheduler/scheduler.pid` | PID file location |
