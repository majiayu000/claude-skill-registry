---
name: reference-docs
description: Reference documentation patterns for API and symbol documentation. Use when writing reference docs, API docs, parameter tables, or technical specifications. Triggers on reference docs, API reference, function reference, parameters table, symbol documentation.
---

# Reference Documentation Patterns

Reference documentation is information-oriented - helping experienced users find precise technical details quickly. This skill provides patterns for writing clear, scannable reference pages.

**Dependency:** Always use this skill in conjunction with `docs-style` for core writing principles.

## Purpose and Audience

- **Who:** Experienced users seeking specific information
- **Goal:** Quick lookup of technical details
- **Mode:** Not for learning, for looking up
- **Expectation:** Brevity, consistency, completeness

## Document Structure Template

Use this template when creating reference documentation:

```markdown
---
title: "[Symbol/API Name]"
description: "One-line description of what it does"
---

# [Name]

Brief description (1-2 sentences). State what it is and its primary purpose.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `param1` | `string` | Yes | What this parameter controls |
| `param2` | `number` | No | Optional behavior modification. Default: `10` |

## Returns

| Type | Description |
|------|-------------|
| `ReturnType` | What the function returns and when |

## Example

```language
import { symbolName } from 'package';

// Complete, runnable example showing common use case
const result = symbolName({
  param1: 'realistic-value',
  param2: 42
});

console.log(result);
// Expected output: { ... }
```

## Related

- [RelatedSymbol](/reference/related-symbol) - Brief description
- [AnotherSymbol](/reference/another-symbol) - Brief description
```

## Writing Principles

### Brevity Over Explanation

- State facts, not rationale
- Avoid "why" - save that for Explanation docs
- Cut unnecessary words

**Do:**
```markdown
Returns the user's display name.
```

**Avoid:**
```markdown
This function is useful when you need to get the user's display name
because it handles all the edge cases for you automatically.
```

### Scannable Tables, Not Prose

**Do:**
```markdown
| Name | Type | Description |
|------|------|-------------|
| `userId` | `string` | Unique user identifier |
| `options` | `Options` | Configuration object |
```

**Avoid:**
```markdown
The first parameter is `userId`, which should be a string containing
the unique user identifier. The second parameter is `options`, which
is an Options object containing the configuration.
```

### Consistent Format Across Entries

All reference pages for similar items should follow identical structure:

- Same heading order
- Same table columns
- Same code example format
- Same related links section

### Every Example Must Be Runnable

- Include all imports
- Show complete, working code
- Use realistic values (not "foo", "bar", "test123")
- Include expected output when helpful

## Code Example Patterns

### Show Common Use Case First

```markdown
## Example

### Basic Usage

```typescript
const user = await getUser('user-123');
console.log(user.name);
```

### With Options

```typescript
const user = await getUser('user-123', {
  includeMetadata: true,
  fields: ['name', 'email', 'role']
});
```
```

### Include Setup and Context

```markdown
```typescript
import { Client } from '@example/sdk';

// Initialize client (required once per application)
const client = new Client({ apiKey: process.env.API_KEY });

// Now use the function
const result = await client.users.list();
```
```

### Use Realistic Values

**Do:** `userId: 'usr_a1b2c3d4'`
**Avoid:** `userId: 'foo'`

**Do:** `email: 'jane.smith@company.com'`
**Avoid:** `email: 'test@test.com'`

## Parameter Documentation Patterns

### Required vs Optional

Clearly indicate which parameters are required:

```markdown
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `apiKey` | `string` | Yes | - | Your API key |
| `timeout` | `number` | No | `30000` | Request timeout in ms |
| `retries` | `number` | No | `3` | Number of retry attempts |
```

### Complex Types

For object parameters, document the shape:

```markdown
## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `options` | `UserOptions` | No | Configuration options |

### UserOptions

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `includeDeleted` | `boolean` | No | Include soft-deleted users |
| `fields` | `string[]` | No | Fields to return |
| `limit` | `number` | No | Maximum results (default: 100) |
```

### Enum Values

Document allowed values clearly:

```markdown
| Name | Type | Values | Description |
|------|------|--------|-------------|
| `status` | `string` | `active`, `pending`, `suspended` | User account status |
```

## Return Value Documentation

### Simple Returns

```markdown
## Returns

`User` - The requested user object, or `null` if not found.
```

### Complex Returns

```markdown
## Returns

| Property | Type | Description |
|----------|------|-------------|
| `data` | `User[]` | Array of user objects |
| `pagination` | `Pagination` | Pagination metadata |
| `total` | `number` | Total matching records |
```

### Error Conditions

```markdown
## Errors

| Error | Condition |
|-------|-----------|
| `NotFoundError` | User does not exist |
| `UnauthorizedError` | Invalid or expired API key |
| `RateLimitError` | Too many requests |
```

## API Reference Specifics

### HTTP Endpoints

```markdown
## Endpoint

```http
GET /api/v1/users/{userId}
```

## Path Parameters

| Name | Type | Description |
|------|------|-------------|
| `userId` | `string` | The user's unique identifier |

## Query Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fields` | `string` | No | Comma-separated list of fields |

## Headers

| Name | Required | Description |
|------|----------|-------------|
| `Authorization` | Yes | Bearer token |
| `X-Request-ID` | No | Request tracking ID |

## Response

```json
{
  "id": "usr_a1b2c3d4",
  "name": "Jane Smith",
  "email": "jane@company.com"
}
```
```

## Component/Props Reference

For UI components:

```markdown
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `'primary' \| 'secondary'` | `'primary'` | Visual style |
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | Button size |
| `disabled` | `boolean` | `false` | Disable interactions |
| `onClick` | `() => void` | - | Click handler |

## Slots

| Name | Description |
|------|-------------|
| `default` | Button content |
| `icon` | Icon to display before text |
```

## Related Links Section

Always include links to related content:

```markdown
## Related

- [createUser](/reference/create-user) - Create a new user
- [updateUser](/reference/update-user) - Modify user properties
- [deleteUser](/reference/delete-user) - Remove a user
- [User Authentication Guide](/guides/authentication) - How authentication works
```

## Checklist for Reference Pages

Before considering a reference page complete:

- [ ] Title matches the symbol/API name exactly
- [ ] Description is one clear sentence
- [ ] All parameters documented with types
- [ ] Required vs optional clearly marked
- [ ] Default values specified for optional parameters
- [ ] Return type and structure documented
- [ ] At least one complete, runnable example
- [ ] Example uses realistic values
- [ ] Related pages linked
- [ ] Format matches other reference pages in the docs
