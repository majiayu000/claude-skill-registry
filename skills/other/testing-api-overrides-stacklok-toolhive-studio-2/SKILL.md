---
name: testing-api-overrides
description: Test that components send correct query parameters or request arguments. Use when testing filtering, sorting, pagination, or any read operation where request parameters matter. Use for test-scoped mock customization.
---

# Testing API Overrides

Test that your code sends correct API parameters by using conditional overrides that respond differently based on the request. This approach tests actual user-facing behavior rather than inspecting internal request details.

## Philosophy

**Good tests verify what users see, not implementation details.**

Instead of:

1. ❌ Recording the request and checking query params
2. ❌ Asserting on internal function calls

Do this:

1. ✅ Set up conditional mocks that respond based on params
2. ✅ Verify the component renders the expected data

If the code sends wrong parameters, the mock returns wrong data, the UI shows wrong content, and the test fails. This catches real bugs.

## When to Use Conditional Overrides

- Testing list filtering (e.g., filter by group, status, search term)
- Testing pagination parameters
- Testing sort order
- Any read operation where request parameters affect what data is returned

**Note:** For mutations (create/update/delete), use `recordRequests()` instead. See the **testing-api-assertions** skill.

## conditionalOverride()

Returns different data based on request properties:

```typescript
import { mockedGetApiV1BetaWorkloads } from '@mocks/fixtures/workloads/get'

mockedGetApiV1BetaWorkloads.conditionalOverride(
  // Predicate: when should this override apply?
  ({ query }) => query.group === 'archive',
  // Transform: what data to return?
  (data) => ({
    ...data,
    workloads: [], // Archive group is empty
  })
)
```

### Predicate Function

The predicate receives parsed request info with easy access to query params, path params, body, and headers:

```typescript
;({ query, path, body, headers }) => {
  // Query parameters (pre-parsed)
  query.group // '?group=archive' -> 'archive'
  query.status // '?status=running' -> 'running'

  // Path parameters (from route like /workloads/:name)
  path.name // for /workloads/:name

  // Request body (for POST/PUT/DELETE)
  body?.name // parsed JSON body

  // Headers
  headers.get('Authorization')

  return true // or false
}
```

### Transform Function

The transform receives default data and returns modified data:

```typescript
;(data) => ({
  ...data, // Spread defaults
  workloads: data.workloads?.filter(
    // Modify as needed
    (w) => w.status === 'running'
  ),
})
```

## Example: Testing Group Filter

```typescript
import { mockedGetApiV1BetaWorkloads } from '@mocks/fixtures/workloads/get'

it('shows only workloads from the selected group', async () => {
  // Default mock returns workloads from multiple groups
  // Add conditional override for 'production' group
  mockedGetApiV1BetaWorkloads.conditionalOverride(
    ({ query }) => query.group === 'production',
    (data) => ({
      ...data,
      workloads: [
        { name: 'prod-server-1', group: 'production', status: 'running' },
        { name: 'prod-server-2', group: 'production', status: 'running' },
      ],
    })
  )

  render(<WorkloadsList group="production" />)

  // If component sends ?group=production, it gets the filtered data
  // If component forgets the param, it gets default data with mixed groups
  await waitFor(() => {
    expect(screen.getByText('prod-server-1')).toBeVisible()
    expect(screen.getByText('prod-server-2')).toBeVisible()
  })

  // These would appear if the filter param wasn't sent correctly
  expect(screen.queryByText('dev-server')).not.toBeInTheDocument()
})
```

## Example: Testing Empty State

```typescript
it('shows empty message when group has no workloads', async () => {
  mockedGetApiV1BetaWorkloads.conditionalOverride(
    ({ query }) => query.group === 'empty-group',
    () => ({ workloads: [] })
  )

  render(<WorkloadsList group="empty-group" />)

  await waitFor(() => {
    expect(screen.getByText(/no workloads found/i)).toBeVisible()
  })
})
```

## Multiple Conditional Overrides

Chain multiple overrides for different conditions:

```typescript
mockedGetApiV1BetaWorkloads
  .conditionalOverride(
    ({ query }) => query.group === 'production',
    () => ({ workloads: productionWorkloads })
  )
  .conditionalOverride(
    ({ query }) => query.group === 'staging',
    () => ({ workloads: stagingWorkloads })
  )
```

Later overrides wrap earlier ones. If no predicate matches, the default fixture data is returned.

## Simple Overrides (No Condition)

For test-scoped data changes without conditions, use `.override()`:

```typescript
// Override for entire test - no condition
mockedGetApiV1BetaGroups.override(() => ({
  groups: [{ name: 'only-group', registered_clients: [] }],
}))

// Modify default data
mockedGetApiV1BetaGroups.override((data) => ({
  ...data,
  groups: data.groups?.slice(0, 1),
}))
```

## Error Responses

Use `.overrideHandler()` for full control over the response:

```typescript
import { HttpResponse } from 'msw'

// Return error
mockedGetApiV1BetaGroups.overrideHandler(() =>
  HttpResponse.json({ error: 'Server error' }, { status: 500 })
)

// Network failure
mockedGetApiV1BetaGroups.overrideHandler(() => HttpResponse.error())
```

## Automatic Reset

All overrides are automatically reset before each test via `resetAllAutoAPIMocks()` in `vitest.setup.ts`. No cleanup needed.

## Reusable Scenarios

When the same response override is needed across many tests, define it as a scenario in the fixture instead of duplicating `.override()` calls.

### Defining Scenarios (in fixtures)

```typescript
// In fixtures/workloads/get.ts
export const mockedGetApiV1BetaWorkloads = AutoAPIMock<...>({
  workloads: [/* default data */],
}).scenario('empty', (mock) => mock.override(() => ({ workloads: [] })))
```

### Using Scenarios (in tests)

```typescript
mockedGetApiV1BetaWorkloads.activateScenario('empty')
```

Scenario names are defined in `renderer/src/common/mocks/scenarioNames.ts`. Use existing names when possible to keep scenarios consolidated.

## Related Skills

- **testing-with-api-mocks** - Auto-generated mocks and fixture basics
- **testing-api-assertions** - Verifying mutations with `recordRequests()` (create/update/delete only)
