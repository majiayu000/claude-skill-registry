---
name: datadog
description: Query logs, metrics, monitors, and dashboards from Datadog. Search logs, check alert status, and investigate incidents.
---

# Datadog Monitoring

This skill provides access to Datadog for monitoring, logging, and alerting via the Datadog API.

## Setup Required

**You need to set up API credentials:**

1. Go to Datadog → Organization Settings → API Keys
2. Create or copy an API Key
3. Go to Organization Settings → Application Keys
4. Create an Application Key

Set these as environment variables (add to your shell profile or .env):
```bash
export DD_API_KEY="your-api-key"
export DD_APP_KEY="your-application-key"
export DD_SITE="us3.datadoghq.com"  # Your Datadog site (from browser history: us3)
```

## When to Use

Use this skill when the user:
- Asks about logs, errors, or application behavior
- Wants to check monitor/alert status
- Needs to investigate an incident
- Asks about metrics or performance
- Mentions "Datadog" or monitoring

## API Endpoints

Base URL: `https://api.$(printenv DD_SITE)/api/v1` or `v2`

### Logs

**Search Logs** (POST /api/v2/logs/events/search):
```bash
curl -s -X POST "https://api.$(printenv DD_SITE)/api/v2/logs/events/search" \
  -H "DD-API-KEY: $(printenv DD_API_KEY)" \
  -H "DD-APPLICATION-KEY: $(printenv DD_APP_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "query": "service:my-service status:error",
      "from": "now-1h",
      "to": "now"
    },
    "sort": "-timestamp",
    "page": {"limit": 50}
  }'
```

Common log query filters:
- `service:name` - Filter by service
- `status:error` - Filter by log level (error, warn, info, debug)
- `@http.status_code:500` - Filter by HTTP status
- `host:hostname` - Filter by host
- `env:production` - Filter by environment

### Monitors (Alerts)

**List All Monitors** (GET /api/v1/monitor):
```bash
curl -s "https://api.$(printenv DD_SITE)/api/v1/monitor" \
  -H "DD-API-KEY: $(printenv DD_API_KEY)" \
  -H "DD-APPLICATION-KEY: $(printenv DD_APP_KEY)"
```

**Get Monitor by ID** (GET /api/v1/monitor/{id}):
```bash
curl -s "https://api.$(printenv DD_SITE)/api/v1/monitor/{MONITOR_ID}" \
  -H "DD-API-KEY: $(printenv DD_API_KEY)" \
  -H "DD-APPLICATION-KEY: $(printenv DD_APP_KEY)"
```

**Search Monitors**:
```bash
curl -s "https://api.$(printenv DD_SITE)/api/v1/monitor?query=status:Alert" \
  -H "DD-API-KEY: $(printenv DD_API_KEY)" \
  -H "DD-APPLICATION-KEY: $(printenv DD_APP_KEY)"
```

### Metrics

**Query Metrics** (GET /api/v1/query):
```bash
curl -s -G "https://api.$(printenv DD_SITE)/api/v1/query" \
  --data-urlencode "query=avg:system.cpu.user{*}" \
  --data-urlencode "from=$(date -v-1H +%s)" \
  --data-urlencode "to=$(date +%s)" \
  -H "DD-API-KEY: $(printenv DD_API_KEY)" \
  -H "DD-APPLICATION-KEY: $(printenv DD_APP_KEY)"
```

**List Available Metrics** (GET /api/v1/metrics):
```bash
curl -s "https://api.$(printenv DD_SITE)/api/v1/metrics?from=$(date -v-1d +%s)" \
  -H "DD-API-KEY: $(printenv DD_API_KEY)" \
  -H "DD-APPLICATION-KEY: $(printenv DD_APP_KEY)"
```

### Events

**Query Events** (GET /api/v1/events):
```bash
curl -s "https://api.$(printenv DD_SITE)/api/v1/events?start=$(date -v-1d +%s)&end=$(date +%s)" \
  -H "DD-API-KEY: $(printenv DD_API_KEY)" \
  -H "DD-APPLICATION-KEY: $(printenv DD_APP_KEY)"
```

### Dashboards

**List Dashboards** (GET /api/v1/dashboard):
```bash
curl -s "https://api.$(printenv DD_SITE)/api/v1/dashboard" \
  -H "DD-API-KEY: $(printenv DD_API_KEY)" \
  -H "DD-APPLICATION-KEY: $(printenv DD_APP_KEY)"
```

### Incidents

**List Incidents** (GET /api/v2/incidents):
```bash
curl -s "https://api.$(printenv DD_SITE)/api/v2/incidents" \
  -H "DD-API-KEY: $(printenv DD_API_KEY)" \
  -H "DD-APPLICATION-KEY: $(printenv DD_APP_KEY)"
```

## Common Workflows

### Check for Recent Errors
```bash
# Search for error logs in the last hour
curl -s -X POST "https://api.$(printenv DD_SITE)/api/v2/logs/events/search" \
  -H "DD-API-KEY: $(printenv DD_API_KEY)" \
  -H "DD-APPLICATION-KEY: $(printenv DD_APP_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "query": "status:error",
      "from": "now-1h",
      "to": "now"
    },
    "page": {"limit": 25}
  }' | jq '.data[] | {timestamp: .attributes.timestamp, message: .attributes.message, service: .attributes.service}'
```

### Check Alert Status
```bash
# List monitors that are currently alerting
curl -s "https://api.$(printenv DD_SITE)/api/v1/monitor?query=status:Alert" \
  -H "DD-API-KEY: $(printenv DD_API_KEY)" \
  -H "DD-APPLICATION-KEY: $(printenv DD_APP_KEY)" | jq '.[] | {name, overall_state, message}'
```

### Investigate a Service
```bash
# Get logs for a specific service
curl -s -X POST "https://api.$(printenv DD_SITE)/api/v2/logs/events/search" \
  -H "DD-API-KEY: $(printenv DD_API_KEY)" \
  -H "DD-APPLICATION-KEY: $(printenv DD_APP_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "query": "service:SERVICE_NAME",
      "from": "now-30m",
      "to": "now"
    },
    "page": {"limit": 100}
  }'
```

## Log Query Syntax

Datadog uses a powerful query syntax for logs:

| Operator | Example | Description |
|----------|---------|-------------|
| AND | `service:api status:error` | Both conditions (implicit) |
| OR | `status:error OR status:warn` | Either condition |
| NOT | `-status:debug` | Exclude matches |
| Wildcard | `service:api-*` | Pattern matching |
| Range | `@duration:>1000` | Numeric comparisons |
| Exists | `@http.url:*` | Field exists |

## Time Ranges

For the `from` and `to` parameters:
- `now` - Current time
- `now-1h` - 1 hour ago
- `now-1d` - 1 day ago
- `now-7d` - 1 week ago
- Unix timestamps (seconds)

## Notes

- Your Datadog site appears to be `us3.datadoghq.com` based on browser history
- API rate limits apply - be mindful of query frequency
- Log queries return max 1000 results per request; use pagination for more
- Use `jq` to parse JSON responses
- Monitor status values: OK, Alert, Warn, No Data
