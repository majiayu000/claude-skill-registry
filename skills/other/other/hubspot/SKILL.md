---
name: hubspot
description: "Manage HubSpot CRM — contacts, companies, deals, and tickets via the REST API."
metadata: {"thinkfleetbot":{"emoji":"🧲","requires":{"bins":["curl","jq"],"env":["HUBSPOT_ACCESS_TOKEN"]}}}
---

# HubSpot

Manage contacts, companies, deals, and tickets via the HubSpot API.

## Environment Variables

- `HUBSPOT_ACCESS_TOKEN` - Private app access token

## List contacts

```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/crm/v3/objects/contacts?limit=10&properties=email,firstname,lastname" | jq '.results[] | {id, properties}'
```

## Create contact

```bash
curl -s -X POST -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.hubapi.com/crm/v3/objects/contacts" \
  -d '{"properties":{"email":"user@example.com","firstname":"John","lastname":"Doe"}}' | jq '{id, properties}'
```

## List deals

```bash
curl -s -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  "https://api.hubapi.com/crm/v3/objects/deals?limit=10&properties=dealname,amount,dealstage" | jq '.results[] | {id, properties}'
```

## Search contacts

```bash
curl -s -X POST -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.hubapi.com/crm/v3/objects/contacts/search" \
  -d '{"filterGroups":[{"filters":[{"propertyName":"email","operator":"CONTAINS_TOKEN","value":"example.com"}]}],"limit":10}' | jq '.results[] | {id, properties}'
```

## Notes

- Always confirm before creating or updating CRM records.
