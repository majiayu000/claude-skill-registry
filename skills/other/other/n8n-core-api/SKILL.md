---
name: n8n-core-api
description: >
  Use when integrating with n8n programmatically, managing workflows via API,
  or building n8n admin tools. Prevents authentication errors and incorrect
  endpoint usage. Covers all REST API endpoints (workflows, executions,
  credentials, users, tags, variables, projects), API key authentication via
  X-N8N-API-KEY header, cursor-based pagination, and API configuration.
  Keywords: n8n, REST API, endpoints, API key, X-N8N-API-KEY, pagination,
  workflows, executions, credentials, admin tools.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n-core-api

## Quick Reference

### API Fundamentals

| Aspect | Value |
|--------|-------|
| Base URL | `<N8N_HOST>:<N8N_PORT>/<N8N_PATH>/api/v1/` |
| Authentication | `X-N8N-API-KEY` header |
| Content-Type | `application/json` |
| Pagination | Cursor-based (`nextCursor` field) |
| Max page size | 250 results |
| Default page size | 100 results |
| API Playground | `<base-url>/api/v1/docs` (Scalar UI) |
| Availability | Requires a paid plan (not available during free trial) |

### Resource Endpoints Overview

| Resource | CRUD | Special Operations |
|----------|------|--------------------|
| Workflows | GET, POST, PUT, DELETE | activate, deactivate, transfer, tags, versions |
| Executions | GET, DELETE | retry, stop, stop-bulk, tags |
| Credentials | GET, POST, PUT, DELETE | transfer, credential-type schema |
| Users | GET | role management |
| Tags | GET, POST, PUT, DELETE | — |
| Variables | GET, POST, PUT, DELETE | — |
| Projects | GET, POST, PUT, DELETE | user management |
| Audit | POST | security audit |
| Source Control | POST | pull from source control |

### Critical Warnings

**NEVER** use offset-based pagination -- n8n uses cursor-based pagination exclusively. ALWAYS use the `nextCursor` value from the response to fetch the next page.

**NEVER** hardcode API keys in source code or commit them to version control. ALWAYS use environment variables or secret management systems to store API keys.

**NEVER** use `limit` values greater than 250 -- the API silently caps at 250 results per page. ALWAYS implement cursor-based pagination for large result sets.

**NEVER** attempt to delete a running execution -- the API returns an error. ALWAYS stop the execution first with `POST /executions/:id/stop`, then delete it.

**NEVER** assume API access is available on free trial instances -- the public REST API requires a paid plan.

---

## Authentication

### API Key Creation

1. Navigate to **Settings > n8n API** in the n8n UI
2. Select **Create API Key**
3. Provide a label and set an expiration period
4. On enterprise plans, select specific scopes for resource access
5. Copy the generated key immediately (it is shown only once)

### Header Format

ALWAYS include the API key in every request:

```
X-N8N-API-KEY: <your-api-key>
```

### Scope System (Enterprise Only)

Non-enterprise API keys grant full access to all account resources. Enterprise instances support scope-based restrictions per key. Scopes follow the pattern `resource:action`:

| Scope Pattern | Example |
|---------------|---------|
| `workflow:list` | List workflows |
| `workflow:create` | Create workflows |
| `workflow:read` | Read single workflow |
| `workflow:update` | Update workflow content |
| `workflow:delete` | Delete workflow |
| `workflow:activate` | Activate workflow |
| `workflow:deactivate` | Deactivate workflow |
| `workflow:move` | Transfer workflow to another project |
| `execution:list` | List executions |
| `execution:read` | Read single execution |
| `execution:delete` | Delete execution |
| `execution:retry` | Retry failed execution |
| `execution:stop` | Stop running execution |
| `credential:list` | List credentials |
| `credential:create` | Create credentials |
| `credential:update` | Update credentials |
| `credential:delete` | Delete credentials |
| `credential:move` | Transfer credentials |

---

## Cursor-Based Pagination

### How It Works

1. First request: specify `limit` (default 100, max 250)
2. Response contains `data` array and `nextCursor` string
3. Pass `nextCursor` as `cursor` parameter in the next request
4. When `nextCursor` is `null` or absent, you have reached the last page

### Pagination Pattern

```
Request 1:  GET /api/v1/workflows?limit=100
Response 1: { "data": [...], "nextCursor": "MTIzNA==" }

Request 2:  GET /api/v1/workflows?limit=100&cursor=MTIzNA==
Response 2: { "data": [...], "nextCursor": "NTY3OA==" }

Request 3:  GET /api/v1/workflows?limit=100&cursor=NTY3OA==
Response 3: { "data": [...], "nextCursor": null }  // Last page
```

ALWAYS check for `nextCursor` being `null` or absent to detect the final page. NEVER assume a fixed number of pages.

---

## Essential Patterns

### Pattern 1: List Active Workflows

```bash
curl -X GET \
  '<BASE_URL>/api/v1/workflows?active=true&limit=100' \
  -H 'accept: application/json' \
  -H 'X-N8N-API-KEY: <your-api-key>'
```

### Pattern 2: Create and Activate a Workflow

1. `POST /api/v1/workflows` with workflow JSON body
2. `POST /api/v1/workflows/:id/activate` to activate

ALWAYS create the workflow first, then activate in a separate call. There is no single-step create-and-activate endpoint.

### Pattern 3: Retry a Failed Execution

```bash
curl -X POST \
  '<BASE_URL>/api/v1/executions/<execution-id>/retry' \
  -H 'accept: application/json' \
  -H 'X-N8N-API-KEY: <your-api-key>'
```

ALWAYS verify the execution status is `error` or `crashed` before retrying. Retrying a successful execution has no effect.

### Pattern 4: Transfer Workflow Between Projects

```bash
curl -X POST \
  '<BASE_URL>/api/v1/workflows/<workflow-id>/transfer' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-N8N-API-KEY: <your-api-key>' \
  -d '{ "destinationProjectId": "<project-id>" }'
```

### Pattern 5: Paginate Through All Executions

```bash
cursor=""
while true; do
  if [ -z "$cursor" ]; then
    response=$(curl -s '<BASE_URL>/api/v1/executions?limit=250' \
      -H 'X-N8N-API-KEY: <key>')
  else
    response=$(curl -s "<BASE_URL>/api/v1/executions?limit=250&cursor=$cursor" \
      -H 'X-N8N-API-KEY: <key>')
  fi
  # Process $response data...
  cursor=$(echo "$response" | jq -r '.nextCursor // empty')
  [ -z "$cursor" ] && break
done
```

---

## API Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `N8N_PUBLIC_API_DISABLED` | `false` | Disable the public API entirely |
| `N8N_PUBLIC_API_ENDPOINT` | `api` | Path prefix for public API endpoints |
| `N8N_PUBLIC_API_SWAGGERUI_DISABLED` | `false` | Disable Scalar UI API playground |

### API Playground

The interactive API documentation (Scalar UI) is available at:

```
<base-url>/api/v1/docs
```

This is available on self-hosted instances by default. Set `N8N_PUBLIC_API_SWAGGERUI_DISABLED=true` to disable it in production.

---

## Decision Trees

### Which Endpoint to Use?

```
Need to manage workflow definitions?
├── List/search workflows → GET /workflows (with query filters)
├── Create new workflow   → POST /workflows
├── Update workflow JSON  → PUT /workflows/:id
├── Delete workflow       → DELETE /workflows/:id
├── Toggle activation     → POST /workflows/:id/activate or /deactivate
└── Move to project       → POST /workflows/:id/transfer

Need to inspect or manage executions?
├── List executions       → GET /executions (filter by status, workflowId)
├── Get execution detail  → GET /executions/:id?includeData=true
├── Retry failed          → POST /executions/:id/retry
├── Stop running          → POST /executions/:id/stop
└── Bulk stop             → POST /executions/stop

Need to manage credentials?
├── List credentials      → GET /credentials
├── Create credential     → POST /credentials
├── Update credential     → PUT /credentials/:id
├── Delete credential     → DELETE /credentials/:id
├── Get type schema       → GET /credential-types/:typeName
└── Move to project       → POST /credentials/:id/transfer

Need organizational resources?
├── Tags                  → /tags (CRUD)
├── Variables             → /variables (CRUD)
├── Projects              → /projects (CRUD + user management)
└── Users                 → /users (list, get, role)
```

### Should You Use the API or the CLI?

```
Running n8n in Docker/remote?
├── YES → Use REST API (only option for remote management)
└── NO (local access to n8n process)
    ├── Need programmatic integration? → REST API
    ├── One-off admin task?            → CLI (n8n export, n8n import)
    └── Backup automation?             → CLI for export, API for monitoring
```

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete endpoint reference with methods, paths, and scopes
- [references/examples.md](references/examples.md) -- curl examples for each major resource type with authentication and pagination
- [references/anti-patterns.md](references/anti-patterns.md) -- Common API usage mistakes and how to avoid them

### Official Sources

- https://docs.n8n.io/api/ -- n8n Public REST API documentation
- https://docs.n8n.io/api/authentication/ -- API authentication guide
- https://docs.n8n.io/api/pagination/ -- Pagination documentation
- https://docs.n8n.io/hosting/configuration/environment-variables/ -- Environment variables reference
