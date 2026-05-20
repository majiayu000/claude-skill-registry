---
name: workers-runtime-apis
description: Cloudflare Workers Runtime APIs including Fetch, Streams, Crypto, Cache, WebSockets, and Encoding. Use for HTTP requests, streaming, encryption, caching, real-time connections, or encountering API compatibility, response handling, stream processing errors.
---

# Cloudflare Workers Runtime APIs

Master the Workers runtime APIs: Fetch, Streams, Crypto, Cache, WebSockets, and text encoding.

## Quick Reference

| API | Purpose | Common Use |
|-----|---------|------------|
| **Fetch** | HTTP requests | External APIs, proxying |
| **Streams** | Data streaming | Large files, real-time |
| **Crypto** | Cryptography | Hashing, signing, encryption |
| **Cache** | Response caching | Performance optimization |
| **WebSockets** | Real-time connections | Chat, live updates |
| **Encoding** | Text encoding | UTF-8, Base64 |

## Quick Start: Fetch API

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Basic fetch
    const response = await fetch('https://api.example.com/data');

    // With options
    const postResponse = await fetch('https://api.example.com/users', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${env.API_KEY}`,
      },
      body: JSON.stringify({ name: 'John' }),
    });

    // Clone for multiple reads
    const clone = response.clone();
    const json = await response.json();
    const text = await clone.text();

    return Response.json(json);
  }
};
```

## Critical Rules

1. **Always set timeouts for external requests** - Workers have a 30s limit, external APIs can hang
2. **Clone responses before reading body** - Body can only be read once
3. **Use streaming for large payloads** - Don't buffer entire response in memory
4. **Cache external API responses** - Reduce latency and API costs
5. **Handle Crypto operations in try/catch** - Invalid inputs throw errors
6. **WebSocket hibernation for cost** - Use Durable Objects with hibernation

## Top 10 Errors Prevented

| Error | Symptom | Prevention |
|-------|---------|------------|
| Body already read | `TypeError: Body has already been consumed` | Clone response before reading |
| Fetch timeout | Request hangs, worker times out | Use `AbortController` with timeout |
| Invalid JSON | `SyntaxError: Unexpected token` | Check content-type before parsing |
| Stream locked | `TypeError: ReadableStream is locked` | Don't read stream multiple times |
| Crypto key error | `DOMException: Invalid keyData` | Validate key format and algorithm |
| Cache miss | Returns `undefined` instead of response | Check cache before returning |
| WebSocket close | Connection drops unexpectedly | Handle close event, implement reconnect |
| Encoding error | `TypeError: Invalid code point` | Use TextEncoder/TextDecoder properly |
| CORS blocked | Browser rejects response | Add proper CORS headers |
| Request size | `413 Request Entity Too Large` | Stream large uploads |

## Fetch API Patterns

### With Timeout

```typescript
async function fetchWithTimeout(url: string, timeout: number = 5000): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, { signal: controller.signal });
    return response;
  } finally {
    clearTimeout(timeoutId);
  }
}
```

### With Retry

```typescript
async function fetchWithRetry(
  url: string,
  options: RequestInit = {},
  retries: number = 3
): Promise<Response> {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url, options);
      if (response.ok) return response;

      // Retry on 5xx errors
      if (response.status >= 500 && i < retries - 1) {
        await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
        continue;
      }

      return response;
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
    }
  }
  throw new Error('Max retries exceeded');
}
```

## Streams API

### Transform Stream

```typescript
function createUppercaseStream(): TransformStream<string, string> {
  return new TransformStream({
    transform(chunk, controller) {
      controller.enqueue(chunk.toUpperCase());
    }
  });
}

// Usage
const response = await fetch('https://example.com/text');
const transformed = response.body!
  .pipeThrough(new TextDecoderStream())
  .pipeThrough(createUppercaseStream())
  .pipeThrough(new TextEncoderStream());

return new Response(transformed);
```

### Stream Large Response

```typescript
async function streamLargeFile(url: string): Promise<Response> {
  const response = await fetch(url);

  // Stream directly without buffering
  return new Response(response.body, {
    headers: {
      'Content-Type': response.headers.get('Content-Type') || 'application/octet-stream',
    },
  });
}
```

## Crypto API

### Hashing

```typescript
async function sha256(data: string): Promise<string> {
  const encoder = new TextEncoder();
  const dataBuffer = encoder.encode(data);
  const hashBuffer = await crypto.subtle.digest('SHA-256', dataBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}
```

### HMAC Signing

```typescript
async function signHMAC(key: string, data: string): Promise<string> {
  const encoder = new TextEncoder();
  const keyData = encoder.encode(key);
  const dataBuffer = encoder.encode(data);

  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    keyData,
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );

  const signature = await crypto.subtle.sign('HMAC', cryptoKey, dataBuffer);
  return btoa(String.fromCharCode(...new Uint8Array(signature)));
}
```

## Cache API

```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const cache = caches.default;
    const cacheKey = new Request(request.url, { method: 'GET' });

    // Check cache
    let response = await cache.match(cacheKey);
    if (response) {
      return response;
    }

    // Fetch and cache
    response = await fetch(request);
    response = new Response(response.body, response);
    response.headers.set('Cache-Control', 'public, max-age=3600');

    // Store in cache (don't await)
    ctx.waitUntil(cache.put(cacheKey, response.clone()));

    return response;
  }
};
```

## WebSockets (Durable Objects)

```typescript
// Durable Object with WebSocket hibernation
export class WebSocketRoom {
  state: DurableObjectState;

  constructor(state: DurableObjectState) {
    this.state = state;
  }

  async fetch(request: Request): Promise<Response> {
    const upgradeHeader = request.headers.get('Upgrade');
    if (upgradeHeader !== 'websocket') {
      return new Response('Expected websocket', { status: 426 });
    }

    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);

    // Accept with hibernation
    this.state.acceptWebSocket(server);

    return new Response(null, { status: 101, webSocket: client });
  }

  async webSocketMessage(ws: WebSocket, message: string | ArrayBuffer) {
    // Handle incoming message
    const data = typeof message === 'string' ? message : new TextDecoder().decode(message);

    // Broadcast to all connected clients
    for (const client of this.state.getWebSockets()) {
      client.send(data);
    }
  }

  async webSocketClose(ws: WebSocket, code: number, reason: string) {
    ws.close(code, reason);
  }
}
```

## When to Load References

Load specific references based on the task:

- **Making HTTP requests?** → Load `references/fetch-api.md` for timeout, retry, proxy patterns
- **Processing large data?** → Load `references/streams-api.md` for TransformStream, chunking
- **Encryption/signing?** → Load `references/crypto-api.md` for AES, RSA, JWT verification
- **Caching responses?** → Load `references/cache-api.md` for Cache API patterns, TTL strategies
- **Real-time features?** → Load `references/websockets.md` for WebSocket patterns, Durable Objects
- **Text encoding?** → Load `references/encoding-api.md` for TextEncoder, Base64, Unicode

## Templates

| Template | Purpose | Use When |
|----------|---------|----------|
| `templates/fetch-patterns.ts` | HTTP request utilities | Building API clients |
| `templates/stream-processing.ts` | Stream transformation | Processing large files |
| `templates/crypto-operations.ts` | Crypto utilities | Signing, hashing, encryption |
| `templates/websocket-handler.ts` | WebSocket DO | Real-time applications |

## Resources

- Runtime APIs: https://developers.cloudflare.com/workers/runtime-apis/
- Fetch API: https://developers.cloudflare.com/workers/runtime-apis/fetch/
- Streams API: https://developers.cloudflare.com/workers/runtime-apis/streams/
- Web Crypto: https://developers.cloudflare.com/workers/runtime-apis/web-crypto/
- Cache API: https://developers.cloudflare.com/workers/runtime-apis/cache/
- WebSockets: https://developers.cloudflare.com/workers/runtime-apis/websockets/
