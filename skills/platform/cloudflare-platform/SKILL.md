---
name: Cloudflare Platform Products
description: This skill should be used when the user asks about "R2", "D1", "KV", "Durable Objects", "Queues", "Vectorize", "Hyperdrive", "Workers Analytics", "Email Routing", "Browser Rendering", or discusses Cloudflare platform services, storage options, database choices, when to use which service, or integration patterns between Workers and platform products.
version: 0.1.0
---

# Cloudflare Platform Products

## Purpose

This skill provides guidance on Cloudflare's platform products and services that integrate with Workers. It covers storage options (KV, R2, D1), coordination services (Durable Objects, Queues), data services (Vectorize, Hyperdrive), and specialized services (Analytics Engine, Browser Rendering). Use this skill when choosing between platform products, designing system architecture, or integrating multiple Cloudflare services.

## Platform Products Overview

Cloudflare offers a comprehensive suite of platform products designed to work seamlessly with Workers:

| Product | Category | Use Case | Key Features |
|---------|----------|----------|--------------|
| **KV** | Storage | Key-value cache, static content | Eventually consistent, global, 25MB values |
| **D1** | Database | Relational data, SQL queries | SQLite, transactions, migrations |
| **R2** | Storage | Large files, object storage | S3-compatible, unlimited size, no egress fees |
| **Durable Objects** | Coordination | Stateful services, real-time | Strong consistency, WebSockets, single-threaded |
| **Queues** | Messaging | Async processing, event-driven | At-least-once delivery, batching |
| **Vectorize** | Data | Semantic search, embeddings | Vector similarity, RAG support |
| **Hyperdrive** | Database | Postgres connection pooling | Reduced latency, connection management |
| **Analytics Engine** | Analytics | Custom metrics, time-series | High-cardinality data, SQL queries |
| **Workers AI** | AI/ML | Inference, embeddings | Text generation, vision, audio |

See `references/platform-products-matrix.md` for detailed comparison and selection guide.

## Storage Services

### KV (Key-Value Storage)

**Best for**: Static content, configuration, caching, read-heavy workloads

**Characteristics**:
- Eventually consistent (writes propagate in ~60 seconds globally)
- Optimized for reads (not writes)
- 25 MB max value size
- Global replication included
- Metadata support

**When to use**:
- Caching API responses
- Storing static assets
- Configuration data
- Session data (with expiration)
- Read-heavy data with infrequent writes

**When NOT to use**:
- Frequently changing data
- Strong consistency requirements
- Large objects (> 25 MB)
- Complex queries

**Example use cases**:
```javascript
// Cache API responses
await env.CACHE.put(`api:users:${id}`, JSON.stringify(user), {
  expirationTtl: 3600
});

// Store configuration
await env.CONFIG.put('feature_flags', JSON.stringify(flags));

// Session storage
await env.SESSIONS.put(sessionId, userData, {
  expirationTtl: 86400 // 24 hours
});
```

### D1 (SQLite Database)

**Best for**: Relational data, complex queries, transactional workloads

**Characteristics**:
- SQLite database
- Strong consistency
- ACID transactions
- SQL query support
- Migrations support
- 25 MB database size (beta limit)

**When to use**:
- Structured relational data
- Complex queries with JOINs
- Transactional operations
- Data with relationships
- Migrations-driven schema

**When NOT to use**:
- Large datasets (> 25 MB in beta)
- Very high write throughput
- Unstructured data
- Simple key-value lookups (use KV instead)

**Example use cases**:
```javascript
// User management
await env.DB.prepare(
  'SELECT * FROM users WHERE email = ? AND active = 1'
).bind(email).first();

// Transactions (via batch)
await env.DB.batch([
  env.DB.prepare('INSERT INTO orders (user_id, total) VALUES (?, ?)').bind(userId, total),
  env.DB.prepare('UPDATE users SET last_order = ? WHERE id = ?').bind(Date.now(), userId)
]);

// Complex queries
await env.DB.prepare(`
  SELECT orders.*, users.email
  FROM orders
  JOIN users ON orders.user_id = users.id
  WHERE orders.status = ?
`).bind('pending').all();
```

### R2 (Object Storage)

**Best for**: Large files, user uploads, backups, media storage

**Characteristics**:
- S3-compatible API
- No size limits per object
- Zero egress fees (from Workers)
- Custom metadata
- Streaming support

**When to use**:
- Large files (> 25 MB)
- User-uploaded content
- Media files (images, videos)
- Backups and archives
- Static website hosting

**When NOT to use**:
- Small values (< 1 KB, use KV)
- Frequently updated small data
- Requires low-latency for small reads (KV is faster)

**Example use cases**:
```javascript
// Store user upload
await env.UPLOADS.put(`users/${userId}/avatar.jpg`, imageData, {
  httpMetadata: {
    contentType: 'image/jpeg'
  },
  customMetadata: {
    uploadedBy: userId,
    uploadedAt: Date.now().toString()
  }
});

// Stream large file
const object = await env.MEDIA.get('videos/large-video.mp4');
return new Response(object.body);

// Store backup
await env.BACKUPS.put(`db-backup-${Date.now()}.sql`, backupData);
```

See `references/storage-options-guide.md` for detailed storage selection criteria.

## Coordination Services

### Durable Objects

**Best for**: Coordination, real-time collaboration, WebSockets, rate limiting

**Characteristics**:
- Strong consistency
- Stateful instances
- Single-threaded execution per object
- Persistent storage
- WebSocket support
- Global coordination

**When to use**:
- Real-time collaboration (chat, docs)
- Rate limiting and quotas
- Coordination between distributed requests
- Persistent WebSocket connections
- Stateful game servers
- Sequential processing requirements

**When NOT to use**:
- Simple stateless operations
- Read-heavy workloads (use KV)
- Pure data storage (use D1/R2)
- High-throughput parallel processing

**Example use cases**:
```javascript
// Rate limiting
export class RateLimiter {
  constructor(state, env) {
    this.state = state;
  }

  async fetch(request) {
    const count = await this.state.storage.get('count') || 0;
    const limit = 100;

    if (count >= limit) {
      return new Response('Rate limit exceeded', { status: 429 });
    }

    await this.state.storage.put('count', count + 1);
    return new Response('OK');
  }
}

// Chat room coordination
export class ChatRoom {
  constructor(state, env) {
    this.state = state;
    this.sessions = [];
  }

  async fetch(request) {
    const pair = new WebSocketPair();
    this.sessions.push(pair[1]);

    pair[1].accept();
    pair[1].addEventListener('message', event => {
      // Broadcast to all sessions
      this.sessions.forEach(session => {
        session.send(event.data);
      });
    });

    return new Response(null, { status: 101, webSocket: pair[0] });
  }
}
```

### Queues

**Best for**: Asynchronous processing, background jobs, event-driven workflows

**Characteristics**:
- At-least-once delivery
- Message batching
- Dead letter queues
- Automatic retries
- Guaranteed ordering per message

**When to use**:
- Background processing
- Webhook handling
- Email sending
- Data pipeline stages
- Decoupling services
- Batch processing

**When NOT to use**:
- Synchronous request-response
- Exactly-once delivery required (handle idempotency in consumer)
- Real-time requirements (use Durable Objects + WebSockets)

**Example use cases**:
```javascript
// Producer: Queue email sending
await env.EMAIL_QUEUE.send({
  to: user.email,
  subject: 'Welcome',
  body: 'Welcome to our service!'
});

// Consumer: Process emails in batches
export default {
  async queue(batch, env) {
    for (const message of batch.messages) {
      const { to, subject, body } = message.body;

      try {
        await sendEmail(to, subject, body, env);
        message.ack();
      } catch (error) {
        console.error('Email failed:', error);
        message.retry();
      }
    }
  }
};
```

## Data Services

### Vectorize

**Best for**: Semantic search, RAG, recommendations, similarity matching

**Characteristics**:
- Vector similarity search
- Configurable dimensions (matching embedding model)
- Metadata storage
- Batch operations
- Cosine/Euclidean/Dot product metrics

**When to use**:
- Semantic search
- RAG (Retrieval Augmented Generation)
- Recommendation systems
- Image similarity
- Duplicate detection
- Content clustering

**When NOT to use**:
- Exact text search (use D1 with LIKE or full-text search)
- Simple key-value lookup (use KV)
- Small datasets that fit in memory

**Example use cases**:
```javascript
// Generate and store embeddings
const embeddings = await env.AI.run('@cf/baai/bge-base-en-v1.5', {
  text: [document.text]
});

await env.VECTOR_INDEX.insert([{
  id: document.id,
  values: embeddings.data[0],
  metadata: { text: document.text, title: document.title }
}]);

// Semantic search
const queryEmbedding = await env.AI.run('@cf/baai/bge-base-en-v1.5', {
  text: [userQuestion]
});

const results = await env.VECTOR_INDEX.query(queryEmbedding.data[0], {
  topK: 5
});

// Use results for RAG
const context = results.matches.map(m => m.metadata.text).join('\n');
```

### Hyperdrive

**Best for**: Postgres connection pooling, reducing database latency

**Characteristics**:
- Connection pooling for Postgres
- Reduces connection overhead
- Regional caching
- Automatic connection management

**When to use**:
- Connecting to external Postgres databases
- High connection churn
- Reducing latency to databases
- Traditional database migration to Workers

**When NOT to use**:
- SQLite databases (use D1)
- Non-Postgres databases
- When D1 meets requirements

**Example use cases**:
```javascript
// Connect to Postgres via Hyperdrive
const client = env.HYPERDRIVE.connect();

const result = await client.query(
  'SELECT * FROM users WHERE id = $1',
  [userId]
);

// Connection automatically pooled and managed
```

## Analytics and Observability

### Analytics Engine

**Best for**: Custom metrics, high-cardinality analytics, time-series data

**Characteristics**:
- Write-optimized time-series database
- SQL query support
- High cardinality support
- Automatic aggregation

**When to use**:
- Application metrics
- User analytics
- Performance monitoring
- Business intelligence
- Custom event tracking

**When NOT to use**:
- Real-time queries (data available after ~1 minute)
- Transactional data (use D1)
- Simple counters (use Durable Objects)

**Example use cases**:
```javascript
// Write analytics events
await env.ANALYTICS.writeDataPoint({
  blobs: ['api_call', request.url, request.method],
  doubles: [responseTime, statusCode],
  indexes: [userId]
});

// Query via GraphQL API or Dashboard
```

## Specialized Services

### Browser Rendering

**Best for**: Web scraping, PDF generation, screenshots, browser automation

**Characteristics**:
- Headless Chrome browser
- Puppeteer API compatibility
- Full browser environment
- JavaScript execution

**When to use**:
- Taking screenshots
- Generating PDFs
- Web scraping dynamic sites
- Testing web pages
- Browser automation

**Example use cases**:
```javascript
// Take screenshot
const browser = await puppeteer.launch(env.BROWSER);
const page = await browser.newPage();
await page.goto('https://example.com');
const screenshot = await page.screenshot();
await browser.close();

return new Response(screenshot, {
  headers: { 'Content-Type': 'image/png' }
});
```

### Email Routing

**Best for**: Custom email handling, email forwarding, email processing

**Characteristics**:
- Programmable email handling
- Email parsing
- Forward or drop emails
- Integration with Workers

**When to use**:
- Custom email routing logic
- Email processing pipelines
- Spam filtering
- Email-triggered workflows

## Service Selection Guide

### Storage Decision Tree

**Need to store data → What kind?**

1. **Large files (> 25 MB) or media?** → Use **R2**
2. **Relational data with complex queries?** → Use **D1**
3. **Key-value, read-heavy, cache?** → Use **KV**
4. **Vector embeddings for search?** → Use **Vectorize**

### Processing Decision Tree

**Need to process requests → What pattern?**

1. **Real-time coordination, WebSockets?** → Use **Durable Objects**
2. **Async background jobs?** → Use **Queues**
3. **Stateless request processing?** → Use **Workers** (no special binding)
4. **Rate limiting per user/IP?** → Use **Durable Objects**

### Integration Patterns

**Common multi-product patterns:**

1. **RAG Application**:
   - Workers AI (embeddings)
   - Vectorize (vector storage)
   - D1 (original text storage)
   - Workers AI (text generation)

2. **E-commerce Platform**:
   - D1 (product catalog, orders)
   - R2 (product images)
   - KV (session data, cache)
   - Queues (order processing)
   - Durable Objects (inventory management)

3. **Content Platform**:
   - R2 (media files)
   - D1 (metadata, users)
   - KV (CDN cache)
   - Analytics Engine (usage metrics)

4. **Real-time Collaboration**:
   - Durable Objects (room coordination)
   - D1 (persistent data)
   - R2 (file attachments)
   - Queues (notifications)

See `examples/multi-product-architecture.js` for complete integration examples.

## Cost Optimization

### General Principles

1. **Right-size storage**: Use KV for small data, R2 for large files
2. **Cache effectively**: Use KV to cache D1 queries or API responses
3. **Batch operations**: Use Queue batching, D1 batch(), Vectorize bulk inserts
4. **Use Workers AI + Vectorize**: No egress costs between services
5. **Leverage free tiers**: Most products have generous free tiers

### Free Tier Limits

- **KV**: 100k reads/day, 1k writes/day, 1 GB storage
- **D1**: 5 million rows read, 100k rows written
- **R2**: 10 GB storage, 1 million Class A operations
- **Queues**: 1 million operations/month
- **Vectorize**: 30 million queried vectors/month
- **Workers AI**: Limited free inference requests

See `references/pricing-optimization.md` for detailed cost optimization strategies.

## Migration Patterns

### From Traditional Database to D1

```javascript
// Before: External Postgres via Hyperdrive
const result = await env.HYPERDRIVE.query('SELECT * FROM users WHERE id = ?', [id]);

// After: D1 (if dataset fits in 25 MB)
const result = await env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(id).first();
```

### From S3 to R2

```javascript
// R2 is S3-compatible, minimal code changes needed
// Before: aws-sdk with S3
// After: R2 binding (native integration)

await env.MY_BUCKET.put('key', data);
const object = await env.MY_BUCKET.get('key');
```

### From Redis to KV or Durable Objects

```javascript
// Simple cache: KV
await env.CACHE.put('key', 'value', { expirationTtl: 3600 });

// Stateful/counters: Durable Objects
const id = env.COUNTER.idFromName('global');
const counter = env.COUNTER.get(id);
await counter.fetch(request);
```

## Best Practices

### Storage Selection

- **Hot data**: KV (frequently accessed, rarely changed)
- **Warm data**: D1 (structured, occasional queries)
- **Cold data**: R2 (archival, backups)

### Consistency Requirements

- **Strong consistency needed**: D1, Durable Objects
- **Eventually consistent OK**: KV, Vectorize
- **At-least-once delivery**: Queues

### Performance Optimization

- Cache D1 queries in KV for read-heavy workloads
- Use Vectorize batch inserts for efficiency
- Leverage Durable Objects for coordination, not storage
- Stream large R2 objects instead of buffering

### Security

- Use Cloudflare Access for private buckets/databases
- Validate all user input before storing
- Use signed URLs for temporary R2 access
- Implement rate limiting with Durable Objects
- Encrypt sensitive data before storing in KV/R2

## Additional Resources

### Reference Files

For detailed information, consult:
- **`references/platform-products-matrix.md`** - Complete product comparison and selection criteria
- **`references/storage-options-guide.md`** - Deep dive on KV vs D1 vs R2 decisions
- **`references/pricing-optimization.md`** - Cost optimization strategies

### Example Files

Working examples in `examples/`:
- **`multi-product-architecture.js`** - Integrating multiple platform products

### Documentation Links

For the latest platform documentation:
- Platform overview: https://developers.cloudflare.com/products/
- KV: https://developers.cloudflare.com/kv/
- D1: https://developers.cloudflare.com/d1/
- R2: https://developers.cloudflare.com/r2/
- Durable Objects: https://developers.cloudflare.com/durable-objects/
- Queues: https://developers.cloudflare.com/queues/
- Vectorize: https://developers.cloudflare.com/vectorize/

Use the cloudflare-docs-specialist agent to search documentation and fetch the latest platform information.
