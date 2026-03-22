---
name: grafana
description: Avoid common Grafana mistakes — query pitfalls, variable templating, alerting traps, and provisioning gotchas. Also use for querying Grafana API and Loki directly via HTTP.
---

# Grafana + Loki

## Grafana API (local — porta 3000)

```bash
GRAFANA_URL="http://localhost:3000"
GRAFANA_AUTH="admin:${GRAFANA_PASSWORD}"  # ou token

# Health check
curl -s "$GRAFANA_URL/api/health" | jq .

# List dashboards
curl -s -u "$GRAFANA_AUTH" "$GRAFANA_URL/api/search" | jq '.[] | {id, title, url}'

# Get dashboard by UID
curl -s -u "$GRAFANA_AUTH" "$GRAFANA_URL/api/dashboards/uid/UID" | jq '.dashboard.panels[].title'

# List datasources
curl -s -u "$GRAFANA_AUTH" "$GRAFANA_URL/api/datasources" | jq '.[] | {id, name, type}'

# Query datasource directly
curl -s -u "$GRAFANA_AUTH" -X POST "$GRAFANA_URL/api/ds/query" \
  -H "Content-Type: application/json" \
  -d '{"queries":[{"refId":"A","expr":"{job=\"nginx\"}","datasource":{"type":"loki"},"maxLines":100}],"from":"now-1h","to":"now"}'
```

## Loki API (local — porta 3100)

```bash
LOKI_URL="http://localhost:3100"

# Query logs (últimos 100 de nginx)
curl -s "$LOKI_URL/loki/api/v1/query_range" \
  --data-urlencode 'query={job="nginx"}' \
  --data-urlencode 'start='"$(date -d '1 hour ago' +%s%N)" \
  --data-urlencode 'end='"$(date +%s%N)" \
  --data-urlencode 'limit=100' | jq '.data.result[].values[][1]'

# Query com filtro de texto
curl -s "$LOKI_URL/loki/api/v1/query_range" \
  --data-urlencode 'query={job="nginx"} |= "error"' \
  --data-urlencode 'limit=50' | jq '.data.result[].values[][1]'

# Labels disponíveis
curl -s "$LOKI_URL/loki/api/v1/labels" | jq '.data[]'

# Valores de um label
curl -s "$LOKI_URL/loki/api/v1/label/job/values" | jq '.data[]'
```

## LogQL — Queries Úteis

```logql
# Erros Laravel nas últimas 2h
{job="laravel"} |= "ERROR" | json

# Erros por app
sum by (app) (count_over_time({job="laravel"} |= "ERROR" [1h]))

# Nginx 5xx
{job="nginx"} | regexp `"(?P<status>\d{3})"` | status >= 500

# Timeout Next.js
{job="nginx"} |= "timed out" |= "myapp"

# Top IPs com erros
{job="nginx"} |= "error" | regexp `(?P<ip>[\d.]+)` | count by (ip) > 10

# SSH brute force attempts
{job="auth"} |= "Failed password" | count_over_time[5m] > 5

# OOM kills
{job="syslog"} |= "Out of memory"

# Queries lentas Laravel
{job="laravel"} |= "SLOW"
```

## Variables e Templating

- Multi-value variable precisa de `$__all` no regex
- `${var:csv}` para comma-separated — `${var:pipe}` para pipe-separated em regex
- `$__interval` se auto-ajusta ao range — use para aggregation window
- Variáveis encadeadas: filho depende do pai — setar "Refresh" em "On time range change"

## Panel Tips

- "No data" vs "null" são diferentes — configurar em display options
- Thresholds funcionam no último valor — não em todos do range
- Time series para tendências, stat para valor atual
- Evite `networkidle` como waitUntil — SPAs podem nunca atingir idle

## Alerting

- Alert avalia no servidor — não no browser, query deve funcionar sem variáveis
- Variáveis NÃO são suportadas em alerts — hardcode os valores
- Alert state "Pending" antes de "Firing" — previne flapping
- Canal de notificação deve estar configurado — alert sem canal = silêncio

## Provisioning

```bash
# Dashboards em /etc/grafana/provisioning/dashboards/
# Datasources em /etc/grafana/provisioning/datasources/

# Reload após mudanças
curl -s -X POST -u admin:$GRAFANA_PASSWORD http://localhost:3000/api/admin/provisioning/dashboards/reload
curl -s -X POST -u admin:$GRAFANA_PASSWORD http://localhost:3000/api/admin/provisioning/datasources/reload
```

## Erros Comuns

- Dashboard exportado inclui UID do datasource — vai falhar em import diferente
- Dashboards provisionados são read-only por default — `allowEditing: true` no yaml
- Queries de anotação adicionam carga no DB — usar com moderação
- Panel queries rodam em todo refresh — queries pesadas = dashboard lento
