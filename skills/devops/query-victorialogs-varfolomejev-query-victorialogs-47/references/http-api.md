# VictoriaLogs HTTP API Reference

All endpoints support GET (query string) and POST (x-www-form-urlencoded). POST recommended for long queries.

## Time Parameters (common)

- `start` / `end`: RFC3339 (`2023-06-20T15:32:10Z`), Unix seconds/ms/us/ns, or duration (`5m`, `1h`, `1d`)
- Range is half-open: `[start, end)`
- If omitted: uses min/max timestamps in storage

## Query Endpoints

### `/select/logsql/query` — Query Logs

Returns NDJSON stream of matching log entries.

| Param | Required | Description |
|-------|----------|-------------|
| `query` | Yes | LogsQL query |
| `limit` | No | Max entries to return |
| `start` | No | Time range start |
| `end` | No | Time range end |

```bash
curl "$VL_URL/select/logsql/query" \
  -H 'Accept: application/stream+json' \
  -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' \
  --data-urlencode "query=_time:5m error" \
  -d 'limit=100' \
  --insecure
```

### `/select/logsql/hits` — Hit Counts by Time Buckets

| Param | Required | Description |
|-------|----------|-------------|
| `query` | Yes | LogsQL query |
| `step` | No | Bucket duration (e.g. `60000ms`, `1m`) |
| `start` | No | Time range start |
| `end` | No | Time range end |

```bash
curl "$VL_URL/select/logsql/hits" \
  -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' \
  --data-urlencode "query=_time:1h error" \
  -d 'step=60000ms' \
  --insecure
```

### `/select/logsql/stats_query` — Instant Stats

Query must contain a `stats` pipe.

| Param | Required | Description |
|-------|----------|-------------|
| `query` | Yes | LogsQL with `| stats ...` |
| `time` | No | Evaluation timestamp (default: now) |
| `start` | No | Time range start |
| `end` | No | Time range end |

```bash
curl "$VL_URL/select/logsql/stats_query" \
  -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' \
  --data-urlencode "query=_time:5m error | stats count() as errors" \
  --insecure
```

### `/select/logsql/stats_query_range` — Range Stats (Time Series)

| Param | Required | Description |
|-------|----------|-------------|
| `query` | Yes | LogsQL with `| stats ...` |
| `start` | Yes | Time range start |
| `end` | Yes | Time range end |
| `step` | Yes | Aggregation interval (e.g. `1m`, `5m`) |

### `/select/logsql/tail` — Live Tailing

Persistent streaming connection.

| Param | Required | Description |
|-------|----------|-------------|
| `query` | Yes | LogsQL query |
| `start_offset` | No | Return historical logs from this duration ago |

```bash
curl -N "$VL_URL/select/logsql/tail" \
  --data-urlencode "query=error" \
  -d 'start_offset=5m' \
  --insecure
```

## Discovery Endpoints

### `/select/logsql/field_names` — List Field Names
```bash
curl "$VL_URL/select/logsql/field_names" \
  --data-urlencode "query=_time:5m *" --insecure
```

### `/select/logsql/field_values` — List Field Values
```bash
curl "$VL_URL/select/logsql/field_values" \
  --data-urlencode "query=_time:5m *" \
  -d 'field=level' --insecure
```

### `/select/logsql/streams` — List Log Streams
```bash
curl "$VL_URL/select/logsql/streams" \
  --data-urlencode "query=_time:5m *" --insecure
```

### `/select/logsql/stream_field_names` — List Stream Field Names
### `/select/logsql/stream_field_values` — List Stream Field Values
### `/select/logsql/stream_ids` — List Stream IDs
### `/select/logsql/facets` — Facets (frequent values per field)
