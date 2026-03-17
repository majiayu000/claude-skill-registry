---
name: xero
description: |
  Xero Accounting API integration skill. Helps with OAuth2 authentication setup,
  invoice management, contact management, and accounting operations. Provides
  guidance on rate limits, token refresh, and API best practices.
license: Apache-2.0
---

# Xero API Integration Skill

**Version:** 1.0.0
**Author:** Claude Code
**Purpose:** Integrate with Xero Accounting API for invoice and contact management

## Overview and Purpose

This skill provides comprehensive guidance for integrating with the Xero Accounting API. It helps you:

- Set up OAuth 2.0 authentication with proper scopes
- Manage access tokens and refresh tokens
- Create and manage invoices
- Manage contacts (customers and suppliers)
- Handle rate limits (5,000/day, 10,000/minute)
- Query reports and financial data

**Important:** This skill provides guidance and patterns. Actual API calls require a registered Xero application with valid credentials stored securely (use the 1password-secrets skill).

## Prerequisites

### Required

1. **Xero Developer Account**
   - Sign up at https://developer.xero.com
   - Enable demo company for testing

2. **Registered OAuth 2.0 Application**
   ```
   1. Go to https://developer.xero.com/app/manage
   2. Click "New app"
   3. Choose "Web app" for server-side integration
   4. Configure redirect URI (e.g., http://localhost:3000/callback)
   5. Save Client ID and Client Secret securely
   ```

3. **Secure Credential Storage**
   ```bash
   # Store credentials in 1Password (recommended)
   op item create --category=API_Credential \
     --title="Xero-OAuth" \
     --vault="ProjectSecrets" \
     client_id=<your-client-id> \
     client_secret=<your-client-secret>
   ```

### Environment Template

Create `.env.template` with 1Password references:

```env
# Xero OAuth2 Credentials
XERO_CLIENT_ID=op://ProjectSecrets/Xero-OAuth/client_id
XERO_CLIENT_SECRET=op://ProjectSecrets/Xero-OAuth/client_secret
XERO_REDIRECT_URI=http://localhost:3000/callback

# Token Storage (use secure storage in production)
XERO_ACCESS_TOKEN=op://ProjectSecrets/Xero-Tokens/access_token
XERO_REFRESH_TOKEN=op://ProjectSecrets/Xero-Tokens/refresh_token
XERO_TENANT_ID=op://ProjectSecrets/Xero-Tokens/tenant_id
```

---

## Workflow 1: OAuth 2.0 Setup

**Purpose:** Establish secure authentication with Xero API.

### When to Use

- Initial application setup
- After credential rotation
- When adding new organization connections

### OAuth 2.0 Flow

```
1. User Authorization
   ----------------------
   Redirect user to Xero authorization URL:

   https://login.xero.com/identity/connect/authorize?
     response_type=code&
     client_id=<CLIENT_ID>&
     redirect_uri=<REDIRECT_URI>&
     scope=openid profile email offline_access accounting.transactions accounting.contacts&
     state=<RANDOM_STATE>

2. Authorization Callback
   ----------------------
   User returns with authorization code:
   GET <REDIRECT_URI>?code=<AUTH_CODE>&state=<STATE>

3. Token Exchange
   ----------------------
   POST https://identity.xero.com/connect/token
   Content-Type: application/x-www-form-urlencoded
   Authorization: Basic base64(<CLIENT_ID>:<CLIENT_SECRET>)

   grant_type=authorization_code&
   code=<AUTH_CODE>&
   redirect_uri=<REDIRECT_URI>

4. Response
   ----------------------
   {
     "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6...",
     "expires_in": 1800,
     "token_type": "Bearer",
     "refresh_token": "abc123...",
     "scope": "openid profile email offline_access accounting.transactions"
   }
```

### Scopes Reference

| Scope | Access Level |
|-------|-------------|
| `openid` | OpenID Connect authentication |
| `profile` | User profile information |
| `email` | User email address |
| `offline_access` | Refresh tokens (required for token refresh) |
| `accounting.transactions` | Invoices, bills, bank transactions |
| `accounting.transactions.read` | Read-only transactions |
| `accounting.contacts` | Contacts (customers/suppliers) |
| `accounting.contacts.read` | Read-only contacts |
| `accounting.reports.read` | Financial reports |
| `accounting.settings` | Organization settings |
| `accounting.settings.read` | Read-only settings |
| `accounting.attachments` | File attachments |

### Security Considerations

- Store credentials in 1Password, never in code
- Use HTTPS for all redirect URIs in production
- Validate `state` parameter to prevent CSRF
- Access tokens expire in 30 minutes; implement refresh

---

## Workflow 2: Token Management

**Purpose:** Handle token refresh and storage securely.

### Token Refresh Flow

```
Access tokens expire after 30 minutes.
Refresh before expiry to maintain session.

POST https://identity.xero.com/connect/token
Content-Type: application/x-www-form-urlencoded
Authorization: Basic base64(<CLIENT_ID>:<CLIENT_SECRET>)

grant_type=refresh_token&
refresh_token=<REFRESH_TOKEN>

Response:
{
  "access_token": "new_access_token...",
  "expires_in": 1800,
  "token_type": "Bearer",
  "refresh_token": "new_refresh_token...",
  "scope": "..."
}
```

### Token Storage Pattern

```python
# Python example using 1Password CLI
import subprocess
import json
from datetime import datetime, timedelta

class XeroTokenManager:
    def __init__(self, vault="ProjectSecrets", item="Xero-Tokens"):
        self.vault = vault
        self.item = item
        self._token_expiry = None

    def get_access_token(self):
        """Get current access token, refreshing if needed."""
        if self._is_token_expired():
            self._refresh_token()

        result = subprocess.run(
            ["op", "item", "get", self.item,
             "--vault", self.vault,
             "--fields", "access_token"],
            capture_output=True, text=True
        )
        return result.stdout.strip()

    def _is_token_expired(self):
        """Check if token needs refresh (5 min buffer)."""
        if self._token_expiry is None:
            return True
        return datetime.now() >= self._token_expiry - timedelta(minutes=5)

    def _refresh_token(self):
        """Refresh access token using refresh token."""
        # Implementation: call Xero token endpoint
        # Update tokens in 1Password
        pass
```

### Best Practices

1. **Refresh proactively** - Refresh 5 minutes before expiry
2. **Handle refresh failures** - Implement re-authorization flow
3. **Store securely** - Use 1Password or similar secret manager
4. **Log token events** - Track refresh attempts for debugging

---

## Workflow 3: Invoice Management

**Purpose:** Create, retrieve, and manage invoices.

### When to Use

- Creating sales invoices
- Querying invoice status
- Sending invoices to customers
- Managing invoice payments

### Create Invoice

```
POST https://api.xero.com/api.xro/2.0/Invoices
Authorization: Bearer <ACCESS_TOKEN>
xero-tenant-id: <TENANT_ID>
Content-Type: application/json

{
  "Type": "ACCREC",
  "Contact": {
    "ContactID": "a1b2c3d4-..."
  },
  "LineItems": [
    {
      "Description": "Consulting Services",
      "Quantity": 10,
      "UnitAmount": 150.00,
      "AccountCode": "200"
    }
  ],
  "Date": "2026-01-10",
  "DueDate": "2026-02-10",
  "Reference": "INV-001",
  "Status": "DRAFT"
}
```

### Invoice Types

| Type | Description |
|------|-------------|
| `ACCREC` | Accounts Receivable (Sales Invoice) |
| `ACCPAY` | Accounts Payable (Bill) |

### Invoice Statuses

| Status | Description | Transitions |
|--------|-------------|-------------|
| `DRAFT` | Not yet approved | -> SUBMITTED, AUTHORISED, DELETED |
| `SUBMITTED` | Awaiting approval | -> AUTHORISED, DELETED |
| `AUTHORISED` | Approved, awaiting payment | -> PAID, VOIDED |
| `PAID` | Fully paid | (final state) |
| `VOIDED` | Cancelled | (final state) |
| `DELETED` | Removed | (final state) |

### Bulk Operations

```
Create up to 50 invoices per request (3.5MB max).
Counts as single API call.

POST https://api.xero.com/api.xro/2.0/Invoices
{
  "Invoices": [
    { "Type": "ACCREC", ... },
    { "Type": "ACCREC", ... },
    ...
  ]
}
```

### Query Invoices

```
GET https://api.xero.com/api.xro/2.0/Invoices
Authorization: Bearer <ACCESS_TOKEN>
xero-tenant-id: <TENANT_ID>

Optional parameters:
- where: Filter expression (e.g., Status=="AUTHORISED")
- order: Sort order (e.g., UpdatedDateUTC DESC)
- page: Page number for pagination
- summaryOnly: true for smaller response
```

### Common Patterns

**Get overdue invoices:**
```
GET /Invoices?where=Status=="AUTHORISED"AND AmountDue>0 AND DueDate<DateTime(2026,01,10)
```

**Get recent invoices:**
```
GET /Invoices?where=UpdatedDateUTC>=DateTime(2026,01,01)&order=UpdatedDateUTC DESC
```

---

## Workflow 4: Contact Management

**Purpose:** Manage customers and suppliers.

### When to Use

- Adding new customers
- Updating supplier information
- Syncing contacts from CRM
- Querying contact details

### Create Contact

```
POST https://api.xero.com/api.xro/2.0/Contacts
Authorization: Bearer <ACCESS_TOKEN>
xero-tenant-id: <TENANT_ID>
Content-Type: application/json

{
  "Name": "Acme Corporation",
  "FirstName": "John",
  "LastName": "Smith",
  "EmailAddress": "john.smith@acme.com",
  "Phones": [
    {
      "PhoneType": "DEFAULT",
      "PhoneNumber": "555-1234"
    }
  ],
  "Addresses": [
    {
      "AddressType": "STREET",
      "AddressLine1": "123 Main Street",
      "City": "San Francisco",
      "Region": "CA",
      "PostalCode": "94105",
      "Country": "USA"
    }
  ],
  "IsCustomer": true,
  "IsSupplier": false
}
```

### Query Contacts

```
GET https://api.xero.com/api.xro/2.0/Contacts
Authorization: Bearer <ACCESS_TOKEN>
xero-tenant-id: <TENANT_ID>

Optional parameters:
- where: Filter expression
- order: Sort order
- page: Page number
- summaryOnly: true for smaller response
- includeArchived: true to include archived contacts
```

### Contact Types

| Field | Values | Description |
|-------|--------|-------------|
| `IsCustomer` | true/false | Receives invoices |
| `IsSupplier` | true/false | Sends bills |
| Both can be true | | Contact is both |

---

## Workflow 5: Rate Limit Management

**Purpose:** Stay within API limits and handle throttling gracefully.

### Xero Rate Limits

| Limit Type | Value | Reset |
|------------|-------|-------|
| Daily per organization | 5,000 calls | Midnight UTC |
| Minute per organization | 10,000 calls | Rolling 60 seconds |
| Concurrent connections | 60 | Per integration |

### Response Headers

```
X-Rate-Limit-Problem: daily
Retry-After: 3600

X-MinLimit-Remaining: 9500
X-DayLimit-Remaining: 4800
```

### Implementation Pattern

```python
import time
from functools import wraps

def rate_limit_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        max_retries = 3
        for attempt in range(max_retries):
            response = func(*args, **kwargs)

            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                print(f"Rate limited. Waiting {retry_after}s...")
                time.sleep(retry_after)
                continue

            return response

        raise Exception("Max retries exceeded")
    return wrapper
```

### Best Practices

1. **Monitor limits** - Check X-DayLimit-Remaining header
2. **Use pagination** - Reduce calls with larger page sizes
3. **Batch operations** - Use bulk endpoints when possible
4. **Cache responses** - Store frequently accessed data
5. **Implement backoff** - Exponential backoff for retries

---

## Workflow 6: Multi-Tenant Support

**Purpose:** Handle multiple Xero organizations.

### When to Use

- Accounting firms managing multiple clients
- SaaS platforms with multiple users
- Organizations with multiple entities

### Tenant Discovery

After OAuth, query connected tenants:

```
GET https://api.xero.com/connections
Authorization: Bearer <ACCESS_TOKEN>

Response:
[
  {
    "id": "abc123...",
    "tenantId": "tenant-uuid-1",
    "tenantType": "ORGANISATION",
    "tenantName": "Demo Company (US)"
  },
  {
    "id": "def456...",
    "tenantId": "tenant-uuid-2",
    "tenantType": "ORGANISATION",
    "tenantName": "Client Company Ltd"
  }
]
```

### Making Tenant-Specific Calls

Always include tenant ID header:

```
GET https://api.xero.com/api.xro/2.0/Invoices
Authorization: Bearer <ACCESS_TOKEN>
xero-tenant-id: <TENANT_ID>
```

### Best Practices

1. **Store tenant mappings** - Map users to tenant IDs
2. **Handle disconnections** - Users can revoke access
3. **Per-tenant rate limits** - Limits apply per organization

---

## Workflow 7: Webhooks

**Purpose:** Receive real-time notifications of data changes.

### When to Use

- Real-time invoice status updates
- Contact synchronization
- Payment notifications
- Audit logging

### Webhook Setup

1. Register webhook URL in Xero Developer Portal
2. Verify webhook with intent validation
3. Process events asynchronously

### Webhook Payload

```json
{
  "events": [
    {
      "resourceUrl": "https://api.xero.com/api.xro/2.0/Invoices/abc123",
      "resourceId": "abc123",
      "tenantId": "tenant-uuid",
      "tenantType": "ORGANISATION",
      "eventCategory": "INVOICE",
      "eventType": "UPDATE",
      "eventDateUtc": "2026-01-10T12:00:00Z"
    }
  ],
  "firstEventSequence": 1,
  "lastEventSequence": 1
}
```

### Event Types

| Category | Event Types |
|----------|-------------|
| `INVOICE` | CREATE, UPDATE |
| `CONTACT` | CREATE, UPDATE |
| `PAYMENT` | CREATE, UPDATE |
| `CREDITNOTE` | CREATE, UPDATE |

### Security

1. **Validate signature** - Verify webhook HMAC signature
2. **Respond quickly** - Return 2xx within 5 seconds
3. **Process async** - Queue events for processing
4. **Handle duplicates** - Events may be sent multiple times

---

## Common Patterns

### Pattern 1: Sync Invoices to External System

```python
def sync_invoices_since(last_sync_date):
    """Fetch invoices modified since last sync."""
    page = 1
    while True:
        response = xero_api.get(
            "/Invoices",
            params={
                "where": f"UpdatedDateUTC>=DateTime({last_sync_date})",
                "page": page
            }
        )

        invoices = response.json()["Invoices"]
        if not invoices:
            break

        for invoice in invoices:
            process_invoice(invoice)

        page += 1
```

### Pattern 2: Create Invoice from Order

```python
def create_invoice_from_order(order, contact_id):
    """Convert order to Xero invoice."""
    line_items = [
        {
            "Description": item["name"],
            "Quantity": item["quantity"],
            "UnitAmount": item["price"],
            "AccountCode": "200"  # Sales account
        }
        for item in order["items"]
    ]

    return xero_api.post("/Invoices", json={
        "Type": "ACCREC",
        "Contact": {"ContactID": contact_id},
        "LineItems": line_items,
        "Date": order["date"],
        "DueDate": order["due_date"],
        "Reference": order["reference"],
        "Status": "AUTHORISED"  # Ready for payment
    })
```

### Pattern 3: Find or Create Contact

```python
def find_or_create_contact(email, name):
    """Get existing contact by email or create new."""
    # Search by email
    response = xero_api.get(
        "/Contacts",
        params={"where": f'EmailAddress=="{email}"'}
    )

    contacts = response.json()["Contacts"]
    if contacts:
        return contacts[0]["ContactID"]

    # Create new contact
    response = xero_api.post("/Contacts", json={
        "Name": name,
        "EmailAddress": email,
        "IsCustomer": True
    })

    return response.json()["Contacts"][0]["ContactID"]
```

---

## Troubleshooting

### Issue 1: 401 Unauthorized

**Symptoms:**
```json
{"Type": "OAuth2", "Detail": "The access token has expired"}
```

**Solution:**
- Check token expiry (30 minutes)
- Implement automatic token refresh
- Verify refresh token is still valid

### Issue 2: 403 Forbidden

**Symptoms:**
```json
{"Type": "NoPermissions", "Detail": "You do not have permission"}
```

**Solution:**
- Verify required scopes are requested
- Check user has necessary permissions in Xero
- Re-authorize with correct scopes

### Issue 3: 429 Rate Limited

**Symptoms:**
```
HTTP 429 Too Many Requests
X-Rate-Limit-Problem: daily
```

**Solution:**
- Check X-DayLimit-Remaining header
- Implement exponential backoff
- Use bulk endpoints where possible
- Wait for daily reset at midnight UTC

### Issue 4: Invalid Tenant ID

**Symptoms:**
```json
{"Type": "InvalidTenantId"}
```

**Solution:**
- Query /connections to get valid tenant IDs
- Verify user has access to the organization
- Check for tenant disconnection

### Issue 5: Validation Errors

**Symptoms:**
```json
{
  "Type": "ValidationException",
  "Message": "A validation exception occurred",
  "Elements": [
    {
      "ValidationErrors": [
        {"Message": "Contact Name must be specified"}
      ]
    }
  ]
}
```

**Solution:**
- Check required fields in documentation
- Validate data before API call
- Handle validation errors gracefully

---

## Security Best Practices

1. **Never commit credentials** - Use 1Password templates
2. **Use HTTPS** - All redirect URIs in production
3. **Validate state** - Prevent CSRF in OAuth flow
4. **Limit scopes** - Request only needed permissions
5. **Rotate secrets** - Regular credential rotation
6. **Audit access** - Log API calls and token usage
7. **Handle token revocation** - Users can disconnect

---

## Quick Reference

### API Base URLs

| Environment | URL |
|-------------|-----|
| Production | `https://api.xero.com/api.xro/2.0/` |
| Identity | `https://identity.xero.com/` |
| OAuth | `https://login.xero.com/identity/connect/` |

### Required Headers

```
Authorization: Bearer <ACCESS_TOKEN>
xero-tenant-id: <TENANT_ID>
Content-Type: application/json
Accept: application/json
```

### Common Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized (token expired) |
| 403 | Forbidden (insufficient scope) |
| 404 | Not Found |
| 429 | Rate Limited |
| 500 | Server Error |

---

## Related Skills

- **1password-secrets**: Secure credential storage
- **devops**: CI/CD integration with Xero

---

## References

- [Xero Developer Portal](https://developer.xero.com/)
- [OAuth 2.0 Overview](https://developer.xero.com/documentation/guides/oauth2/overview/)
- [API Scopes](https://developer.xero.com/documentation/guides/oauth2/scopes/)
- [Invoices API](https://developer.xero.com/documentation/api/accounting/invoices)
- [Contacts API](https://developer.xero.com/documentation/api/accounting/contacts)
- [Rate Limits](https://developer.xero.com/documentation/guides/oauth2/limits/)

---

**Version History:**
- 1.0.0 (2026-01-10): Initial release with OAuth2, invoices, contacts workflows

**Maintainer:** Claude Code
**License:** Apache-2.0
