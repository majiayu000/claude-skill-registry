---
name: resilient-connections
model: standard
description: Patterns for building resilient API clients and real-time connections with retry logic, circuit breakers, and graceful degradation. Use when building production systems that need to handle failures. Triggers on retry logic, circuit breaker, connection resilience, exponential backoff, API client, fault tolerance.
---

# Resilient Connections

Build API clients and real-time connections that handle failures gracefully with retries, circuit breakers, and fallbacks.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install resilient-connections
```


---

## When to Use

- Building API clients that need to handle transient failures
- Real-time connections that should reconnect automatically
- Systems that need graceful degradation
- Any production system calling external services

---

## Pattern 1: Exponential Backoff

```typescript
interface RetryOptions {
  maxRetries: number;
  baseDelay: number;
  maxDelay: number;
  jitter?: boolean;
}

async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions
): Promise<T> {
  const { maxRetries, baseDelay, maxDelay, jitter = true } = options;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) throw error;

      // Calculate delay with exponential backoff
      let delay = Math.min(baseDelay * 2 ** attempt, maxDelay);
      
      // Add jitter to prevent thundering herd
      if (jitter) {
        delay = delay * (0.5 + Math.random());
      }

      await sleep(delay);
    }
  }

  throw new Error('Unreachable');
}

// Usage
const data = await withRetry(
  () => fetch('/api/data').then(r => r.json()),
  { maxRetries: 3, baseDelay: 1000, maxDelay: 30000 }
);
```

---

## Pattern 2: Circuit Breaker

```typescript
enum CircuitState {
  Closed,    // Normal operation
  Open,      // Failing, reject requests
  HalfOpen,  // Testing if recovered
}

class CircuitBreaker {
  private state = CircuitState.Closed;
  private failures = 0;
  private lastFailure = 0;
  
  constructor(
    private threshold: number = 5,
    private timeout: number = 30000
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === CircuitState.Open) {
      if (Date.now() - this.lastFailure > this.timeout) {
        this.state = CircuitState.HalfOpen;
      } else {
        throw new Error('Circuit breaker is open');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failures = 0;
    this.state = CircuitState.Closed;
  }

  private onFailure() {
    this.failures++;
    this.lastFailure = Date.now();
    
    if (this.failures >= this.threshold) {
      this.state = CircuitState.Open;
    }
  }
}
```

---

## Pattern 3: Resilient Fetch Wrapper

```typescript
interface FetchOptions extends RequestInit {
  timeout?: number;
  retries?: number;
}

async function resilientFetch(
  url: string,
  options: FetchOptions = {}
): Promise<Response> {
  const { timeout = 10000, retries = 3, ...fetchOptions } = options;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  const fetchWithTimeout = async () => {
    try {
      const response = await fetch(url, {
        ...fetchOptions,
        signal: controller.signal,
      });

      if (!response.ok && response.status >= 500) {
        throw new Error(`Server error: ${response.status}`);
      }

      return response;
    } finally {
      clearTimeout(timeoutId);
    }
  };

  return withRetry(fetchWithTimeout, {
    maxRetries: retries,
    baseDelay: 1000,
    maxDelay: 10000,
  });
}
```

---

## Pattern 4: Reconnecting WebSocket

```typescript
class ReconnectingWebSocket {
  private ws: WebSocket | null = null;
  private retries = 0;
  private maxRetries = 10;

  constructor(
    private url: string,
    private onMessage: (data: unknown) => void
  ) {
    this.connect();
  }

  private connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      this.retries = 0;
    };

    this.ws.onmessage = (event) => {
      this.onMessage(JSON.parse(event.data));
    };

    this.ws.onclose = () => {
      if (this.retries < this.maxRetries) {
        const delay = Math.min(1000 * 2 ** this.retries, 30000);
        this.retries++;
        setTimeout(() => this.connect(), delay);
      }
    };
  }

  send(data: unknown) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  close() {
    this.maxRetries = 0; // Prevent reconnection
    this.ws?.close();
  }
}
```

---

## Pattern 5: Graceful Degradation

```typescript
async function fetchWithFallback<T>(
  primary: () => Promise<T>,
  fallback: () => Promise<T>,
  cache?: T
): Promise<T> {
  try {
    return await primary();
  } catch (primaryError) {
    console.warn('Primary failed, trying fallback:', primaryError);
    
    try {
      return await fallback();
    } catch (fallbackError) {
      console.warn('Fallback failed:', fallbackError);
      
      if (cache !== undefined) {
        console.warn('Using cached data');
        return cache;
      }
      
      throw fallbackError;
    }
  }
}

// Usage
const data = await fetchWithFallback(
  () => fetchFromPrimaryAPI(),
  () => fetchFromBackupAPI(),
  cachedData
);
```

---

## Related Skills

- **Meta-skill:** [ai/skills/meta/realtime-dashboard/](../../meta/realtime-dashboard/) — Complete realtime dashboard guide
- [realtime-react-hooks](../realtime-react-hooks/) — Hook usage
- [websocket-hub-patterns](../websocket-hub-patterns/) — Server patterns

---

## NEVER Do

- **NEVER retry non-idempotent requests** — POST/PUT might succeed but fail to respond
- **NEVER use fixed delays** — Always add jitter to prevent thundering herd
- **NEVER retry 4xx errors** — Client errors won't resolve themselves
- **NEVER keep circuit open forever** — Always have a timeout to half-open
- **NEVER hide connection failures** — Show users the degraded state

---

## Quick Reference

```typescript
// Exponential backoff
const delay = Math.min(baseDelay * 2 ** attempt, maxDelay);

// With jitter
const jitteredDelay = delay * (0.5 + Math.random());

// Retry check
const shouldRetry = 
  error.status >= 500 || 
  error.code === 'ETIMEDOUT' ||
  error.code === 'ECONNRESET';

// Circuit breaker states
Closed -> (failures >= threshold) -> Open
Open -> (timeout elapsed) -> HalfOpen
HalfOpen -> (success) -> Closed
HalfOpen -> (failure) -> Open
```
