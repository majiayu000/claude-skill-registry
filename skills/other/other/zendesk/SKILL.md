---
name: zendesk
description: "Manage Zendesk Support — tickets, users, organizations, and search via the REST API."
metadata: {"thinkfleetbot":{"emoji":"🎟️","requires":{"bins":["curl","jq"],"env":["ZENDESK_SUBDOMAIN","ZENDESK_EMAIL","ZENDESK_API_TOKEN"]}}}
---

# Zendesk

Manage tickets, users, and organizations.

## Environment Variables

- `ZENDESK_SUBDOMAIN` - Subdomain (e.g. `mycompany`)
- `ZENDESK_EMAIL` - Agent email
- `ZENDESK_API_TOKEN` - API token

## List tickets

```bash
curl -s -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
  "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/tickets?per_page=10" | jq '.tickets[] | {id, subject, status, priority}'
```

## Create ticket

```bash
curl -s -X POST -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/tickets" \
  -d '{"ticket":{"subject":"Issue","description":"Details","priority":"normal"}}' | jq '.ticket | {id, subject}'
```

## Search

```bash
curl -s -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
  "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/search?query=type:ticket%20status:open" | jq '.results[] | {id, subject, status}'
```

## Notes

- Always confirm before creating or updating tickets.
