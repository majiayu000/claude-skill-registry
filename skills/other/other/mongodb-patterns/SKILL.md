---
name: mongodb-patterns
description: Document modeling, aggregation pipeline, indexing strategy, change streams, and multi-document transactions.
---

# MongoDB Patterns

Document database design and query optimization for MongoDB.

## Document Modeling Strategies

```typescript
// EMBED when: 1:1 or 1:few, data read together, child has no independent lifecycle
interface Order {
  _id: ObjectId
  customerId: ObjectId
  status: 'pending' | 'paid' | 'shipped'
  items: OrderItem[]        // Embedded - always read with order
  shippingAddress: Address  // Embedded - 1:1
  createdAt: Date
}

interface OrderItem {
  productId: ObjectId
  name: string              // Denormalized - avoid join at read time
  price: number             // Snapshot at purchase time
  quantity: number
}

// REFERENCE when: 1:many (unbounded), independent queries, shared across documents
interface Product {
  _id: ObjectId
  name: string
  price: number
  categoryId: ObjectId     // Reference - category queried independently
  reviews: never           // DON'T embed - unbounded array
}

// Bucket pattern: group time-series data into fixed-size documents
interface SensorBucket {
  _id: ObjectId
  sensorId: string
  startTime: Date
  endTime: Date
  count: number            // Track bucket fullness
  measurements: {          // Embed up to 200 per bucket
    timestamp: Date
    value: number
  }[]
}
```

## Indexing Strategy

```typescript
// Compound index: field order matters (ESR rule)
// Equality → Sort → Range
db.orders.createIndex({
  status: 1,       // Equality: exact match filter
  createdAt: -1,   // Sort: avoid in-memory sort
  total: 1         // Range: price > 100
})

// Partial index: only index documents matching filter (smaller index)
db.orders.createIndex(
  { customerId: 1, createdAt: -1 },
  { partialFilterExpression: { status: 'pending' } }
)

// Text index for search
db.products.createIndex({ name: 'text', description: 'text' })

// TTL index for auto-expiration
db.sessions.createIndex(
  { createdAt: 1 },
  { expireAfterSeconds: 86400 }  // Auto-delete after 24h
)

// Wildcard index for dynamic schemas
db.events.createIndex({ 'metadata.$**': 1 })
```

## Aggregation Pipeline

```typescript
// Sales analytics: top products by revenue per category
const pipeline = [
  // Stage 1: Filter date range
  { $match: {
    createdAt: { $gte: new Date('2025-01-01'), $lt: new Date('2025-02-01') },
    status: 'paid'
  }},

  // Stage 2: Unwind embedded items array
  { $unwind: '$items' },

  // Stage 3: Group by product
  { $group: {
    _id: '$items.productId',
    productName: { $first: '$items.name' },
    totalRevenue: { $sum: { $multiply: ['$items.price', '$items.quantity'] } },
    totalSold: { $sum: '$items.quantity' },
    orderCount: { $addToSet: '$_id' }
  }},

  // Stage 4: Add computed fields
  { $addFields: {
    orderCount: { $size: '$orderCount' },
    avgOrderValue: { $divide: ['$totalRevenue', { $size: '$orderCount' }] }
  }},

  // Stage 5: Sort by revenue descending
  { $sort: { totalRevenue: -1 } },

  // Stage 6: Limit to top 20
  { $limit: 20 },

  // Stage 7: Lookup category details
  { $lookup: {
    from: 'products',
    localField: '_id',
    foreignField: '_id',
    pipeline: [{ $project: { categoryId: 1 } }],
    as: 'product'
  }}
]

const results = await db.orders.aggregate(pipeline).toArray()
```

## Change Streams (Real-time Reactivity)

```typescript
async function watchOrderChanges(): Promise<void> {
  const pipeline = [
    { $match: {
      operationType: { $in: ['insert', 'update'] },
      'fullDocument.status': 'paid'
    }}
  ]

  // resumeAfter enables resuming from last processed change (crash recovery)
  const changeStream = db.orders.watch(pipeline, {
    fullDocument: 'updateLookup',  // Include full document on updates
    resumeAfter: await getLastResumeToken()
  })

  changeStream.on('change', async (event) => {
    try {
      await processOrderPayment(event.fullDocument!)
      await saveResumeToken(event._id)  // Persist for crash recovery
    } catch (err) {
      console.error('Change stream processing failed:', err)
    }
  })

  changeStream.on('error', (err) => {
    console.error('Change stream error:', err)
    // Reconnect with resume token
    setTimeout(() => watchOrderChanges(), 5000)
  })
}
```

## Multi-Document Transactions

```typescript
async function transferFunds(
  fromAccountId: string,
  toAccountId: string,
  amount: number
): Promise<void> {
  const session = client.startSession()

  try {
    await session.withTransaction(async () => {
      const from = await db.accounts.findOne(
        { _id: new ObjectId(fromAccountId) },
        { session }
      )
      if (!from || from.balance < amount) {
        throw new Error('Insufficient funds')
      }

      await db.accounts.updateOne(
        { _id: new ObjectId(fromAccountId) },
        { $inc: { balance: -amount } },
        { session }
      )

      await db.accounts.updateOne(
        { _id: new ObjectId(toAccountId) },
        { $inc: { balance: amount } },
        { session }
      )

      await db.transactions.insertOne({
        from: fromAccountId,
        to: toAccountId,
        amount,
        createdAt: new Date()
      }, { session })
    })
  } finally {
    await session.endSession()
  }
}
```

## Checklist

- [ ] Embed for 1:1 and 1:few; reference for 1:many and many:many
- [ ] Follow ESR (Equality-Sort-Range) for compound index field order
- [ ] Use partial indexes to reduce index size on filtered queries
- [ ] Set TTL indexes for session/temp data auto-cleanup
- [ ] Use aggregation pipeline for analytics (not client-side loops)
- [ ] Change streams with resume tokens for crash-safe event processing
- [ ] Keep documents under 16MB (MongoDB limit)
- [ ] Use `explain()` to verify queries use indexes

## Anti-Patterns

- Unbounded arrays: reviews/comments embedded in parent (grows forever, hits 16MB)
- Missing indexes: full collection scans on frequently queried fields
- $lookup in hot paths: use denormalization, not joins, for read-heavy queries
- Storing related data in separate collections when always read together
- Using MongoDB as a relational database (normalize everything)
- Not using write concern `majority` for critical writes (data loss risk)
