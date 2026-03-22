---
name: monitoring-alerting
description: Grafana alerts, Loki LogQL advanced queries, SLO dashboards, Telegram contact points, alerting rules for Laravel/Nginx/MySQL/Next.js
---

# Skill: Monitoring & Alerting — Grafana + Loki

## Quando Usar
- Criar ou debugar alertas no Grafana que não estão disparando (ou disparando demais)
- Escrever LogQL para encontrar padrões de erro em produção antes que o the owner perceba
- Construir dashboard de SLO para um projeto novo

## Contexto

**Stack de observabilidade deste servidor:**

| Componente | Porta | Config |
|------------|-------|--------|
| Grafana | :3000 | `/etc/grafana/grafana.ini` |
| Loki | :3100 | `/etc/loki/config.yml` |
| Promtail | :9080 | `/etc/promtail/config.yml` |

**Labels Promtail configurados (fonte: `/etc/promtail/config.yml`):**
```
job="laravel"      → apps Laravel em /home/deploy/*/storage/logs/laravel.log
job="nginx"        → /var/log/nginx/access.log + error.log
job="syslog"       → /var/log/syslog
job="auth"         → /var/log/auth.log
```

**Grafana API via curl (evita abrir navegador):**
```bash
GRAFANA="http://localhost:3000"
GRAFANA_AUTH="admin:$(grep admin_password /etc/grafana/grafana.ini | awk -F= '{print $2}' | tr -d ' ')"
```

---

## Passos / Comandos

### 1. LogQL — Queries Práticas para Este Servidor

```logql
# Taxa de erros Laravel por app (últimas 1h)
sum by (filename) (
  count_over_time({job="laravel"} |= "ERROR" [1h])
)

# 5xx Nginx — quais apps estão falhando
{job="nginx"} 
  | regexp `(?P<status>\d{3}) \d+ "(?P<agent>[^"]+)"` 
  | status >= `500`
  | line_format "{{.status}} {{.agent}}"

# Erros específicos por projeto
{job="laravel", filename=~".*api-myapp.*"} 
  |= "ERROR" 
  | json 
  | line_format "{{.message}}"

# Timeouts Nginx → Next.js (NewsApp crawler problem)
{job="nginx"} |= "timed out" |= "upstream" |= "3001"

# OOM kills (crítico — detecta memory leaks)
{job="syslog"} |= "Out of memory" | regexp `Killed process (?P<pid>\d+) \((?P<name>[^)]+)\)`

# Tentativas de brute force SSH
{job="auth"} |= "Failed password" 
  | regexp `from (?P<ip>\S+) port`
  | line_format "{{.ip}}"

# Queries lentas MySQL (se slow_query_log ativo)
{job="syslog"} |= "slow query"

# Erros de queue/job Laravel
{job="laravel"} |= "CRITICAL" |~ "job.*failed|exception.*queue"

# Monitor NewsApp pipeline — falhas de processamento
{job="laravel", filename=~".*api-myapp.*"} 
  |= "ERROR" 
  |~ "Curator|Writer|FactChecker|Translator|Gemini"
```

### 2. Alerting — Criar Alert Rule via API

```bash
# Listar alert rules existentes
curl -s "$GRAFANA/api/v1/provisioning/alert-rules" \
  -u "$GRAFANA_AUTH" | jq '.[] | {title, state}'

# Criar Contact Point Telegram (se não existir)
curl -s -X POST "$GRAFANA/api/v1/provisioning/contact-points" \
  -u "$GRAFANA_AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "telegram-alerts",
    "type": "telegram",
    "settings": {
      "botToken": "'"$TELEGRAM_BOT_TOKEN"'",
      "chatId": "'"$TELEGRAM_CHAT_ID"'"
    }
  }'

# Silenciar alerta durante deploy (15 min)
curl -s -X POST "$GRAFANA/api/alertmanager/grafana/api/v2/silences" \
  -u "$GRAFANA_AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "matchers": [{"name": "alertname", "value": "LaravelHighErrors", "isRegex": false}],
    "startsAt": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'",
    "endsAt": "'"$(date -u -d '+15 minutes' +%Y-%m-%dT%H:%M:%SZ)"'",
    "createdBy": "sre-bot",
    "comment": "Deploy em andamento"
  }'
```

### 3. SLO Dashboard — Métricas Calculadas via LogQL

```logql
# Error Rate Laravel (SLO: < 0.5%)
(
  count_over_time({job="laravel"} |= "ERROR" [5m])
  /
  count_over_time({job="laravel"} [5m])
) * 100

# Nginx 5xx Rate
(
  count_over_time({job="nginx"} | regexp `" (?P<s>[5]\d\d) ` [5m])
  /
  count_over_time({job="nginx"} [5m])
) * 100

# Taxa de falhas Horizon/Queue (NewsApp)
count_over_time(
  {job="laravel", filename=~".*api-myapp.*"} 
  |= "CRITICAL" 
  |~ "failed|exception" [10m]
)
```

### 4. Debugar Promtail — Logs Não Chegando no Loki

```bash
# Status Promtail
curl -s http://localhost:9080/metrics | grep promtail_sent_entries_total

# Ver targets configurados (quais arquivos está lendo)
curl -s http://localhost:9080/targets | python3 -m json.tool | grep -A3 "health"

# Log do próprio Promtail
journalctl -u promtail --since "30 minutes ago" --no-pager | tail -50

# Testar pipeline de um log específico
cat /home/deploy/api-myapp/storage/logs/laravel.log | tail -5

# Verificar Loki está recebendo
curl -s "http://localhost:3100/loki/api/v1/query?query={job=\"laravel\"}&limit=1" | jq .
```

### 5. Queries de Investigação Rápida (post-incident)

```bash
# Janela de tempo customizada via API Loki diretamente
START=$(date -d '2 hours ago' +%s)000000000
END=$(date +%s)000000000

curl -s "http://localhost:3100/loki/api/v1/query_range" \
  --data-urlencode "query={job=\"laravel\"} |= \"ERROR\"" \
  --data-urlencode "start=$START" \
  --data-urlencode "end=$END" \
  --data-urlencode "limit=100" | jq '.data.result[].values[][1]'

# Contar erros por hora (últimas 6h)
for h in 6 5 4 3 2 1; do
  echo -n "$h h atrás: "
  curl -s "http://localhost:3100/loki/api/v1/query" \
    --data-urlencode "query=count_over_time({job=\"laravel\"} |= \"ERROR\" [1h])" \
    --data-urlencode "time=$(date -d "$h hours ago" +%s)" | jq '.data.result[0].value[1] // "0"'
done
```

### 6. Alertas Recomendados para Este Servidor

| Alert | Condição LogQL | Severidade |
|-------|---------------|-----------|
| LaravelCritical | `count_over_time({job="laravel"} \|= "CRITICAL" [5m]) > 5` | critical |
| HorizonDead | `count_over_time({job="laravel"} \|= "No Horizon processes" [5m]) > 0` | critical |
| NginxHighErrors | Taxa 5xx > 1% em 5min | warning |
| OOMKill | `{job="syslog"} \|= "Out of memory"` qualquer ocorrência | critical |
| SSHBruteForce | `count_over_time({job="auth"} \|= "Failed password" [5m]) > 20` | warning |
| NewsAppPipeline | Sem entries `WriterAgent` em 2h (pipeline parado) | warning |

---

## Observações

- **Grafana na porta 3000 só escuta localhost** (UFW bloqueia externo) — acesse via `ssh -L 3000:localhost:3000 root@IP`
- **Loki retention**: verificar `/etc/loki/config.yml` → `retention_period` — padrão pode ser 168h (7 dias); ajustar se disco crescer muito
- **Armadilha comum**: LogQL `|= "ERROR"` é case-sensitive. Use `|~ "(?i)error"` para case-insensitive
- **Rate limits Loki**: Muitas queries simultâneas → throttle. Preferir Grafana dashboard a curl repetitivo
- **Promtail não relê logs antigos** por padrão — se perder dados, verificar `/var/lib/promtail/positions.yaml` e resetar position do arquivo
- **Alert fatigue**: Não criar alertas sem runbook. Cada alerta deve ter ação clara no CLAUDE.md