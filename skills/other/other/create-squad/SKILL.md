---
name: create-squad
description: Create multi-assistant squads in Vapi with handoffs between specialized voice agents. Use when building complex voice workflows that need multiple assistants with different roles, like triage-to-booking or sales-to-support handoffs.
license: MIT
compatibility: Requires internet access and a Vapi API key (VAPI_API_KEY).
metadata:
  author: vapi
  version: "1.0"
---

# Vapi Squad Creation

Create squads that orchestrate multiple specialized assistants with context-preserving handoffs. Break complex workflows into focused assistants that transfer calls between each other.

> **Setup:** Ensure `VAPI_API_KEY` is set. See the `setup-api-key` skill if needed.

## Why Squads?

Single assistants with large prompts cause higher hallucination rates, increased costs, and greater latency. Squads solve this by creating focused assistants with specific roles:

- **Triage** → **Booking** → **Confirmation**
- **Sales** → **Technical Support** → **Billing**
- **Receptionist** → **Department Specialist**

## Quick Start

### cURL

```bash
curl -X POST https://api.vapi.ai/squad \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Support Squad",
    "members": [
      {
        "assistant": {
          "name": "Receptionist",
          "firstMessage": "Hello! How can I direct your call today?",
          "model": {
            "provider": "openai",
            "model": "gpt-4.1",
            "messages": [
              {
                "role": "system",
                "content": "You are a receptionist. Determine if the caller needs sales or support, then transfer them to the right department."
              }
            ],
            "tools": [
              {
                "type": "handoff",
                "destinations": [
                  {
                    "type": "assistant",
                    "assistantId": "sales-assistant-id",
                    "description": "Transfer when the caller asks about pricing, plans, or wants to purchase"
                  },
                  {
                    "type": "assistant",
                    "assistantId": "support-assistant-id",
                    "description": "Transfer when the caller has a technical issue or needs help"
                  }
                ]
              }
            ]
          },
          "voice": { "provider": "vapi", "voiceId": "Lily" },
          "transcriber": { "provider": "deepgram", "model": "nova-3", "language": "en" }
        }
      },
      {
        "assistantId": "sales-assistant-id"
      },
      {
        "assistantId": "support-assistant-id"
      }
    ]
  }'
```

### TypeScript (Server SDK)

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const vapi = new VapiClient({ token: process.env.VAPI_API_KEY! });

const squad = await vapi.squads.create({
  name: "Support Squad",
  members: [
    {
      assistant: {
        name: "Receptionist",
        firstMessage: "Hello! How can I direct your call today?",
        model: {
          provider: "openai",
          model: "gpt-4.1",
          messages: [
            {
              role: "system",
              content:
                "You are a receptionist. Determine if the caller needs sales or support, then transfer them.",
            },
          ],
          tools: [
            {
              type: "handoff",
              destinations: [
                {
                  type: "assistant",
                  assistantId: "sales-assistant-id",
                  description: "Transfer for pricing and purchasing questions",
                },
                {
                  type: "assistant",
                  assistantId: "support-assistant-id",
                  description: "Transfer for technical issues",
                },
              ],
            },
          ],
        },
        voice: { provider: "vapi", voiceId: "Lily" },
        transcriber: { provider: "deepgram", model: "nova-3", language: "en" },
      },
    },
    { assistantId: "sales-assistant-id" },
    { assistantId: "support-assistant-id" },
  ],
});

console.log("Squad created:", squad.id);
```

## Squad Structure

### Members

The first member in the array starts the call. Each member is either:

- **Transient** — Defined inline with `assistant: { ... }`
- **Persistent** — References a saved assistant via `assistantId: "..."`

```json
{
  "members": [
    { "assistant": { "name": "Inline Assistant", "..." : "..." } },
    { "assistantId": "saved-assistant-id" }
  ]
}
```

### Handoff Tools

Handoff tools define how assistants transfer between each other:

```json
{
  "type": "handoff",
  "destinations": [
    {
      "type": "assistant",
      "assistantId": "target-assistant-id",
      "description": "Clear description of WHEN to transfer. Be specific about trigger conditions."
    }
  ],
  "function": {
    "name": "handoff_to_sales"
  }
}
```

### Assistant Overrides

Override saved assistant settings within the squad context without modifying the original:

```json
{
  "assistantId": "saved-assistant-id",
  "assistantOverrides": {
    "voice": { "provider": "vapi", "voiceId": "Elliot" },
    "firstMessage": "Overridden greeting for this squad"
  }
}
```

### Appending Tools via Overrides

Add squad-specific tools to a saved assistant:

```json
{
  "assistantId": "saved-assistant-id",
  "assistantOverrides": {
    "tools:append": [
      {
        "type": "handoff",
        "destinations": [
          {
            "type": "assistant",
            "assistantId": "another-assistant-id",
            "description": "Transfer when customer needs billing help"
          }
        ],
        "function": { "name": "handoff_to_billing" }
      }
    ]
  }
}
```

### Member Overrides

Apply configuration to ALL members simultaneously:

```json
{
  "members": [
    { "assistant": { "name": "Agent A", "..." : "..." } },
    { "assistantId": "agent-b-id" }
  ],
  "memberOverrides": {
    "voice": { "provider": "vapi", "voiceId": "Elliot" },
    "transcriber": { "provider": "deepgram", "model": "nova-3", "language": "en" }
  }
}
```

## Using Squads in Calls

### Outbound call with a squad

```bash
curl -X POST https://api.vapi.ai/call \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "squadId": "your-squad-id",
    "phoneNumberId": "your-phone-number-id",
    "customer": {
      "number": "+11234567890"
    }
  }'
```

### Transient squad in a call

```json
{
  "squad": {
    "members": [
      { "assistant": { "..." : "..." } },
      { "assistantId": "..." }
    ]
  },
  "phoneNumberId": "phone-number-id",
  "customer": { "number": "+11234567890" }
}
```

## Common Patterns

### Clinic Triage → Scheduling

```json
{
  "name": "Clinic Squad",
  "members": [
    {
      "assistant": {
        "name": "Triage Nurse",
        "firstMessage": "Hello, this is the clinic. How can I help you today?",
        "model": {
          "provider": "openai",
          "model": "gpt-4.1",
          "messages": [
            {
              "role": "system",
              "content": "You are a clinic triage assistant. Assess the caller's needs: if they need an appointment, transfer to scheduling. If it's urgent, transfer to the nurse line."
            }
          ],
          "tools": [
            {
              "type": "handoff",
              "destinations": [
                {
                  "type": "assistant",
                  "assistantId": "scheduling-assistant-id",
                  "description": "Transfer when caller wants to book, reschedule, or cancel an appointment"
                },
                {
                  "type": "assistant",
                  "assistantId": "nurse-assistant-id",
                  "description": "Transfer for urgent medical questions or symptoms"
                }
              ]
            }
          ]
        },
        "voice": { "provider": "vapi", "voiceId": "Lily" }
      }
    },
    { "assistantId": "scheduling-assistant-id" },
    { "assistantId": "nurse-assistant-id" }
  ]
}
```

### E-commerce: Sales → Support → Returns

```json
{
  "name": "E-commerce Squad",
  "members": [
    {
      "assistant": {
        "name": "Sales Agent",
        "firstMessage": "Welcome to our store! Are you looking to make a purchase today?",
        "model": {
          "provider": "openai",
          "model": "gpt-4.1",
          "messages": [
            { "role": "system", "content": "You are a sales assistant. Help customers find products and make purchases. Transfer to support for order issues or returns." }
          ],
          "tools": [
            {
              "type": "handoff",
              "destinations": [
                { "type": "assistant", "assistantId": "support-id", "description": "Transfer for order status, shipping, or account issues" },
                { "type": "assistant", "assistantId": "returns-id", "description": "Transfer for returns, refunds, or exchanges" }
              ]
            }
          ]
        }
      }
    },
    { "assistantId": "support-id" },
    { "assistantId": "returns-id" }
  ]
}
```

## Best Practices

1. **Keep assistants focused** — Each assistant should have 1-3 goals maximum
2. **Minimize squad size** — Split only when there's a clear functional boundary
3. **Write specific handoff descriptions** — The LLM uses these to decide when to transfer
4. **Mention handoffs in system prompts** — Tell each assistant what departments exist
5. **Use member overrides** — Apply consistent voice and transcriber settings across the squad

## Managing Squads

```bash
# List squads
curl https://api.vapi.ai/squad -H "Authorization: Bearer $VAPI_API_KEY"

# Get a squad
curl https://api.vapi.ai/squad/{id} -H "Authorization: Bearer $VAPI_API_KEY"

# Update a squad
curl -X PATCH https://api.vapi.ai/squad/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Squad Name"}'

# Delete a squad
curl -X DELETE https://api.vapi.ai/squad/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

## References

- [Vapi Squads Docs](https://docs.vapi.ai/squads) — Official documentation
- [Squad Examples](https://docs.vapi.ai/squads-example) — More patterns
- [Handoff Configuration](https://docs.vapi.ai/squads/handoff) — Detailed handoff guide

## Additional Resources

This skills repository includes a **Vapi documentation MCP server** (`vapi-docs`) that gives your AI agent access to the full Vapi knowledge base. Use the `searchDocs` tool to look up anything beyond what this skill covers — advanced configuration, troubleshooting, SDK details, and more.

**Auto-configured:** If you cloned or installed these skills, the MCP server is already configured via `.mcp.json` (Claude Code), `.cursor/mcp.json` (Cursor), or `.vscode/mcp.json` (VS Code Copilot).

**Manual setup:** If your agent doesn't auto-detect the config, run:
```bash
claude mcp add vapi-docs -- npx -y mcp-remote https://docs.vapi.ai/_mcp/server
```

See the [README](../README.md#vapi-documentation-server-mcp) for full setup instructions across all supported agents.
