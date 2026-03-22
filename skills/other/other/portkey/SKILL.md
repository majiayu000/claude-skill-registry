---
name: portkey
description: >-
  You are an expert in Portkey, the AI gateway that sits between your app and
  LLM providers. You help developers add caching, fallbacks, load balancing,
  request retries, guardrails, semantic caching, budget limits, and
  observability to LLM calls — using a single unified API that works with 200+
  models from OpenAI, Anthropic, Google, and open-source providers.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: AI & Machine Learning
  tags:
    - llm
    - gateway
    - observability
    - routing
    - caching
    - guardrails
    - production
---

# Portkey — AI Gateway for Production LLM Apps

You are an expert in Portkey, the AI gateway that sits between your app and LLM providers. You help developers add caching, fallbacks, load balancing, request retries, guardrails, semantic caching, budget limits, and observability to LLM calls — using a single unified API that works with 200+ models from OpenAI, Anthropic, Google, and open-source providers.

## Core Capabilities

```typescript
import Portkey from "portkey-ai";

const portkey = new Portkey({
  apiKey: process.env.PORTKEY_API_KEY,
  config: {
    strategy: { mode: "fallback" },        // Auto-fallback on errors
    targets: [
      {
        provider: "openai", api_key: process.env.OPENAI_KEY,
        override_params: { model: "gpt-4o" },
        weight: 0.7,
      },
      {
        provider: "anthropic", api_key: process.env.ANTHROPIC_KEY,
        override_params: { model: "claude-sonnet-4-20250514" },
        weight: 0.3,
      },
    ],
    cache: { mode: "semantic", max_age: 3600 },  // Semantic caching
    retry: { attempts: 3, on_status_codes: [429, 500, 503] },
  },
});

// Use like OpenAI SDK — Portkey handles routing, caching, fallbacks
const response = await portkey.chat.completions.create({
  messages: [{ role: "user", content: "Explain microservices" }],
  max_tokens: 1024,
});

// Guardrails
const guarded = new Portkey({
  apiKey: process.env.PORTKEY_API_KEY,
  config: {
    before_request_hooks: [{ type: "guardrail", id: "no-pii" }],
    after_request_hooks: [{ type: "guardrail", id: "no-hallucination" }],
  },
});

// Budget limits
// Set in Portkey dashboard: max $100/day per API key
```

## Installation

```bash
npm install portkey-ai
# or
pip install portkey-ai
```

## Best Practices

1. **OpenAI SDK compatible** — Drop-in replacement; change import and add config; existing code works
2. **Fallbacks** — Route to backup provider when primary fails; 99.99% effective uptime
3. **Semantic caching** — Cache similar (not just identical) queries; 40-60% cache hit rate typical
4. **Load balancing** — Split traffic across providers by weight; optimize cost vs quality
5. **Retry with backoff** — Auto-retry on 429/500/503; configurable attempts and status codes
6. **Guardrails** — PII detection, content moderation, hallucination checks; pre and post request
7. **Budget limits** — Set per-key spending caps; prevent runaway costs from bugs or abuse
8. **Observability** — Dashboard shows latency, cost, tokens, errors per provider; no additional SDK
