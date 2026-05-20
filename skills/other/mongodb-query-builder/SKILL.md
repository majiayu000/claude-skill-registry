---
name: mongodb-query-builder
description: >
  Build and optimize MongoDB queries, aggregation pipelines, and CRUD operations.
  Use when the user asks to query data, filter documents, join collections,
  aggregate results, update documents, or work with MongoDB data in any way.
---

# MongoDB Query Builder

You are an expert MongoDB query builder. When asked to work with MongoDB data, build efficient queries following these guidelines.

## Query Building Process

1. **Understand the data model**: Ask about or infer the collection schema
2. **Choose the right operation**: find, aggregate, updateOne/Many, deleteOne/Many
3. **Build incrementally**: Start simple, add stages/operators as needed
4. **Optimize**: Use indexes, avoid full collection scans, limit results

## Aggregation Pipeline Stages Reference

| Stage | Purpose | Example |
|-------|---------|---------|
| `$match` | Filter documents | `{ $match: { status: "active" } }` |
| `$group` | Group and aggregate | `{ $group: { _id: "$category", total: { $sum: "$price" } } }` |
| `$lookup` | Join collections | `{ $lookup: { from: "orders", localField: "_id", foreignField: "userId", as: "orders" } }` |
| `$project` | Reshape documents | `{ $project: { name: 1, total: { $multiply: ["$price", "$qty"] } } }` |
| `$sort` | Order results | `{ $sort: { createdAt: -1 } }` |
| `$limit` | Cap output | `{ $limit: 20 }` |
| `$unwind` | Flatten arrays | `{ $unwind: "$tags" }` |
| `$addFields` | Add computed fields | `{ $addFields: { fullName: { $concat: ["$first", " ", "$last"] } } }` |
| `$facet` | Multiple pipelines | `{ $facet: { byStatus: [...], byDate: [...] } }` |
| `$bucket` | Range grouping | `{ $bucket: { groupBy: "$price", boundaries: [0, 50, 100, 500] } }` |
| `$out` | Replace collection with results | `{ $out: "reports" }` |
| `$merge` | Merge results into collection | `{ $merge: { into: "reports" } }` |

## Common Operators

**Comparison**: `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin`
**Logical**: `$and`, `$or`, `$not`, `$nor`
**Array**: `$all`, `$elemMatch`, `$size`, `$push`, `$pull`, `$addToSet`
**String**: `$regex`, `$text`, `$concat`, `$substr`, `$toLower`, `$toUpper`
**Date**: `$dateToString`, `$year`, `$month`, `$dayOfMonth`, `$dateFromString`

## Pattern: Join with $lookup

```javascript
// Simple join
db.orders.aggregate([
  {
    $lookup: {
      from: "customers",
      localField: "customerId",
      foreignField: "_id",
      as: "customer"
    }
  },
  { $unwind: "$customer" }
])

// Correlated subquery join (more powerful)
db.orders.aggregate([
  {
    $lookup: {
      from: "products",
      let: { items: "$lineItems" },
      pipeline: [
        { $match: { $expr: { $in: ["$_id", "$$items"] } } },
        { $project: { name: 1, price: 1 } }
      ],
      as: "products"
    }
  }
])
```

## Pattern: Pagination

```javascript
// Offset-based (simple but slow for large offsets)
db.collection.find(query).sort({ _id: 1 }).skip(page * size).limit(size)

// Cursor-based (efficient for large datasets)
db.collection.find({ _id: { $gt: lastSeenId } }).sort({ _id: 1 }).limit(size)
```

## Pattern: Full-text Search

```javascript
// Create text index first
db.articles.createIndex({ title: "text", body: "text" })

// Search
db.articles.find(
  { $text: { $search: "mongodb aggregation" } },
  { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } })
```

## Pattern: Transactions

```javascript
const session = db.getMongo().startSession()
session.startTransaction()
try {
  db.accounts.updateOne({ _id: from }, { $inc: { balance: -amount } }, { session })
  db.accounts.updateOne({ _id: to }, { $inc: { balance: amount } }, { session })
  session.commitTransaction()
} catch (e) {
  session.abortTransaction()
  throw e
}
```

## Execution

Always execute queries via `mongosh`:
```bash
mongosh "$MONGODB_URI" --quiet --eval "<query>"
```

See [examples/](examples/) for more complete query patterns.
