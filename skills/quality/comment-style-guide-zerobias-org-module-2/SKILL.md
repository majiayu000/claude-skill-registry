---
name: comment-style-guide
description: Code comment style guidelines - when to comment and when not to
---

# Code Comment Style Guidelines

## Philosophy

**Write code that doesn't need comments. When comments are needed, make them count.**

## 🚨 CRITICAL RULES

### Rule #1: No Redundant Comments

**FORBIDDEN**: Comments that restate what the code obviously does

```typescript
// ❌ WRONG - Comment restates the code
// Convert pageNumber/pageSize to offset/limit
if (results.pageNumber && results.pageSize) {
  params.offset = (results.pageNumber - 1) * results.pageSize;
  params.limit = Math.min(Math.max(results.pageSize, 1), 1000);
}

// ✅ CORRECT - No comment needed, code is self-explanatory
if (results.pageNumber && results.pageSize) {
  params.offset = (results.pageNumber - 1) * results.pageSize;
  params.limit = Math.min(Math.max(results.pageSize, 1), 1000);
}
```

```typescript
// ❌ WRONG - Obvious from context
// Apply mappers and set pagination info from response structure
results.items = response.data.data.map(toUser);
results.count = response.data.totalCount || 0;

// ✅ CORRECT - Code speaks for itself
results.items = response.data.data.map(toUser);
results.count = response.data.totalCount || 0;
```

### Rule #2: No Structural Comments in Tests

**FORBIDDEN**: Comments that describe test structure instead of business logic

```typescript
// ❌ WRONG
// Validate structure
const groups = groupsResult.items;
expect(groups).to.be.an('array');

// If groups exist, validate the first one
if (groups.length > 0) {
  const firstGroup = groups[0];

  // Validate common group fields that should exist
  if (firstGroup.id) {
    // ID should be a string
    expect(firstGroup.id).to.be.a('string');
  }
}

// ✅ CORRECT - Let the test structure be self-documenting
const groups = groupsResult.items;
expect(groups).to.be.an('array');

if (groups.length > 0) {
  const firstGroup = groups[0];

  if (firstGroup.id) {
    expect(firstGroup.id).to.be.a('string');
  }
}
```

### Rule #3: Concise JSDoc

**Keep JSDoc focused and minimal. Avoid redundant examples.**

```typescript
// ❌ WRONG - Excessive examples
/**
 * Normalizes null to undefined for optional properties
 *
 * This helper ensures consistent handling of optional values by converting
 * null to undefined, while preserving all other values including falsy ones
 * like 0, false, and empty strings.
 *
 * @param value - The value to normalize
 * @returns undefined if input is null or undefined, otherwise returns the value as-is
 *
 * @example
 * // Replaces manual normalization
 * // Before:
 * phoneNumber: raw.phoneNumber ?? undefined,
 * avatarUrl: raw.avatarUrl ?? undefined,
 *
 * // After:
 * phoneNumber: optional(raw.phoneNumber),
 * avatarUrl: optional(raw.avatarUrl),
 *
 * @example
 * // Preserves falsy values (0, false, "")
 * optional(0)        // returns 0 (not undefined)
 * optional(false)    // returns false (not undefined)
 * optional("")       // returns "" (not undefined)
 * optional(null)     // returns undefined
 * optional(undefined) // returns undefined
 */
export function optional<T>(value: T | null | undefined): T | undefined {
  return (value ?? undefined) as T | undefined;
}

// ✅ CORRECT - Concise and focused
/**
 * Normalizes null to undefined for optional properties
 *
 * Converts null to undefined while preserving other falsy values (0, false, "")
 *
 * @param value - The value to normalize
 * @returns undefined if input is null or undefined, otherwise returns the value as-is
 */
export function optional<T>(value: T | null | undefined): T | undefined {
  return (value ?? undefined) as T | undefined;
}
```

### Rule #4: No Function Name Restating

**FORBIDDEN**: JSDoc that only restates the function name

```typescript
// ❌ WRONG - Adds no information
/**
 * Mock authenticated request with proper headers
 */
export function mockAuthenticatedRequest(baseUrl: string, token: string) {
  // ...
}

/**
 * Clean up all nock mocks
 */
export function cleanNock(): void {
  nock.cleanAll();
}

// ✅ CORRECT - Function names are self-documenting for simple functions
export function mockAuthenticatedRequest(baseUrl: string, token: string) {
  // ...
}

export function cleanNock(): void {
  nock.cleanAll();
}
```

## When Comments ARE Valuable

### 1. Business Logic Explanation

```typescript
// ✅ GOOD - Explains WHY, not WHAT
// API returns 400 for invalid credentials but 404 for missing users
// We normalize both to NotConnectedError for consistent handling
if (error.status === 400 || error.status === 404) {
  throw new NotConnectedError();
}
```

### 2. Non-Obvious Behavior

```typescript
// ✅ GOOD - Warns about API quirk
// API returns user data in response.data.data for single gets
// but directly in response.data for list operations
const rawData = response.data.data || response.data;
```

### 3. TODOs and Future Work

```typescript
// ✅ GOOD - Tracks technical debt
// TODO: Move to @zerobias-org/util-hub-module-utils once stabilized
export function mapWith<T>(mapper: (raw: any) => T, value: any): T | undefined {
  // ...
}
```

### 4. Complex Algorithm Explanation

```typescript
// ✅ GOOD - Explains non-trivial logic
// Calculate weighted priority: active bugs (3x) + planned features (1x)
const priority = (bugCount * 3) + featureCount;
```

## Producer-Specific Guidelines

### Pagination Pattern Comments

**NEVER comment standard pagination conversion:**

```typescript
// ❌ WRONG
// Convert pageNumber/pageSize to offset/limit
if (results.pageNumber && results.pageSize) {
  params.offset = (results.pageNumber - 1) * results.pageSize;
  params.limit = Math.min(Math.max(results.pageSize, 1), 1000);
}

// ✅ CORRECT - Standard pattern, no comment needed
if (results.pageNumber && results.pageSize) {
  params.offset = (results.pageNumber - 1) * results.pageSize;
  params.limit = Math.min(Math.max(results.pageSize, 1), 1000);
}
```

### Parameter Handling

**NEVER comment obvious parameter handling:**

```typescript
// ❌ WRONG
// Add optional filter parameter
if (filter) {
  params.filter = filter;
}

// Add optional options parameter
if (options) {
  params.options = options;
}

// ✅ CORRECT
if (filter) {
  params.filter = filter;
}

if (options) {
  params.options = options;
}
```

## Test-Specific Guidelines

### Assertion Comments

**NEVER comment assertions that match their code:**

```typescript
// ❌ WRONG
// Required fields
expect(entry).to.have.property('id');
expect(entry).to.have.property('name');

// ID should be a string
expect(entry.id).to.be.a('string');

// ✅ CORRECT
expect(entry).to.have.property('id');
expect(entry).to.have.property('name');
expect(entry.id).to.be.a('string');
```

### Setup Comments

**Only comment non-obvious test setup:**

```typescript
// ❌ WRONG - Obvious from describe block and test name
describe('Group Operations', () => {
  it('should list groups with pagination', async () => {
    // First get a list to find valid IDs
    const result = await groupApi.list(orgId, 1, 10);
    // ...
  });
});

// ✅ CORRECT - Comment explains special case
describe('Group Operations', () => {
  it('should handle groups with special characters in names', async () => {
    // Unicode group names require special URL encoding on this endpoint
    const result = await groupApi.get(orgId, '测试组');
    // ...
  });
});
```

## Summary

**Write Comments That:**
- ✅ Explain WHY, not WHAT
- ✅ Document non-obvious behavior
- ✅ Warn about API quirks
- ✅ Track technical debt (TODOs)

**Avoid Comments That:**
- ❌ Restate the code
- ❌ Describe obvious structure
- ❌ Repeat function names
- ❌ Explain self-documenting code
