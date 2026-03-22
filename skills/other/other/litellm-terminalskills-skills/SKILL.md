---
name: litellm
description: >-
  Call 100+ LLM APIs with one interface using LiteLLM — unified API proxy for
  OpenAI, Anthropic, Google, Mistral, Cohere, and self-hosted models. Use when
  someone asks to "switch between LLM providers", "LiteLLM", "unified LLM API",
  "LLM proxy", "call Claude and GPT with the same code", "LLM load balancing",
  or "multi-model AI gateway". Covers provider routing, fallbacks, rate limiting,
  spend tracking, and self-hosted proxy.
license: Apache-2.0
compatibility: "Python. Node.js via OpenAI SDK (proxy mode). Self-hostable."
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: data-ai
  tags: ["llm", "proxy", "litellm", "gateway", "multi-model"]
---

# LiteLLM

## Overview

LiteLLM provides a single API to call 100+ LLM providers — OpenAI, Anthropic, Google Gemini, Mistral, Cohere, Azure, Bedrock, Ollama, and more. Write your code once using the OpenAI SDK format, then switch providers by changing a model string. As a proxy server, it adds load balancing, fallbacks, rate limiting, spend tracking, and API key management for teams.

## When to Use

- Using multiple LLM providers and want a unified interface
- Need automatic fallbacks (if Claude is down, use GPT)
- Cost tracking across multiple providers and teams
- Load balancing requests across multiple API keys or models
- Self-hosted proxy to manage LLM access for a team

## Instructions

### Setup

```bash
pip install litellm

# Or run as proxy server
pip install 'litellm[proxy]'
```

### SDK Usage (Python)

```python
# llm.py — Call any LLM with the same interface
from litellm import completion

# OpenAI
response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
)

# Anthropic — same interface, just change the model string
response = completion(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "Hello!"}],
)

# Google Gemini
response = completion(
    model="gemini/gemini-2.0-flash",
    messages=[{"role": "user", "content": "Hello!"}],
)

# Local Ollama
response = completion(
    model="ollama/llama3",
    messages=[{"role": "user", "content": "Hello!"}],
    api_base="http://localhost:11434",
)

# All return the same response format (OpenAI-compatible)
print(response.choices[0].message.content)
```

### Proxy Server

```yaml
# litellm_config.yaml — Proxy configuration
model_list:
  - model_name: "fast"
    litellm_params:
      model: gpt-4o-mini
      api_key: sk-...

  - model_name: "smart"
    litellm_params:
      model: claude-sonnet-4-20250514
      api_key: sk-ant-...

  - model_name: "smart"  # Second "smart" model = load balancing
    litellm_params:
      model: gpt-4o
      api_key: sk-...

  - model_name: "cheap"
    litellm_params:
      model: gemini/gemini-2.0-flash
      api_key: AIza...

router_settings:
  routing_strategy: "latency-based-routing"
  num_retries: 3
  timeout: 30
  fallbacks: [{"smart": ["fast"]}]  # If smart fails, use fast

general_settings:
  master_key: "sk-master-key-xxx"  # Admin key
```

```bash
# Start proxy
litellm --config litellm_config.yaml --port 4000

# Call via OpenAI SDK (any language!)
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-master-key-xxx" \
  -d '{"model": "smart", "messages": [{"role": "user", "content": "Hello"}]}'
```

### Node.js via Proxy

```typescript
// app.ts — Use any OpenAI SDK client with LiteLLM proxy
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://localhost:4000/v1",
  apiKey: "sk-master-key-xxx",
});

// Calls route to Claude or GPT based on load balancing config
const response = await client.chat.completions.create({
  model: "smart",
  messages: [{ role: "user", content: "Explain monads simply." }],
});
```

### Spend Tracking

```python
# Track costs per team/user/project
from litellm import completion

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
    metadata={
        "user": "user-123",
        "team": "engineering",
        "project": "chatbot",
    },
)

# LiteLLM proxy stores costs in its database
# Query via API: GET /spend/logs?user=user-123
```

## Examples

### Example 1: Multi-provider AI application

**User prompt:** "My app uses Claude for reasoning and GPT-4o for function calling. Set up a unified interface."

The agent will configure LiteLLM with named model groups, route by capability, and add fallbacks between providers.

### Example 2: Team LLM gateway with cost controls

**User prompt:** "Set up an LLM proxy for our team with per-user rate limits and spend tracking."

The agent will deploy the LiteLLM proxy, configure API keys per team member, set rate limits and budget caps, and enable spend logging.

## Guidelines

- **Model format: `provider/model`** — `anthropic/claude-sonnet-4-20250514`, `gemini/gemini-2.0-flash`
- **Proxy for teams** — centralize API keys, track spend, enforce rate limits
- **Fallbacks for reliability** — if primary model fails, route to backup
- **Load balancing** — multiple entries with same `model_name` distribute traffic
- **Latency-based routing** — LiteLLM picks the fastest responding provider
- **Spend tracking** — costs calculated per-request, queryable via API
- **OpenAI SDK compatible** — any OpenAI client library works with the proxy
- **Streaming works** — `stream=True` works across all providers
- **Environment variables** — `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` etc. auto-detected
