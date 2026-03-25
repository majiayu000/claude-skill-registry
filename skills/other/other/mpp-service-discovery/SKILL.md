---
name: mpp-service-discovery
description: Implement MPP service discovery — OpenAPI documents with x-payment-info extensions, x-service-info metadata, and llms.txt for autonomous agent discovery. Use when publishing paid API metadata for AI agents to find and pay for your services.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# MPP Service Discovery

## Before writing code

**Fetch live docs**:
1. Fetch `https://paymentauth.org/draft-payment-discovery-00.html` for the canonical service discovery specification
2. Web-search `mpp service discovery openapi x-payment-info llms.txt` for implementation examples
3. Web-search `site:mpp.dev directory` for the MPP payments directory and listing requirements
4. Fetch `https://mpp.dev/overview` for discovery-related documentation

## Conceptual Architecture

### What Service Discovery Does

MPP service discovery allows AI agents to autonomously find, understand, and pay for HTTP services. It uses two mechanisms:

1. **OpenAPI Document** — Machine-readable API spec with payment extensions
2. **llms.txt** — Human/AI-readable service description for LLM agent discovery

### OpenAPI Document (GET /openapi.json)

Services publish an OpenAPI 3.x document with two custom extensions:

#### x-service-info (Top-Level)

```json
{
  "openapi": "3.0.0",
  "info": { "title": "My Paid API", "version": "1.0.0" },
  "x-service-info": {
    "categories": ["compute", "data", "media"],
    "docs": {
      "apiReference": "https://api.example.com/docs",
      "homepage": "https://example.com",
      "llms": "https://api.example.com/llms.txt"
    }
  }
}
```

#### x-payment-info (Per-Operation)

```json
{
  "paths": {
    "/api/data": {
      "get": {
        "summary": "Get premium data",
        "x-payment-info": {
          "intent": "charge",
          "method": "tempo",
          "amount": "100",
          "currency": "0x20C000000000000000000000b9537d11c60E8b50",
          "description": "$0.01 per request"
        },
        "responses": {
          "200": { "description": "Premium data" },
          "402": { "description": "Payment required" }
        }
      }
    }
  }
}
```

### x-payment-info Fields

| Field | Required | Description |
|-------|----------|-------------|
| `intent` | Yes | `"charge"` or `"session"` |
| `method` | Yes | Payment method (e.g., `"tempo"`, `"stripe"`) |
| `amount` | No | Price (null for dynamic pricing) |
| `currency` | Yes | Currency identifier (contract address for crypto, code for fiat) |
| `description` | No | Human-readable pricing description |

### Discovery Properties

- `amount` can be `null` for dynamic pricing — the 402 challenge remains authoritative
- Discovery data is **advisory only** — agents should still handle the actual 402 challenge
- Servers should include `Cache-Control: max-age=300`
- Size limit: 64 KB per OpenAPI document
- Registries recrawl every 24 hours minimum
- Services are delisted after 7+ consecutive crawl failures

### llms.txt

A text file (analogous to `robots.txt`) describing the service for autonomous agents:

```
# My Paid API
> AI-powered data analysis service

## Endpoints
- GET /api/analyze — Analyze data ($0.05/request, Tempo USDC)
- GET /api/summarize — Summarize text ($0.02/request, Tempo USDC)

## Pricing
All prices in USDC. Volume discounts available via session payments.

## Authentication
Payments via MPP (HTTP 402). No API key required.

## Contact
support@example.com
```

### MPP Payments Directory

Services can be listed in the MPP payments directory (100+ services):
- Categories: model providers, developer tools, compute, data vendors
- Listing requires a valid OpenAPI document with `x-payment-info`
- Directory recrawls services periodically

### Implementation Pattern

```typescript
app.get('/openapi.json', (c) => {
  return c.json({
    openapi: '3.0.0',
    info: { title: 'My API', version: '1.0.0' },
    'x-service-info': {
      categories: ['data'],
      docs: { llms: 'https://api.example.com/llms.txt' },
    },
    paths: {
      '/api/data': {
        get: {
          summary: 'Get data',
          'x-payment-info': {
            intent: 'charge',
            method: 'tempo',
            amount: '100',
            currency: '0x20C000000000000000000000b9537d11c60E8b50',
            description: '$0.01 per request',
          },
          responses: {
            '200': { description: 'Data returned' },
            '402': { description: 'Payment required' },
          },
        },
      },
    },
  });
});

app.get('/llms.txt', (c) => {
  return c.text(`# My API\n> Premium data service\n\n## Endpoints\n...`);
});
```

### Best Practices

- Include both `openapi.json` and `llms.txt` for maximum discoverability
- Keep the OpenAPI document under 64 KB
- Set `Cache-Control: max-age=300` on discovery endpoints
- Include all payable operations with 402 responses declared
- Use descriptive `description` fields for human-readable pricing
- Update discovery documents when pricing changes
- Register with the MPP payments directory for broader visibility

Fetch the latest service discovery specification from paymentauth.org for exact extension schemas, directory listing requirements, and llms.txt format before implementing.
