---
name: akhrot
description: Use Akhrot APIs to manage OAuth tokens and API keys for external services (Gmail, GitHub, Slack, OpenAI, Stripe, etc.). Check connections, fetch tokens, create OAuth sessions, then call provider APIs directly.
---
# Akhrot - OAuth & API Key Integration Skill

You have access to Akhrot, an OAuth-as-a-Service platform that manages OAuth tokens and API keys for external services. Your API key identifies the user account — all connections are tied to this key.

## Architecture

Akhrot manages credentials only. You:
1. Fetch credentials from Akhrot (tokens or API keys)
2. Call provider APIs directly (Gmail API, GitHub API, Slack, etc.)

Base URL: `https://akhrot.ai` (or user's Akhrot instance). All requests use header: `Authorization: Bearer {Akhrot_API_KEY}`.

## Quick Start

### Step 1: Check connection status (lightweight)

```bash
curl -s -H "Authorization: Bearer {Akhrot_API_KEY}" "https://akhrot.ai/ai/context/summary"
```

Returns which providers are connected and available services (~500 bytes).

### Step 2: Get provider or service details (when needed)

```bash
# One provider
curl -s -H "Authorization: Bearer {Akhrot_API_KEY}" "https://akhrot.ai/ai/context/google"

# One service
curl -s -H "Authorization: Bearer {Akhrot_API_KEY}" "https://akhrot.ai/ai/context/google/gmail"
```

### Step 3: Fetch token for connected provider

```bash
curl -s -X POST "https://akhrot.ai/tokens/fetch" \
  -H "Authorization: Bearer {Akhrot_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"provider": "google"}'
```

Returns `accessToken` (and for Telegram MTProto: `apiId`, `apiHash`, `type: "mtproto"`). Tokens auto-refresh when expired.

### Step 4: Create OAuth session (for new connections)

If the user has not connected a provider yet:

```bash
curl -s -X POST "https://akhrot.ai/oauth/sessions" \
  -H "Authorization: Bearer {Akhrot_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"provider": "google"}'
```

Response includes `url`. Send the user to that URL to authorize; after they finish, the provider is connected.

### Step 5: Call provider API directly

Use the token with the provider's native API:

```bash
# Gmail
curl -s -H "Authorization: Bearer {accessToken}" \
  "https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=10"

# GitHub
curl -s -H "Authorization: Bearer {accessToken}" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/user/repos"
```

## Available Providers

Use the `provider` code in `/tokens/fetch` and `/oauth/sessions`.

| Provider | Code | Token Type | Use Cases |
|----------|------|------------|-----------|
| Google | `google` | OAuth Bearer | Gmail, Drive, Calendar, Sheets |
| MongoDB | `mongodb` | API Key | Database |
| Supabase | `supabase` | API Key | Database |
| Railway | `railway` | API Key | Database / services |
| ElevenLabs | `elevenlabs` | API Key | Voice, TTS |
| Typefully | `typefully` | API Key | Content, Drafts |
| OpenAI | `openai` | API Key | GPT, DALL-E, Embeddings |
| Twilio | `twilio` | API Key | SMS, Voice, Video |
| Stripe | `stripe` | API Key | Payments, Billing |
| SendGrid | `sendgrid` | API Key | Email |
| Anthropic | `anthropic` | API Key | Claude |
| Replicate | `replicate` | API Key | ML Models |
| Cloudflare | `cloudflare` | API Key | DNS, CDN |
| Cohere | `cohere` | API Key | NLP |
| Postmark | `postmark` | API Key | Email |
| Mailgun | `mailgun` | API Key | Email |
| PagerDuty | `pagerduty` | API Key | Incidents |
| Vercel | `vercel` | API Key | Deployments |

## Key points

- **API key = user identity.** No userId; the Akhrot API key identifies the user.
- **Token auto-refresh.** Expired OAuth tokens are refreshed automatically on `/tokens/fetch`.
- **Direct API calls.** You call provider APIs directly; Akhrot only stores and returns credentials.
- **User must authorize.** For OAuth, users must complete the flow at the URL from `/oauth/sessions`; you cannot authorize for them.
- **Telegram is special.** Uses MTProto. Response includes `accessToken` (session string), `apiId`, `apiHash`. Use with gramjs (JS) or telethon (Python).

## Error codes

| Code | HTTP | Meaning |
|------|------|--------|
| UNAUTHORIZED | 401 | Invalid or missing API key |
| INTEGRATION_NOT_FOUND | 404 | User has not connected this provider |
| TOKEN_EXPIRED | 400 | Token expired, no refresh token |
| SESSION_EXPIRED | 400 | OAuth session expired (e.g. 10 min) |
| RATE_LIMITED | 429 | Too many requests |

## Live skill document

For the latest version from the Akhrot server:

```bash
GET https://akhrot.ai/ai/skill
```

(No auth required; returns markdown.)
