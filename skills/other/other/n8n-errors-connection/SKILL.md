---
name: n8n-errors-connection
description: >
  Use when troubleshooting API connection failures, credential errors,
  or timeout issues in n8n. Prevents misdiagnosis by providing
  deterministic symptom-cause-fix tables. Covers API failures, credential
  errors, timeout configuration, SSL/TLS issues, webhook URL problems
  (test vs production), rate limiting, queue mode connection issues
  (Redis), database connection failures, and retry strategies.
  Keywords: n8n, connection, API, timeout, SSL, credential, Redis.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n Connection Error Diagnosis & Resolution

> Deterministic diagnostic guide for all n8n v1.x connection failures.
> Format: Symptom -> Cause -> Fix. ALWAYS follow the diagnostic tables.

## Quick Reference: Connection Error Categories

| Category | Common Symptom | Go To |
|----------|---------------|-------|
| API connection | HTTP 4xx/5xx, ECONNREFUSED, ETIMEDOUT | [API Failures](#api-connection-failures) |
| Credentials | 401 Unauthorized, 403 Forbidden | [Credential Errors](#credential-errors) |
| Timeouts | ETIMEDOUT, ESOCKETTIMEDOUT, execution hangs | [Timeout Configuration](#timeout-configuration) |
| SSL/TLS | UNABLE_TO_VERIFY_LEAF_SIGNATURE, CERT_HAS_EXPIRED | [SSL/TLS Errors](#ssltls-errors) |
| Webhooks | Webhook not triggering, 404 on webhook URL | [Webhook URL Issues](#webhook-url-issues) |
| Rate limiting | 429 Too Many Requests | [Rate Limiting](#rate-limiting) |
| Queue mode | Redis ECONNREFUSED, worker not picking up jobs | [Queue Mode (Redis)](#queue-mode-redis-connection) |
| Database | ECONNREFUSED on 5432, SQLite SQLITE_BUSY | [Database Errors](#database-connection-errors) |

---

## API Connection Failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ECONNREFUSED` | Target service is down or wrong host/port | ALWAYS verify the service is running and the URL is correct. Check `host:port` in credential or node config. |
| `ENOTFOUND` (DNS) | Hostname cannot be resolved | ALWAYS check for typos in the URL. Verify DNS resolution from the n8n host with `nslookup` or `dig`. |
| `ETIMEDOUT` | Network unreachable or firewall blocking | ALWAYS check firewall rules, security groups, and network connectivity from the n8n container/host. |
| HTTP 500 | Remote server internal error | NEVER assume this is an n8n issue. Check the target API's status page and logs. Retry after delay. |
| HTTP 502/503 | Upstream service unavailable | Check if the target service is overloaded or restarting. Use retry-on-fail configuration. |
| `ECONNRESET` | Connection dropped mid-request | Typically a network instability issue. Enable retry-on-fail on the node. |
| Proxy errors | Corporate proxy blocking requests | Set `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` environment variables. See [references/methods.md](references/methods.md). |

---

## Credential Errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| 401 Unauthorized | Invalid API key, expired token, wrong credentials | ALWAYS verify credentials in n8n Settings > Credentials. Re-enter the API key or regenerate it. |
| 403 Forbidden | Credentials valid but insufficient permissions | Check API key scopes/permissions on the target service. NEVER assume n8n grants permissions. |
| "Credential not found" | Credential deleted or not shared with workflow owner | Re-create the credential or share it with the correct project/user. |
| OAuth2 token expired | Refresh token flow failed | ALWAYS click "Reconnect" in the credential settings to re-authorize. Check if the OAuth app is still active. |
| Wrong credential type selected | Node expects different credential type | ALWAYS match the credential type to the node. Example: "Header Auth" for API key in header, "OAuth2" for OAuth flows. |
| `N8N_ENCRYPTION_KEY` mismatch | Credentials encrypted with different key | ALWAYS ensure `N8N_ENCRYPTION_KEY` is identical across all instances. Credentials are NOT recoverable with wrong key. |

---

## Timeout Configuration

Three timeout levels exist in n8n. ALWAYS configure from specific to general.

### Level 1: Node-Level (Retry on Fail)

Configure in each node's **Settings** tab:

| Setting | Default | Description |
|---------|---------|-------------|
| Retry On Fail | `false` | Enable automatic retries |
| Max Tries | `3` | Number of retry attempts |
| Wait Between Tries (ms) | `1000` | Delay between retries |

### Level 2: Workflow-Level

Set in **Workflow Settings** for per-workflow timeout.

### Level 3: Instance-Level

| Variable | Default | Description |
|----------|---------|-------------|
| `EXECUTIONS_TIMEOUT` | `-1` (disabled) | Default timeout for all workflows (seconds) |
| `EXECUTIONS_TIMEOUT_MAX` | `3600` | Maximum timeout users can set (seconds) |
| `N8N_AI_TIMEOUT_MAX` | `3600000` | AI/LLM node HTTP timeout (ms) |

ALWAYS set `EXECUTIONS_TIMEOUT` in production to prevent runaway workflows.
NEVER leave `EXECUTIONS_TIMEOUT` at `-1` in production environments.

---

## SSL/TLS Errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| `UNABLE_TO_VERIFY_LEAF_SIGNATURE` | Self-signed certificate on target | Set `NODE_TLS_REJECT_UNAUTHORIZED=0` (dev only). For production: add CA cert to Node.js trust store. |
| `CERT_HAS_EXPIRED` | Target's SSL certificate expired | Contact the target service owner. NEVER disable TLS verification in production. |
| `DEPTH_ZERO_SELF_SIGNED_CERT` | Self-signed cert without CA chain | Add the self-signed cert to `NODE_EXTRA_CA_CERTS` environment variable. |
| `ERR_TLS_CERT_ALTNAME_INVALID` | Certificate hostname mismatch | Verify the URL matches the certificate's Common Name or SAN entries. |
| PostgreSQL SSL errors | `DB_POSTGRESDB_SSL_ENABLED=false` or wrong certs | Set `DB_POSTGRESDB_SSL_ENABLED=true`, provide `DB_POSTGRESDB_SSL_CA`, `DB_POSTGRESDB_SSL_CERT`, `DB_POSTGRESDB_SSL_KEY`. |

NEVER set `NODE_TLS_REJECT_UNAUTHORIZED=0` in production. This disables ALL certificate validation.

---

## Webhook URL Issues

> CRITICAL: This is the #1 source of webhook confusion in n8n.

### Test vs Production URL Decision Tree

```
Is the workflow ACTIVE (published)?
├── YES → Use PRODUCTION URL: <base>/webhook/<path>
│         Webhook triggers automatically on incoming requests
└── NO  → Use TEST URL: <base>/webhook-test/<path>
          MUST click "Listen for Test Event" in editor first
```

| Symptom | Cause | Fix |
|---------|-------|-----|
| Webhook works in editor but not when deployed | Using test URL (`/webhook-test/`) in external service | ALWAYS switch to production URL (`/webhook/`) AND activate the workflow. |
| 404 on webhook URL | Workflow not active, or wrong URL path | ALWAYS verify: (1) workflow is active, (2) URL uses `/webhook/` not `/webhook-test/`, (3) path matches node config. |
| Webhook returns empty response | Response mode set to "Immediately" | Change to "When Last Node Finishes" or use "Respond to Webhook" node. |
| Webhook not accessible externally | `WEBHOOK_URL` not set or wrong | ALWAYS set `WEBHOOK_URL` to the full public URL including protocol. Example: `WEBHOOK_URL=https://n8n.example.com/`. |
| Wrong webhook domain in UI | `WEBHOOK_URL` misconfigured | ALWAYS set `WEBHOOK_URL` to match the public-facing URL of your reverse proxy. |
| Webhook payload too large | Exceeds 16MB default limit | Set `N8N_PAYLOAD_SIZE_MAX` to a higher value. |

### WEBHOOK_URL Environment Variable

ALWAYS set `WEBHOOK_URL` when n8n is behind a reverse proxy:
```
WEBHOOK_URL=https://n8n.example.com/
```

NEVER omit `WEBHOOK_URL` in production — n8n will generate localhost URLs that external services cannot reach.

---

## Rate Limiting

| Symptom | Cause | Fix |
|---------|-------|-----|
| HTTP 429 Too Many Requests | API rate limit exceeded | Enable **Retry On Fail** with increasing wait times. Use the **Wait** node for explicit delays. |
| Batch operations hitting limits | Too many items processed simultaneously | Use the **Split In Batches** node. ALWAYS set batch size below the API's rate limit. |
| OAuth rate limits | Too many token refresh requests | Cache tokens and check expiry before refreshing. |

### Backoff Strategy

ALWAYS configure retry with exponential-style backoff for rate-limited APIs:

1. Set **Retry On Fail** = `true` on the HTTP Request node
2. Set **Max Tries** = `3` (or higher for aggressive rate limiters)
3. Set **Wait Between Tries** = `2000` ms (minimum for most APIs)
4. For additional control, use **Split In Batches** with a **Wait** node between batches

---

## Queue Mode (Redis) Connection

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ECONNREFUSED` on Redis port (6379) | Redis not running or wrong host | ALWAYS verify Redis is running: `redis-cli ping` must return `PONG`. Check `QUEUE_BULL_REDIS_HOST` and `QUEUE_BULL_REDIS_PORT`. |
| Workers not picking up jobs | Workers not connected to same Redis/DB | ALWAYS ensure ALL instances share identical `QUEUE_BULL_REDIS_*` variables and `N8N_ENCRYPTION_KEY`. |
| Redis AUTH failed | Wrong Redis password | Verify `QUEUE_BULL_REDIS_PASSWORD` matches Redis `requirepass` configuration. |
| Redis timeout | Network latency or Redis overloaded | Increase `QUEUE_BULL_REDIS_TIMEOUT_THRESHOLD` (default: 10000ms). Check Redis memory usage. |
| Executions stuck in "waiting" | Worker crashed or lost connection | Restart workers. Check worker logs for connection errors. Verify `EXECUTIONS_MODE=queue` on workers. |

### Queue Mode Requirements Checklist

ALWAYS verify ALL of these before enabling queue mode:

- [ ] `EXECUTIONS_MODE=queue` on ALL instances
- [ ] PostgreSQL database (NEVER SQLite with queue mode)
- [ ] Redis running and accessible from all instances
- [ ] Same `N8N_ENCRYPTION_KEY` on ALL instances
- [ ] Same n8n version on ALL instances
- [ ] `WEBHOOK_URL` set on main instance
- [ ] S3-compatible storage configured for binary data

---

## Database Connection Errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| PostgreSQL `ECONNREFUSED` | Database not running or wrong host/port | Verify PostgreSQL is running. Check `DB_POSTGRESDB_HOST` and `DB_POSTGRESDB_PORT`. |
| `password authentication failed` | Wrong database password | Verify `DB_POSTGRESDB_PASSWORD`. Use `_FILE` suffix for Docker Secrets. |
| `database "n8n" does not exist` | Database not created | Create the database: `CREATE DATABASE n8n;` |
| `SQLITE_BUSY` | Concurrent writes to SQLite | NEVER use SQLite in production with multiple connections. Switch to PostgreSQL. |
| `SQLITE_CORRUPT` | Database file corrupted | Restore from backup. Run `DB_SQLITE_VACUUM_ON_STARTUP=true` after restore. |
| Connection pool exhaustion | Too many concurrent connections | Increase `DB_POSTGRESDB_POOL_SIZE` (default: 2). Monitor with `pg_stat_activity`. |
| Connection timeout | Slow network or overloaded DB | Increase `DB_POSTGRESDB_CONNECTION_TIMEOUT` (default: 20000ms). |
| Idle connections dropped | Firewall/NAT killing idle connections | Decrease `DB_POSTGRESDB_IDLE_CONNECTION_TIMEOUT` (default: 30000ms) or configure `DB_PING_INTERVAL_SECONDS`. |

---

## Diagnostic Flowchart

```
Connection error occurred
│
├── Is it an HTTP status code?
│   ├── 401/403 → Credential Errors table
│   ├── 404 on webhook → Webhook URL Issues table
│   ├── 429 → Rate Limiting table
│   └── 500/502/503 → API Connection Failures table
│
├── Is it a Node.js error code?
│   ├── ECONNREFUSED → Check target service is running
│   ├── ENOTFOUND → DNS resolution issue
│   ├── ETIMEDOUT → Firewall or network issue
│   ├── ECONNRESET → Network instability, enable retries
│   └── TLS/SSL errors → SSL/TLS Errors table
│
├── Is it a database error?
│   ├── PostgreSQL → Database Connection Errors table
│   └── SQLite → Switch to PostgreSQL for production
│
└── Is it a queue/Redis error?
    └── Queue Mode (Redis) Connection table
```

## Reference Files

- [references/methods.md](references/methods.md) — Connection error types, retry configuration, timeout settings
- [references/examples.md](references/examples.md) — Connection error scenarios with step-by-step fixes
- [references/anti-patterns.md](references/anti-patterns.md) — Connection handling mistakes to avoid
