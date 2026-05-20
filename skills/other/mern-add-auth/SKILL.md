---
name: mern-add-auth
description: Add authentication to a MERN project using NextAuth.js with OAuth and/or credentials.
argument-hint: "[--providers google,github,credentials] [--with-user-model]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Add secure authentication to an existing MERN project using NextAuth.js (Auth.js).

## Arguments
- `--providers <list>` — Comma-separated providers (default: `google,github`)
  - Options: `google`, `github`, `discord`, `credentials`
- `--with-user-model` — Create User model in MongoDB for storing user data

## What gets created

```
apps/web/
├── app/api/auth/[...nextauth]/route.ts   # NextAuth API route
├── src/lib/auth.ts                        # Auth config + providers
├── src/lib/auth-client.ts                 # Client-side helpers
├── src/components/auth/
│   ├── SignInButton.tsx                   # OAuth sign-in
│   ├── SignOutButton.tsx                  # Sign-out
│   └── UserMenu.tsx                       # User avatar + dropdown
├── src/server/db/models/user.ts           # (if --with-user-model)
└── middleware.ts                          # Route protection

packages/shared/schemas/
└── user.ts                                # User schemas

.env.example                               # Updated with auth vars
```

## Environment variables required

```bash
# OAuth (per provider)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=

# NextAuth
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=  # Generate with: openssl rand -base64 32
```

## Workflow
1. Install dependencies: `next-auth`, `@auth/mongodb-adapter` (if using DB)
2. Create auth config with selected providers
3. Create API route handler
4. Create auth components
5. Create middleware for protected routes
6. Update env.ts schema with auth variables
7. Create User model (if --with-user-model)
8. Add session provider to app layout
9. Run tests to verify

## Protected routes
Middleware protects routes matching these patterns by default:
- `/dashboard/*`
- `/settings/*`
- `/api/*` (except `/api/auth/*` and `/api/health`)

Customize in `middleware.ts`.

## Usage patterns

### Server Component
```typescript
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';

const session = await getServerSession(authOptions);
if (!session) redirect('/api/auth/signin');
```

### Client Component
```typescript
'use client';
import { useSession } from 'next-auth/react';

const { data: session, status } = useSession();
```

### API Route
```typescript
const session = await getServerSession(authOptions);
if (!session?.user?.id) {
  return NextResponse.json(err('UNAUTHORIZED', 'Authentication required'), { status: 401 });
}
```

## Output
Summarize: providers configured, environment variables needed, protected routes, components available.

## Reference
For templates and OAuth setup guides, see `reference/mern-add-auth-reference.md`
