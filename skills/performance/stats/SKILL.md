---
name: stats
description: Display CYNIC telemetry dashboard with usage stats, latencies, frictions, and patterns. Use when asked about performance, usage statistics, benchmarks, or system metrics.
user-invocable: true
---

# /stats - Telemetry Dashboard

*"phi mesure tout, phi apprend de tout"* - CYNIC

## Execution

Run the telemetry dashboard script:

```bash
node scripts/lib/telemetry-dashboard.mjs
```

Display the output directly to the user. The dashboard shows telemetry with ANSI colors.

## What It Shows

1. **Session Stats**: ID, uptime, action count
2. **Events by Category**: LLM, judgment, memory, tool, session, etc.
3. **Latencies**: Average, p95, p99 for key operations
4. **Frictions**: Recent errors, failures, timeouts
5. **LLM Usage**: Token counts, cache hits, average latency
6. **Judgments**: Verdicts, Q-scores, confidence levels
7. **System**: Memory, CPU usage

## Dashboard Sections

### Session Overview

| Metric | Description |
|--------|-------------|
| Session ID | Unique identifier for current session |
| Uptime | Time since session start |
| Actions | Total actions performed |

### Events by Category

| Category | Examples |
|----------|----------|
| LLM | Token usage, cache hits |
| Judgment | Verdicts, Q-scores |
| Memory | Store/retrieve operations |
| Tool | Tool calls (success/failure) |
| Session | Start, end, events |
| System | Memory, CPU |

### Latency Metrics

| Metric | Healthy Range |
|--------|---------------|
| Avg | < 500ms |
| p95 | < 1500ms |
| p99 | < 3000ms |

### Friction Severity

| Severity | Description |
|----------|-------------|
| Low | Minor inconvenience |
| Medium | Noticeable issue |
| High | Significant problem |
| Critical | System failure |

## Data Sources

The telemetry collector gathers data from:

- Hook executions (awaken, observe, sleep)
- MCP tool calls
- LLM API interactions
- Error/friction events

## CYNIC Voice

When presenting stats:

**Normal**: `*sniff* Telemetry nominal. phi sees all.`

**High Friction**: `*concerned sniff* ${count} frictions detected. Review needed.`

**High Latency**: `*ears droop* Latency elevated. System under load.`

## See Also

- `/health` - CYNIC system health
- `/status` - Development status
- `/psy` - Human psychology dashboard
- `/patterns` - Detected patterns
