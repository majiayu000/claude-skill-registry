---
name: monitor-episodic-archiver
description: >
  Monitor episodic archiver health and run nightly analysis pipeline.
  Health dashboard, failure patterns, session aging alerts.
  Nightly: archive + high-fidelity taxonomy + user profiling + lessons.
allowed-tools:
  - Bash
  - Read
triggers:
  - monitor episodes
  - episodic health
  - unresolved sessions
  - session health
  - context loss check
  - nightly episodes
metadata:
  short-description: Health monitoring + nightly pipeline for episodic archiver

provides:
  - monitor-episodic-archiver
composes:
  - episodic-archiver
  - scheduler
  - memory
  - task-monitor
---

# Monitor Episodic Archiver

**Track session health, run nightly analysis with user profiling, and catch aging unresolved sessions.**

## Continuous Operation (Non-Negotiable)

This skill is **always-on**. It:
- Runs on its configured schedule indefinitely — it NEVER stops unless explicitly halted by the user
- The agent MUST NOT stop and wait for the human to ask for status or remember to check
- If a cycle fails, diagnose the failure, attempt auto-repair, and continue
- Only escalate to the human if genuinely blocked after exhausting /dogpile research
- Gracefully handles restarts and maintains state across cycles
- Is designed for multi-day/week/month autonomous operation

**Anti-pattern**: Reporting status and waiting for the human to ask "what next?" is UNACCEPTABLE. The agent must proactively fix issues and continue the monitoring loop.

## Quick Start

```bash
cd .pi/skills/monitor-episodic-archiver

# Health dashboard
./run.sh dashboard

# Quick health check (JSON for automation)
./run.sh check --json

# List unresolved sessions with aging flags
./run.sh list-unresolved

# Analyze failure patterns
./run.sh analyze-patterns

# Run nightly pipeline (archive + analyze + profile)
./run.sh nightly --hours 24

# Dry run (see what would be processed)
./run.sh nightly --dry-run --json

# Register for daily scheduler
./run.sh register-nightly
```

## Nightly Pipeline

```
3:00 AM daily (via scheduler)
    |
    v
Archive recent sessions (--no-analyze, fast)
    |
    v
Re-analyze with high-fidelity taxonomy (LLM)
    |
    v
Extract user behavioral profiles
    |
    v
Merge into user_priors (RGMem incremental)
    |
    v
Store lessons to /memory with bridge tags
    |
    v
Health check + report
    |
    v
~/.pi/monitor-episodic-archiver/nightly_report.json
```

### Model Selection

- Default: `deepseek-ai/DeepSeek-V3.1-TEE` (0.60s latency, 6 instances)
- Override: `./run.sh nightly --model <model-id>`
- Set via `CHUTES_MODEL_ID` env var

## Commands

### `dashboard` - Rich health overview
### `check` - Automated health check (exit 0/1/2)
### `list-unresolved` - Sessions needing attention
### `analyze-patterns` - Failure pattern analysis
### `nightly` - Full nightly pipeline
### `register-nightly` - Register with scheduler

## Health Criteria

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Unresolved rate | <20% | 20-40% | >40% |
| Oldest unresolved | <14 days | 14-30 days | >30 days |
| Success rate | >75% | 50-75% | <50% |

## Integration

| Skill | How |
|-------|-----|
| `episodic-archiver` | Queries collections, runs archive/analyze |
| `task-monitor` | Reports pipeline progress via registry.json |
| `scheduler` | Registers nightly job at 3am |
| `memory` | Stores lessons from resolved sessions |
| `taxonomy` | High-fidelity bridge classification |
| `scillm` | LLM completions for analysis + profiling |

## State Files

```
~/.pi/monitor-episodic-archiver/
  health_report.json       # Latest health check
  nightly_report.json      # Latest nightly pipeline report
  nightly_state.json       # Nightly run history
  task_state_nightly.json  # Task-monitor progress tracking
  pattern_cache.json       # Cached failure patterns
  alert_history.jsonl      # Alert log
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ARANGO_URL` | http://localhost:8529 | ArangoDB connection |
| `ARANGO_DB` | memory | Database name |
| `CHUTES_MODEL_ID` | deepseek-ai/DeepSeek-V3.1-TEE | LLM model for nightly |
| `ALERT_AGE_DAYS` | 14 | Days before session flagged |
| `CRITICAL_AGE_DAYS` | 30 | Days before critical alert |
