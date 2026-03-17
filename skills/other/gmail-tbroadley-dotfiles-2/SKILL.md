---
name: gmail
description: Read and search Gmail emails. Check inbox, search messages, and view email threads.
---

# Gmail Integration

This skill provides read access to Gmail via the Gmail API.

## Setup Required

Uses OAuth with persistent refresh token (same setup for Calendar, Gmail, Drive).

**One-time setup:**
```bash
google-oauth-setup <path-to-client-secret.json>
```

See `claude/skills/SETUP.md` for detailed OAuth setup instructions.

**Get Access Token (auto-refreshes):**
```bash
ACCESS_TOKEN=$(google-oauth-token)
```

**Required header for all requests:**
```bash
-H "x-goog-user-project: ${GOOGLE_QUOTA_PROJECT}"
```

## When to Use

Use this skill when the user:
- Asks about their email or inbox
- Wants to search for emails
- Needs to find a specific message
- Asks about recent emails
- Mentions "Gmail" or email

## API Endpoints

Base URL: `https://gmail.googleapis.com/gmail/v1/users/me`

### List Messages

**List Recent Messages**:
```bash
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

**List with Query**:
```bash
curl -s -G "https://gmail.googleapis.com/gmail/v1/users/me/messages" \
  --data-urlencode "q=is:unread" \
  --data-urlencode "maxResults=20" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Get Message

**Get Full Message**:
```bash
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages/{MESSAGE_ID}?format=full" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

**Get Metadata Only** (faster):
```bash
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages/{MESSAGE_ID}?format=metadata" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Get Thread

**Get Full Thread**:
```bash
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/threads/{THREAD_ID}?format=full" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Labels

**List Labels**:
```bash
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/labels" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Profile

**Get Profile Info**:
```bash
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/profile" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

## Gmail Search Query Syntax

Use the `q` parameter with Gmail search syntax:

| Query | Description |
|-------|-------------|
| `is:unread` | Unread messages |
| `is:starred` | Starred messages |
| `from:user@example.com` | From specific sender |
| `to:user@example.com` | To specific recipient |
| `subject:hello` | Subject contains "hello" |
| `has:attachment` | Has attachments |
| `filename:pdf` | Has PDF attachment |
| `after:2024/01/01` | After date |
| `before:2024/01/31` | Before date |
| `newer_than:7d` | Last 7 days |
| `older_than:1m` | Older than 1 month |
| `label:work` | Has label |
| `in:inbox` | In inbox |
| `in:sent` | In sent |

Combine queries: `from:boss@company.com subject:urgent after:2024/01/01`

## Common Workflows

### Check Unread Emails
```bash
ACCESS_TOKEN=$(google-oauth-token)

curl -s -G "https://gmail.googleapis.com/gmail/v1/users/me/messages" \
  --data-urlencode "q=is:unread" \
  --data-urlencode "maxResults=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Search for Emails from Someone
```bash
curl -s -G "https://gmail.googleapis.com/gmail/v1/users/me/messages" \
  --data-urlencode "q=from:colleague@company.com newer_than:7d" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Read a Specific Email
```bash
# Get message list first, then fetch specific message
MESSAGE_ID="18d1234567890abc"
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages/${MESSAGE_ID}?format=full" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq '{
    subject: .payload.headers[] | select(.name == "Subject") | .value,
    from: .payload.headers[] | select(.name == "From") | .value,
    snippet: .snippet
  }'
```

### Get Recent Important Emails
```bash
curl -s -G "https://gmail.googleapis.com/gmail/v1/users/me/messages" \
  --data-urlencode "q=is:important newer_than:1d" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

## Extracting Message Content

Email bodies are base64 encoded. To decode:
```bash
# For simple text/plain messages
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages/${MESSAGE_ID}?format=full" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq -r '.payload.body.data' | base64 -d

# For multipart messages, find the text/plain part
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages/${MESSAGE_ID}?format=full" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq -r '.payload.parts[] | select(.mimeType == "text/plain") | .body.data' | base64 -d
```

## Extracting Headers

Common headers to extract:
```bash
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages/${MESSAGE_ID}?format=metadata" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq '.payload.headers[] | select(.name | IN("From", "To", "Subject", "Date"))'
```

## Notes

- Access tokens expire after 1 hour; use refresh token to get new ones
- Message format options: `minimal`, `metadata`, `raw`, `full`
- Gmail API has quotas (250 quota units/user/second)
- The `snippet` field gives a preview without needing to decode the body
- Thread IDs group related messages together
