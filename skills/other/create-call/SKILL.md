---
name: create-call
description: Create outbound phone calls, web calls, and batch calls using the Vapi API. Use when making automated calls, testing voice assistants, scheduling call campaigns, or initiating conversations programmatically.
license: MIT
compatibility: Requires internet access and a Vapi API key (VAPI_API_KEY).
metadata:
  author: vapi
  version: "1.0"
---

# Vapi Call Creation

Initiate outbound phone calls, web calls, and batch calls using Vapi's API. Connect your voice assistants to real phone numbers and test them programmatically.

> **Setup:** Ensure `VAPI_API_KEY` is set. See the `setup-api-key` skill if needed.

## Quick Start — Outbound Phone Call

### cURL

```bash
curl -X POST https://api.vapi.ai/call \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "your-assistant-id",
    "phoneNumberId": "your-phone-number-id",
    "customer": {
      "number": "+11234567890"
    }
  }'
```

### TypeScript (Server SDK)

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const vapi = new VapiClient({ token: process.env.VAPI_API_KEY! });

const call = await vapi.calls.create({
  assistantId: "your-assistant-id",
  phoneNumberId: "your-phone-number-id",
  customer: {
    number: "+11234567890",
  },
});

console.log("Call created:", call.id);
```

### Python

```python
import requests
import os

response = requests.post(
    "https://api.vapi.ai/call",
    headers={
        "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "assistantId": "your-assistant-id",
        "phoneNumberId": "your-phone-number-id",
        "customer": {"number": "+11234567890"},
    },
)

call = response.json()
print(f"Call initiated: {call['id']}")
```

## Call Types

### Outbound Phone Call

Requires an assistant, a Vapi phone number, and a customer number.

```json
{
  "assistantId": "assistant-id",
  "phoneNumberId": "phone-number-id",
  "customer": {
    "number": "+11234567890",
    "name": "John Doe",
    "numberE164CheckEnabled": true
  }
}
```

### Web Call

For browser-based calls — no phone number needed. Use the Vapi Web SDK on the client side.

```json
{
  "assistantId": "assistant-id"
}
```

Client-side (JavaScript):
```javascript
import Vapi from "@vapi-ai/web";

const vapi = new Vapi("your-public-key");
vapi.start("your-assistant-id");
```

### Transient Assistant Call

Define an assistant inline instead of referencing a saved one:

```json
{
  "assistant": {
    "name": "Quick Test",
    "firstMessage": "Hello! This is a test call.",
    "model": {
      "provider": "openai",
      "model": "gpt-4.1",
      "messages": [
        {
          "role": "system",
          "content": "You are a test assistant. Confirm the call is working and end politely."
        }
      ]
    },
    "voice": { "provider": "vapi", "voiceId": "Elliot" },
    "transcriber": { "provider": "deepgram", "model": "nova-3", "language": "en" }
  },
  "phoneNumberId": "phone-number-id",
  "customer": {
    "number": "+11234567890"
  }
}
```

## Scheduled Calls

Schedule a call for a future time:

```json
{
  "assistantId": "assistant-id",
  "phoneNumberId": "phone-number-id",
  "customer": {
    "number": "+11234567890"
  },
  "schedulePlan": {
    "earliestAt": "2025-06-15T14:00:00Z",
    "latestAt": "2025-06-15T15:00:00Z"
  }
}
```

- `earliestAt` — Earliest time to attempt the call (ISO 8601)
- `latestAt` — Latest time to attempt the call (optional)
- If using `assistantId`, the latest version of the assistant is used at call time
- For a fixed assistant config, use `assistant` (transient) instead

## Batch Calls

Call multiple numbers in one request:

```json
{
  "assistantId": "assistant-id",
  "phoneNumberId": "phone-number-id",
  "customers": [
    { "number": "+11234567890", "name": "Alice" },
    { "number": "+10987654321", "name": "Bob" },
    { "number": "+15551234567", "name": "Carol" }
  ]
}
```

Combine with `schedulePlan` for scheduled batch calls.

## Call with Metadata

Pass custom data accessible during the call:

```json
{
  "assistantId": "assistant-id",
  "phoneNumberId": "phone-number-id",
  "customer": {
    "number": "+11234567890"
  },
  "metadata": {
    "orderId": "ORD-12345",
    "department": "billing"
  }
}
```

## Managing Calls

```bash
# List calls
curl "https://api.vapi.ai/call?limit=10" \
  -H "Authorization: Bearer $VAPI_API_KEY"

# Get a specific call
curl https://api.vapi.ai/call/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"

# Get call with transcript and recording
curl https://api.vapi.ai/call/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
# Response includes: transcript, recordingUrl, summary, costBreakdown

# Delete a call
curl -X DELETE https://api.vapi.ai/call/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

## Call Response

A successful call creation returns:

```json
{
  "id": "call-uuid",
  "orgId": "org-uuid",
  "type": "outboundPhoneCall",
  "status": "queued",
  "assistantId": "assistant-id",
  "phoneNumberId": "phone-number-id",
  "customer": {
    "number": "+11234567890"
  },
  "createdAt": "2025-01-15T10:00:00Z"
}
```

Call statuses: `queued` → `ringing` → `in-progress` → `ended`

## Compliance Warning

It is a violation of FCC law to dial phone numbers without consent in an automated manner. Review TCPA consent requirements before launching automated call campaigns.

## References

- [Vapi Outbound Calls Docs](https://docs.vapi.ai/calls/outbound-calling)
- [Call Features](https://docs.vapi.ai/calls/call-features)
- [Voicemail Detection](https://docs.vapi.ai/calls/voicemail-detection)

## Additional Resources

This skills repository includes a **Vapi documentation MCP server** (`vapi-docs`) that gives your AI agent access to the full Vapi knowledge base. Use the `searchDocs` tool to look up anything beyond what this skill covers — advanced configuration, troubleshooting, SDK details, and more.

**Auto-configured:** If you cloned or installed these skills, the MCP server is already configured via `.mcp.json` (Claude Code), `.cursor/mcp.json` (Cursor), or `.vscode/mcp.json` (VS Code Copilot).

**Manual setup:** If your agent doesn't auto-detect the config, run:
```bash
claude mcp add vapi-docs -- npx -y mcp-remote https://docs.vapi.ai/_mcp/server
```

See the [README](../README.md#vapi-documentation-server-mcp) for full setup instructions across all supported agents.
