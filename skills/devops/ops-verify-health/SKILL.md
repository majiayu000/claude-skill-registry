---
name: ops-verify-health
description: Health check all services across environments. Checks frontend URLs, backend GraphQL endpoints, and reports response times.
allowed-tools:
  - Bash
  - Read
---

# Ops: Verify Health

Health check all services across environments.

**Argument**: `$ARGUMENTS` — environment(s) to check (default: `all`). Options: `local`, `dev`, `staging`, `production`, `all`

## Discovery

Read these files to build the environment URL table:

1. `e2e/constants.ts` — frontend URLs per environment
2. `.env.localhost`, `.env.development`, `.env.staging`, `.env.production` — `EXPO_PUBLIC_GRAPHQL_BASE_URL` for backend GraphQL URLs

## Health Checks

For each environment, run these checks:

### Frontend Check

```bash
curl -sf -o /dev/null -w "HTTP %{http_code} in %{time_total}s" {frontend_url}
```

Verify the response contains Expo/React markers:
```bash
curl -sf {frontend_url} | head -20
```

### Backend GraphQL Check

```bash
curl -sf {graphql_url} -X POST \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __typename }"}' \
  -w "\nHTTP %{http_code} in %{time_total}s\n"
```

### GraphQL Introspection (detailed check)

```bash
curl -sf {graphql_url} -X POST \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { queryType { name } } }"}' \
  -w "\nHTTP %{http_code} in %{time_total}s\n"
```

## Full Health Check Script

Run all checks for the specified environment(s):

```bash
check_env() {
  local ENV=$1
  local FE_URL=$2
  local BE_URL=$3

  echo "=== $ENV ==="

  # Frontend
  FE_STATUS=$(curl -sf -o /dev/null -w "%{http_code}" --max-time 10 "$FE_URL" 2>/dev/null || echo "000")
  FE_TIME=$(curl -sf -o /dev/null -w "%{time_total}" --max-time 10 "$FE_URL" 2>/dev/null || echo "timeout")
  echo "Frontend: HTTP $FE_STATUS ($FE_TIME s)"

  # Backend
  BE_RESULT=$(curl -sf --max-time 10 "$BE_URL" -X POST \
    -H "Content-Type: application/json" \
    -d '{"query":"{ __typename }"}' \
    -w "\n%{http_code} %{time_total}" 2>/dev/null || echo -e "\n000 timeout")
  BE_STATUS=$(echo "$BE_RESULT" | tail -1 | awk '{print $1}')
  BE_TIME=$(echo "$BE_RESULT" | tail -1 | awk '{print $2}')
  echo "Backend:  HTTP $BE_STATUS ($BE_TIME s)"
  echo ""
}
```

## EAS Update Status

Check the latest OTA updates deployed to each branch:

```bash
eas update:list --branch {env} --limit 3
```

## Output Format

Report results as a table:

| Service | Environment | Status | Response Time | Details |
|---------|-------------|--------|---------------|---------|
| Frontend | dev | UP (200) | 0.45s | HTML contains React root |
| Backend | dev | UP (200) | 0.32s | GraphQL responds `__typename` |

Flag any service with status != 200 or response time > 5s as a concern.
