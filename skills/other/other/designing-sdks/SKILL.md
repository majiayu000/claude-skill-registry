---
name: designing-sdks
description: Design production-ready SDKs with retry logic, error handling, pagination, and multi-language support. Use when building client libraries for APIs or creating developer-facing SDK interfaces.
---

# SDK Design

Design client libraries (SDKs) with excellent developer experience through intuitive APIs, robust error handling, automatic retries, and consistent patterns across programming languages.

## When to Use This Skill

Use when building a client library for a REST API, creating internal service SDKs, implementing retry logic with exponential backoff, handling authentication patterns, creating typed error hierarchies, implementing pagination with async iterators, or designing streaming APIs for real-time data.

## Core Architecture Patterns

### Client → Resources → Methods

Organize SDK code hierarchically:

```
Client (config: API key, base URL, retries, timeout)
├─ Resources (users, payments, posts)
│   ├─ create(), retrieve(), update(), delete()
│   └─ list() (with pagination)
└─ Top-Level Methods (convenience)
```

**Resource-Based (Stripe style):**

```typescript
const client = new APIClient({ apiKey: 'sk_test_...' })
const user = await client.users.create({ email: 'user@example.com' })
```

Use for APIs <100 methods. Prioritizes developer experience.

**Command-Based (AWS SDK v3):**

```typescript
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'
await client.send(new PutObjectCommand({ Bucket: '...' }))
```

Use for APIs >100 methods. Prioritizes bundle size and tree-shaking.

For detailed architectural guidance, see `references/architecture-patterns.md`.

## Language-Specific Patterns

### TypeScript: Async-Only

```typescript
const user = await client.users.create({ email: 'user@example.com' })
```

All methods return Promises. Avoid callbacks.

### Python: Dual Sync/Async

```python
# Sync
client = APIClient(api_key='sk_test_...')
user = client.users.create(email='user@example.com')

# Async
async_client = AsyncAPIClient(api_key='sk_test_...')
user = await async_client.users.create(email='user@example.com')
```

Provide both clients. Users choose based on architecture.

### Go: Sync with Context

```go
client := apiclient.New("api_key")
user, err := client.Users().Create(ctx, req)
```

Use context.Context for timeout and cancellation.

## Authentication

### API Key (Most Common)

```typescript
const client = new APIClient({ apiKey: process.env.API_KEY })
```

Store keys in environment variables, never hardcode.

### OAuth Token Refresh

```typescript
const client = new APIClient({
  clientId: 'id',
  clientSecret: 'secret',
  refreshToken: 'token',
  onTokenRefresh: (newToken) => saveToken(newToken)
})
```

SDK automatically refreshes tokens before expiry.

### Bearer Token Per-Request

```typescript
await client.users.list({
  headers: { Authorization: `Bearer ${userToken}` }
})
```

Use for multi-tenant applications.

See `references/authentication.md` for OAuth flows, JWT handling, and credential providers.

## Retry and Backoff

### Exponential Backoff with Jitter

```typescript
async function retryWithBackoff<T>(fn: () => Promise<T>, maxRetries: number): Promise<T> {
  let attempt = 0

  while (attempt <= maxRetries) {
    try {
      return await fn()
    } catch (error) {
      attempt++
      if (attempt > maxRetries || !isRetryable(error)) throw error

      const exponential = Math.min(1000 * Math.pow(2, attempt - 1), 10000)
      const jitter = Math.random() * 500
      await sleep(exponential + jitter)
    }
  }
}

function isRetryable(error: any): boolean {
  return (
    error.code === 'ECONNRESET' ||
    error.code === 'ETIMEDOUT' ||
    (error.status >= 500 && error.status < 600) ||
    error.status === 429
  )
}
```

**Retry Decision Matrix:**

| Error Type | Retry? | Rationale |
|------------|--------|-----------|
| 5xx, 429, Network Timeout | ✅ Yes | Transient errors |
| 4xx, 401, 403, 404 | ❌ No | Client errors won't fix themselves |

### Rate Limit Handling

```typescript
if (error.status === 429) {
  const retryAfter = parseInt(error.headers['retry-after'] || '60')
  await sleep(retryAfter * 1000)
}
```

Respect `Retry-After` header on 429 responses.

See `references/retry-backoff.md` for jitter strategies, circuit breakers, and idempotency keys.

## Error Handling

### Typed Error Hierarchy

```typescript
class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public code: string,
    public requestId: string
  ) {
    super(message)
    this.name = 'APIError'
  }
}

class RateLimitError extends APIError {
  constructor(message: string, requestId: string, public retryAfter: number) {
    super(message, 429, 'rate_limit_error', requestId)
  }
}

class AuthenticationError extends APIError {
  constructor(message: string, requestId: string) {
    super(message, 401, 'authentication_error', requestId)
  }
}
```

### Error Handling in Practice

```typescript
try {
  const user = await client.users.create({ email: 'invalid' })
} catch (error) {
  if (error instanceof RateLimitError) {
    await sleep(error.retryAfter * 1000)
  } else if (error instanceof AuthenticationError) {
    console.error('Invalid API key')
  } else if (error instanceof APIError) {
    console.error(`${error.message} (Request ID: ${error.requestId})`)
  }
}
```

Include request ID in all errors for debugging.

See `references/error-handling.md` for user-friendly messages, validation errors, and debugging support.

## Pagination

### Async Iterators (Recommended)

**TypeScript:**

```typescript
for await (const user of client.users.list({ limit: 100 })) {
  console.log(user.id, user.email)
}
```

**Python:**

```python
async for user in client.users.list(limit=100):
    print(user.id, user.email)
```

SDK automatically fetches next page.

### Implementation

```typescript
class UsersResource {
  async *list(options?: { limit?: number }): AsyncGenerator<User> {
    let cursor: string | undefined = undefined

    while (true) {
      const response = await this.client.request('GET', '/users', {
        query: { limit: String(options?.limit || 100), ...(cursor ? { cursor } : {}) }
      })

      for (const user of response.data) yield user

      if (!response.has_more) break
      cursor = response.next_cursor
    }
  }
}
```

### Manual Pagination

```typescript
let cursor: string | undefined = undefined
while (true) {
  const response = await client.users.list({ limit: 100, cursor })
  for (const user of response.data) console.log(user.id)
  if (!response.has_more) break
  cursor = response.next_cursor
}
```

Provide both automatic and manual options.

See `references/pagination.md` for cursor vs. offset pagination and Go channel patterns.

## Streaming

### Server-Sent Events

```typescript
async *stream(path: string, body?: any): AsyncGenerator<any> {
  const response = await fetch(url, {
    headers: { 'Accept': 'text/event-stream' },
    body: JSON.stringify(body)
  })

  const reader = response.body!.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    const chunk = decoder.decode(value)
    for (const line of chunk.split('\n')) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6)
        if (data === '[DONE]') return
        yield JSON.parse(data)
      }
    }
  }
}

// Usage
for await (const chunk of client.posts.stream({ prompt: 'Write a story' })) {
  process.stdout.write(chunk.content)
}
```

## Idempotency Keys

Prevent duplicate operations during retries:

```typescript
import { randomUUID } from 'crypto'

if (['POST', 'PATCH', 'PUT'].includes(method)) {
  headers['Idempotency-Key'] = options?.idempotencyKey || randomUUID()
}

// Usage
await client.charges.create(
  { amount: 1000 },
  { idempotencyKey: 'charge_unique_123' }
)
```

Server deduplicates requests by key.

## Versioning

### Semantic Versioning

- `1.0.0` → `1.1.0`: New features (safe)
- `1.1.0` → `2.0.0`: Breaking changes (review)
- `1.0.0` → `1.0.1`: Bug fixes (safe)

### Deprecation Warnings

```typescript
function deprecated(message: string, since: string) {
  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value
    descriptor.value = function (...args: any[]) {
      console.warn(`[DEPRECATED] ${propertyKey} since ${since}. ${message}`)
      return originalMethod.apply(this, args)
    }
    return descriptor
  }
}

@deprecated('Use users.list() instead', 'v2.0.0')
async getAll() { return this.list() }
```

### API Version Pinning

```typescript
const client = new APIClient({
  apiKey: 'sk_test_...',
  apiVersion: '2025-01-01'
})
```

See `references/versioning.md` for migration strategies.

## Configuration Best Practices

```typescript
interface ClientConfig {
  apiKey: string
  baseURL?: string
  maxRetries?: number
  timeout?: number
  apiVersion?: string
  onTokenRefresh?: (token: string) => void
}

class APIClient {
  constructor(config: ClientConfig) {
    this.apiKey = config.apiKey
    this.baseURL = config.baseURL || 'https://api.example.com'
    this.maxRetries = config.maxRetries ?? 3
    this.timeout = config.timeout ?? 30000
  }
}
```

Provide sensible defaults, require only apiKey.

## Quick Reference Tables

### Authentication Patterns

| Pattern | Use Case |
|---------|----------|
| API Key | Service-to-service |
| OAuth Refresh | User-based auth |
| Bearer Per-Request | Multi-tenant |

### Retry Strategies

| Strategy | Use Case |
|----------|----------|
| Exponential Backoff | Default retry |
| Rate Limit | 429 responses |
| Max Retries | Avoid infinite loops (3-5) |

### Pagination Options

| Pattern | Language | Use Case |
|---------|----------|----------|
| Async Iterator | TypeScript, Python | Automatic pagination |
| Generator | Python | Sync pagination |
| Channels | Go | Concurrent iteration |
| Manual | All | Explicit control |

## Reference Documentation

**Architecture:**
- `references/architecture-patterns.md` - Resource vs. command organization

**Core Patterns:**
- `references/authentication.md` - OAuth, token refresh, credential providers
- `references/retry-backoff.md` - Exponential backoff, jitter, circuit breakers
- `references/error-handling.md` - Error hierarchies, debugging support
- `references/pagination.md` - Cursor vs. offset, async iterators
- `references/versioning.md` - SemVer, deprecation strategies
- `references/testing-sdks.md` - Unit testing, mocking, integration tests

## Code Examples

**TypeScript:**
- `examples/typescript/basic-client.ts` - Simple async SDK
- `examples/typescript/advanced-client.ts` - Retry, errors, streaming
- `examples/typescript/resource-based.ts` - Stripe-style organization

**Python:**
- `examples/python/sync-client.py` - Synchronous client
- `examples/python/async-client.py` - Async client with asyncio
- `examples/python/dual-client.py` - Both sync and async

**Go:**
- `examples/go/basic-client.go` - Simple Go client
- `examples/go/context-client.go` - Context patterns
- `examples/go/channel-pagination.go` - Channel-based pagination

## Best-in-Class SDK Examples

Study these production SDKs:

**TypeScript/JavaScript:**
- AWS SDK v3 (`@aws-sdk/client-*`): Modular, tree-shakeable, middleware
- Stripe Node (`stripe`): Resource-based, typed errors, excellent DX
- OpenAI Node (`openai`): Streaming, async iterators, modern TypeScript

**Python:**
- Boto3 (`boto3`): Resource vs. client patterns, paginators
- Stripe Python (`stripe`): Dual sync/async, context managers

**Go:**
- AWS SDK Go v2 (`github.com/aws/aws-sdk-go-v2`): Context, middleware

## Common Pitfalls

Avoid these mistakes:

1. **No Retry Logic** - All SDKs need automatic retries for transient errors
2. **Poor Error Messages** - Include request ID, status code, error type
3. **No Pagination** - Implement automatic pagination with async iterators
4. **Hardcoded Credentials** - Use environment variables or config files
5. **Missing Idempotency** - Add idempotency keys to prevent duplicate operations
6. **Ignoring Rate Limits** - Respect `Retry-After` header on 429 responses
7. **Breaking Changes** - Use SemVer, deprecate before removing

## Integration with Other Skills

- **api-design-principles**: API design complements SDK design (error codes → error classes)
- **building-clis**: CLIs wrap SDKs for command-line access
- **testing-strategies**: Test SDKs with mocked HTTP, retry scenarios

## Next Steps

Review language-specific examples for implementation details. Study references for deep dives on specific patterns. Examine best-in-class SDKs (Stripe, AWS, OpenAI) for inspiration.
