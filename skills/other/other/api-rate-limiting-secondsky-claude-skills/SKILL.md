---
name: api-rate-limiting
description: Implements API rate limiting using token bucket, sliding window, and Redis-based algorithms to protect against abuse. Use when securing public APIs, implementing tiered access, or preventing denial-of-service attacks.
---

# API Rate Limiting

Protect APIs from abuse using rate limiting algorithms with per-user and per-endpoint strategies.

## Algorithms

| Algorithm | Pros | Cons |
|-----------|------|------|
| Token Bucket | Handles bursts, smooth | Memory per user |
| Sliding Window | Accurate | Memory intensive |
| Fixed Window | Simple | Boundary spikes |

## Token Bucket (Node.js)

```javascript
class TokenBucket {
  constructor(capacity, refillRate) {
    this.capacity = capacity;
    this.tokens = capacity;
    this.refillRate = refillRate; // tokens per second
    this.lastRefill = Date.now();
  }

  consume() {
    this.refill();
    if (this.tokens >= 1) {
      this.tokens--;
      return true;
    }
    return false;
  }

  refill() {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000;
    this.tokens = Math.min(this.capacity, this.tokens + elapsed * this.refillRate);
    this.lastRefill = now;
  }
}
```

## Express Middleware

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  standardHeaders: true,
  message: { error: 'Too many requests, try again later' }
});

app.use('/api/', limiter);
```

## Response Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1705320000
Retry-After: 60
```

## Tiered Limits

| Tier | Requests/Hour |
|------|---------------|
| Free | 100 |
| Pro | 1,000 |
| Enterprise | 10,000 |

## Best Practices

- Use Redis for distributed rate limiting
- Include proper headers in responses
- Return 429 status with Retry-After
- Implement tiered limits for different plans
- Monitor rate limit metrics
- Test under load
