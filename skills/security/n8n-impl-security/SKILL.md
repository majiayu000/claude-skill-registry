---
name: n8n-impl-security
description: >
  Use when hardening n8n deployments or configuring security settings.
  Prevents credential leaks and unauthorized access by enforcing
  encryption, network isolation, and audit practices. Covers credential
  encryption (N8N_ENCRYPTION_KEY), execution data pruning, CORS, reverse
  proxy setup, SSL/TLS, task runners (N8N_RUNNERS_ENABLED), external
  secrets, security audit endpoint, Docker Secrets (_FILE suffix), and
  environment variable security.
  Keywords: n8n, security, encryption, SSL, reverse proxy, Docker, audit.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n Security Implementation

> Harden n8n v1.x deployments: credential encryption, sandboxed execution, reverse proxy, SSL/TLS, Docker Secrets, audit, and data pruning.

## Quick Reference

### Critical Security Variables

| Variable | Default | MUST Set |
|----------|---------|----------|
| `N8N_ENCRYPTION_KEY` | random | YES - ALWAYS set explicitly and back up |
| `N8N_RUNNERS_ENABLED` | `false` | YES - `true` for sandboxed Code node execution |
| `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS` | `false` | YES - `true` to set 0600 on settings file |
| `NODE_ENV` | — | YES - `production` for production deployments |
| `N8N_PROTOCOL` | `http` | YES - `https` behind reverse proxy |
| `N8N_BLOCK_ENV_ACCESS_IN_NODE` | `false` | YES - `true` to block env access in expressions |

### Security Audit

```bash
# CLI audit
n8n audit

# API audit (returns JSON report)
curl -X POST '<N8N_HOST>:<N8N_PORT>/api/v1/audit' \
  -H 'X-N8N-API-KEY: <key>' \
  -H 'Content-Type: application/json'
```

The audit checks for: abandoned workflows (default 90 days), insecure credential usage, risky node configurations, and workflow vulnerabilities.

---

## Decision Trees

### "How do I secure credentials?"

```
Set N8N_ENCRYPTION_KEY explicitly?
├─ NO → n8n generates random key stored in .n8n/config
│        ├─ DANGER: Lose this file = lose ALL credentials
│        └─ ALWAYS set explicitly in production
└─ YES → Key encrypts all credentials in database
         ├─ Multi-instance? → ALL instances MUST share the SAME key
         ├─ Back up the key? → YES, ALWAYS, separately from database
         └─ Using Docker? → Pass via _FILE suffix for Docker Secrets
```

### "How do I handle sensitive environment variables?"

```
Running in Docker?
├─ YES → Use Docker Secrets with _FILE suffix
│        Example: DB_POSTGRESDB_PASSWORD_FILE=/run/secrets/db_password
│        ├─ NEVER put secrets in docker-compose.yml directly
│        └─ NEVER put secrets in Dockerfiles
└─ NO → Use OS-level secret management
         ├─ NEVER commit .env files to version control
         └─ NEVER log environment variables
```

### "How do I set up SSL/TLS?"

```
Direct SSL on n8n?
├─ YES → Set N8N_SSL_KEY and N8N_SSL_CERT paths
│        └─ Only for simple setups without reverse proxy
└─ NO (recommended) → Use reverse proxy for TLS termination
                       ├─ Traefik → automatic Let's Encrypt
                       ├─ Nginx → manual cert or certbot
                       └─ Caddy → automatic HTTPS
                       Set: N8N_PROTOCOL=https
                       Set: N8N_PROXY_HOPS=1 (or more)
                       Set: WEBHOOK_URL=https://your-domain/
```

### "How do I restrict Code node execution?"

```
Task runners enabled?
├─ NO → Code node runs in main n8n process (UNSAFE)
│       └─ ALWAYS enable: N8N_RUNNERS_ENABLED=true
└─ YES → Code executes in sandboxed runner
         ├─ N8N_RUNNERS_MODE=internal (default, same machine)
         ├─ N8N_RUNNERS_MODE=external (separate process/container)
         ├─ N8N_RUNNERS_TASK_TIMEOUT=300 (5 min default)
         └─ N8N_RUNNERS_MAX_CONCURRENCY=5
```

---

## Patterns

### Pattern 1: Credential Encryption Key Management

**ALWAYS** set `N8N_ENCRYPTION_KEY` explicitly in production.

```bash
# Generate a secure encryption key
openssl rand -hex 32
```

**Rules:**
- ALWAYS back up the encryption key separately from the database
- ALWAYS use the same key across ALL n8n instances (main + workers)
- NEVER change the key after credentials are stored (they become unreadable)
- NEVER commit the key to version control
- NEVER lose this key — there is NO recovery mechanism

### Pattern 2: Docker Secrets (_FILE Suffix)

ALWAYS use the `_FILE` suffix pattern for sensitive values in Docker:

```yaml
# docker-compose.yml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    secrets:
      - n8n_encryption_key
      - db_password
    environment:
      - N8N_ENCRYPTION_KEY_FILE=/run/secrets/n8n_encryption_key
      - DB_POSTGRESDB_PASSWORD_FILE=/run/secrets/db_password

secrets:
  n8n_encryption_key:
    file: ./secrets/encryption_key.txt
  db_password:
    file: ./secrets/db_password.txt
```

**Rules:**
- ALWAYS use `_FILE` suffix instead of inline secrets in compose files
- ALWAYS set file permissions to 0600 on secret files
- NEVER store secret files in version control
- The `_FILE` suffix works on most credential/connection variables

### Pattern 3: Execution Data Pruning

ALWAYS configure execution data pruning to prevent unbounded database growth:

```bash
EXECUTIONS_DATA_PRUNE=true              # Enable auto-pruning (default: true)
EXECUTIONS_DATA_MAX_AGE=336             # Max age in hours (default: 14 days)
EXECUTIONS_DATA_PRUNE_MAX_COUNT=10000   # Max execution count
EXECUTIONS_DATA_HARD_DELETE_BUFFER=1    # Hours before hard deletion
```

**Rules:**
- ALWAYS enable pruning in production (`EXECUTIONS_DATA_PRUNE=true`)
- ALWAYS set `EXECUTIONS_DATA_MAX_AGE` appropriate to your retention needs
- NEVER disable pruning without monitoring database size
- Consider `EXECUTIONS_DATA_SAVE_ON_SUCCESS=none` if you only need error data

### Pattern 4: Task Runners (Sandboxed Execution)

ALWAYS enable task runners for Code node security:

```bash
N8N_RUNNERS_ENABLED=true
N8N_RUNNERS_MODE=internal           # or 'external' for separate process
N8N_RUNNERS_TASK_TIMEOUT=300        # 5 minute timeout
N8N_RUNNERS_MAX_CONCURRENCY=5       # concurrent task limit
```

**Rules:**
- ALWAYS set `N8N_RUNNERS_ENABLED=true` in production
- ALWAYS set a task timeout to prevent runaway code
- NEVER run untrusted code without task runners enabled
- For external mode, ALWAYS set `N8N_RUNNERS_AUTH_TOKEN`

### Pattern 5: Reverse Proxy with TLS

ALWAYS use a reverse proxy for TLS termination in production. See [references/examples.md](references/examples.md) for full Traefik and Nginx configurations.

**Required environment variables behind a reverse proxy:**
```bash
N8N_PROTOCOL=https
N8N_HOST=n8n.example.com
N8N_PROXY_HOPS=1                    # Number of proxies in front of n8n
WEBHOOK_URL=https://n8n.example.com/
N8N_SECURE_COOKIE=true              # HTTPS-only cookies
```

### Pattern 6: File System and Node Restrictions

ALWAYS restrict file and node access in production:

```bash
N8N_BLOCK_ENV_ACCESS_IN_NODE=true           # Block env access in expressions
N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES=true     # Block .n8n directory access
N8N_RESTRICT_FILE_ACCESS_TO=/files          # Limit file access to specific dirs
N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true  # 0600 on settings file
```

**Optional node restrictions:**
```bash
# Exclude dangerous nodes entirely
NODES_EXCLUDE=["n8n-nodes-base.executeCommand","n8n-nodes-base.localFileTrigger"]

# Restrict Code node module access
NODE_FUNCTION_ALLOW_BUILTIN=crypto,path     # Only allow specific builtins
NODE_FUNCTION_ALLOW_EXTERNAL=lodash         # Only allow specific externals
```

---

## Security Hardening Checklist

### MUST (Critical)

- [ ] `N8N_ENCRYPTION_KEY` set explicitly and backed up separately
- [ ] `NODE_ENV=production`
- [ ] `N8N_RUNNERS_ENABLED=true` (sandboxed Code execution)
- [ ] `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true`
- [ ] HTTPS via reverse proxy (Traefik/Nginx/Caddy)
- [ ] `N8N_PROTOCOL=https` and `WEBHOOK_URL` set to HTTPS URL
- [ ] PostgreSQL for production (NOT SQLite)
- [ ] Docker Secrets (`_FILE` suffix) for all sensitive values
- [ ] Execution data pruning enabled
- [ ] Regular backups: database + encryption key

### SHOULD (Recommended)

- [ ] `N8N_BLOCK_ENV_ACCESS_IN_NODE=true`
- [ ] `N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES=true`
- [ ] `N8N_RESTRICT_FILE_ACCESS_TO` set to specific directories
- [ ] `N8N_SECURE_COOKIE=true`
- [ ] `N8N_SAMESITE_COOKIE=strict` (if single-domain)
- [ ] `NODES_EXCLUDE` for unused dangerous nodes
- [ ] `NODE_FUNCTION_ALLOW_BUILTIN` restricted to needed modules
- [ ] `N8N_PUBLIC_API_SWAGGERUI_DISABLED=true` (disable API playground)
- [ ] `N8N_COMMUNITY_PACKAGES_ENABLED=false` (if not needed)
- [ ] `N8N_DIAGNOSTICS_ENABLED=false` (disable telemetry)

### SHOULD (Monitoring)

- [ ] Run `n8n audit` or `POST /audit` regularly
- [ ] `N8N_SECURITY_AUDIT_DAYS_ABANDONED_WORKFLOW=90`
- [ ] Monitor execution data growth
- [ ] Review API key usage and rotate periodically
- [ ] Enable log streaming for real-time monitoring

---

## Anti-Pattern Summary

| Anti-Pattern | Risk | Fix |
|---|---|---|
| No explicit `N8N_ENCRYPTION_KEY` | Lose key = lose ALL credentials | ALWAYS set and back up explicitly |
| Secrets in docker-compose.yml | Secrets in version control | Use Docker Secrets with `_FILE` suffix |
| SQLite in production | No queue mode, no scaling, corruption risk | Use PostgreSQL |
| No task runners | Code node runs in main process | `N8N_RUNNERS_ENABLED=true` |
| HTTP without TLS | Credentials transmitted in cleartext | Reverse proxy with HTTPS |
| No execution pruning | Unbounded database growth | `EXECUTIONS_DATA_PRUNE=true` |
| `NODE_FUNCTION_ALLOW_BUILTIN=*` | Code node can access all Node.js modules | Whitelist specific modules |

See [references/anti-patterns.md](references/anti-patterns.md) for detailed anti-patterns with examples.

---

## Reference Links

- [Security Environment Variables & Methods](references/methods.md)
- [Security Configuration Examples](references/examples.md)
- [Security Anti-Patterns](references/anti-patterns.md)
- [n8n Security Documentation](https://docs.n8n.io/hosting/configuration/environment-variables/)
- [n8n Task Runners](https://docs.n8n.io/hosting/configuration/task-runners/)
- [n8n Docker Deployment](https://docs.n8n.io/hosting/installation/docker/)
