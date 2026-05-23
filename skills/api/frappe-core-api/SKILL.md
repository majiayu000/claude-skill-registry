---
name: frappe-core-api
description: >
  Use when building ERPNext/Frappe API integrations (v14/v15/v16) including
  REST API, RPC API, authentication, webhooks, and rate limiting. Covers
  external API calls, endpoint design, token/OAuth2/session authentication.
  Keywords: API integration, REST endpoint, webhook, token authentication,
  OAuth, frappe.call, external connection, rate limiting.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe API Patterns

> Deterministic patterns for REST, RPC, and webhook integrations with Frappe.

---

## Decision Tree

```
What do you need?
├── CRUD on documents (external client)
│   ├── v14: REST /api/resource/{doctype}
│   └── v15+: REST /api/v2/document/{doctype} (new) or /api/resource/ (still works)
│
├── Call custom server logic (external client)
│   └── RPC: POST /api/method/{dotted.path.to.function}
│
├── Notify external systems on document events
│   └── Webhooks (configured in UI or via DocType)
│
├── Client-side calls (JavaScript in Frappe desk)
│   ├── frappe.xcall() — async/await (RECOMMENDED)
│   └── frappe.call() — callback/promise pattern
│
└── Authentication method?
    ├── Server-to-server integration → Token Auth (RECOMMENDED)
    ├── Third-party app / mobile → OAuth 2.0
    ├── Browser session (short-lived) → Session/Cookie Auth
    └── Quick scripting / testing → Token Auth
```

---

## Authentication Methods

### Token Auth (RECOMMENDED for integrations)

```python
headers = {
    'Authorization': 'token api_key:api_secret',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}
```

Generate keys: User > Settings > API Access > Generate Keys. ALWAYS store API secret immediately — it is shown only once.

### Basic Auth (alternative token format)

```python
import base64
credentials = base64.b64encode(b'api_key:api_secret').decode()
headers = {'Authorization': f'Basic {credentials}'}
```

### OAuth 2.0 (third-party apps)

```
# Step 1: Authorization redirect
GET /api/method/frappe.integrations.oauth2.authorize
    ?client_id={id}&response_type=code&scope=openid all
    &redirect_uri={uri}&state={random}

# Step 2: Exchange code for token
POST /api/method/frappe.integrations.oauth2.get_token
    grant_type=authorization_code&code={code}
    &redirect_uri={uri}&client_id={id}

# Step 3: Use bearer token
Authorization: Bearer {access_token}

# Refresh token
POST /api/method/frappe.integrations.oauth2.get_token
    grant_type=refresh_token&refresh_token={token}&client_id={id}
```

### Session/Cookie Auth

```python
session = requests.Session()
session.post(url + '/api/method/login', json={'usr': 'email', 'pwd': 'pass'})
# Subsequent requests use session cookie automatically
```

Session cookies expire after ~3 days. NEVER use for long-running integrations.

---

## REST API — Resource CRUD

### Endpoints

| Operation | Method | v14 Endpoint | v15+ v2 Endpoint |
|-----------|--------|--------------|------------------|
| List | GET | `/api/resource/{doctype}` | `/api/v2/document/{doctype}` |
| Create | POST | `/api/resource/{doctype}` | `/api/v2/document/{doctype}` |
| Read | GET | `/api/resource/{doctype}/{name}` | `/api/v2/document/{doctype}/{name}` |
| Update | PUT | `/api/resource/{doctype}/{name}` | PATCH `/api/v2/document/{doctype}/{name}` |
| Delete | DELETE | `/api/resource/{doctype}/{name}` | DELETE `/api/v2/document/{doctype}/{name}` |
| Copy | — | — | GET `/api/v2/document/{doctype}/{name}/copy` [v15+] |
| Doc Method | — | — | POST `/api/v2/document/{doctype}/{name}/method/{method}` [v15+] |

**ALWAYS** include `Accept: application/json` header — without it, Frappe MAY return HTML.

### List Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `fields` | JSON array | Fields to return | `["name"]` |
| `filters` | JSON array | AND conditions | none |
| `or_filters` | JSON array | OR conditions | none |
| `order_by` | string | Sort expression | `modified desc` |
| `limit_start` | int | Pagination offset | `0` |
| `limit_page_length` | int | Page size | `20` |
| `limit` | int | Alias for limit_page_length [v15+] | — |
| `debug` | bool | Show SQL in response | `false` |

### Filter Operators

```python
filters = [["status", "=", "Open"]]
filters = [["amount", ">", 1000]]
filters = [["status", "in", ["Open", "Pending"]]]
filters = [["date", "between", ["2024-01-01", "2024-12-31"]]]
filters = [["reference", "is", "set"]]       # NOT NULL
filters = [["reference", "is", "not set"]]   # IS NULL
filters = [["name", "like", "%INV%"]]
filters = [["status", "not in", ["Cancelled"]]]
```

Full operator list: `=`, `!=`, `>`, `<`, `>=`, `<=`, `like`, `not like`, `in`, `not in`, `is`, `between`.

### Pagination Pattern

```python
import json, requests

def get_all_records(doctype, headers, base_url, page_size=100):
    all_data, offset = [], 0
    while True:
        params = {
            'fields': json.dumps(["name", "modified"]),
            'limit_start': offset,
            'limit_page_length': page_size
        }
        resp = requests.get(f'{base_url}/api/resource/{doctype}',
                            params=params, headers=headers)
        data = resp.json().get('data', [])
        if not data:
            break
        all_data.extend(data)
        if len(data) < page_size:
            break
        offset += page_size
    return all_data
```

### Create with Child Table

```python
requests.post(f'{base_url}/api/resource/Sales Order', json={
    "customer": "CUST-001",
    "items": [
        {"item_code": "ITEM-001", "qty": 5, "rate": 100},
        {"item_code": "ITEM-002", "qty": 2, "rate": 250}
    ]
}, headers=headers)
```

### Update (Partial)

```python
# Only specified fields are changed
requests.put(f'{base_url}/api/resource/Customer/CUST-001',
             json={"customer_group": "Premium"}, headers=headers)
```

### File Upload

```python
requests.post(f'{base_url}/api/method/upload_file',
    files={'file': ('doc.pdf', open('doc.pdf', 'rb'), 'application/pdf')},
    data={'doctype': 'Customer', 'docname': 'CUST-001', 'is_private': 1},
    headers={'Authorization': 'token api_key:api_secret'})
# NOTE: Do NOT set Content-Type header — requests sets multipart boundary automatically
```

---

## RPC API — Custom Methods

### Server-Side Endpoint

```python
@frappe.whitelist()
def get_balance(customer):
    """GET /api/method/myapp.api.get_balance?customer=CUST-001"""
    return frappe.db.get_value("Customer", customer, "outstanding_amount")

@frappe.whitelist(methods=["POST"])
def create_payment(customer, amount):
    """POST /api/method/myapp.api.create_payment"""
    if not frappe.has_permission("Payment Entry", "create"):
        frappe.throw(_("Not permitted"), frappe.PermissionError)
    pe = frappe.new_doc("Payment Entry")
    pe.party_type = "Customer"
    pe.party = customer
    pe.paid_amount = float(amount)
    pe.insert()
    return pe.name

@frappe.whitelist(allow_guest=True)
def public_status():
    """No authentication required."""
    return {"status": "ok"}
```

### Decorator Options

| Option | Effect | Version |
|--------|--------|---------|
| `allow_guest=True` | No authentication needed | All |
| `methods=["POST"]` | Restrict HTTP methods | [v14+] |
| `xss_safe=True` | Skip XSS escaping on response | All |

### Response Structure

```json
// RPC success
{"message": "return_value"}

// REST success
{"data": {...}}

// Error
{"exc_type": "ValidationError", "_server_messages": "[{\"message\": \"...\"}]"}
```

### Client-Side Calls (JavaScript)

```javascript
// RECOMMENDED: async/await with frappe.xcall
const result = await frappe.xcall('myapp.api.get_balance', {
    customer: 'CUST-001'
});

// Alternative: frappe.call with promise
frappe.call({
    method: 'myapp.api.get_balance',
    args: {customer: 'CUST-001'},
    freeze: true,
    freeze_message: __('Loading...')
}).then(r => console.log(r.message));

// Document method (frm.call)
frm.call('get_linked_doc', {throw_if_missing: true})
    .then(r => console.log(r.message));
```

### Standard frappe.client Methods

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `frappe.client.get_value` | POST | Get single field value |
| `frappe.client.get_list` | POST | List with filters |
| `frappe.client.get` | POST | Get full document |
| `frappe.client.insert` | POST | Create document |
| `frappe.client.save` | POST | Update document |
| `frappe.client.delete` | POST | Delete document |
| `frappe.client.submit` | POST | Submit document |
| `frappe.client.cancel` | POST | Cancel document |
| `frappe.client.get_count` | POST | Count documents |

---

## Webhooks

Configure via Webhook DocType in the UI. Events:

| Event | Trigger |
|-------|---------|
| `after_insert` | New document created |
| `on_update` | Every save |
| `on_submit` | After submit (docstatus=1) |
| `on_cancel` | After cancel (docstatus=2) |
| `on_trash` | Before delete |
| `on_update_after_submit` | After amendment |
| `on_change` | On every change |

**Security**: ALWAYS set a Webhook Secret. Frappe adds `X-Frappe-Webhook-Signature` header with base64-encoded HMAC-SHA256 of payload. Verify on receiving end.

**Conditions**: Use Jinja2 — `{{ doc.grand_total > 10000 }}`.

See `references/webhooks-reference.md` for complete handler examples.

---

## HTTP Status Codes

| Code | Meaning | Common Cause |
|------|---------|--------------|
| `200` | Success | — |
| `400` | Bad request | Validation error |
| `401` | Unauthorized | Missing or invalid auth |
| `403` | Forbidden | No permission for operation |
| `404` | Not found | Document does not exist |
| `417` | Expectation failed | Server exception (frappe.throw) |
| `429` | Rate limited | Too many requests |
| `500` | Server error | Unhandled exception |

---

## Critical Rules

1. **ALWAYS** include `Accept: application/json` header in API requests
2. **ALWAYS** add permission checks in `@frappe.whitelist()` methods
3. **ALWAYS** validate and sanitize input in whitelisted methods
4. **ALWAYS** use parameterized queries — NEVER string-interpolate SQL
5. **ALWAYS** use `timeout=30` on external `requests` calls
6. **ALWAYS** store credentials in `frappe.conf` or env vars — NEVER hardcode
7. **ALWAYS** verify webhook signatures with HMAC-SHA256
8. **ALWAYS** paginate list responses — NEVER return unbounded result sets
9. **NEVER** use `allow_guest=True` on state-changing endpoints
10. **NEVER** log credentials or sensitive data
11. **NEVER** use Administrator API keys for integrations — create dedicated API users

---

## Anti-Patterns

| Do NOT | Do Instead |
|--------|------------|
| No permission check in whitelist | `frappe.has_permission()` before action |
| `frappe.db.sql(f"...{user_input}")` | Parameterized `%s` queries |
| `allow_guest=True` + state change | Require authentication |
| Return all records without limit | Paginate with `limit_page_length` |
| Hardcode API credentials | `frappe.conf.get("api_key")` |
| Synchronous heavy processing | `frappe.enqueue()` for long tasks |
| No timeout on external calls | `requests.get(url, timeout=30)` |
| Inconsistent response format | ALWAYS return `{"status": "...", "data": ...}` |

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---------|-----|-----|-----|
| `/api/resource/` (v1) | Yes | Yes | Yes |
| `/api/v2/document/` (v2) | No | Yes | Yes |
| `/api/v2/doctype/{dt}/meta` | No | Yes | Yes |
| `/api/v2/doctype/{dt}/count` | No | Yes | Yes |
| `limit` alias parameter | No | Yes | Yes |
| PKCE for OAuth2 | Limited | Yes | Yes |
| Server Script rate limiting | No | Yes | Yes |
| Doc method via v2 URL | No | Yes | Yes |

---

## Reference Files

| File | Contents |
|------|----------|
| [authentication-methods.md](references/authentication-methods.md) | Token, Session, OAuth2 with code examples |
| [rest-api-reference.md](references/rest-api-reference.md) | Complete REST CRUD with filters and pagination |
| [rpc-api-reference.md](references/rpc-api-reference.md) | Whitelisted methods, frappe.call, frappe.xcall |
| [webhooks-reference.md](references/webhooks-reference.md) | Webhook config, security, handler examples |
| [anti-patterns.md](references/anti-patterns.md) | Common mistakes with fixes |
| [examples.md](references/examples.md) | Python/JS/cURL client implementations |

## Related Skills

- `frappe-core-permissions` — Permission system for API endpoints
- `frappe-core-database` — Database queries behind API methods
- `frappe-syntax-hooks` — Hook configuration for webhooks
- `frappe-syntax-controllers` — Controller methods called via API

---

*Verified against Frappe docs 2026-03-20 | Frappe v14/v15/v16*
