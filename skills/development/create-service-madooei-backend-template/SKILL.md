---
name: create-service
description: Guide for creating services in the backend. Use when asked to create a service layer component. Directs to the appropriate service skill based on the type of service needed.
---

# Create Service

Services contain business logic and orchestrate operations between repositories, external APIs, and other services.

## Service Types

There are two types of services in this architecture:

| Type                 | Purpose                                             | Skill                     |
| -------------------- | --------------------------------------------------- | ------------------------- |
| **Resource Service** | CRUD operations on entities (notes, users, etc.)    | `create-resource-service` |
| **Utility Service**  | Cross-cutting concerns (auth, notifications, email) | `create-utility-service`  |

## Which Skill to Use?

### Use `create-resource-service` when:

- Creating a service for a **domain entity** (Note, User, Course, etc.)
- The service will perform **CRUD operations** via a repository
- The service needs **authorization checks** per operation
- The service should **emit events** for real-time updates
- You've already created the schema and repository for this entity

**Example**: `NoteService`, `UserService`, `CourseService`

### Use `create-utility-service` when:

- Creating a service for **cross-cutting concerns**
- The service calls **external APIs** (auth service, payment gateway, etc.)
- The service provides **shared functionality** used by other services
- The service doesn't directly map to a domain entity

**Example**: `AuthenticationService`, `AuthorizationService`, `EmailService`, `NotificationService`

## Service Layer Principles

Regardless of type, all services follow these principles:

1. **Business logic lives here** - Not in controllers or repositories
2. **Dependency injection** - Inject dependencies via constructor
3. **Throw domain errors** - Use errors from `@/errors` (not HTTP errors)
4. **User context** - Accept `AuthenticatedUserContextType` where needed
5. **Return domain types** - Return schema types, not HTTP responses

## File Naming

**Location**: `src/services/{service-name}.service.ts`

| Type     | Example                                                 |
| -------- | ------------------------------------------------------- |
| Resource | `note.service.ts`, `user.service.ts`                    |
| Utility  | `authentication.service.ts`, `authorization.service.ts` |

## See Also

- `create-resource-service` - CRUD services for entities
- `create-utility-service` - Cross-cutting/specialized services
- `add-resource-events` - Add real-time events to a resource service
