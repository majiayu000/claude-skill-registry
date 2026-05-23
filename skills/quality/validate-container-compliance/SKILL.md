---
name: validate-container-compliance
description: Ensures containers comply with .cursorrules and ModuleImplementationGuide.md standards. Checks for hardcoded ports/URLs, verifies tenant isolation in database queries, validates configuration structure, checks event naming conventions, verifies service-to-service auth patterns, and ensures proper error handling. Use when reviewing code, validating container structure, ensuring standards compliance, or before deployment.
---

# Validate Container Compliance

Validates containers against .cursorrules and ModuleImplementationGuide.md standards.

## Compliance Checklist

### 1. No Hardcoded Values

Check for:
- ❌ Hardcoded ports: `port: 3000`
- ❌ Hardcoded URLs: `'http://localhost:3021'`
- ❌ Hardcoded secrets in code
- ❌ Hardcoded paths

✅ **Correct**: Use config with environment variables
```yaml
server:
  port: ${PORT:-3000}
services:
  auth:
    url: ${AUTH_URL:-http://localhost:3021}
```

Reference: .cursorrules (Core Principles), ModuleImplementationGuide.md Section 4.2

### 2. Tenant Isolation

Verify:
- ✅ All database queries include `tenantId` in partition key
- ✅ Routes use `authenticateRequest()` and `tenantEnforcementMiddleware()` in preHandler
- ✅ Routes access tenantId via `request.user!.tenantId`
- ✅ Service-to-service calls include `X-Tenant-ID` header

**Database Query Pattern:**
```typescript
// ✅ Correct
const query = `SELECT * FROM c WHERE c.tenantId = @tenantId AND c.id = @id`;

// ❌ Wrong
const query = `SELECT * FROM c WHERE c.id = @id`;
```

Reference: .cursorrules (Security Requirements), ModuleImplementationGuide.md Section 8

### 3. Configuration Structure

Validate:
- ✅ `config/default.yaml` exists
- ✅ `config/schema.json` exists
- ✅ Config uses environment variable syntax: `${VAR:-default}`
- ✅ Config typed with TypeScript interfaces
- ✅ Config loader validates against schema

Reference: ModuleImplementationGuide.md Section 4 (Configuration Standards)

### 4. Event Naming Convention

Check events follow: `{domain}.{entity}.{action}`

✅ **Correct:**
- `user.created`
- `auth.login.success`
- `notification.email.sent`

❌ **Wrong:**
- `userCreated`
- `loginSuccess`
- `emailSent`

Reference: ModuleImplementationGuide.md Section 9.1

### 4a. Events: RabbitMQ Only and tenantId

- ✅ No Azure Service Bus, Event Grid, or other message brokers; **RabbitMQ only** for events and job triggers
- ✅ Events and `createBaseEvent` use **tenantId** for tenant context (prefer over organizationId)
- ✅ Batch job triggers: `workflow.job.trigger`; workers consume from a queue (e.g. `bi_batch_jobs`)

Reference: .cursorrules (Platform Conventions), ModuleImplementationGuide.md §9.1, §9.6

### 4b. BI/risk Observability (§8.5)

For risk-analytics, ml-service, forecasting, recommendations, workflow-orchestrator, logging, dashboard-analytics:

- ✅ **App Insights:** `@azure/monitor-opentelemetry`; init before other imports; config `application_insights.connection_string`, `application_insights.disable`
- ✅ **/metrics:** prom-client; `http_requests_total`, `http_request_duration_seconds`, app-specific (`risk_evaluations_total`, `ml_predictions_total`, `batch_job_duration_seconds`); when `metrics.require_auth` true, validate `Authorization: Bearer` against `metrics.bearer_token`
- ✅ Config: `metrics.path`, `metrics.require_auth`, `metrics.bearer_token`

Reference: BI_SALES_RISK_IMPLEMENTATION_PLAN §8.5, deployment/monitoring/README.md

### 5. Service-to-Service Auth

Verify:
- ✅ Uses ServiceClient from @coder/shared
- ✅ Includes JWT token in Authorization header
- ✅ Includes X-Tenant-ID header
- ✅ Uses config-driven URLs

```typescript
// ✅ Correct
const client = new ServiceClient({
  baseUrl: config.services.auth.url,
});
await client.get('/api/v1/users/123', {
  headers: {
    'X-Tenant-ID': tenantId,
    'Authorization': `Bearer ${serviceToken}`,
  },
});
```

Reference: .cursorrules (Service Communication), ModuleImplementationGuide.md Section 5.3

### 6. Error Handling

Check:
- ✅ Uses AppError from @coder/shared
- ✅ Includes proper HTTP status codes
- ✅ Logs errors with context (tenantId, userId, correlationId)
- ✅ Never exposes internal errors to clients

```typescript
// ✅ Correct
import { AppError } from '@coder/shared';
throw new AppError('Invalid input', 400, 'VALIDATION_ERROR');

// ❌ Wrong
throw new Error('Invalid input');
```

Reference: ModuleImplementationGuide.md Section 10 (Error Handling)

### 7. Required Files

Verify all required files exist:
- ✅ Dockerfile
- ✅ package.json
- ✅ tsconfig.json
- ✅ README.md
- ✅ CHANGELOG.md
- ✅ config/default.yaml
- ✅ config/schema.json
- ✅ openapi.yaml (in module root)
- ✅ src/server.ts

Reference: ModuleImplementationGuide.md Section 3.2

### 8. Directory Structure

Validate structure matches Section 3.1:
```
containers/[module-name]/
├── Dockerfile
├── package.json
├── tsconfig.json
├── README.md
├── CHANGELOG.md
├── openapi.yaml
├── config/
│   ├── default.yaml
│   └── schema.json
├── src/
│   ├── server.ts
│   ├── config/
│   ├── routes/
│   ├── services/
│   ├── types/
│   └── utils/
└── tests/
    ├── unit/
    ├── integration/
    └── fixtures/
```

Reference: ModuleImplementationGuide.md Section 3.1

### 9. Dependency Rules

Check:
- ✅ No direct imports from other modules' src/ folders
- ✅ Uses @coder/shared for shared types/utilities
- ✅ Communicates via REST API (config-driven URLs) or events
- ✅ No circular dependencies

Reference: ModuleImplementationGuide.md Section 5 (Dependency Rules)

### 10. Database Standards

Verify:
- ✅ Uses prefixed container names: `{module-name}_data`
- ✅ All queries are parameterized (no string concatenation)
- ✅ tenantId always in partition key
- ✅ Uses CosmosDBClient from @coder/shared

Reference: ModuleImplementationGuide.md Section 8 (Database Standards)

## Validation Script

Run these checks:

```bash
# Check for hardcoded URLs
grep -r "http://localhost" src/ --exclude-dir=node_modules

# Check for hardcoded ports
grep -r "port.*[0-9]\{4\}" src/ --exclude-dir=node_modules

# Check database queries for tenantId
grep -r "SELECT.*FROM.*WHERE" src/ --exclude-dir=node_modules | grep -v tenantId

# Check event naming
grep -r "publish\|emit" src/ --exclude-dir=node_modules
```

## Quick Validation

1. **No hardcoded values**: All config from YAML/env vars
2. **Tenant isolation**: All queries include tenantId; events use tenantId
3. **Required files**: All Section 3.2 files present
4. **Directory structure**: Matches Section 3.1
5. **Error handling**: Uses AppError
6. **Service communication**: Uses ServiceClient
7. **Event naming**: Follows {domain}.{entity}.{action}
8. **Events/jobs**: RabbitMQ only; no Azure Service Bus or other brokers
9. **Dependencies**: No direct imports from other modules
