---
name: outlook
description: |
  Microsoft Outlook API integration with managed OAuth. Read, send, and manage emails, folders, calendar events, and contacts via Microsoft Graph. Use this skill when users want to interact with Outlook. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Outlook

Access the Microsoft Outlook API (via Microsoft Graph) with managed OAuth authentication. Read, send, and manage emails, folders, calendar events, and contacts.

## Quick Start

```bash
# Get user profile
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/outlook/v1.0/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/outlook/{native-api-path}
```

Replace `{native-api-path}` with the actual Microsoft Graph API endpoint path. The gateway proxies requests to `graph.microsoft.com` and automatically injects your OAuth token.

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

Manage your Microsoft OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=outlook&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'outlook'}).encode()
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
    "app": "outlook",
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

If you have multiple Outlook connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/outlook/v1.0/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If omitted, the gateway uses the default (oldest) active connection.

## API Reference

### User Profile

```bash
GET /outlook/v1.0/me
```

### Mail Folders

#### List Mail Folders

```bash
GET /outlook/v1.0/me/mailFolders
```

#### Get Mail Folder

```bash
GET /outlook/v1.0/me/mailFolders/{folderId}
```

Well-known folder names: `Inbox`, `Drafts`, `SentItems`, `DeletedItems`, `Archive`, `JunkEmail`

#### Create Mail Folder

```bash
POST /outlook/v1.0/me/mailFolders
Content-Type: application/json

{
  "displayName": "My Folder"
}
```

#### Delete Mail Folder

```bash
DELETE /outlook/v1.0/me/mailFolders/{folderId}
```

#### List Child Folders

```bash
GET /outlook/v1.0/me/mailFolders/{folderId}/childFolders
```

### Messages

#### List Messages

```bash
GET /outlook/v1.0/me/messages
```

From specific folder:

```bash
GET /outlook/v1.0/me/mailFolders/Inbox/messages
```

With query filter:

```bash
GET /outlook/v1.0/me/messages?$filter=isRead eq false&$top=10
```

#### Get Message

```bash
GET /outlook/v1.0/me/messages/{messageId}
```

#### Create Draft

```bash
POST /outlook/v1.0/me/messages
Content-Type: application/json

{
  "subject": "Hello",
  "body": {
    "contentType": "Text",
    "content": "This is the email body."
  },
  "toRecipients": [
    {
      "emailAddress": {
        "address": "recipient@example.com"
      }
    }
  ]
}
```

#### Send Message

```bash
POST /outlook/v1.0/me/sendMail
Content-Type: application/json

{
  "message": {
    "subject": "Hello",
    "body": {
      "contentType": "Text",
      "content": "This is the email body."
    },
    "toRecipients": [
      {
        "emailAddress": {
          "address": "recipient@example.com"
        }
      }
    ]
  },
  "saveToSentItems": true
}
```

#### Send Existing Draft

```bash
POST /outlook/v1.0/me/messages/{messageId}/send
```

#### Update Message

```bash
PATCH /outlook/v1.0/me/messages/{messageId}
Content-Type: application/json

{
  "isRead": true
}
```

#### Delete Message

```bash
DELETE /outlook/v1.0/me/messages/{messageId}
```

#### Move Message

```bash
POST /outlook/v1.0/me/messages/{messageId}/move
Content-Type: application/json

{
  "destinationId": "{folderId}"
}
```

### Calendar

#### List Calendars

```bash
GET /outlook/v1.0/me/calendars
```

#### List Events

```bash
GET /outlook/v1.0/me/calendar/events
```

With date filter:

```bash
GET /outlook/v1.0/me/calendar/events?$filter=start/dateTime ge '2024-01-01'&$top=10
```

#### Get Event

```bash
GET /outlook/v1.0/me/events/{eventId}
```

#### Create Event

```bash
POST /outlook/v1.0/me/calendar/events
Content-Type: application/json

{
  "subject": "Meeting",
  "start": {
    "dateTime": "2024-01-15T10:00:00",
    "timeZone": "UTC"
  },
  "end": {
    "dateTime": "2024-01-15T11:00:00",
    "timeZone": "UTC"
  },
  "attendees": [
    {
      "emailAddress": {
        "address": "attendee@example.com"
      },
      "type": "required"
    }
  ]
}
```

#### Delete Event

```bash
DELETE /outlook/v1.0/me/events/{eventId}
```

### Contacts

#### List Contacts

```bash
GET /outlook/v1.0/me/contacts
```

#### Get Contact

```bash
GET /outlook/v1.0/me/contacts/{contactId}
```

#### Create Contact

```bash
POST /outlook/v1.0/me/contacts
Content-Type: application/json

{
  "givenName": "John",
  "surname": "Doe",
  "emailAddresses": [
    {
      "address": "john.doe@example.com"
    }
  ]
}
```

#### Delete Contact

```bash
DELETE /outlook/v1.0/me/contacts/{contactId}
```

## Query Parameters

Use OData query parameters:

- `$top=10` - Limit results
- `$skip=20` - Skip results (pagination)
- `$select=subject,from` - Select specific fields
- `$filter=isRead eq false` - Filter results
- `$orderby=receivedDateTime desc` - Sort results
- `$search="keyword"` - Search content

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/outlook/v1.0/me/messages?$top=10',
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
    'https://gateway.maton.ai/outlook/v1.0/me/messages',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'$top': 10, '$filter': 'isRead eq false'}
)
```

## Notes

- Use `me` as the user identifier for the authenticated user
- Message body content types: `Text` or `HTML`
- Well-known folder names work as folder IDs: `Inbox`, `Drafts`, `SentItems`, etc.
- Calendar events use ISO 8601 datetime format
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets (`fields[]`, `sort[]`, `records[]`) to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments. You may get "Invalid API key" errors when piping.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Outlook connection |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from Microsoft Graph API |

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

1. Ensure your URL path starts with `outlook`. For example:

- Correct: `https://gateway.maton.ai/outlook/v1.0/me/messages`
- Incorrect: `https://gateway.maton.ai/v1.0/me/messages`

## Resources

- [Microsoft Graph API Overview](https://learn.microsoft.com/en-us/graph/api/overview)
- [Mail API](https://learn.microsoft.com/en-us/graph/api/resources/mail-api-overview)
- [Calendar API](https://learn.microsoft.com/en-us/graph/api/resources/calendar)
- [Contacts API](https://learn.microsoft.com/en-us/graph/api/resources/contact)
- [Query Parameters](https://learn.microsoft.com/en-us/graph/query-parameters)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
