---
name: migrate-service-to-container
description: Guides migration from old_code/ to containers/ following SERVICE_MIGRATION_GUIDE.md. Transforms imports to use @coder/shared, adds tenantId to database queries, replaces hardcoded URLs with config, updates routes with auth/tenant enforcement, sets up event publishers/consumers, and transforms service communication. Use when migrating existing services, transforming old code patterns, or refactoring legacy code to new architecture.
---

# Migrate Service to Container

Guides migration from `old_code/` to `containers/` following SERVICE_MIGRATION_GUIDE.md and ModuleImplementationGuide.md standards.

## Pre-Migration Analysis

Before migrating, analyze:

- [ ] **Dependencies**: What services does this depend on?
- [ ] **Database**: What Cosmos DB containers does it use?
- [ ] **Events**: What events does it publish/consume?
- [ ] **External APIs**: What external services does it call?
- [ ] **Configuration**: What configuration values does it need?
- [ ] **Routes**: What API endpoints does it expose?
- [ ] **Business Logic**: What are the core services/classes?

## Migration Steps

### Step 1: Create Module Structure

Use `create-container-module` skill or manually create:

```bash
mkdir -p containers/<service-name>/{config,src/{config,routes,services,types,utils,events,middleware},tests/{unit,integration}}
```

### Step 2: Transform Imports

**Old Pattern:**
```typescript
import { config } from '../config/env.js';
import { CosmosClient } from '@azure/cosmos';
```

**New Pattern:**
```typescript
import { CosmosDBClient } from '@coder/shared';
import { loadConfig } from '../config';
```

Reference: ModuleImplementationGuide.md Section 5 (Dependency Rules)

### Step 3: Transform Database Queries

**Old Pattern:**
```typescript
async getData(id: string) {
  const query = `SELECT * FROM c WHERE c.id = @id`;
  // ❌ No tenantId
}
```

**New Pattern:**
```typescript
async getData(tenantId: string, id: string) {
  const container = this.db.getContainer('service_data');
  const query = `SELECT * FROM c WHERE c.tenantId = @tenantId AND c.id = @id`;
  const parameters = [
    { name: '@tenantId', value: tenantId },
    { name: '@id', value: id }
  ];
  // ✅ tenantId required, uses shared client
}
```

Reference: SERVICE_MIGRATION_GUIDE.md Step 6, ModuleImplementationGuide.md Section 8

### Step 4: Replace Hardcoded URLs

**Old Pattern:**
```typescript
const response = await fetch('http://localhost:3021/api/users/123');
```

**New Pattern:**
```typescript
import { ServiceClient } from '@coder/shared';

const client = new ServiceClient({
  baseUrl: config.services.auth.url, // From config
  timeout: 5000,
});

const response = await client.get('/api/v1/users/123', {
  headers: {
    'X-Tenant-ID': tenantId,
    'Authorization': `Bearer ${serviceToken}`,
  },
});
```

Reference: SERVICE_MIGRATION_GUIDE.md Step 7, ModuleImplementationGuide.md Section 5.3

### Step 5: Transform Routes

**Old Pattern:**
```typescript
fastify.get('/api/my-service/data', async (request, reply) => {
  const service = new MyService();
  const data = await service.getData(request.params.id);
  return reply.send(data);
});
```

**New Pattern:**
```typescript
import { authenticateRequest, tenantEnforcementMiddleware } from '@coder/shared';

fastify.get<{ Params: { id: string } }>(
  '/api/v1/data/:id',
  {
    preHandler: [authenticateRequest(), tenantEnforcementMiddleware()],
  },
  async (request, reply) => {
    // ✅ tenantId available from tenantEnforcementMiddleware
    const tenantId = request.user!.tenantId;
    const data = await service.getData(tenantId, request.params.id);
    return reply.send({ data });
  }
);
```

Reference: SERVICE_MIGRATION_GUIDE.md Step 5

### Step 6: Update Error Handling

**Old Pattern:**
```typescript
throw new Error('Something went wrong');
```

**New Pattern:**
```typescript
import { AppError } from '@coder/shared';
throw new AppError('Something went wrong', 400, 'BAD_REQUEST');
```

Reference: ModuleImplementationGuide.md Section 10 (Error Handling)

### Step 7: Set Up Event Publishing

**New Pattern:**
```typescript
import { EventPublisher } from '@coder/shared';

const publisher = new EventPublisher(config.rabbitmq);
await publisher.publish('service.resource.created', {
  id: resource.id,
  tenantId: tenantId,
  timestamp: new Date().toISOString(),
});
```

Reference: ModuleImplementationGuide.md Section 9 (Event-Driven Communication)

### Step 8: Transform Service Initialization

**Old Pattern:**
```typescript
const service = new MyService(cosmosClient, redis, monitoring);
```

**New Pattern:**
```typescript
import { getDatabaseClient, getCacheClient } from '@coder/shared';
const db = getDatabaseClient();
const cache = getCacheClient();
const service = new MyService(db, cache);
```

## Migration Checklist

### Pre-Migration
- [ ] Analyze dependencies
- [ ] Map database containers
- [ ] Identify events (published/consumed)
- [ ] List API endpoints
- [ ] Document configuration needs

### Code Migration
- [ ] Create module directory structure
- [ ] Copy service files
- [ ] Transform imports (use @coder/shared)
- [ ] Add tenantId to all database queries
- [ ] Replace hardcoded URLs with config
- [ ] Transform routes (add auth, tenant enforcement)
- [ ] Update error handling (use AppError)
- [ ] Add event publishing/consuming

### Configuration
- [ ] Create config/default.yaml
- [ ] Create config/schema.json
- [ ] Create config/index.ts loader
- [ ] Add environment variable documentation

### Validation
- [ ] No hardcoded ports/URLs
- [ ] All queries include tenantId
- [ ] Service-to-service auth implemented
- [ ] Follows ModuleImplementationGuide.md
