---
name: producer-implementation
description: Producer implementation patterns for API operations and business logic
---

# Producer Implementation Patterns

## 🚨 CRITICAL RULE #1: ALL Business Logic in Producers

- **Client**: ONLY connection management (connect, isConnected, disconnect)
- **Producers**: ALL API operations (list, get, create, update, delete)
- Client provides HTTP client instance to producers, nothing more

## 🚨 CRITICAL RULE #8: NO Connection Context Parameters

- **FORBIDDEN**: Adding parameters that exist in ConnectionProfile or ConnectionState
- **MANDATORY**: Access connection context through client instance
- Operations receive ONLY operation-specific parameters

```typescript
// ❌ WRONG - Duplicating connection context
class UserProducer {
  async getUser(
    userId: string,
    apiKey: string,      // NO! In ConnectionProfile
    baseUrl: string,     // NO! In ConnectionProfile
    orgId: string        // NO! In ConnectionState
  ): Promise<User> {
    // ...
  }
}

// ✅ CORRECT - Only operation-specific parameters
class UserProducer {
  constructor(private client: GitHubClient) {}

  async getUser(userId: string): Promise<User> {
    // Client already has apiKey, baseUrl, orgId from profile/state
    const { data } = await this.client.apiClient
      .request({
        url: `/users/${userId}`,  // baseUrl handled by client
        method: 'get'
        // apiKey/auth handled by client interceptor
        // orgId available via this.client.getOrganizationId()
      })
      .catch(handleAxiosError);

    return toUser(data);
  }
}
```

**RULES**:
- ✅ Parameters in ConnectionProfile → Access via client
- ✅ Parameters in ConnectionState → Access via client
- ✅ Operation methods receive ONLY business parameters (IDs, filters, etc.)
- ❌ NEVER add apiKey, token, baseUrl, organizationId to method signatures
- ❌ NEVER duplicate what connect() already provides

**WHY**: Connection context is established once during connect() and managed by the client. Operations should focus on business logic, not connection details.

## Producer Pattern - ALL Business Logic Here

### Producer Class Structure

```typescript
class UserProducer {
  constructor(private client: GitHubClient) {}

  // List operation
  async listUsers(
    results: PagedResults<User>,
    name?: string
  ): Promise<void> {
    const { data } = await this.client.apiClient
      .request({
        url: '/users',
        method: 'get',
        params: {
          limit: results.pageSize,
          page: results.pageNumber,
          name
        }
      })
      .catch(handleAxiosError);

    // Manual assignment (NOT ingest)
    results.items = data.map(toUser) || [];

    // Update count if API provides it
    if (data.total !== undefined) {
      results.count = data.total;
    }
  }

  // Get operation
  async getUser(userId: string): Promise<User> {
    const { data } = await this.client.apiClient
      .request({
        url: `/users/${userId}`,
        method: 'get'
      })
      .catch(handleAxiosError);

    return toUser(data);
  }

  // Create operation
  async createUser(input: UserCreateInput): Promise<User> {
    const { data } = await this.client.apiClient
      .request({
        url: '/users',
        method: 'post',
        data: input
      })
      .catch(handleAxiosError);

    return toUser(data);
  }

  // Delete operation
  async deleteUser(userId: string): Promise<void> {
    await this.client.apiClient
      .request({
        url: `/users/${userId}`,
        method: 'delete'
      })
      .catch(handleAxiosError);
  }
}
```

### 🚨 CRITICAL: NEVER use Promise<any>

- **NEVER use `any`** in producer method signatures
- **ALWAYS use generated interfaces** from generated/api/

## PagedResults Rules

- **ALWAYS use manual assignment**: `results.items = ...`
- **NEVER use `ingest()`** - Unreliable trimming behavior
- **Update `results.count`** when API provides total
- **Set `results.pageToken`** for token-based pagination
- **NEVER modify** `pageNumber`, `pageSize`, or `pageCount`
- **Sorting**: ALWAYS done by API via params, never post-process

## Mapper Pattern - MANDATORY

### ALWAYS use `const output: Type` pattern

```typescript
// ✅ REQUIRED PATTERN
export function toUser(data: any): User {
  // Validate required fields first
  if (!data?.id || !data?.name) {
    throw new InvalidInputError('user', 'Missing required fields');
  }

  const output: User = {
    id: map(UUID, data.id),           // Required - validated above
    name: data.name,                   // Required - validated above
    email: map(Email, data.email),    // Optional - returns Email | undefined
    website: map(URL, data.website),  // Optional - returns URL | undefined
    createdAt: map(DateTime, data.created_at)?.toDate() // DateTime requires .toDate()
  };

  return output;
}
```

**CRITICAL**:
- **NEVER use `!`** (non-null assertion) - Design code to avoid it
- **PREFER `map()` over constructors** - Use `map()` from `@auditmation/util-hub-module-utils` unless map() doesn't meet requirements
- **Validate required fields** - Throw if missing, then TypeScript knows they exist
- **Let map() handle optionals** - It returns `Type | undefined` automatically
- **Always declare const with type** - Enables type checking
- **DateTime special case** - Use `map(DateTime, value)?.toDate()` since interface expects `Date` not `DateTime`
- **Constructor fallback** - Only use constructors directly if map() doesn't provide needed functionality
- **🚨 Null to undefined** - Convert null values to undefined (use `|| undefined` or `map()` which handles this)

```typescript
// ⚠️ AVOID - Using constructors without checking if map() works
export function toUser(data: any): User {
  const output: User = {
    id: new UUID(data.id),                    // ⚠️ Try map(UUID, ...) first
    email: new Email(data.email),             // ⚠️ Try map(Email, ...) first
    createdAt: new DateTime(data.created_at).toDate() // ⚠️ Try map(DateTime, ...)?.toDate() first
  };
  return output;
}
// Only use constructors if map() doesn't meet requirements
```

### Null to Undefined Conversion

**🚨 CRITICAL: API spec never uses `nullable: true`, mappers convert null → undefined**

**RULE**: If external API returns `null` values, convert them to `undefined` in mappers.

```typescript
// ✅ CORRECT - map() automatically converts null → undefined
export function toUser(data: any): User {
  const output: User = {
    id: map(UUID, data.id),              // map() returns undefined if data.id is null
    name: data.name || undefined,         // Explicit: null → undefined
    email: map(Email, data.email),        // map() handles null → undefined
    website: map(URL, data.website)       // map() handles null → undefined
  };
  return output;
}

// ✅ CORRECT - Explicit conversion for non-map fields
export function toOrganization(data: any): Organization {
  const output: Organization = {
    id: data.id !== null ? String(data.id) : undefined,  // null → undefined
    name: data.name || undefined,                        // null → undefined
    isActive: data.isActive ?? undefined                 // null → undefined (nullish coalescing)
  };
  return output;
}

// ❌ WRONG - Leaving null values as-is
export function toUser(data: any): User {
  const output: User = {
    id: map(UUID, data.id),
    name: data.name,        // ❌ Could be null
    email: data.email       // ❌ Could be null
  };
  return output;
}
```

**WHY**:
- TypeScript uses `| undefined` for optional fields, not `| null`
- API spec doesn't have `nullable: true` (keeps it clean)
- Generated types use `Type | undefined`, not `Type | null`
- Consistent with TypeScript conventions

**map() function behavior**:
- `map(Type, null)` → returns `undefined`
- `map(Type, undefined)` → returns `undefined`
- `map(Type, value)` → returns `Type` instance or `undefined`

### ⚠️ WARNING: NEVER use `|| undefined` on number fields

```typescript
// ❌ WRONG - Turns 0 into undefined
count: data.count || undefined         // 0 becomes undefined!
age: data.age || undefined             // 0 becomes undefined!
balance: data.balance || undefined     // 0 becomes undefined!

// ✅ CORRECT - Preserves 0 values
count: data.count ?? undefined         // 0 stays 0, null/undefined → undefined
age: data.age !== null ? data.age : undefined  // Explicit null check
balance: data.balance !== undefined ? data.balance : undefined
```

**WHY**: `0 || undefined` evaluates to `undefined` because 0 is falsy.
- Use `?? undefined` (nullish coalescing) for numbers
- Or explicit `!== null` / `!== undefined` checks
- `|| undefined` is ONLY safe for strings, objects, and arrays

### Extending Mappers

```typescript
export function toUserInfo(data: any): UserInfo {
  const output: UserInfo = {
    ...toUser(data),                          // Reuse base mapper
    lastLogin: map(DateTime, data.last_login)?.toDate(),
    permissions: data.permissions || []
  };
  return output;
}
```

### Field Validation Process

**MANDATORY 3-STEP:**

1. **Analyze interface** (generated/api/index.ts)
2. **Check API schema** (api.yml response)
3. **Map ALL fields** (count must match)

```typescript
// Interface has 5 fields → Mapper must map 5 fields
interface UserInfo {
  id: UUID;           // Required
  name: string;       // Required
  email?: Email;      // Optional
  createdAt: Date;    // Required
  status?: StatusEnum;// Optional
}

export function toUserInfo(raw: any): UserInfo {
  const output: UserInfo = {
    // Required (3)
    id: map(UUID, raw.id),
    name: raw.name,
    createdAt: map(Date, raw.created_at),
    // Optional (2) - MUST be mapped too
    email: map(Email, raw.email),
    status: toEnum(StatusEnum, raw.status)
  };
  return output;
}
```

### Required Field Validation

**🚨 CRITICAL: Mappers MUST throw errors for missing required fields**

```typescript
// ✅ CORRECT - Validate required fields
export function toOrganization(data: any): Organization | undefined {
  if (!data) return undefined;

  // Required field validation - MUST throw error
  if (!data.id && data.id !== 0) {
    throw new InvalidInputError('organization', 'Missing required field: id');
  }

  return {
    id: String(data.id),
    name: data.name || undefined,  // Optional field
  };
}

// ❌ WRONG - Silently returning undefined for missing required field
export function toOrganization(data: any): Organization | undefined {
  if (!data) return undefined;
  if (!data.id) return undefined;  // NO! Should throw error

  return {
    id: String(data.id),
    name: data.name || undefined,
  };
}
```

### Nested Object Handling

When objects appear in nested contexts and might have incomplete data, the **parent mapper** handles validation errors:

```typescript
// Parent mapper catches validation errors from child mappers
export function toTokenScope(data: any): TokenScope {
  // Nested org might have null id in some API responses
  let org: Organization | undefined;
  if (data.org) {
    try {
      org = toOrganization(data.org);  // May throw if id is null
    } catch (error) {
      // Incomplete nested organization - treat as undefined
      org = undefined;
    }
  }

  return {
    org,
    user: data.user ? toUser(data.user) : undefined,
    scope: data.scope || undefined,
  };
}
```

**RULE**:
- **Child mappers**: Always validate required fields, throw errors
- **Parent mappers**: Catch validation errors when nesting allows incomplete objects
- **Direct API responses**: Let errors propagate (invalid response = error)
- **Nested contexts**: Catch and convert to undefined (incomplete nested = skip)

### Enum Mapping

**🚨 CRITICAL: Enum values MUST be snake_case**

**STANDARD**: All enum values in this codebase use snake_case format.

- **NEVER** instantiate EnumValue directly
- **ALWAYS** use `toEnum(EnumClass, value)`
- **DEFAULT**: `toEnum` automatically converts input to snake_case (matches our standard)
- **RARELY NEEDED**: Pass third parameter to override transform only if API truly doesn't use snake_case

```typescript
// ✅ CORRECT - Default snake_case transform (PREFERRED)
const status = toEnum(StatusEnum, data.status);
// Input: "ActiveUser" or "active_user" or "ACTIVE_USER" → Converted to "active_user" → Mapped to enum
// This is the standard - use this unless API has special requirements

// ⚠️ RARE - Custom transform only when API doesn't use snake_case
const status = toEnum(StatusEnum, data.status, (val) => val);
// Only use if API truly returns exact enum values in non-snake_case format
// Most APIs return snake_case, so this is rarely needed

// For required enums, validate first
if (!data?.status) {
  throw new InvalidInputError('resource', 'Missing status');
}
const status = toEnum(StatusEnum, data.status); // Safe - uses default snake_case
```

**Why snake_case is our standard:**
- Consistent across all modules
- Matches OpenAPI spec conventions
- Most REST APIs return enum values in snake_case
- Generated enums from OpenAPI use snake_case values
- `toEnum` default behavior aligns with this standard

**When custom transform might be needed (rare):**
- Legacy API uses ONLY PascalCase enum values (e.g., "ActiveUser" not "active_user")
- Legacy API uses ONLY UPPERCASE values (e.g., "ACTIVE" not "active")
- API documentation explicitly shows non-snake_case enum format

**IMPORTANT**: Before using custom transform, verify the API truly doesn't accept snake_case. Most APIs accept multiple formats but prefer snake_case.

## Complex Mapper Patterns

### Nested objects

```typescript
function toAddress(data: any): Address | undefined {
  if (!data) return undefined;

  const output: Address = {
    street: data.street,
    city: data.city,
    country: toCountry(data.country)
  };
  return output;
}
```

### Arrays

```typescript
function toUsers(data: any[]): User[] {
  if (!Array.isArray(data)) return [];
  return data.map(toUser);
}
```

### Recursive structures

```typescript
function toTreeNode(data: any): TreeNode {
  const output: TreeNode = {
    id: data.id,
    name: data.name,
    children: data.children?.map(toTreeNode)
  };
  return output;
}
```

## Validation Scripts

### Validate Producer Implementation

```bash
# Check producers don't have connection parameters
grep -E "async (get|list|create|update|delete).*\(.*[,\s](apiKey|token|baseUrl|organizationId)" src/*Producer.ts && echo "❌ Producer has connection params!" || echo "✅ Producers clean"

# Check producers use error handler
grep -E "\.catch\(handleAxiosError\)" src/*Producer.ts && echo "✅ Error handling present" || echo "⚠️ Missing error handler"

# Check no Promise<any> in producers
grep -E "Promise<any>" src/*Producer.ts && echo "❌ Found Promise<any>!" || echo "✅ No Promise<any>"
```

### Validate Mapper Patterns

```bash
# Check mappers use const output pattern
grep -E "const output: [A-Z]" src/Mappers.ts && echo "✅ Using output pattern" || echo "⚠️ Check mapper pattern"

# Check mappers validate required fields
grep -E "throw new InvalidInputError.*Missing required" src/Mappers.ts && echo "✅ Required field validation present" || echo "⚠️ Check required field validation"

# Check no non-null assertions
grep "!" src/Mappers.ts | grep -v "//" | grep -v "!=" && echo "❌ Found non-null assertions!" || echo "✅ No non-null assertions"
```

### Validate PagedResults Usage

```bash
# Check PagedResults uses manual assignment (not ingest)
grep -E "results\.items\s*=" src/*Producer.ts && echo "✅ Manual assignment" || echo "⚠️ Check PagedResults pattern"

# Check no ingest() usage
grep "ingest(" src/*Producer.ts && echo "❌ Found ingest()!" || echo "✅ No ingest()"
```

## Comment Style for Producers

**See [code-comment-style skill](./code-comment-style.md) for complete guidelines**

### Key Rules for Producer Code

**NEVER comment standard patterns:**

```typescript
// ❌ WRONG - Commenting obvious pagination conversion
// Convert pageNumber/pageSize to offset/limit
if (results.pageNumber && results.pageSize) {
  params.offset = (results.pageNumber - 1) * results.pageSize;
  params.limit = Math.min(Math.max(results.pageSize, 1), 1000);
}

// ✅ CORRECT - Standard pattern needs no comment
if (results.pageNumber && results.pageSize) {
  params.offset = (results.pageNumber - 1) * results.pageSize;
  params.limit = Math.min(Math.max(results.pageSize, 1), 1000);
}
```

```typescript
// ❌ WRONG - Commenting obvious mapper application
// Apply mappers and set pagination info from response structure
results.items = response.data.data.map(toUser);
results.count = response.data.totalCount || 0;

// ✅ CORRECT - Code is self-documenting
results.items = response.data.data.map(toUser);
results.count = response.data.totalCount || 0;
```

**DO comment non-obvious API behavior:**

```typescript
// ✅ GOOD - Explains API quirk
// API returns user in response.data.data for single gets
// but directly in response.data for list operations
const rawData = response.data.data || response.data;
```

**Reference**: See [code-comment-style.md](./code-comment-style.md) for full guidelines
