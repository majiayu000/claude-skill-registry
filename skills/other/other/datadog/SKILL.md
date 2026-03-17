---
name: datadog-cli
description: "Use this skill when you need to search Datadog logs, query metrics, tail logs in real-time, trace distributed requests, investigate errors, compare time periods, find log patterns, check service health, or export observability data."
license: MIT
compatibility: opencode
---

# Datadog

This skill will help you to interact with Datadog, through the unofficial datadog-cli to search Datadog logs, query metrics, tail logs in real-time, trace distributed requests, investigate errors, compare time periods, find log patterns, check service health, or export observability data.

## When to Use This Skill

- Trigger phrases include:
  - "search logs"
  - "tail logs"
  - "query metrics"
  - "check Datadog"
  - "find errors"
  - "trace request"
  - "compare errors"
  - "what services exist"
  - "log patterns"
  - "CPU usage"
  - "service health"
  - "get service activity"

## How to Use

### Log Search

```bash
datadog logs search --query "<query>" [--from <time>] [--to <time>] [--limit <n>] [--sort <order>]
```

**Examples:**

```bash
datadog logs search --query "status:error" --from 1h
datadog logs search --query "service:api status:error @http.status_code:500" --from 1h
```

### Live Tail (Real-time Streaming)

Stream logs as they arrive. Press Ctrl+C to stop.

```bash
datadog logs tail --query "<query>" [--interval <seconds>]
```

**Examples:**

```bash
datadog logs tail --query "status:error"
datadog logs tail --query "service:api" --interval 5
```

### Trace Correlation

Find all logs for a distributed trace across services.

```bash
datadog logs trace --id "<trace-id>" [--from <time>] [--to <time>]
```

**Example:**

```bash
datadog logs trace --id "abc123def456" --from 24h
```

### Log Context

Get logs before and after a specific timestamp to understand what happened.

```bash
datadog logs context --timestamp "<iso-timestamp>" [--before <time>] [--after <time>] [--service <svc>]
```

**Examples:**

```bash
datadog logs context --timestamp "2024-01-15T10:30:00Z" --before 5m --after 2m
datadog logs context --timestamp "2024-01-15T10:30:00Z" --service api --before 10m
```

### Error Summary

Quick breakdown of errors by service, type, and message.

```bash
datadog errors [--from <time>] [--to <time>] [--service <svc>]
```

**Examples:**

```bash
datadog errors --from 1h
datadog errors --service payment-api --from 24h
```

### Period Comparison

Compare log counts between current period and previous period.

```bash
datadog logs compare --query "<query>" --period <time>
```

**Examples:**

```bash
datadog logs compare --query "status:error" --period 1h
datadog logs compare --query "service:api status:error" --period 6h
```

### Log Patterns

Group similar log messages to find patterns (replaces UUIDs, numbers, etc.).

```bash
datadog logs patterns --query "<query>" [--from <time>] [--limit <n>]
```

**Examples:**

```bash
datadog logs patterns --query "status:error" --from 1h
datadog logs patterns --query "service:api" --from 6h --limit 1000
```

### Service Discovery

List all services with recent log activity.

```bash
datadog services [--from <time>] [--to <time>]
```

**Example:**

```bash
datadog services --from 24h
```

### Log Aggregation

```bash
datadog logs agg --query "<query>" --facet <facet> [--from <time>]
```

**Common facets:** `status`, `service`, `host`, `@http.status_code`, `@error.kind`

**Examples:**

```bash
datadog logs agg --query "*" --facet status --from 1h
datadog logs agg --query "status:error" --facet service --from 24h
```

### Multiple Queries

Run multiple queries in parallel.

```bash
datadog logs multi --queries "name1:query1,name2:query2" [--from <time>]
```

**Example:**

```bash
datadog logs multi --queries "errors:status:error,warnings:status:warn" --from 1h
```

### Metrics Query

```bash
datadog metrics query --query "<metrics-query>" [--from <time>] [--to <time>]
```

**Query format:** `<aggregation>:<metric>{<tags>}`

**Examples:**

```bash
datadog metrics query --query "avg:system.cpu.user{*}" --from 1h
datadog metrics query --query "avg:system.cpu.user{service:api}" --from 1h
datadog metrics query --query "sum:trace.http.request.errors{service:api}.as_count()" --from 1h
```

## Global Flags

| Flag | Description |
|------|-------------|
| `--pretty` | Human-readable output with colors |
| `--output <file>` | Export results to JSON file |
| `--site <site>` | Datadog site (e.g., `datadoghq.eu`) |

## Time Formats

- Relative: `30m`, `1h`, `6h`, `24h`, `7d`
- ISO 8601: `2024-01-15T10:30:00Z`

## Common Workflows

### Incident Triage

```bash
# 1. Quick error overview
datadog errors --from 1h

# 2. Is this new? Compare to previous period
datadog logs compare --query "status:error" --period 1h

# 3. What patterns are we seeing?
datadog logs patterns --query "status:error" --from 1h

# 4. Narrow down by service
datadog logs search --query "status:error service:payment-api" --from 1h

# 5. Get context around a specific timestamp
datadog logs context --timestamp "2024-01-15T10:30:00Z" --service api --before 5m --after 2m

# 6. Follow the distributed trace
datadog logs trace --id "TRACE_ID"
```

### Real-time Debugging

```bash
# Stream errors as they happen
datadog logs tail --query "status:error"

# Watch specific service
datadog logs tail --query "service:api status:error"
```

### Service Health Check

```bash
# List services
datadog services --from 24h

# Check error distribution
datadog logs agg --query "service:api" --facet status --from 1h

# Check CPU/memory
datadog metrics query --query "avg:system.cpu.user{service:api}" --from 1h
```

### Export for Sharing

```bash
# Save search results
datadog logs search --query "status:error" --from 1h --output errors.json

# Save error summary
datadog errors --from 24h --output error-report.json
```

## Datadog Query Syntax

| Operator | Example | Description |
|----------|---------|-------------|
| `AND` | `service:api status:error` | Both conditions |
| `OR` | `status:error OR status:warn` | Either condition |
| `-` | `-status:info` | Exclude |
| `*` | `service:api-*` | Wildcard |
| `>=` `<=` | `@http.status_code:>=400` | Numeric comparison |
| `[TO]` | `@duration:[1000 TO 5000]` | Range |

### Common Attributes

- `service` - Service name
- `status` - Log level (error, warn, info, debug)
- `host` - Hostname
- `@http.status_code` - HTTP status code
- `@error.kind` - Error type
- `@trace_id` / `@dd.trace_id` - Trace ID
