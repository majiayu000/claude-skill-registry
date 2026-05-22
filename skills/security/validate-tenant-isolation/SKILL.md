---
name: validate-tenant-isolation
description: Verifies tenant isolation is enforced at all layers (gateway, service, database) following .cursorrules Security Requirements and ModuleImplementationGuide.md Section 11. Checks X-Tenant-ID header validation in routes, verifies tenantId in all database queries, validates tenant enforcement middleware, checks service-to-service tenant propagation, verifies audit logging includes tenantId, and ensures tenantId is in partition key for all Cosmos DB queries. Use when performing security audits, pre-deployment checks, or ensuring multi-tenancy compliance.
---

# Validate Tenant Isolation

Verifies tenant isolation is enforced at all layers (gateway, service, database).

## Multi-Layer Validation

Reference: .cursorrules (Security Requirements), ModuleImplementationGuide.md Section 11

### Layer 1: Gateway/API Layer

**Check X-Tenant-ID header validation:**

```typescript
// ✅ Correct: Use authenticateRequest and tenantEnforcementMiddleware
import { authenticateRequest, tenantEnforcementMiddleware } from '@coder/shared';

fastify.get<{ Params: { id: string } }>(
  '/api/v1/resource/:id',
  {
    preHandler: [authenticateRequest(), tenantEnforcementMiddleware()],
  },
  async (request, reply) => {
    // ✅ tenantId automatically validated and attached by tenantEnforcementMiddleware
    const tenantId = request.user!.tenantId;
    
  const resource = await service.getResource(tenantId, request.params.id);
    return reply.send({ data: resource });
  }
);
```

**Validation Checklist:**
- [ ] Routes use `authenticateRequest()` and `tenantEnforcementMiddleware()` in preHandler
- [ ] Routes validate tenantId exists
- [ ] Routes reject requests without X-Tenant-ID header
- [ ] Tenant enforcement middleware registered

### Layer 2: Service Layer

**Check service methods require tenantId:**

```typescript
// ✅ Correct: tenantId is first parameter
class ResourceService {
  async getResource(tenantId: string, id: string): Promise<Resource> {
    // tenantId is required
  }
  
  async listResources(tenantId: string, filters: Filters): Promise<Resource[]> {
    // tenantId is required
  }
}

// ❌ Wrong: Missing tenantId
class ResourceService {
  async getResource(id: string): Promise<Resource> {
    // Missing tenantId
  }
}
```

**Validation Checklist:**
- [ ] All service methods have tenantId as first parameter
- [ ] tenantId is validated (not empty, valid format)
- [ ] Service methods never query without tenantId

### Layer 3: Database Layer

**Check all queries include tenantId in partition key:**

```typescript
// ✅ Correct: tenantId in WHERE clause
const query = `SELECT * FROM c WHERE c.tenantId = @tenantId AND c.id = @id`;
const parameters = [
  { name: '@tenantId', value: tenantId },
  { name: '@id', value: id }
];

// ❌ Wrong: No tenantId
const query = `SELECT * FROM c WHERE c.id = @id`;
```

**Validation Checklist:**
- [ ] All queries include `c.tenantId = @tenantId` in WHERE clause
- [ ] tenantId is in partition key (first condition in WHERE)
- [ ] All CREATE operations include tenantId in document
- [ ] All UPDATE operations filter by tenantId first
- [ ] All DELETE operations filter by tenantId first

### Layer 4: Service-to-Service Communication

**Check tenant propagation:**

```typescript
// ✅ Correct: Include X-Tenant-ID in service calls
const client = new ServiceClient({
  baseURL: config.services.auth.url,
});

const response = await client.get('/api/v1/users/123', {
  headers: {
    'X-Tenant-ID': tenantId, // ✅ Propagate tenantId
    'Authorization': `Bearer ${serviceToken}`,
  },
});
```

**Validation Checklist:**
- [ ] Service calls include X-Tenant-ID header
- [ ] tenantId is extracted from request and propagated
- [ ] No service calls without tenant context

### Layer 5: Audit Logging

**Check logs include tenantId:**

```typescript
// ✅ Correct: Include tenantId in logs
log.info('Resource created', {
  resourceId: resource.id,
  tenantId: tenantId, // ✅ Always include
  userId: userId,
  correlationId: requestId,
});

// ❌ Wrong: Missing tenantId
log.info('Resource created', {
  resourceId: resource.id,
  userId: userId,
});
```

**Validation Checklist:**
- [ ] All log entries include tenantId
- [ ] Error logs include tenantId
- [ ] Audit logs include tenantId
- [ ] Event logs include tenantId (organizationId field)

## Validation Scripts

### Check Database Queries

```bash
# Find queries without tenantId
grep -r "SELECT.*FROM.*WHERE" src/ --exclude-dir=node_modules | grep -v "tenantId"

# Find service methods without tenantId parameter
grep -r "async.*\(.*\)" src/services/ --exclude-dir=node_modules | grep -v "tenantId"
```

### Check Routes

```bash
# Find routes not using tenantEnforcementMiddleware
grep -r "fastify\.(get|post|put|delete)" src/routes/ --exclude-dir=node_modules | grep -v "tenantEnforcementMiddleware"
```

### Check Service Calls

```bash
# Find service calls without X-Tenant-ID
grep -r "ServiceClient\|client\.(get|post|put|delete)" src/ --exclude-dir=node_modules | grep -v "X-Tenant-ID"
```

## Comprehensive Checklist

### Gateway/API Layer
- [ ] All protected routes use `authenticateRequest()` and `tenantEnforcementMiddleware()` in preHandler
- [ ] Routes access tenantId via `request.user!.tenantId`
- [ ] Routes return 401 if X-Tenant-ID header missing (handled by middleware)
- [ ] Tenant enforcement middleware used in all protected routes

### Service Layer
- [ ] All service methods have tenantId as first parameter
- [ ] tenantId is validated (not empty, valid UUID format)
- [ ] No service methods query without tenantId

### Database Layer
- [ ] All SELECT queries include `c.tenantId = @tenantId`
- [ ] tenantId is first condition in WHERE clause (partition key)
- [ ] All CREATE operations include tenantId in document
- [ ] All UPDATE operations filter by tenantId before update
- [ ] All DELETE operations filter by tenantId before delete
- [ ] Container names use prefixed format: `{module-name}_data`

### Service Communication
- [ ] All service calls include X-Tenant-ID header
- [ ] tenantId is extracted and propagated to downstream services
- [ ] No service calls made without tenant context

### Logging
- [ ] All log entries include tenantId
- [ ] Error logs include tenantId
- [ ] Audit logs include tenantId
- [ ] Events include organizationId (tenantId) field

### Events
- [ ] All published events include organizationId (tenantId)
- [ ] Event consumers validate tenantId before processing

## Testing Tenant Isolation

### Unit Tests

```typescript
describe('tenant isolation', () => {
  it('should not return resources from other tenants', async () => {
    const tenantId = 'tenant-123';
    const otherTenantId = 'tenant-456';
    
    const result = await service.listResources(tenantId);
    
    expect(result.every(r => r.tenantId === tenantId)).toBe(true);
    expect(result.some(r => r.tenantId === otherTenantId)).toBe(false);
  });
  
  it('should throw error if tenantId is missing', async () => {
    await expect(service.getResource('', 'resource-123')).rejects.toThrow();
  });
});
```

### Integration Tests

```typescript
it('should return 400 without X-Tenant-ID header', async () => {
  const response = await app.inject({
    method: 'GET',
    url: '/api/v1/resource/resource-123',
    headers: {
      'Authorization': 'Bearer valid-token',
      // Missing X-Tenant-ID
    },
  });
  
  expect(response.statusCode).toBe(400);
});
```

## Common Violations

1. **Missing tenantId in queries**
   - Always include `c.tenantId = @tenantId` in WHERE clause

2. **Missing tenantId in service methods**
   - tenantId should be first parameter

3. **Missing X-Tenant-ID in service calls**
   - Always include in headers

4. **Missing tenantId in logs**
   - Always include tenantId for traceability

5. **Missing tenantId in events**
   - Always include organizationId field

## Quick Validation

Run these checks before deployment:

1. **No queries without tenantId**: All database queries include tenantId
2. **No routes without tenantId**: All routes extract and validate tenantId
3. **No service calls without tenantId**: All service calls include X-Tenant-ID
4. **No logs without tenantId**: All logs include tenantId
5. **No events without tenantId**: All events include organizationId
