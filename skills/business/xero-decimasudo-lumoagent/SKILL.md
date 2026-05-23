---
name: xero
description: Manage Xero accounting - invoices, contacts, bank transactions, and reports via Xero API.
metadata: {"clawdbot":{"emoji":"💵","requires":{"env":["XERO_ACCESS_TOKEN","XERO_TENANT_ID"]}}}
---

# Xero

Cloud accounting platform.

## Environment

```bash
export XERO_ACCESS_TOKEN="xxxxxxxxxx"
export XERO_TENANT_ID="xxxxxxxxxx"
```

## List Contacts

```bash
curl "https://api.xero.com/api.xro/2.0/Contacts" \
  -H "Authorization: Bearer $XERO_ACCESS_TOKEN" \
  -H "Xero-Tenant-Id: $XERO_TENANT_ID" \
  -H "Accept: application/json"
```

## Create Invoice

```bash
curl -X POST "https://api.xero.com/api.xro/2.0/Invoices" \
  -H "Authorization: Bearer $XERO_ACCESS_TOKEN" \
  -H "Xero-Tenant-Id: $XERO_TENANT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "Invoices": [{
      "Type": "ACCREC",
      "Contact": {"ContactID": "xxxxx"},
      "LineItems": [{"Description": "Consulting", "Quantity": 1, "UnitAmount": 500}],
      "Date": "2024-01-30",
      "DueDate": "2024-02-28"
    }]
  }'
```

## List Invoices

```bash
curl "https://api.xero.com/api.xro/2.0/Invoices" \
  -H "Authorization: Bearer $XERO_ACCESS_TOKEN" \
  -H "Xero-Tenant-Id: $XERO_TENANT_ID" \
  -H "Accept: application/json"
```

## Get Bank Transactions

```bash
curl "https://api.xero.com/api.xro/2.0/BankTransactions" \
  -H "Authorization: Bearer $XERO_ACCESS_TOKEN" \
  -H "Xero-Tenant-Id: $XERO_TENANT_ID"
```

## Get Profit & Loss Report

```bash
curl "https://api.xero.com/api.xro/2.0/Reports/ProfitAndLoss?fromDate=2024-01-01&toDate=2024-12-31" \
  -H "Authorization: Bearer $XERO_ACCESS_TOKEN" \
  -H "Xero-Tenant-Id: $XERO_TENANT_ID"
```

## Links
- Dashboard: https://go.xero.com
- Docs: https://developer.xero.com/documentation/api/accounting/overview
