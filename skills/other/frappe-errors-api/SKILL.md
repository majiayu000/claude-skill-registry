---
name: frappe-errors-api
description: >
  Use when debugging or handling API errors in Frappe/ERPNext v14/v15/v16.
  Prevents silent failures and wrong HTTP status codes in REST endpoints.
  Covers 401 Unauthorized (wrong token format, expired OAuth), 403 Forbidden
  (missing @whitelist, allow_guest needed), 404 Not Found (wrong endpoint URL),
  417 Expectation Failed (validation via frappe.throw), 500 Internal Server
  Error, CORS issues, CSRF token missing/invalid, rate limit exceeded (429),
  file upload failures, JSON parse errors in request/response, webhook delivery
  failures, and timeout on long operations.
  Keywords: API error, 401, 403, 404, 417, 429, 500, CSRF, CORS, REST,
  whitelist, webhook, rate limit, file upload, authentication token.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# API Error Handling

For API implementation patterns see `frappe-core-api`. For permission errors see `frappe-errors-permissions`.

---

## HTTP Status Code Map: Error -> Cause -> Fix

| Code | Frappe Exception | When It Happens | Fix |
|------|-----------------|-----------------|-----|
| 200 | — | Success | — |
| 401 | `AuthenticationError` | Bad/expired token, wrong format | Check `Authorization: token key:secret` or `Bearer access_token` |
| 403 | `PermissionError` | Missing `@whitelist`, no role, no `allow_guest` | Add decorator or grant permission |
| 404 | `DoesNotExistError` | Wrong URL, doc not found, typo in endpoint path | Verify `/api/resource/:doctype/:name` or `/api/method/dotted.path` |
| 409 | `DuplicateEntryError` | Unique constraint violated | Check existing records before insert |
| 417 | `ValidationError` | `frappe.throw()` called | Fix validation logic or input data |
| 429 | `RateLimitExceededError` | Too many requests | Respect `Retry-After` header; throttle requests |
| 500 | `Exception` (unhandled) | Unhandled server error | Check Error Log; wrap in try/except |
| 503 | — | Server overloaded / maintenance | Retry with exponential backoff |

---

## Authentication Errors (401)

### Wrong Token Format

```
Error:  HTTP 401 Unauthorized
Cause:  Using "Bearer api_key:api_secret" instead of "token api_key:api_secret"
```

**Frappe uses TWO authentication formats — NEVER mix them:**

| Method | Header Format | When to Use |
|--------|--------------|-------------|
| API Key/Secret | `Authorization: token api_key:api_secret` | Server-to-server, scripts |
| OAuth Bearer | `Authorization: Bearer access_token` | OAuth 2.0 flows |
| Session Cookie | Cookie from `/api/method/login` | Browser-based apps |

```python
# WRONG — Bearer with API key:secret
headers = {"Authorization": f"Bearer {api_key}:{api_secret}"}

# CORRECT — token keyword for API key:secret
headers = {"Authorization": f"token {api_key}:{api_secret}"}

# CORRECT — Bearer for OAuth access tokens only
headers = {"Authorization": f"Bearer {oauth_access_token}"}
```

### Expired OAuth Token

```
Error:  HTTP 401 after token was working
Cause:  OAuth access_token expired
Fix:    Use refresh_token to get new access_token
```

```python
def get_fresh_token(settings):
    """ALWAYS implement token refresh for OAuth integrations."""
    if is_token_expired(settings.token_expiry):
        response = requests.post(f"{settings.base_url}/api/method/frappe.integrations.oauth2.get_token", data={
            "grant_type": "refresh_token",
            "refresh_token": settings.get_password("refresh_token"),
            "client_id": settings.client_id,
        })
        if response.status_code == 200:
            data = response.json()
            settings.access_token = data["access_token"]
            settings.token_expiry = frappe.utils.add_to_date(None, seconds=data["expires_in"])
            settings.save(ignore_permissions=True)
        else:
            frappe.throw(_("OAuth token refresh failed"), exc=frappe.AuthenticationError)
    return settings.access_token
```

---

## Forbidden Errors (403)

### Missing @frappe.whitelist()

```
Error:  HTTP 403 on /api/method/myapp.api.my_function
Cause:  Function exists but lacks @frappe.whitelist() decorator
Fix:    Add decorator — without it, NO external call is allowed
```

```python
# WRONG — Callable internally but returns 403 via REST
def my_function(name):
    return frappe.get_doc("Item", name)

# CORRECT — Exposed to authenticated users
@frappe.whitelist()
def my_function(name):
    return frappe.get_doc("Item", name)

# CORRECT — Exposed to everyone including unauthenticated
@frappe.whitelist(allow_guest=True)
def public_function():
    return {"status": "ok"}
```

### Missing allow_guest for Public Endpoints

```
Error:  HTTP 403 for unauthenticated requests
Cause:  @frappe.whitelist() without allow_guest=True
Fix:    Add allow_guest=True — but ALWAYS validate inputs
```

**NEVER use `allow_guest=True` without input validation** — these endpoints are exposed to the internet.

---

## Not Found Errors (404)

### Common URL Mistakes

| Wrong URL | Correct URL | Issue |
|-----------|-------------|-------|
| `/api/resource/SalesOrder/SO-001` | `/api/resource/Sales Order/SO-001` | Space in DocType name |
| `/api/method/myapp.my_function` | `/api/method/myapp.api.my_function` | Missing module path |
| `/api/resource/sales_order` | `/api/resource/Sales Order` | Wrong case / underscore |
| `/api/v2/document/Item/ITEM-001` [v14] | `/api/resource/Item/ITEM-001` | v2 API only in v15+ |

```python
# ALWAYS URL-encode DocType names with spaces
import urllib.parse
url = f"/api/resource/{urllib.parse.quote('Sales Order')}/{name}"
```

---

## Validation Errors (417)

Every `frappe.throw()` call returns HTTP 417 by default (unless a specific exception class is provided).

```python
# Returns 417 — generic validation error
frappe.throw(_("Amount must be positive"))

# Returns 417 — with explicit ValidationError type
frappe.throw(_("Amount must be positive"), exc=frappe.ValidationError)

# Returns 403 — PermissionError overrides to 403
frappe.throw(_("Access denied"), exc=frappe.PermissionError)

# Returns 404 — DoesNotExistError overrides to 404
frappe.throw(_("Not found"), exc=frappe.DoesNotExistError)
```

**ALWAYS use the specific exception class** so clients can handle error types correctly:
```python
# WRONG — all errors look the same to the client
frappe.throw(_("Customer not found"))  # 417, generic

# CORRECT — client can distinguish 404 from validation error
frappe.throw(_("Customer not found"), exc=frappe.DoesNotExistError)  # 404
```

---

## CSRF Token Errors

```
Error:  HTTP 403 "CSRF token missing or invalid"
Cause:  POST/PUT/DELETE request without X-Frappe-CSRF-Token header
```

**Rules:**
- ALWAYS include `X-Frappe-CSRF-Token` header for session-based (cookie) auth.
- Token-based auth (`Authorization: token ...`) does NOT require CSRF token.
- OAuth Bearer auth does NOT require CSRF token.
- The CSRF token is available in `frappe.csrf_token` in JavaScript or embedded as `window.CSRF_TOKEN`.

```javascript
// Browser-side: ALWAYS include CSRF for session-based requests
fetch("/api/method/myapp.api.update", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "X-Frappe-CSRF-Token": frappe.csrf_token
    },
    body: JSON.stringify({data: "value"})
});
```

---

## CORS Errors

```
Error:  "Access-Control-Allow-Origin" header missing
Cause:  Cross-origin request not configured in site_config.json
```

```json
// site_config.json — NEVER use "*" in production
{
    "allow_cors": "https://your-frontend.example.com"
}
```

**For multiple origins [v15+]:**
```json
{
    "allow_cors": ["https://app1.example.com", "https://app2.example.com"]
}
```

---

## Rate Limit Errors (429)

```
Error:  HTTP 429 Too Many Requests
Cause:  Exceeded rate limit configured in site_config.json or hooks.py
```

```python
# hooks.py — rate limiting on whitelisted methods [v14+]
rate_limit = {"myapp.api.heavy_endpoint": {"limit": 10, "seconds": 60}}
```

**ALWAYS handle 429 in external API calls:**
```python
def call_with_rate_limit(url, data):
    response = requests.post(url, json=data, timeout=30)
    if response.status_code == 429:
        wait = int(response.headers.get("Retry-After", 60))
        time.sleep(min(wait, 120))  # Cap at 2 minutes
        response = requests.post(url, json=data, timeout=30)
    response.raise_for_status()
    return response.json()
```

---

## File Upload Errors

```
Error:  HTTP 500 on /api/method/upload_file
Cause:  Wrong content type, file too large, or missing file field
```

```python
# CORRECT file upload via REST API
import requests

response = requests.post(
    f"{base_url}/api/method/upload_file",
    headers={"Authorization": f"token {api_key}:{api_secret}"},
    files={"file": ("document.pdf", open("document.pdf", "rb"), "application/pdf")},
    data={
        "doctype": "Sales Invoice",
        "docname": "SINV-001",
        "is_private": 1  # 1 = private, 0 = public
    },
    timeout=60  # ALWAYS set timeout for uploads
)
```

**Common upload failures:**
- `Content-Type` must be `multipart/form-data` (set automatically by `files=` param)
- NEVER set `Content-Type: application/json` for file uploads
- Check `max_file_size` in site_config.json (default 10MB)
- [v15+] `allowed_file_extensions` restricts file types

---

## JSON Parse Errors

```
Error:  "Failed to decode JSON" or unexpected behavior
Cause:  API arguments sent as JSON string instead of parsed object
```

```python
@frappe.whitelist()
def update_items(items):
    # ALWAYS handle both string and parsed input
    if isinstance(items, str):
        try:
            items = frappe.parse_json(items)
        except Exception:
            frappe.throw(_("Invalid JSON format"), exc=frappe.ValidationError)

    if not isinstance(items, (list, dict)):
        frappe.throw(_("Expected list or dict"), exc=frappe.ValidationError)
```

---

## Webhook Delivery Failures

```
Error:  Webhook not firing or returning errors
Cause:  Target URL unreachable, wrong format, or timeout
```

**Debug checklist:**
1. Check Error Log for webhook delivery errors
2. Verify target URL is reachable from server
3. Check webhook condition — is it filtering out the event?
4. [v15+] Check Webhook Request Log for delivery status

```python
# Custom webhook with error handling
@frappe.whitelist(allow_guest=True)
def incoming_webhook():
    """Handle incoming webhook with validation."""
    payload = frappe.request.data
    signature = frappe.request.headers.get("X-Webhook-Signature")

    if not verify_signature(payload, signature):
        frappe.local.response["http_status_code"] = 401
        return {"error": "Invalid signature"}

    try:
        data = frappe.parse_json(payload)
    except Exception:
        frappe.local.response["http_status_code"] = 400
        return {"error": "Invalid JSON payload"}

    # ALWAYS return 200 quickly to prevent sender retries
    frappe.enqueue(process_webhook_data, data=data, queue="short")
    return {"status": "accepted"}
```

---

## Timeout on Long Operations

```
Error:  HTTP 504 Gateway Timeout or connection reset
Cause:  Operation takes longer than proxy/server timeout (typically 60s)
```

**Fix: Use background jobs for long operations:**
```python
@frappe.whitelist()
def start_long_operation(filters):
    """NEVER run long operations synchronously in API calls."""
    job_id = frappe.generate_hash(length=10)

    frappe.enqueue(
        "myapp.tasks.run_long_operation",
        queue="long",
        timeout=600,
        job_id=job_id,
        filters=filters
    )

    return {"status": "queued", "job_id": job_id}

@frappe.whitelist()
def check_job_status(job_id):
    """Poll for job completion."""
    from frappe.utils.background_jobs import get_info
    jobs = get_info()
    for job in jobs:
        if job.get("job_id") == job_id:
            return {"status": job.get("status", "unknown")}
    return {"status": "completed"}
```

---

## Server-Side Error Pattern (Standard)

```python
@frappe.whitelist()
def safe_api_endpoint(docname, action):
    """ALWAYS follow: validate -> check permission -> execute -> handle errors."""

    # 1. Validate input
    if not docname:
        frappe.throw(_("Document name required"), exc=frappe.ValidationError)

    # 2. Check existence
    if not frappe.db.exists("My DocType", docname):
        frappe.throw(_("Document not found"), exc=frappe.DoesNotExistError)

    # 3. Check permission
    frappe.has_permission("My DocType", "write", docname, throw=True)

    # 4. Execute with error handling
    try:
        doc = frappe.get_doc("My DocType", docname)
        result = doc.run_method(action)
        return {"status": "success", "data": result}

    except frappe.ValidationError:
        raise  # Let Frappe handle — returns 417
    except frappe.PermissionError:
        raise  # Let Frappe handle — returns 403
    except Exception:
        frappe.log_error(frappe.get_traceback(), f"API Error: {docname}")
        frappe.throw(_("Operation failed. Please try again."))
```

---

## Client-Side Error Handling

```javascript
// ALWAYS handle errors in frappe.call
frappe.call({
    method: "myapp.api.safe_api_endpoint",
    args: {docname: "DOC-001", action: "approve"},
    freeze: true,
    freeze_message: __("Processing..."),
    callback: function(r) {
        if (r.message && r.message.status === "success") {
            frappe.show_alert({message: __("Done"), indicator: "green"});
        }
    },
    error: function(r) {
        // ALWAYS check exc_type for specific handling
        if (r.exc_type === "PermissionError") {
            frappe.msgprint(__("You lack permission for this action."));
        } else if (r.exc_type === "DoesNotExistError") {
            frappe.msgprint(__("Record not found."));
        } else if (!r.status) {
            frappe.msgprint(__("Network error. Check your connection."));
        }
    }
});
```

---

## Critical Rules

### ALWAYS
1. **Use specific exception classes** in `frappe.throw()` — enables correct HTTP status codes
2. **Set timeout on all external requests** — `requests.get(url, timeout=30)`
3. **Validate ALL inputs** before processing — whitelisted methods are callable by any logged-in user
4. **Log errors before throwing** — `frappe.log_error()` then `frappe.throw()`
5. **Handle error callback** in every `frappe.call()` — silent failures confuse users
6. **Use background jobs** for operations exceeding 30 seconds
7. **Return 200 quickly** from incoming webhooks then process asynchronously

### NEVER
1. **Expose internal errors to users** — log traceback, show friendly message
2. **Mix token formats** — `token key:secret` vs `Bearer oauth_token`
3. **Retry 4xx errors** (except 429) — they indicate client bugs, not transient failures
4. **Skip CSRF token** for session-based POST requests — results in 403
5. **Set Content-Type: application/json** for file uploads — must be multipart/form-data
6. **Catch exceptions without logging** — makes production debugging impossible
7. **Hardcode API credentials** — use `settings.get_password("field")` from a DocType

---

## Reference Files

| File | Contents |
|------|----------|
| `references/patterns.md` | Complete whitelisted method, webhook, external API patterns |
| `references/examples.md` | Full working API module, client integration, external API client |
| `references/anti-patterns.md` | 15 common API error handling mistakes |

---

## See Also

- `frappe-core-api` — API implementation patterns
- `frappe-errors-permissions` — Permission error handling (403 deep dive)
- `frappe-syntax-whitelisted` — Whitelisted method syntax
- `frappe-errors-serverscripts` — Server Script error handling
