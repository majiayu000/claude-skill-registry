---
name: nosql-databases
description: "Master NoSQL database systems including MongoDB, Cassandra, Redis, and DynamoDB for scalable data storage. Use for: choosing the right NoSQL database, implementing document stores (MongoDB), building distributed systems (Cassandra), caching and real-time data (Redis), serverless databases (DynamoDB), data modeling for NoSQL, scaling strategies, and migrating from SQL to NoSQL."
---

# NoSQL Databases

Master modern NoSQL database systems for scalable, flexible data storage across diverse use cases.

## Overview

NoSQL databases provide alternatives to traditional relational databases, offering flexible schemas, horizontal scalability, and specialized data models. This skill covers the four major NoSQL types: document stores (MongoDB), wide-column stores (Cassandra), key-value stores (Redis), and managed services (DynamoDB).

## When to Use NoSQL

| Scenario | Database Type | Recommended Solution |
|----------|---------------|---------------------|
| Flexible, evolving schemas | Document | MongoDB |
| High write throughput | Wide-column | Cassandra |
| Caching, real-time data | Key-value | Redis |
| Serverless, auto-scaling | Managed | DynamoDB |
| Time-series data | Wide-column | Cassandra |
| Session management | Key-value | Redis |
| Content management | Document | MongoDB |
| IoT data collection | Wide-column | Cassandra |

## MongoDB (Document Store)

### Data Model

```javascript
// Document structure
{
  _id: ObjectId("507f1f77bcf86cd799439011"),
  title: "Introduction to NoSQL",
  author: {
    name: "John Doe",
    email: "john@example.com"
  },
  tags: ["database", "nosql", "mongodb"],
  comments: [
    { user: "Jane", text: "Great post!", date: ISODate("2026-01-15") }
  ],
  views: 1250,
  published: true
}
```

### CRUD Operations

```javascript
// Insert
db.posts.insertOne({
  title: "My Post",
  content: "Content here",
  author: "John"
})

// Find
db.posts.find({ published: true })
db.posts.findOne({ _id: ObjectId("...") })

// Update
db.posts.updateOne(
  { _id: ObjectId("...") },
  { $set: { published: true }, $inc: { views: 1 } }
)

// Delete
db.posts.deleteOne({ _id: ObjectId("...") })
```

### Aggregation Pipeline

```javascript
db.posts.aggregate([
  { $match: { published: true } },
  { $group: {
      _id: "$author",
      totalPosts: { $sum: 1 },
      avgViews: { $avg: "$views" }
  }},
  { $sort: { totalPosts: -1 } },
  { $limit: 10 }
])
```

### Indexing

```javascript
// Create index
db.posts.createIndex({ title: 1 })
db.posts.createIndex({ author: 1, published: 1 })

// Text search index
db.posts.createIndex({ title: "text", content: "text" })
db.posts.find({ $text: { $search: "nosql database" } })
```

## Cassandra (Wide-Column Store)

### Data Model

```cql
CREATE KEYSPACE blog WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 3
};

CREATE TABLE posts (
  author_id uuid,
  post_id timeuuid,
  title text,
  content text,
  tags set<text>,
  views counter,
  PRIMARY KEY (author_id, post_id)
) WITH CLUSTERING ORDER BY (post_id DESC);
```

### Queries

```cql
-- Insert
INSERT INTO posts (author_id, post_id, title, content)
VALUES (uuid(), now(), 'My Post', 'Content');

-- Select
SELECT * FROM posts WHERE author_id = ?;
SELECT * FROM posts WHERE author_id = ? AND post_id > ?;

-- Update
UPDATE posts SET views = views + 1 WHERE author_id = ? AND post_id = ?;

-- Delete
DELETE FROM posts WHERE author_id = ? AND post_id = ?;
```

### Partitioning Strategy

```cql
-- Time-series partitioning
CREATE TABLE sensor_data (
  sensor_id uuid,
  date date,
  timestamp timestamp,
  temperature double,
  PRIMARY KEY ((sensor_id, date), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);
```

## Redis (Key-Value Store)

### Data Structures

```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# Strings
r.set('user:1:name', 'John Doe')
r.get('user:1:name')
r.incr('page:views')

# Hashes
r.hset('user:1', mapping={'name': 'John', 'email': 'john@example.com'})
r.hgetall('user:1')

# Lists
r.lpush('queue:tasks', 'task1', 'task2')
r.rpop('queue:tasks')

# Sets
r.sadd('tags', 'python', 'redis', 'nosql')
r.smembers('tags')

# Sorted Sets
r.zadd('leaderboard', {'player1': 100, 'player2': 200})
r.zrange('leaderboard', 0, -1, withscores=True)
```

### Caching Pattern

```python
def get_user(user_id):
    # Try cache first
    cached = r.get(f'user:{user_id}')
    if cached:
        return json.loads(cached)
    
    # Fetch from database
    user = db.query(User).get(user_id)
    
    # Cache for 5 minutes
    r.setex(f'user:{user_id}', 300, json.dumps(user.to_dict()))
    
    return user.to_dict()
```

### Pub/Sub

```python
# Publisher
r.publish('notifications', json.dumps({'message': 'New post'}))

# Subscriber
pubsub = r.pubsub()
pubsub.subscribe('notifications')

for message in pubsub.listen():
    if message['type'] == 'message':
        data = json.loads(message['data'])
        print(data)
```

## DynamoDB (Managed NoSQL)

### Table Design

```python
import boto3

dynamodb = boto3.resource('dynamodb')

# Create table
table = dynamodb.create_table(
    TableName='Posts',
    KeySchema=[
        {'AttributeName': 'author_id', 'KeyType': 'HASH'},
        {'AttributeName': 'post_id', 'KeyType': 'RANGE'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'author_id', 'AttributeType': 'S'},
        {'AttributeName': 'post_id', 'AttributeType': 'S'}
    ],
    BillingMode='PAY_PER_REQUEST'
)
```

### Operations

```python
table = dynamodb.Table('Posts')

# Put item
table.put_item(
    Item={
        'author_id': 'user123',
        'post_id': 'post456',
        'title': 'My Post',
        'content': 'Content here',
        'views': 0
    }
)

# Get item
response = table.get_item(
    Key={'author_id': 'user123', 'post_id': 'post456'}
)

# Query
response = table.query(
    KeyConditionExpression='author_id = :author',
    ExpressionAttributeValues={':author': 'user123'}
)

# Update
table.update_item(
    Key={'author_id': 'user123', 'post_id': 'post456'},
    UpdateExpression='SET views = views + :inc',
    ExpressionAttributeValues={':inc': 1}
)
```

## Database Comparison

| Feature | MongoDB | Cassandra | Redis | DynamoDB |
|---------|---------|-----------|-------|----------|
| Data Model | Document | Wide-column | Key-value | Key-value/Document |
| Scalability | Horizontal (sharding) | Linear (masterless) | Cluster mode | Auto-scaling |
| Consistency | Tunable | Tunable | Strong | Eventual/Strong |
| Query Language | Rich (MQL) | CQL (SQL-like) | Commands | Limited |
| Best For | Flexible schemas | Write-heavy | Caching | Serverless |
| Performance | Mixed workloads | High writes | Sub-millisecond | Low latency |

## Data Modeling Patterns

### Embedding vs Referencing (MongoDB)

```javascript
// Embedding (denormalized)
{
  _id: ObjectId("..."),
  title: "Post",
  author: {
    name: "John",
    email: "john@example.com"
  }
}

// Referencing (normalized)
{
  _id: ObjectId("..."),
  title: "Post",
  author_id: ObjectId("...")
}
```

### Partition Key Design (Cassandra/DynamoDB)

```cql
-- Bad: Hot partition
PRIMARY KEY (status, user_id)  -- All "active" users in one partition

-- Good: Distributed
PRIMARY KEY (user_id, status)  -- Users distributed across partitions
```

## Performance Optimization

### MongoDB

```javascript
// Use projection
db.posts.find({}, { title: 1, author: 1 })

// Use covered queries
db.posts.createIndex({ author: 1, title: 1 })
db.posts.find({ author: "John" }, { author: 1, title: 1, _id: 0 })

// Batch operations
db.posts.insertMany([...])
```

### Redis

```python
# Use pipeline
pipe = r.pipeline()
pipe.set('key1', 'value1')
pipe.set('key2', 'value2')
pipe.execute()

# Use connection pooling
pool = redis.ConnectionPool(host='localhost', port=6379)
r = redis.Redis(connection_pool=pool)
```

## Using the Reference Files

### When to Read Each Reference

**`/references/mongodb-advanced.md`** — Read when implementing complex MongoDB queries, aggregations, or optimizing performance.

**`/references/cassandra-architecture.md`** — Read when designing Cassandra data models, understanding consistency, or scaling clusters.

**`/references/redis-patterns.md`** — Read when implementing caching strategies, pub/sub systems, or distributed locks.

**`/references/dynamodb-best-practices.md`** — Read when designing DynamoDB tables, optimizing costs, or implementing access patterns.
