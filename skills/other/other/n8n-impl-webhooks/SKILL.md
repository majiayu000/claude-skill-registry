---
name: n8n-impl-webhooks
description: >
  Use when configuring webhook endpoints in n8n workflows. Prevents the
  #1 mistake of using test URLs in production (different base paths).
  Covers Webhook node setup, 6 HTTP methods, test vs production URLs,
  4 response modes, 4 auth methods, Respond to Webhook node (8 response
  types including JWT and streaming), dynamic path parameters, binary
  data handling, CORS configuration, IP whitelist, and 16MB payload limit.
  Keywords: n8n, webhook, HTTP, REST, callback, trigger, response mode.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n Webhook Implementation

## Quick Reference

| Aspect | Details |
|--------|---------|
| **Trigger node** | Webhook |
| **HTTP methods** | GET, POST, PUT, PATCH, DELETE, HEAD |
| **Test URL** | `<base>/webhook-test/<path>` |
| **Production URL** | `<base>/webhook/<path>` |
| **Response modes** | 4 (Immediately, Last Node, Respond to Webhook, Streaming) |
| **Auth methods** | 4 (None, Basic Auth, Header Auth, JWT Auth) |
| **Payload limit** | 16MB default (`N8N_PAYLOAD_SIZE_MAX`) |
| **Response node** | Respond to Webhook (8 response types) |

## Critical: Test vs Production URLs

ALWAYS understand the two-URL system before deploying webhooks:

### Test URL
- **Format**: `<base>/webhook-test/<path>`
- **Active when**: Clicking "Listen for Test Event" or running manually in the editor
- **Data display**: Results appear directly in the workflow editor
- **Use for**: Development and testing ONLY
- **Env var**: `N8N_ENDPOINT_WEBHOOK_TEST` (default: `webhook-test`)

### Production URL
- **Format**: `<base>/webhook/<path>`
- **Active when**: Workflow is activated (published)
- **Data display**: Results appear ONLY in the Executions tab
- **Use for**: Live integrations and external services
- **Env var**: `N8N_ENDPOINT_WEBHOOK` (default: `webhook`)

### WEBHOOK_URL Environment Variable

ALWAYS set `WEBHOOK_URL` when n8n is behind a reverse proxy:
```
WEBHOOK_URL=https://n8n.example.com/
```
Without this, n8n generates URLs using its internal hostname, which external services cannot reach.

## Decision Tree: Response Mode

```
Need to respond to the caller?
|
+-- No --> "Immediately" (returns 200 + "Workflow got started")
|
+-- Yes --> Need custom response logic?
    |
    +-- No --> "When Last Node Finishes" (returns last node's data)
    |   |
    |   +-- Response Data options:
    |       - All Entries: array of all items
    |       - First Entry JSON: single JSON object
    |       - First Entry Binary: binary file download
    |       - No Response Body: empty 200
    |
    +-- Yes --> Need streaming?
        |
        +-- Yes --> "Streaming" (real-time data from streaming-capable nodes)
        |
        +-- No --> "Using 'Respond to Webhook' Node"
                   (full control: JSON, text, binary, JWT, redirect, etc.)
```

## Decision Tree: Authentication Method

```
Who calls this webhook?
|
+-- Internal/trusted service --> None (use network-level security instead)
|
+-- External service with API key --> Header Auth
|   (custom header name + value)
|
+-- External service with credentials --> Basic Auth
|   (username + password)
|
+-- Service requiring token validation --> JWT Auth
    (validate incoming JWTs, extract claims)
```

## Webhook Node Configuration

### Path Configuration

The Path field defines the URL endpoint. ALWAYS use lowercase, hyphenated paths:

```
# Static paths
my-webhook
orders/incoming
api/v1/notifications

# Dynamic path parameters (use :param syntax)
orders/:orderId
users/:userId/events
:tenantId/webhooks/:eventType
```

Access dynamic parameters in subsequent nodes:
```javascript
// In expressions
{{ $json.params.orderId }}

// In Code node
const orderId = $input.first().json.params.orderId;
```

### HTTP Method Selection

| Method | Use When |
|--------|----------|
| **POST** | Receiving data submissions, form data, JSON payloads |
| **GET** | Health checks, status queries, simple triggers |
| **PUT** | Full resource updates from external systems |
| **PATCH** | Partial resource updates |
| **DELETE** | Deletion notifications |
| **HEAD** | Availability checks (no body returned) |

ALWAYS use POST for webhooks receiving payload data. NEVER use GET for sensitive data (parameters appear in URL/logs).

### Additional Options

| Option | When to Use |
|--------|-------------|
| **Binary Data** | ALWAYS enable when receiving file uploads |
| **IP Whitelist** | ALWAYS use when caller IPs are known (comma-separated) |
| **CORS** | Set specific domains; use `*` only for public APIs |
| **Ignore Bots** | Enable for public-facing webhooks |
| **Raw Body** | Enable when receiving XML or non-JSON payloads |
| **Response Headers** | Add custom headers (Content-Type, Cache-Control, etc.) |
| **Response Code** | Override default status code (e.g., 201 for created) |

## Respond to Webhook Node

### Setup Requirements

1. Add Webhook node as trigger
2. Set Webhook **Respond** to "Using 'Respond to Webhook' Node"
3. Place Respond to Webhook node AFTER all processing nodes

### Response Types (8 Options)

| Type | Use Case |
|------|----------|
| **All Incoming Items** | Return processed data array |
| **First Incoming Item** | Return single processed item |
| **JSON** | Return custom-crafted JSON response |
| **Text** | Return plain text or HTML |
| **Binary File** | Return file download |
| **JWT Token** | Return signed JWT for authentication flows |
| **Redirect** | Send caller to another URL (302) |
| **No Data** | Acknowledge with empty body |

### Critical Behavior Rules

- The node executes ONCE using the first incoming data item
- NEVER place multiple Respond to Webhook nodes in the same execution path (only the first executes)
- If the node is skipped (via IF/Switch), n8n returns 200 with a standard message
- Pre-execution errors return HTTP 500 automatically
- In non-webhook contexts, the node is silently ignored
- Since v1.103.0: HTML responses are wrapped in `<iframe>` with sandbox (NEVER rely on JS access to parent window)

### Additional Options

| Option | Description |
|--------|-------------|
| **Response Code** | Custom HTTP status code |
| **Response Headers** | Custom headers (e.g., `Content-Type: application/xml`) |
| **Put Response in Field** | Rename the response data field |
| **Enable Streaming** | Enable for streaming-configured triggers |

## Webhook Lifecycle

### Registration and Activation

```
1. Create workflow with Webhook node
2. Configure path, method, auth, response mode
3. Test: Click "Listen for Test Event" --> test URL active
4. Deploy: Activate workflow --> production URL active
5. Deactivate workflow --> production URL stops responding
```

ALWAYS verify webhook registration after activation:
```bash
curl -I https://n8n.example.com/webhook/<path>
# Expected: HTTP 200 (or auth challenge)
# If 404: workflow is not active or path is wrong
```

### Environment Variables for Webhooks

| Variable | Default | Purpose |
|----------|---------|---------|
| `WEBHOOK_URL` | — | Public URL for reverse proxy setups |
| `N8N_ENDPOINT_WEBHOOK` | `webhook` | Production path prefix |
| `N8N_ENDPOINT_WEBHOOK_TEST` | `webhook-test` | Test path prefix |
| `N8N_ENDPOINT_WEBHOOK_WAIT` | `webhook-waiting` | Waiting webhook path prefix |
| `N8N_PAYLOAD_SIZE_MAX` | 16MB | Maximum request payload size |
| `N8N_FORMDATA_FILE_SIZE_MAX` | — | Maximum form data file size |
| `N8N_DISABLE_PRODUCTION_MAIN_PROCESS` | `false` | Offload webhooks to separate process |

## Binary Data via Webhooks

ALWAYS enable the **Binary Data** option when receiving files:

1. Enable "Binary Data" in Webhook node options
2. Files arrive as binary properties on the incoming item
3. Access binary data in subsequent nodes via `$binary`
4. For multipart form data, each file becomes a separate binary property

```javascript
// Access uploaded file in Code node
const fileBuffer = await $input.first().binary.file.data;
const fileName = $input.first().binary.file.fileName;
const mimeType = $input.first().binary.file.mimeType;
```

## CORS Configuration

- Default: `*` (all origins allowed)
- ALWAYS restrict to specific domains in production
- Set via the **CORS** additional option in the Webhook node
- Example: `https://app.example.com,https://admin.example.com`

## IP Whitelist

- Set via the **IP Whitelist** additional option
- Comma-separated list of allowed IP addresses
- Unlisted IPs receive HTTP 403 Forbidden
- ALWAYS use when the calling service has known, static IPs

## Queue Mode Webhook Handling

In queue mode (multi-instance deployments):
- The **main instance** handles all webhook reception
- Workers execute the triggered workflows
- Set `WEBHOOK_URL` to point to the main instance
- For high traffic: use a dedicated webhook processor (`n8n webhook` command)
- Set `N8N_DISABLE_PRODUCTION_MAIN_PROCESS=true` when using a separate webhook processor

## Reference Files

- [methods.md](references/methods.md) — Webhook node options, response modes, auth methods
- [examples.md](references/examples.md) — Webhook configuration examples
- [anti-patterns.md](references/anti-patterns.md) — Common webhook mistakes
