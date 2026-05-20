---
name: create-assistant
description: Create and configure Vapi voice AI assistants with models, voices, transcribers, tools, hooks, and advanced settings. Use when building voice agents, phone bots, customer support assistants, or any conversational AI that handles phone or web calls.
license: MIT
compatibility: Requires internet access and a Vapi API key (VAPI_API_KEY).
metadata:
  author: vapi
  version: "1.0"
---

# Vapi Assistant Creation

Create fully configured voice AI assistants using the Vapi API. Assistants combine a language model, voice, and transcriber to handle real-time phone and web conversations.

> **Setup:** Ensure `VAPI_API_KEY` is set. See the `setup-api-key` skill if needed.

## Quick Start

### cURL

```bash
curl -X POST https://api.vapi.ai/assistant \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Support Assistant",
    "firstMessage": "Hello! How can I help you today?",
    "model": {
      "provider": "openai",
      "model": "gpt-4.1",
      "messages": [
        {
          "role": "system",
          "content": "You are a friendly phone support assistant. Keep responses concise and under 30 words."
        }
      ]
    },
    "voice": {
      "provider": "vapi",
      "voiceId": "Elliot"
    },
    "transcriber": {
      "provider": "deepgram",
      "model": "nova-3",
      "language": "en"
    }
  }'
```

### TypeScript (Server SDK)

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const vapi = new VapiClient({ token: process.env.VAPI_API_KEY! });

const assistant = await vapi.assistants.create({
  name: "Support Assistant",
  firstMessage: "Hello! How can I help you today?",
  model: {
    provider: "openai",
    model: "gpt-4.1",
    messages: [
      {
        role: "system",
        content: "You are a friendly phone support assistant. Keep responses concise and under 30 words.",
      },
    ],
  },
  voice: {
    provider: "vapi",
    voiceId: "Elliot",
  },
  transcriber: {
    provider: "deepgram",
    model: "nova-3",
    language: "en",
  },
});

console.log("Assistant created:", assistant.id);
```

### Python

```python
import requests
import os

response = requests.post(
    "https://api.vapi.ai/assistant",
    headers={
        "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "name": "Support Assistant",
        "firstMessage": "Hello! How can I help you today?",
        "model": {
            "provider": "openai",
            "model": "gpt-4.1",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a friendly phone support assistant. Keep responses concise and under 30 words.",
                }
            ],
        },
        "voice": {"provider": "vapi", "voiceId": "Elliot"},
        "transcriber": {"provider": "deepgram", "model": "nova-3", "language": "en"},
    },
)

assistant = response.json()
print(f"Assistant created: {assistant['id']}")
```

## Core Configuration

### Model (required)

The language model powering the assistant's intelligence.

| Provider | Models | Notes |
|----------|--------|-------|
| `openai` | `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo` | Most popular, best tool calling |
| `anthropic` | `claude-3-5-sonnet-20241022`, `claude-3-5-haiku-20241022` | Strong reasoning |
| `google` | `gemini-1.5-pro`, `gemini-1.5-flash` | Multimodal capable |
| `groq` | `llama-3.1-70b-versatile`, `llama-3.1-8b-instant` | Ultra-fast inference |
| `deepinfra` | `meta-llama/Meta-Llama-3.1-70B-Instruct` | Open-source models |
| `openrouter` | Various | Access 100+ models |
| `perplexity` | `llama-3.1-sonar-large-128k-online` | Web-connected |
| `together-ai` | Various open-source | Cost-effective |

```json
{
  "model": {
    "provider": "openai",
    "model": "gpt-4.1",
    "temperature": 0.7,
    "maxTokens": 1000,
    "messages": [
      {
        "role": "system",
        "content": "Your system prompt here. Define the assistant's personality, rules, and behavior."
      }
    ]
  }
}
```

### Voice

The text-to-speech voice for the assistant.

| Provider | Popular Voices | Notes |
|----------|---------------|-------|
| `vapi` | `Elliot`, `Lily`, `Rohan`, `Paola`, `Kian` | Vapi's optimized voices, lowest latency |
| `11labs` | Use voice IDs from ElevenLabs | High quality, many voices |
| `playht` | Use voice IDs from PlayHT | Expressive voices |
| `cartesia` | Use voice IDs from Cartesia | Fast, high quality |
| `openai` | `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer` | OpenAI TTS voices |
| `azure` | Azure voice names | Enterprise-grade |
| `deepgram` | `aura-asteria-en`, `aura-luna-en` | Low latency |
| `rime-ai` | Use voice IDs from Rime | Specialized voices |

```json
{
  "voice": {
    "provider": "vapi",
    "voiceId": "Elliot"
  }
}
```

### Transcriber

The speech-to-text engine for understanding callers.

| Provider | Models | Notes |
|----------|--------|-------|
| `deepgram` | `nova-3`, `nova-2` | Fastest, most accurate |
| `google` | `latest_long`, `latest_short` | Google Cloud STT |
| `gladia` | `fast`, `accurate` | European provider |
| `assembly-ai` | `best`, `nano` | High accuracy |
| `speechmatics` | Various | Enterprise STT |
| `talkscriber` | Default | Specialized |

```json
{
  "transcriber": {
    "provider": "deepgram",
    "model": "nova-3",
    "language": "en",
    "keywords": ["Vapi:2", "AI:1"]
  }
}
```

The `keywords` field boosts recognition of specific words (word:boost format, boost 1-10).

## Behavior Configuration

### First Message

```json
{
  "firstMessage": "Hello! Thanks for calling Acme Corp. How can I help you today?",
  "firstMessageMode": "assistant-speaks-first"
}
```

`firstMessageMode` options:
- `"assistant-speaks-first"` — Assistant greets immediately (default)
- `"assistant-waits-for-user"` — Assistant waits for caller to speak first
- `"assistant-speaks-first-with-model-generated-message"` — LLM generates the greeting

### Background Sound

```json
{
  "backgroundSound": "office"
}
```

Options: `"off"`, `"office"`, `"static"`

### Backchanneling

Enable natural conversational acknowledgments ("uh-huh", "I see"):

```json
{
  "backgroundDenoisingEnabled": true,
  "backchannelingEnabled": true
}
```

### HIPAA Compliance

```json
{
  "hipaaEnabled": true
}
```

When enabled, Vapi won't store call recordings or transcripts.

## Adding Tools

Attach tools so the assistant can take actions during calls.

### Using saved tool IDs

```json
{
  "model": {
    "provider": "openai",
    "model": "gpt-4.1",
    "toolIds": ["tool-id-1", "tool-id-2"],
    "messages": [{"role": "system", "content": "..."}]
  }
}
```

### Inline tool definition

```json
{
  "model": {
    "provider": "openai",
    "model": "gpt-4.1",
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "check_availability",
          "description": "Check appointment availability for a given date",
          "parameters": {
            "type": "object",
            "properties": {
              "date": {
                "type": "string",
                "description": "Date in YYYY-MM-DD format"
              }
            },
            "required": ["date"]
          }
        },
        "server": {
          "url": "https://your-server.com/api/tools"
        }
      }
    ],
    "messages": [{"role": "system", "content": "..."}]
  }
}
```

## Hooks

Automate actions when specific call events occur. See [hooks reference](references/hooks.md) for details.

```json
{
  "hooks": [
    {
      "on": "customer.speech.timeout",
      "options": {
        "timeoutSeconds": 10,
        "triggerMaxCount": 3
      },
      "do": [
        {
          "type": "say",
          "exact": "Are you still there?"
        }
      ]
    },
    {
      "on": "call.ending",
      "filters": [
        {
          "type": "oneOf",
          "key": "call.endedReason",
          "oneOf": ["pipeline-error"]
        }
      ],
      "do": [
        {
          "type": "tool",
          "tool": {
            "type": "transferCall",
            "destinations": [
              {
                "type": "number",
                "number": "+1234567890"
              }
            ]
          }
        }
      ]
    }
  ]
}
```

## Managing Assistants

### List

```bash
curl https://api.vapi.ai/assistant \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Get

```bash
curl https://api.vapi.ai/assistant/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Update

```bash
curl -X PATCH https://api.vapi.ai/assistant/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "firstMessage": "Updated greeting!"
  }'
```

### Delete

```bash
curl -X DELETE https://api.vapi.ai/assistant/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

## Common Patterns

### Customer Support Agent

```json
{
  "name": "Customer Support",
  "firstMessage": "Thank you for calling! How can I assist you today?",
  "model": {
    "provider": "openai",
    "model": "gpt-4.1",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful customer support agent for Acme Corp. Be empathetic, concise, and solution-oriented. If you cannot resolve an issue, offer to transfer to a human agent. Keep responses under 30 words."
      }
    ]
  },
  "voice": { "provider": "vapi", "voiceId": "Lily" },
  "transcriber": { "provider": "deepgram", "model": "nova-3", "language": "en" },
  "backchannelingEnabled": true
}
```

### Appointment Scheduler

```json
{
  "name": "Appointment Scheduler",
  "firstMessage": "Hi there! I can help you schedule an appointment. What date works best for you?",
  "model": {
    "provider": "openai",
    "model": "gpt-4.1",
    "messages": [
      {
        "role": "system",
        "content": "You are an appointment scheduling assistant. Collect the customer's preferred date, time, and service type. Confirm details before booking. Be friendly and efficient."
      }
    ],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "book_appointment",
          "description": "Book an appointment for the given date, time, and service",
          "parameters": {
            "type": "object",
            "properties": {
              "date": { "type": "string", "description": "YYYY-MM-DD" },
              "time": { "type": "string", "description": "HH:MM in 24h format" },
              "service": { "type": "string", "description": "Type of service" },
              "name": { "type": "string", "description": "Customer name" }
            },
            "required": ["date", "time", "service", "name"]
          }
        },
        "server": { "url": "https://your-server.com/api/book" }
      }
    ]
  },
  "voice": { "provider": "vapi", "voiceId": "Paola" },
  "transcriber": { "provider": "deepgram", "model": "nova-3", "language": "en" }
}
```

### Multilingual Agent

```json
{
  "name": "Multilingual Support",
  "firstMessage": "Hello! How can I help you? / Hola! Como puedo ayudarte?",
  "model": {
    "provider": "openai",
    "model": "gpt-4.1",
    "messages": [
      {
        "role": "system",
        "content": "You are a multilingual support assistant. Detect the caller's language and respond in the same language. You support English and Spanish."
      }
    ]
  },
  "voice": { "provider": "vapi", "voiceId": "Paola" },
  "transcriber": { "provider": "deepgram", "model": "nova-3", "language": "multi" }
}
```

## References

- [Hooks Configuration](references/hooks.md) — Complete hook events and actions
- [Voice & Model Providers](references/providers.md) — All supported providers and models
- [Vapi API Docs](https://docs.vapi.ai/assistants/quickstart) — Official documentation

## Additional Resources

This skills repository includes a **Vapi documentation MCP server** (`vapi-docs`) that gives your AI agent access to the full Vapi knowledge base. Use the `searchDocs` tool to look up anything beyond what this skill covers — advanced configuration, troubleshooting, SDK details, and more.

**Auto-configured:** If you cloned or installed these skills, the MCP server is already configured via `.mcp.json` (Claude Code), `.cursor/mcp.json` (Cursor), or `.vscode/mcp.json` (VS Code Copilot).

**Manual setup:** If your agent doesn't auto-detect the config, run:
```bash
claude mcp add vapi-docs -- npx -y mcp-remote https://docs.vapi.ai/_mcp/server
```

See the [README](../README.md#vapi-documentation-server-mcp) for full setup instructions across all supported agents.
