---
name: backend-controller-pattern-nestjs
description: Comprehensive NestJS Controller patterns for all controller types. This skill should be used when implementing any controller in NestJS to ensure consistency and use of shared utilities.
metadata:
  priority: 3
  applies_to: [backend, nestjs, controllers]
  supersedes: [backend-controller-pattern, backend-controller-pattern-admin, backend-controller-pattern-me, backend-controller-pattern-studio, backend-controller-pattern-backdoor, backend-controller-pattern-integration]
---

# NestJS Controller Patterns

This skill covers **all controller patterns** in `erify_api`, from general principles to module-specific implementations.

## Canonical Examples

Study these real implementations as the source of truth:
- **Admin**: [admin-client.controller.ts](../../../apps/erify_api/src/admin/clients/admin-client.controller.ts)
- **Studio**: [studio-task-template.controller.ts](../../../apps/erify_api/src/studios/studio-task-template/studio-task-template.controller.ts)
- **Base Controllers**: [base-admin.controller.ts](../../../apps/erify_api/src/admin/base-admin.controller.ts), [base-studio.controller.ts](../../../apps/erify_api/src/studios/base-studio.controller.ts), [base.controller.ts](../../../apps/erify_api/src/lib/controllers/base.controller.ts)

**Detailed code examples**: See [references/controller-examples.md](references/controller-examples.md)

---

## Core Responsibilities

ALL controllers share these responsibilities:

1. **Accept HTTP requests** (Method, Body, Query, Headers)
2. **Validate input** (Check format, required fields)
3. **Translate DTOs** (Convert external format → internal service payloads)
4. **Call Service Layer** (Delegate business logic)
5. **Serialize Response** (Transform/Filter data)
6. **Handle Errors** (Map exceptions to HTTP Status codes)

---

## Shared Principles

### 1. Response Serialization

🔴 **Critical**: ALL endpoints must use Zod for response serialization to ensure no internal data (like database IDs) leaks.

- Use `@ZodResponse(Schema, Status)` for standard responses
- Use `@ZodPaginatedResponse(Schema)` for list endpoints

```typescript
@Get(':id')
@ZodResponse(UserDto)
async getUser(...) { ... }
```

### 2. Validation Pipes

🟡 **Recommended**: Always use `UidValidationPipe` for validating `uid` parameters.

```typescript
@Param('id', new UidValidationPipe(UserService.UID_PREFIX, 'User'))
id: string
```

### 3. DTO Standards

- **Request DTOs**: Define validation rules using `zod`
- **Response DTOs**: Define output shape, excluding sensitive fields
- **Pagination**: Use `PaginationQueryDto` from `@/lib/pagination/pagination.schema`

### 4. HTTP Status Codes

| Method   | Success Code   | Decorator Implementation                         |
| :------- | :------------- | :----------------------------------------------- |
| `GET`    | 200 OK         | Default / `@ZodResponse(S, HttpStatus.OK)`       |
| `POST`   | 201 Created    | `@ZodResponse(S, HttpStatus.CREATED)`            |
| `PATCH`  | 200 OK         | `@ZodResponse(S, HttpStatus.OK)`                 |
| `DELETE` | 204 No Content | `@ZodResponse(undefined, HttpStatus.NO_CONTENT)` |

### 5. Payload Translation & Property Filtering

🔴 **Critical**: Controllers MUST adapt external DTOs to internal Service Payloads and filter unnecessary properties.

**Why:**
1. Services should be decoupled from HTTP layer and context-agnostic
2. Services define clean contracts for exactly what they need
3. DTOs may contain extra fields (pagination, UI state, metadata) that services don't need
4. Passing entire DTOs couples services to API structure changes

**Rule**: ALWAYS extract only the properties the service contract requires. NEVER pass entire DTO objects.

```typescript
@Post()
async create(@Param('orgId') orgId: string, @Body() dto: CreateUserDto) {
  // ✅ GOOD: Extract ONLY what service needs
  const { name, email } = dto;
  // Filtered out: dto.pageSize, dto.sortOrder, etc.
  return this.userService.create({
    name,
    email,
    org: { connect: { uid: orgId } }
  });
}

// ❌ BAD: Pass entire DTO
async create(@Body() dto: CreateUserDto) {
  return this.userService.create(dto); // Service now knows about ALL DTO fields
}

// ❌ BAD: Spread operator without explicit filtering
async create(@Body() dto: CreateUserDto) {
  return this.userService.create({ ...dto }); // Same problem
}

// ❌ BAD: Deleting properties
async create(@Body() dto: CreateUserDto) {
  delete dto.pageSize; // Mutating DTO, not explicit about what service needs
  return this.userService.create(dto);
}
```

**Pattern for complex DTOs**:

```typescript
// DTO may have many fields for validation/UI purposes
interface CreateTaskDto {
  name: string;
  description: string;
  assigneeId?: string;
  // Extra fields controllers use but services don't need:
  returnUrl?: string;      // UI navigation
  skipNotification?: boolean; // HTTP-specific flag
}

@Post()
async create(@Body() dto: CreateTaskDto) {
  // ✅ Extract only service contract fields
  const { name, description, assigneeId } = dto;

  const task = await this.taskService.create({
    name,
    description,
    assigneeId,
  });

  // Controller handles HTTP-specific logic
  if (dto.skipNotification) {
    // Controller decision, not service concern
  }

  return task;
}
```

### 6. Layer Boundaries

🟡 **Recommended**: Maintain strict separation of concerns.

```
[ HTTP Controller ]  <-- Knows about Requests, Responses, Status Codes
        |
        v
[ Business Service ] <-- Knows about Logic, Transactions, Domain Errors
        |
        v
[ Data Repository ]  <-- Knows about Database, SQL, ORM
```

**Anti-Patterns:**
- ❌ Controller running SQL queries (Leaky abstraction)
- ❌ Controller containing complex logic (Fat controller)
- ❌ Service returning HTTP objects (Service coupled to transport)

### 7. Pagination

🟡 **Recommended**: Always limit lists to prevent DoS and performance issues.

**Standard Response Format:**
```json
{
  "data": [ ... ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 150
  }
}
```

---

## Admin Controllers

**Use Case:** System admin endpoints for managing resources across the entire system.

### Core Principles

1. 🔴 **Critical**: All admin controllers MUST extend `BaseAdminController`
2. 🔴 **Critical**: Automatically protected by `@AdminProtected()` via the base class
3. 🟡 **Recommended**: Use `@AdminResponse()` and `@AdminPaginatedResponse()` instead of generic Zod decorators
4. 🟡 **Recommended**: All routes must start with `admin/`

### Base Controller Features

`BaseAdminController` provides:
- `@AdminProtected()` decorator application
- `createPaginatedResponse()` helper
- `ensureResourceExists()` and `ensureFieldExists()` helpers

### Checklist

- [ ] Controller extends `BaseAdminController`
- [ ] Route prefix is `admin/<resource>`
- [ ] Uses `@AdminResponse` / `@AdminPaginatedResponse`
- [ ] Uses `UidValidationPipe` for ID parameters
- [ ] Uses `ensureResourceExists` for 404 checks

---

## Studio Controllers

**Use Case:** Studio-scoped endpoints for resources that belong to a specific studio.

### Core Principles

1. 🔴 **Critical**: Extend `BaseStudioController`
2. 🔴 **Critical**: Path structure must be `studios/:studioId/resource`
3. 🔴 **Critical**: All queries must filter by studio context
4. 🟡 **Recommended**: Use `@ZodResponse()` and `@ZodPaginatedResponse()`

### Authorization

`BaseStudioController` automatically requires studio membership via `@StudioProtected()`.

**Add role restrictions** at class or method level:

```typescript
import { STUDIO_ROLE } from '@eridu/api-types/memberships';
import { StudioProtected } from '@/lib/decorators/studio-protected.decorator';

// All endpoints require ADMIN
@StudioProtected([STUDIO_ROLE.ADMIN])
@Controller('studios/:studioId/task-templates')
export class StudioTaskTemplateController extends BaseStudioController { }

// Mixed: default membership, admin for delete
@Controller('studios/:studioId/resource')
export class ResourceController extends BaseStudioController {
  @Get() list() { } // Any member
  
  @StudioProtected([STUDIO_ROLE.ADMIN])
  @Delete(':id') delete() { } // Admin only
}
```

**Available roles**: `STUDIO_ROLE.ADMIN`, `STUDIO_ROLE.MEMBER`

### Quick Reference

| Pattern | Code |
|---------|------|
| **Studio scoping** | `studioUid: studioId` (list), `studio: { uid: studioId }` (findOne/update/delete) |
| **UID validation** | `@Param('studioId', new UidValidationPipe(StudioService.UID_PREFIX, 'Studio'))` |
| **Studio relation** | `studio: { connect: { uid: studioId } }` (create) |
| **DTO extraction** | `const { name, description } = dto;` then pass to service |

### Checklist

- [ ] Extends `BaseStudioController`
- [ ] Route: `studios/:studioId/resource`
- [ ] Authorization: `@StudioProtected([roles])` if role restrictions needed
- [ ] UID validation on `studioId` and resource `id`
- [ ] Studio scoping in all queries
- [ ] Create operations connect studio relation

---

## User (Me) Controllers

**Use Case:** Authenticated users interacting with their own resources.

### Core Principles

1. 🟡 **Recommended**: Standard NestJS controller (no specific base class required)
2. 🔴 **Critical**: ALWAYS use `@CurrentUser()` to scope operations to the authenticated user
3. 🟡 **Recommended**: Routes typically start with `me/` or implied user context

### Checklist

- [ ] Route starts with `me/` or is user-scoped
- [ ] Uses `@CurrentUser()` to get user ID
- [ ] 🔴 **Critical**: NEVER trusts user ID from request body/params for self-operations
- [ ] Uses `@ZodResponse` or `@ZodPaginatedResponse`

---

## Backdoor Controllers

**Use Case:** Service-to-service communication or internal tools using API Key authentication.

### Core Principles

1. 🔴 **Critical**: All backdoor controllers MUST extend `BaseBackdoorController`
2. 🔴 **Critical**: Automatically authenticated via API Key using the `@Backdoor()` decorator (from base class)
3. 🟡 **Recommended**: All routes must start with `backdoor/`

### Checklist

- [ ] Controller extends `BaseBackdoorController`
- [ ] Route prefix is `backdoor/<resource>`
- [ ] Uses `@ZodResponse` for serialization
- [ ] NO `@CurrentUser` decorator (concept doesn't exist for API keys)

---

## Integration Controllers

**Use Case:** External integrations like Google Sheets extensions or webhooks.

### Core Principles

1. 🟡 **Recommended**: Integration controllers should extend their specific base class (e.g., `BaseGoogleSheetsController`)
2. 🟡 **Recommended**: Use specific decorators for the integration type (e.g., `@GoogleSheets()`)
3. 🟡 **Recommended**: Response format often requires specific serialization compatibility (e.g., snake_case for external tools)

### Checklist

- [ ] Controller extends appropriate base (e.g., `BaseGoogleSheetsController`)
- [ ] Uses specific auth decorator (e.g., `@GoogleSheets`)
- [ ] Uses `@ZodSerializerDto` for strict output serialization

---

## Best Practices Summary

- [ ] Choose the correct controller type (Admin/Studio/Me/Backdoor/Integration)
- [ ] Extend the appropriate base controller
- [ ] Use Zod serialization for ALL outputs with `@ZodResponse`
- [ ] Use `UidValidationPipe` for all UIDs
- [ ] 🔴 **Critical**: Translate DTOs into typed Service Payloads (never pass DTOs directly)
- [ ] Apply proper authorization decorators
- [ ] Scope queries appropriately (studio/user context)
- [ ] Document all endpoints via decorators
- [ ] Use correct HTTP status codes
- [ ] Implement pagination for list endpoints

---

## Related Skills

- **[Service Pattern NestJS](service-pattern-nestjs/SKILL.md)** - Service layer patterns
- **[Data Validation](data-validation/SKILL.md)** - Input validation and serialization
- **[Shared API Types](shared-api-types/SKILL.md)** - API contracts and schemas
- **[Database Patterns](database-patterns/SKILL.md)** - Soft delete, transactions
