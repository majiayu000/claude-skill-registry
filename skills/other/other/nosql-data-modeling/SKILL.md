---
name: nosql-data-modeling
description: "Use when designing MongoDB, DynamoDB, or Redis data models, implementing access-pattern-driven design, or migrating from relational to NoSQL databases."
---

# NoSQL Data Modeling

## Database Selection Table

| Factor | MongoDB | DynamoDB | Redis | Firestore |
|--------|---------|----------|-------|-----------|
| Data model | Document (JSON) | Key-value + document | Key-value + data structures | Document (nested) |
| Query flexibility | High (ad-hoc queries) | Low (key-based only) | Low (key-based) | Medium (indexed fields) |
| Scale model | Sharded clusters | Fully managed, infinite | Single-node or cluster | Fully managed |
| Consistency | Tunable (strong or eventual) | Tunable per-request | Strong (single node) | Strong within entity group |
| Cost model | Self-host or Atlas | Pay per RCU/WCU | Memory-based | Pay per read/write ops |
| Best for | General purpose, flexible schemas | Predictable high-scale workloads | Caching, sessions, leaderboards | Mobile/web apps, real-time sync |
| Avoid when | Need ACID joins | Need ad-hoc queries | Data > memory | Need complex queries |
| Max item size | 16 MB | 400 KB | 512 MB (value) | 1 MB |

## Access-Pattern-Driven Design

NoSQL design is backwards from relational. Start with queries, not entities.

### Step-by-Step Process

```
1. List ALL access patterns (reads and writes)
2. Estimate frequency and latency requirements per pattern
3. Choose primary key to satisfy the most critical patterns
4. Design secondary indexes for remaining patterns
5. Denormalize data to avoid joins
6. Accept data duplication as a tradeoff for read performance
```

### Example: E-Commerce

```
Access Patterns:
  1. Get order by order_id                    (100k/day, <10ms)
  2. Get all orders for a user                (50k/day, <50ms)
  3. Get all orders in date range for a user  (10k/day, <100ms)
  4. Get order items for an order             (100k/day, <10ms)
  5. Get user profile                         (200k/day, <10ms)

Design decisions:
  - Pattern 1,4: embed items IN the order document (no join needed)
  - Pattern 2,3: user_id as partition key, order_date as sort key
  - Pattern 5: separate user collection/table
  - Denormalize: store user_name in order (avoid lookup for display)
```

## MongoDB Patterns

### Embed vs Reference Decision

| Factor | Embed | Reference |
|--------|-------|-----------|
| Read together? | Always | Sometimes |
| Array growth | Bounded (<100) | Unbounded |
| Update frequency | Low | High (independent updates) |
| Document size | Fits in 16MB | Would exceed limit |
| Data duplication OK? | Yes | No (single source of truth) |

### Schema Design Patterns

```python
from pymongo import MongoClient
from datetime import datetime

db = MongoClient()["ecommerce"]

# Pattern 1: Embedded (1:few, always read together)
order = {
    "_id": "ord_abc123",
    "user_id": "usr_456",
    "user_name": "Alice",          # Denormalized from users collection
    "created_at": datetime.utcnow(),
    "status": "shipped",
    "items": [                     # Embedded -- always fetched with order
        {"sku": "WIDGET-1", "name": "Blue Widget", "qty": 2, "price": 9.99},
        {"sku": "GADGET-3", "name": "Red Gadget", "qty": 1, "price": 24.99},
    ],
    "total": 44.97,
}
db.orders.insert_one(order)

# Pattern 2: Reference (1:many, unbounded growth)
# Blog post with comments -- comments can grow to thousands
post = {
    "_id": "post_789",
    "title": "NoSQL Modeling",
    "body": "...",
    "comment_count": 0,  # Cached count to avoid counting query
}

comment = {
    "_id": "cmt_001",
    "post_id": "post_789",    # Reference to parent
    "author": "Bob",
    "text": "Great post!",
    "created_at": datetime.utcnow(),
}

# Pattern 3: Bucket pattern (time-series, IoT)
# Instead of one doc per measurement, bucket by hour
sensor_bucket = {
    "_id": "sensor_1_2024010112",  # sensor_id + YYYYMMDDHH
    "sensor_id": "sensor_1",
    "start": datetime(2024, 1, 1, 12, 0),
    "count": 60,
    "measurements": [
        {"ts": datetime(2024, 1, 1, 12, 0, 0), "temp": 22.1, "humidity": 45},
        {"ts": datetime(2024, 1, 1, 12, 1, 0), "temp": 22.3, "humidity": 44},
        # ... up to 60 per hour
    ],
    "avg_temp": 22.2,  # Pre-computed aggregates
    "max_temp": 23.1,
}
```

### MongoDB Indexes

```python
# Compound index for user orders by date (covers patterns 2 and 3)
db.orders.create_index([("user_id", 1), ("created_at", -1)])

# Text index for search
db.posts.create_index([("title", "text"), ("body", "text")])

# TTL index for auto-expiring documents
db.sessions.create_index("expires_at", expireAfterSeconds=0)

# Partial index (only index active orders -- saves space)
db.orders.create_index(
    [("user_id", 1), ("created_at", -1)],
    partialFilterExpression={"status": {"$ne": "cancelled"}},
)
```

## DynamoDB Patterns

### Single-Table Design

```python
import boto3
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("app-data")

# All entities in ONE table with overloaded PK/SK

# User entity
table.put_item(Item={
    "PK": "USER#usr_456",
    "SK": "PROFILE",
    "name": "Alice",
    "email": "alice@example.com",
    "created_at": "2024-01-01T00:00:00Z",
    "entity_type": "User",
})

# Order entity (under user partition)
table.put_item(Item={
    "PK": "USER#usr_456",
    "SK": "ORDER#2024-01-15#ord_abc123",  # Date prefix for range queries
    "order_id": "ord_abc123",
    "status": "shipped",
    "total": "44.97",
    "entity_type": "Order",
})

# Order items (under order partition for direct lookup)
table.put_item(Item={
    "PK": "ORDER#ord_abc123",
    "SK": "ITEM#WIDGET-1",
    "sku": "WIDGET-1",
    "name": "Blue Widget",
    "qty": 2,
    "price": "9.99",
    "entity_type": "OrderItem",
})

# Query: Get user profile
resp = table.get_item(Key={"PK": "USER#usr_456", "SK": "PROFILE"})

# Query: Get all orders for user (sorted by date)
resp = table.query(
    KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
    ExpressionAttributeValues={":pk": "USER#usr_456", ":sk": "ORDER#"},
    ScanIndexForward=False,  # Newest first
)

# Query: Get orders in date range
resp = table.query(
    KeyConditionExpression="PK = :pk AND SK BETWEEN :start AND :end",
    ExpressionAttributeValues={
        ":pk": "USER#usr_456",
        ":start": "ORDER#2024-01-01",
        ":end": "ORDER#2024-01-31",
    },
)
```

### GSI Overloading

```python
# GSI1: Inverted index (access order by order_id directly)
# Main table: PK=USER#id, SK=ORDER#date#id
# GSI1:       PK=ORDER#id, SK=USER#id
table.put_item(Item={
    "PK": "USER#usr_456",
    "SK": "ORDER#2024-01-15#ord_abc123",
    "GSI1PK": "ORDER#ord_abc123",     # GSI partition key
    "GSI1SK": "USER#usr_456",          # GSI sort key
    "order_id": "ord_abc123",
    "status": "shipped",
    "entity_type": "Order",
})

# Query GSI: Get order by order_id
resp = table.query(
    IndexName="GSI1",
    KeyConditionExpression="GSI1PK = :pk",
    ExpressionAttributeValues={":pk": "ORDER#ord_abc123"},
)

# GSI2: Status index (get all orders by status)
# GSI2PK = STATUS#shipped, GSI2SK = date
```

### Partition Key Selection

| Pattern | Key Design | Rationale |
|---------|-----------|-----------|
| User data | `USER#{user_id}` | Natural partition, bounded size |
| Time-series | `SENSOR#{id}#YYYY-MM-DD` | Prevent hot partition; shard by day |
| High-write | `ITEM#{id}#SHARD#{0-9}` | Write sharding for hot keys |
| Global config | `CONFIG#GLOBAL` | Single item, cache it |

## Redis Data Structures

| Structure | Use When | Example |
|-----------|---------|---------|
| String | Simple key-value, counters, cache | Session data, feature flags |
| Hash | Object with fields | User profile fields |
| List | Ordered collection, queue | Job queue, recent items |
| Set | Unique members, intersections | Tags, online users |
| Sorted Set | Ranked data, range queries | Leaderboards, rate limiting |
| Stream | Event log, pub/sub with history | Activity feed, event sourcing |

```python
import redis

r = redis.Redis(decode_responses=True)

# Hash: user profile (better than serialized JSON -- update fields individually)
r.hset("user:456", mapping={"name": "Alice", "email": "alice@example.com", "login_count": "0"})
r.hincrby("user:456", "login_count", 1)
profile = r.hgetall("user:456")

# Sorted set: leaderboard
r.zadd("leaderboard:weekly", {"alice": 2500, "bob": 1800, "carol": 3200})
top_10 = r.zrevrange("leaderboard:weekly", 0, 9, withscores=True)
alice_rank = r.zrevrank("leaderboard:weekly", "alice")  # 0-indexed

# Sorted set: rate limiting (sliding window)
import time

def is_rate_limited(user_id: str, limit: int = 100, window_s: int = 60) -> bool:
    key = f"rate:{user_id}"
    now = time.time()
    pipe = r.pipeline()
    pipe.zremrangebyscore(key, 0, now - window_s)  # Remove old entries
    pipe.zadd(key, {f"{now}": now})                  # Add current request
    pipe.zcard(key)                                   # Count in window
    pipe.expire(key, window_s)                        # TTL cleanup
    _, _, count, _ = pipe.execute()
    return count > limit

# Stream: event log
r.xadd("events:orders", {"type": "created", "order_id": "ord_123", "user_id": "usr_456"})
# Read latest events
events = r.xrevrange("events:orders", count=10)

# Cache with TTL
r.setex("cache:product:789", 300, '{"name": "Widget", "price": 9.99}')  # 5min TTL
```

## Consistency Patterns

| Pattern | Consistency | Use When |
|---------|------------|----------|
| Read-your-writes | Session-level | User sees their own updates immediately |
| Eventual consistency | None guaranteed | Analytics, feeds, non-critical reads |
| Strong consistency | Immediate | Financial data, inventory counts |
| Write-behind cache | Eventual | High-read, tolerate stale |

```python
# DynamoDB: strong consistency per-read
resp = table.get_item(
    Key={"PK": "USER#456", "SK": "BALANCE"},
    ConsistentRead=True,  # Costs 2x RCU but guarantees latest
)

# MongoDB: read concern + write concern
from pymongo import ReadPreference, WriteConcern

# Strong: write to majority, read from primary
collection = db.get_collection(
    "orders",
    write_concern=WriteConcern(w="majority"),
    read_preference=ReadPreference.PRIMARY,
)

# Eventual: read from secondaries (lower latency, possibly stale)
collection_eventual = db.get_collection(
    "orders",
    read_preference=ReadPreference.SECONDARY_PREFERRED,
)
```

## Migration from Relational

### Step-by-Step

```
1. Map access patterns (not tables)
   - List every SQL query your app runs
   - Group by frequency and latency requirement

2. Denormalize JOIN results
   - If you always JOIN orders + users: embed user_name in order
   - If you sometimes JOIN: reference with user_id

3. Handle relationships
   - 1:1 → embed
   - 1:few (bounded) → embed array
   - 1:many (unbounded) → reference (separate collection/item)
   - many:many → reference array on one side, or adjacency list

4. Replace transactions
   - Single-document operations are atomic in MongoDB
   - Use DynamoDB TransactWriteItems for multi-item
   - Redesign to minimize multi-document transactions

5. Migrate incrementally
   - Dual-write to both databases during transition
   - Shadow-read from NoSQL, compare with SQL results
   - Switch reads to NoSQL once validated
   - Remove SQL writes last
```

### Relational to MongoDB Example

```sql
-- Relational
SELECT o.id, o.total, u.name, u.email,
       oi.sku, oi.qty, oi.price
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN order_items oi ON oi.order_id = o.id
WHERE o.user_id = 456
ORDER BY o.created_at DESC;
```

```python
# MongoDB: single query, no joins needed
orders = db.orders.find(
    {"user_id": "usr_456"},
    sort=[("created_at", -1)],
)
# Each order already contains:
#   user_name (denormalized)
#   items[] (embedded)
```

### Relational to DynamoDB Example

```sql
-- Relational: 3 tables, 2 joins
SELECT * FROM orders WHERE user_id = 456 AND created_at > '2024-01-01';
SELECT * FROM order_items WHERE order_id = 'abc123';
```

```python
# DynamoDB: 2 queries, no joins
# Query 1: user's orders in date range
orders = table.query(
    KeyConditionExpression="PK = :pk AND SK BETWEEN :start AND :end",
    ExpressionAttributeValues={
        ":pk": "USER#usr_456",
        ":start": "ORDER#2024-01-01",
        ":end": "ORDER#2024-12-31",
    },
)

# Query 2: order items (if not embedded)
items = table.query(
    KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
    ExpressionAttributeValues={":pk": "ORDER#ord_abc123", ":sk": "ITEM#"},
)
```

## Gotchas

- **Modeling entities before access patterns**: NoSQL design starts with queries, not ER diagrams; design for reads, not normalization
- **Unbounded arrays in MongoDB**: embedding 10k comments in a post hits the 16MB limit; reference instead and paginate
- **Hot partitions in DynamoDB**: a single PK receiving disproportionate traffic throttles; add write sharding for hot keys
- **DynamoDB 400KB item limit**: embed carefully; large items hit the limit fast; store blobs in S3, reference by key
- **Scanning instead of querying**: DynamoDB full table scans are expensive and slow; if you need one, your key design is wrong
- **Redis as primary database**: Redis is a cache/data-structure server; data loss on restart unless using AOF persistence; always have a source of truth elsewhere
- **Ignoring GSI costs in DynamoDB**: every GSI duplicates data and consumes its own capacity; 5 GSIs on a hot table = 6x write cost
- **MongoDB without indexes**: queries without index support cause collection scans; use `explain()` to verify index usage
- **Eventual consistency surprises**: write then immediately read may return stale data; use strong consistency for read-after-write patterns
- **Over-denormalization**: duplicating user email in 10 collections means updating 10 places when it changes; denormalize what's read-heavy and rarely updated
- **Forgetting TTL**: cache entries and session data without expiry grow forever; set TTLs on everything temporal
