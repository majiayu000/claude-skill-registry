---
name: log-dive
description: >
  Unified log search across Loki, Elasticsearch, and CloudWatch.
  Natural language queries translated to LogQL, ES DSL, or CloudWatch filter patterns.
  Read-only. Never modifies or deletes logs.
version: 0.1.2
author: Anvil AI
tags: [logs, observability, loki, elasticsearch, cloudwatch, incident-response, sre, discord, discord-v2]
---

# Log Dive — Unified Log Search 🤿

Search logs across **Loki**, **Elasticsearch/OpenSearch**, and **AWS CloudWatch** from a single interface. Ask in plain English; the skill translates to the right query language.

> **⚠️ Sensitive Data Warning:** Logs frequently contain PII, secrets, tokens, passwords, and other sensitive data. Never cache, store, or repeat raw log content beyond the current conversation. Treat all log output as confidential.

## Activation

This skill activates when the user mentions:
- "search logs", "find in logs", "log search", "check the logs"
- "Loki", "LogQL", "logcli"
- "Elasticsearch logs", "Kibana", "OpenSearch"
- "CloudWatch logs", "AWS logs", "log groups"
- "error logs", "find errors", "what happened in [service]"
- "tail logs", "follow logs", "live logs"
- "log backends", "which log sources", "log indices", "log labels"
- Incident triage involving log analysis
- "log-dive" explicitly

## Permissions

```yaml
permissions:
  exec: true          # Required to run backend scripts
  read: true          # Read script files
  write: false        # Never writes files — logs may contain secrets
  network: true       # Queries remote log backends
```

## Example Prompts

1. "Find error logs from the checkout service in the last 30 minutes"
2. "Search for timeout exceptions across all services"
3. "What log backends do I have configured?"
4. "List available log indices in Elasticsearch"
5. "Show me the labels available in Loki"
6. "Tail the payment-service logs"
7. "Find all 5xx errors in CloudWatch for api-gateway"
8. "Correlate errors between user-service and payment-service"
9. "What happened in production between 2pm and 3pm today?"

## Backend Configuration

Each backend uses environment variables. Users may have one, two, or all three configured.

### Loki
| Variable | Required | Description |
|----------|----------|-------------|
| `LOKI_ADDR` | Yes | Loki server URL (e.g., `http://loki.internal:3100`) |
| `LOKI_TOKEN` | No | Bearer token for authentication |
| `LOKI_TENANT_ID` | No | Multi-tenant header (`X-Scope-OrgID`) |

### Elasticsearch / OpenSearch
| Variable | Required | Description |
|----------|----------|-------------|
| `ELASTICSEARCH_URL` | Yes | Base URL (e.g., `https://es.internal:9200`) |
| `ELASTICSEARCH_TOKEN` | No | `Basic <base64>` or `Bearer <token>` for auth |

### AWS CloudWatch Logs
| Variable | Required | Description |
|----------|----------|-------------|
| `AWS_PROFILE` or `AWS_ACCESS_KEY_ID` | Yes | Standard AWS credentials |
| `AWS_REGION` | Yes | AWS region for CloudWatch |

## Agent Workflow

Follow this sequence:

### Step 1: Check Backends

Run the backends check to see what's configured:

```bash
bash <skill_dir>/scripts/log-dive.sh backends
```

Parse the JSON output. If no backends are configured, tell the user which environment variables to set.

### Step 2: Translate the User's Query

This is the critical step. Convert the user's natural language request into the appropriate backend-specific query. Use the query language reference below.

**For ALL backends, pass the query through the dispatcher:**

```bash
# Search across all configured backends
bash <skill_dir>/scripts/log-dive.sh search --query '<QUERY>' [OPTIONS]

# Search a specific backend
bash <skill_dir>/scripts/log-dive.sh search --backend loki --query '{app="checkout"} |= "error"' --since 30m --limit 200

bash <skill_dir>/scripts/log-dive.sh search --backend elasticsearch --query '{"query":{"bool":{"must":[{"match":{"message":"error"}},{"match":{"service":"checkout"}}]}}}' --index 'app-logs-*' --since 30m --limit 200

bash <skill_dir>/scripts/log-dive.sh search --backend cloudwatch --query '"ERROR" "checkout"' --log-group '/ecs/checkout-service' --since 30m --limit 200
```

### Step 3: List Available Targets

Before searching, you may need to discover what's available:

```bash
# Loki: list labels and label values
bash <skill_dir>/scripts/log-dive.sh labels --backend loki
bash <skill_dir>/scripts/log-dive.sh labels --backend loki --label app

# Elasticsearch: list indices
bash <skill_dir>/scripts/log-dive.sh indices --backend elasticsearch

# CloudWatch: list log groups
bash <skill_dir>/scripts/log-dive.sh indices --backend cloudwatch
```

### Step 4: Tail Logs (Live Follow)

```bash
bash <skill_dir>/scripts/log-dive.sh tail --backend loki --query '{app="checkout"}'
bash <skill_dir>/scripts/log-dive.sh tail --backend cloudwatch --log-group '/ecs/checkout-service'
```

Tail runs for a limited time (default 30s) and streams results.

### Step 5: Analyze Results

After receiving log output, you MUST:

1. **Identify unique error types** — group similar errors, count occurrences
2. **Find the root cause** — look for the earliest error, trace dependency chains
3. **Correlate across services** — if errors in service A mention service B, note the dependency
4. **Build a timeline** — order events chronologically
5. **Summarize actionably** — "The checkout service started returning 500s at 14:23 because the database connection pool was exhausted (max 10 connections, 10 in use). The pool exhaustion was triggered by a slow query in the inventory service."

**NEVER dump raw log output to the user.** Always summarize, extract patterns, and present structured findings.

### Discord v2 Delivery Mode (OpenClaw v2026.2.14+)

When the conversation is happening in a Discord channel:

- Send a compact incident summary first (backend, query intent, top error types, root-cause hypothesis), then ask if the user wants full detail.
- Keep the first response under ~1200 characters and avoid dumping raw log lines in the first message.
- If Discord components are available, include quick actions:
  - `Show Error Timeline`
  - `Show Top Error Patterns`
  - `Run Related Service Query`
- If components are not available, provide the same follow-ups as a numbered list.
- Prefer short follow-up chunks (<=15 lines per message) when sharing timelines or grouped findings.

## Query Language Reference

### LogQL (Loki)

LogQL has two parts: a stream selector and a filter pipeline.

**Stream selectors:**
```
{app="myapp"}                          # exact match
{namespace="prod", app=~"api-.*"}      # regex match
{app!="debug"}                         # negative match
```

**Filter pipeline (chained after selector):**
```
{app="myapp"} |= "error"              # line contains "error"
{app="myapp"} != "healthcheck"         # line does NOT contain
{app="myapp"} |~ "error|warn"          # regex match on line
{app="myapp"} !~ "DEBUG|TRACE"         # negative regex
```

**Structured metadata (parsed logs):**
```
{app="myapp"} | json                   # parse JSON logs
{app="myapp"} | json | status >= 500   # filter by parsed field
{app="myapp"} | logfmt                 # parse logfmt
{app="myapp"} | regexp `(?P<ip>\d+\.\d+\.\d+\.\d+)` # regex extract
```

**Common patterns:**
- Errors in service: `{app="checkout"} |= "error" | json | level="error"`
- HTTP 5xx: `{app="api"} | json | status >= 500`
- Slow requests: `{app="api"} | json | duration > 5s`
- Stack traces: `{app="myapp"} |= "Exception" |= "at "`

### Elasticsearch Query DSL

**Simple match:**
```json
{"query": {"match": {"message": "error"}}}
```

**Boolean query (AND/OR):**
```json
{
  "query": {
    "bool": {
      "must": [
        {"match": {"message": "error"}},
        {"match": {"service.name": "checkout"}}
      ],
      "must_not": [
        {"match": {"message": "healthcheck"}}
      ]
    }
  },
  "sort": [{"@timestamp": "desc"}],
  "size": 200
}
```

**Time range filter:**
```json
{
  "query": {
    "bool": {
      "must": [{"match": {"message": "timeout"}}],
      "filter": [
        {"range": {"@timestamp": {"gte": "now-30m", "lte": "now"}}}
      ]
    }
  }
}
```

**Wildcard / regex:**
```json
{"query": {"regexp": {"message": "error.*timeout"}}}
```

**Common patterns:**
- Errors in service: `{"query":{"bool":{"must":[{"match":{"message":"error"}},{"match":{"service.name":"checkout"}}]}}}`
- HTTP 5xx: `{"query":{"range":{"http.status_code":{"gte":500}}}}`
- Aggregate by field: Use `"aggs"` — but prefer simple queries for agent use

### CloudWatch Filter Patterns

**Simple text match:**
```
"ERROR"                              # contains ERROR
"ERROR" "checkout"                   # contains ERROR AND checkout
```

**JSON filter patterns:**
```
{ $.level = "error" }               # JSON field match
{ $.statusCode >= 500 }             # numeric comparison
{ $.duration > 5000 }               # duration threshold
{ $.level = "error" && $.service = "checkout" }  # compound
```

**Negation and wildcards:**
```
?"ERROR" ?"timeout"                  # ERROR OR timeout (any term)
-"healthcheck"                       # does NOT contain (use with other terms)
```

**Common patterns:**
- Errors: `"ERROR"`
- Errors in service: `{ $.level = "error" && $.service = "checkout" }`
- HTTP 5xx: `{ $.statusCode >= 500 }`
- Exceptions: `"Exception" "at "`

## Output Format

When presenting search results, use this structure:

```markdown
## Log Search Results

**Backend:** Loki | **Query:** `{app="checkout"} |= "error"`
**Time range:** Last 30 minutes | **Results:** 47 entries

### Error Summary

| Error Type | Count | First Seen | Last Seen | Service |
|-----------|-------|------------|-----------|---------|
| NullPointerException | 23 | 14:02:31 | 14:28:45 | checkout |
| ConnectionTimeout | 18 | 14:05:12 | 14:29:01 | checkout → db |
| HTTP 503 | 6 | 14:06:00 | 14:27:33 | checkout → payment |

### Root Cause Analysis

1. **14:02:31** — First `NullPointerException` in checkout service...
2. **14:05:12** — Database connection timeouts begin...

### Recommended Actions

- [ ] Check database connection pool settings
- [ ] Review recent deployments to checkout service

---
*Powered by Anvil AI 🤿*
```

## Common Workflows

### Incident Triage
1. Check backends → search for errors in affected service → search upstream/downstream services → correlate → build timeline → recommend actions.

### Performance Investigation
1. Search for slow requests (`duration > 5s`) → identify common patterns → check for database slow queries → check for external service timeouts.

### Deployment Verification
1. Search for errors in the deployed service since deploy time → compare error rate with pre-deploy period → flag new error types.

## Limitations

- **Read-only:** This skill can only search and read logs. It cannot delete, modify, or create log entries.
- **Output size:** Default limit is 200 entries. Log output is pre-filtered to reduce token consumption. For larger investigations, use multiple targeted queries rather than one broad query.
- **Network access:** Log backends must be reachable from the machine running OpenClaw.
- **No streaming aggregation:** For complex aggregations (percentiles, rates), consider using your backend's native UI (Grafana, Kibana, CloudWatch Insights).

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| "No backends configured" | No env vars set | Set `LOKI_ADDR`, `ELASTICSEARCH_URL`, or configure AWS CLI |
| "logcli not found" | logcli not installed | Install from https://grafana.com/docs/loki/latest/tools/logcli/ |
| "aws: command not found" | AWS CLI not installed | Install from https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html |
| "curl: command not found" | curl not installed | `apt install curl` or `brew install curl` |
| "jq: command not found" | jq not installed | `apt install jq` or `brew install jq` |
| "connection refused" | Backend unreachable | Check URL, VPN, firewall rules |
| "401 Unauthorized" | Bad credentials | Check `LOKI_TOKEN`, `ELASTICSEARCH_TOKEN`, or AWS credentials |

---
*Powered by Anvil AI 🤿*
