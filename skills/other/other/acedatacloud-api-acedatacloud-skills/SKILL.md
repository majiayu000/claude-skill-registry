---
name: acedatacloud-api
description: Guide for using AceDataCloud APIs. Use when authenticating, making API calls, managing credentials, understanding billing, or integrating AceDataCloud services into applications. Covers setup, authentication, request patterns, error handling, and SDK integration.
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
compatibility: Requires an AceDataCloud account at platform.acedata.cloud.
---

# AceDataCloud API Usage Guide

Complete guide for using AceDataCloud's AI-powered data services API.

## Getting Started

### 1. Create an Account

Register at [platform.acedata.cloud](https://platform.acedata.cloud).

### 2. Subscribe to a Service

Browse available services and click **Get** to subscribe. Most services include free quota.

### 3. Create API Credentials

Go to your service's **Credentials** page and create an API Token.

## Authentication

All APIs use Bearer token authentication:

```bash
curl -X POST https://api.acedata.cloud/<endpoint> \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

### Token Types

| Type | Format | Scope |
|------|--------|-------|
| **Service Token** | UUID string | Access to subscribed service only |
| **Global Token** | UUID string | Access to all subscribed services |

## Base URL

```
https://api.acedata.cloud
```

## SDK Integration (OpenAI-Compatible)

For chat completion services, use the standard OpenAI SDK:

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_TOKEN",
    base_url="https://api.acedata.cloud/v1"
)

response = client.chat.completions.create(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: "YOUR_API_TOKEN",
  baseURL: "https://api.acedata.cloud/v1"
});

const response = await client.chat.completions.create({
  model: "gpt-4.1",
  messages: [{ role: "user", content: "Hello!" }]
});
```

## Common Request Patterns

### Synchronous APIs

Some APIs return results immediately (e.g., face transform, search):

```bash
curl -X POST https://api.acedata.cloud/face/analyze \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/photo.jpg"}'
```

### Async Task APIs

Most generation APIs (images, video, music) are asynchronous:

**Step 1:** Submit request

```json
POST /suno/audios
{"prompt": "a jazz song", "wait": false}
→ {"task_id": "abc123"}
```

**Step 2:** Poll for results

```json
POST /suno/tasks
{"task_id": "abc123"}
→ {"state": "succeeded", "data": [...]}
```

**Shortcut:** Pass `"wait": true` to block until completion (simpler but longer timeout).

## Error Handling

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 400 | Bad request | Check request parameters |
| 401 | Unauthorized | Check API token |
| 403 | Forbidden | Content filtered or insufficient permissions |
| 429 | Rate limited | Wait and retry with backoff |
| 500 | Server error | Retry or contact support |

Error response format:

```json
{
  "error": {
    "code": "token_mismatched",
    "message": "Invalid or expired token"
  }
}
```

## Billing

- Each API call deducts from your **subscription balance** (remaining_amount)
- Cost varies by service, model, and usage (tokens, requests, data size)
- Check balance at [platform.acedata.cloud](https://platform.acedata.cloud)
- Most services offer free trial quota

## Service Categories

| Category | Services | Base Path |
|----------|----------|-----------|
| **AI Chat** | GPT, Claude, Gemini, DeepSeek, Grok | `/v1/chat/completions` |
| **Image Gen** | Midjourney, Flux, Seedream, NanoBanana | `/midjourney/*`, `/flux/*`, etc. |
| **Video Gen** | Luma, Sora, Veo, Kling, Hailuo, Seedance | `/luma/*`, `/sora/*`, etc. |
| **Music Gen** | Suno, Producer, Fish Audio | `/suno/*`, `/producer/*`, `/fish/*` |
| **Search** | Google Search (web/images/news/maps) | `/serp/*` |
| **Face** | Analyze, beautify, swap, cartoon, age | `/face/*` |
| **Utility** | Short URL, QR Art, Headshots | `/short-url`, `/qrart/*`, `/headshots/*` |

## Gotchas

- Tokens are **service-scoped** by default — create a global token if you need cross-service access
- Async APIs return a `task_id` — you must poll to get the result
- `wait: true` is convenient but has a timeout limit (typically 60–120s)
- Rate limits vary by service tier — upgrade your plan if hitting limits
- All timestamps are in UTC
