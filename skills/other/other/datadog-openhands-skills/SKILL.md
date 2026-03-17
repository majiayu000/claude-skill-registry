---
name: datadog
description: Query and analyze Datadog logs, metrics, APM traces, and monitors using the Datadog API. Use when debugging production issues, monitoring application performance, or investigating alerts.
triggers:
- datadog
---

# Datadog

<IMPORTANT>
Before performing any Datadog operations, first check if the required environment variables are set:

```bash
[ -n "$DD_API_KEY" ] && echo "DD_API_KEY is set" || echo "DD_API_KEY is NOT set"
[ -n "$DD_APP_KEY" ] && echo "DD_APP_KEY is set" || echo "DD_APP_KEY is NOT set"
[ -n "$DD_SITE" ] && echo "DD_SITE is set" || echo "DD_SITE is NOT set"
```

If any of these variables are missing, ask the user to provide them before proceeding:
- **DD_API_KEY**: Datadog API key
- **DD_APP_KEY**: Datadog Application key
- **DD_SITE**: Datadog site (e.g., `datadoghq.com`, `datadoghq.eu`, `us3.datadoghq.com`)
</IMPORTANT>

## Authentication Headers

```bash
-H "DD-API-KEY: ${DD_API_KEY}" \
-H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
-H "Content-Type: application/json"
```

## Query Logs

```bash
curl -s -X POST "https://api.${DD_SITE}/api/v2/logs/events/search" \
  -H "DD-API-KEY: ${DD_API_KEY}" \
  -H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "query": "service:my-service status:error",
      "from": "now-1h",
      "to": "now"
    },
    "sort": "-timestamp",
    "page": {"limit": 50}
  }' | jq .
```

## Query Metrics

```bash
curl -s -G "https://api.${DD_SITE}/api/v1/query" \
  -H "DD-API-KEY: ${DD_API_KEY}" \
  -H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
  --data-urlencode "query=avg:system.cpu.user{*}" \
  --data-urlencode "from=$(date -d '1 hour ago' +%s)" \
  --data-urlencode "to=$(date +%s)" | jq .
```

## Query APM Traces

```bash
curl -s -X POST "https://api.${DD_SITE}/api/v2/spans/events/search" \
  -H "DD-API-KEY: ${DD_API_KEY}" \
  -H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "query": "service:my-service",
      "from": "now-1h",
      "to": "now"
    },
    "sort": "-timestamp",
    "page": {"limit": 25}
  }' | jq .
```

## List Monitors

```bash
curl -s -G "https://api.${DD_SITE}/api/v1/monitor" \
  -H "DD-API-KEY: ${DD_API_KEY}" \
  -H "DD-APPLICATION-KEY: ${DD_APP_KEY}" | jq .
```

## Documentation

- [Logs API](https://docs.datadoghq.com/api/latest/logs/)
- [Metrics API](https://docs.datadoghq.com/api/latest/metrics/)
- [APM/Tracing API](https://docs.datadoghq.com/api/latest/tracing/)
- [Monitors API](https://docs.datadoghq.com/api/latest/monitors/)
- [Events API](https://docs.datadoghq.com/api/latest/events/)
- [Dashboards API](https://docs.datadoghq.com/api/latest/dashboards/)