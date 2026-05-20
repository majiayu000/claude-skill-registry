---
name: pilt
description: Access Pilt fundraising data -- investor matches, campaign stats, outreach events, and deck analysis.
metadata: {"openclaw":{"requires":{"env":["PILT_API_KEY"],"bins":["curl"]},"primaryEnv":"PILT_API_KEY","emoji":"🦞","homepage":"https://pilt.ai"}}
---

# Pilt API Skill

You can retrieve fundraising data from Pilt using curl. All requests go to a single endpoint and require your personal API key.

## Endpoint

```
POST https://pilt.ai/api/v1/gateway
```

## Required Headers

Every request must include these two headers:

- `Content-Type: application/json`
- `x-pilt-api-key: $PILT_API_KEY`

## Security

All authorization is performed exclusively via your personal `x-pilt-api-key`. The gateway validates your key server-side against a hashed key store and scopes every response to your account. No other credentials are required.

## Request Body

JSON object with a mandatory `action` field. Supported actions: `get_matches`, `get_campaign_stats`, `get_campaign_events`, `get_analysis`.

## Actions

### get_matches

Returns matched investors with fit scores from the user's latest deck analysis.

```bash
curl -s -X POST \
  https://pilt.ai/api/v1/gateway \
  -H "Content-Type: application/json" \
  -H "x-pilt-api-key: $PILT_API_KEY" \
  -d '{"action": "get_matches"}'
```

### get_campaign_stats

Returns aggregated email outreach statistics: queued, sent, opened, and replied counts.

```bash
curl -s -X POST \
  https://pilt.ai/api/v1/gateway \
  -H "Content-Type: application/json" \
  -H "x-pilt-api-key: $PILT_API_KEY" \
  -d '{"action": "get_campaign_stats"}'
```

### get_campaign_events

Returns a per-investor event log with timestamps (e.g. sent, opened, replied).

```bash
curl -s -X POST \
  https://pilt.ai/api/v1/gateway \
  -H "Content-Type: application/json" \
  -H "x-pilt-api-key: $PILT_API_KEY" \
  -d '{"action": "get_campaign_events"}'
```

### get_analysis

Returns the deck analysis summary: score, industry, stage, and one-liner.

```bash
curl -s -X POST \
  https://pilt.ai/api/v1/gateway \
  -H "Content-Type: application/json" \
  -H "x-pilt-api-key: $PILT_API_KEY" \
  -d '{"action": "get_analysis"}'
```

## Error Handling

| Status | Meaning |
|--------|---------|
| 401 | Missing or invalid `x-pilt-api-key` header (must start with `pilt_sk_`) |
| 403 | API key not found or revoked |
| 400 | Missing or unsupported `action` field |
| 413 | Request body exceeds 10KB limit |
| 503 | API gateway is not yet configured on the server side |

## User Setup

Store your Pilt API key so it is available as the `PILT_API_KEY` environment variable. In OpenClaw, add it to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "pilt": {
        "enabled": true,
        "apiKey": "pilt_sk_..."
      }
    }
  }
}
```

The API key can be generated in the Pilt dashboard under Settings → API Keys.
