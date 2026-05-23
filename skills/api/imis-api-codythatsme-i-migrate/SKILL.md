---
name: imis-api
description: iMIS API integration patterns and workflows. Use when implementing iMIS API features, adding new endpoints, creating schemas, or debugging API issues. Triggers on: iMIS, ImisApiService, iMIS API, API endpoint, iMIS schema.
user-invocable: false
allowed-tools: Read, Grep, Glob, Bash
---

# iMIS API Development Guide

## Reference Code

**Do NOT rely on web searches for iMIS API information.** Instead, use the reference implementation:

```
~/.local/share/imis/index.ts
```

This file contains working API call patterns for many iMIS endpoints. Search it for the endpoint you need:

```bash
grep -n "api.party\|api.query\|api.document" ~/.local/share/imis/index.ts
```

**Important**: The reference code shows correct request shapes and URL patterns, but may need refactoring to use Effect patterns. Don't copy verbatim—adapt to this project's Effect-based architecture.

## API Discovery Workflow

When implementing a new iMIS API endpoint:

### Step 1: Find the Pattern

Search the reference code for similar functionality:

```bash
grep -A 20 "relevant-endpoint-name" ~/.local/share/imis/index.ts
```

### Step 2: Create Exploration Script

Create a script to hit the real API and inspect the response. This is critical because iMIS response schemas are complex and often inconsistent.

**Template** (`test/scripts/explore-{endpoint}.ts`):

```typescript
import { Effect } from "effect"

// Get credentials from environment
const baseUrl = process.env.IMIS_BASE_URL!
const username = process.env.IMIS_USERNAME!
const password = process.env.IMIS_PASSWORD!

// Get token
const tokenResponse = await fetch(`${baseUrl}/token`, {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: `grant_type=password&username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
})
const { access_token } = await tokenResponse.json()

// Make API request
const response = await fetch(`${baseUrl}/api/{endpoint}`, {
  headers: {
    Authorization: `Bearer ${access_token}`,
    Accept: "application/json",
  },
})
const data = await response.json()

// Pretty print for schema analysis
console.log(JSON.stringify(data, null, 2))
```

Run with:
```bash
bun test/scripts/explore-{endpoint}.ts
```

### Step 3: Analyze Response Shape

Look for:
- `$type` fields indicating .NET SOA contract types
- `$values` arrays (iMIS collection pattern)
- `{ $type: "System.XXX", $value: ... }` wrapped primitives
- Nested `Properties` arrays with `GenericPropertyData`

### Step 4: Implement

1. **Add schema** to `src/api/imis-schemas.ts`
2. **Add method** to `ImisApiService` in `src/services/imis-api.ts`
3. **Add RPC handler** if needed in `src/api/handlers.ts`

## Implementation Patterns

### Adding a Schema

Follow existing patterns in `src/api/imis-schemas.ts`:

```typescript
// For simple response types
export const MyResponseSchema = Schema.Struct({
  $type: Schema.String,
  SomeField: Schema.String,
  Items: Schema.Struct({
    $type: Schema.String,
    $values: Schema.Array(MyItemSchema),
  }),
})

// For wrapped values (common in iMIS)
export const WrappedValue = Schema.Struct({
  $type: Schema.String,
  $value: Schema.Unknown,
})
```

### Adding an ImisApiService Method

Use the `executeWithAuth` pattern:

```typescript
myMethod: (envId: string, param: string) =>
  executeWithAuth(envId, `/api/MyEndpoint`, (token, env) =>
    HttpClientRequest.get(`${env.baseUrl}/api/MyEndpoint`)
      .pipe(
        HttpClientRequest.setUrlParam("param", param),
        HttpClientRequest.bearerToken(token),
        HttpClientRequest.setHeader("Accept", "application/json"),
        httpClient.execute,
        Effect.flatMap(HttpClientResponse.schemaBodyJson(MyResponseSchema)),
        Effect.scoped,
        Effect.withSpan("imis.myMethod", {
          attributes: { environmentId: envId, param },
        })
      )
  ),
```

For POST requests with `_execute` pattern:

```typescript
myExecuteMethod: (envId: string, operation: string, params: Record<string, unknown>) =>
  executeWithAuth(envId, `/api/MyEndpoint/_execute`, (token, env) =>
    HttpClientRequest.post(`${env.baseUrl}/api/MyEndpoint/_execute`)
      .pipe(
        HttpClientRequest.bearerToken(token),
        HttpClientRequest.setHeader("Content-Type", "application/json"),
        HttpClientRequest.jsonBody({
          $type: "Asi.Soa.Core.DataContracts.GenericExecuteRequest, Asi.Contracts",
          OperationName: operation,
          EntityTypeName: "MyEndpoint",
          Parameters: {
            $type: "System.Collections.Generic.Dictionary`2[[System.String],[System.Object]], mscorlib",
            ...params,
          },
        }),
        httpClient.execute,
        Effect.flatMap(HttpClientResponse.schemaBodyJson(MyExecuteResponseSchema)),
        Effect.scoped,
        Effect.withSpan("imis.myExecuteMethod", { attributes: { environmentId: envId, operation } })
      )
  ),
```

## Key Files

| File | Purpose |
|------|---------|
| `src/services/imis-api.ts` | ImisApiService - all API methods |
| `src/api/imis-schemas.ts` | Request/response schemas |
| `src/api/handlers.ts` | RPC handlers using the API |
| `src/api/procedures.ts` | RPC procedure definitions |
| `test/imis-api/setup.ts` | Test environment setup patterns |
| `~/.local/share/imis/index.ts` | Reference API patterns |

## Common iMIS Patterns

### Pagination
- Max 500 records per request
- Use `limit` and `offset` query params
- Response includes: `Count`, `TotalCount`, `HasNext`, `NextOffset`

### Version Differences (EMS vs 2017)
- EMS uses `/api/query`, 2017 uses `/api/iqa`
- 2017 responses need normalization (see `normalize2017Response`)
- Check `env.version` to determine which endpoint

### GenericPropertyData
Convert to/from flat objects:
```typescript
// To properties array (for requests)
const properties = Object.entries(data).map(([Name, Value]) => ({ Name, Value }))

// From properties array (for responses)
const flat = Object.fromEntries(props.map((p) => [p.Name, unwrapValue(p.Value)]))
```

### Error Types
- `ImisAuthError` - Authentication failed
- `ImisRequestError` - Network/connection error
- `ImisResponseError` - HTTP error (includes status code)
- `ImisSchemaError` - Response parsing failed

## Testing

Integration tests use the pattern from `test/imis-api/`:

```typescript
describe.skipIf(!shouldRunIntegrationTests())("My Feature", () => {
  let envId: string

  beforeAll(async () => {
    envId = await createTestEnvironment()
  })

  afterAll(async () => {
    await cleanupTestEnvironment(envId)
  })

  it("should do something", async () => {
    const result = await runExpectSuccess(ImisApiService.myMethod(envId, "param"))
    expect(result).toBeDefined()
  })
})
```

Run integration tests:
```bash
bun test test/imis-api --timeout 30000
```
