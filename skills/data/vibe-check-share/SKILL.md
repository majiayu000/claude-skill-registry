---
name: share-session
description: Create a public share link for the current Claude Code session. Use when user says "share session", "share this session", "get share link", "create share link", or "share my work".
---

# Share Current Session

**Purpose:** Create a public share link for the current Claude Code session so users can share their conversation with friends.

---

## Overview

This skill:
1. Gets the current session ID (using the marker technique)
2. Reads the API key from vibe-check config
3. Calls the vibecheck API to create a public share
4. Displays the shareable URL

---

## Execution Steps

### Step 1: Generate and Emit Session Marker

Generate a unique marker string:
```
VIBE_SESSION_MARKER_[random 16 character hex string]
```

**IMPORTANT:** Output this marker directly in your response:

```
Creating share link for this session...
Session marker: VIBE_SESSION_MARKER_[your-generated-marker]
```

### Step 2: Wait for Logging

Wait 2 seconds for vibe-check to log the marker:

```bash
sleep 2
```

### Step 3: Get Session ID from Database

Query the local SQLite database to find the session ID:

```bash
sqlite3 "file:$HOME/.vibe-check/vibe_check.db?mode=ro" \
  "SELECT event_session_id FROM conversation_events WHERE event_data LIKE '%VIBE_SESSION_MARKER_[your-marker]%' ORDER BY inserted_at DESC LIMIT 1;"
```

Replace `[your-marker]` with the actual marker you generated.

Save the result as `SESSION_ID`.

### Step 4: Get API Configuration

Read the API key and URL from the vibe-check config:

```bash
# Get API key
cat ~/.vibe-check/config.json | jq -r '.api.api_key'

# Get API URL (defaults to https://vibecheck.wanderingstan.com)
cat ~/.vibe-check/config.json | jq -r '.api.url // "https://vibecheck.wanderingstan.com"'
```

### Step 5: Create the Share

Make the API call to create a public session share:

```bash
curl -s -X POST "${API_URL}/api/shares" \
  -H "X-API-Key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"scope_type\": \"session\",
    \"scope_session_id\": \"${SESSION_ID}\",
    \"visibility\": \"public\"
  }"
```

The response will include:
```json
{
  "status": "ok",
  "share_id": 123,
  "share_token": "7Kx9mPqR2vL...",
  "share_url": "https://vibecheck.wanderingstan.com/s/7Kx9mPqR2vL...",
  "slug": null
}
```

### Step 6: Display the Share URL

Present the share URL prominently to the user:

```
Session Share Created!

Share URL: https://vibecheck.wanderingstan.com/s/[token]

Anyone with this link can view your conversation from this session.
```

---

## Complete Script

Here's the full sequence (run each step, substituting your values):

```bash
# Step 1: Generate marker (do this in your head, output it in response)
# Example: VIBE_SESSION_MARKER_a7f3b2c9e4d1f8a6

# Step 2: Wait
sleep 2

# Step 3: Get session ID
SESSION_ID=$(sqlite3 "file:$HOME/.vibe-check/vibe_check.db?mode=ro" \
  "SELECT event_session_id FROM conversation_events WHERE event_data LIKE '%VIBE_SESSION_MARKER_a7f3b2c9e4d1f8a6%' ORDER BY inserted_at DESC LIMIT 1;")

# Step 4: Get config
API_KEY=$(cat ~/.vibe-check/config.json | jq -r '.api.api_key')
API_URL=$(cat ~/.vibe-check/config.json | jq -r '.api.url // "https://vibecheck.wanderingstan.com"')

# Step 5: Create share
curl -s -X POST "${API_URL}/api/shares" \
  -H "X-API-Key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"scope_type\": \"session\",
    \"scope_session_id\": \"${SESSION_ID}\",
    \"visibility\": \"public\"
  }"
```

---

## Troubleshooting

### "Cannot share content you do not own"

This means the session ID doesn't have any events owned by this user. Possible causes:
- vibe-check isn't running or hasn't synced to the remote API yet
- The API key belongs to a different user
- The session is too new and hasn't been synced

**Fix:** Run `vibe-check status` to check if remote sync is working.

### "No session ID found"

The marker wasn't logged. Possible causes:
- vibe-check monitor isn't running
- Database path is different

**Fix:** Check `vibe-check status` to verify the monitor is running and get the correct database path.

### "Not authenticated"

No API key found in config.

**Fix:** Run `vibe-check auth login` to authenticate.

---

## Advanced Options

You can customize the share by adding optional fields:

```bash
curl -s -X POST "${API_URL}/api/shares" \
  -H "X-API-Key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"scope_type\": \"session\",
    \"scope_session_id\": \"${SESSION_ID}\",
    \"visibility\": \"public\",
    \"title\": \"My awesome coding session\",
    \"description\": \"Building a feature with Claude\",
    \"slug\": \"my-cool-session\"
  }"
```

With a slug, the URL becomes: `https://vibecheck.wanderingstan.com/s/my-cool-session`
