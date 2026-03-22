---
name: cassandra
description: |
  Apache Cassandra is a distributed NoSQL database designed for high availability and linear scalability.
  Learn CQL (Cassandra Query Language), data modeling with partition keys, replication strategies,
  and integration with Node.js using the DataStax driver.
license: Apache-2.0
compatibility: 'macos, linux'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: data-ai
  tags:
    - cassandra
    - nosql
    - distributed-database
    - cql
    - nodejs
---

# Cassandra

Apache Cassandra is a peer-to-peer distributed database that provides high availability with no single point of failure. Data is distributed across nodes using consistent hashing.

## Installation

```bash
# Docker (recommended)
docker run -d --name cassandra -p 9042:9042 cassandra:4

# Wait for startup then connect with cqlsh
docker exec -it cassandra cqlsh

# Node.js driver
npm install cassandra-driver

# Python driver
pip install cassandra-driver
```

## CQL Basics

```sql
-- keyspace.cql: Create keyspace with replication strategy
CREATE KEYSPACE IF NOT EXISTS myapp
  WITH replication = {
    'class': 'NetworkTopologyStrategy',
    'datacenter1': 3
  }
  AND durable_writes = true;

USE myapp;
```

## Data Modeling

```sql
-- tables.cql: Design tables around query patterns (partition key + clustering key)
-- Rule: one table per query pattern

-- Users by email (partition key: email)
CREATE TABLE users (
  email text PRIMARY KEY,
  name text,
  created_at timestamp
);

-- Posts by user, ordered by time (partition: user_id, clustering: created_at DESC)
CREATE TABLE posts_by_user (
  user_id uuid,
  created_at timestamp,
  post_id uuid,
  title text,
  body text,
  PRIMARY KEY (user_id, created_at)
) WITH CLUSTERING ORDER BY (created_at DESC);

-- Time-series: sensor readings bucketed by day
CREATE TABLE sensor_readings (
  sensor_id text,
  day text,
  reading_time timestamp,
  value double,
  PRIMARY KEY ((sensor_id, day), reading_time)
) WITH CLUSTERING ORDER BY (reading_time DESC);
```

## CRUD Operations

```sql
-- crud.cql: Basic insert, select, update, delete
INSERT INTO users (email, name, created_at)
VALUES ('alice@example.com', 'Alice', toTimestamp(now()));

SELECT * FROM users WHERE email = 'alice@example.com';

-- Query with partition and clustering key
SELECT * FROM posts_by_user
WHERE user_id = 550e8400-e29b-41d4-a716-446655440000
  AND created_at > '2026-01-01'
LIMIT 20;

UPDATE users SET name = 'Alice Smith' WHERE email = 'alice@example.com';

DELETE FROM users WHERE email = 'alice@example.com';

-- Batch for atomicity within a partition
BEGIN BATCH
  INSERT INTO posts_by_user (user_id, created_at, post_id, title) VALUES (?, ?, ?, ?);
  UPDATE user_stats SET post_count = post_count + 1 WHERE user_id = ?;
APPLY BATCH;
```

## Node.js Driver

```javascript
// db.js: Cassandra client with DataStax Node.js driver
const { Client, types } = require('cassandra-driver');

const client = new Client({
  contactPoints: ['localhost'],
  localDataCenter: 'datacenter1',
  keyspace: 'myapp',
  queryOptions: { consistency: types.consistencies.localQuorum },
});

async function main() {
  await client.connect();

  // Insert
  await client.execute(
    'INSERT INTO users (email, name, created_at) VALUES (?, ?, ?)',
    ['bob@example.com', 'Bob', new Date()],
    { prepare: true }
  );

  // Query
  const result = await client.execute(
    'SELECT * FROM users WHERE email = ?',
    ['bob@example.com'],
    { prepare: true }
  );
  console.log(result.rows[0]);

  // Paginated query
  const query = 'SELECT * FROM posts_by_user WHERE user_id = ?';
  for await (const row of client.stream(query, [userId], { prepare: true })) {
    console.log(row.title);
  }

  await client.shutdown();
}

main().catch(console.error);
```

## Python Driver

```python
# app.py: Cassandra with Python DataStax driver
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement, ConsistencyLevel

cluster = Cluster(['localhost'])
session = cluster.connect('myapp')

# Insert
session.execute(
    "INSERT INTO users (email, name, created_at) VALUES (%s, %s, toTimestamp(now()))",
    ('alice@example.com', 'Alice')
)

# Query with consistency level
stmt = SimpleStatement(
    "SELECT * FROM users WHERE email = %s",
    consistency_level=ConsistencyLevel.LOCAL_QUORUM
)
row = session.execute(stmt, ('alice@example.com',)).one()
print(row.name)

cluster.shutdown()
```

## Replication and Consistency

```text
Consistency Levels:
- ONE: Fast, low consistency. Good for logs/metrics.
- QUORUM: Majority of replicas. Balanced read/write.
- LOCAL_QUORUM: Majority in local datacenter. Best for multi-DC.
- ALL: All replicas must respond. Slowest, strongest consistency.

Rule of thumb: Write CL + Read CL > Replication Factor = strong consistency
Example: RF=3, Write=QUORUM(2), Read=QUORUM(2) → 2+2 > 3 ✓
```

## Operations

```bash
# nodetool.sh: Common operational commands
# Check cluster status
docker exec cassandra nodetool status

# Check ring token distribution
docker exec cassandra nodetool ring

# Repair data (run regularly)
docker exec cassandra nodetool repair myapp

# Compact SSTables
docker exec cassandra nodetool compact myapp posts_by_user

# Take a snapshot backup
docker exec cassandra nodetool snapshot myapp -t backup_20260219
```
