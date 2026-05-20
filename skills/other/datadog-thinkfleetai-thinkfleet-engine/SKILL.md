---
name: datadog
description: "Query Datadog metrics, monitors, events, and logs via the REST API."
metadata: {"thinkfleetbot":{"emoji":"🐕","requires":{"bins":["curl","jq"],"env":["DD_API_KEY","DD_APP_KEY"]}}}
---

# Datadog

Query metrics, monitors, and logs via the Datadog API.

## Environment Variables

- `DD_API_KEY` - Datadog API key
- `DD_APP_KEY` - Datadog Application key
- `DD_SITE` - Datadog site (e.g. `datadoghq.com`, `datadoghq.eu`, default: `datadoghq.com`)

## List monitors

```bash
curl -s -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" \
  "https://api.${DD_SITE:-datadoghq.com}/api/v1/monitor" | jq '.[] | {id, name, type, overall_state}'
```

## Get monitor details

```bash
curl -s -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" \
  "https://api.${DD_SITE:-datadoghq.com}/api/v1/monitor/12345" | jq '{id, name, type, query, overall_state, message}'
```

## Mute monitor

```bash
curl -s -X POST -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" \
  -H "Content-Type: application/json" \
  "https://api.${DD_SITE:-datadoghq.com}/api/v1/monitor/12345/mute" \
  -d '{"end": '$(date -d '+1 hour' +%s)'}' | jq '{id, name}'
```

## Query metrics

```bash
curl -s -G -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" \
  "https://api.${DD_SITE:-datadoghq.com}/api/v1/query" \
  --data-urlencode "query=avg:system.cpu.user{host:my-server}" \
  --data-urlencode "from=$(date -d '1 hour ago' +%s)" \
  --data-urlencode "to=$(date +%s)" | jq '.series[0] | {metric, pointlist: .pointlist[-5:]}'
```

## Search logs

```bash
curl -s -X POST -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" \
  -H "Content-Type: application/json" \
  "https://api.${DD_SITE:-datadoghq.com}/api/v2/logs/events/search" \
  -d '{
    "filter": {"query": "service:my-app status:error", "from": "now-1h", "to": "now"},
    "page": {"limit": 10}
  }' | jq '.data[] | {timestamp: .attributes.timestamp, message: .attributes.message}'
```

## List events

```bash
curl -s -G -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" \
  "https://api.${DD_SITE:-datadoghq.com}/api/v1/events" \
  --data-urlencode "start=$(date -d '24 hours ago' +%s)" \
  --data-urlencode "end=$(date +%s)" | jq '.events[:5] | .[] | {title, date_happened, priority}'
```

## Post event

```bash
curl -s -X POST -H "DD-API-KEY: $DD_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.${DD_SITE:-datadoghq.com}/api/v1/events" \
  -d '{"title": "Deployment Complete", "text": "v1.2.3 deployed to production", "priority": "normal", "tags": ["env:prod"]}' | jq '{id: .event.id}'
```

## List dashboards

```bash
curl -s -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" \
  "https://api.${DD_SITE:-datadoghq.com}/api/v1/dashboard" | jq '.dashboards[:10] | .[] | {id, title}'
```

## Notes

- Use `DD_SITE` for EU or other regional endpoints.
- Metric queries use Datadog's query language (e.g. `avg:metric{tags}`).
- Confirm before muting monitors or posting events.
