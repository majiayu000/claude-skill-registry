---
name: rate-limiting
model: standard
description: Rate limiting algorithms, implementation strategies, HTTP conventions, tiered limits, distributed patterns, and client-side handling. Use when protecting APIs from abuse, implementing usage tiers, or configuring gateway-level throttling.
---

# Rate Limiting Patterns

## Algorithms

| Algorithm | Accuracy | Burst Handling | Best For |
|-----------|----------|----------------|----------|
| **Token Bucket** | High | Allows controlled bursts | API rate limiting, traffic shaping |
| **Leaky Bucket** | High | Smooths bursts entirely | Steady-rate processing, queues |
| **Fixed Window** | Low | Allows edge bursts (2x) | Simple use cases, prototyping |
| **Sliding Window Log** | Very High | Precise control | Strict compliance, billing-critical |
| **Sliding Window Counter** | High | Good approximation | **Production APIs — best tradeoff** |

**Fixed window problem:** A user sends the full limit at 11:59 and again at 12:01, doubling the effective rate. Sliding window fixes this.

### Token Bucket

Bucket holds tokens up to capacity. Tokens refill at a fixed rate. Each request consumes one.

```python
class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.last_refill = time.monotonic()

    def allow(self) -> bool:
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

### Sliding Window Counter

Hybrid of fixed window and sliding window log — weights the previous window's count by overlap percentage:

```python
def sliding_window_allow(key: str, limit: int, window_sec: int) -> bool:
    now = time.time()
    current_window = int(now // window_sec)
    position_in_window = (now % window_sec) / window_sec

    prev_count = get_count(key, current_window - 1)
    curr_count = get_count(key, current_window)

    estimated = prev_count * (1 - position_in_window) + curr_count
    if estimated >= limit:
        return False
    increment_count(key, current_window)
    return True
```


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install rate-limiting
```


---

## Implementation Options

| Approach | Scope | Best For |
|----------|-------|----------|
| **In-memory** | Single server | Zero latency, no dependencies |
| **Redis** (`INCR` + `EXPIRE`) | Distributed | **Multi-instance deployments** |
| **API Gateway** | Edge | No code, built-in dashboards |
| **Middleware** | Per-service | Fine-grained per-user/endpoint control |

Use gateway-level limiting as outer defense + application-level for fine-grained control.

---

## HTTP Headers

Always return rate limit info, even on successful requests:

```
RateLimit-Limit: 1000
RateLimit-Remaining: 742
RateLimit-Reset: 1625097600
Retry-After: 30
```

| Header | When to Include |
|--------|-----------------|
| `RateLimit-Limit` | Every response |
| `RateLimit-Remaining` | Every response |
| `RateLimit-Reset` | Every response |
| `Retry-After` | 429 responses only |

### 429 Response Body

```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Rate limit exceeded. Maximum 1000 requests per hour.",
    "retry_after": 30,
    "limit": 1000,
    "reset_at": "2025-07-01T12:00:00Z"
  }
}
```

Never return `500` or `503` for rate limiting — `429` is the correct status code.

---

## Rate Limit Tiers

Apply limits at multiple granularities:

| Scope | Key | Example Limit | Purpose |
|-------|-----|---------------|---------|
| **Per-IP** | Client IP | 100 req/min | Abuse prevention |
| **Per-User** | User ID | 1000 req/hr | Fair usage |
| **Per-API-Key** | API key | 5000 req/hr | Service-to-service |
| **Per-Endpoint** | Route + key | 60 req/min on `/search` | Protect expensive ops |

**Tiered pricing:**

| Tier | Rate Limit | Burst | Cost |
|------|-----------|-------|------|
| Free | 100 req/hr | 10 | $0 |
| Pro | 5,000 req/hr | 100 | $49/mo |
| Enterprise | 100,000 req/hr | 2,000 | Custom |

Evaluate from most specific to least specific: per-endpoint > per-user > per-IP.

---

## Distributed Rate Limiting

Redis-based pattern for consistent limiting across instances:

```python
def redis_rate_limit(redis, key: str, limit: int, window: int) -> bool:
    pipe = redis.pipeline()
    now = time.time()
    window_key = f"rl:{key}:{int(now // window)}"
    pipe.incr(window_key)
    pipe.expire(window_key, window * 2)
    results = pipe.execute()
    return results[0] <= limit
```

**Atomic Lua script** (prevents race conditions):

```lua
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local current = redis.call('INCR', key)
if current == 1 then
    redis.call('EXPIRE', key, window)
end
return current <= limit and 1 or 0
```

Never do separate GET then SET — the gap allows overcount.

---

## API Gateway Configuration

**NGINX:**

```nginx
http {
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    server {
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            limit_req_status 429;
        }
    }
}
```

**Kong:**

```yaml
plugins:
  - name: rate-limiting
    config:
      minute: 60
      hour: 1000
      policy: redis
      redis_host: redis.internal
```

---

## Client-Side Handling

Clients must handle `429` gracefully:

```typescript
async function fetchWithRetry(url: string, maxRetries = 3): Promise<Response> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    const res = await fetch(url);
    if (res.status !== 429) return res;

    const retryAfter = res.headers.get('Retry-After');
    const delay = retryAfter
      ? parseInt(retryAfter, 10) * 1000
      : Math.min(1000 * 2 ** attempt, 30000);
    await new Promise(r => setTimeout(r, delay));
  }
  throw new Error('Rate limit exceeded after retries');
}
```

- Always respect `Retry-After` when present
- Use exponential backoff with jitter when absent
- Implement request queuing for batch operations

---

## Monitoring

Track these metrics:

- **Rate limit hit rate** — % of requests returning 429 (alert if >5% sustained)
- **Near-limit warnings** — requests where remaining < 10% of limit
- **Top offenders** — keys/IPs hitting limits most frequently
- **Limit headroom** — how close normal traffic is to the ceiling
- **False positives** — legitimate users being rate limited

---

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| **Application-only limiting** | Always combine with infrastructure-level limits |
| **No retry guidance** | Always include `Retry-After` header on 429 |
| **Inconsistent limits** | Same endpoint, same limits across services |
| **No burst allowance** | Allow controlled bursts for legitimate traffic |
| **Silent dropping** | Always return 429 so clients can distinguish from errors |
| **Global single counter** | Per-endpoint counters to protect expensive operations |
| **Hard-coded limits** | Use configuration, not code constants |

---

## NEVER Do

1. **NEVER rate limit health check endpoints** — monitoring systems will false-alarm
2. **NEVER use client-supplied identifiers as sole rate limit key** — trivially spoofed
3. **NEVER return `200 OK` when rate limiting** — clients must know they were throttled
4. **NEVER set limits without measuring actual traffic first** — you'll block legitimate users or set limits too high to matter
5. **NEVER share counters across unrelated tenants** — noisy neighbor problem
6. **NEVER skip rate limiting on internal APIs** — misbehaving internal services can take down shared infrastructure
7. **NEVER implement rate limiting without logging** — you need visibility to tune limits and detect abuse
