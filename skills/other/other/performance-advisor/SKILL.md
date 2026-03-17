---
name: performance-advisor
description: >
  Reference guide for MongoDB performance patterns: index strategies (ESR rule,
  compound, partial, TTL), explain plan interpretation, and performance checklists.
  Use as background knowledge when advising on indexing or performance. For
  hands-on optimization of a specific slow query, trigger the query-advisor agent instead.
---

# MongoDB Performance Advisor

You are a MongoDB performance specialist. Analyze queries, recommend indexes, and optimize database operations.

## Performance Analysis Process

1. **Get the query plan**: Run `.explain("executionStats")` on the problematic query
2. **Identify bottlenecks**: Look for COLLSCAN, high docsExamined, slow stages
3. **Recommend indexes**: Suggest compound indexes based on query patterns
4. **Verify improvement**: Show before/after comparison of explain output

## Explain Plan Analysis

```bash
mongosh "$MONGODB_URI" --quiet --eval "
  const plan = db.<collection>.<operation>.explain('executionStats');
  printjson({
    queryPlanner: plan.queryPlanner.winningPlan,
    executionStats: {
      nReturned: plan.executionStats.nReturned,
      totalDocsExamined: plan.executionStats.totalDocsExamined,
      totalKeysExamined: plan.executionStats.totalKeysExamined,
      executionTimeMillis: plan.executionStats.executionTimeMillis
    }
  });
"
```

## Key Metrics to Check

| Metric | Good | Bad |
|--------|------|-----|
| Stage | IXSCAN | COLLSCAN |
| docsExamined/nReturned ratio | Close to 1:1 | Much higher than results |
| executionTimeMillis | < 100ms | > 1000ms |
| keysExamined | Close to nReturned | 0 (no index used) |

## Index Recommendations

### Compound Index Strategy (ESR Rule)
Build indexes following **Equality, Sort, Range**:

```javascript
// Query: find active users in age range, sorted by name
db.users.find({ status: "active", age: { $gte: 18, $lte: 65 } }).sort({ name: 1 })

// Optimal index: equality first, then sort, then range
db.users.createIndex({ status: 1, name: 1, age: 1 })
```

### Common Index Patterns

```javascript
// Single field
db.collection.createIndex({ email: 1 })

// Compound
db.collection.createIndex({ category: 1, createdAt: -1 })

// Text search
db.collection.createIndex({ title: "text", description: "text" })

// TTL (auto-expire documents)
db.collection.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 })

// Partial (index only matching documents)
db.collection.createIndex(
  { email: 1 },
  { partialFilterExpression: { status: "active" } }
)

// Unique
db.collection.createIndex({ email: 1 }, { unique: true })
```

## Current Index Analysis

```bash
mongosh "$MONGODB_URI" --quiet --eval "
  db.getCollectionNames().forEach(coll => {
    const indexes = db.getCollection(coll).getIndexes();
    const stats = db.getCollection(coll).stats();
    print('=== ' + coll + ' ===');
    print('Documents: ' + stats.count + ', Size: ' + (stats.size / 1024 / 1024).toFixed(2) + ' MB');
    indexes.forEach(idx => {
      print('  Index: ' + JSON.stringify(idx.key) + (idx.unique ? ' [unique]' : '') + (idx.sparse ? ' [sparse]' : ''));
    });
    print('');
  });
"
```

## Performance Checklist

- [ ] All frequent queries use indexes (no COLLSCAN)
- [ ] Compound indexes follow ESR rule
- [ ] No unused indexes consuming write overhead
- [ ] Write concern appropriate for use case
- [ ] Read preference configured for replica sets
- [ ] Connection pooling configured
- [ ] Aggregation pipelines have early `$match` stages
- [ ] Projections limit returned fields
- [ ] Results are paginated with cursor-based pagination
