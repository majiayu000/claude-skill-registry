---
description: Testing patterns for Ballee using Vitest E2E tests with dual-client architecture, RLS validation, and authentication patterns. Use when writing tests, validating RLS policies, or debugging test failures.
---

# Test Patterns

## Dual-Client Architecture

```typescript
import { createAdminClient, createAuthenticatedClient } from '@/tests/utils/supabase';

describe('Feature Tests', () => {
  let adminClient: SupabaseClient;  // Bypasses RLS - for seeding
  let userClient: SupabaseClient;   // Respects RLS - for testing

  beforeAll(async () => {
    adminClient = createAdminClient();
    userClient = await createAuthenticatedClient('test@example.com');
  });
});
```

## When to Use Each Client

| Client | Use For |
|--------|---------|
| `adminClient` | Seeding data, cleanup, verifying DB state |
| `userClient` | Testing user-facing operations, RLS validation |

## RLS Validation Pattern

```typescript
it('should allow access to own client data', async () => {
  // Seed with admin
  const { data: item } = await adminClient
    .from('items')
    .insert({ client_id: userClientId, name: 'Test' })
    .select()
    .single();

  // Verify user can access
  const { data, error } = await userClient
    .from('items')
    .select()
    .eq('id', item.id)
    .single();

  expect(error).toBeNull();
  expect(data.id).toBe(item.id);
});

it('should deny access to other client data', async () => {
  // Seed with different client
  const { data: otherItem } = await adminClient
    .from('items')
    .insert({ client_id: otherClientId, name: 'Other' })
    .select()
    .single();

  // Verify user CANNOT access
  const { data, error } = await userClient
    .from('items')
    .select()
    .eq('id', otherItem.id)
    .single();

  expect(data).toBeNull();
});
```

## Super Admin Bypass Test

```typescript
it('super admin should access all data', async () => {
  const superAdminClient = await createAuthenticatedClient('admin@ballee.io');

  const { data, error } = await superAdminClient
    .from('items')
    .select()
    .eq('id', otherClientItem.id)
    .single();

  expect(error).toBeNull();
  expect(data).not.toBeNull();
});
```

## Test File Structure

```
apps/web/__tests__/
├── e2e/
│   ├── events.test.ts        # E2E feature tests
│   └── auth.test.ts
├── unit/
│   ├── services/             # Service unit tests
│   └── utils/
└── utils/
    └── supabase.ts           # Test client utilities
```

## Common Test Patterns

### Service Test
```typescript
describe('EventService', () => {
  it('should create event and return Result.success', async () => {
    const service = new EventService(userClient);
    const result = await service.create({ name: 'Test Event' });

    expect(result.success).toBe(true);
    expect(result.data.name).toBe('Test Event');
  });

  it('should return Result.error on failure', async () => {
    const service = new EventService(userClient);
    const result = await service.create({ name: '' }); // Invalid

    expect(result.success).toBe(false);
    expect(result.error).toBeDefined();
  });
});
```

### Server Action Test
```typescript
it('should require authentication', async () => {
  // Call without auth context
  const result = await createEventAction(formData);
  expect(result.error).toContain('Unauthorized');
});
```

## Test Commands

```bash
pnpm test              # Run all tests
pnpm test:e2e          # Run E2E tests only
pnpm test:unit         # Run unit tests only
pnpm test --coverage   # With coverage report
```

## Common Pitfalls

| Issue | Fix |
|-------|-----|
| RLS blocking test data | Use adminClient for seeding |
| Test pollution | Clean up in afterEach/afterAll |
| Flaky auth tests | Use fresh authenticated client per test |
| Missing test data | Seed required dependencies first |

## Cleanup Pattern

```typescript
afterAll(async () => {
  // Clean up test data (use admin to bypass RLS)
  await adminClient.from('items').delete().eq('name', 'Test%');
});
```
