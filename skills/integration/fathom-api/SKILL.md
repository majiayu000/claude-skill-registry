---
name: fathom
description: |
  Fathom API integration with managed OAuth. Access meeting recordings, transcripts, summaries, and manage webhooks. Use this skill when users want to retrieve meeting content, search recordings, or set up webhook notifications for new meetings.
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
---

# Fathom

Access the Fathom API with managed OAuth authentication. Retrieve meeting recordings, transcripts, summaries, action items, and manage webhooks for notifications.

## Quick Start

```bash
# List recent meetings
curl -s -X GET 'https://gateway.maton.ai/fathom/external/v1/meetings' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

## Base URL

```
https://gateway.maton.ai/fathom/{native-api-path}
```

Replace `{native-api-path}` with the actual Fathom API endpoint path. The gateway proxies requests to `api.fathom.ai` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer YOUR_API_KEY
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

Manage your Fathom OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
curl -s -X GET 'https://ctrl.maton.ai/connections?app=fathom&status=ACTIVE' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### Create Connection

```bash
curl -s -X POST 'https://ctrl.maton.ai/connections' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{"app": "fathom"}'
```

### Get Connection

```bash
curl -s -X GET 'https://ctrl.maton.ai/connections/{connection_id}' \
  -H 'Authorization: Bearer YOUR_API_KEY'
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
    "app": "fathom",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
curl -s -X DELETE 'https://ctrl.maton.ai/connections/{connection_id}' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### Specifying Connection

If you have multiple Fathom connections, specify which one to use with the `Maton-Connection` header:

```bash
curl -s -X GET 'https://gateway.maton.ai/fathom/external/v1/meetings' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Maton-Connection: 21fd90f9-5935-43cd-b6c8-bde9d915ca80'
```

If omitted, the gateway uses the default (oldest) active connection.

## API Reference

### Meetings

#### List Meetings

```bash
GET /fathom/external/v1/meetings
```

Query parameters:
- `cursor` - Cursor for pagination
- `created_after` - Filter to meetings created after this timestamp (e.g., `2025-01-01T00:00:00Z`)
- `created_before` - Filter to meetings created before this timestamp
- `calendar_invitees_domains[]` - Filter by company domains (pass once per value)
- `calendar_invitees_domains_type` - Filter by invitee type: `all`, `only_internal`, `one_or_more_external`
- `recorded_by[]` - Filter by email addresses of users who recorded meetings
- `teams[]` - Filter by team names

**Note:** OAuth users cannot use `include_transcript`, `include_summary`, `include_action_items`, or `include_crm_matches` parameters on this endpoint. Use the `/recordings/{recording_id}/summary` and `/recordings/{recording_id}/transcript` endpoints instead.

**Example with filters:**

```bash
curl -s -X GET 'https://gateway.maton.ai/fathom/external/v1/meetings?created_after=2025-01-01T00:00:00Z&teams[]=Sales' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response:**
```json
{
  "limit": 10,
  "next_cursor": "eyJwYWdlX251bSI6Mn0=",
  "items": [
    {
      "title": "Quarterly Business Review",
      "meeting_title": "QBR 2025 Q1",
      "recording_id": 123456789,
      "url": "https://fathom.video/xyz123",
      "share_url": "https://fathom.video/share/xyz123",
      "created_at": "2025-03-01T17:01:30Z",
      "scheduled_start_time": "2025-03-01T16:00:00Z",
      "scheduled_end_time": "2025-03-01T17:00:00Z",
      "recording_start_time": "2025-03-01T16:01:12Z",
      "recording_end_time": "2025-03-01T17:00:55Z",
      "calendar_invitees_domains_type": "one_or_more_external",
      "transcript_language": "en",
      "transcript": null,
      "default_summary": null,
      "action_items": null,
      "crm_matches": null,
      "recorded_by": {
        "name": "Alice Johnson",
        "email": "alice.johnson@acme.com",
        "email_domain": "acme.com",
        "team": "Marketing"
      },
      "calendar_invitees": [
        {
          "name": "Alice Johnson",
          "email": "alice.johnson@acme.com",
          "email_domain": "acme.com",
          "is_external": false,
          "matched_speaker_display_name": null
        }
      ]
    }
  ]
}
```

### Recordings

#### Get Summary

```bash
GET /fathom/external/v1/recordings/{recording_id}/summary
```

Query parameters:
- `destination_url` - Optional URL for async callback. If provided, the summary will be POSTed to this URL.

**Synchronous example:**

```bash
curl -s -X GET 'https://gateway.maton.ai/fathom/external/v1/recordings/123456789/summary' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response:**
```json
{
  "summary": {
    "template_name": "general",
    "markdown_formatted": "## Summary\n\nWe reviewed Q1 OKRs, identified budget risks, and agreed to revisit projections next month."
  }
}
```

**Async example:**

```bash
curl -s -X GET 'https://gateway.maton.ai/fathom/external/v1/recordings/123456789/summary?destination_url=https://example.com/webhook' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

#### Get Transcript

```bash
GET /fathom/external/v1/recordings/{recording_id}/transcript
```

Query parameters:
- `destination_url` - Optional URL for async callback. If provided, the transcript will be POSTed to this URL.

**Synchronous example:**

```bash
curl -s -X GET 'https://gateway.maton.ai/fathom/external/v1/recordings/123456789/transcript' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response:**
```json
{
  "transcript": [
    {
      "speaker": {
        "display_name": "Alice Johnson",
        "matched_calendar_invitee_email": "alice.johnson@acme.com"
      },
      "text": "Let's revisit the budget allocations.",
      "timestamp": "00:05:32"
    }
  ]
}
```

### Teams

#### List Teams

```bash
GET /fathom/external/v1/teams
```

Query parameters:
- `cursor` - Cursor for pagination

**Example:**

```bash
curl -s -X GET 'https://gateway.maton.ai/fathom/external/v1/teams' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response:**
```json
{
  "limit": 25,
  "next_cursor": null,
  "items": [
    {
      "name": "Sales",
      "created_at": "2023-11-10T12:00:00Z"
    }
  ]
}
```

### Team Members

#### List Team Members

```bash
GET /fathom/external/v1/team_members
```

Query parameters:
- `cursor` - Cursor for pagination
- `team` - Team name to filter by

**Example:**

```bash
curl -s -X GET 'https://gateway.maton.ai/fathom/external/v1/team_members?team=Sales' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response:**
```json
{
  "limit": 25,
  "next_cursor": null,
  "items": [
    {
      "name": "Bob Lee",
      "email": "bob.lee@acme.com",
      "created_at": "2024-06-01T08:30:00Z"
    }
  ]
}
```

### Webhooks

#### Create Webhook

```bash
POST /fathom/external/v1/webhooks
Content-Type: application/json

{
  "destination_url": "https://example.com/webhook",
  "triggered_for": ["my_recordings", "my_shared_with_team_recordings"],
  "include_transcript": true,
  "include_summary": true,
  "include_action_items": true,
  "include_crm_matches": false
}
```

**triggered_for options:**
- `my_recordings` - Your private recordings (excludes those shared with teams on Team Plans)
- `shared_external_recordings` - Recordings shared with you by other users
- `my_shared_with_team_recordings` - (Team Plans) Recordings you've shared with teams
- `shared_team_recordings` - (Team Plans) Recordings from other users on your Team Plan

At least one of `include_transcript`, `include_summary`, `include_action_items`, or `include_crm_matches` must be true.

**Example:**

```bash
curl -s -X POST 'https://gateway.maton.ai/fathom/external/v1/webhooks' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{
    "destination_url": "https://example.com/webhook",
    "triggered_for": ["my_recordings"],
    "include_summary": true
  }'
```

**Response:**
```json
{
  "id": "ikEoQ4bVoq4JYUmc",
  "url": "https://example.com/webhook",
  "secret": "whsec_x6EV6NIAAz3ldclszNJTwrow",
  "created_at": "2025-06-30T10:40:46Z",
  "include_transcript": false,
  "include_crm_matches": false,
  "include_summary": true,
  "include_action_items": false,
  "triggered_for": ["my_recordings"]
}
```

#### Delete Webhook

```bash
DELETE /fathom/external/v1/webhooks/{id}
```

**Example:**

```bash
curl -s -X DELETE 'https://gateway.maton.ai/fathom/external/v1/webhooks/ikEoQ4bVoq4JYUmc' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

Returns `204 No Content` on success.

## Pagination

Use `cursor` for pagination. Response includes `next_cursor` when more results exist:

```bash
curl -s -X GET 'https://gateway.maton.ai/fathom/external/v1/meetings?cursor=eyJwYWdlX251bSI6Mn0=' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/fathom/external/v1/meetings?created_after=2025-01-01T00:00:00Z',
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
    'https://gateway.maton.ai/fathom/external/v1/meetings',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'created_after': '2025-01-01T00:00:00Z'}
)
data = response.json()
```

## Notes

- Recording IDs are integers
- Timestamps are in ISO 8601 format
- Transcripts and summaries are in English
- Webhook secrets are used to verify webhook signatures
- CRM matches only return data from your or your team's linked CRM

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Bad request or missing Fathom connection |
| 401 | Invalid or missing Maton API key |
| 404 | Resource not found |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Fathom API |

## Resources

- [Fathom API Documentation](https://developers.fathom.ai)
- [LLM Reference](https://developers.fathom.ai/llms.txt)
