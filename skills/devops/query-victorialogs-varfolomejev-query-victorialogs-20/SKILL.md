---
name: query-victorialogs
description: Query and analyze logs from VictoriaLogs using LogsQL via HTTP API. Use when the user asks to "query logs", "search logs", "check VictoriaLogs", "find errors in logs", "tail logs", "get log stats", "search VictoriaLogs", "check dev/prod logs", or any log investigation task involving VictoriaLogs. Also triggers on mentions of LogsQL, VictoriaLogs, or log troubleshooting.
---

# Query VictoriaLogs

## Environment Setup

Read the project CLAUDE.md for `VL_DEV_URL` and `VL_PROD_URL` values. Default to DEV unless user specifies production.

## CRITICAL: Time Range Limits

**NEVER query more than 3 hours without explicit `_time` filter.** The server will crash on wide time ranges.

- Default: use `_time:5m` to `_time:1h` for recent logs
- Max safe range: 3 hours. NEVER exceed 3 days under any circumstances.
- Always include `_time` filter in every query — no exceptions.

### When User Knows Only a Date (Not Exact Time)

If the user says "check logs from March 20" but doesn't know the exact time, use a **two-step approach**:

**Step 1: Find the time range using `/select/logsql/hits`** — lightweight, returns only counts:
```bash
curl -s "$VL_URL/select/logsql/hits" \
  -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' \
  --data-urlencode "query=SEARCH_TERM" \
  -d 'step=3600000ms' \
  -d 'start=2026-03-20T00:00:00Z' \
  -d 'end=2026-03-20T23:59:59Z' \
  --insecure
```
This returns hit counts per hour — find which hours have data.

**Step 2: Query only the narrow time range** identified from Step 1:
```bash
curl -s "$VL_URL/select/logsql/query" \
  -H 'Accept: application/stream+json' \
  -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' \
  --data-urlencode "query=SEARCH_TERM" \
  -d 'limit=500' \
  -d 'start=2026-03-20T14:00:00Z' \
  -d 'end=2026-03-20T15:00:00Z' \
  --insecure
```

Always follow this pattern: **hits first to locate, then query to fetch.**

## How to Query

Use `curl` directly via Bash tool. Always use `--insecure` flag and POST with `application/x-www-form-urlencoded;charset=UTF-8`.

### Query Logs

```bash
curl -s "$VL_URL/select/logsql/query" \
  -H 'Accept: application/stream+json' \
  -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' \
  --data-urlencode "query=_time:5m error" \
  -d 'limit=500' \
  --insecure
```

### Hit Counts (histogram) — use to locate time ranges

```bash
curl -s "$VL_URL/select/logsql/hits" \
  -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' \
  --data-urlencode "query=_time:1h error" \
  -d 'step=60000ms' \
  --insecure
```

### Stats Query

```bash
curl -s "$VL_URL/select/logsql/stats_query" \
  -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' \
  --data-urlencode "query=_time:5m error | stats count() as errors" \
  --insecure
```

### Discover Fields/Streams

```bash
# Field names
curl -s "$VL_URL/select/logsql/field_names" --data-urlencode "query=_time:5m *" --insecure

# Field values
curl -s "$VL_URL/select/logsql/field_values" --data-urlencode "query=_time:5m *" -d 'field=level' --insecure

# Streams
curl -s "$VL_URL/select/logsql/streams" --data-urlencode "query=_time:5m *" --insecure
```

## LogsQL Quick Reference

### Filters
```
error                           # word in _msg
"connection refused"            # phrase
{app="nginx"}                   # stream filter
_time:5m                        # last 5 minutes
field:value                     # field filter
field:re("pattern")             # regexp
q1 AND q2 / q1 OR q2 / NOT q   # logical
```

### Pipes
```
| fields f1, f2                 # keep fields
| unpack_json                   # parse JSON
| stats by (field) count() as c # aggregate
| sort by (field desc)          # sort
| limit 10                      # limit
| filter field > 100            # post-filter
| top 10 by (path)             # top N
| extract_regexp "(?P<ip>...)"  # extract via regex
```

### Stats Functions
`count()`, `sum(f)`, `avg(f)`, `min(f)`, `max(f)`, `median(f)`, `quantile(0.95, f)`, `rate()`, `count_uniq(f)`, `uniq_values(f)`

For full LogsQL syntax: read `references/logsql-reference.md`
For full HTTP API details: read `references/http-api.md`

## Best Practices

- **ALWAYS include `_time` filter** — server crashes without it. Default to `_time:5m` or `_time:1h`.
- **Max 3 hours per query.** If broader search needed, use hits endpoint first to locate the right window.
- **Unknown time? Hits first, query second.** Use `/select/logsql/hits` with 1h step to scan a day, then query only the relevant hours.
- Place fastest filters (word, phrase) first, slowest (regexp) last
- Use `limit` to avoid overwhelming output — start with 100-500
- Use `| unpack_json` when logs are JSON-structured
- Use `| collapse_nums` to group similar error messages
- Use `| stats by (_stream) count()` to find noisiest services
- Pipe output through `jq` for readability when needed
