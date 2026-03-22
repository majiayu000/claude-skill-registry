---
name: quo
description: |
  Quo API integration with managed OAuth. Manage calls, messages, contacts, and conversations for your business phone system.
  Use this skill when users want to send SMS, list calls, manage contacts, or retrieve call recordings/transcripts.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Quo

Access the Quo API with managed OAuth authentication. Send SMS messages, manage calls and contacts, and retrieve call recordings and transcripts.

## Quick Start

```bash
# List phone numbers
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/quo/v1/phone-numbers')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('User-Agent', 'Maton/1.0')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/quo/{native-api-path}
```

Replace `{native-api-path}` with the actual Quo API endpoint path. The gateway proxies requests to `api.openphone.com` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header and a User-Agent header:

```
Authorization: Bearer $MATON_API_KEY
User-Agent: Maton/1.0
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

Manage your Quo OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=quo&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'quo'}).encode()
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
    "app": "quo",
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

If you have multiple Quo connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/quo/v1/phone-numbers')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('User-Agent', 'Maton/1.0')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If omitted, the gateway uses the default (oldest) active connection.

## API Reference

### Phone Numbers

#### List Phone Numbers

```bash
GET /quo/v1/phone-numbers
```

Optional query parameter:
- `userId` - Filter by user ID (pattern: `^US(.*)$`)

**Response:**
```json
{
  "data": [
    {
      "id": "PN123abc",
      "number": "+15555555555",
      "formattedNumber": "(555) 555-5555",
      "name": "Main Line",
      "users": [
        {
          "id": "US123abc",
          "email": "user@example.com",
          "firstName": "John",
          "lastName": "Doe",
          "role": "admin"
        }
      ],
      "createdAt": "2022-01-01T00:00:00Z",
      "updatedAt": "2022-01-01T00:00:00Z"
    }
  ]
}
```

### Users

#### List Users

```bash
GET /quo/v1/users?maxResults=50
```

Query parameters:
- `maxResults` (required) - Results per page (1-50, default: 10)
- `pageToken` - Pagination token

**Response:**
```json
{
  "data": [
    {
      "id": "US123abc",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "owner",
      "createdAt": "2022-01-01T00:00:00Z",
      "updatedAt": "2022-01-01T00:00:00Z"
    }
  ],
  "totalItems": 10,
  "nextPageToken": null
}
```

#### Get User by ID

```bash
GET /quo/v1/users/{userId}
```

### Messages

#### Send Text Message

```bash
POST /quo/v1/messages
Content-Type: application/json

{
  "content": "Hello, world!",
  "from": "PN123abc",
  "to": ["+15555555555"]
}
```

Request body:
- `content` (required) - Message text (1-1600 characters)
- `from` (required) - Phone number ID (`PN*`) or E.164 format
- `to` (required) - Array with single recipient in E.164 format
- `userId` - User ID (defaults to phone owner)
- `setInboxStatus` - Set to `"done"` to mark conversation complete

**Response (202):**
```json
{
  "id": "AC123abc",
  "to": ["+15555555555"],
  "from": "+15555555555",
  "text": "Hello, world!",
  "phoneNumberId": "PN123abc",
  "direction": "outgoing",
  "userId": "US123abc",
  "status": "queued",
  "createdAt": "2022-01-01T00:00:00Z",
  "updatedAt": "2022-01-01T00:00:00Z"
}
```

#### List Messages

```bash
GET /quo/v1/messages?phoneNumberId=PN123abc&participants[]=+15555555555&maxResults=100
```

Query parameters:
- `phoneNumberId` (required) - Phone number ID
- `participants` (required) - Array of participant phone numbers in E.164 format
- `maxResults` (required) - Results per page (1-100, default: 10)
- `userId` - Filter by user ID
- `createdAfter` - ISO 8601 timestamp
- `createdBefore` - ISO 8601 timestamp
- `pageToken` - Pagination token

#### Get Message by ID

```bash
GET /quo/v1/messages/{messageId}
```

### Calls

#### List Calls

```bash
GET /quo/v1/calls?phoneNumberId=PN123abc&participants[]=+15555555555&maxResults=100
```

Query parameters:
- `phoneNumberId` (required) - Phone number ID
- `participants` (required) - Array with single participant phone number in E.164 format (max 1)
- `maxResults` (required) - Results per page (1-100, default: 10)
- `userId` - Filter by user ID
- `createdAfter` - ISO 8601 timestamp
- `createdBefore` - ISO 8601 timestamp
- `pageToken` - Pagination token

**Response:**
```json
{
  "data": [
    {
      "id": "AC123abc",
      "phoneNumberId": "PN123abc",
      "userId": "US123abc",
      "direction": "incoming",
      "status": "completed",
      "duration": 120,
      "participants": ["+15555555555"],
      "answeredAt": "2022-01-01T00:00:00Z",
      "completedAt": "2022-01-01T00:02:00Z",
      "createdAt": "2022-01-01T00:00:00Z",
      "updatedAt": "2022-01-01T00:02:00Z"
    }
  ],
  "totalItems": 50,
  "nextPageToken": "..."
}
```

#### Get Call by ID

```bash
GET /quo/v1/calls/{callId}
```

#### Get Call Recordings

```bash
GET /quo/v1/call-recordings/{callId}
```

**Response:**
```json
{
  "data": [
    {
      "id": "REC123abc",
      "duration": 120,
      "startTime": "2022-01-01T00:00:00Z",
      "status": "completed",
      "type": "voicemail",
      "url": "https://..."
    }
  ]
}
```

Recording status values: `absent`, `completed`, `deleted`, `failed`, `in-progress`, `paused`, `processing`, `stopped`, `stopping`

#### Get Call Summary

```bash
GET /quo/v1/call-summaries/{callId}
```

#### Get Call Transcript

```bash
GET /quo/v1/call-transcripts/{callId}
```

#### Get Call Voicemail

```bash
GET /quo/v1/call-voicemails/{callId}
```

### Contacts

#### List Contacts

```bash
GET /quo/v1/contacts?maxResults=50
```

Query parameters:
- `maxResults` (required) - Results per page (1-50, default: 10)
- `externalIds` - Array of external identifiers
- `sources` - Array of source indicators
- `pageToken` - Pagination token

**Response:**
```json
{
  "data": [
    {
      "id": "CT123abc",
      "externalId": null,
      "source": null,
      "defaultFields": {
        "company": "Acme Corp",
        "firstName": "Jane",
        "lastName": "Doe",
        "role": "Manager",
        "emails": [{"name": "work", "value": "jane@example.com", "id": "EM1"}],
        "phoneNumbers": [{"name": "mobile", "value": "+15555555555", "id": "PH1"}]
      },
      "customFields": [],
      "createdAt": "2022-01-01T00:00:00Z",
      "updatedAt": "2022-01-01T00:00:00Z",
      "createdByUserId": "US123abc"
    }
  ],
  "totalItems": 100,
  "nextPageToken": "..."
}
```

#### Get Contact by ID

```bash
GET /quo/v1/contacts/{contactId}
```

#### Create Contact

```bash
POST /quo/v1/contacts
Content-Type: application/json

{
  "defaultFields": {
    "firstName": "Jane",
    "lastName": "Doe",
    "company": "Acme Corp",
    "phoneNumbers": [{"name": "mobile", "value": "+15555555555"}],
    "emails": [{"name": "work", "value": "jane@example.com"}]
  }
}
```

#### Update Contact

```bash
PATCH /quo/v1/contacts/{contactId}
Content-Type: application/json

{
  "defaultFields": {
    "company": "New Company"
  }
}
```

#### Delete Contact

```bash
DELETE /quo/v1/contacts/{contactId}
```

#### Get Contact Custom Fields

```bash
GET /quo/v1/contact-custom-fields
```

### Conversations

#### List Conversations

```bash
GET /quo/v1/conversations?maxResults=100
```

Query parameters:
- `maxResults` (required) - Results per page (1-100, default: 10)
- `phoneNumbers` - Array of phone number IDs or E.164 numbers (1-100 items)
- `userId` - Filter by user ID
- `createdAfter` - ISO 8601 timestamp
- `createdBefore` - ISO 8601 timestamp
- `updatedAfter` - ISO 8601 timestamp
- `updatedBefore` - ISO 8601 timestamp
- `excludeInactive` - Boolean to exclude inactive conversations
- `pageToken` - Pagination token

**Response:**
```json
{
  "data": [
    {
      "id": "CV123abc",
      "phoneNumberId": "PN123abc",
      "name": "Jane Doe",
      "participants": ["+15555555555"],
      "assignedTo": "US123abc",
      "lastActivityAt": "2022-01-01T00:00:00Z",
      "createdAt": "2022-01-01T00:00:00Z",
      "updatedAt": "2022-01-01T00:00:00Z"
    }
  ],
  "totalItems": 50,
  "nextPageToken": "..."
}
```

## Pagination

Quo uses token-based pagination. Include `maxResults` to set page size and use `pageToken` to retrieve subsequent pages.

```bash
GET /quo/v1/contacts?maxResults=50&pageToken=eyJsYXN0SWQiOi...
```

Response includes pagination info:

```json
{
  "data": [...],
  "totalItems": 150,
  "nextPageToken": "eyJsYXN0SWQiOi..."
}
```

When `nextPageToken` is `null`, you've reached the last page.

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/quo/v1/phone-numbers',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'User-Agent': 'Maton/1.0'
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
    'https://gateway.maton.ai/quo/v1/phone-numbers',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'User-Agent': 'Maton/1.0'
    }
)
data = response.json()
```

### Send SMS Example

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/quo/v1/messages',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'User-Agent': 'Maton/1.0',
        'Content-Type': 'application/json'
    },
    json={
        'content': 'Hello from Quo!',
        'from': 'PN123abc',
        'to': ['+15555555555']
    }
)
data = response.json()
```

## Notes

- Phone number IDs start with `PN`
- User IDs start with `US`
- Call/Message IDs start with `AC`
- Phone numbers must be in E.164 format (e.g., `+15555555555`)
- SMS pricing: $0.01 per segment (US/Canada); international rates apply
- Maximum 1600 characters per message
- List calls requires exactly 1 participant (1:1 conversations only)
- IMPORTANT: All API requests require a `User-Agent` header (e.g., `User-Agent: Maton/1.0`). Requests without this header will be blocked.
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets (`participants[]`) to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Bad request (e.g., too many participants, invalid format) |
| 401 | Invalid or missing Maton API key |
| 402 | Insufficient credits for SMS |
| 403 | Not authorized for this phone number |
| 404 | Resource not found |
| 429 | Rate limited |
| 500 | Server error |

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

1. Ensure your URL path starts with `quo`. For example:

- Correct: `https://gateway.maton.ai/quo/v1/phone-numbers`
- Incorrect: `https://gateway.maton.ai/openphone/v1/phone-numbers`

## Resources

- [Quo API Introduction](https://www.quo.com/docs/mdx/api-reference/introduction)
- [Quo API Authentication](https://www.quo.com/docs/mdx/api-reference/authentication)
- [Quo Support Center](https://support.quo.com/core-concepts/integrations/api)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
