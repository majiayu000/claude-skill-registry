---
name: kit
description: |
  Kit (formerly ConvertKit) API integration with managed OAuth. Manage email subscribers, forms, tags, sequences, broadcasts, and custom fields.
  Use this skill when users want to manage their email marketing lists, create or update subscribers, manage tags, or work with email sequences and broadcasts.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Kit

Access the Kit (formerly ConvertKit) API with managed OAuth authentication. Manage subscribers, tags, forms, sequences, broadcasts, custom fields, and webhooks.

## Quick Start

```bash
# List subscribers
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/kit/v4/subscribers?per_page=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/kit/{native-api-path}
```

Replace `{native-api-path}` with the actual Kit API endpoint path. The gateway proxies requests to `api.kit.com` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
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

Manage your Kit OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=kit&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'kit'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "cb2025b3-706f-4b5d-87a5-c6809c0c7ec4",
    "status": "ACTIVE",
    "creation_time": "2026-02-07T00:04:08.476727Z",
    "last_updated_time": "2026-02-07T00:05:58.001964Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "kit",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Kit connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/kit/v4/subscribers')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'cb2025b3-706f-4b5d-87a5-c6809c0c7ec4')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If omitted, the gateway uses the default (oldest) active connection.

## API Reference

### Subscribers

#### List Subscribers

```bash
GET /kit/v4/subscribers
```

Query parameters:
- `per_page` - Results per page (default: 500, max: 1000)
- `after` - Cursor for next page
- `before` - Cursor for previous page
- `status` - Filter by: `active`, `inactive`, `bounced`, `complained`, `cancelled`, or `all`
- `email_address` - Filter by specific email
- `created_after` / `created_before` - Filter by creation date (yyyy-mm-dd)
- `updated_after` / `updated_before` - Filter by update date (yyyy-mm-dd)
- `include_total_count` - Include total count (slower)

**Response:**
```json
{
  "subscribers": [
    {
      "id": 3914682852,
      "first_name": "Test User",
      "email_address": "test@example.com",
      "state": "active",
      "created_at": "2026-02-07T00:42:54Z",
      "fields": {"company": null}
    }
  ],
  "pagination": {
    "has_previous_page": false,
    "has_next_page": false,
    "start_cursor": "WzE0OV0=",
    "end_cursor": "WzE0OV0=",
    "per_page": 500
  }
}
```

#### Get Subscriber

```bash
GET /kit/v4/subscribers/{id}
```

#### Create Subscriber

```bash
POST /kit/v4/subscribers
Content-Type: application/json

{
  "email_address": "user@example.com",
  "first_name": "John"
}
```

#### Update Subscriber

```bash
PUT /kit/v4/subscribers/{id}
Content-Type: application/json

{
  "first_name": "Updated Name"
}
```

### Tags

#### List Tags

```bash
GET /kit/v4/tags
```

Query parameters: `per_page`, `after`, `before`, `include_total_count`

#### Create Tag

```bash
POST /kit/v4/tags
Content-Type: application/json

{
  "name": "new-tag"
}
```

**Response:**
```json
{
  "tag": {
    "id": 15690016,
    "name": "new-tag",
    "created_at": "2026-02-07T00:42:53Z"
  }
}
```

#### Update Tag

```bash
PUT /kit/v4/tags/{id}
Content-Type: application/json

{
  "name": "updated-tag-name"
}
```

#### Delete Tag

```bash
DELETE /kit/v4/tags/{id}
```

Returns 204 No Content on success.

#### Tag a Subscriber

```bash
POST /kit/v4/tags/{tag_id}/subscribers
Content-Type: application/json

{
  "email_address": "user@example.com"
}
```

#### Remove Tag from Subscriber

```bash
DELETE /kit/v4/tags/{tag_id}/subscribers/{subscriber_id}
```

Returns 204 No Content on success.

#### List Subscribers with Tag

```bash
GET /kit/v4/tags/{tag_id}/subscribers
```

### Forms

#### List Forms

```bash
GET /kit/v4/forms
```

Query parameters:
- `per_page`, `after`, `before`, `include_total_count`
- `status` - Filter by: `active`, `archived`, `trashed`, or `all`
- `type` - `embed` for embedded forms, `hosted` for landing pages

**Response:**
```json
{
  "forms": [
    {
      "id": 9061198,
      "name": "Creator Profile",
      "created_at": "2026-02-07T00:00:32Z",
      "type": "embed",
      "format": null,
      "embed_js": "https://chris-kim-2.kit.com/c682763b07/index.js",
      "embed_url": "https://chris-kim-2.kit.com/c682763b07",
      "archived": false,
      "uid": "c682763b07"
    }
  ],
  "pagination": {...}
}
```

#### Add Subscriber to Form

```bash
POST /kit/v4/forms/{form_id}/subscribers
Content-Type: application/json

{
  "email_address": "user@example.com"
}
```

#### List Form Subscribers

```bash
GET /kit/v4/forms/{form_id}/subscribers
```

### Sequences

#### List Sequences

```bash
GET /kit/v4/sequences
```

**Response:**
```json
{
  "sequences": [
    {
      "id": 123,
      "name": "Welcome Sequence",
      "hold": false,
      "repeat": false,
      "created_at": "2026-01-01T00:00:00Z"
    }
  ],
  "pagination": {...}
}
```

#### Add Subscriber to Sequence

```bash
POST /kit/v4/sequences/{sequence_id}/subscribers
Content-Type: application/json

{
  "email_address": "user@example.com"
}
```

#### List Sequence Subscribers

```bash
GET /kit/v4/sequences/{sequence_id}/subscribers
```

### Broadcasts

#### List Broadcasts

```bash
GET /kit/v4/broadcasts
```

Query parameters: `per_page`, `after`, `before`, `include_total_count`

**Response:**
```json
{
  "broadcasts": [
    {
      "id": 123,
      "publication_id": 456,
      "created_at": "2026-02-07T00:00:00Z",
      "subject": "My Broadcast",
      "preview_text": "Preview...",
      "content": "<p>Content</p>",
      "public": false,
      "published_at": null,
      "send_at": null,
      "email_template": {"id": 123, "name": "Text only"}
    }
  ],
  "pagination": {...}
}
```

### Segments

#### List Segments

```bash
GET /kit/v4/segments
```

Query parameters: `per_page`, `after`, `before`, `include_total_count`

### Custom Fields

#### List Custom Fields

```bash
GET /kit/v4/custom_fields
```

**Response:**
```json
{
  "custom_fields": [
    {
      "id": 1192946,
      "name": "ck_field_1192946_company",
      "key": "company",
      "label": "Company"
    }
  ],
  "pagination": {...}
}
```

#### Create Custom Field

```bash
POST /kit/v4/custom_fields
Content-Type: application/json

{
  "label": "Company"
}
```

#### Update Custom Field

```bash
PUT /kit/v4/custom_fields/{id}
Content-Type: application/json

{
  "label": "Company Name"
}
```

#### Delete Custom Field

```bash
DELETE /kit/v4/custom_fields/{id}
```

Returns 204 No Content on success.

### Purchases

#### List Purchases

```bash
GET /kit/v4/purchases
```

Query parameters: `per_page`, `after`, `before`, `include_total_count`

### Email Templates

#### List Email Templates

```bash
GET /kit/v4/email_templates
```

**Response:**
```json
{
  "email_templates": [
    {
      "id": 4956167,
      "name": "Text only",
      "is_default": true,
      "category": "Classic"
    }
  ],
  "pagination": {...}
}
```

### Webhooks

#### List Webhooks

```bash
GET /kit/v4/webhooks
```

#### Create Webhook

```bash
POST /kit/v4/webhooks
Content-Type: application/json

{
  "target_url": "https://example.com/webhook",
  "event": {"name": "subscriber.subscriber_activate"}
}
```

**Response:**
```json
{
  "webhook": {
    "id": 5291560,
    "account_id": 2596262,
    "event": {
      "name": "subscriber_activate",
      "initiator_value": null
    },
    "target_url": "https://example.com/webhook"
  }
}
```

#### Delete Webhook

```bash
DELETE /kit/v4/webhooks/{id}
```

Returns 204 No Content on success.

## Pagination

Kit uses cursor-based pagination. Use `after` and `before` query parameters with cursor values from the response.

```bash
GET /kit/v4/subscribers?per_page=100&after=WzE0OV0=
```

Response includes pagination info:

```json
{
  "subscribers": [...],
  "pagination": {
    "has_previous_page": false,
    "has_next_page": true,
    "start_cursor": "WzE0OV0=",
    "end_cursor": "WzI0OV0=",
    "per_page": 100
  }
}
```

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/kit/v4/subscribers?per_page=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/kit/v4/subscribers',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'per_page': 10}
)
data = response.json()
```

## Notes

- Kit API uses V4 (V3 is deprecated)
- Subscriber IDs are integers
- Custom field keys are auto-generated from labels
- Bulk operations (>100 items) are processed asynchronously
- Delete operations return 204 No Content with empty body
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Kit connection |
| 401 | Invalid or missing Maton API key |
| 403 | Insufficient permissions (check OAuth scopes) |
| 404 | Resource not found |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Kit API |

### Troubleshooting: API Key Issues

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

1. Ensure your URL path starts with `kit`. For example:

- Correct: `https://gateway.maton.ai/kit/v4/subscribers`
- Incorrect: `https://gateway.maton.ai/v4/subscribers`

## Resources

- [Kit API Overview](https://developers.kit.com/api-reference/overview)
- [Kit API Subscribers](https://developers.kit.com/api-reference/subscribers/list-subscribers)
- [Kit API Tags](https://developers.kit.com/api-reference/tags/list-tags)
- [Kit API Forms](https://developers.kit.com/api-reference/forms/list-forms)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
