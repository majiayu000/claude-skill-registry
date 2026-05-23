---
name: http-client-patterns
description: HTTP client patterns for axios configuration, interceptors, and request handling
---

# HTTP Client Implementation Patterns

## Core Principles

1. **ALL errors mapped to core types** - never generic Error
2. **Proper connection cleanup** - no resource leaks
3. **Appropriate timeouts** - prevent hanging
4. **Retry logic** for transient failures only
5. **No credential exposure** in error messages
6. **Real connection validation** - not just state checks

See error-handling skill for complete error mapping reference.

## Client Class Structure

### Basic Client Implementation

```typescript
class GitHubClient {
  private httpClient: AxiosInstance;
  private token?: string;
  private baseUrl: string;

  async connect(profile: ConnectionProfile): Promise<void> {
    // Configure HTTP client
    this.baseUrl = profile.endpoint || 'https://api.github.com';
    this.token = profile.credentials.token;

    // Set up HTTP client
    this.httpClient = axios.create({
      baseURL: this.baseUrl,
      timeout: 30000,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });

    // Set up interceptors
    this.setupInterceptors();

    // Validate connection with real API call
    await this.isConnected();

    // Return void (not ConnectionState)
  }

  async isConnected(): Promise<boolean> {
    try {
      // Real API call to verify - NOT just checking stored state
      await this.httpClient.get('/user');
      return true;
    } catch {
      return false;
    }
  }

  async disconnect(): Promise<void> {
    // Clean up resources
    this.httpClient = undefined;
    this.token = undefined;
    // Clear any cached data
  }
}
```

**Key points:**
- `connect()` returns `Promise<void>` (not ConnectionState)
- `isConnected()` makes real API call (not state check)
- `disconnect()` cleans up all resources
- Use axios or similar HTTP client library

## HTTP Client Configuration

### Axios Client Setup

```typescript
const client = axios.create({
  baseURL: this.baseUrl,
  timeout: 30000,  // 30 seconds
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
});
```

**Configuration options:**
- `baseURL` - API endpoint from connection profile
- `timeout` - Reasonable timeout (30s typical)
- `headers` - Accept and content-type for JSON APIs

### Request Interceptor (Authentication)

```typescript
// Request interceptor for auth
client.interceptors.request.use(config => {
  if (this.token) {
    config.headers.Authorization = `Bearer ${this.token}`;
  }
  return config;
});
```

**Use cases:**
- Add authentication headers
- Add request ID for tracing
- Log requests (without credentials!)

### Response Interceptor (Error Handling)

```typescript
// Response interceptor for errors
client.interceptors.response.use(
  response => response,
  error => this.handleApiError(error)
);
```

## Error Handling Patterns

### HTTP Status to Core Error Mapping

```typescript
private handleApiError(error: any): never {
  const status = error.response?.status || 500;
  const message = error.response?.data?.message || error.message;

  switch (status) {
    case 401:
      throw new InvalidCredentialsError();

    case 403:
      throw new UnauthorizedError();

    case 404:
      throw new NoSuchObjectError('resource', 'id');

    case 429:
      throw new RateLimitExceededError();

    case 500:
    case 502:
    case 503:
      throw new ServiceUnavailableError();

    default:
      throw new UnexpectedError(`API error: ${message}`, status);
  }
}
```

**Critical rules:**
- ALWAYS map to core error types (see error-handling skill)
- NEVER throw generic `Error` or leave unhandled
- Include status code in UnexpectedError
- Don't expose credentials in error messages

### Safe Error Messages

```typescript
// ❌ WRONG - Exposes credentials
throw new Error(`Failed to connect with token ${this.token}`);

// ✅ CORRECT - Safe error message
throw new InvalidCredentialsError();
```

## Producer Pattern

### Basic Producer Structure

```typescript
class UserProducer {
  constructor(private client: GitHubClient) {}

  async list(): Promise<User[]> {
    const response = await this.client.get('/users');

    // Validate response format
    if (!Array.isArray(response.data)) {
      throw new UnexpectedError('Invalid response format');
    }

    // Map to internal types
    return response.data.map(toUser);
  }

  async get(id: string): Promise<User> {
    const response = await this.client.get(`/users/${id}`);
    return toUser(response.data);
  }

  async create(data: CreateUserRequest): Promise<User> {
    const response = await this.client.post('/users', data);
    return toUser(response.data);
  }

  async update(id: string, data: UpdateUserRequest): Promise<User> {
    const response = await this.client.put(`/users/${id}`, data);
    return toUser(response.data);
  }

  async delete(id: string): Promise<void> {
    await this.client.delete(`/users/${id}`);
  }
}
```

**Key patterns:**
- Producer depends on client (injected)
- Each operation is async method
- Use mapper functions to convert responses
- Validate response format before mapping
- Return appropriate types (arrays, objects, void)

## Connection Validation

### Pattern: Real API Call

```typescript
async isConnected(): Promise<boolean> {
  try {
    // Real API call - lightweight endpoint
    await this.client.get('/user');
    return true;
  } catch {
    return false;
  }
}
```

**Why real API call:**
- Verifies network connectivity
- Confirms credentials still valid
- Detects API availability
- Not just checking stored state

**Anti-pattern:**
```typescript
// ❌ WRONG - Just checking state
async isConnected(): Promise<boolean> {
  return this.token !== undefined;
}
```

## Retry Logic

### Pattern: Exponential Backoff

```typescript
// For transient failures only (5xx errors, timeouts)
async function withRetry<T>(
  operation: () => Promise<T>,
  maxAttempts = 3
): Promise<T> {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      return await operation();
    } catch (error) {
      // Don't retry client errors (4xx)
      if (error.response?.status >= 400 && error.response?.status < 500) {
        throw error;
      }

      // Last attempt - throw error
      if (i === maxAttempts - 1) {
        throw error;
      }

      // Exponential backoff: 1s, 2s, 4s
      await delay(Math.pow(2, i) * 1000);
    }
  }
}

function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

**Retry rules:**
- Only retry transient failures (5xx, network errors)
- NEVER retry client errors (4xx) - they won't succeed
- Use exponential backoff (1s, 2s, 4s)
- Limit retries (3 attempts typical)

### Using Retry in Client

```typescript
async get(path: string): Promise<any> {
  return withRetry(() => this.httpClient.get(path));
}
```

## Response Validation

### Validate Before Mapping

```typescript
async list(): Promise<User[]> {
  const response = await this.client.get('/users');

  // ✅ CORRECT - Validate response format
  if (!Array.isArray(response.data)) {
    throw new UnexpectedError('Invalid response format: expected array');
  }

  return response.data.map(toUser);
}
```

**Validation checks:**
- Array responses: `Array.isArray(data)`
- Object responses: `typeof data === 'object' && data !== null`
- Required fields: `if (!data.id) throw ...`

## Timeout Configuration

### Setting Timeouts

```typescript
const client = axios.create({
  baseURL: this.baseUrl,
  timeout: 30000,  // 30 seconds (typical)
});
```

**Timeout guidelines:**
- **Fast operations** (list, get): 10-30 seconds
- **Slow operations** (search, reports): 60-120 seconds
- **Long-running** (exports, batch): 300+ seconds
- **Default**: 30 seconds

### Per-Request Timeout

```typescript
async longRunningOperation(): Promise<Result> {
  return this.client.get('/export', {
    timeout: 120000  // 2 minutes for this specific call
  });
}
```

## Connection Cleanup

### Proper Disconnect Pattern

```typescript
async disconnect(): Promise<void> {
  // Clear client reference
  this.httpClient = undefined;

  // Clear credentials
  this.token = undefined;

  // Clear any cached data
  this.cache?.clear();

  // Cancel pending requests (if using axios)
  this.cancelTokenSource?.cancel('Connection closed');
}
```

**Cleanup checklist:**
- Clear HTTP client reference
- Clear authentication tokens
- Clear cached data
- Cancel pending requests
- Remove event listeners (if any)

## Quality Standards

### Zero Tolerance For:
- Unhandled promise rejections
- Memory leaks in connections
- Synchronous blocking operations
- Missing error handling
- Generic Error thrown
- Credentials in error messages

### Must Ensure:
- All errors mapped to core types
- Proper connection cleanup
- Appropriate timeouts set
- Retry logic for transient failures only
- Real connection validation
- Response validation before mapping

## Common Anti-Patterns

### ❌ WRONG: Generic Errors

```typescript
throw new Error('API call failed');  // Generic!
```

### ✅ CORRECT: Core Error Types

```typescript
throw new ServiceUnavailableError();  // Core type
```

### ❌ WRONG: No Response Validation

```typescript
return response.data.map(toUser);  // What if not array?
```

### ✅ CORRECT: Validate First

```typescript
if (!Array.isArray(response.data)) {
  throw new UnexpectedError('Invalid response format');
}
return response.data.map(toUser);
```

### ❌ WRONG: State-Based Connection Check

```typescript
async isConnected(): Promise<boolean> {
  return this.token !== undefined;  // Just checking state!
}
```

### ✅ CORRECT: Real API Call

```typescript
async isConnected(): Promise<boolean> {
  try {
    await this.client.get('/user');
    return true;
  } catch {
    return false;
  }
}
```

## Testing Patterns

### Mock HTTP Responses (with nock)

```typescript
import nock from 'nock';

describe('UserProducer', () => {
  it('should list users', async () => {
    nock('https://api.github.com')
      .get('/users')
      .reply(200, [
        { id: '1', name: 'Alice' },
        { id: '2', name: 'Bob' }
      ]);

    const users = await producer.list();
    expect(users).toHaveLength(2);
  });
});
```

See nock-patterns skill for complete mocking patterns.

## Success Metrics

HTTP client implementation MUST meet all criteria:

- ✅ All API calls succeed in integration tests
- ✅ Proper error handling coverage (all status codes)
- ✅ No connection leaks (cleanup verified)
- ✅ Optimal performance (timeouts configured)
- ✅ Clean retry patterns (transient failures only)
- ✅ All errors map to core types (ZERO generic errors)
- ✅ Response validation before mapping
- ✅ Real connection validation (not state-based)
