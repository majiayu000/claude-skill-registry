---
name: auth0
description: Implements Auth0 authentication with Next.js SDK, React hooks, role-based access, and API protection. Use when integrating Auth0, implementing enterprise SSO, or needing managed authentication with MFA.
---

# Auth0

Auth0 is an identity platform providing authentication, authorization, and user management. The Next.js SDK (v4) offers full App Router and Pages Router support.

## Quick Start

### Installation

```bash
npm install @auth0/nextjs-auth0
```

### Environment Variables

```env
# .env.local
AUTH0_SECRET='use-a-long-random-string-min-32-chars'
AUTH0_BASE_URL='http://localhost:3000'
AUTH0_ISSUER_BASE_URL='https://your-tenant.auth0.com'
AUTH0_CLIENT_ID='your-client-id'
AUTH0_CLIENT_SECRET='your-client-secret'
```

Generate secret: `openssl rand -hex 32`

### Auth0 Dashboard Setup

1. Create Regular Web Application
2. Set Allowed Callback URLs: `http://localhost:3000/auth/callback`
3. Set Allowed Logout URLs: `http://localhost:3000`
4. Set Allowed Web Origins: `http://localhost:3000`

## App Router Setup (Next.js 13+)

### Create Auth Route Handler

```typescript
// app/auth/[auth0]/route.ts
import { handleAuth } from '@auth0/nextjs-auth0'

export const GET = handleAuth()
```

This creates routes:
- `/auth/login` - Initiates login
- `/auth/logout` - Logs out user
- `/auth/callback` - OAuth callback
- `/auth/me` - Returns user profile

### Add Provider

```typescript
// app/layout.tsx
import { Auth0Provider } from '@auth0/nextjs-auth0'

export default function RootLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <Auth0Provider>
          {children}
        </Auth0Provider>
      </body>
    </html>
  )
}
```

### Client Component Usage

```typescript
'use client'
import { useUser } from '@auth0/nextjs-auth0'

export default function Profile() {
  const { user, error, isLoading } = useUser()

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  if (!user) return <a href="/auth/login">Login</a>

  return (
    <div>
      <img src={user.picture} alt={user.name} />
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      <a href="/auth/logout">Logout</a>
    </div>
  )
}
```

### Server Component Usage

```typescript
// app/dashboard/page.tsx
import { getSession } from '@auth0/nextjs-auth0'
import { redirect } from 'next/navigation'

export default async function Dashboard() {
  const session = await getSession()

  if (!session) {
    redirect('/auth/login')
  }

  return (
    <div>
      <h1>Welcome, {session.user.name}</h1>
      <pre>{JSON.stringify(session.user, null, 2)}</pre>
    </div>
  )
}
```

## Protected Routes

### Middleware Protection

```typescript
// middleware.ts
import { withMiddlewareAuthRequired } from '@auth0/nextjs-auth0/edge'

export default withMiddlewareAuthRequired()

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*']
}
```

### Page-Level Protection

```typescript
// app/protected/page.tsx
import { withPageAuthRequired, getSession } from '@auth0/nextjs-auth0'

export default withPageAuthRequired(async function ProtectedPage() {
  const session = await getSession()
  return <div>Protected content for {session?.user.email}</div>
}, {
  returnTo: '/protected'
})
```

## API Route Protection

### Server Component API

```typescript
// app/api/me/route.ts
import { getSession } from '@auth0/nextjs-auth0'
import { NextResponse } from 'next/server'

export async function GET() {
  const session = await getSession()

  if (!session) {
    return NextResponse.json(
      { error: 'Not authenticated' },
      { status: 401 }
    )
  }

  return NextResponse.json({ user: session.user })
}
```

### Protected API Route

```typescript
// app/api/protected/route.ts
import { withApiAuthRequired, getSession } from '@auth0/nextjs-auth0'
import { NextResponse } from 'next/server'

export const GET = withApiAuthRequired(async function handler(req) {
  const session = await getSession()
  return NextResponse.json({
    message: `Hello ${session?.user.name}`
  })
})
```

## Calling External APIs

### Get Access Token

```typescript
// app/api/external/route.ts
import { getAccessToken } from '@auth0/nextjs-auth0'
import { NextResponse } from 'next/server'

export async function GET() {
  try {
    const { accessToken } = await getAccessToken({
      scopes: ['read:data']
    })

    const response = await fetch('https://api.example.com/data', {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    })

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get token' },
      { status: 500 }
    )
  }
}
```

### Configure API Audience

```env
AUTH0_AUDIENCE='https://api.example.com'
AUTH0_SCOPE='openid profile email read:data'
```

## Role-Based Access Control

### Add Roles to Tokens

In Auth0 Dashboard > Actions > Flows > Login, add:

```javascript
exports.onExecutePostLogin = async (event, api) => {
  const namespace = 'https://myapp.com'
  if (event.authorization) {
    api.idToken.setCustomClaim(`${namespace}/roles`, event.authorization.roles)
    api.accessToken.setCustomClaim(`${namespace}/roles`, event.authorization.roles)
  }
}
```

### Check Roles

```typescript
// lib/auth.ts
import { getSession } from '@auth0/nextjs-auth0'

export async function getUserRoles(): Promise<string[]> {
  const session = await getSession()
  if (!session) return []
  return session.user['https://myapp.com/roles'] || []
}

export async function hasRole(role: string): Promise<boolean> {
  const roles = await getUserRoles()
  return roles.includes(role)
}

export async function requireRole(role: string) {
  if (!(await hasRole(role))) {
    throw new Error('Unauthorized')
  }
}
```

### Role-Protected Component

```typescript
// app/admin/page.tsx
import { getSession } from '@auth0/nextjs-auth0'
import { redirect } from 'next/navigation'

export default async function AdminPage() {
  const session = await getSession()
  const roles = session?.user['https://myapp.com/roles'] || []

  if (!roles.includes('admin')) {
    redirect('/unauthorized')
  }

  return <div>Admin Dashboard</div>
}
```

## Custom Login/Logout

### Custom Login Options

```typescript
// app/auth/[auth0]/route.ts
import { handleAuth, handleLogin } from '@auth0/nextjs-auth0'

export const GET = handleAuth({
  login: handleLogin({
    authorizationParams: {
      audience: 'https://api.example.com',
      scope: 'openid profile email read:data'
    },
    returnTo: '/dashboard'
  }),
  signup: handleLogin({
    authorizationParams: {
      screen_hint: 'signup'
    }
  })
})
```

### Custom Logout

```typescript
import { handleAuth, handleLogout } from '@auth0/nextjs-auth0'

export const GET = handleAuth({
  logout: handleLogout({
    returnTo: '/'
  })
})
```

## Session Management

### Update Session

```typescript
// app/api/update-session/route.ts
import { getSession, updateSession } from '@auth0/nextjs-auth0'
import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  const session = await getSession()
  if (!session) {
    return NextResponse.json({ error: 'Not authenticated' }, { status: 401 })
  }

  // Update session with custom data
  await updateSession({
    ...session,
    user: {
      ...session.user,
      customData: 'new value'
    }
  })

  return NextResponse.json({ success: true })
}
```

### Session Configuration

```typescript
// app/auth/[auth0]/route.ts
import { handleAuth } from '@auth0/nextjs-auth0'

export const GET = handleAuth({
  onError(req, error) {
    console.error(error)
  }
})
```

## Organization Support

### Login to Organization

```typescript
import { handleAuth, handleLogin } from '@auth0/nextjs-auth0'

export const GET = handleAuth({
  login: handleLogin({
    authorizationParams: {
      organization: 'org_123'
    }
  })
})
```

### Dynamic Organization

```typescript
// app/login/[org]/route.ts
import { handleLogin } from '@auth0/nextjs-auth0'
import { NextRequest } from 'next/server'

export async function GET(
  req: NextRequest,
  { params }: { params: { org: string } }
) {
  return handleLogin(req, {
    authorizationParams: {
      organization: params.org
    }
  })
}
```

## Multi-Factor Authentication

Enable MFA in Auth0 Dashboard > Security > Multi-factor Auth:

```typescript
// Force MFA for sensitive actions
import { handleAuth, handleLogin } from '@auth0/nextjs-auth0'

export const GET = handleAuth({
  'login-mfa': handleLogin({
    authorizationParams: {
      acr_values: 'http://schemas.openid.net/pape/policies/2007/06/multi-factor'
    }
  })
})
```

## Testing

### Mock User in Tests

```typescript
// __tests__/profile.test.tsx
import { render, screen } from '@testing-library/react'
import { UserProvider } from '@auth0/nextjs-auth0'
import Profile from '@/app/profile/page'

const mockUser = {
  name: 'Test User',
  email: 'test@example.com',
  picture: 'https://example.com/avatar.png'
}

test('renders user profile', () => {
  render(
    <UserProvider user={mockUser}>
      <Profile />
    </UserProvider>
  )
  expect(screen.getByText('Test User')).toBeInTheDocument()
})
```

## Best Practices

1. **Use environment variables** - Never hardcode secrets
2. **Protect API routes** - Use `withApiAuthRequired`
3. **Add roles to tokens** - Use Auth0 Actions
4. **Configure audiences** - For API access tokens
5. **Handle errors gracefully** - Provide user-friendly messages
6. **Use middleware** - For route protection at scale

## References

- [Organizations & SSO](references/organizations.md)
- [Custom Actions](references/actions.md)
