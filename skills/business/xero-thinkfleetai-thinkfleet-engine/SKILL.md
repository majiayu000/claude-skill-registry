---
name: xero
description: "Query Xero accounting — invoices, contacts, accounts, and bank transactions via the REST API."
metadata: {"thinkfleetbot":{"emoji":"💰","requires":{"bins":["curl","jq"],"env":["XERO_ACCESS_TOKEN","XERO_TENANT_ID"]}}}
---

# Xero

Query invoices, contacts, accounts, and bank transactions.

## Environment Variables

- `XERO_ACCESS_TOKEN` - OAuth 2.0 access token
- `XERO_TENANT_ID` - Xero tenant ID

## List invoices

```bash
curl -s -H "Authorization: Bearer $XERO_ACCESS_TOKEN" \
  -H "Xero-Tenant-Id: $XERO_TENANT_ID" \
  "https://api.xero.com/api.xro/2.0/Invoices?page=1" | jq '.Invoices[:10] | .[] | {InvoiceID, InvoiceNumber, Contact: .Contact.Name, Total, Status}'
```

## List contacts

```bash
curl -s -H "Authorization: Bearer $XERO_ACCESS_TOKEN" \
  -H "Xero-Tenant-Id: $XERO_TENANT_ID" \
  "https://api.xero.com/api.xro/2.0/Contacts?page=1" | jq '.Contacts[:10] | .[] | {ContactID, Name, EmailAddress}'
```

## Get profit/loss

```bash
curl -s -H "Authorization: Bearer $XERO_ACCESS_TOKEN" \
  -H "Xero-Tenant-Id: $XERO_TENANT_ID" \
  "https://api.xero.com/api.xro/2.0/Reports/ProfitAndLoss?fromDate=2024-01-01&toDate=2024-12-31" | jq '.Reports[0].Rows'
```

## List accounts

```bash
curl -s -H "Authorization: Bearer $XERO_ACCESS_TOKEN" \
  -H "Xero-Tenant-Id: $XERO_TENANT_ID" \
  "https://api.xero.com/api.xro/2.0/Accounts" | jq '.Accounts[:10] | .[] | {AccountID, Name, Type, Code}'
```

## Notes

- Always confirm before creating invoices or payments.
