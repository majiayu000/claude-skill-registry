---
name: server-actions
description: |
  Next.js Server Actions for mutations in this application.
  Covers entity actions, user actions, team actions, and best practices.
  Use this skill when implementing mutations from Client Components.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# Server Actions Skill

Patterns for using Next.js Server Actions to perform mutations from Client Components.

## Architecture Overview

```
core/lib/actions/
├── index.ts              # Re-exports all actions
├── types.ts              # Shared types (EntityActionResult, etc.)
├── entity.actions.ts     # Generic CRUD for any registered entity
├── user.actions.ts       # User profile management
└── team.actions.ts       # Team and member management
```

## When to Use This Skill

- Calling mutations from Client Components (`'use client'`)
- Form submissions without JavaScript
- Automatic cache revalidation after mutations
- Type-safe end-to-end mutations

## Import Pattern

```typescript
// From Client Components
'use client'

import {
  // Entity actions
  createEntity,
  updateEntity,
  deleteEntity,
  getEntity,
  listEntities,
  deleteEntities,
  entityExists,
  countEntities,
  // User actions
  updateProfile,
  updateAvatar,
  deleteAccount,
  // Team actions
  updateTeam,
  inviteMember,
  removeMember,
  updateMemberRole,
} from '@nextsparkjs/core/actions'
```

## Security Model

**All actions follow the same security pattern:**

1. Auth is obtained from session/cookies (NEVER from client parameters)
2. `userId` comes from `getTypedSession()`
3. `teamId` comes from `httpOnly` cookie `activeTeamId`
4. Permissions are checked via `checkPermission()`

**Never pass userId/teamId as parameters:**
```typescript
// WRONG - Never trust client data for auth
export async function updateProfile(userId: string, data: ProfileData) { ... }

// CORRECT - Get auth from server context
export async function updateProfile(data: ProfileData) {
  const session = await getTypedSession(await headers())
  if (!session?.user?.id) {
    return { success: false, error: 'Authentication required' }
  }
  const userId = session.user.id
  // ...
}
```

## Entity Actions

### createEntity

Create a new entity record.

```typescript
const result = await createEntity('products', {
  name: 'New Product',
  price: 99.99,
  status: 'draft',
})

if (result.success) {
  console.log('Created:', result.data)
} else {
  console.error('Error:', result.error)
}
```

### updateEntity

Update an existing entity.

```typescript
const result = await updateEntity('products', productId, {
  status: 'published',
})

// With custom revalidation
await updateEntity('products', productId, data, {
  revalidatePaths: ['/dashboard/overview'],
  revalidateTags: ['product-stats'],
})
```

### deleteEntity

Delete an entity by ID.

```typescript
const result = await deleteEntity('products', productId)

// With redirect after delete
await deleteEntity('products', productId, {
  redirectTo: '/dashboard/products',
})
```

### deleteEntities (Batch)

Delete multiple entities at once.

```typescript
const result = await deleteEntities('products', ['id1', 'id2', 'id3'])

if (result.success) {
  console.log(`Deleted ${result.data.deletedCount} products`)
}
```

### getEntity / listEntities

For reads from Client Components (prefer Server Components when possible).

```typescript
// Get single entity
const result = await getEntity('products', productId)

// List with pagination and filters
const result = await listEntities('products', {
  limit: 20,
  offset: 0,
  where: { status: 'active' },
  orderBy: 'createdAt',
  orderDir: 'desc',
})
```

### entityExists / countEntities

```typescript
// Check if entity exists
const result = await entityExists('products', productId)

// Count with filter
const result = await countEntities('products', { status: 'active' })
```

## User Actions

### updateProfile

Update the current user's profile.

```typescript
const result = await updateProfile({
  firstName: 'John',
  lastName: 'Doe',
  timezone: 'America/New_York',
  language: 'en',
})

// Allowed fields: firstName, lastName, name, country, timezone, language
```

### updateAvatar

Update the user's avatar (URL, not file upload).

```typescript
// After uploading file to storage and getting URL
const formData = new FormData()
formData.append('avatar', 'https://example.com/uploaded-avatar.jpg')

const result = await updateAvatar(formData)
```

### deleteAccount

Delete the current user's account.

```typescript
// Check conditions first!
const result = await deleteAccount()

// Will fail if user owns teams
// Error: "Cannot delete account while owning teams. Transfer ownership first."
```

## Team Actions

### updateTeam

Update team information (requires owner or admin role).

```typescript
const result = await updateTeam(teamId, {
  name: 'New Team Name',
  description: 'Updated description',
  slug: 'new-slug',
})

// Will check slug availability if changing
```

### inviteMember

Add a user to the team (requires owner or admin role).

```typescript
const result = await inviteMember(
  teamId,
  'user@example.com',  // User must already exist
  'member'             // 'member' | 'admin' | 'viewer'
)

if (result.success) {
  console.log('Invited:', result.data.memberId)
}
```

### removeMember

Remove a member from the team.

```typescript
const result = await removeMember(teamId, userId)

// Cannot remove:
// - Team owner (must transfer ownership first)
// - Other admins (if requestor is admin, not owner)
```

### updateMemberRole

Change a member's role.

```typescript
const result = await updateMemberRole(teamId, userId, 'admin')

// Restrictions:
// - Cannot set role to 'owner' (use transferOwnership)
// - Only owner can promote to admin
// - Only owner can demote admins
```

## Result Types

All actions return a discriminated union:

```typescript
type EntityActionResult<T> =
  | { success: true; data: T }
  | { success: false; error: string }

type EntityActionVoidResult =
  | { success: true }
  | { success: false; error: string }
```

Usage with type guards:

```typescript
const result = await createEntity('products', data)

if (result.success) {
  // TypeScript knows result.data exists
  console.log(result.data.id)
} else {
  // TypeScript knows result.error exists
  toast.error(result.error)
}
```

## Revalidation Patterns

### Default Revalidation

Entity actions automatically revalidate:
- Create: `/dashboard/{entitySlug}`
- Update: `/dashboard/{entitySlug}` and `/dashboard/{entitySlug}/{id}`
- Delete: `/dashboard/{entitySlug}`

### Custom Revalidation

```typescript
await createEntity('products', data, {
  revalidatePaths: ['/dashboard/overview', '/public/catalog'],
  revalidateTags: ['product-count', 'catalog'],
})
```

### Redirect After Mutation

```typescript
await deleteEntity('products', id, {
  redirectTo: '/dashboard/products',
})
// Note: redirect() throws NEXT_REDIRECT - action won't return data
```

## Form Integration

### With React Hook Form

```typescript
'use client'

function ProductForm() {
  const form = useForm()

  async function onSubmit(data) {
    const result = await createEntity('products', data)
    if (result.success) {
      router.push(`/products/${result.data.id}`)
    } else {
      form.setError('root', { message: result.error })
    }
  }

  return <form onSubmit={form.handleSubmit(onSubmit)}>...</form>
}
```

### With Native Forms

```typescript
'use client'

function ProfileForm() {
  async function handleAction(formData: FormData) {
    const result = await updateProfile({
      firstName: formData.get('firstName') as string,
      lastName: formData.get('lastName') as string,
    })
    // Handle result
  }

  return (
    <form action={handleAction}>
      <input name="firstName" />
      <input name="lastName" />
      <button type="submit">Save</button>
    </form>
  )
}
```

## Creating New Server Actions

### Template

```typescript
// core/lib/actions/[domain].actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { headers } from 'next/headers'
import { getTypedSession } from '../auth'
import type { EntityActionResult, EntityActionVoidResult } from './types'

export async function myAction(data: MyInput): Promise<EntityActionResult<MyOutput>> {
  try {
    // 1. Get auth context
    const headersList = await headers()
    const session = await getTypedSession(headersList)
    if (!session?.user?.id) {
      return { success: false, error: 'Authentication required' }
    }
    const userId = session.user.id

    // 2. Validate input
    if (!data.requiredField) {
      return { success: false, error: 'Required field is missing' }
    }

    // 3. Check permissions (if needed)
    // const hasPermission = await checkPermission(userId, teamId, 'resource.action')

    // 4. Execute business logic via Service
    const result = await MyService.doSomething(userId, data)

    // 5. Revalidate caches
    revalidatePath('/dashboard/relevant-path')

    return { success: true, data: result }
  } catch (error) {
    console.error('[myAction] Error:', error)
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    }
  }
}
```

### Checklist for New Actions

- [ ] File marked with `'use server'` at top
- [ ] Auth obtained from session (not parameters)
- [ ] Input validation before service calls
- [ ] Permission checks where needed
- [ ] Business logic delegated to Services
- [ ] `revalidatePath` called for affected routes
- [ ] Error handling with try/catch
- [ ] Proper return type (`EntityActionResult` or `EntityActionVoidResult`)
- [ ] Export from `index.ts`

## Testing Server Actions

```typescript
// tests/jest/lib/actions/my.actions.test.ts

import { myAction } from '@/core/lib/actions/my.actions'

// Mock dependencies
jest.mock('@/core/lib/auth', () => ({
  getTypedSession: jest.fn(),
}))

jest.mock('next/cache', () => ({
  revalidatePath: jest.fn(),
}))

jest.mock('next/headers', () => ({
  headers: jest.fn().mockReturnValue(new Headers()),
}))

describe('myAction', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    // Setup authenticated user
    const { getTypedSession } = require('@/core/lib/auth')
    getTypedSession.mockResolvedValue({
      user: { id: 'user-123' },
    })
  })

  it('succeeds with valid data', async () => {
    const result = await myAction({ name: 'Test' })
    expect(result.success).toBe(true)
  })

  it('fails when not authenticated', async () => {
    const { getTypedSession } = require('@/core/lib/auth')
    getTypedSession.mockResolvedValue(null)

    const result = await myAction({ name: 'Test' })
    expect(result.success).toBe(false)
    expect(result.error).toBe('Authentication required')
  })
})
```

## Performance Considerations

1. **Prefer Server Components for reads** - Server Actions are for mutations
2. **Batch operations when possible** - Use `deleteEntities` instead of multiple `deleteEntity`
3. **Minimal revalidation** - Only revalidate affected paths
4. **Early validation** - Fail fast before expensive operations

## Related Skills

- `service-layer` - Business logic implementation
- `tanstack-query` - Optimistic updates and caching
- `react-patterns` - Form and component patterns
- `zod-validation` - Input validation schemas
