---
name: azure-cosmosdb
description: Azure Cosmos DB partition keys, consistency levels, change feed, SDK patterns
---

# Azure Cosmos DB Skill

*Load with: base.md + [typescript.md | python.md]*

Azure Cosmos DB is a globally distributed, multi-model database with guaranteed low latency, elastic scalability, and multiple consistency models.

**Sources:** [Cosmos DB Docs](https://learn.microsoft.com/en-us/azure/cosmos-db/) | [Partitioning](https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning-overview) | [SDK](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/sdk-nodejs)

---

## Core Principle

**Choose partition key wisely, design for your access patterns, understand consistency tradeoffs.**

Cosmos DB distributes data across partitions. Your partition key choice determines scalability, performance, and cost. Design for even distribution and query efficiency.

---

## Cosmos DB APIs

| API | Use Case |
|-----|----------|
| **NoSQL (Core)** | Document database, most flexible |
| **MongoDB** | MongoDB wire protocol compatible |
| **PostgreSQL** | Distributed PostgreSQL (Citus) |
| **Apache Cassandra** | Wide-column store |
| **Apache Gremlin** | Graph database |
| **Table** | Key-value (Azure Table Storage compatible) |

This skill focuses on **NoSQL (Core) API** - the most common choice.

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Container** | Collection of items (like a table) |
| **Item** | Single document/record (JSON) |
| **Partition Key** | Determines data distribution |
| **Logical Partition** | Items with same partition key |
| **Physical Partition** | Storage unit (max 50GB, 10K RU/s) |
| **RU (Request Unit)** | Throughput currency |

---

## Partition Key Design

### Good Partition Keys
```typescript
// High cardinality, even distribution, used in queries

// E-commerce: userId for user data
{ "id": "order-123", "userId": "user-456", ... }  // PK: /userId

// Multi-tenant: tenantId
{ "id": "doc-1", "tenantId": "tenant-abc", ... }  // PK: /tenantId

// IoT: deviceId for telemetry
{ "id": "reading-1", "deviceId": "device-789", ... }  // PK: /deviceId

// Logs: synthetic key (date + category)
{ "id": "log-1", "partitionKey": "2024-01-15_errors", ... }  // PK: /partitionKey
```

### Hierarchical Partition Keys
```typescript
// For multi-level distribution (e.g., tenant → user)
// Container created with: /tenantId, /userId

{
  "id": "order-123",
  "tenantId": "acme-corp",
  "userId": "user-456",
  "items": [...]
}

// Query within tenant and user efficiently
```

### Bad Partition Keys
```typescript
// Avoid:
// - Low cardinality (status, type, boolean)
// - Monotonically increasing (timestamp, auto-increment)
// - Frequently updated fields
// - Fields not used in queries

// Bad: Only 3 values → hot partitions
{ "status": "pending" | "completed" | "cancelled" }

// Bad: All writes go to latest partition
{ "timestamp": "2024-01-15T10:30:00Z" }
```

---

## SDK Setup (TypeScript)

### Install
```bash
npm install @azure/cosmos
```

### Initialize Client
```typescript
// lib/cosmosdb.ts
import { CosmosClient, Database, Container } from '@azure/cosmos';

const endpoint = process.env.COSMOS_ENDPOINT!;
const key = process.env.COSMOS_KEY!;
const databaseId = process.env.COSMOS_DATABASE!;

const client = new CosmosClient({ endpoint, key });

// Or with connection string
// const client = new CosmosClient(process.env.COSMOS_CONNECTION_STRING!);

export const database: Database = client.database(databaseId);

export function getContainer(containerId: string): Container {
  return database.container(containerId);
}
```

### Type Definitions
```typescript
// types/cosmos.ts
export interface BaseItem {
  id: string;
  _ts?: number;      // Auto-generated timestamp
  _etag?: string;    // For optimistic concurrency
}

export interface User extends BaseItem {
  userId: string;    // Partition key
  email: string;
  name: string;
  createdAt: string;
  updatedAt: string;
}

export interface Order extends BaseItem {
  userId: string;    // Partition key
  orderId: string;
  items: OrderItem[];
  total: number;
  status: 'pending' | 'paid' | 'shipped' | 'delivered';
  createdAt: string;
}

export interface OrderItem {
  productId: string;
  name: string;
  quantity: number;
  price: number;
}
```

---

## CRUD Operations

### Create Item
```typescript
import { getContainer } from './cosmosdb';
import { User } from './types';

const usersContainer = getContainer('users');

async function createUser(data: Omit<User, 'id' | 'createdAt' | 'updatedAt'>): Promise<User> {
  const now = new Date().toISOString();
  const user: User = {
    id: crypto.randomUUID(),
    ...data,
    createdAt: now,
    updatedAt: now
  };

  const { resource } = await usersContainer.items.create(user);
  return resource as User;
}
```

### Read Item (Point Read)
```typescript
// Most efficient read - requires id AND partition key
async function getUser(userId: string, id: string): Promise<User | null> {
  try {
    const { resource } = await usersContainer.item(id, userId).read<User>();
    return resource || null;
  } catch (error: any) {
    if (error.code === 404) return null;
    throw error;
  }
}

// If id equals partition key value
async function getUserById(userId: string): Promise<User | null> {
  try {
    const { resource } = await usersContainer.item(userId, userId).read<User>();
    return resource || null;
  } catch (error: any) {
    if (error.code === 404) return null;
    throw error;
  }
}
```

### Query Items
```typescript
// Query within partition (efficient)
async function getUserOrders(userId: string): Promise<Order[]> {
  const ordersContainer = getContainer('orders');

  const { resources } = await ordersContainer.items
    .query<Order>({
      query: 'SELECT * FROM c WHERE c.userId = @userId ORDER BY c.createdAt DESC',
      parameters: [{ name: '@userId', value: userId }]
    })
    .fetchAll();

  return resources;
}

// Cross-partition query (use sparingly)
async function getOrdersByStatus(status: string): Promise<Order[]> {
  const ordersContainer = getContainer('orders');

  const { resources } = await ordersContainer.items
    .query<Order>({
      query: 'SELECT * FROM c WHERE c.status = @status',
      parameters: [{ name: '@status', value: status }]
    })
    .fetchAll();

  return resources;
}

// Paginated query
async function getOrdersPaginated(
  userId: string,
  pageSize: number = 10,
  continuationToken?: string
): Promise<{ items: Order[]; continuationToken?: string }> {
  const ordersContainer = getContainer('orders');

  const queryIterator = ordersContainer.items.query<Order>(
    {
      query: 'SELECT * FROM c WHERE c.userId = @userId ORDER BY c.createdAt DESC',
      parameters: [{ name: '@userId', value: userId }]
    },
    {
      maxItemCount: pageSize,
      continuationToken
    }
  );

  const { resources, continuationToken: nextToken } = await queryIterator.fetchNext();

  return {
    items: resources,
    continuationToken: nextToken
  };
}
```

### Update Item
```typescript
// Replace entire item
async function updateUser(userId: string, id: string, updates: Partial<User>): Promise<User> {
  const existing = await getUser(userId, id);
  if (!existing) throw new Error('User not found');

  const updated: User = {
    ...existing,
    ...updates,
    updatedAt: new Date().toISOString()
  };

  const { resource } = await usersContainer.item(id, userId).replace(updated);
  return resource as User;
}

// Partial update (patch operations)
async function patchUser(userId: string, id: string, operations: any[]): Promise<User> {
  const { resource } = await usersContainer.item(id, userId).patch(operations);
  return resource as User;
}

// Usage:
await patchUser('user-123', 'user-123', [
  { op: 'set', path: '/name', value: 'New Name' },
  { op: 'set', path: '/updatedAt', value: new Date().toISOString() },
  { op: 'incr', path: '/loginCount', value: 1 }
]);
```

### Delete Item
```typescript
async function deleteUser(userId: string, id: string): Promise<void> {
  await usersContainer.item(id, userId).delete();
}
```

### Optimistic Concurrency (ETags)
```typescript
async function updateUserWithETag(
  userId: string,
  id: string,
  updates: Partial<User>,
  etag: string
): Promise<User> {
  const existing = await getUser(userId, id);
  if (!existing) throw new Error('User not found');

  const updated: User = {
    ...existing,
    ...updates,
    updatedAt: new Date().toISOString()
  };

  try {
    const { resource } = await usersContainer.item(id, userId).replace(updated, {
      accessCondition: { type: 'IfMatch', condition: etag }
    });
    return resource as User;
  } catch (error: any) {
    if (error.code === 412) {
      throw new Error('Document was modified by another process');
    }
    throw error;
  }
}
```

---

## Consistency Levels

| Level | Guarantees | Latency | Use Case |
|-------|-----------|---------|----------|
| **Strong** | Linearizable reads | Highest | Financial, inventory |
| **Bounded Staleness** | Consistent within bounds | High | Leaderboards, counters |
| **Session** | Read your writes | Medium | User sessions (default) |
| **Consistent Prefix** | Ordered reads | Low | Social feeds |
| **Eventual** | No ordering guarantee | Lowest | Analytics, logs |

### Set Consistency Per Request
```typescript
// Override default consistency
const { resource } = await usersContainer.item(id, userId).read<User>({
  consistencyLevel: 'Strong'
});

// For queries
const { resources } = await container.items.query(
  { query: 'SELECT * FROM c' },
  { consistencyLevel: 'BoundedStaleness' }
).fetchAll();
```

---

## Batch Operations

### Transactional Batch (Same Partition)
```typescript
async function createOrderWithItems(userId: string, order: Order, items: any[]): Promise<void> {
  const ordersContainer = getContainer('orders');

  const operations = [
    { operationType: 'Create' as const, resourceBody: order },
    ...items.map(item => ({
      operationType: 'Create' as const,
      resourceBody: { ...item, userId, orderId: order.orderId }
    }))
  ];

  const { result } = await ordersContainer.items.batch(operations, userId);

  // Check if any operation failed
  if (result.some(r => r.statusCode >= 400)) {
    throw new Error('Batch operation failed');
  }
}
```

### Bulk Operations
```typescript
// For large-scale imports (not transactional)
async function bulkImportUsers(users: User[]): Promise<void> {
  const operations = users.map(user => ({
    operationType: 'Create' as const,
    resourceBody: user,
    partitionKey: user.userId
  }));

  // Process in chunks
  const chunkSize = 100;
  for (let i = 0; i < operations.length; i += chunkSize) {
    const chunk = operations.slice(i, i + chunkSize);
    await usersContainer.items.bulk(chunk);
  }
}
```

---

## Change Feed

### Process Changes
```typescript
import { ChangeFeedStartFrom } from '@azure/cosmos';

async function processChangeFeed(): Promise<void> {
  const container = getContainer('orders');

  const changeFeedIterator = container.items.changeFeed({
    changeFeedStartFrom: ChangeFeedStartFrom.Beginning()
  });

  while (changeFeedIterator.hasMoreResults) {
    const { result: items, statusCode } = await changeFeedIterator.fetchNext();

    if (statusCode === 304) {
      // No new changes
      await sleep(1000);
      continue;
    }

    for (const item of items) {
      console.log('Changed item:', item);
      // Process the change...
    }
  }
}

// For production, use Change Feed Processor with lease container
```

### Change Feed Processor Pattern
```typescript
async function startChangeFeedProcessor(): Promise<void> {
  const sourceContainer = getContainer('orders');
  const leaseContainer = getContainer('leases');

  const changeFeedProcessor = sourceContainer.items.changeFeed
    .for(item => {
      // Process each change
      console.log('Processing:', item);
    })
    .withLeaseContainer(leaseContainer)
    .build();

  await changeFeedProcessor.start();
}
```

---

## Python SDK

### Install
```bash
pip install azure-cosmos
```

### Setup and Operations
```python
# cosmos_db.py
import os
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from typing import Optional, List
from datetime import datetime
import uuid

# Initialize client
endpoint = os.environ['COSMOS_ENDPOINT']
key = os.environ['COSMOS_KEY']
database_name = os.environ['COSMOS_DATABASE']

client = CosmosClient(endpoint, key)
database = client.get_database_client(database_name)


def get_container(container_name: str):
    return database.get_container_client(container_name)


# CRUD Operations
users_container = get_container('users')


def create_user(email: str, name: str, user_id: str = None) -> dict:
    user_id = user_id or str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    user = {
        'id': user_id,
        'userId': user_id,  # Partition key
        'email': email,
        'name': name,
        'createdAt': now,
        'updatedAt': now
    }

    return users_container.create_item(user)


def get_user(user_id: str) -> Optional[dict]:
    try:
        return users_container.read_item(item=user_id, partition_key=user_id)
    except CosmosResourceNotFoundError:
        return None


def query_users(email_domain: str) -> List[dict]:
    query = "SELECT * FROM c WHERE CONTAINS(c.email, @domain)"
    parameters = [{'name': '@domain', 'value': email_domain}]

    return list(users_container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))


def update_user(user_id: str, **updates) -> dict:
    user = get_user(user_id)
    if not user:
        raise ValueError('User not found')

    user.update(updates)
    user['updatedAt'] = datetime.utcnow().isoformat()

    return users_container.replace_item(item=user_id, body=user)


def delete_user(user_id: str) -> None:
    users_container.delete_item(item=user_id, partition_key=user_id)


# Paginated query
def get_users_paginated(page_size: int = 10, continuation_token: str = None):
    query = "SELECT * FROM c ORDER BY c.createdAt DESC"

    items = users_container.query_items(
        query=query,
        enable_cross_partition_query=True,
        max_item_count=page_size,
        continuation_token=continuation_token
    )

    page = items.by_page()
    results = list(next(page))

    return {
        'items': results,
        'continuation_token': page.continuation_token
    }
```

---

## Indexing

### Custom Indexing Policy
```json
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    { "path": "/userId/?" },
    { "path": "/status/?" },
    { "path": "/createdAt/?" }
  ],
  "excludedPaths": [
    { "path": "/content/*" },
    { "path": "/_etag/?" }
  ],
  "compositeIndexes": [
    [
      { "path": "/userId", "order": "ascending" },
      { "path": "/createdAt", "order": "descending" }
    ]
  ]
}
```

### Create Container with Index
```typescript
await database.containers.createIfNotExists({
  id: 'orders',
  partitionKey: { paths: ['/userId'] },
  indexingPolicy: {
    indexingMode: 'consistent',
    includedPaths: [
      { path: '/userId/?' },
      { path: '/status/?' },
      { path: '/createdAt/?' }
    ],
    excludedPaths: [
      { path: '/*' }  // Exclude all by default
    ]
  }
});
```

---

## Throughput Management

### Provisioned Throughput
```typescript
// Container level
await database.containers.createIfNotExists({
  id: 'orders',
  partitionKey: { paths: ['/userId'] },
  throughput: 1000  // RU/s
});

// Scale throughput
const container = database.container('orders');
await container.throughput.replace(2000);
```

### Autoscale
```typescript
await database.containers.createIfNotExists({
  id: 'orders',
  partitionKey: { paths: ['/userId'] },
  maxThroughput: 10000  // Auto-scales 10% to 100%
});
```

### Serverless
```typescript
// No throughput configuration needed
// Pay per request (good for dev/test, intermittent workloads)
await database.containers.createIfNotExists({
  id: 'orders',
  partitionKey: { paths: ['/userId'] }
  // No throughput = serverless
});
```

---

## CLI Quick Reference

```bash
# Azure CLI
az cosmosdb create --name myaccount --resource-group mygroup
az cosmosdb sql database create --account-name myaccount --name mydb --resource-group mygroup
az cosmosdb sql container create \
  --account-name myaccount \
  --database-name mydb \
  --name orders \
  --partition-key-path /userId \
  --throughput 400

# Query
az cosmosdb sql query --account-name myaccount --database-name mydb \
  --container-name orders --query "SELECT * FROM c"

# Keys
az cosmosdb keys list --name myaccount --resource-group mygroup
az cosmosdb keys list --name myaccount --resource-group mygroup --type connection-strings
```

---

## Cost Optimization

| Strategy | Impact |
|----------|--------|
| **Right partition key** | Avoid hot partitions (wasted RUs) |
| **Index only what you query** | Reduce write RU cost |
| **Use point reads** | 1 RU vs 3+ RU for queries |
| **Serverless for dev/test** | Pay per request |
| **Autoscale for production** | Scale down during low traffic |
| **TTL for temporary data** | Auto-delete old items |

### Time-to-Live (TTL)
```typescript
// Enable TTL on container
await database.containers.createIfNotExists({
  id: 'sessions',
  partitionKey: { paths: ['/userId'] },
  defaultTtl: 3600  // 1 hour
});

// Per-item TTL
const session = {
  id: 'session-123',
  userId: 'user-456',
  ttl: 1800  // Override: 30 minutes
};
```

---

## Anti-Patterns

- **Bad partition key** - Low cardinality causes hot partitions
- **Cross-partition queries** - Expensive; design for single-partition queries
- **Over-indexing** - Increases write cost; index only queried paths
- **Large items** - Max 2MB; store blobs in Azure Blob Storage
- **Ignoring RU cost** - Monitor and optimize expensive queries
- **Strong consistency everywhere** - Use Session (default) unless required
- **No retry logic** - Handle 429 (throttling) with exponential backoff
- **Missing TTL** - Set TTL for temporary/session data
