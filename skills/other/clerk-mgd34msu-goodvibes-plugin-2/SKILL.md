---
name: clerk
description: Implements authentication with Clerk including user management, protected routes, middleware, and React components. Use when adding authentication, managing users, protecting routes, or implementing sign-in/sign-up flows.
---

# Clerk

Complete authentication and user management platform for modern web applications.

## Quick Start

**Install:**
```bash
npm install @clerk/nextjs
```

**Environment variables:**
```bash
# .env.local
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
```

## Middleware Setup

```typescript
// middleware.ts (or proxy.ts for Next.js 15+)
import { clerkMiddleware } from '@clerk/nextjs/server';

export default clerkMiddleware();

export const config = {
  matcher: [
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    '/(api|trpc)(.*)',
  ],
};
```

## Provider Setup

```tsx
// app/layout.tsx
import { ClerkProvider } from '@clerk/nextjs';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}
```

## UI Components

### Auth Buttons

```tsx
import {
  SignInButton,
  SignUpButton,
  SignedIn,
  SignedOut,
  UserButton,
} from '@clerk/nextjs';

export function Header() {
  return (
    <header className="flex justify-between items-center p-4">
      <h1>My App</h1>
      <div className="flex gap-4">
        <SignedOut>
          <SignInButton mode="modal" />
          <SignUpButton mode="modal" />
        </SignedOut>
        <SignedIn>
          <UserButton afterSignOutUrl="/" />
        </SignedIn>
      </div>
    </header>
  );
}
```

### Custom Sign-In Page

```tsx
// app/sign-in/[[...sign-in]]/page.tsx
import { SignIn } from '@clerk/nextjs';

export default function SignInPage() {
  return (
    <div className="flex justify-center items-center min-h-screen">
      <SignIn
        appearance={{
          elements: {
            rootBox: 'mx-auto',
            card: 'shadow-xl',
          },
        }}
      />
    </div>
  );
}
```

### Custom Sign-Up Page

```tsx
// app/sign-up/[[...sign-up]]/page.tsx
import { SignUp } from '@clerk/nextjs';

export default function SignUpPage() {
  return (
    <div className="flex justify-center items-center min-h-screen">
      <SignUp />
    </div>
  );
}
```

## Route Protection

### Using createRouteMatcher

```typescript
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

const isProtectedRoute = createRouteMatcher([
  '/dashboard(.*)',
  '/settings(.*)',
  '/api/private(.*)',
]);

const isPublicRoute = createRouteMatcher([
  '/',
  '/sign-in(.*)',
  '/sign-up(.*)',
  '/api/public(.*)',
]);

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) {
    await auth.protect();
  }
});
```

### Protect All Routes

```typescript
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

const isPublicRoute = createRouteMatcher([
  '/',
  '/sign-in(.*)',
  '/sign-up(.*)',
]);

export default clerkMiddleware(async (auth, req) => {
  if (!isPublicRoute(req)) {
    await auth.protect();
  }
});
```

### Role-Based Protection

```typescript
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

const isAdminRoute = createRouteMatcher(['/admin(.*)']);

export default clerkMiddleware(async (auth, req) => {
  if (isAdminRoute(req)) {
    await auth.protect((has) => {
      return has({ role: 'org:admin' });
    });
  }
});
```

### Permission-Based Protection

```typescript
export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) {
    await auth.protect((has) => {
      return has({ permission: 'org:billing:manage' });
    });
  }
});
```

## React Hooks

### useUser

```tsx
'use client';

import { useUser } from '@clerk/nextjs';

export function Profile() {
  const { isLoaded, isSignedIn, user } = useUser();

  if (!isLoaded) {
    return <div>Loading...</div>;
  }

  if (!isSignedIn) {
    return <div>Please sign in</div>;
  }

  return (
    <div>
      <h1>Hello, {user.firstName}!</h1>
      <p>Email: {user.primaryEmailAddress?.emailAddress}</p>
      <img src={user.imageUrl} alt="Profile" className="w-16 h-16 rounded-full" />
    </div>
  );
}
```

### useAuth

```tsx
'use client';

import { useAuth } from '@clerk/nextjs';

export function AuthInfo() {
  const { isLoaded, userId, sessionId, getToken } = useAuth();

  if (!isLoaded) {
    return <div>Loading...</div>;
  }

  if (!userId) {
    return <div>Not signed in</div>;
  }

  return (
    <div>
      <p>User ID: {userId}</p>
      <p>Session ID: {sessionId}</p>
    </div>
  );
}

// Get token for API calls
async function fetchWithAuth() {
  const { getToken } = useAuth();
  const token = await getToken();

  const res = await fetch('/api/protected', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}
```

### useClerk

```tsx
'use client';

import { useClerk } from '@clerk/nextjs';

export function CustomSignOut() {
  const { signOut, openSignIn, openUserProfile } = useClerk();

  return (
    <div className="flex gap-2">
      <button onClick={() => openSignIn()}>Sign In</button>
      <button onClick={() => openUserProfile()}>Profile</button>
      <button onClick={() => signOut()}>Sign Out</button>
    </div>
  );
}
```

### useOrganization

```tsx
'use client';

import { useOrganization } from '@clerk/nextjs';

export function OrgInfo() {
  const { isLoaded, organization, membership } = useOrganization();

  if (!isLoaded) return <div>Loading...</div>;
  if (!organization) return <div>No organization selected</div>;

  return (
    <div>
      <h2>{organization.name}</h2>
      <p>Role: {membership?.role}</p>
      <p>Members: {organization.membersCount}</p>
    </div>
  );
}
```

## Server-Side Auth

### Server Components

```tsx
// app/dashboard/page.tsx
import { currentUser, auth } from '@clerk/nextjs/server';

export default async function DashboardPage() {
  const user = await currentUser();

  if (!user) {
    return <div>Please sign in</div>;
  }

  return (
    <div>
      <h1>Welcome, {user.firstName}!</h1>
      <p>Email: {user.emailAddresses[0].emailAddress}</p>
    </div>
  );
}

// Using auth() for session data
export default async function ProtectedPage() {
  const { userId, sessionClaims } = await auth();

  if (!userId) {
    return <div>Unauthorized</div>;
  }

  return <div>User ID: {userId}</div>;
}
```

### API Routes

```typescript
// app/api/user/route.ts
import { auth, currentUser } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';

export async function GET() {
  const { userId } = await auth();

  if (!userId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const user = await currentUser();

  return NextResponse.json({
    id: userId,
    email: user?.emailAddresses[0].emailAddress,
  });
}
```

### Server Actions

```typescript
// app/actions.ts
'use server';

import { auth, currentUser } from '@clerk/nextjs/server';

export async function updateProfile(formData: FormData) {
  const { userId } = await auth();

  if (!userId) {
    throw new Error('Unauthorized');
  }

  const name = formData.get('name') as string;

  // Update user in database
  await db.user.update({
    where: { clerkId: userId },
    data: { name },
  });

  return { success: true };
}
```

## User Metadata

### Public Metadata (Read-only from client)

```typescript
// Server-side: Update public metadata
import { clerkClient } from '@clerk/nextjs/server';

await clerkClient.users.updateUserMetadata(userId, {
  publicMetadata: {
    role: 'admin',
    plan: 'premium',
  },
});
```

### Private Metadata (Server-only)

```typescript
// Only accessible on server
await clerkClient.users.updateUserMetadata(userId, {
  privateMetadata: {
    stripeCustomerId: 'cus_...',
    internalNotes: 'VIP customer',
  },
});
```

### Unsafe Metadata (Client-writable)

```tsx
'use client';

import { useUser } from '@clerk/nextjs';

export function UpdatePreferences() {
  const { user } = useUser();

  async function updateTheme(theme: string) {
    await user?.update({
      unsafeMetadata: {
        theme,
        notifications: true,
      },
    });
  }

  return (
    <button onClick={() => updateTheme('dark')}>
      Set Dark Theme
    </button>
  );
}
```

## Webhooks

```typescript
// app/api/webhooks/clerk/route.ts
import { Webhook } from 'svix';
import { headers } from 'next/headers';
import { WebhookEvent } from '@clerk/nextjs/server';

export async function POST(req: Request) {
  const WEBHOOK_SECRET = process.env.CLERK_WEBHOOK_SECRET!;
  const headerPayload = headers();
  const svix_id = headerPayload.get('svix-id');
  const svix_timestamp = headerPayload.get('svix-timestamp');
  const svix_signature = headerPayload.get('svix-signature');

  if (!svix_id || !svix_timestamp || !svix_signature) {
    return new Response('Missing svix headers', { status: 400 });
  }

  const payload = await req.json();
  const body = JSON.stringify(payload);

  const wh = new Webhook(WEBHOOK_SECRET);
  let evt: WebhookEvent;

  try {
    evt = wh.verify(body, {
      'svix-id': svix_id,
      'svix-timestamp': svix_timestamp,
      'svix-signature': svix_signature,
    }) as WebhookEvent;
  } catch (err) {
    return new Response('Invalid signature', { status: 400 });
  }

  const eventType = evt.type;

  if (eventType === 'user.created') {
    const { id, email_addresses, first_name, last_name } = evt.data;

    await db.user.create({
      data: {
        clerkId: id,
        email: email_addresses[0].email_address,
        firstName: first_name,
        lastName: last_name,
      },
    });
  }

  if (eventType === 'user.updated') {
    const { id, first_name, last_name } = evt.data;

    await db.user.update({
      where: { clerkId: id },
      data: { firstName: first_name, lastName: last_name },
    });
  }

  if (eventType === 'user.deleted') {
    const { id } = evt.data;

    await db.user.delete({
      where: { clerkId: id },
    });
  }

  return new Response('OK', { status: 200 });
}
```

## Theming

```tsx
// app/layout.tsx
import { ClerkProvider } from '@clerk/nextjs';
import { dark } from '@clerk/themes';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider
      appearance={{
        baseTheme: dark,
        variables: {
          colorPrimary: '#3b82f6',
          colorBackground: '#1f2937',
        },
        elements: {
          card: 'shadow-xl rounded-xl',
          formButtonPrimary: 'bg-blue-500 hover:bg-blue-600',
          footerActionLink: 'text-blue-400 hover:text-blue-300',
        },
      }}
    >
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}
```

## Best Practices

1. **Use middleware for route protection** - Centralized, secure
2. **Sync users via webhooks** - Keep database in sync
3. **Store user IDs, not emails** - Emails can change
4. **Use public metadata for roles** - Accessible client-side
5. **Leverage organizations** - For multi-tenant apps

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing middleware | Add clerkMiddleware() |
| Unprotected API routes | Check auth() in routes |
| Client-side role checks only | Validate on server |
| Hardcoded redirect URLs | Use environment variables |
| Missing webhook verification | Always verify signatures |

## Reference Files

- [references/middleware.md](references/middleware.md) - Advanced middleware patterns
- [references/organizations.md](references/organizations.md) - Multi-tenant auth
- [references/webhooks.md](references/webhooks.md) - Event handling
