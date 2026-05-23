---
name: data-validation
description: Provides comprehensive guidance for input validation, data serialization, and ID management in backend APIs. This skill should be used when designing validation schemas, transforming request/response data, mapping database IDs to external identifiers, and ensuring type safety across API boundaries.
---

# Data Validation Skill

Provides comprehensive guidance for input validation, response serialization, and ID management.

## Core Concepts

**API Contract vs Internal Implementation**:

```
┌─────────────────────────────────────────┐
│          Client (External)              │
│    snake_case IDs, user-friendly        │
└──────────────┬──────────────────────────┘
               │
         HTTP API Boundary
               │
┌──────────────▼──────────────────────────┐
│    Your Application (Internal)          │
│    camelCase IDs, database structure    │
└─────────────────────────────────────────┘
```

**Responsibilities at each layer**:

| Layer      | Responsibility                                     |
| ---------- | -------------------------------------------------- |
| Controller | Validate input (schema), serialize output (schema) |
| Service    | Business logic with internal format                |
| Repository | Database access with internal format               |
| Database   | Storage with primary keys                          |

## ID Management Pattern

### External API Contract

```
URL:
  GET /admin/users/:id     // id = uid (user_abc123)

Response:
{
  "id": "user_abc123",                  // UID mapped as id
  "email": "user@example.com",
  "name": "John Doe",
  // NO "uid" field
  // NO database "id" field (bigint primary key)
}
```

### Internal Implementation

```
Database:
{
  id: 12345,                // bigint primary key (NEVER exposed)
  uid: "user_abc123",       // Branded UID
  email: "user@example.com",
  name: "John Doe",
}

Services and Repositories:
- Use uid: "user_abc123"
- Never expose id: 12345
- Query by uid: WHERE uid = 'user_abc123'
```

### UID Format

```
Pattern: {PREFIX}_{RANDOM_ID}

Examples:
- user_abc123
- show_xyz789
- client_def456
- studio_ghi012

Key Rules:
- ✅ Prefix has no trailing underscore
- ✅ Use cryptographically secure random
- ✅ Make globally unique
- ❌ Never expose database ID pattern
- ❌ Never expose prefix pattern in error messages
```

## Input Validation Pattern

**Validate at API boundary, transform format**:

```
Client Request (snake_case):
{
  "email": "user@example.com",
  "user_id": "user_123",
  "is_banned": false
}
    ↓
Validation Layer:
- Check required fields
- Check format (email, length, etc.)
- Check references exist (user_id)
    ↓
Transform Layer (snake_case → camelCase):
{
  email: "user@example.com",
  userId: "user_123",
  isBanned: false
}
    ↓
Service Layer (processes camelCase)
```

**Validation Schema Example**:

```
Input schema:
- email: string, email format, required
- name: string, min 1 char, max 255 chars
- is_banned: boolean, optional
- user_id: string, matches UID format

Validation rules:
- Transform snake_case → camelCase
- Check format of IDs (startsWith prefix)
- Check required fields
- Check string lengths
```

## Response Serialization Pattern

**Transform internal format to API format**:

```
Service returns (camelCase, internal):
{
  id: 12345n,                 // database ID (never in response!)
  uid: "user_abc123",         // UID (maps to "id")
  email: "user@example.com",
  isBanned: false,
  createdAt: Date,
  updatedAt: Date,
}
    ↓
Serialization Layer:
- Map uid → id
- Hide database id field
- Transform camelCase → snake_case
- Transform dates to ISO format
    ↓
Client receives (snake_case, friendly):
{
  "id": "user_abc123",        // UID as id
  "email": "user@example.com",
  "is_banned": false,
  "created_at": "2025-01-14T10:00:00Z",
  "updated_at": "2025-01-14T10:00:00Z"
  // NO "uid" field
  // NO database "id" field
}
```

**Serialization Schema Example**:

```
Output schema (from service):
- uid: string
- email: string
- isBanned: boolean
- createdAt: Date
- updatedAt: Date

Transform to DTO:
- uid → id
- isBanned → is_banned
- createdAt → created_at
- updatedAt → updated_at
```

## Nested Validation

**Validate related entities by UID**:

```
Input (user creating a show):
{
  "name": "Studio A Show",
  "client_id": "client_123",      // Client UID
  "studio_room_id": "room_456",   // StudioRoom UID
  "show_type_id": "type_bau",     // ShowType UID
}

Validation:
1. Check string format (looks like UID)
2. Service verifies entity exists
3. Service queries by UID
4. If not found, throw not-found error
```

**Key Rules**:
- ✅ Validate UID format (starts with prefix)
- ✅ Service verifies entity exists (query)
- ✅ Return not-found error if missing
- ❌ Never assume IDs exist without checking
- ❌ Never expose missing ID in error details

## Type Mapping

**Database → Service → API**:

```
Database     | Service       | API Response
─────────────┼───────────────┼──────────────
bigint       | bigint        | string (UID)
string (uid) | string (uid)  | string (id)
boolean      | boolean       | boolean
timestamp    | Date          | ISO string
```

**Transformation Examples**:

```
Database integer → API string (UID):
  DB: { id: 12345, uid: "user_abc123" }
  Service: { uid: "user_abc123" }
  API: { "id": "user_abc123" }

Database TIMESTAMP → API ISO string:
  DB: { created_at: 2025-01-14 10:00:00 }
  Service: { createdAt: Date(2025-01-14 10:00:00) }
  API: { "created_at": "2025-01-14T10:00:00Z" }

Database boolean → API boolean:
  DB: { is_banned: true }
  Service: { isBanned: true }
  API: { "is_banned": true }
```

## Pagination Validation

**Validate pagination parameters**:

```
Input:
{
  "page": "1",      // String from query param
  "limit": "10"
}

Validation:
- Convert to number
- Check >= 1
- Check <= max (e.g., 100)
- Provide defaults (page: 1, limit: 10)

Output:
{
  page: 1,
  limit: 10
}
```

## Error Messages

**Security-conscious error messages**:

```
✅ GOOD: Context-specific, doesn't expose internals
{
  "statusCode": 404,
  "message": "User not found",
  "error": "NotFound"
}

✅ GOOD: Validation error with field info
{
  "statusCode": 400,
  "message": "Validation failed",
  "error": "BadRequest",
  "details": [
    { "field": "email", "message": "Invalid email format" }
  ]
}

❌ BAD: Exposes internal ID format
{
  "statusCode": 404,
  "message": "User uid_123 not found"  // Reveals UID pattern
}

❌ BAD: Exposes database structure
{
  "statusCode": 404,
  "message": "No row with id 12345 found"  // Reveals database ID
}
```

## Best Practices Checklist

- [ ] Validate all input at controller boundary
- [ ] Use schema validation (Zod, Joi, Pydantic)
- [ ] Transform snake_case → camelCase on input
- [ ] Map uid → id in API responses
- [ ] Hide database primary keys completely
- [ ] Transform camelCase → snake_case on output
- [ ] Check UID format (matches prefix pattern)
- [ ] Validate referenced entities exist
- [ ] Return not-found error if entity missing
- [ ] Support pagination with validation
- [ ] Convert timestamps to ISO format
- [ ] Error messages don't expose internal structure
- [ ] Error messages are actionable for clients
- [ ] Serialization is consistent across endpoints
- [ ] No sensitive data in responses

## Related Skills

- **backend-controller-pattern/SKILL.md** - Validation at HTTP boundary
- **service-pattern/SKILL.md** - Business logic validation
- **repository-pattern/SKILL.md** - Data access layer
