---
name: generating-typescript-types-from-apis
description: Generates TypeScript interfaces from API responses or OpenAPI schemas. Use when the user asks about typing API responses, creating interfaces from JSON, parsing Swagger/OpenAPI, or keeping types in sync with backend.
---

# API Response → TypeScript Types

## When to use this skill

- User asks to type an API response
- User has JSON and needs TypeScript interfaces
- User mentions OpenAPI or Swagger schemas
- User wants to generate types from endpoints
- User asks about keeping frontend/backend types in sync

## Workflow

- [ ] Identify API source (JSON response, OpenAPI, endpoint)
- [ ] Parse response structure
- [ ] Generate TypeScript interfaces
- [ ] Handle nested objects and arrays
- [ ] Add JSDoc comments
- [ ] Export types to appropriate location

## Instructions

### Step 1: Identify Source Type

| Source          | Approach              |
| --------------- | --------------------- |
| JSON response   | Parse and infer types |
| OpenAPI/Swagger | Use generator tool    |
| GraphQL         | Use codegen           |
| Live endpoint   | Fetch and parse       |

### Step 2: Parse JSON Response

**Sample API response:**

```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "isActive": true,
  "roles": ["admin", "user"],
  "profile": {
    "avatar": "https://example.com/avatar.jpg",
    "bio": null,
    "socialLinks": [
      { "platform": "twitter", "url": "https://twitter.com/john" }
    ]
  },
  "createdAt": "2026-01-18T10:00:00Z",
  "metadata": {}
}
```

**Generated TypeScript:**

```typescript
// types/api/user.ts

export interface User {
  /** Unique identifier */
  id: number;
  /** User's full name */
  name: string;
  /** Email address */
  email: string;
  /** Whether the user account is active */
  isActive: boolean;
  /** Assigned roles */
  roles: string[];
  /** User profile information */
  profile: UserProfile;
  /** Account creation timestamp (ISO 8601) */
  createdAt: string;
  /** Additional metadata */
  metadata: Record<string, unknown>;
}

export interface UserProfile {
  /** Avatar image URL */
  avatar: string;
  /** User biography */
  bio: string | null;
  /** Social media links */
  socialLinks: SocialLink[];
}

export interface SocialLink {
  /** Platform name */
  platform: string;
  /** Profile URL */
  url: string;
}
```

### Step 3: Type Inference Rules

| JSON Value      | TypeScript Type             |
| --------------- | --------------------------- |
| `123`           | `number`                    |
| `"text"`        | `string`                    |
| `true`/`false`  | `boolean`                   |
| `null`          | `null` (or `T \| null`)     |
| `[]`            | `T[]` (infer from items)    |
| `{}` empty      | `Record<string, unknown>`   |
| `{}` with keys  | Named interface             |
| ISO date string | `string` (add comment)      |
| UUID string     | `string` (add branded type) |

**Branded types for special strings:**

```typescript
// types/branded.ts
export type UUID = string & { readonly __brand: "UUID" };
export type ISODateString = string & { readonly __brand: "ISODateString" };
export type Email = string & { readonly __brand: "Email" };

// Usage
export interface User {
  id: UUID;
  email: Email;
  createdAt: ISODateString;
}
```

### Step 4: Handle Arrays

**Homogeneous array:**

```typescript
// JSON: [1, 2, 3]
items: number[];

// JSON: ["a", "b"]
tags: string[];
```

**Array of objects:**

```typescript
// JSON: [{ "id": 1, "name": "Item" }]
items: Item[];

interface Item {
  id: number;
  name: string;
}
```

**Mixed array (avoid if possible):**

```typescript
// JSON: [1, "two", true]
values: (number | string | boolean)[];
```

**Tuple (fixed length, known types):**

```typescript
// JSON: [37.7749, -122.4194] (lat/lng)
coordinates: [number, number];
```

### Step 5: Handle Optional Fields

**Detect optional fields from multiple samples:**

```typescript
// Sample 1: { "name": "John", "nickname": "Johnny" }
// Sample 2: { "name": "Jane" }

export interface User {
  name: string;
  nickname?: string; // Optional - not present in all responses
}
```

**Nullable vs optional:**

```typescript
export interface User {
  bio: string | null; // Present but can be null
  nickname?: string; // May not be present
  avatar?: string | null; // May not be present, or null
}
```

### Step 6: API Response Wrappers

**Paginated response:**

```typescript
export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    perPage: number;
    total: number;
    totalPages: number;
  };
}

// Usage
type UsersResponse = PaginatedResponse<User>;
```

**API envelope:**

```typescript
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: ApiError;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, string[]>;
}

// Usage
type UserResponse = ApiResponse<User>;
type UsersResponse = ApiResponse<User[]>;
```

### Step 7: OpenAPI/Swagger Generation

**Using openapi-typescript:**

```bash
npm install -D openapi-typescript
```

```bash
# From URL
npx openapi-typescript https://api.example.com/openapi.json -o types/api.ts

# From local file
npx openapi-typescript ./openapi.yaml -o types/api.ts

# Watch mode
npx openapi-typescript ./openapi.yaml -o types/api.ts --watch
```

**Generated usage:**

```typescript
import type { paths, components } from "./types/api";

// Extract response type
type User = components["schemas"]["User"];

// Extract endpoint types
type GetUsersResponse =
  paths["/users"]["get"]["responses"]["200"]["content"]["application/json"];
type CreateUserBody =
  paths["/users"]["post"]["requestBody"]["content"]["application/json"];
```

**With openapi-fetch for type-safe requests:**

```bash
npm install openapi-fetch
```

```typescript
import createClient from "openapi-fetch";
import type { paths } from "./types/api";

const client = createClient<paths>({ baseUrl: "https://api.example.com" });

// Fully typed request/response
const { data, error } = await client.GET("/users/{id}", {
  params: { path: { id: "123" } },
});
// data is typed as User
```

### Step 8: Fetch and Generate Script

```typescript
// scripts/generate-types.ts
import { writeFileSync } from "fs";

interface TypeDefinition {
  name: string;
  properties: PropertyDefinition[];
}

interface PropertyDefinition {
  name: string;
  type: string;
  optional: boolean;
  nullable: boolean;
  comment?: string;
}

function inferType(value: unknown, key: string): string {
  if (value === null) return "null";
  if (Array.isArray(value)) {
    if (value.length === 0) return "unknown[]";
    const itemType = inferType(value[0], `${key}Item`);
    return `${itemType}[]`;
  }
  if (typeof value === "object") {
    return toPascalCase(key);
  }
  return typeof value;
}

function toPascalCase(str: string): string {
  return str.replace(/(^|_)(\w)/g, (_, __, c) => c.toUpperCase());
}

function generateInterface(
  name: string,
  obj: Record<string, unknown>,
): string[] {
  const lines: string[] = [];
  const nested: string[] = [];

  lines.push(`export interface ${name} {`);

  for (const [key, value] of Object.entries(obj)) {
    const type = inferType(value, key);
    const nullable = value === null ? " | null" : "";

    if (typeof value === "object" && value !== null && !Array.isArray(value)) {
      nested.push(
        ...generateInterface(
          toPascalCase(key),
          value as Record<string, unknown>,
        ),
      );
    }

    lines.push(`  ${key}: ${type}${nullable};`);
  }

  lines.push("}");
  lines.push("");

  return [...nested, ...lines];
}

async function main() {
  const response = await fetch("https://api.example.com/users/1");
  const data = await response.json();

  const types = generateInterface("User", data);
  const output = types.join("\n");

  writeFileSync("types/user.ts", output);
  console.log("Generated types/user.ts");
}

main();
```

### Step 9: Keep Types in Sync

**CI check for OpenAPI changes:**

```yaml
# .github/workflows/types.yml
name: Generate API Types

on:
  schedule:
    - cron: "0 0 * * *" # Daily
  workflow_dispatch:

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Generate types
        run: npx openapi-typescript ${{ vars.API_SPEC_URL }} -o types/api.ts

      - name: Check for changes
        id: changes
        run: |
          if git diff --quiet types/api.ts; then
            echo "changed=false" >> $GITHUB_OUTPUT
          else
            echo "changed=true" >> $GITHUB_OUTPUT
          fi

      - name: Create PR
        if: steps.changes.outputs.changed == 'true'
        uses: peter-evans/create-pull-request@v5
        with:
          title: "chore: update API types"
          branch: update-api-types
```

**Pre-commit hook:**

```bash
# .husky/pre-commit
npx openapi-typescript ./openapi.yaml -o types/api.ts
git add types/api.ts
```

## Output Location

```
types/
├── api/
│   ├── user.ts       # User-related types
│   ├── product.ts    # Product types
│   └── index.ts      # Re-exports
├── api.ts            # OpenAPI generated (single file)
└── branded.ts        # Branded types (UUID, Email, etc.)
```

**Index file:**

```typescript
// types/api/index.ts
export * from "./user";
export * from "./product";
export type { ApiResponse, ApiError, PaginatedResponse } from "./common";
```

## Validation

Before completing:

- [ ] All interfaces have JSDoc comments
- [ ] Nested objects have named interfaces
- [ ] Optional fields marked with `?`
- [ ] Nullable fields use `| null`
- [ ] Arrays are properly typed
- [ ] No `any` types in output
- [ ] Types compile without errors

```bash
# Validate generated types
npx tsc --noEmit types/**/*.ts
```

## Error Handling

- **Empty object `{}`**: Use `Record<string, unknown>` not `object`.
- **Mixed arrays**: Union type or `unknown[]`; flag for manual review.
- **Circular references**: OpenAPI generators handle this; manual parsing needs tracking.
- **Conflicting samples**: Mark field as optional with union of observed types.
- **Unknown date format**: Default to `string` with JSDoc explaining format.

## Resources

- [openapi-typescript](https://openapi-ts.pages.dev/)
- [openapi-fetch](https://openapi-ts.pages.dev/openapi-fetch/)
- [TypeScript Handbook: Object Types](https://www.typescriptlang.org/docs/handbook/2/objects.html)
- [json-to-ts VSCode Extension](https://marketplace.visualstudio.com/items?itemName=MariusAlchiworker.json-to-ts)
