---
name: retry-fallback
description: Handle transient failures with exponential backoff and graceful fallbacks. Retry on network blips, fall back to cached data when services fail.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: resilience
  time: 2h
  source: drift-masterguide
---

# Retry & Fallback Patterns

Handle transient failures gracefully.

## When to Use This Skill

- Network requests that occasionally fail
- External services with temporary outages
- Need graceful degradation when dependencies fail
- Want to avoid cascading failures

## Core Concepts

1. **Exponential backoff** - Increasing delays between retries
2. **Jitter** - Random variation prevents thundering herd
3. **Fallback** - Alternative data source when primary fails
4. **Graceful degradation** - Reduced functionality beats total failure

## TypeScript Implementation

### Retry with Exponential Backoff

```typescript
// retry.ts
export interface RetryConfig {
  maxRetries: number;
  baseDelayMs: number;
  maxDelayMs: number;
  backoffMultiplier: number;
  jitter: boolean;
  retryableErrors?: (error: Error) => boolean;
}

const DEFAULT_CONFIG: RetryConfig = {
  maxRetries: 3,
  baseDelayMs: 1000,
  maxDelayMs: 30000,
  backoffMultiplier: 2,
  jitter: true,
};

function calculateDelay(attempt: number, config: RetryConfig): number {
  let delay = config.baseDelayMs * Math.pow(config.backoffMultiplier, attempt);
  delay = Math.min(delay, config.maxDelayMs);
  
  if (config.jitter) {
    const jitterRange = delay * 0.25;
    delay = delay + (Math.random() * jitterRange * 2 - jitterRange);
  }
  
  return Math.floor(delay);
}

function isRetryable(error: Error): boolean {
  const message = error.message.toLowerCase();
  return (
    message.includes('network') ||
    message.includes('timeout') ||
    message.includes('rate limit') ||
    message.includes('429') ||
    message.includes('503') ||
    message.includes('502')
  );
}

export async function retry<T>(
  fn: () => Promise<T>,
  config: Partial<RetryConfig> = {}
): Promise<T> {
  const cfg = { ...DEFAULT_CONFIG, ...config };
  const shouldRetry = cfg.retryableErrors || isRetryable;
  
  let lastError: Error;
  
  for (let attempt = 0; attempt <= cfg.maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));
      
      if (attempt === cfg.maxRetries || !shouldRetry(lastError)) {
        throw lastError;
      }
      
      const delay = calculateDelay(attempt, cfg);
      console.log(`[Retry] Attempt ${attempt + 1} failed, retrying in ${delay}ms`);
      
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw lastError!;
}
```

### Fallback Pattern

```typescript
// fallback.ts
export interface FallbackConfig<T> {
  timeout?: number;
  fallbackValue?: T;
  fallbackFn?: () => T | Promise<T>;
  onFallback?: (error: Error) => void;
}

export async function withFallback<T>(
  fn: () => Promise<T>,
  config: FallbackConfig<T>
): Promise<T> {
  const { timeout, fallbackValue, fallbackFn, onFallback } = config;
  
  try {
    if (timeout) {
      return await Promise.race([
        fn(),
        new Promise<never>((_, reject) =>
          setTimeout(() => reject(new Error('Timeout')), timeout)
        ),
      ]);
    }
    return await fn();
  } catch (error) {
    const err = error instanceof Error ? error : new Error(String(error));
    
    if (onFallback) onFallback(err);
    
    if (fallbackFn) return await fallbackFn();
    if (fallbackValue !== undefined) return fallbackValue;
    
    throw err;
  }
}

export async function tryMultiple<T>(
  sources: Array<() => Promise<T>>,
  options: { timeout?: number } = {}
): Promise<T> {
  const errors: Error[] = [];
  
  for (const source of sources) {
    try {
      if (options.timeout) {
        return await Promise.race([
          source(),
          new Promise<never>((_, reject) =>
            setTimeout(() => reject(new Error('Timeout')), options.timeout)
          ),
        ]);
      }
      return await source();
    } catch (error) {
      errors.push(error instanceof Error ? error : new Error(String(error)));
    }
  }
  
  throw new AggregateError(errors, 'All sources failed');
}
```

### Combined: Retry with Fallback

```typescript
// resilient-fetch.ts
export async function resilientFetch<T>(
  fn: () => Promise<T>,
  config: {
    retry?: Partial<RetryConfig>;
    fallback?: FallbackConfig<T>;
  } = {}
): Promise<T> {
  const withRetryFn = config.retry
    ? () => retry(fn, config.retry)
    : fn;
  
  if (config.fallback) {
    return withFallback(withRetryFn, config.fallback);
  }
  
  return withRetryFn();
}
```

## Python Implementation

```python
# retry.py
import asyncio
import random
from typing import Callable, TypeVar, Optional
from functools import wraps

T = TypeVar('T')

class RetryConfig:
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 30.0,
        backoff_multiplier: float = 2.0,
        jitter: bool = True,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_multiplier = backoff_multiplier
        self.jitter = jitter


def calculate_delay(attempt: int, config: RetryConfig) -> float:
    delay = config.base_delay * (config.backoff_multiplier ** attempt)
    delay = min(delay, config.max_delay)
    
    if config.jitter:
        jitter_range = delay * 0.25
        delay = delay + random.uniform(-jitter_range, jitter_range)
    
    return delay


async def retry(
    fn: Callable[[], T],
    config: Optional[RetryConfig] = None,
    retryable: Optional[Callable[[Exception], bool]] = None,
) -> T:
    config = config or RetryConfig()
    
    def is_retryable(error: Exception) -> bool:
        if retryable:
            return retryable(error)
        msg = str(error).lower()
        return any(x in msg for x in ['network', 'timeout', '429', '503'])
    
    last_error: Exception = Exception("No attempts made")
    
    for attempt in range(config.max_retries + 1):
        try:
            return await fn()
        except Exception as e:
            last_error = e
            
            if attempt == config.max_retries or not is_retryable(e):
                raise
            
            delay = calculate_delay(attempt, config)
            print(f"[Retry] Attempt {attempt + 1} failed, retrying in {delay:.1f}s")
            await asyncio.sleep(delay)
    
    raise last_error


def with_retry(config: Optional[RetryConfig] = None):
    """Decorator for retry."""
    def decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            return await retry(lambda: fn(*args, **kwargs), config)
        return wrapper
    return decorator


# Fallback
async def with_fallback(
    fn: Callable[[], T],
    fallback: T | Callable[[], T],
    timeout: Optional[float] = None,
) -> T:
    try:
        if timeout:
            return await asyncio.wait_for(fn(), timeout=timeout)
        return await fn()
    except Exception as e:
        print(f"[Fallback] Primary failed: {e}")
        if callable(fallback):
            return await fallback() if asyncio.iscoroutinefunction(fallback) else fallback()
        return fallback
```

## Usage Examples

### Basic Retry

```typescript
const data = await retry(
  () => fetch('https://api.example.com/data').then(r => r.json()),
  { maxRetries: 3 }
);
```

### Retry with Custom Logic

```typescript
const result = await retry(
  () => processPayment(order),
  {
    maxRetries: 5,
    baseDelayMs: 2000,
    retryableErrors: (error) => error.message.includes('temporary'),
  }
);
```

### Fallback to Cache

```typescript
const data = await withFallback(
  () => fetchFromAPI(),
  {
    timeout: 5000,
    fallbackFn: () => getFromCache(),
    onFallback: (error) => {
      console.warn('Using cached data:', error.message);
    },
  }
);
```

### Try Multiple Sources

```typescript
const user = await tryMultiple([
  () => fetchFromPrimaryDB(userId),
  () => fetchFromReplicaDB(userId),
  () => fetchFromCache(userId),
], { timeout: 3000 });
```

### Combined Pattern

```typescript
const dashboard = await resilientFetch(
  () => fetchFromMLPipeline(),
  {
    retry: { maxRetries: 2, baseDelayMs: 500 },
    fallback: {
      timeout: 5000,
      fallbackFn: async () => {
        const snapshot = await fetchLatestSnapshot();
        return snapshot || { status: 'degraded', data: getCachedData() };
      },
    },
  }
);
```

## Graceful Degradation

```typescript
interface DegradedResponse<T> {
  data: T;
  degraded: boolean;
  message?: string;
}

async function withDegradation<T>(
  fullFn: () => Promise<T>,
  degradedFn: () => Promise<T>,
  minimalFn: () => T
): Promise<DegradedResponse<T>> {
  try {
    return { data: await fullFn(), degraded: false };
  } catch {
    try {
      return { data: await degradedFn(), degraded: true, message: 'Some features unavailable' };
    } catch {
      return { data: minimalFn(), degraded: true, message: 'Limited functionality' };
    }
  }
}

// Usage
const response = await withDegradation(
  () => fetchRealtimeAnalytics(),
  () => fetchCachedAnalytics(),
  () => ({ message: 'Analytics unavailable', data: [] })
);
```

## Best Practices

1. **Only retry transient errors** - Don't retry 400 Bad Request
2. **Use jitter** - Prevents thundering herd
3. **Set max delay** - Don't wait forever
4. **Log retries** - Track retry frequency
5. **Have fallbacks** - Always have a backup plan

## Common Mistakes

- Retrying non-transient errors (400, 401, 404)
- No jitter (all instances retry simultaneously)
- Infinite retries (no max)
- No fallback for critical paths
- Not logging retry attempts

## Related Skills

- [Circuit Breaker](../circuit-breaker/)
- [Graceful Degradation](../graceful-degradation/)
- [Caching Strategies](../caching-strategies/)
