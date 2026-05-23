---
name: data-mapping
description: Data mapping patterns for transforming API responses to internal types
---

# Mapper Implementation Patterns

## Core Mapper Principles

1. **API spec drives mapper logic** - NOT the other way around
2. **ZERO MISSING FIELDS** - Interface field count MUST EQUAL mapped field count
3. **PREFER map() utility** over constructors
4. **ALWAYS validate required fields** from API spec
5. **Use const output pattern** in all mappers
6. **Convert snake_case to camelCase** consistently
7. **Apply core types** (UUID, Email, URL, DateTime) via map()
8. **Use `optional()` for optional fields** - Normalize null to undefined, preserve "", 0, false
9. **NEVER weaken API spec** to make mapper easier
10. **Use InvalidState for validation errors** - throw immediately on missing required fields
11. **Declare helpers before exports** - nested mappers declared BEFORE main mapper but NOT exported
12. **map() handles null/undefined** - No ternary checks needed with map(), it returns undefined automatically
13. **No fallbacks between different fields** - If API has 2 fields, output has 2 fields. No merging, no defaults
14. **Use any for raw parameters** - All raw parameters should be `any` for simplicity
15. **Extract complex inline mappings** - Nested objects with 3+ properties should be helper functions
16. **Helper functions MUST validate** - All helper functions need `ensureProperties()` for required fields
17. **Enum arrays use map pattern** - `raw.field?.map((d: any) => toEnum(EnumType, d))`

See type-mapping skill for complete type conversion reference.

## Mapper Function Naming Convention

**MANDATORY**: All mapper functions MUST use the `to<Model>` naming pattern.

### Pattern: to<Model>

```typescript
// ✅ CORRECT - to<Model> pattern with any
export function toUser(raw: any): User { }
export function toGroup(raw: any): Group { }
export function toEntry(raw: any): Entry { }

// Helper functions (non-exported) also use to<Model>
function toUserIdentity(raw: any): UserIdentity { }
function toAddress(raw: any): Address { }

// ❌ WRONG - Using 'any' instead of any
export function mapUser(raw: any): User { }      // NO!
export function mapGroup(raw: any): Group { }    // NO!
```

### Rationale

1. **Concise and clear** - "to" clearly indicates conversion/transformation
2. **Consistent with helpers** - Internal helpers already use `to` prefix
3. **Industry standard** - Common pattern in TypeScript/JavaScript
4. **Matches other utilities** - toEnum(), toString(), toDate() convention

### Naming Rules

- **Exported mappers**: `export function to<Model>(raw: any): <Model>`
- **Helper mappers**: `function to<NestedModel>(raw: any): <NestedModel>` (not exported)
- **Model name**: Exact TypeScript interface name (User, Group, Entry, UserIdentity, etc.)
- **NO map prefix**: `toUser` not `mapUser`
- **NO get prefix**: `toUser` not `getUser`

### Examples

```typescript
// Main resource mappers
export function toUser(raw: any): User { }
export function toGroup(raw: any): Group { }
export function toRole(raw: any): Role { }
export function toSite(raw: any): Site { }
export function toEntry(raw: any): Entry { }
export function toZone(raw: any): Zone { }

// Nested object helpers (not exported)
function toUserIdentity(raw: any): UserIdentity { }
function toAddress(raw: any): Address { }
function toContactInfo(raw: any): ContactInfo { }
function toOrganizationRef(raw: any): OrganizationRef { }

// Extended models
export function toUserInfo(raw: any): UserInfo { }
export function toGroupInfo(raw: any): GroupInfo { }
```

## Standard Mapper Function Structure

### Canonical Format

All mapper functions MUST follow this exact structure:

```typescript
export function to<Resource>(raw: any): <Resource> {
  // 1. Check for required fields
  ensureProperties(raw, ['id', 'required_field']);
  // Or manual validation:
  // if (!raw.id) {
  //   throw new InvalidStateError('Missing required field: id');
  // }

  // 2. Create output object
  const output: <Resource> = {
    // Property mappings here
  };

  return output;
}
```

### Complete Example with All Patterns

```typescript
// src/Mappers.ts
import { map } from '@zerobias-org/util-hub-module-utils';
import { UUID, Email, URL, DateTime, InvalidStateError } from '@zerobias-org/types-core-js';
import { User, Address, UserStatus, UserRole } from '../generated/model';
import { mapWith, ensureProperties, optional } from './util';  // Import helpers

// Helper function - NOT exported, declared BEFORE main mapper
function toAddress(raw: any): Address {
  // 1. Check for required fields
  ensureProperties(raw, ['street']);

  // 2. Create output object
  const output: Address = {
    street: raw.street,
    city: optional(raw.city),
    zipCode: optional(raw.zip_code)
  };

  return output;
}

// Main mapper - exported, uses helper
export function toUser(raw: any): User {
  // 1. Check for required fields
  ensureProperties(raw, ['id', 'email', 'first_name', 'status']);

  // 2. Create output object
  const output: User = {
    id: raw.id.toString(),                              // ID conversion
    email: raw.email,                                   // Direct mapping (required)
    firstName: raw.first_name,                          // snake_case → camelCase (required)
    lastName: optional(raw.last_name),                  // Optional - normalizes null to undefined, keeps ""
    createdAt: map(DateTime, raw.created_at),          // map() handles required/optional automatically
    updatedAt: map(DateTime, raw.updated_at),          // map() returns undefined if null/undefined
    dateOfBirth: map(Date, raw.date_of_birth),         // No ternary needed - map() handles it
    status: toEnum(UserStatus, raw.status),            // Enum conversion
    phoneNumber: optional(raw.phone_number),           // Optional - null→undefined, keeps "", 0, false
    address: mapWith(toAddress, raw.address),          // Nested object with mapWith
    roles: raw.roles?.map((r: any) => toEnum(UserRole, r))  // Array mapping
  };

  return output;
}
```

## Property Mapping Patterns

### 1. Direct Mapping (Same Type)

**For required fields** - direct mapping:

```typescript
{
  email: raw.email,        // Required - direct mapping
  firstName: raw.first_name // Required - snake_case → camelCase
}
```

**For optional fields** - use `optional()`:

```typescript
{
  description: optional(raw.description), // Optional - null→undefined, keeps ""
  count: optional(raw.count),        // Optional - null→undefined, keeps 0
  active: optional(raw.active)       // Optional - null→undefined, keeps false
}
```

**Rule:** Direct mapping for required fields. Use `optional()` for optional fields to normalize null.

### 2. ID Conversion

Always convert numeric IDs to strings:

```typescript
{
  id: raw.id.toString()  // or raw.id if already string
}
```

### 3. Constructor-Based Conversion with map()

Use `map()` helper for types with constructors (Date, UUID, Email, URL, etc.):

```typescript
import { map } from '@zerobias-org/util-hub-module-utils';
import { UUID, Email, URL, DateTime } from '@zerobias-org/types-core-js';

{
  createdAt: map(DateTime, raw.created_at),    // Required or optional - map() handles both
  updatedAt: map(DateTime, raw.updated_at),    // map() returns undefined if raw.updated_at is null/undefined
  userId: map(UUID, raw.user_id),
  email: map(Email, raw.email)
}
```

**Rule:** `map()` handles undefined/null automatically and returns undefined. No need for ternary checks.

**❌ WRONG - Don't use ternary with map():**
```typescript
{
  dateOfBirth: raw.dateOfBirth ? map(Date, raw.dateOfBirth) : undefined  // ❌ Redundant
}
```

**✅ CORRECT - map() handles it:**
```typescript
{
  dateOfBirth: map(Date, raw.dateOfBirth)  // ✅ map() returns undefined if raw.dateOfBirth is null/undefined
}
```

**Why map() is preferred:**
- Handles optional/undefined values automatically - returns undefined if input is null/undefined
- Provides consistent error handling
- Validates input during conversion
- Cleaner, more concise code - no ternary needed

### 4. Enum Conversion with toEnum()

Use `toEnum()` helper for enum properties:

```typescript
{
  status: toEnum(StatusEnum, raw.status)
}
```

**Default behavior:** Values are converted to `snake_case` before enum lookup.

**Custom transformation:** Pass a second parameter transformation function:

```typescript
{
  type: toEnum(TypeEnum, raw.type, (v) => v.toUpperCase()),
  format: toEnum(FormatEnum, raw.format, (v) => v.toLowerCase())
}
```

### 5. Optional/Nullable Properties

**Use `optional()` helper to normalize null while preserving all other values:**

```typescript
{
  description: optional(raw.description),  // null→undefined, preserves "", 0, false
  phoneNumber: optional(raw.phone_number), // Normalizes only null
  name: optional(raw.name),                // Keeps empty strings
  count: optional(raw.count),              // Keeps 0 as 0
  active: optional(raw.active)             // Keeps false as false
}
```

**Why `optional()`?**
- Normalizes `null` → `undefined` (consistent "no value" representation) ✅
- Preserves empty strings `""` (legitimate value) ✅
- Preserves zeros `0` (legitimate value) ✅
- Preserves `false` (legitimate boolean value) ✅
- One "no value" state (`undefined`) instead of two (`null` and `undefined`)
- Cleaner, more semantic than `?? undefined` ✅

**❌ WRONG - Logical OR destroys legitimate values:**
```typescript
{
  name: raw.name || undefined,  // ❌ Converts "", 0, false to undefined (data loss!)
  count: raw.count || 0,        // ❌ Converts null/undefined to 0 (default injection!)
  active: raw.active || false,  // ❌ Converts null/undefined to false (default injection!)
  description: raw.description ? raw.description : undefined  // ❌ Converts "", 0, false to undefined
}
```

**✅ CORRECT - optional() preserves legitimate falsy values:**
```typescript
{
  name: optional(raw.name),        // ✅ null→undefined, keeps ""
  count: optional(raw.count),      // ✅ null→undefined, keeps 0
  active: optional(raw.active),    // ✅ null→undefined, keeps false
  description: optional(raw.description)  // ✅ null→undefined, keeps ""
}
```

**IMPORTANT - No Fallbacks or Defaults Between Different Fields:**

**❌ WRONG - Don't merge different API fields:**
```typescript
{
  phoneNumber: raw.mobilePhone || raw.phoneNumber || undefined  // ❌ NO!
}
```

**✅ CORRECT - Map each API field to its own output field:**
```typescript
{
  mobilePhone: optional(raw.mobilePhone),
  phoneNumber: optional(raw.phoneNumber)
}
```

**Rule:** If the API has 2 different fields, your output should have 2 different fields. No fallbacks, no defaults, no merging. Use `optional()` for optional fields.

### 6. Nested Objects

**For single nested objects:** Use non-exported helper functions with `mapWith()`:

```typescript
// Helper function - NOT exported, declared BEFORE main mapper
// Does NOT check for null - mapWith() handles that
function toSubResource(raw: any): SubResource {
  // 1. Check for required fields
  ensureProperties(raw, ['id']);

  // 2. Create output object
  const output: SubResource = {
    id: raw.id.toString(),
    name: optional(raw.name)
  };

  return output;
}

// Main mapper - exported, uses helper with mapWith()
export function toResource(raw: any): Resource {
  // 1. Check for required fields
  ensureProperties(raw, ['id']);

  // 2. Create output object
  const output: Resource = {
    id: raw.id.toString(),
    nestedObject: mapWith(toSubResource, raw.nested_object)  // ✅ mapWith handles null/undefined
  };

  return output;
}
```

**For arrays:** Call mapper directly (NO mapWith):

```typescript
// Helper for array items - call directly, NO mapWith
function toSubResource(raw: any): SubResource {
  // 1. Check for required fields
  ensureProperties(raw, ['id']);

  // 2. Create output object
  const output: SubResource = {
    id: raw.id.toString(),
    name: optional(raw.name)
  };

  return output;
}

// Main mapper - arrays call helper directly
export function toResource(raw: any): Resource {
  const output: Resource = {
    id: raw.id.toString(),
    items: raw.items?.map(toSubResource)  // ✅ Direct call, no mapWith
  };

  return output;
}
```

**Rules:**
- Nested mappers are declared BEFORE the parent mapper but are NOT exported
- **Helper functions assume valid input** - they don't check for null/undefined
- **Single objects:** Use `mapWith()` - handles null/undefined at boundary
- **Arrays:** Call mapper directly (NO mapWith) - `raw.items?.map(toMapper)`
- **Return type:** Helpers return plain `T`, not `T | undefined` (mapWith adds the undefined)

## Function Ordering Rules

Mapper functions in `Mappers.ts` MUST be ordered as follows:

### 1. Helper Functions First

All non-exported helper functions declared BEFORE any exported functions:

```typescript
// Helper 1 - NOT exported
function toAddress(raw: any): Address {
  // Implementation
}

// Helper 2 - NOT exported
function toContactInfo(raw: any): ContactInfo {
  // Implementation
}

// Exported mapper that uses helpers
export function toUser(raw: any): User {
  const output: User = {
    address: toAddress(raw.address),
    contact: toContactInfo(raw.contact)
  };
  return output;
}
```

### 2. Dependency Order

If mapper A uses mapper B, B MUST be declared first:

```typescript
// B declared first
function toAddress(raw: any): Address { }

// A declared second (depends on B)
function toUser(raw: any): User {
  return {
    address: toAddress(raw.address)  // Uses B
  };
}
```

### 3. Alphabetical Within Groups

Within each group (helpers, exports), order functions alphabetically:

```typescript
// Helpers in alphabetical order
function toAddress(raw: any): Address { }
function toContactInfo(raw: any): ContactInfo { }
function toMetadata(raw: any): Metadata { }

// Exports in alphabetical order
export function toOrganization(raw: any): Organization { }
export function toUser(raw: any): User { }
export function toWebhook(raw: any): Webhook { }
```

**Exception:** Dependency order overrides alphabetical order.

### 7. Array Mapping

**For arrays of nested objects** - call mapper directly (NO mapWith):

```typescript
{
  // Array of nested objects - call mapper directly
  items: Array.isArray(raw.items) ? raw.items.map(toSubResource) : undefined
}
```

For required arrays (no optional chaining):

```typescript
{
  // Required array - validate and map
  items: Array.isArray(raw.items) ? raw.items.map(toSubResource) : []
}
```

**For array of enums:**

```typescript
{
  // Single enum array
  roles: Array.isArray(raw.roles) ? raw.roles.map(r => toEnum(UserRole, r)) : undefined,

  // ✅ CORRECT - daysOfWeek enum array pattern
  daysOfWeek: Array.isArray(raw.daysOfWeek) ? raw.daysOfWeek.map(d => toEnum(ScheduleEvent.DaysOfWeekEnum, d)) : undefined
}
```

**Key points:**
- Arrays: use `Array.isArray()` check first for type safety
- Helper functions don't check null/undefined - they assume valid input
- Enum arrays use same pattern with `toEnum()` in map callback

## Required Field Validation

### Pattern: Validate Before Mapping

```typescript
// API spec says 'id' is required
export function toWebhook(raw: any): Webhook {
  // 1. Check for required fields
  if (!raw.id) {
    throw new InvalidStateError('Missing required field: id');
  }

  // 2. Create output object
  const output: Webhook = {
    id: raw.id.toString(),
    // ... other fields
  };

  return output;
}
```

**Key points:**
- Check for required fields BEFORE any mapping
- Use `InvalidStateError` from `@zerobias-org/types-core-js`
- Use `ensureProperties()` helper for multiple fields or manual `if` checks for single fields
- Throw immediately - don't return undefined for missing required fields
- Use section comment: `// 1. Check for required fields`

### Handling Falsy Values

**`ensureProperties()` correctly handles all falsy values:**

```typescript
// ✅ CORRECT - ensureProperties handles 0, "", false correctly
ensureProperties(raw, ['id', 'count', 'active', 'name']);
// Passes validation for: id=0, count=0, active=false, name=""
// Fails validation for: id=null, id=undefined
```

The helper only checks for `null` and `undefined`, so all other falsy values (`0`, `''`, `false`) pass validation correctly.

## Optional Field Handling

### Pattern: Use `optional()` to Normalize Null

```typescript
// Handle optional fields with optional()
const output: Webhook = {
  name: optional(raw.name),             // null→undefined, keeps ""
  email: map(Email, raw.email),         // map() handles undefined/null
  count: optional(raw.count),           // null→undefined, keeps 0
  active: optional(raw.active),         // null→undefined, keeps false
  tags: optional(raw.tags),             // null→undefined, keeps []
  metadata: mapWith(toMetadata, raw.metadata)  // mapWith handles optional nested objects
};
```

**Key patterns:**
- `raw.field` - Direct mapping for required fields
- `optional(raw.field)` - Normalize null to undefined for optional fields
- `map(Type, raw.field)` - map() automatically handles undefined/null
- `mapWith(toNested, raw.nested)` - mapWith handles optional nested objects

**❌ NEVER use logical OR or inject defaults:**
```typescript
// ❌ WRONG - Logical OR destroys legitimate values
name: raw.name || undefined   // Converts "", 0, false to undefined
count: raw.count || 0         // Converts null/undefined to 0 (default injection!)
tags: raw.tags || []          // Converts null/undefined to [] (default injection!)
active: raw.active || false   // Converts null/undefined to false (default injection!)

// ✅ CORRECT - optional() preserves legitimate values
name: optional(raw.name)    // null→undefined, keeps ""
count: optional(raw.count)  // null→undefined, keeps 0
tags: optional(raw.tags)    // null→undefined, keeps []
active: optional(raw.active) // null→undefined, keeps false
```

## snake_case to camelCase Conversion

### Always Convert Field Names

```typescript
// API returns snake_case, internal types use camelCase
const output: Webhook = {
  createdAt: map(DateTime, data.created_at),              // ✅
  updatedAt: map(DateTime, data.updated_at),              // ✅
  lastTriggeredAt: map(DateTime, data.last_triggered_at)  // ✅
};
```

**Conversion rules:**
- `created_at` → `createdAt`
- `updated_at` → `updatedAt`
- `last_triggered_at` → `lastTriggeredAt`
- `content_type` → `contentType`
- `insecure_ssl` → `insecureSsl`

## API Spec is Source of Truth

### ❌ WRONG APPROACH: Weakening spec for mapper

```yaml
# api.yml - DON'T DO THIS
Organization:
  type: object
  properties:    # ❌ NO! Don't remove required to make mapper easier
    id:
      type: string
```

**Why wrong:** Removes critical API contract information just to avoid validation in mapper.

### ✅ CORRECT APPROACH: Mapper validates spec

```yaml
# api.yml - Keep spec accurate
Organization:
  type: object
  required:
    - id       # ✅ YES! Spec reflects API reality
  properties:
    id:
      type: string
```

```typescript
// Mapper validates required fields
export function toOrganization(raw: any): Organization {
  // 1. Check for required fields
  if (!raw.id) {
    throw new InvalidStateError('Missing required field: id');
  }

  // 2. Create output object
  const output: Organization = {
    id: raw.id.toString(),
    name: raw.name
  };

  return output;
}
```

**Why correct:** API spec stays accurate, mapper enforces the contract.

## Nested Object Mapping

### Pattern: Create Separate Mapper Functions

```typescript
// Parent mapper
export function toWebhook(data: any): Webhook | undefined {
  if (!data) return undefined;

  const output: Webhook = {
    id: map(UUID, data.id),
    config: toWebhookConfig(data.config),  // Call nested mapper
    metadata: toMetadata(data.metadata)     // Another nested mapper
  };

  return output;
}

// Nested mapper
export function toWebhookConfig(data: any): WebhookConfig | undefined {
  if (!data) return undefined;

  const output: WebhookConfig = {
    url: map(URL, data.url),
    contentType: data.content_type || 'json'
  };

  return output;
}
```

## Array Mapping

### Pattern: Map and Filter

```typescript
// Array mapper
export function toWebhookArray(data: any): Webhook[] {
  if (!Array.isArray(data)) return [];
  return data.map(toWebhook).filter((w): w is Webhook => w !== undefined);
}
```

**Key points:**
- Check `Array.isArray()` first
- Use `.map()` to transform each item
- Use `.filter()` to remove undefined results
- Type predicate: `(w): w is Webhook => w !== undefined`

## Const Output Pattern

### Always Use const output

```typescript
export function toWebhook(data: any): Webhook | undefined {
  if (!data) return undefined;

  // ✅ YES - Use const output pattern
  const output: Webhook = {
    id: map(UUID, data.id),
    name: data.name || undefined,
    // ... all fields
  };

  return output;
}
```

**Why this pattern:**
- Clear type declaration
- All fields visible in one place
- Easy to review completeness
- TypeScript catches missing fields

**Anti-pattern:**
```typescript
// ❌ NO - Building object incrementally
export function toWebhook(data: any): Webhook | undefined {
  if (!data) return undefined;

  const webhook: Partial<Webhook> = {};
  webhook.id = map(UUID, data.id);
  webhook.name = data.name;
  // Easy to miss fields
  return webhook as Webhook;
}
```

## Validation Checklist

### Verify Mapper Implementation

```bash
# Mappers.ts exists
ls src/Mappers.ts

# Uses map() utility
grep "import.*map.*from.*@zerobias-org/util-hub-module-utils" src/Mappers.ts
# Should show import

# Prefers map() over constructors
CONSTRUCTOR_COUNT=$(grep -E "new (UUID|Email|URL|DateTime)\(" src/Mappers.ts | wc -l)
MAP_COUNT=$(grep -E "map\((UUID|Email|URL|DateTime)," src/Mappers.ts | wc -l)
# MAP_COUNT should be >= CONSTRUCTOR_COUNT

# Validates required fields
grep "Missing required field" src/Mappers.ts
# Should show validation for required fields

# Const output pattern
grep "const output:" src/Mappers.ts
# Should show const pattern

# No environment variables
grep "process.env" src/Mappers.ts
# Should return nothing
```

## Standard Output Format

When documenting mapper implementation:

```markdown
# Mapper Implementation: Mappers.ts

## Mapper Functions Created

### toWebhook(data: any): Webhook | undefined
- **Validates**: id (required field)
- **Converts**: created_at → createdAt (DateTime)
- **Handles**: Optional fields (name, description)
- **Nested**: config → WebhookConfig via toWebhookConfig()
- **Uses**: map() for UUID, DateTime conversions

### toWebhookArray(data: any): Webhook[]
- **Handles**: Array conversion
- **Filters**: undefined results

### toWebhookConfig(data: any): WebhookConfig | undefined
- **Converts**: content_type → contentType
- **Uses**: map() for URL conversion
- **Handles**: Optional fields

## Type Conversions Applied
✅ UUID via map()
✅ DateTime via map() (snake_case → camelCase)
✅ URL via map()
✅ Optional fields handled
✅ Required fields validated

## Validation
✅ map() utility used (preferred)
✅ Required fields validated
✅ const output pattern
✅ snake_case → camelCase
✅ Core types applied
✅ No environment variables

## Code Location
- src/Mappers.ts
```

## Success Criteria

Mapper implementation MUST meet all criteria:

- ✅ All mappers use **const output pattern**
- ✅ **map() utility preferred** over constructors
- ✅ **Required fields validated** per API spec
- ✅ **Optional fields handled** correctly (still map them!)
- ✅ **snake_case converted** to camelCase consistently
- ✅ **Core types applied** (UUID, Email, URL, DateTime)
- ✅ **No API spec weakening** for mapper convenience
- ✅ **ZERO MISSING FIELDS** - all interface fields mapped
- ✅ One mapper function per type
- ✅ Nested objects use separate mapper functions
- ✅ Arrays use array mapper pattern with filter

## Utility Functions

### toEnum() Helper

The `toEnum()` function converts string values to enum values with optional transformation:

```typescript
/**
 * Converts a string value to an enum value
 * @param enumType - The enum object
 * @param value - The string value to convert
 * @param transform - Optional transformation function (default: converts to snake_case)
 */
function toEnum<T>(
  enumType: object,
  value: string,
  transform?: (v: string) => string
): T {
  // Implementation expected to be available in the module
}
```

**Usage examples:**

```typescript
// Default: converts to snake_case
status: toEnum(UserStatus, raw.status)
// raw.status = "activeUser" → converted to "active_user" → matched to enum

// Custom transformation: uppercase
type: toEnum(TypeEnum, raw.type, (v) => v.toUpperCase())
// raw.type = "admin" → "ADMIN" → matched to enum

// Custom transformation: lowercase
format: toEnum(FormatEnum, raw.format, (v) => v.toLowerCase())
```

### map() Helper

The `map()` utility function handles type conversion with automatic optional/undefined handling:

```typescript
import { map } from '@zerobias-org/util-hub-module-utils';
import { UUID, Email, URL, DateTime } from '@zerobias-org/types-core-js';

// Automatically handles optional/undefined
id: map(UUID, raw.id)           // Required
email: map(Email, raw.email)     // Optional - returns undefined if raw.email is undefined
createdAt: map(DateTime, raw.created_at)
```

### ensureProperties() Helper for Required Field Validation

For validating multiple required fields at once, use `ensureProperties()` from `src/util.ts`:

```typescript
import { ensureProperties } from './util';
```

**Type Signature:**

```typescript
function ensureProperties<K extends string>(
  raw: unknown,
  properties: readonly K[]
): asserts raw is Record<K, NonNullable<unknown>>
```

**Usage:**

```typescript
// Before - Manual validation
export function toUser(raw: any): User {
  // 1. Check for required fields
  if (!raw.id) {
    throw new InvalidStateError('Missing required field: id');
  }
  if (!raw.email) {
    throw new InvalidStateError('Missing required field: email');
  }
  if (!raw.status) {
    throw new InvalidStateError('Missing required field: status');
  }

  // 2. Create output object
  const output: User = {
    id: raw.id.toString(),
    email: raw.email,
    status: toEnum(UserStatus, raw.status)
  };

  return output;
}

// After - Using ensureProperties with TypeScript type inference
export function toUser(raw: any): User {
  // 1. Check for required fields
  ensureProperties(raw, ['id', 'email', 'status']);
  // TypeScript now knows: raw.id, raw.email, raw.status exist and are not null/undefined

  // 2. Create output object
  const output: User = {
    id: raw.id.toString(),    // ✅ TypeScript knows raw.id exists
    email: raw.email,          // ✅ TypeScript knows raw.email exists
    status: toEnum(UserStatus, raw.status)  // ✅ TypeScript knows raw.status exists
  };

  return output;
}
```

**Benefits:**
- **Less boilerplate** - One line instead of multiple if statements
- **TypeScript type inference** - Assertion signature tells TypeScript properties exist
- **Consistent error messages** - All use same format
- **Easy to see requirements** - Array shows all required fields at a glance
- **Correctly handles falsy values** - Only checks `null`/`undefined`, allows `0`, `false`, `""` ✅
- **Better IDE support** - Autocomplete and type checking after validation

**Falsy Value Handling:**

`ensureProperties()` implementation explicitly checks `value === null || value === undefined`, which means:
- ✅ `0` passes validation (legitimate numeric value)
- ✅ `""` passes validation (legitimate empty string)
- ✅ `false` passes validation (legitimate boolean value)
- ❌ `null` fails validation (missing value)
- ❌ `undefined` fails validation (missing value)

This is the correct behavior - we preserve all legitimate values and only reject truly missing ones.

### optional() Helper for Normalizing Null to Undefined

For optional fields that may be `null`, use `optional()` from `src/util.ts` to normalize `null` → `undefined`:

```typescript
import { optional } from './util';
```

**Type Signature:**

```typescript
function optional<T>(value: T | null | undefined): T | undefined {
  return value ?? undefined;
}
```

**Usage:**

```typescript
// Before - Manual null normalization
export function toUser(raw: any): User {
  ensureProperties(raw, ['id', 'email']);

  const output: User = {
    id: raw.id.toString(),
    email: raw.email,
    phoneNumber: raw.phoneNumber ?? undefined,
    avatarUrl: raw.avatarUrl ?? undefined,
    middleName: raw.middleName ?? undefined
  };

  return output;
}

// After - Using optional() for cleaner code
export function toUser(raw: any): User {
  ensureProperties(raw, ['id', 'email']);

  const output: User = {
    id: raw.id.toString(),
    email: raw.email,
    phoneNumber: optional(raw.phoneNumber),
    avatarUrl: optional(raw.avatarUrl),
    middleName: optional(raw.middleName)
  };

  return output;
}
```

**Benefits:**
- **Cleaner code** - `optional(raw.field)` vs `raw.field ?? undefined`
- **More semantic** - Clearly indicates "this field is optional"
- **Preserves falsy values** - Only converts `null` to `undefined`, keeps `0`, `''`, `false`
- **Consistent pattern** - Works alongside `map()`, `mapWith()`, `ensureProperties()`

**What optional() does:**
- ✅ `optional(null)` → `undefined` (normalizes null)
- ✅ `optional(undefined)` → `undefined` (passes through)
- ✅ `optional(0)` → `0` (preserves zero)
- ✅ `optional("")` → `""` (preserves empty string)
- ✅ `optional(false)` → `false` (preserves false)
- ✅ `optional("value")` → `"value"` (preserves value)

### mapWith() Helper for Single Nested Objects

For single nested objects, use `mapWith()` from `src/util.ts` which works like `map()` but for custom mapper functions:

```typescript
import { mapWith } from './util';
```

```typescript
/**
 * Applies a mapper function to a value, handling null/undefined at the boundary
 * Works like map() but for custom mapper functions instead of constructors
 * @param mapper - The mapper function to apply (assumes valid input)
 * @param value - The value to map
 * @returns Mapped value or undefined if input is null/undefined
 */
function mapWith<T>(mapper: (raw: any) => T, value: any): T | undefined {
  if (value === null || value === undefined) {
    return undefined;
  }
  return mapper(value);
}
```

**Usage examples:**

```typescript
// Helper function - does NOT check for null (mapWith handles it)
function toSubResource(raw: any): SubResource {
  ensureProperties(raw, ['id']);

  const output: SubResource = {
    id: raw.id.toString(),
    name: optional(raw.name)
  };

  return output;
}

// Single nested object - mapWith handles null/undefined
export function toResource(raw: any): Resource {
  ensureProperties(raw, ['id']);

  const output: Resource = {
    id: raw.id.toString(),
    subResource: mapWith(toSubResource, raw.sub_resource),  // ✅ Clean! mapWith handles null
    contact: mapWith(toContactInfo, raw.contact)
  };

  return output;
}

// For arrays - DON'T use mapWith, call mapper directly
export function toUser(raw: any): User {
  const output: User = {
    id: raw.id.toString(),
    // ✅ Call mapper directly (NO mapWith for arrays)
    addresses: raw.addresses?.map(toAddress)
  };

  return output;
}

// Helper for arrays - same structure, no null check
function toAddress(raw: any): Address {
  ensureProperties(raw, ['street']);

  return {
    street: raw.street,
    city: optional(raw.city)
  };
}
```

**Benefits:**
- **Consistent with `map()` pattern** - handles null/undefined automatically
- **Separation of concerns** - null handling in `mapWith()`, validation in helpers
- **Only for single nested objects** - arrays use direct mapper call
- **No ternary clutter**: `mapWith(toSubResource, raw.sub)` vs `raw.sub ? toSubResource(raw.sub) : undefined`
- **Helper functions are simpler** - no null checks, just validation + transformation

**Implementation location:**
- Currently: `src/util.ts` - import with `import { mapWith } from './util'`
- Future: Will be moved to `@zerobias-org/util-hub-module-utils` alongside `map()` and `toEnum()`

## Inline Object Mapping - ANTI-PATTERN

### ❌ AVOID: Complex Inline Object Mappings

Never create complex inline object mappings with 3+ properties. Extract to helper functions instead.

```typescript
// ❌ WRONG - Complex inline mapping (hard to read, test, maintain)
export function toEntryUser(raw: any): EntryUser {
  ensureProperties(raw, ['id']);

  const output: EntryUser = {
    id: String(raw.id),
    identity: raw.identity ? {  // ❌ COMPLEX INLINE MAPPING
      id: (raw.identity as any).id ? String((raw.identity as any).id) : undefined,
      firstName: optional((raw.identity as any).firstName),
      middleName: optional((raw.identity as any).middleName),
      lastName: optional((raw.identity as any).lastName),
      fullName: optional((raw.identity as any).fullName),
      initials: optional((raw.identity as any).initials),
      email: map(Email, (raw.identity as any).email as string),
    } : undefined,
  };
  return output;
}
```

### ✅ CORRECT: Extract to Helper Function

```typescript
// Helper function - declared before main mapper
function toEntryUserIdentity(raw: any): EntryUserIdentity {
  ensureProperties(raw, ['id', 'email']);  // ✅ Validates required fields

  const output: EntryUserIdentity = {
    id: String(raw.id),
    firstName: optional(raw.firstName),
    middleName: optional(raw.middleName),
    lastName: optional(raw.lastName),
    fullName: optional(raw.fullName),
    initials: optional(raw.initials),
    email: map(Email, raw.email),
  };
  return output;
}

// Main mapper - uses helper with mapWith
export function toEntryUser(raw: any): EntryUser {
  ensureProperties(raw, ['id']);

  const output: EntryUser = {
    id: String(raw.id),
    identity: mapWith(toEntryUserIdentity, raw.identity),  // ✅ Clean, testable
  };
  return output;
}
```

**Benefits of Helper Functions:**
1. **Readability** - Each function has single responsibility
2. **Testability** - Can unit test helpers independently
3. **Reusability** - Helper can be used by multiple mappers
4. **Maintainability** - Changes isolated to one function
5. **Validation** - Helper can validate its own required fields

**Rule:** If an inline object mapping has 3+ properties OR requires type casting, extract it to a helper function.

## Common Patterns Quick Reference

```typescript
// Required field validation - use ensureProperties helper
ensureProperties(raw, ['id', 'email', 'status']);
// ✅ Correctly handles 0, "", false - only rejects null/undefined

// Core type conversion - map() handles undefined automatically
id: map(UUID, raw.id)
email: map(Email, raw.email)
url: map(URL, raw.url)
createdAt: map(DateTime, raw.created_at)
dateOfBirth: map(Date, raw.dateOfBirth)  // No ternary needed!

// Enum conversion
status: toEnum(StatusEnum, raw.status)
type: toEnum(TypeEnum, raw.type, (v) => v.toUpperCase())

// Optional field handling - use optional() to normalize null
name: optional(raw.name)           // null→undefined, keeps ""
description: optional(raw.description)  // null→undefined, preserves ""
phoneNumber: optional(raw.phone_number) // null→undefined, keeps "", 0, false
count: optional(raw.count)         // null→undefined, keeps 0
active: optional(raw.active)       // null→undefined, keeps false

// Single nested object - use mapWith()
config: mapWith(toConfig, raw.config)      // mapWith handles null/undefined at boundary
address: mapWith(toAddress, raw.address)

// Array of nested objects - call mapper directly (NO mapWith)
items: raw.items?.map(toSubResource)       // toSubResource assumes valid input
contacts: raw.contacts?.map(toContact)     // toContact returns Contact

// Array of enums
roles: raw.roles?.map((r: any) => toEnum(UserRole, r))

// ❌ NEVER use logical OR - destroys legitimate values
name: raw.name || undefined        // ❌ WRONG - converts "" to undefined
count: raw.count || 0              // ❌ WRONG - default injection

// ❌ NEVER merge different API fields
phoneNumber: raw.mobilePhone || raw.phoneNumber  // ❌ WRONG - fallback between fields

// ✅ Use optional() for optional fields
name: optional(raw.name)        // ✅ CORRECT - null→undefined, keeps ""
count: optional(raw.count)      // ✅ CORRECT - null→undefined, keeps 0

// ✅ Map each field separately
mobilePhone: optional(raw.mobilePhone)  // ✅ CORRECT
phoneNumber: optional(raw.phoneNumber)  // ✅ CORRECT
```
