---
name: Better Auth
description: Authentication and session management with Better Auth in LivestockAI
---

# Better Auth

LivestockAI uses [Better Auth](https://better-auth.com) for authentication. It provides secure session management with email/password authentication.

## Table Structure

Better Auth uses two tables:

| Table     | Purpose                                             |
| --------- | --------------------------------------------------- |
| `users`   | User profile data (name, email, role) - NO password |
| `account` | Authentication credentials (password, providerId)   |

**Important**: Passwords are stored in `account`, not `users`.

## Creating Users Programmatically

**ALWAYS use the `createUserWithAuth` helper**:

```typescript
import { createUserWithAuth } from '~/lib/db/seeds/helpers'

const result = await createUserWithAuth(db, {
  email: 'user@example.com',
  password: 'securepassword',
  name: 'John Doe',
  role: 'user', // or 'admin'
})
```

This helper:

1. Hashes the password using PBKDF2 (100,000 iterations, SHA-256)
2. Creates entry in `users` table
3. Creates entry in `account` table with `providerId: 'credential'`

### Wrong Way

```typescript
// ❌ WRONG - users table has no password field!
await db
  .insertInto('users')
  .values({
    email: 'user@example.com',
    password: 'hashedpassword', // This field doesn't exist!
  })
  .execute()
```

## Auth Configuration

The auth config is in `app/features/auth/config.ts`:

```typescript
import { betterAuth } from 'better-auth'

export const auth = betterAuth({
  database: {
    type: 'postgres',
    url: process.env.DATABASE_URL,
  },
  emailAndPassword: {
    enabled: true,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
  },
})
```

## Server Middleware

Use `requireAuth()` in server functions:

```typescript
export const myServerFn = createServerFn({ method: 'GET' }).handler(
  async () => {
    const { requireAuth } = await import('../auth/server-middleware')
    const session = await requireAuth()

    // session.user contains:
    // - id: string
    // - email: string
    // - name: string
    // - role: 'user' | 'admin'

    return { userId: session.user.id }
  },
)
```

## Auth Utilities

```typescript
// app/features/auth/utils.ts

// Check if user has access to a farm
export async function checkFarmAccess(
  userId: string,
  farmId: string,
): Promise<boolean>

// Get all farms a user has access to
export async function getUserFarms(userId: string): Promise<string[]>
```

## Client-Side Auth

```typescript
import { useSession, signIn, signOut } from '~/features/auth/client'

function LoginButton() {
  const { data: session, isLoading } = useSession()

  if (isLoading) return <Spinner />

  if (session) {
    return (
      <Button onClick={() => signOut()}>
        Sign Out ({session.user.email})
      </Button>
    )
  }

  return (
    <Button onClick={() => signIn('credential', { email, password })}>
      Sign In
    </Button>
  )
}
```

## Protected Routes

The `_auth.tsx` layout protects routes:

```typescript
// app/routes/_auth.tsx
export const Route = createFileRoute('/_auth')({
  beforeLoad: async () => {
    const session = await getSession()
    if (!session) {
      throw redirect({ to: '/login' })
    }
    return { session }
  },
})
```

## User Roles

LivestockAI supports roles:

| Role              | Access               |
| ----------------- | -------------------- |
| `user`            | Standard farm access |
| `admin`           | Full system access   |
| `extension_agent` | District-level view  |

```typescript
// Check role in server function
const session = await requireAuth()
if (session.user.role !== 'admin') {
  throw new AppError('ACCESS_DENIED')
}
```

## Session Data

The session object contains:

```typescript
interface Session {
  user: {
    id: string
    email: string
    name: string
    role: 'user' | 'admin' | 'extension_agent'
    image?: string
  }
  expires: Date
}
```

## Related Skills

- `three-layer-architecture` - Auth in server layer
- `error-handling` - Auth error handling
- `tanstack-start` - Server function patterns
