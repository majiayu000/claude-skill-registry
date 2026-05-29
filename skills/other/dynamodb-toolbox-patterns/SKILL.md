---
name: dynamodb-toolbox-patterns
description: Provides TypeScript patterns for DynamoDB-Toolbox v2 including schema/table/entity modeling, .build() command workflow, query/scan access patterns, batch and transaction operations, and single-table design with computed keys. Use when implementing type-safe DynamoDB access layers with DynamoDB-Toolbox v2 in TypeScript services or serverless applications.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# DynamoDB-Toolbox v2 Patterns (TypeScript)

## Overview

This skill provides practical TypeScript patterns for using DynamoDB-Toolbox v2 with AWS SDK v3 DocumentClient. It focuses on type-safe schema modeling, `.build()` command usage, and production-ready single-table design.

## When to Use

- Defining DynamoDB tables and entities with strict TypeScript inference
- Modeling schemas with `item`, `string`, `number`, `list`, `set`, `map`, and `record`
- Implementing `GetItem`, `PutItem`, `UpdateItem`, `DeleteItem` via `.build()`
- Building query and scan access paths with primary keys and GSIs
- Handling batch and transactional operations
- Designing single-table systems with computed keys and entity patterns

## Instructions

1. **Start from access patterns**: identify read/write queries first, then design keys.
2. **Create table + entity boundaries**: one table, multiple entities if using single-table design.
3. **Define schemas with constraints**: apply `.key()`, `.required()`, `.default()`, `.transform()`, `.link()`.
4. **Use `.build()` commands everywhere**: avoid ad-hoc command construction for consistency and type safety.
5. **Add query/index coverage**: validate GSI/LSI paths for each required access pattern.
6. **Use batch/transactions intentionally**: batch for throughput, transactions for atomicity.
7. **Keep items evolvable**: use optional fields, defaults, and derived attributes for schema evolution.

## Examples

### Install and Setup

```bash
npm install dynamodb-toolbox @aws-sdk/client-dynamodb @aws-sdk/lib-dynamodb
```

```typescript
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient } from '@aws-sdk/lib-dynamodb';
import { Table } from 'dynamodb-toolbox/table';
import { Entity } from 'dynamodb-toolbox/entity';
import { item, string, number, list, map } from 'dynamodb-toolbox/schema';

const client = new DynamoDBClient({ region: process.env.AWS_REGION ?? 'eu-west-1' });
const documentClient = DynamoDBDocumentClient.from(client);

export const AppTable = new Table({
  name: 'app-single-table',
  partitionKey: { name: 'PK', type: 'string' },
  sortKey: { name: 'SK', type: 'string' },
  indexes: {
    byType: { type: 'global', partitionKey: { name: 'GSI1PK', type: 'string' }, sortKey: { name: 'GSI1SK', type: 'string' } }
  },
  documentClient
});
```

### Entity Schema with Modifiers and Complex Attributes

```typescript
const now = () => new Date().toISOString();

export const UserEntity = new Entity({
  name: 'User',
  table: AppTable,
  schema: item({
    tenantId: string().required('always'),
    userId: string().required('always'),
    email: string().required('always').transform(input => input.toLowerCase()),
    role: string().enum('admin', 'member').default('member'),
    loginCount: number().default(0),
    tags: list(string()).default([]),
    profile: map({
      displayName: string().optional(),
      timezone: string().default('UTC')
    }).default({ timezone: 'UTC' })
  }),
  computeKey: ({ tenantId, userId }) => ({
    PK: `TENANT#${tenantId}`,
    SK: `USER#${userId}`,
    GSI1PK: `TENANT#${tenantId}#TYPE#USER`,
    GSI1SK: `EMAIL#${userId}`
  })
});
```

### `.build()` CRUD Commands

```typescript
import { PutItemCommand } from 'dynamodb-toolbox/entity/actions/put';
import { GetItemCommand } from 'dynamodb-toolbox/entity/actions/get';
import { UpdateItemCommand, $add } from 'dynamodb-toolbox/entity/actions/update';
import { DeleteItemCommand } from 'dynamodb-toolbox/entity/actions/delete';

await UserEntity.build(PutItemCommand)
  .item({ tenantId: 't1', userId: 'u1', email: 'A@Example.com' })
  .send();

const { Item } = await UserEntity.build(GetItemCommand)
  .key({ tenantId: 't1', userId: 'u1' })
  .send();

await UserEntity.build(UpdateItemCommand)
  .item({ tenantId: 't1', userId: 'u1', loginCount: $add(1) })
  .send();

await UserEntity.build(DeleteItemCommand)
  .key({ tenantId: 't1', userId: 'u1' })
  .send();
```

### Query and Scan Patterns

```typescript
import { QueryCommand } from 'dynamodb-toolbox/table/actions/query';
import { ScanCommand } from 'dynamodb-toolbox/table/actions/scan';

const byTenant = await AppTable.build(QueryCommand)
  .query({
    partition: `TENANT#t1`,
    range: { beginsWith: 'USER#' }
  })
  .send();

const byTypeIndex = await AppTable.build(QueryCommand)
  .query({
    index: 'byType',
    partition: 'TENANT#t1#TYPE#USER'
  })
  .options({ limit: 25 })
  .send();

const scanned = await AppTable.build(ScanCommand)
  .options({ limit: 100 })
  .send();
```

### Batch and Transaction Workflows

```typescript
import { BatchWriteCommand } from 'dynamodb-toolbox/table/actions/batchWrite';
import { TransactWriteCommand } from 'dynamodb-toolbox/table/actions/transactWrite';

await AppTable.build(BatchWriteCommand)
  .requests(
    UserEntity.build(PutItemCommand).item({ tenantId: 't1', userId: 'u2', email: 'u2@example.com' }),
    UserEntity.build(PutItemCommand).item({ tenantId: 't1', userId: 'u3', email: 'u3@example.com' })
  )
  .send();

await AppTable.build(TransactWriteCommand)
  .requests(
    UserEntity.build(PutItemCommand).item({ tenantId: 't1', userId: 'u4', email: 'u4@example.com' }),
    UserEntity.build(UpdateItemCommand).item({ tenantId: 't1', userId: 'u1', loginCount: $add(1) })
  )
  .send();
```

## Single-Table Design Guidance

- Model each business concept as an entity with strict schema.
- Keep PK/SK predictable and composable (`TENANT#`, `USER#`, `ORDER#`).
- Encode access paths into GSI keys, not in-memory filters.
- Prefer append-only timelines for audit/history data.
- Keep hot partitions under control with scoped partitions and sharding where needed.

## Best Practices

- Design keys from access patterns first, then derive entity attributes.
- Keep one source of truth for key composition (`computeKey`) to avoid drift.
- Use `.options({ consistent: true })` only where strict read-after-write is required.
- Prefer targeted queries over scans for runtime request paths.
- Add conditional expressions for idempotency and optimistic concurrency control.
- Validate batch/transaction size limits before execution to avoid partial failures.

## Constraints and Warnings

- DynamoDB-Toolbox v2 relies on AWS SDK v3 DocumentClient integration.
- Avoid table scans in request paths unless explicitly bounded.
- Use conditional writes for concurrency-sensitive updates.
- Transactions are limited and slower than single-item writes; use only for true atomic requirements.
- Validate key design against target throughput before implementation.

## References

Primary references curated from Context7 are available in:

- `references/api-dynamodb-toolbox-v2.md`
