---
name: clio
description: |
  Clio API integration with managed OAuth. Legal practice management including matters, contacts, activities, tasks, documents, calendar entries, time entries, and billing.
  Use this skill when users want to manage legal practice data in Clio Manage.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Clio

Access the Clio Manage API with managed OAuth authentication. Manage matters, contacts, activities, tasks, documents, calendar entries, time entries, and billing for legal practice management.

## Quick Start

```bash
# List matters
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clio/api/v4/matters?fields=id,display_number,description,status')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/clio/{native-api-path}
```

Replace `{native-api-path}` with the actual Clio API endpoint path. The gateway proxies requests to `app.clio.com` and automatically injects your OAuth token.

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

Manage your Clio OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=clio&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'clio'}).encode()
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
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "clio",
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

If you have multiple Clio connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clio/api/v4/matters')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If omitted, the gateway uses the default (oldest) active connection.

## API Reference

### Field Selection

By default, Clio returns minimal fields (`id`, `etag`). Use the `fields` parameter to request specific fields:

```bash
GET /clio/api/v4/matters?fields=id,display_number,description,status
```

For nested resources, use curly bracket syntax:

```bash
GET /clio/api/v4/activities?fields=id,type,matter{id,description}
```

### Matters

#### List Matters

```bash
GET /clio/api/v4/matters?fields=id,display_number,description,status,client_reference
```

#### Get Matter

```bash
GET /clio/api/v4/matters/{id}?fields=id,display_number,description,status,open_date,close_date
```

#### Create Matter

```bash
POST /clio/api/v4/matters
Content-Type: application/json

{
  "data": {
    "description": "New Legal Matter",
    "status": "open",
    "client": {"id": 12345}
  }
}
```

#### Update Matter

```bash
PATCH /clio/api/v4/matters/{id}
Content-Type: application/json

{
  "data": {
    "description": "Updated Matter Description",
    "status": "closed"
  }
}
```

#### Delete Matter

```bash
DELETE /clio/api/v4/matters/{id}
```

### Contacts

#### List Contacts

```bash
GET /clio/api/v4/contacts?fields=id,name,type,primary_email_address,primary_phone_number
```

#### Get Contact

```bash
GET /clio/api/v4/contacts/{id}?fields=id,name,type,first_name,last_name,company
```

#### Create Contact (Person)

```bash
POST /clio/api/v4/contacts
Content-Type: application/json

{
  "data": {
    "type": "Person",
    "first_name": "John",
    "last_name": "Doe",
    "email_addresses": [
      {"name": "Work", "address": "john@example.com", "default_email": true}
    ]
  }
}
```

#### Create Contact (Company)

```bash
POST /clio/api/v4/contacts
Content-Type: application/json

{
  "data": {
    "type": "Company",
    "name": "Acme Corporation"
  }
}
```

#### Update Contact

```bash
PATCH /clio/api/v4/contacts/{id}
Content-Type: application/json

{
  "data": {
    "first_name": "Jane"
  }
}
```

#### Delete Contact

```bash
DELETE /clio/api/v4/contacts/{id}
```

### Activities

#### List Activities

```bash
GET /clio/api/v4/activities?fields=id,type,date,quantity,matter{id,description}
```

#### Get Activity

```bash
GET /clio/api/v4/activities/{id}?fields=id,type,date,quantity,note
```

#### Create Activity

```bash
POST /clio/api/v4/activities
Content-Type: application/json

{
  "data": {
    "type": "TimeEntry",
    "date": "2026-02-11",
    "quantity": 3600,
    "matter": {"id": 12345},
    "note": "Legal research"
  }
}
```

#### Update Activity

```bash
PATCH /clio/api/v4/activities/{id}
Content-Type: application/json

{
  "data": {
    "note": "Updated note"
  }
}
```

#### Delete Activity

```bash
DELETE /clio/api/v4/activities/{id}
```

### Tasks

#### List Tasks

```bash
GET /clio/api/v4/tasks?fields=id,name,status,due_at,priority,matter{id,description}
```

#### Get Task

```bash
GET /clio/api/v4/tasks/{id}?fields=id,name,description,status,due_at,priority
```

#### Create Task

Requires `assignee` with both `id` and `type` ("User" or "Contact"):

```bash
POST /clio/api/v4/tasks
Content-Type: application/json

{
  "data": {
    "name": "Review contract",
    "due_at": "2026-02-15T17:00:00Z",
    "priority": "Normal",
    "assignee": {"id": 12345, "type": "User"},
    "matter": {"id": 67890}
  }
}
```

#### Update Task

```bash
PATCH /clio/api/v4/tasks/{id}
Content-Type: application/json

{
  "data": {
    "status": "complete"
  }
}
```

#### Delete Task

```bash
DELETE /clio/api/v4/tasks/{id}
```

### Calendar Entries

#### List Calendar Entries

```bash
GET /clio/api/v4/calendar_entries?fields=id,summary,start_at,end_at,matter{id,description}
```

#### Get Calendar Entry

```bash
GET /clio/api/v4/calendar_entries/{id}?fields=id,summary,description,start_at,end_at,location
```

#### Create Calendar Entry

Requires `calendar_owner` with `id` and `type`:

```bash
POST /clio/api/v4/calendar_entries
Content-Type: application/json

{
  "data": {
    "summary": "Client Meeting",
    "start_at": "2026-02-15T10:00:00Z",
    "end_at": "2026-02-15T11:00:00Z",
    "calendar_owner": {"id": 12345, "type": "User"}
  }
}
```

**Note:** Associating a matter with a calendar entry during creation may return a 404 error. To link a matter, update the calendar entry after creation using PATCH.

#### Update Calendar Entry

```bash
PATCH /clio/api/v4/calendar_entries/{id}
Content-Type: application/json

{
  "data": {
    "summary": "Updated Meeting Title"
  }
}
```

#### Delete Calendar Entry

```bash
DELETE /clio/api/v4/calendar_entries/{id}
```

### Documents

#### List Documents

```bash
GET /clio/api/v4/documents?fields=id,name,content_type,size,matter{id,description}
```

#### Get Document

```bash
GET /clio/api/v4/documents/{id}?fields=id,name,content_type,size,created_at
```

#### Download Document

```bash
GET /clio/api/v4/documents/{id}/download
```

### Users

#### Get Current User

```bash
GET /clio/api/v4/users/who_am_i?fields=id,name,email,enabled
```

#### List Users

```bash
GET /clio/api/v4/users?fields=id,name,email,enabled,rate
```

### Bills

#### List Bills

```bash
GET /clio/api/v4/bills?fields=id,number,issued_at,due_at,total,balance,state
```

#### Get Bill

```bash
GET /clio/api/v4/bills/{id}?fields=id,number,issued_at,due_at,total,balance,state
```

## Pagination

Clio uses cursor-based pagination. Response includes pagination metadata:

```bash
GET /clio/api/v4/matters?fields=id,description&limit=50
```

Response includes pagination info in the `meta` object:

```json
{
  "data": [...],
  "meta": {
    "paging": {
      "next": "https://app.clio.com/api/v4/matters?page_token=xyz123"
    },
    "records": 50
  }
}
```

Use the `page_token` parameter to fetch the next page:

```bash
GET /clio/api/v4/matters?fields=id,description&page_token=xyz123
```

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/clio/api/v4/matters?fields=id,display_number,description',
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
    'https://gateway.maton.ai/clio/api/v4/matters',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'fields': 'id,display_number,description'}
)
data = response.json()
```

## Notes

- Field selection is important - default responses only include `id` and `etag`
- Nested resources use curly bracket syntax: `matter{id,description}`
- Only one level of nesting is supported
- Contact types: `Person` or `Company`
- Task assignees require both `id` and `type` ("User" or "Contact")
- Calendar entries require `calendar_owner` with `id` and `type`; associating a matter during creation may fail - use PATCH to link matters after creation
- Activity quantity is in seconds (3600 = 1 hour)
- Contact records limited to 20 email addresses, phone numbers, and addresses each
- Activities, Documents, and Bills endpoints require additional OAuth scopes beyond the basic integration
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Clio connection or bad request |
| 401 | Invalid or missing Maton API key |
| 404 | Resource not found |
| 429 | Rate limited (50 req/min during peak hours) |
| 4xx/5xx | Passthrough error from Clio API |

### Rate Limit Headers

Clio includes rate limit headers in responses:
- `X-RateLimit-Limit` - Maximum requests in 60-second window
- `X-RateLimit-Remaining` - Requests remaining in current window
- `X-RateLimit-Reset` - Unix timestamp for window reset
- `Retry-After` - Seconds to wait (when throttled)

## Resources

- [Clio API Documentation](https://docs.developers.clio.com/api-reference/)
- [Clio Fields Guide](https://docs.developers.clio.com/api-docs/clio-manage/fields/)
- [Clio Rate Limits](https://docs.developers.clio.com/api-docs/clio-manage/rate-limits/)
- [Clio Permissions](https://docs.developers.clio.com/api-docs/permissions/)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
