---
name: write-tenant-isolated-queries
description: Transforms database queries to include tenantId in partition keys following ModuleImplementationGuide.md Section 8 and .cursorrules tenant isolation requirements. Adds tenantId to all Cosmos DB queries, uses parameterized queries, uses prefixed container names from config, and ensures all queries include tenantId in WHERE clause. Use when writing database queries, migrating queries, or ensuring tenant isolation.
---

# Write Tenant-Isolated Queries

Transforms database queries to include tenantId in partition keys for tenant isolation.

## Core Principle

**ALL database queries MUST include tenantId in the partition key.**

Reference: .cursorrules (Security Requirements), ModuleImplementationGuide.md Section 8

## Query Patterns

### ✅ Correct Pattern

```typescript
import { getDatabaseClient } from '@coder/shared';
import { loadConfig } from '../config';

const db = getDatabaseClient();
const config = loadConfig();
const container = db.getContainer(config.cosmos_db.containers.main);

async function getData(tenantId: string, id: string) {
  const query = `SELECT * FROM c WHERE c.tenantId = @tenantId AND c.id = @id`;
  const parameters = [
    { name: '@tenantId', value: tenantId },
    { name: '@id', value: id }
  ];
  
  const { resources } = await container.items
    .query({ query, parameters })
    .fetchAll();
  
  return resources[0];
}
```

### ❌ Wrong Patterns

```typescript
// ❌ No tenantId
const query = `SELECT * FROM c WHERE c.id = @id`;

// ❌ Hardcoded container name
const container = cosmosClient.database('castiel').container('data');

// ❌ String concatenation (SQL injection risk)
const query = `SELECT * FROM c WHERE c.id = '${id}'`;
```

## Container Names

Use prefixed container names from config:

```typescript
// ✅ Correct: From config
const container = db.getContainer(config.cosmos_db.containers.main);
// Container name: {module-name}_data

// ❌ Wrong: Hardcoded
const container = cosmosClient.database('castiel').container('data');
```

Reference: SERVICE_MIGRATION_GUIDE.md Step 6.2

## Parameterized Queries

Always use parameterized queries:

```typescript
// ✅ Correct: Parameterized
const query = `SELECT * FROM c WHERE c.tenantId = @tenantId AND c.status = @status`;
const parameters = [
  { name: '@tenantId', value: tenantId },
  { name: '@status', value: 'active' }
];

// ❌ Wrong: String concatenation
const query = `SELECT * FROM c WHERE c.tenantId = '${tenantId}' AND c.status = '${status}'`;
```

## Common Query Patterns

### Create

```typescript
async function createResource(tenantId: string, data: ResourceData) {
  const item = {
    id: randomUUID(),
    tenantId, // ✅ Always include tenantId
    ...data,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };
  
  const { resource } = await container.items.create(item);
  return resource;
}
```

### Read by ID

```typescript
async function getResourceById(tenantId: string, id: string) {
  const query = `SELECT * FROM c WHERE c.tenantId = @tenantId AND c.id = @id`;
  const parameters = [
    { name: '@tenantId', value: tenantId },
    { name: '@id', value: id }
  ];
  
  const { resources } = await container.items
    .query({ query, parameters })
    .fetchAll();
  
  return resources[0];
}
```

### List with Filters

```typescript
async function listResources(tenantId: string, filters: { status?: string }) {
  let query = `SELECT * FROM c WHERE c.tenantId = @tenantId`;
  const parameters: any[] = [
    { name: '@tenantId', value: tenantId }
  ];
  
  if (filters.status) {
    query += ` AND c.status = @status`;
    parameters.push({ name: '@status', value: filters.status });
  }
  
  query += ` ORDER BY c.createdAt DESC`;
  
  const { resources } = await container.items
    .query({ query, parameters })
    .fetchAll();
  
  return resources;
}
```

### Update

```typescript
async function updateResource(tenantId: string, id: string, updates: Partial<ResourceData>) {
  // First get the item to ensure tenant isolation
  const item = await getResourceById(tenantId, id);
  if (!item) {
    throw new AppError('Resource not found', 404, 'NOT_FOUND');
  }
  
  const updated = {
    ...item,
    ...updates,
    updatedAt: new Date().toISOString(),
  };
  
  const { resource } = await container.items.upsert(updated);
  return resource;
}
```

### Delete

```typescript
async function deleteResource(tenantId: string, id: string) {
  // First get the item to ensure tenant isolation
  const item = await getResourceById(tenantId, id);
  if (!item) {
    throw new AppError('Resource not found', 404, 'NOT_FOUND');
  }
  
  await container.item(id, tenantId).delete();
}
```

## Query Result Caching

Implement caching with tenant isolation:

```typescript
import { getCacheClient } from '@coder/shared';

const cache = getCacheClient();

async function getResourceCached(tenantId: string, id: string) {
  const cacheKey = `resource:${tenantId}:${id}`;
  
  // Try cache first
  const cached = await cache.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }
  
  // Query database
  const resource = await getResourceById(tenantId, id);
  
  // Cache result
  if (resource) {
    await cache.set(cacheKey, JSON.stringify(resource), 'EX', 3600);
  }
  
  return resource;
}
```

## Service Method Signatures

Always include tenantId as first parameter:

```typescript
// ✅ Correct
class ResourceService {
  async getResource(tenantId: string, id: string): Promise<Resource> {
    // tenantId is required
  }
  
  async listResources(tenantId: string, filters: Filters): Promise<Resource[]> {
    // tenantId is required
  }
}

// ❌ Wrong
class ResourceService {
  async getResource(id: string): Promise<Resource> {
    // Missing tenantId
  }
}
```

## Validation Checklist

- [ ] All queries include `c.tenantId = @tenantId` in WHERE clause
- [ ] tenantId is first parameter in all service methods
- [ ] Container names come from config (not hardcoded)
- [ ] All queries use parameterized syntax (no string concatenation)
- [ ] Queries are typed with TypeScript
- [ ] Cache keys include tenantId for isolation

## Common Mistakes

1. **Forgetting tenantId in WHERE clause**
   - Always start queries with `WHERE c.tenantId = @tenantId`

2. **Hardcoding container names**
   - Use `config.cosmos_db.containers.main`

3. **String concatenation in queries**
   - Always use parameterized queries

4. **Missing tenantId in service methods**
   - tenantId should be first parameter

5. **Cache keys without tenantId**
   - Cache keys must include tenantId: `resource:${tenantId}:${id}`
