---
name: api-rate-limiting
description: Implement API rate limiting strategies using token bucket, sliding window, and fixed window algorithms. Use when protecting APIs from abuse, managing traffic, or implementing tiered rate limits.
---

# API Rate Limiting

## Overview

Protect APIs from abuse and manage traffic using various rate limiting algorithms with per-user, per-IP, and per-endpoint strategies.

## When to Use

- Protecting APIs from brute force attacks
- Managing traffic spikes
- Implementing tiered service plans
- Preventing DoS attacks
- Fairness in resource allocation
- Enforcing quotas and usage limits

## Instructions

### 1. **Token Bucket Algorithm**

```javascript
// Token Bucket Rate Limiter
class TokenBucket {
  constructor(capacity, refillRate) {
    this.capacity = capacity;
    this.tokens = capacity;
    this.refillRate = refillRate; // tokens per second
    this.lastRefillTime = Date.now();
  }

  refill() {
    const now = Date.now();
    const timePassed = (now - this.lastRefillTime) / 1000;
    const tokensToAdd = timePassed * this.refillRate;

    this.tokens = Math.min(this.capacity, this.tokens + tokensToAdd);
    this.lastRefillTime = now;
  }

  consume(tokens = 1) {
    this.refill();

    if (this.tokens >= tokens) {
      this.tokens -= tokens;
      return true;
    }
    return false;
  }

  available() {
    this.refill();
    return Math.floor(this.tokens);
  }
}

// Express middleware
const express = require('express');
const app = express();

const rateLimiters = new Map();

const tokenBucketRateLimit = (capacity, refillRate) => {
  return (req, res, next) => {
    const key = req.user?.id || req.ip;

    if (!rateLimiters.has(key)) {
      rateLimiters.set(key, new TokenBucket(capacity, refillRate));
    }

    const limiter = rateLimiters.get(key);

    if (limiter.consume(1)) {
      res.setHeader('X-RateLimit-Limit', capacity);
      res.setHeader('X-RateLimit-Remaining', limiter.available());
      next();
    } else {
      res.status(429).json({
        error: 'Rate limit exceeded',
        retryAfter: Math.ceil(1 / limiter.refillRate)
      });
    }
  };
};

app.get('/api/data', tokenBucketRateLimit(100, 10), (req, res) => {
  res.json({ data: 'api response' });
});
```

### 2. **Sliding Window Algorithm**

```javascript
class SlidingWindowLimiter {
  constructor(maxRequests, windowSizeSeconds) {
    this.maxRequests = maxRequests;
    this.windowSize = windowSizeSeconds * 1000; // Convert to ms
    this.requests = [];
  }

  isAllowed() {
    const now = Date.now();
    const windowStart = now - this.windowSize;

    // Remove old requests outside window
    this.requests = this.requests.filter(time => time > windowStart);

    if (this.requests.length < this.maxRequests) {
      this.requests.push(now);
      return true;
    }
    return false;
  }

  remaining() {
    const now = Date.now();
    const windowStart = now - this.windowSize;
    this.requests = this.requests.filter(time => time > windowStart);
    return Math.max(0, this.maxRequests - this.requests.length);
  }
}

const slidingWindowRateLimit = (maxRequests, windowSeconds) => {
  const limiters = new Map();

  return (req, res, next) => {
    const key = req.user?.id || req.ip;

    if (!limiters.has(key)) {
      limiters.set(key, new SlidingWindowLimiter(maxRequests, windowSeconds));
    }

    const limiter = limiters.get(key);

    if (limiter.isAllowed()) {
      res.setHeader('X-RateLimit-Limit', maxRequests);
      res.setHeader('X-RateLimit-Remaining', limiter.remaining());
      next();
    } else {
      res.status(429).json({ error: 'Rate limit exceeded' });
    }
  };
};

app.get('/api/search', slidingWindowRateLimit(30, 60), (req, res) => {
  res.json({ results: [] });
});
```

### 3. **Redis-Based Rate Limiting**

```javascript
const redis = require('redis');
const client = redis.createClient();

// Sliding window with Redis
const redisRateLimit = (maxRequests, windowSeconds) => {
  return async (req, res, next) => {
    const key = `ratelimit:${req.user?.id || req.ip}`;
    const now = Date.now();
    const windowStart = now - (windowSeconds * 1000);

    try {
      // Remove old requests
      await client.zremrangebyscore(key, 0, windowStart);

      // Count requests in window
      const count = await client.zcard(key);

      if (count < maxRequests) {
        // Add current request
        await client.zadd(key, now, `${now}-${Math.random()}`);
        // Set expiration
        await client.expire(key, windowSeconds);

        res.setHeader('X-RateLimit-Limit', maxRequests);
        res.setHeader('X-RateLimit-Remaining', maxRequests - count - 1);
        next();
      } else {
        const oldestRequest = await client.zrange(key, 0, 0);
        const resetTime = parseInt(oldestRequest[0]) + (windowSeconds * 1000);
        const retryAfter = Math.ceil((resetTime - now) / 1000);

        res.set('Retry-After', retryAfter);
        res.status(429).json({
          error: 'Rate limit exceeded',
          retryAfter
        });
      }
    } catch (error) {
      console.error('Rate limit error:', error);
      next(); // Allow request if Redis fails
    }
  };
};

app.get('/api/expensive', redisRateLimit(10, 60), (req, res) => {
  res.json({ result: 'expensive operation' });
});
```

### 4. **Tiered Rate Limiting**

```javascript
const RATE_LIMITS = {
  free: { requests: 100, window: 3600 },      // 100 per hour
  pro: { requests: 10000, window: 3600 },     // 10,000 per hour
  enterprise: { requests: null, window: null } // Unlimited
};

const tieredRateLimit = async (req, res, next) => {
  const user = req.user;
  const plan = user?.plan || 'free';
  const limits = RATE_LIMITS[plan];

  if (!limits.requests) {
    return next(); // Unlimited plan
  }

  const key = `ratelimit:${user.id}`;
  const now = Date.now();
  const windowStart = now - (limits.window * 1000);

  try {
    await client.zremrangebyscore(key, 0, windowStart);
    const count = await client.zcard(key);

    if (count < limits.requests) {
      await client.zadd(key, now, `${now}-${Math.random()}`);
      await client.expire(key, limits.window);

      res.setHeader('X-RateLimit-Limit', limits.requests);
      res.setHeader('X-RateLimit-Remaining', limits.requests - count - 1);
      res.setHeader('X-Plan', plan);
      next();
    } else {
      res.status(429).json({
        error: 'Rate limit exceeded',
        plan,
        upgradeUrl: '/plans'
      });
    }
  } catch (error) {
    next();
  }
};

app.use(tieredRateLimit);
```

### 5. **Python Rate Limiting (Flask)**

```python
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timedelta
import redis

app = Flask(__name__)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Custom rate limit based on user plan
redis_client = redis.Redis(host='localhost', port=6379)

def get_rate_limit(user_id):
    plan = redis_client.get(f'user:{user_id}:plan').decode()
    limits = {
        'free': (100, 3600),
        'pro': (10000, 3600),
        'enterprise': (None, None)
    }
    return limits.get(plan, (100, 3600))

@app.route('/api/data', methods=['GET'])
@limiter.limit("30 per minute")
def get_data():
    return jsonify({'data': 'api response'}), 200

@app.route('/api/premium', methods=['GET'])
def get_premium_data():
    user_id = request.user_id
    max_requests, window = get_rate_limit(user_id)

    if max_requests is None:
        return jsonify({'data': 'unlimited data'}), 200

    key = f'ratelimit:{user_id}'
    current = redis_client.incr(key)
    redis_client.expire(key, window)

    if current <= max_requests:
        return jsonify({'data': 'premium data'}), 200
    else:
        return jsonify({'error': 'Rate limit exceeded'}), 429
```

### 6. **Response Headers**

```javascript
// Standard rate limit headers
res.setHeader('X-RateLimit-Limit', maxRequests);          // Total requests allowed
res.setHeader('X-RateLimit-Remaining', remaining);        // Remaining requests
res.setHeader('X-RateLimit-Reset', resetTime);            // Unix timestamp of reset
res.setHeader('Retry-After', secondsToWait);              // How long to wait

// 429 Too Many Requests response
{
  "error": "Rate limit exceeded",
  "code": "RATE_LIMIT_EXCEEDED",
  "retryAfter": 60,
  "resetAt": "2025-01-15T15:00:00Z"
}
```

## Best Practices

### ✅ DO
- Include rate limit headers in responses
- Use Redis for distributed rate limiting
- Implement tiered limits for different user plans
- Set appropriate window sizes and limits
- Monitor rate limit metrics
- Provide clear retry guidance
- Document rate limits in API docs
- Test under high load

### ❌ DON'T
- Use in-memory storage in production
- Set limits too restrictively
- Forget to include Retry-After header
- Ignore distributed scenarios
- Make rate limits public (security)
- Use simple counters for distributed systems
- Forget cleanup of old data

## Monitoring

```javascript
// Track rate limit metrics
const metrics = {
  totalRequests: 0,
  limitedRequests: 0,
  byUser: new Map()
};

app.use((req, res, next) => {
  metrics.totalRequests++;
  res.on('finish', () => {
    if (res.statusCode === 429) {
      metrics.limitedRequests++;
    }
  });
  next();
});

app.get('/metrics/rate-limit', (req, res) => {
  res.json({
    totalRequests: metrics.totalRequests,
    limitedRequests: metrics.limitedRequests,
    percentage: (metrics.limitedRequests / metrics.totalRequests * 100).toFixed(2)
  });
});
```
