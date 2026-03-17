---
name: front-api
description: Reference for Front REST API integration. Use when working with Front API schemas, nullable fields, webhooks, or debugging Front SDK issues.
allowed-tools: Read, Grep
---

# Front API Skill

Reference for Front REST API integration.

## OpenAPI Spec

The full OpenAPI spec is in `core-api.json` (13k+ lines). Use it as the source of truth for:
- Request/response schemas
- Nullable fields
- Enum values
- Endpoint paths

## Key Schemas

### Message
- `recipients[].name` - nullable
- `recipients[]._links.related.contact` - nullable
- `recipients[].role` - enum: `from`, `to`, `cc`, `bcc`, `reply-to`
- `author` - nullable (null for inbound from external)
- `text` - nullable (plain text version of body)

### Conversation
- `assignee` - nullable
- `recipient` - nullable for some conversation types
- `tags` - can be empty array
- `last_message` - nullable
- `scheduled_reminders` - nullable

### Recipient
```json
{
  "name": "string | null",
  "handle": "string (required)",
  "role": "from | to | cc | bcc | reply-to",
  "_links": {
    "related": {
      "contact": "string | null"
    }
  }
}
```

## Common Gotchas

1. **Webhooks send previews only** - must fetch full data via API
2. **Many fields nullable** - don't assume presence, use `.nullable()` in Zod
3. **`_links.related.contact`** - null when recipient has no contact record
4. **`role` includes `reply-to`** - often forgotten in enums

## SDK Location

`@skillrecordings/front-sdk` - Zod schemas should match this spec exactly.

## Useful Endpoints

- `GET /messages/{id}` - Full message with body
- `GET /conversations/{id}` - Conversation details
- `GET /conversations/{id}/messages` - Message history
- `POST /conversations/{id}/drafts` - Create draft reply
- `GET /inboxes/{id}` - Inbox details
