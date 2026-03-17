---
name: setup-webhook
description: Configure Vapi server URLs and webhooks to receive real-time call events, transcripts, tool calls, and end-of-call reports. Use when setting up webhook endpoints, building tool servers, or integrating Vapi events into your application.
license: MIT
compatibility: Requires internet access and a Vapi API key (VAPI_API_KEY).
metadata:
  author: vapi
  version: "1.0"
---

# Vapi Webhook / Server URL Setup

Configure server URLs to receive real-time events from Vapi during calls — transcripts, tool calls, status changes, and end-of-call reports.

> **Setup:** Ensure `VAPI_API_KEY` is set. See the `setup-api-key` skill if needed.

## Overview

Vapi uses "Server URLs" (webhooks) to communicate with your application. Unlike traditional one-way webhooks, Vapi server URLs support bidirectional communication — your server can respond with data that affects the call.

## Where to Set Server URLs

### On an Assistant

```bash
curl -X PATCH https://api.vapi.ai/assistant/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "serverUrl": "https://your-server.com/vapi/webhook",
    "serverUrlSecret": "your-webhook-secret"
  }'
```

### On a Phone Number

```bash
curl -X PATCH https://api.vapi.ai/phone-number/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "serverUrl": "https://your-server.com/vapi/webhook"
  }'
```

### At the Organization Level

Set a default server URL in the Vapi Dashboard under **Settings > Server URL**.

Priority order: Tool server URL > Assistant server URL > Phone Number server URL > Organization server URL.

## Event Types

| Event | Description | Expects Response? |
|-------|-------------|-------------------|
| `assistant-request` | Request for dynamic assistant config | Yes — return assistant config |
| `tool-calls` | Assistant is calling a tool | Yes — return tool results |
| `status-update` | Call status changed | No |
| `transcript` | Real-time transcript update | No |
| `end-of-call-report` | Call completed with summary | No |
| `hang` | Assistant failed to respond | No |
| `speech-update` | Speech activity detected | No |

## Webhook Server Example (Express.js)

```typescript
import express from "express";
import crypto from "crypto";

const app = express();
app.use(express.json());

app.post("/vapi/webhook", (req, res) => {
  const { message } = req.body;

  switch (message.type) {
    case "assistant-request":
      // Dynamically configure the assistant based on the caller
      res.json({
        assistant: {
          name: "Dynamic Assistant",
          firstMessage: `Hello ${message.call.customer?.name || "there"}!`,
          model: {
            provider: "openai",
            model: "gpt-4.1",
            messages: [
              { role: "system", content: "You are a helpful assistant." },
            ],
          },
          voice: { provider: "vapi", voiceId: "Elliot" },
          transcriber: { provider: "deepgram", model: "nova-3", language: "en" },
        },
      });
      break;

    case "tool-calls":
      // Handle tool calls from the assistant
      const results = message.toolCallList.map((toolCall: any) => ({
        toolCallId: toolCall.id,
        result: handleToolCall(toolCall.name, toolCall.arguments),
      }));
      res.json({ results });
      break;

    case "end-of-call-report":
      // Process the call report
      console.log("Call ended:", {
        callId: message.call.id,
        duration: message.durationSeconds,
        cost: message.cost,
        summary: message.summary,
        transcript: message.transcript,
      });
      res.json({});
      break;

    case "status-update":
      console.log("Call status:", message.status);
      res.json({});
      break;

    case "transcript":
      console.log(`[${message.role}]: ${message.transcript}`);
      res.json({});
      break;

    default:
      res.json({});
  }
});

function handleToolCall(name: string, args: any): string {
  // Implement your tool logic here
  return `Result for ${name}`;
}

app.listen(3000, () => console.log("Webhook server running on port 3000"));
```

## Webhook Server Example (Python / Flask)

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/vapi/webhook", methods=["POST"])
def vapi_webhook():
    data = request.json
    message = data.get("message", {})
    msg_type = message.get("type")

    if msg_type == "assistant-request":
        return jsonify({
            "assistant": {
                "name": "Dynamic Assistant",
                "firstMessage": "Hello! How can I help?",
                "model": {
                    "provider": "openai",
                    "model": "gpt-4.1",
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."}
                    ],
                },
                "voice": {"provider": "vapi", "voiceId": "Elliot"},
                "transcriber": {"provider": "deepgram", "model": "nova-3", "language": "en"},
            }
        })

    elif msg_type == "tool-calls":
        results = []
        for tool_call in message.get("toolCallList", []):
            results.append({
                "toolCallId": tool_call["id"],
                "result": f"Handled {tool_call['name']}",
            })
        return jsonify({"results": results})

    elif msg_type == "end-of-call-report":
        print(f"Call ended: {message['call']['id']}")
        print(f"Summary: {message.get('summary')}")

    return jsonify({})

if __name__ == "__main__":
    app.run(port=3000)
```

## Webhook Authentication

Verify webhook authenticity using the secret:

```typescript
function verifyWebhook(req: express.Request, secret: string): boolean {
  const signature = req.headers["x-vapi-signature"] as string;
  if (!signature || !secret) return false;

  const payload = JSON.stringify(req.body);
  const expected = crypto
    .createHmac("sha256", secret)
    .update(payload)
    .digest("hex");

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  );
}
```

## Local Development

Use the Vapi CLI to forward webhooks to your local server:

```bash
# Install the CLI
curl -sSL https://vapi.ai/install.sh | bash

# Forward events to local server
vapi listen --forward-to localhost:3000/vapi/webhook
```

Or use ngrok:

```bash
ngrok http 3000
# Copy the ngrok URL and set it as your server URL
```

## End-of-Call Report Fields

The `end-of-call-report` event includes:

| Field | Description |
|-------|-------------|
| `call` | Full call object with metadata |
| `transcript` | Complete conversation transcript |
| `summary` | AI-generated call summary |
| `recordingUrl` | URL to the call recording |
| `durationSeconds` | Call duration |
| `cost` | Total call cost |
| `costBreakdown` | Breakdown by component (STT, LLM, TTS, transport) |
| `messages` | Array of all conversation messages |

## References

- [Server URL Events](references/webhook-events.md) — All event types with payload schemas
- [Vapi Server URL Docs](https://docs.vapi.ai/server-url) — Official documentation
- [Local Development](https://docs.vapi.ai/server-url/developing-locally) — Testing webhooks locally

## Additional Resources

This skills repository includes a **Vapi documentation MCP server** (`vapi-docs`) that gives your AI agent access to the full Vapi knowledge base. Use the `searchDocs` tool to look up anything beyond what this skill covers — advanced configuration, troubleshooting, SDK details, and more.

**Auto-configured:** If you cloned or installed these skills, the MCP server is already configured via `.mcp.json` (Claude Code), `.cursor/mcp.json` (Cursor), or `.vscode/mcp.json` (VS Code Copilot).

**Manual setup:** If your agent doesn't auto-detect the config, run:
```bash
claude mcp add vapi-docs -- npx -y mcp-remote https://docs.vapi.ai/_mcp/server
```

See the [README](../README.md#vapi-documentation-server-mcp) for full setup instructions across all supported agents.
