---
name: create-tool
description: Create custom tools for Vapi voice assistants including function tools, API request tools, transfer call tools, end call tools, and integrations with Google Calendar, Sheets, Slack, and more. Use when adding capabilities to voice agents, building tool servers, or integrating external APIs.
license: MIT
compatibility: Requires internet access and a Vapi API key (VAPI_API_KEY).
metadata:
  author: vapi
  version: "1.0"
---

# Vapi Tool Creation

Create tools that give voice assistants the ability to take actions during calls — look up data, book appointments, transfer calls, send messages, and more.

> **Setup:** Ensure `VAPI_API_KEY` is set. See the `setup-api-key` skill if needed.

## Quick Start

### Create a Function Tool (cURL)

```bash
curl -X POST https://api.vapi.ai/tool \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Get current weather for a location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "City name, e.g. San Francisco"
          }
        },
        "required": ["location"]
      }
    },
    "server": {
      "url": "https://your-server.com/api/tools"
    }
  }'
```

### TypeScript (Server SDK)

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const vapi = new VapiClient({ token: process.env.VAPI_API_KEY! });

const tool = await vapi.tools.create({
  type: "function",
  function: {
    name: "get_weather",
    description: "Get current weather for a location",
    parameters: {
      type: "object",
      properties: {
        location: {
          type: "string",
          description: "City name, e.g. San Francisco",
        },
      },
      required: ["location"],
    },
  },
  server: {
    url: "https://your-server.com/api/tools",
  },
});

console.log("Tool created:", tool.id);
```

## Tool Types

### Function Tool

The most common tool type. Your server receives the function call and returns a result.

```json
{
  "type": "function",
  "function": {
    "name": "lookup_order",
    "description": "Look up order status by order number",
    "parameters": {
      "type": "object",
      "properties": {
        "orderNumber": {
          "type": "string",
          "description": "The order number to look up"
        }
      },
      "required": ["orderNumber"]
    }
  },
  "server": {
    "url": "https://your-server.com/api/tools"
  },
  "messages": [
    {
      "type": "request-start",
      "content": "Let me look that up for you..."
    },
    {
      "type": "request-complete",
      "content": "I found your order information."
    },
    {
      "type": "request-failed",
      "content": "I'm having trouble looking that up. Let me try again."
    }
  ]
}
```

### Transfer Call Tool

Transfer the caller to another number or SIP endpoint.

```json
{
  "type": "transferCall",
  "destinations": [
    {
      "type": "number",
      "number": "+1234567890",
      "message": "Transferring you to our billing department now.",
      "description": "Transfer to billing department when customer has billing questions"
    }
  ],
  "function": {
    "name": "transfer_to_billing",
    "description": "Transfer the caller to the billing department"
  }
}
```

SIP transfer:
```json
{
  "type": "transferCall",
  "destinations": [
    {
      "type": "sip",
      "sipUri": "sip:billing@company.com",
      "description": "Transfer to billing via SIP"
    }
  ]
}
```

### End Call Tool

Allows the assistant to end the call programmatically.

```json
{
  "type": "endCall",
  "function": {
    "name": "end_call",
    "description": "End the call when the conversation is complete"
  }
}
```

### DTMF Tool

Send DTMF tones (touch-tone signals) during a call for IVR navigation.

```json
{
  "type": "dtmf",
  "function": {
    "name": "press_digits",
    "description": "Press phone keypad digits to navigate phone menus",
    "parameters": {
      "type": "object",
      "properties": {
        "digits": {
          "type": "string",
          "description": "Digits to press (0-9, *, #)"
        }
      },
      "required": ["digits"]
    }
  }
}
```

### Voicemail Tool

Detect and handle voicemail.

```json
{
  "type": "voicemail",
  "function": {
    "name": "leave_voicemail",
    "description": "Leave a voicemail message"
  }
}
```

### Google Calendar Tool

```json
{
  "type": "google.calendar.event.create",
  "function": {
    "name": "create_calendar_event",
    "description": "Schedule a meeting on Google Calendar"
  }
}
```

### Google Sheets Tool

```json
{
  "type": "google.sheets.row.append",
  "function": {
    "name": "log_to_sheet",
    "description": "Log call data to a Google Sheet"
  }
}
```

### Slack Tool

```json
{
  "type": "slack.message.send",
  "function": {
    "name": "notify_slack",
    "description": "Send a notification to Slack"
  }
}
```

### MCP Tool

Connect to Model Context Protocol servers.

```json
{
  "type": "mcp",
  "server": {
    "url": "https://your-mcp-server.com"
  }
}
```

## Tool Server Implementation

When the assistant calls a tool, Vapi sends a POST request to your server URL.

### Request Format

```json
{
  "message": {
    "type": "tool-calls",
    "toolCallList": [
      {
        "id": "call_abc123",
        "name": "get_weather",
        "arguments": {
          "location": "San Francisco"
        }
      }
    ],
    "call": {
      "id": "call-uuid",
      "orgId": "org-uuid",
      "type": "webCall"
    }
  }
}
```

### Response Format

Your server must return:

```json
{
  "results": [
    {
      "toolCallId": "call_abc123",
      "result": "San Francisco: 65°F, partly cloudy"
    }
  ]
}
```

### Example Server (Express.js)

```typescript
import express from "express";

const app = express();
app.use(express.json());

app.post("/api/tools", async (req, res) => {
  const { message } = req.body;
  const results = [];

  for (const toolCall of message.toolCallList) {
    let result: string;

    switch (toolCall.name) {
      case "get_weather":
        const weather = await fetchWeather(toolCall.arguments.location);
        result = `${toolCall.arguments.location}: ${weather.temp}°F, ${weather.condition}`;
        break;
      case "lookup_order":
        const order = await lookupOrder(toolCall.arguments.orderNumber);
        result = `Order ${order.number}: ${order.status}`;
        break;
      default:
        result = "Unknown tool";
    }

    results.push({ toolCallId: toolCall.id, result });
  }

  res.json({ results });
});

app.listen(3000);
```

## Attaching Tools to Assistants

### By tool ID (recommended for reusable tools)

```bash
curl -X PATCH https://api.vapi.ai/assistant/{assistant-id} \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": {
      "provider": "openai",
      "model": "gpt-4.1",
      "toolIds": ["tool-id-1", "tool-id-2"],
      "messages": [{"role": "system", "content": "Your prompt here"}]
    }
  }'
```

### Inline (for one-off tools)

Define tools directly in the assistant's model configuration — see the `create-assistant` skill.

## Managing Tools

```bash
# List all tools
curl https://api.vapi.ai/tool -H "Authorization: Bearer $VAPI_API_KEY"

# Get a tool
curl https://api.vapi.ai/tool/{id} -H "Authorization: Bearer $VAPI_API_KEY"

# Update a tool
curl -X PATCH https://api.vapi.ai/tool/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"function": {"description": "Updated description"}}'

# Delete a tool
curl -X DELETE https://api.vapi.ai/tool/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

## Async Tools

For long-running operations, mark a tool as async. The assistant continues speaking while the tool executes:

```json
{
  "type": "function",
  "async": true,
  "function": {
    "name": "send_email",
    "description": "Send a confirmation email (runs in background)"
  },
  "server": {
    "url": "https://your-server.com/api/tools"
  }
}
```

## Tool Messages

Control what the assistant says during tool execution:

```json
{
  "messages": [
    {
      "type": "request-start",
      "content": "One moment while I look that up..."
    },
    {
      "type": "request-complete",
      "content": "Got it!"
    },
    {
      "type": "request-failed",
      "content": "Sorry, I couldn't complete that action."
    },
    {
      "type": "request-response-delayed",
      "content": "This is taking a bit longer than usual, please hold.",
      "timingMilliseconds": 5000
    }
  ]
}
```

## References

- [Tool Server Implementation](references/tool-server.md) — Detailed server setup guide
- [Vapi Tools Docs](https://docs.vapi.ai/tools) — Official documentation

## Additional Resources

This skills repository includes a **Vapi documentation MCP server** (`vapi-docs`) that gives your AI agent access to the full Vapi knowledge base. Use the `searchDocs` tool to look up anything beyond what this skill covers — advanced configuration, troubleshooting, SDK details, and more.

**Auto-configured:** If you cloned or installed these skills, the MCP server is already configured via `.mcp.json` (Claude Code), `.cursor/mcp.json` (Cursor), or `.vscode/mcp.json` (VS Code Copilot).

**Manual setup:** If your agent doesn't auto-detect the config, run:
```bash
claude mcp add vapi-docs -- npx -y mcp-remote https://docs.vapi.ai/_mcp/server
```

See the [README](../README.md#vapi-documentation-server-mcp) for full setup instructions across all supported agents.
