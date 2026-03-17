---
name: mapper-validation
description: Mapper field validation process ensuring zero missing fields
---

# Mapper Field Validation Process

Complete validation workflow for ensuring mappers correctly handle all interface fields.

## MANDATORY 3-STEP VALIDATION

Every mapper MUST follow this validation process:

### Step 1: Interface Analysis

**READ the target interface** from `generated/api/index.ts`:

```typescript
// Example: After running npm run clean && npm run generate
interface UserInfo {
  id: UUID;           // Required
  name: string;       // Required
  email?: Email;      // Optional
  createdAt: Date;    // Required
  status?: StatusEnum;// Optional
}
```

**DOCUMENT ALL FIELDS**:
- Count total fields: 5
- Required fields (3): id, name, createdAt
- Optional fields (2): email, status
- **CRITICAL**: Record the exact count

### Step 2: API Response Schema Validation

**EXAMINE the corresponding response schema** in api.yml:

```yaml
components:
  schemas:
    UserInfo:
      type: object
      required:
        - id
        - name
        - created_at
      properties:
        id:
          type: string
        name:
          type: string
        email:
          type: string
          format: email
        created_at:
          type: string
          format: date-time
        status:
          type: string
          enum: [active, inactive, pending]
```

**VERIFY**:
- Each interface field has corresponding API response field
- Required fields match between interface and schema
- Optional fields are correctly optional

### Step 3: Complete Mapping Implementation

**IMPLEMENT mapper with ALL fields using any**:

```typescript
export function toUserInfo(raw: any): UserInfo {
  // Validate required fields first using ensureProperties
  ensureProperties(raw, ['id', 'name', 'created_at']);

  // 🚨 CRITICAL: Map ALL fields (must match interface count)
  const output: UserInfo = {
    // Required (3) - validated above
    id: String(raw.id),
    name: raw.name,
    createdAt: map(DateTime, raw.created_at),

    // Optional (2) - MUST be mapped too
    email: map(Email, raw.email),
    status: toEnum(StatusEnum, raw.status)
  };

  return output;
}
```

**Type Safety Rules:**
- ✅ ALL mapper parameters use `any` for simplicity
- ✅ Use `ensureProperties()` helper for validating required fields
- ✅ Add `/* eslint-disable */` at top of mapper file
```

**VALIDATION**:
- **ZERO MISSING FIELDS**: Interface field count = Mapped field count
- If interface has 5 fields → mapper MUST map 5 fields
- If interface has 10 fields → mapper MUST map 10 fields

## Field Count Validation

**MANDATORY CHECK**: Before considering mapper complete, count fields:

```typescript
// ✅ CORRECT - All 5 fields mapped
interface UserInfo {
  id: UUID;           // 1
  name: string;       // 2
  email?: Email;      // 3
  createdAt: Date;    // 4
  status?: StatusEnum;// 5
}

export function toUserInfo(raw: any): UserInfo {
  ensureProperties(raw, ['id', 'name', 'created_at']);

  const output: UserInfo = {
    id: map(UUID, raw.id),           // 1 ✓
    name: raw.name,                   // 2 ✓
    email: map(Email, raw.email),    // 3 ✓
    createdAt: map(DateTime, raw.created_at), // 4 ✓
    status: toEnum(StatusEnum, raw.status) // 5 ✓
  };
  return output;
}
// Field count: 5 = 5 ✅ PASS

// ❌ WRONG - Missing fields
export function toUserInfo(raw: any): UserInfo {
  ensureProperties(raw, ['id', 'name', 'created_at']);

  const output: UserInfo = {
    id: map(UUID, raw.id),           // 1 ✓
    name: raw.name,                   // 2 ✓
    createdAt: map(DateTime, raw.created_at) // 3 ✓
    // Missing: email (field 4)
    // Missing: status (field 5)
  };
  return output;
}
// Field count: 3 ≠ 5 ❌ FAIL
```

**RULE**: Interface field count MUST EQUAL mapped field count.

## Nested Object Handling

For nested objects, use non-exported helper mappers:

```typescript
// Parent interface
interface Organization {
  id: UUID;
  name: string;
  address?: Address;  // Nested object
}

// Nested interface
interface Address {
  street: string;
  city: string;
  country?: string;
}

// ✅ CORRECT - Helper mapper for nested object with validation
function toAddress(raw: any): Address {
  // 🚨 CRITICAL: Helper functions MUST validate required fields
  ensureProperties(raw, ['street', 'city']);

  const output: Address = {
    street: raw.street,
    city: raw.city,
    country: optional(raw.country)
  };
  return output;
}

// Main mapper uses helper with mapWith
export function toOrganization(raw: any): Organization {
  ensureProperties(raw, ['id', 'name']);

  const output: Organization = {
    id: String(raw.id),
    name: raw.name,
    address: mapWith(toAddress, raw.address)  // mapWith handles null/undefined
  };
  return output;
}
```

**CRITICAL RULES**:
- ✅ Helper mappers MUST use `any` parameter type
- ✅ Helper mappers MUST validate their own required fields with `ensureProperties()`
- ✅ Helper mappers are NOT exported (no `export` keyword)
- ✅ Defined above the main mapper function
- ✅ Use `mapWith()` in parent to handle null/undefined at boundary
- ✅ Helper returns plain type `T`, not `T | undefined` (mapWith adds the undefined)
- ❌ NEVER skip validation in helper functions

## Optional Field Handling

Optional fields MUST still be mapped, returning `undefined` when absent:

```typescript
// ✅ CORRECT - Optional field mapped
export function toUser(data: any): User {
  ensureProperties(data, ['id', 'name']);

  const output: User = {
    id: map(UUID, data.id),              // Required
    name: data.name,                      // Required
    email: map(Email, data.email),       // Optional - returns Email | undefined
    website: map(URL, data.website)      // Optional - returns URL | undefined
  };
  return output;
}

// ❌ WRONG - Optional field missing
export function toUser(data: any): User {
  ensureProperties(data, ['id', 'name']);

  const output: User = {
    id: map(UUID, data.id),
    name: data.name,
    email: map(Email, data.email)
    // Missing: website - even though optional, must be mapped
  };
  return output;
}
```

**WHY**: TypeScript interface includes the field, mapper must provide it (even if undefined).

## Validation Checklist

Before completing a mapper:

- [ ] Read generated interface from `generated/api/index.ts`
- [ ] Counted total interface fields (required + optional)
- [ ] Documented required vs optional fields
- [ ] Checked API response schema in api.yml
- [ ] Validated required fields with error throwing
- [ ] Mapped ALL required fields
- [ ] Mapped ALL optional fields (with `| undefined`)
- [ ] Used `const output: Type` pattern
- [ ] Verified field count: interface count = mapper count
- [ ] No fields missing from mapper
- [ ] Helper mappers for nested objects (not exported)

## Common Mistakes

### Mistake 1: Skipping Optional Fields

```typescript
// ❌ WRONG - Skipping optional fields
interface User {
  id: UUID;
  name: string;
  email?: Email;      // Optional but must be mapped!
  phone?: string;     // Optional but must be mapped!
}

export function toUser(data: any): User {
  ensureProperties(data, ['id', 'name']);

  return {
    id: map(UUID, data.id),
    name: data.name
    // Missing email and phone - WRONG even if optional
  };
}
```

**FIX**: Map all fields, optional or not.

### Mistake 2: Not Counting Fields

```typescript
// ❌ WRONG - No validation of field count
// Developer maps 3 fields, interface has 5, doesn't notice
```

**FIX**: Explicitly count before and after.

### Mistake 3: Assuming Defaults

```typescript
// ❌ WRONG - Assuming undefined for missing fields
interface Resource {
  id: UUID;
  name: string;
  tags?: string[];  // Optional array
}

export function toResource(data: any): Resource {
  ensureProperties(data, ['id', 'name']);

  return {
    id: map(UUID, data.id),
    name: data.name
    // Missing tags - TypeScript might allow but it's wrong
  };
}
```

**FIX**: Explicitly map optional fields:
```typescript
export function toResource(data: any): Resource {
  ensureProperties(data, ['id', 'name']);

  return {
    id: map(UUID, data.id),
    name: data.name,
    tags: data.tags || undefined  // Explicit
  };
}
```

## Nested Model Example

Complete example with nested objects:

```typescript
// Interfaces (from generated/api/index.ts)
interface Organization {
  id: UUID;
  name: string;
  address?: Address;
  owner?: User;
}

interface Address {
  street: string;
  city: string;
  postalCode?: string;
}

interface User {
  id: UUID;
  name: string;
  email?: Email;
}

// Helper mappers (not exported)
function toAddress(data: any): Address {
  ensureProperties(data, ['street', 'city']);

  const output: Address = {
    street: data.street,
    city: data.city,
    postalCode: data.postal_code || undefined  // All 3 fields mapped
  };
  return output;
}

function toUser(data: any): User {
  ensureProperties(data, ['id', 'name']);

  const output: User = {
    id: map(UUID, data.id),
    name: data.name,
    email: map(Email, data.email)  // All 3 fields mapped
  };
  return output;
}

// Main mapper (exported)
export function toOrganization(data: any): Organization {
  ensureProperties(data, ['id', 'name']);

  const output: Organization = {
    id: map(UUID, data.id),
    name: data.name,
    address: mapWith(toAddress, data.address),  // mapWith handles null/undefined
    owner: mapWith(toUser, data.owner)           // mapWith handles null/undefined
  };
  return output;  // All 4 fields mapped
}
```

**VALIDATION**:
- Organization interface: 4 fields → Mapper: 4 fields ✅
- Address interface: 3 fields → Helper mapper: 3 fields ✅
- User interface: 3 fields → Helper mapper: 3 fields ✅

## Discovery Process

### When implementing a new mapper:

1. **Run generation**:
   ```bash
   npm run clean && npm run generate
   ```

2. **Open generated interface**:
   ```typescript
   // generated/api/index.ts
   export interface NewResource {
     // Read all fields here
   }
   ```

3. **Count fields**:
   - Total: ?
   - Required: ?
   - Optional: ?

4. **Check API schema**:
   ```yaml
   # api.yml
   components:
     schemas:
       NewResource:
         required: [...]
         properties:
           ...
   ```

5. **Implement mapper**:
   ```typescript
   export function toNewResource(data: any): NewResource {
     ensureProperties(data, ['required_field1', 'required_field2']);

     const output: NewResource = {
       // Map ALL fields
     };
     return output;
   }
   ```

6. **Validate**:
   - Count fields in mapper
   - Compare with interface count
   - Must match exactly

## Runtime Validation (MANDATORY)

**CRITICAL**: Static field counting is necessary but NOT sufficient.

After implementing mapper, you MUST perform runtime validation to detect:
- Field name mismatches (API `mobilePhone` vs spec `phoneNumber`)
- Fields in API but not in spec
- Fields in spec but not mapped correctly
- Type conversion errors

### When to Run Runtime Validation

**MANDATORY for:**
- New module creation (after all operations implemented)
- Adding new operations to existing module
- API spec updates
- After mapper refactoring

### Quick Runtime Validation Process

1. **Add temporary debug log** in producer BEFORE mapping:
   ```typescript
   this.logger.debug('[TEMP-RAW-API] operationName:', JSON.stringify(response.data, null, 2));
   ```

2. **Run tests with debug logging:**
   ```bash
   env LOG_LEVEL=debug npm run test:integration > /tmp/debug.log 2>&1
   ```

3. **Compare raw API vs mapped output:**
   ```bash
   # Extract raw API response
   grep -A 100 "\[TEMP-RAW-API\]" /tmp/debug.log

   # Compare with mapped result in test logs
   grep "Api\." /tmp/debug.log
   ```

4. **Fix any missing fields** then remove temp logs

**RULE**: Mapper validation is NOT complete until runtime validation shows ZERO missing fields.

See complete process: mapper-runtime-validation skill

## References

- Mapper Pattern: implementation skill (Mapper Pattern section)
- Runtime Validation: mapper-runtime-validation skill
- Type Mapping: type-mapping skill
- Error Handling: error-handling skill
- Operation Engineer agent: @.claude/agents/operation-engineer.md
- Mapping Engineer agent: @.claude/agents/mapping-engineer.md
