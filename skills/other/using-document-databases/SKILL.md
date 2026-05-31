---
name: using-document-databases
description: Document database implementation for flexible schema applications. Use when building content management, user profiles, catalogs, or event logging. Covers MongoDB (primary), DynamoDB, Firestore, schema design patterns, indexing strategies, and aggregation pipelines.
---

# Document Database Implementation

Guide NoSQL document database selection and implementation for flexible schema applications across Python, TypeScript, Rust, and Go.

## When to Use This Skill

Use document databases when applications need:
- **Flexible schemas** - Data models evolve rapidly without migrations
- **Nested structures** - JSON-like hierarchical data
- **Horizontal scaling** - Built-in sharding and replication
- **Developer velocity** - Object-to-database mapping without ORM complexity

## Database Selection

### Quick Decision Framework

```
DEPLOYMENT ENVIRONMENT?
├── AWS-Native Application → DynamoDB
│   ✓ Serverless, auto-scaling, single-digit ms latency
│   ✗ Limited query flexibility
│
├── Firebase/GCP Ecosystem → Firestore
│   ✓ Real-time sync, offline support, mobile-first
│   ✗ More expensive for heavy reads
│
└── General-Purpose/Complex Queries → MongoDB
    ✓ Rich aggregation, full-text search, vector search
    ✓ ACID transactions, self-hosted or managed
```

### Database Comparison

| Database | Best For | Latency | Max Item | Query Language |
|----------|----------|---------|----------|----------------|
| **MongoDB** | General-purpose, complex queries | 1-5ms | 16MB | MQL (rich) |
| **DynamoDB** | AWS serverless, predictable performance | <10ms | 400KB | PartiQL (limited) |
| **Firestore** | Real-time apps, mobile-first | 50-200ms | 1MB | Firebase queries |

See `references/mongodb.md` for MongoDB details
See `references/dynamodb.md` for DynamoDB single-table design
See `references/firestore.md` for Firestore real-time patterns

## Schema Design Patterns

### Embedding vs Referencing

**Use the decision matrix in `references/schema-design-patterns.md`**

Quick guide:

| Relationship | Pattern | Example |
|--------------|---------|---------|
| One-to-Few | Embed | User addresses (2-3 max) |
| One-to-Many | Hybrid | Blog posts → comments |
| One-to-Millions | Reference | User → events (logging) |
| Many-to-Many | Reference | Products ↔ Categories |

### Embedding Example (MongoDB)

```javascript
// User with embedded addresses
{
  _id: ObjectId("..."),
  email: "user@example.com",
  name: "Jane Doe",
  addresses: [
    {
      type: "home",
      street: "123 Main St",
      city: "Boston",
      default: true
    }
  ],
  preferences: {
    theme: "dark",
    notifications: { email: true, sms: false }
  }
}
```

### Referencing Example (E-commerce)

```javascript
// Orders reference products
{
  _id: ObjectId("..."),
  userId: ObjectId("..."),
  items: [
    {
      productId: ObjectId("..."),      // Reference
      priceAtPurchase: 49.99,          // Denormalize (historical)
      quantity: 2
    }
  ],
  totalAmount: 99.98
}
```

**When to denormalize:**
- Frequently read together
- Historical snapshots (prices, names)
- Read-heavy workloads

## Indexing Strategies

### MongoDB Index Types

```javascript
// 1. Single field (unique email)
db.users.createIndex({ email: 1 }, { unique: true })

// 2. Compound index (ORDER MATTERS!)
db.orders.createIndex({ status: 1, createdAt: -1 })

// 3. Partial index (index subset)
db.orders.createIndex(
  { userId: 1 },
  { partialFilterExpression: { status: { $eq: "pending" }}}
)

// 4. TTL index (auto-delete after 30 days)
db.sessions.createIndex(
  { createdAt: 1 },
  { expireAfterSeconds: 2592000 }
)

// 5. Text index (full-text search)
db.articles.createIndex({
  title: "text",
  content: "text"
})
```

**Index Best Practices:**
- Add indexes for all query filters
- Compound index order: Equality → Range → Sort
- Use covering indexes (query + projection in index)
- Use `explain()` to verify index usage
- Monitor with Performance Advisor (Atlas)

**Validate indexes with the script:**
```bash
python scripts/validate_indexes.py
```

See `references/indexing-strategies.md` for complete guide.

## MongoDB Aggregation Pipelines

**Key Operators:** `$match` (filter), `$group` (aggregate), `$lookup` (join), `$unwind` (arrays), `$project` (reshape)

**For complete pipeline patterns and examples, see:** `references/aggregation-patterns.md`

## DynamoDB Single-Table Design

Design for access patterns using PK/SK patterns. Store multiple entity types in one table with composite keys.

**For complete single-table design patterns and GSI strategies, see:** `references/dynamodb.md`

## Firestore Real-Time Patterns

Use `onSnapshot()` for real-time listeners and Firestore security rules for access control.

**For complete real-time patterns and security rules, see:** `references/firestore.md`

## Multi-Language Examples

**Complete implementations available in `examples/` directory:**
- `examples/mongodb-fastapi/` - Python FastAPI + MongoDB
- `examples/mongodb-nextjs/` - TypeScript Next.js + MongoDB
- `examples/dynamodb-serverless/` - Python Lambda + DynamoDB
- `examples/firestore-react/` - React + Firestore real-time

## Frontend Skill Integration

- **Media Skill** - Use MongoDB GridFS for large file storage with metadata
- **AI Chat Skill** - MongoDB Atlas Vector Search for semantic conversation retrieval
- **Feedback Skill** - DynamoDB for high-throughput event logging with TTL

**For integration examples, see:** `references/skill-integrations.md`

## Performance Optimization

**Key practices:**
- Always use indexes for query filters (verify with `.explain()`)
- Use connection pooling (reuse clients across requests)
- Avoid collection scans in production

**For complete optimization guide, see:** `references/performance.md`

## Common Patterns

**Pagination:** Use cursor-based pagination for large datasets (recommended over offset)
**Soft Deletes:** Mark as deleted with timestamp instead of removing
**Audit Logs:** Store version history within documents

**For implementation details, see:** `references/common-patterns.md`

## Validation and Scripts

### Validate Index Coverage

```bash
# Run validation script
python scripts/validate_indexes.py --db myapp --collection orders

# Output:
# ✓ Query { status: "pending" } covered by index status_1
# ✗ Query { userId: "..." } missing index - add: { userId: 1 }
```

### Schema Analysis

```bash
# Analyze schema patterns
python scripts/analyze_schema.py --db myapp

# Output:
# Collection: users
# - Average document size: 2.4 KB
# - Embedding ratio: 87% (addresses, preferences)
# - Reference ratio: 13% (orderIds)
# Recommendation: Good balance
```

## Anti-Patterns to Avoid

**Unbounded Arrays:** Limit embedded arrays (use references for large collections)
**Over-Indexing:** Only index queried fields (indexes slow writes)
**DynamoDB Scans:** Always use Query with partition key (avoid Scan)

**For detailed anti-patterns, see:** `references/anti-patterns.md`

## Dependencies

### Python
```bash
# MongoDB
pip install motor pymongo

# DynamoDB
pip install boto3

# Firestore
pip install firebase-admin
```

### TypeScript
```bash
# MongoDB
npm install mongodb

# DynamoDB
npm install @aws-sdk/client-dynamodb @aws-sdk/util-dynamodb

# Firestore
npm install firebase firebase-admin
```

### Rust
```toml
# MongoDB
mongodb = "2.8"

# DynamoDB
aws-sdk-dynamodb = "1.0"
```

### Go
```bash
# MongoDB
go get go.mongodb.org/mongo-driver

# DynamoDB
go get github.com/aws/aws-sdk-go-v2/service/dynamodb
```

## Additional Resources

**Database-Specific Guides:**
- `references/mongodb.md` - Complete MongoDB documentation
- `references/dynamodb.md` - DynamoDB single-table patterns
- `references/firestore.md` - Firestore real-time guide

**Pattern Guides:**
- `references/schema-design-patterns.md` - Embedding vs referencing decisions
- `references/indexing-strategies.md` - Index optimization
- `references/aggregation-patterns.md` - MongoDB pipeline cookbook
- `references/common-patterns.md` - Pagination, soft deletes, audit logs
- `references/anti-patterns.md` - Mistakes to avoid
- `references/performance.md` - Query optimization
- `references/skill-integrations.md` - Frontend skill integration

**Examples:** `examples/mongodb-fastapi/`, `examples/mongodb-nextjs/`, `examples/dynamodb-serverless/`, `examples/firestore-react/`
