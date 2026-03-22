---
version: 1.0.0
name: dev-perf
description: Performance profiling via Aspire traces
user-invocable: true
argument-hint: "[endpoint-or-url]"
---

# Performance Profiling

Investigate and resolve performance issues using .NET Aspire distributed tracing. Analyzes trace span patterns to identify N+1 queries, excessive aggregate rehydration, and missing projections.

## When to Use

- An endpoint feels slow or returns high latency
- You suspect N+1 database/storage reads
- After adding new data access code and want to verify efficiency
- Comparing before/after performance of an optimization

## Prerequisites

- Aspire AppHost running (all resources healthy)
- The Aspire MCP server connected (provides `mcp__aspire__*` tools)

## Instructions for Claude

### Phase 1: Verify Environment

Check that the Aspire AppHost is running and the API is healthy.

```
mcp__aspire__list_resources
```

Confirm the target resource (usually `api`) shows `Running` / `Healthy`. If not, check console logs:

```
mcp__aspire__list_console_logs  resourceName: "<resource>"
```

If the AppHost is not running, tell the user and stop.

### Phase 2: Generate Traces

If the user provided a specific endpoint or URL, exercise it to generate a trace:

```bash
# Login (if auth required) and hit the endpoint
curl -s -c /tmp/perf-cookies.txt -X POST 'http://localhost:5132/api/auth/dev-login' \
  -H 'Content-Type: application/json' -d '{"isAdmin":true}'

curl -s -b /tmp/perf-cookies.txt -D /tmp/perf-headers.txt \
  'http://localhost:5132/api/<endpoint>' \
  -o /dev/null -w "Status: %{http_code}, Time: %{time_total}s\n"
```

Extract the trace ID from the response headers:

```bash
grep -i traceparent /tmp/perf-headers.txt
# Format: 00-{traceId}-{spanId}-{flags}
```

If no specific endpoint was given, list recent traces and pick the slowest:

```
mcp__aspire__list_traces  resourceName: "api"
```

### Phase 3: Analyze Trace

Drill into the trace to see all spans:

```
mcp__aspire__list_trace_structured_logs  traceId: "<trace-id>"
```

Count and categorize the spans. See [trace-patterns.md](trace-patterns.md) for the pattern reference.

**Key metrics to extract:**
- Total span count
- Total duration
- Number of storage reads (blob GET/HEAD operations)
- Number of unique aggregates loaded
- Number of projection reads

### Phase 4: Diagnose

Map spans back to code. Common patterns to look for:

| Span pattern | Diagnosis | Fix |
|--------------|-----------|-----|
| 3 spans per aggregate (HEAD + GET doc + GET events) | Aggregate rehydration | Use projection if only reading |
| Same aggregate loaded multiple times | Duplicate rehydration | Cache or restructure the call chain |
| 30+ spans for a single request | N+1 — loading aggregates in a loop | Replace with projection or batch query |
| Many `GetAll*` or `GetBy*` factory calls | Iterating all streams | Add a projection with an index |
| 2 spans (HEAD + GET on `projections/*.json`) | Projection read (efficient) | This is good — no action needed |
| 1 span (`GET tags/document/*.json`) | Tag-based lookup (efficient) | This is good — no action needed |

Read the relevant endpoint code to confirm which calls produce the excess spans.

### Phase 5: Recommend

Present findings to the user:

```
PERFORMANCE ANALYSIS — {endpoint}
==================================

Request:    {method} {url}
Duration:   {time}s
Spans:      {count} ({breakdown})

Diagnosis:
  {description of the bottleneck}

Bottleneck Code:
  {file}:{line} — {description of the problematic call}

Recommendation:
  {specific fix — e.g., "Replace factory.GetByXAsync() with projection lookup"}

Expected Improvement:
  Spans: {current} → ~{expected}
  Reason: {why this reduces spans}
```

### Phase 6: Verify Fix (if user applies the fix)

After code changes:

1. Restart the resource:
   ```
   mcp__aspire__execute_resource_command  resourceName: "api"  commandName: "resource-restart"
   ```

2. Wait for healthy state, then re-exercise the same endpoint (Phase 2)

3. Pull the new trace and compare:
   ```
   Before: {X} spans, {Y}s
   After:  {X} spans, {Y}s
   Improvement: {reduction}
   ```

4. If spans are still high, repeat from Phase 3.

## Flags

| Flag | Behavior |
|------|----------|
| (no flag) | Full profiling workflow — trace, analyze, recommend |
| `--compare` | Re-run a previous trace comparison after a fix |

## Supporting Files

- [trace-patterns.md](trace-patterns.md) — Detailed span pattern reference for event sourcing projects
