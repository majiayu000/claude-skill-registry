---
name: grafana
description: "Query Grafana dashboards, data sources, alerts, and annotations via the REST API."
metadata: {"thinkfleetbot":{"emoji":"📈","requires":{"bins":["curl","jq"],"env":["GRAFANA_URL","GRAFANA_TOKEN"]}}}
---

# Grafana

Query dashboards, alerts, and data sources.

## Environment Variables

- `GRAFANA_URL` - Grafana instance URL (e.g. `https://grafana.example.com`)
- `GRAFANA_TOKEN` - API key or service account token

## List dashboards

```bash
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/search?type=dash-db&limit=20" | jq '.[] | {uid, title, url}'
```

## Get dashboard

```bash
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/dashboards/uid/my-dashboard-uid" | jq '{title: .dashboard.title, panels: [.dashboard.panels[].title], tags: .meta.tags}'
```

## List data sources

```bash
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/datasources" | jq '.[] | {id, name, type, url}'
```

## List alert rules

```bash
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/v1/provisioning/alert-rules" | jq '.[] | {uid, title, condition, for: .for}'
```

## List firing alerts

```bash
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/alertmanager/grafana/api/v2/alerts?active=true" | jq '.[] | {labels: .labels, status: .status.state, startsAt}'
```

## Query Prometheus data source

```bash
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/datasources/proxy/1/api/v1/query" \
  --data-urlencode "query=up{job='my-service'}" | jq '.data.result[] | {metric: .metric, value: .value[1]}'
```

## Query range (Prometheus)

```bash
curl -s -H "Authorization: Bearer $GRAFANA_TOKEN" \
  "$GRAFANA_URL/api/datasources/proxy/1/api/v1/query_range" \
  --data-urlencode "query=rate(http_requests_total{job='my-service'}[5m])" \
  --data-urlencode "start=$(date -d '1 hour ago' +%s)" \
  --data-urlencode "end=$(date +%s)" \
  --data-urlencode "step=60" | jq '.data.result[0].values[-5:]'
```

## Create annotation

```bash
curl -s -X POST -H "Authorization: Bearer $GRAFANA_TOKEN" \
  -H "Content-Type: application/json" \
  "$GRAFANA_URL/api/annotations" \
  -d '{"text": "Deployment v1.2.3", "tags": ["deploy","prod"], "time": '$(date +%s000)'}' | jq '{id, message}'
```

## Silence alert

```bash
curl -s -X POST -H "Authorization: Bearer $GRAFANA_TOKEN" \
  -H "Content-Type: application/json" \
  "$GRAFANA_URL/api/alertmanager/grafana/api/v2/silences" \
  -d '{
    "matchers": [{"name": "alertname", "value": "HighCPU", "isRegex": false}],
    "startsAt": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
    "endsAt": "'$(date -u -d '+1 hour' +%Y-%m-%dT%H:%M:%SZ)'",
    "comment": "Silenced by ThinkFleetBot",
    "createdBy": "thinkfleetbot"
  }' | jq '{silenceID}'
```

## Notes

- Data source proxy URLs use the data source ID (get from list data sources).
- Grafana Cloud uses `https://your-stack.grafana.net`.
- Confirm before silencing alerts or creating annotations.
