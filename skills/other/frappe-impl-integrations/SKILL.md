---
name: frappe-impl-integrations
description: >
  Use when implementing OAuth providers, Connected Apps, Webhooks, Payment Gateways, or Data Import/Export in Frappe.
  Prevents authentication failures from wrong OAuth flow, missed webhook deliveries, and data corruption during bulk imports.
  Covers OAuth2 provider/client, Connected App DocType, Webhook DocType, Payment Gateway integration, Data Import, Data Export, frappe.integrations module.
  Keywords: OAuth, Connected App, Webhook, Payment Gateway, Data Import, Data Export, integration, API key, OAuth2, webhook trigger.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Integrations

Step-by-step workflows for OAuth, Webhooks, Payment Gateways, Data Import/Export, and external API calls.

**Version**: v14/v15/v16

---

## Decision Tree: Which Integration Pattern?

```
WHAT ARE YOU INTEGRATING?
│
├─► External service needs to call YOUR Frappe site?
│   ├─► On document events → Webhook (push to external)
│   ├─► External sends data to you → Whitelisted API endpoint
│   └─► External needs user auth → OAuth 2.0 Provider
│
├─► YOUR Frappe site calls an external service?
│   ├─► Needs user-level OAuth consent → Connected App
│   ├─► Server-to-server with API key → make_request / requests
│   └─► Recurring sync → Scheduler + API calls
│
├─► Bulk data in/out?
│   ├─► Import CSV/XLSX → Data Import DocType
│   ├─► Export data → Report Builder / export-csv / API
│   └─► Programmatic bulk → frappe.get_doc().insert()
│
├─► Payment processing?
│   └─► Payment Request + Payment Gateway controller
│
└─► Real-time vs batch?
    ├─► Real-time → Webhook or API endpoint
    ├─► Near real-time → frappe.enqueue() after event
    └─► Batch → Scheduler task (hourly/daily)
```

---

## Workflow 1: OAuth 2.0 — Frappe as Provider

Use when external applications need "Sign in with Frappe" or API access on behalf of users.

### Step 1: Configure OAuth Provider Settings

Navigate to **Setup > Integrations > OAuth Provider Settings**:
- **Force**: ALWAYS asks user for confirmation
- **Auto**: Asks only if no active token exists

### Step 2: Create OAuth Client

Navigate to **Setup > Integrations > OAuth Client**:

| Field | Value |
|-------|-------|
| App Name | External app identifier |
| Scopes | Space-separated (e.g., `openid all`) |
| Redirect URIs | Space-separated callback URLs |
| Default Redirect URI | Primary callback URL |
| Grant Type | `Authorization Code` (RECOMMENDED) or `Implicit` |
| Response Type | `Code` (for Auth Code) or `Token` (for Implicit) |
| Skip Authorization | Check for trusted first-party apps only |

### Step 3: Use the Generated Endpoints

| Endpoint | URL |
|----------|-----|
| Authorize | `/api/method/frappe.integrations.oauth2.authorize` |
| Token | `/api/method/frappe.integrations.oauth2.get_token` |
| Profile | `/api/method/frappe.integrations.oauth2.openid_profile` |

### Step 4: Configure External App

```ini
# Example: Grafana generic_oauth config
client_id = <generated_client_id>
client_secret = <generated_client_secret>
auth_url = https://your-frappe.com/api/method/frappe.integrations.oauth2.authorize
token_url = https://your-frappe.com/api/method/frappe.integrations.oauth2.get_token
api_url = https://your-frappe.com/api/method/frappe.integrations.oauth2.openid_profile
scopes = openid all
```

### Critical Rules

- **NEVER** use `Implicit` grant type for server-side apps — use `Authorization Code`
- **ALWAYS** use HTTPS in production for all OAuth endpoints
- **NEVER** expose `client_secret` in client-side JavaScript

---

## Workflow 2: Connected App — Frappe as OAuth Consumer

Use when your Frappe instance needs to access external services (Google, Microsoft, etc.) on behalf of users.

### Step 1: Create Connected App DocType

| Field | Purpose |
|-------|---------|
| Name | Identifier for the connection |
| OpenID Configuration URL | Auto-fetches endpoints (e.g., `/.well-known/openid-configuration`) |
| Authorization URI | Consent screen URL (auto-filled from OpenID) |
| Token URI | Token exchange URL (auto-filled from OpenID) |
| Redirect URI | Auto-generated — copy this to external provider |
| Client ID | From external provider |
| Client Secret | From external provider |
| Scopes | Permissions needed (e.g., `https://mail.google.com/`) |

### Step 2: Register Redirect URI with Provider

Copy the auto-generated Redirect URI and register it in the external provider's OAuth console.

### Step 3: Add Extra Parameters (if needed)

```
access_type=offline    # Google: enables refresh tokens
prompt=consent         # Google: forces re-consent for refresh token
```

### Step 4: Use in Code

```python
import frappe

connected_app = frappe.get_doc("Connected App", "My Google App")
# Initiates OAuth flow — user clicks "Connect to..." button
# After consent, tokens are stored automatically

# Making authenticated calls:
session = connected_app.get_oauth2_session()
response = session.get("https://www.googleapis.com/gmail/v1/users/me/messages")
```

### Critical Rules

- **ALWAYS** add `access_type=offline` for Google APIs to get refresh tokens
- **NEVER** store tokens manually — Connected App manages token lifecycle
- **ALWAYS** handle `TokenExpiredError` — call `session.refresh_token()` or reconnect

---

## Workflow 3: Webhooks — Push Notifications to External Services

### Step 1: Create Webhook DocType

Navigate to **Integrations > Webhook**:

| Field | Value |
|-------|-------|
| DocType | Target document type |
| Doc Event | `on_update`, `after_insert`, `on_submit`, `on_cancel`, `on_trash` |
| Request URL | External endpoint |
| Request Method | POST (default) |
| Conditions | Optional Jinja filter (e.g., `doc.status == "Approved"`) |
| Enabled | Check to activate |

### Step 2: Configure Headers

Add custom headers for authentication:
```
Authorization: Bearer <api_token>
Content-Type: application/json
```

### Step 3: Configure Data — Choose Format

**Form URL-encoded**: Select specific fields from a table.

**JSON**: Use Jinja templates for structured payloads:
```json
{
  "id": "{{ doc.name }}",
  "total": "{{ doc.grand_total }}",
  "items": {{ doc.items | tojson }},
  "event": "{{ event }}"
}
```

### Step 4: Enable Webhook Secret (HMAC Verification)

Set a **Webhook Secret** — Frappe adds `X-Frappe-Webhook-Signature` header with base64-encoded HMAC-SHA256 hash of the payload.

**Receiver verification (Python example):**

```python
import hmac, hashlib, base64

def verify_webhook(payload_body, secret, signature_header):
    expected = base64.b64encode(
        hmac.new(secret.encode(), payload_body, hashlib.sha256).digest()
    ).decode()
    return hmac.compare_digest(expected, signature_header)
```

### Critical Rules

- **ALWAYS** enable Webhook Secret for production webhooks
- **NEVER** rely on webhooks for guaranteed delivery — implement idempotency on the receiver
- **ALWAYS** use `| tojson` filter for child table data in JSON payloads
- Webhook logs are created for every delivery — check **Webhook Request Log** for debugging

---

## Workflow 4: External API Calls from Frappe

### Using frappe.integrations.utils

```python
from frappe.integrations.utils import make_get_request, make_post_request

# GET request
response = make_get_request(
    "https://api.example.com/data",
    headers={"Authorization": "Bearer token123"}
)

# POST request
response = make_post_request(
    "https://api.example.com/submit",
    data={"key": "value"},
    headers={"Content-Type": "application/json"}
)
```

### Using requests Library Directly

```python
import requests
import frappe

def sync_to_external():
    try:
        response = requests.post(
            "https://api.example.com/endpoint",
            json={"data": "value"},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        frappe.log_error(f"API call failed: {e}", "Integration Error")
        raise
```

### Critical Rules

- **ALWAYS** set a `timeout` on external requests (30s recommended)
- **ALWAYS** wrap external calls in try/except and log errors with `frappe.log_error()`
- **NEVER** call external APIs inside `validate` or `before_save` — use `on_update` + `frappe.enqueue()`
- **ALWAYS** use `frappe.enqueue()` for slow external calls to avoid blocking the web request

---

## Workflow 5: Data Import

### Via UI (Data Import DocType)

1. Navigate to **Home > Data Import > New**
2. Select DocType and Import Type (`Insert` or `Update`)
3. Download template CSV/XLSX
4. Fill in data following the template format
5. Upload and preview
6. Start Import

### CSV Format Rules

```csv
ID,Item Name,Item Group,Stock UOM
,Widget A,Products,Nos
,Widget B,Raw Material,Kg
```

- First row: field labels or API field names
- Leave `ID`/`name` empty for Insert (auto-generated)
- For Update: `ID` column MUST contain existing document names
- Child tables: repeat parent row data, add child fields as extra columns

### Programmatic Import

```python
import frappe
from frappe.core.doctype.data_import.data_import import DataImport

# Create Data Import document
di = frappe.get_doc({
    "doctype": "Data Import",
    "reference_doctype": "Item",
    "import_type": "Insert New Records",
    "import_file": "/path/to/file.csv"
})
di.insert()
di.start_import()
```

### Critical Rules

- **ALWAYS** download and use the template — column order and names must match exactly
- **NEVER** import more than 5,000 rows at once — split into batches
- **ALWAYS** test with 5-10 rows first before bulk import
- **ALWAYS** check Import Log for row-level errors after import completes

---

## Workflow 6: Data Export

### Via Report Builder

1. Open any DocType list view
2. Apply filters
3. Menu > Export (CSV/Excel)

### Via CLI

```bash
bench --site mysite export-csv "Sales Invoice"
bench --site mysite export-doc "Sales Invoice" "INV-001"
bench --site mysite export-json "Sales Invoice" "INV-001"
bench --site mysite export-fixtures --app myapp
```

### Programmatic Export

```python
import frappe

# Export filtered data
data = frappe.get_all("Sales Invoice",
    filters={"status": "Paid", "posting_date": [">", "2024-01-01"]},
    fields=["name", "customer", "grand_total", "posting_date"],
    order_by="posting_date desc",
    limit_page_length=0  # No limit
)

# Convert to CSV
import csv, io
output = io.StringIO()
writer = csv.DictWriter(output, fieldnames=["name", "customer", "grand_total", "posting_date"])
writer.writeheader()
writer.writerows(data)
csv_content = output.getvalue()
```

---

## Workflow 7: Frappe REST API Authentication

### API Key + Secret (Server-to-Server)

```bash
# Generate via User > API Access > Generate Keys
curl -H "Authorization: token api_key:api_secret" \
  https://your-site.com/api/resource/Sales%20Invoice
```

### OAuth Bearer Token

```bash
curl -H "Authorization: Bearer access_token" \
  https://your-site.com/api/resource/Sales%20Invoice
```

### Session-Based (Login)

```bash
# Login first
curl -X POST https://your-site.com/api/method/login \
  -d "usr=user@example.com&pwd=password"
# Subsequent requests use session cookie
```

---

## Integration Patterns: Sync vs Async

| Pattern | When to Use | Implementation |
|---------|-------------|----------------|
| Synchronous | Response needed immediately | Direct API call in controller |
| Async (enqueue) | External call > 5s | `frappe.enqueue("myapp.api.sync_record", doc_name=doc.name)` |
| Webhook | Push on event | Webhook DocType configuration |
| Scheduled sync | Periodic batch | `scheduler_events` in hooks.py |
| Real-time | Live updates | Socket.IO + `frappe.publish_realtime()` |

### Retry Pattern

```python
import frappe
from frappe.utils.background_jobs import get_jobs

def sync_with_retry(doc_name, retry_count=0, max_retries=3):
    try:
        result = call_external_api(doc_name)
        frappe.db.set_value("Sales Invoice", doc_name, "sync_status", "Success")
        frappe.db.commit()
    except Exception as e:
        if retry_count < max_retries:
            frappe.enqueue(
                "myapp.integrations.sync_with_retry",
                doc_name=doc_name,
                retry_count=retry_count + 1,
                queue="short",
                enqueue_after_commit=True
            )
        else:
            frappe.log_error(f"Sync failed after {max_retries} retries: {e}")
            frappe.db.set_value("Sales Invoice", doc_name, "sync_status", "Failed")
            frappe.db.commit()
```

---

## Version Differences

| Feature | V14 | V15 | V16 |
|---------|:---:|:---:|:---:|
| Webhook DocType | Yes | Yes | Yes |
| Connected App | Yes | Yes | Yes |
| OAuth 2.0 Provider | Yes | Yes | Yes |
| Data Import (new UI) | Yes | Yes | Yes |
| Print Designer | No | **Yes** | Yes |
| `make_get_request` | Yes | Yes | Yes |
| Webhook HMAC | Yes | Yes | Yes |

---

## Reference Files

| File | Contents |
|------|----------|
| [workflows.md](references/workflows.md) | Complete integration workflow patterns |
| [examples.md](references/examples.md) | Working code examples for all integration types |
| [anti-patterns.md](references/anti-patterns.md) | Common integration mistakes and fixes |
| [decision-tree.md](references/decision-tree.md) | Extended decision trees for integration choice |
