---
name: idempotency-handling
description: Idempotent API operations with idempotency keys, Redis caching, DB constraints. Use for payment systems, webhook retries, safe retries, or encountering duplicate processing, race conditions, key expiry errors.
---

# Idempotency Handling

Ensure operations produce identical results regardless of execution count.

## Idempotency Key Pattern

```javascript
const redis = require('redis');
const client = redis.createClient();

async function idempotencyMiddleware(req, res, next) {
  const key = req.headers['idempotency-key'];
  if (!key) return next();

  const cached = await client.get(`idempotency:${key}`);
  if (cached) {
    const { status, body } = JSON.parse(cached);
    return res.status(status).json(body);
  }

  // Store original send
  const originalSend = res.json.bind(res);
  res.json = async (body) => {
    await client.setEx(
      `idempotency:${key}`,
      86400, // 24 hours
      JSON.stringify({ status: res.statusCode, body })
    );
    return originalSend(body);
  };

  next();
}
```

## Database-Backed Idempotency

```sql
CREATE TABLE idempotency_keys (
  key VARCHAR(255) PRIMARY KEY,
  request_hash VARCHAR(64) NOT NULL,
  response JSONB,
  status VARCHAR(20) DEFAULT 'processing',
  created_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP DEFAULT NOW() + INTERVAL '24 hours'
);

CREATE INDEX idx_idempotency_expires ON idempotency_keys(expires_at);
```

```javascript
async function processPayment(idempotencyKey, payload) {
  const requestHash = crypto.createHash('sha256')
    .update(JSON.stringify(payload)).digest('hex');

  // Try to insert with 'processing' status - only one request will succeed
  const insertResult = await db.query(
    `INSERT INTO idempotency_keys (key, request_hash, status)
     VALUES ($1, $2, 'processing')
     ON CONFLICT (key) DO NOTHING
     RETURNING *`,
    [idempotencyKey, requestHash]
  );

  // If we inserted the row (rowCount === 1), we're responsible for processing
  if (insertResult.rowCount === 1) {
    try {
      // Execute the payment
      const result = await executePayment(payload);

      // Update to completed with response
      await db.query(
        'UPDATE idempotency_keys SET status = $1, response = $2 WHERE key = $3',
        ['completed', JSON.stringify(result), idempotencyKey]
      );

      return result;
    } catch (error) {
      // Mark as failed on error
      await db.query(
        'UPDATE idempotency_keys SET status = $1, response = $2 WHERE key = $3',
        ['failed', JSON.stringify({ error: error.message }), idempotencyKey]
      );
      throw error;
    }
  }

  // Another request is/was processing this key - check status
  const existing = await db.query(
    'SELECT * FROM idempotency_keys WHERE key = $1',
    [idempotencyKey]
  );

  const row = existing.rows[0];
  if (!row) {
    throw new Error('Unexpected: idempotency key vanished');
  }

  // Verify request hasn't changed
  if (row.request_hash !== requestHash) {
    throw new Error('Idempotency key reused with different request');
  }

  // Check status
  if (row.status === 'completed') {
    return JSON.parse(row.response);
  } else if (row.status === 'processing') {
    throw new Error('Request already processing - retry later');
  } else if (row.status === 'failed') {
    const failedResponse = JSON.parse(row.response);
    throw new Error(`Previous attempt failed: ${failedResponse.error}`);
  }

  throw new Error(`Unknown status: ${row.status}`);
}
```

## When to Apply

- Payment processing
- Order creation
- Webhook handling
- Email sending
- Any operation where duplicates cause issues

## Best Practices

- Require idempotency keys for mutations
- Validate request body matches stored request
- Set appropriate TTL (24 hours typical)
- Use atomic database operations
- Implement cleanup jobs to prevent table bloat

### TTL Cleanup Strategy

To prevent unbounded table growth, implement periodic cleanup of expired keys:

**Option 1: Scheduled Database Job (PostgreSQL)**
```sql
-- Run hourly via pg_cron or external scheduler
DELETE FROM idempotency_keys
WHERE expires_at < NOW()
LIMIT 1000; -- Batch delete to avoid long locks
```

**Option 2: Application Cleanup Job (Node.js)**
```javascript
// Run via cron or job scheduler (e.g., node-cron, Bull)
async function cleanupExpiredKeys() {
  try {
    const result = await db.query(
      'DELETE FROM idempotency_keys WHERE expires_at < NOW()'
    );
    console.log(`Cleaned up ${result.rowCount} expired idempotency keys`);
  } catch (error) {
    console.error('Cleanup job failed:', error);
  }
}

// Schedule to run every hour
cron.schedule('0 * * * *', cleanupExpiredKeys);
```

**Option 3: Application Cleanup Job (Python)**
```python
import asyncio
from datetime import datetime

async def cleanup_expired_keys():
    """Remove expired idempotency keys to prevent table bloat."""
    try:
        result = await db.execute(
            "DELETE FROM idempotency_keys WHERE expires_at < $1",
            datetime.now()
        )
        print(f"Cleaned up {result} expired idempotency keys")
    except Exception as e:
        print(f"Cleanup job failed: {e}")

# Run with APScheduler, Celery, or similar
# scheduler.add_job(cleanup_expired_keys, 'interval', hours=1)
```

**Cleanup Best Practices:**
- Run cleanup during low-traffic periods to minimize lock contention
- Use batched deletes (`LIMIT 1000`) for large tables
- Monitor cleanup job execution and failures
- Consider partitioning the table by created_at for easier cleanup
- Set up alerts if table size grows unexpectedly
