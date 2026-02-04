---
name: xero
description: |
  Xero API integration with managed OAuth. Manage contacts, invoices, payments, accounts, and run financial reports. Use this skill when users want to interact with Xero accounting data.
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
---

# Xero

Access the Xero API with managed OAuth authentication. Manage contacts, invoices, payments, bank transactions, and run financial reports.

## Quick Start

```bash
# List contacts
curl -s -X GET 'https://gateway.maton.ai/xero/api.xro/2.0/Contacts' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

## Base URL

```
https://gateway.maton.ai/xero/{native-api-path}
```

Replace `{native-api-path}` with the actual Xero API endpoint path. The gateway proxies requests to `api.xero.com` and automatically injects your OAuth token and Xero-Tenant-Id header.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer YOUR_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Xero OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
curl -s -X GET 'https://ctrl.maton.ai/connections?app=xero&status=ACTIVE' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### Create Connection

```bash
curl -s -X POST 'https://ctrl.maton.ai/connections' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{"app": "xero"}'
```

### Get Connection

```bash
curl -s -X GET 'https://ctrl.maton.ai/connections/{connection_id}' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response:**
```json
{
  "connection": {
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "xero",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
curl -s -X DELETE 'https://ctrl.maton.ai/connections/{connection_id}' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### Specifying Connection

If you have multiple Xero connections, specify which one to use with the `Maton-Connection` header:

```bash
curl -s -X GET 'https://gateway.maton.ai/xero/api.xro/2.0/Contacts' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Maton-Connection: 21fd90f9-5935-43cd-b6c8-bde9d915ca80'
```

If omitted, the gateway uses the default (oldest) active connection.

## API Reference

### Contacts

#### List Contacts

```bash
GET /xero/api.xro/2.0/Contacts
```

#### Get Contact

```bash
GET /xero/api.xro/2.0/Contacts/{contactId}
```

#### Create Contact

```bash
POST /xero/api.xro/2.0/Contacts
Content-Type: application/json

{
  "Contacts": [{
    "Name": "John Doe",
    "EmailAddress": "john@example.com",
    "Phones": [{"PhoneType": "DEFAULT", "PhoneNumber": "555-1234"}]
  }]
}
```

### Invoices

#### List Invoices

```bash
GET /xero/api.xro/2.0/Invoices
```

#### Create Invoice

```bash
POST /xero/api.xro/2.0/Invoices
Content-Type: application/json

{
  "Invoices": [{
    "Type": "ACCREC",
    "Contact": {"ContactID": "xxx"},
    "LineItems": [{
      "Description": "Service",
      "Quantity": 1,
      "UnitAmount": 100.00,
      "AccountCode": "200"
    }]
  }]
}
```

### Accounts

#### List Accounts

```bash
GET /xero/api.xro/2.0/Accounts
```

### Payments

#### List Payments

```bash
GET /xero/api.xro/2.0/Payments
```

### Bank Transactions

#### List Bank Transactions

```bash
GET /xero/api.xro/2.0/BankTransactions
```

### Reports

#### Profit and Loss

```bash
GET /xero/api.xro/2.0/Reports/ProfitAndLoss?fromDate=2024-01-01&toDate=2024-12-31
```

#### Balance Sheet

```bash
GET /xero/api.xro/2.0/Reports/BalanceSheet?date=2024-12-31
```

#### Trial Balance

```bash
GET /xero/api.xro/2.0/Reports/TrialBalance?date=2024-12-31
```

### Organisation

```bash
GET /xero/api.xro/2.0/Organisation
```

## Invoice Types

- `ACCREC` - Accounts Receivable (sales invoice)
- `ACCPAY` - Accounts Payable (bill)

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/xero/api.xro/2.0/Contacts',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/xero/api.xro/2.0/Contacts',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
```

## Notes

- `Xero-Tenant-Id` header is automatically injected
- Dates are in `YYYY-MM-DD` format
- Multiple records can be created in a single request using arrays
- Use `where` query parameter for filtering

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Xero connection |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from Xero API |

## Resources

- [Xero API Overview](https://developer.xero.com/documentation/api/accounting/overview)
- [Contacts](https://developer.xero.com/documentation/api/accounting/contacts)
- [Invoices](https://developer.xero.com/documentation/api/accounting/invoices)
- [Accounts](https://developer.xero.com/documentation/api/accounting/accounts)
- [Payments](https://developer.xero.com/documentation/api/accounting/payments)
- [Reports](https://developer.xero.com/documentation/api/accounting/reports)
