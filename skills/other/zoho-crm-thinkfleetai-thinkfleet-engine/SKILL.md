---
name: zoho-crm
description: "Manage Zoho CRM — leads, contacts, deals, and accounts via the REST API."
metadata: {"thinkfleetbot":{"emoji":"📊","requires":{"bins":["curl","jq"],"env":["ZOHO_ACCESS_TOKEN","ZOHO_API_DOMAIN"]}}}
---

# Zoho CRM

Manage leads, contacts, deals, and accounts.

## Environment Variables

- `ZOHO_ACCESS_TOKEN` - OAuth access token
- `ZOHO_API_DOMAIN` - API domain (e.g. `https://www.zohoapis.com`)

## List leads

```bash
curl -s -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  "$ZOHO_API_DOMAIN/crm/v5/Leads?per_page=10" | jq '.data[] | {id, Full_Name, Email, Company, Lead_Status}'
```

## List deals

```bash
curl -s -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  "$ZOHO_API_DOMAIN/crm/v5/Deals?per_page=10" | jq '.data[] | {id, Deal_Name, Amount, Stage}'
```

## Create lead

```bash
curl -s -X POST -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "$ZOHO_API_DOMAIN/crm/v5/Leads" \
  -d '{"data":[{"Last_Name":"Doe","First_Name":"John","Email":"john@example.com","Company":"Acme"}]}' | jq '.data[]'
```

## Notes

- Always confirm before creating or updating records.
