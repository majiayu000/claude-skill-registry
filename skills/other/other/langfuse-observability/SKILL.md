---
name: langfuse-observability
description: LLM observability with Langfuse — query traces, generations, costs, metrics, and debug LLM pipelines via the REST API
---

# Langfuse Observability

Langfuse is an open-source LLM observability platform. Use this skill to query traces, generations, costs, and metrics from a self-hosted or cloud Langfuse instance.

## Setup

```bash
# Set your Langfuse credentials
export LANGFUSE_HOST="https://langfuse.example.com"  # or https://cloud.langfuse.com
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
```

All API calls use basic auth with public key as username and secret key as password.

```bash
# Base pattern for all requests
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/<endpoint>"
```

## Health check

```bash
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/health" | jq .
```

## Traces

### List recent traces

```bash
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/traces?limit=10&page=1" | \
  jq '.data[] | {id, name, timestamp, userId, totalCost, latency, tags}'
```

### Filter by time range

```bash
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/traces?limit=20&fromTimestamp=2026-02-01T00:00:00Z&toTimestamp=2026-02-28T23:59:59Z" | \
  jq '.data[] | {id, name, timestamp, totalCost, latency}'
```

### Filter by user or name

```bash
# By user
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/traces?limit=10&userId=USER_ID" | \
  jq '.data[] | {id, name, timestamp, totalCost}'

# By trace name
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/traces?limit=10&name=TRACE_NAME" | \
  jq '.data[] | {id, name, timestamp, totalCost}'
```

### Get trace details

```bash
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/traces/TRACE_ID" | \
  jq '{id, name, timestamp, userId, sessionId, totalCost, latency, tags, metadata,
       observations: [.observations[] | {id, type, name, model, startTime, totalCost, usage}]}'
```

### Get trace input/output

```bash
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/traces/TRACE_ID" | jq '{input, output}'
```

## Generations (LLM calls)

### List recent generations

```bash
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/observations?type=GENERATION&limit=10&page=1" | \
  jq '.data[] | {id, name, model, startTime, totalCost, inputUsage: .usage.input, outputUsage: .usage.output}'
```

### Filter by model

```bash
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/observations?type=GENERATION&limit=10" | \
  jq '[.data[] | select(.model | test("gpt-4"))] | .[] | {id, model, totalCost}'
```

### Get generations for a trace

```bash
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/observations?type=GENERATION&traceId=TRACE_ID" | \
  jq '.data[] | {id, name, model, totalCost, usage, input, output}'
```

### Generation details

```bash
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/observations/OBSERVATION_ID" | \
  jq '{id, type, name, model, modelParameters, startTime, endTime, totalCost, usage, level, statusMessage}'
```

## Errors and warnings

```bash
# Find errors
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/observations?level=ERROR&limit=10" | \
  jq '.data[] | {id, traceId, name, model, level, statusMessage, startTime}'

# Find warnings
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/observations?level=WARNING&limit=10" | \
  jq '.data[] | {id, traceId, name, model, level, statusMessage, startTime}'
```

## Daily metrics

### Cost and usage by day

```bash
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/metrics/daily?limit=7" | \
  jq '.data[] | {date, traces: .countTraces, cost: .totalCost,
      models: [.usage[] | {model, input: .inputUsage, output: .outputUsage, total: .totalUsage}]}'
```

### Total cost summary

```bash
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/metrics/daily?limit=30" | \
  jq '{totalCost: ([.data[].totalCost] | add), totalTraces: ([.data[].countTraces] | add),
       days: (.data | length), breakdown: [.data[] | {date, cost: .totalCost, traces: .countTraces}]}'
```

## Sessions

```bash
# List recent sessions
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/sessions?page=1&limit=10" | \
  jq '.data[] | {id, createdAt, projectId}'

# Get session details
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/sessions/SESSION_ID" | jq .
```

## Scores

```bash
# List scores
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/scores?limit=10" | \
  jq '.data[] | {id, name, value, dataType, traceId, comment}'

# Scores for a specific trace
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/scores?traceId=TRACE_ID" | \
  jq '.data[] | {name, value, dataType, comment}'
```

## Docker self-hosted deployment

```yaml
services:
  langfuse-web:
    image: langfuse/langfuse:3
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://user:pass@postgres:5432/langfuse
      NEXTAUTH_SECRET: your-secret
      SALT: your-salt
      ENCRYPTION_KEY: your-encryption-key
      NEXTAUTH_URL: https://langfuse.example.com
      AUTH_DISABLE_SIGNUP: "true"
    depends_on: [postgres]

  langfuse-worker:
    image: langfuse/langfuse-worker:3
    environment:
      DATABASE_URL: postgresql://user:pass@postgres:5432/langfuse
      SALT: your-salt
      ENCRYPTION_KEY: your-encryption-key

  postgres:
    image: postgres:17
    volumes:
      - langfuse_pg:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: langfuse
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
```

Langfuse v3 also supports ClickHouse for trace storage, Redis for queuing, and MinIO for object storage.

## OpenRouter integration

Send traces automatically from OpenRouter to Langfuse:

1. Go to https://openrouter.ai/settings/integrations
2. Enable Langfuse destination
3. Set Base URL: `https://langfuse.example.com`
4. Add Public Key and Secret Key from Langfuse Settings → API Keys

All OpenRouter LLM calls will then appear as traces in Langfuse.

## Common queries

### Most expensive traces this week

```bash
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/traces?limit=50&fromTimestamp=$(date -d '7 days ago' +%FT00:00:00Z)" | \
  jq '[.data[] | {id, name, totalCost, timestamp}] | sort_by(-.totalCost) | .[:10]'
```

### Model usage breakdown

```bash
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/observations?type=GENERATION&limit=100" | \
  jq '[.data[] | .model] | group_by(.) | map({model: .[0], count: length}) | sort_by(-.count)'
```

### Error rate

```bash
ERRORS=$(curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/observations?level=ERROR&limit=1" | jq '.meta.totalItems')
TOTAL=$(curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/observations?limit=1" | jq '.meta.totalItems')
echo "Error rate: $ERRORS / $TOTAL"
```

## Tips

- Always use time filters (`fromTimestamp`/`toTimestamp`) on large queries to avoid timeouts
- Pagination: responses include `meta.page`, `meta.limit`, `meta.totalItems`, `meta.totalPages`
- Timestamps use ISO 8601 format: `2026-02-10T00:00:00Z`
- Cost values are in USD
- Token counts are in `usage.input`, `usage.output`, `usage.total`
- The web UI at your Langfuse URL provides visual exploration of traces
