---
name: mpp-proxy
description: Implement MPP payment proxies — wrap existing APIs with HTTP 402 payment gates without modifying the upstream service. Use when monetizing third-party APIs, adding payment layers to existing services, or building API marketplaces.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# MPP Payment Proxy

## Before writing code

**Fetch live docs**:
1. Fetch `https://www.npmjs.com/package/mppx` for the proxy handler API and configuration
2. Web-search `mppx proxy payment 402 existing API monetize` for proxy implementation patterns
3. Web-search `site:github.com stripe-samples machine-payments proxy` for official proxy sample code
4. Fetch `https://developers.cloudflare.com/agents/agentic-payments/mpp/` for Cloudflare Workers proxy patterns

## Conceptual Architecture

### What the Proxy Does

The MPP proxy wraps an existing upstream API with a payment gate, requiring clients to pay before their requests are forwarded. The upstream API is unmodified — it never sees the payment flow.

```
Client → MPP Proxy (402 challenge-response) → Upstream API
         ↑ payment gate                       ↑ unmodified
```

### Use Cases

- **API monetization** — Charge for access to your own internal APIs
- **Third-party reselling** — Add payment layer on top of third-party APIs (with permission)
- **API marketplace** — Proxy multiple upstream APIs through a single payment gateway
- **Rate-limiting replacement** — Replace API key + rate limits with pay-per-use
- **Value-added wrapper** — Add caching, transformation, or enrichment on top of upstream APIs

### Proxy Architecture

```
┌──────────────┐     ┌──────────────────────┐     ┌──────────────┐
│  AI Agent    │────→│    MPP Proxy          │────→│  Upstream    │
│  (Client)    │←────│  1. 402 Challenge     │←────│  API         │
│              │     │  2. Verify Payment    │     │  (Unmodified)│
│              │     │  3. Forward Request   │     │              │
│              │     │  4. Return + Receipt  │     │              │
└──────────────┘     └──────────────────────┘     └──────────────┘
```

### mppx Proxy Handler

The `mppx` SDK provides a dedicated proxy handler:

```typescript
import { Mppx, tempo } from 'mppx/server';

const mppx = Mppx.create({
  secretKey: process.env.MPP_SECRET_KEY,
  methods: [tempo.charge({ /* config */ })],
});

// Proxy all requests to upstream with payment gate
app.all('/api/*', mppx.charge({ amount: '100' }), async (c) => {
  const upstreamUrl = `https://upstream-api.com${c.req.path}`;
  const response = await fetch(upstreamUrl, {
    method: c.req.method,
    headers: c.req.headers,
    body: c.req.method !== 'GET' ? await c.req.text() : undefined,
  });
  return new Response(response.body, {
    status: response.status,
    headers: response.headers,
  });
});
```

### Cloudflare Workers Proxy

For edge-deployed proxies:

```typescript
// Cloudflare Workers + MPP proxy pattern
export default {
  async fetch(request, env) {
    // MPP middleware handles 402 challenge-response
    // On successful payment, forwards to upstream
  }
};
```

### Pricing Strategies

| Strategy | Description |
|----------|-------------|
| **Flat rate** | Same price for all requests |
| **Endpoint-based** | Different prices per API route |
| **Payload-based** | Price varies by request/response size |
| **Metered** | Session-based, charged per unit consumed |
| **Tiered** | Volume discounts (first 100 at $X, next 1000 at $Y) |

### Request/Response Handling

- **Headers** — Forward client headers to upstream (strip `Authorization: Payment`)
- **Body** — Forward request body unchanged
- **Response** — Add `Payment-Receipt` header to upstream response
- **Errors** — Distinguish between payment errors (402) and upstream errors (pass through)

### Multi-Upstream Proxy

Route to different upstreams based on the path:

```typescript
const upstreams = {
  '/ai/': 'https://api.openai.com',
  '/data/': 'https://api.data-vendor.com',
  '/search/': 'https://api.search-engine.com',
};
```

### Best Practices

- Strip payment headers before forwarding to upstream
- Add service discovery (`/openapi.json`) describing proxied endpoints
- Implement caching for idempotent GET requests to reduce upstream calls
- Add response transformation if needed (but keep it minimal)
- Monitor upstream availability and return appropriate errors
- Set up health checks that verify both proxy and upstream availability
- Consider latency — the proxy adds the payment negotiation round-trip

Fetch the latest mppx proxy documentation and Cloudflare MPP integration guide for exact proxy API, configuration options, and edge deployment patterns before implementing.
