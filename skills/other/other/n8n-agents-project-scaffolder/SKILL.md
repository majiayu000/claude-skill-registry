---
name: n8n-agents-project-scaffolder
description: >
  Use when creating new n8n deployments or scaffolding custom node
  packages from scratch. Prevents misconfiguration by generating
  production-ready project structures. Covers Docker Compose with
  PostgreSQL, environment file templates, custom node package scaffolds
  (n8n-nodes-starter), workflow JSON templates, credential configurations,
  queue mode setup, and backup scripts.
  Keywords: n8n, scaffold, project, Docker, deployment, template.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n Project Scaffolder

> Generate complete, production-ready n8n project structures from scratch.

## Quick Reference

| Scaffold Type | Use Case | Key Files |
|---------------|----------|-----------|
| **Deployment** | New n8n server with PostgreSQL + Traefik | `docker-compose.yml`, `.env`, `backup.sh` |
| **Queue Mode** | Horizontally scaled n8n with Redis workers | `docker-compose.yml`, `.env` |
| **Custom Node** | New community node package | `package.json`, `tsconfig.json`, node + credential templates |
| **Workflow Template** | Starter workflow JSON files | `workflows/*.json` |

## Decision Tree: Which Scaffold?

```
What are you building?
|
+-- A new n8n server deployment?
|   |
|   +-- Single instance (dev/small team)?
|   |   --> DEPLOYMENT SCAFFOLD (PostgreSQL)
|   |
|   +-- High-traffic / horizontal scaling?
|       --> QUEUE MODE SCAFFOLD (PostgreSQL + Redis + Workers)
|
+-- A custom n8n node package?
|   --> CUSTOM NODE SCAFFOLD
|
+-- Starter workflow files?
    --> WORKFLOW TEMPLATE SCAFFOLD
```

## 1. Deployment Scaffold (PostgreSQL + Traefik)

### Generated Structure

```
n8n-deployment/
├── docker-compose.yml       # n8n + PostgreSQL + Traefik
├── .env                     # Environment configuration
├── .env.example             # Template with documentation
├── backup.sh                # Automated backup script
├── restore.sh               # Restore from backup
├── local-files/             # Shared file directory
└── backups/                 # Backup output directory
```

### ALWAYS Include in docker-compose.yml

- PostgreSQL service with named volume (`postgres_data`)
- n8n service with named volume (`n8n_data`) mounted at `/home/node/.n8n`
- Traefik reverse proxy with Let's Encrypt TLS
- Local files bind mount (`./local-files:/files`)
- Explicit `N8N_ENCRYPTION_KEY` (NEVER rely on auto-generated key)
- `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true`
- `N8N_RUNNERS_ENABLED=true`
- `NODE_ENV=production`
- `restart: always` on all services
- PostgreSQL health check with `pg_isready`
- n8n `depends_on` PostgreSQL with `condition: service_healthy`

### ALWAYS Include in .env

```env
# === DOMAIN ===
DOMAIN_NAME=example.com
SUBDOMAIN=n8n
SSL_EMAIL=admin@example.com

# === TIMEZONE ===
GENERIC_TIMEZONE=Europe/Amsterdam
TZ=Europe/Amsterdam

# === DATABASE ===
POSTGRES_USER=n8n
POSTGRES_PASSWORD=CHANGE_ME_STRONG_PASSWORD
POSTGRES_DB=n8n

# === SECURITY (CRITICAL) ===
N8N_ENCRYPTION_KEY=GENERATE_WITH_openssl_rand_hex_32

# === EXECUTION ===
EXECUTIONS_DATA_PRUNE=true
EXECUTIONS_DATA_MAX_AGE=336
EXECUTIONS_DATA_PRUNE_MAX_COUNT=10000
```

### NEVER Do

- NEVER use SQLite for production deployments
- NEVER omit `N8N_ENCRYPTION_KEY` (losing it = losing ALL credential access)
- NEVER expose PostgreSQL port to the internet
- NEVER use default passwords in production

> Full Docker Compose template: [references/methods.md](references/methods.md#deployment-docker-compose-template)

---

## 2. Queue Mode Scaffold (Redis + Workers)

### Generated Structure

```
n8n-queue-deployment/
├── docker-compose.yml       # n8n main + workers + PostgreSQL + Redis
├── .env                     # Shared environment configuration
├── .env.example             # Template with documentation
├── backup.sh                # Automated backup script
└── local-files/             # Shared file directory
```

### ALWAYS Include for Queue Mode

- `EXECUTIONS_MODE=queue` on ALL n8n services (main + workers)
- Redis service with named volume
- Separate `n8n-worker` service using `command: worker`
- Same `N8N_ENCRYPTION_KEY` on ALL instances
- Same n8n Docker image version on ALL instances
- PostgreSQL 13+ (SQLite does NOT support queue mode)
- S3-compatible storage for binary data (`N8N_DEFAULT_BINARY_DATA_MODE=s3`)
- `QUEUE_BULL_REDIS_HOST` pointing to Redis service name
- Worker concurrency setting (`--concurrency=5`)

### NEVER Do in Queue Mode

- NEVER use SQLite (queue mode requires PostgreSQL)
- NEVER use different n8n versions across main and workers
- NEVER use different encryption keys across instances
- NEVER use filesystem binary data mode (use S3 for shared access)

> Full Queue Mode template: [references/methods.md](references/methods.md#queue-mode-docker-compose-template)

---

## 3. Custom Node Scaffold

### Generated Structure

```
n8n-nodes-<your-name>/
├── package.json             # Node registration with n8n block
├── tsconfig.json            # TypeScript configuration
├── .eslintrc.js             # Linting configuration
├── LICENSE                  # MIT license
├── README.md                # Package documentation
├── credentials/
│   └── ExampleApi.credentials.ts
├── nodes/
│   └── ExampleNode/
│       ├── ExampleNode.node.ts
│       └── ExampleNode.node.json
└── icons/
    └── example.svg
```

### ALWAYS Include in package.json

```json
{
  "name": "n8n-nodes-<your-name>",
  "version": "0.1.0",
  "keywords": ["n8n-community-node-package"],
  "n8n": {
    "n8nNodesApiVersion": 1,
    "credentials": ["dist/credentials/ExampleApi.credentials.js"],
    "nodes": ["dist/nodes/ExampleNode/ExampleNode.node.js"]
  },
  "scripts": {
    "build": "n8n-node build",
    "dev": "n8n-node dev",
    "lint": "n8n-node lint",
    "lint:fix": "n8n-node lint --fix"
  },
  "files": ["dist"],
  "devDependencies": {
    "@n8n/node-cli": "*",
    "typescript": "5.9.2"
  },
  "peerDependencies": {
    "n8n-workflow": "*"
  }
}
```

### Critical Rules

- `n8n.nodes` and `n8n.credentials` MUST point to compiled `.js` files in `dist/`
- Package name MUST start with `n8n-nodes-`
- `keywords` MUST include `"n8n-community-node-package"`
- ALWAYS use `n8n-workflow` as a peer dependency (NEVER as a direct dependency)
- ALWAYS use `@n8n/node-cli` as a dev dependency for build tooling
- NEVER modify incoming data from `this.getInputData()` directly; clone first

> Full custom node templates: [references/methods.md](references/methods.md#custom-node-templates)

---

## 4. Workflow Template Scaffold

### Available Templates

| Template | Trigger | Purpose |
|----------|---------|---------|
| **Webhook Workflow** | Webhook node | Receive HTTP requests, process, respond |
| **Scheduled Workflow** | Schedule Trigger | Periodic data processing |
| **Error Handler** | Error Trigger | Centralized error notifications |
| **Sub-Workflow** | Execute Workflow Trigger | Reusable processing module |

### Workflow JSON Structure (ALWAYS Follow)

```json
{
  "name": "Workflow Name",
  "nodes": [
    {
      "id": "unique-uuid",
      "name": "Node Display Name",
      "type": "n8n-nodes-base.nodeType",
      "typeVersion": 1,
      "position": [250, 300],
      "parameters": {}
    }
  ],
  "connections": {
    "Source Node Name": {
      "main": [[{ "node": "Target Node Name", "type": "main", "index": 0 }]]
    }
  },
  "settings": {
    "executionOrder": "v1",
    "saveDataErrorExecution": "all",
    "saveDataSuccessExecution": "all"
  }
}
```

### ALWAYS Include in Workflow Templates

- `"executionOrder": "v1"` in settings
- Error handling via `continueOnFail` or error workflow reference
- Node positions that do not overlap (increment X by 200 per node)
- Unique node names within each workflow

> Full workflow templates: [references/examples.md](references/examples.md)

---

## 5. Environment Template Reference

### Essential Variables (ALWAYS Set in Production)

| Variable | Purpose | Example |
|----------|---------|---------|
| `N8N_ENCRYPTION_KEY` | Credential encryption | `openssl rand -hex 32` |
| `N8N_HOST` | Hostname | `n8n.example.com` |
| `N8N_PORT` | HTTP port | `5678` |
| `N8N_PROTOCOL` | Protocol | `https` |
| `NODE_ENV` | Environment | `production` |
| `WEBHOOK_URL` | Public webhook URL | `https://n8n.example.com/` |
| `DB_TYPE` | Database type | `postgresdb` |
| `GENERIC_TIMEZONE` | Timezone | `Europe/Amsterdam` |
| `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS` | File security | `true` |
| `N8N_RUNNERS_ENABLED` | Task runners | `true` |

### Security Variables (ALWAYS Review)

| Variable | Default | Recommended |
|----------|---------|-------------|
| `N8N_BLOCK_ENV_ACCESS_IN_NODE` | `false` | `true` in shared environments |
| `N8N_SECURE_COOKIE` | `true` | Keep `true` with HTTPS |
| `N8N_COMMUNITY_PACKAGES_ENABLED` | `true` | `false` if not needed |
| `NODES_EXCLUDE` | See docs | Exclude `executeCommand`, `localFileTrigger` |

---

## 6. Backup Script Requirements

### ALWAYS Include in Backup Scripts

- PostgreSQL dump via `pg_dump` (or `docker exec` equivalent)
- Workflow export via `n8n export:workflow --backup`
- Credential export via `n8n export:credentials --backup`
- Timestamped output directories
- Retention policy (delete backups older than N days)
- Encryption key backup reminder/verification

### NEVER Do in Backup Scripts

- NEVER export credentials with `--decrypted` flag in automated scripts
- NEVER store backups without the corresponding `N8N_ENCRYPTION_KEY`
- NEVER skip the PostgreSQL dump (it contains execution history)

> Full backup script template: [references/methods.md](references/methods.md#backup-script-template)

---

## 7. Security Defaults Checklist

ALWAYS apply these security defaults when scaffolding ANY n8n project:

- [ ] Generate `N8N_ENCRYPTION_KEY` with `openssl rand -hex 32`
- [ ] Set `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true`
- [ ] Set `N8N_RUNNERS_ENABLED=true` (sandboxed Code node execution)
- [ ] Set `NODE_ENV=production`
- [ ] Set `N8N_BLOCK_ENV_ACCESS_IN_NODE=true` (shared environments)
- [ ] Exclude dangerous nodes: `NODES_EXCLUDE=["n8n-nodes-base.executeCommand"]`
- [ ] Use HTTPS via reverse proxy (Traefik/nginx/Caddy)
- [ ] Set strong PostgreSQL password
- [ ] Do NOT expose database ports publicly
- [ ] Configure execution data pruning

---

## Reference Links

- [Scaffolding Templates & Methods](references/methods.md)
- [Complete Project Examples](references/examples.md)
- [Anti-Patterns & Common Mistakes](references/anti-patterns.md)
- [n8n Docker Deployment Docs](https://docs.n8n.io/hosting/installation/docker/)
- [n8n Environment Variables](https://docs.n8n.io/hosting/configuration/environment-variables/)
- [n8n Queue Mode Docs](https://docs.n8n.io/hosting/scaling/queue-mode/)
- [n8n Custom Node Starter](https://github.com/n8n-io/n8n-nodes-starter)
