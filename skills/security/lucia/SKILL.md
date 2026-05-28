---
name: lucia
description: Implements session-based authentication with Lucia Auth library for server-side session management and cookie handling. Use when building custom authentication, session management, or when user mentions Lucia, server-side auth, or session cookies.
---

# Lucia Auth

Server-side session-based authentication library that abstracts session management complexity.

**Note**: Lucia v3 will be deprecated by March 2025. The patterns here remain valid for session-based auth.

## Quick Start

```bash
npm install lucia
npm install @lucia-auth/adapter-prisma  # Or your database adapter
```

## Setup

### Basic Configuration

```typescript
// lib/auth.ts
import { Lucia, TimeSpan } from 'lucia';
import { PrismaAdapter } from '@lucia-auth/adapter-prisma';
import { prisma } from './prisma';

const adapter = new PrismaAdapter(prisma.session, prisma.user);

export const lucia = new Lucia(adapter, {
  sessionExpiresIn: new TimeSpan(30, 'd'), // 30 days
  sessionCookie: {
    name: 'session',
    expires: false, // Session cookie
    attributes: {
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
    },
  },
  getUserAttributes: (attributes) => ({
    email: attributes.email,
    name: attributes.name,
    role: attributes.role,
  }),
});

// Type declarations
declare module 'lucia' {
  interface Register {
    Lucia: typeof lucia;
    DatabaseUserAttributes: {
      email: string;
      name: string;
      role: 'user' | 'admin';
    };
  }
}
```

### Database Schema (Prisma)

```prisma
// prisma/schema.prisma
model User {
  id            String    @id @default(cuid())
  email         String    @unique
  name          String
  role          String    @default("user")
  passwordHash  String
  sessions      Session[]
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
}

model Session {
  id        String   @id
  userId    String
  expiresAt DateTime
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
}
```

### Other Adapters

```typescript
// Drizzle
import { DrizzlePostgreSQLAdapter } from '@lucia-auth/adapter-drizzle';
const adapter = new DrizzlePostgreSQLAdapter(db, sessionTable, userTable);

// SQLite with better-sqlite3
import { BetterSqlite3Adapter } from '@lucia-auth/adapter-sqlite';
const adapter = new BetterSqlite3Adapter(db, {
  user: 'users',
  session: 'sessions',
});

// MongoDB
import { MongodbAdapter } from '@lucia-auth/adapter-mongodb';
const adapter = new MongodbAdapter(
  db.collection('sessions'),
  db.collection('users')
);
```

## Authentication Flow

### Registration

```typescript
import { generateId } from 'lucia';
import { hash } from '@node-rs/argon2';

async function register(email: string, password: string, name: string) {
  // Validate input
  if (!email || !password || password.length < 8) {
    throw new Error('Invalid input');
  }

  // Check if user exists
  const existingUser = await prisma.user.findUnique({
    where: { email },
  });

  if (existingUser) {
    throw new Error('Email already registered');
  }

  // Hash password
  const passwordHash = await hash(password, {
    memoryCost: 19456,
    timeCost: 2,
    outputLen: 32,
    parallelism: 1,
  });

  // Create user
  const userId = generateId(15);
  const user = await prisma.user.create({
    data: {
      id: userId,
      email,
      name,
      passwordHash,
    },
  });

  // Create session
  const session = await lucia.createSession(userId, {});
  const sessionCookie = lucia.createSessionCookie(session.id);

  return { user, sessionCookie };
}
```

### Login

```typescript
import { verify } from '@node-rs/argon2';

async function login(email: string, password: string) {
  // Find user
  const user = await prisma.user.findUnique({
    where: { email },
  });

  if (!user) {
    throw new Error('Invalid email or password');
  }

  // Verify password
  const validPassword = await verify(user.passwordHash, password);
  if (!validPassword) {
    throw new Error('Invalid email or password');
  }

  // Create session
  const session = await lucia.createSession(user.id, {});
  const sessionCookie = lucia.createSessionCookie(session.id);

  return { user, sessionCookie };
}
```

### Logout

```typescript
async function logout(sessionId: string) {
  await lucia.invalidateSession(sessionId);
  const blankCookie = lucia.createBlankSessionCookie();
  return blankCookie;
}

// Logout from all devices
async function logoutAll(userId: string) {
  await lucia.invalidateUserSessions(userId);
  const blankCookie = lucia.createBlankSessionCookie();
  return blankCookie;
}
```

## Session Validation

### Reading Session Cookie

```typescript
import { cookies } from 'next/headers'; // Next.js example

function getSessionCookie(): string | null {
  return cookies().get(lucia.sessionCookieName)?.value ?? null;
}

// Or from raw header
function getSessionFromHeader(cookieHeader: string): string | null {
  return lucia.readSessionCookie(cookieHeader);
}
```

### Validating Sessions

```typescript
async function validateRequest() {
  const sessionId = getSessionCookie();

  if (!sessionId) {
    return { user: null, session: null };
  }

  const { user, session } = await lucia.validateSession(sessionId);

  // Session is fresh - set new cookie
  if (session?.fresh) {
    const sessionCookie = lucia.createSessionCookie(session.id);
    cookies().set(
      sessionCookie.name,
      sessionCookie.value,
      sessionCookie.attributes
    );
  }

  // Session is invalid - clear cookie
  if (!session) {
    const blankCookie = lucia.createBlankSessionCookie();
    cookies().set(
      blankCookie.name,
      blankCookie.value,
      blankCookie.attributes
    );
  }

  return { user, session };
}
```

## Framework Integration

### Next.js (App Router)

```typescript
// lib/auth.ts
import { cookies } from 'next/headers';
import { cache } from 'react';

export const validateRequest = cache(async () => {
  const sessionId = cookies().get(lucia.sessionCookieName)?.value ?? null;

  if (!sessionId) {
    return { user: null, session: null };
  }

  const result = await lucia.validateSession(sessionId);

  try {
    if (result.session?.fresh) {
      const sessionCookie = lucia.createSessionCookie(result.session.id);
      cookies().set(
        sessionCookie.name,
        sessionCookie.value,
        sessionCookie.attributes
      );
    }
    if (!result.session) {
      const blankCookie = lucia.createBlankSessionCookie();
      cookies().set(
        blankCookie.name,
        blankCookie.value,
        blankCookie.attributes
      );
    }
  } catch {
    // Next.js throws when setting cookies in Server Components
  }

  return result;
});
```

```typescript
// app/api/auth/login/route.ts
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const { email, password } = await request.json();

  try {
    const { sessionCookie } = await login(email, password);

    return new NextResponse(JSON.stringify({ success: true }), {
      status: 200,
      headers: {
        'Set-Cookie': sessionCookie.serialize(),
      },
    });
  } catch (error) {
    return NextResponse.json(
      { error: error.message },
      { status: 401 }
    );
  }
}
```

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  // CSRF protection
  if (request.method !== 'GET') {
    const origin = request.headers.get('origin');
    const host = request.headers.get('host');

    if (!origin || !host || new URL(origin).host !== host) {
      return new NextResponse(null, { status: 403 });
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/api/:path*'],
};
```

### Express

```typescript
import express from 'express';
import { lucia } from './lib/auth';

const app = express();

// Session middleware
app.use(async (req, res, next) => {
  const sessionId = lucia.readSessionCookie(req.headers.cookie ?? '');

  if (!sessionId) {
    res.locals.user = null;
    res.locals.session = null;
    return next();
  }

  const { session, user } = await lucia.validateSession(sessionId);

  if (session?.fresh) {
    res.appendHeader(
      'Set-Cookie',
      lucia.createSessionCookie(session.id).serialize()
    );
  }

  if (!session) {
    res.appendHeader(
      'Set-Cookie',
      lucia.createBlankSessionCookie().serialize()
    );
  }

  res.locals.user = user;
  res.locals.session = session;
  next();
});

// CSRF protection
app.use((req, res, next) => {
  if (req.method === 'GET') return next();

  const origin = req.headers.origin;
  const host = req.headers.host;

  if (!origin || !host || new URL(origin).host !== host) {
    return res.status(403).send('Forbidden');
  }

  next();
});

// Protected route
app.get('/api/me', (req, res) => {
  if (!res.locals.user) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  res.json({ user: res.locals.user });
});

// Login route
app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;

  try {
    const { sessionCookie } = await login(email, password);
    res.appendHeader('Set-Cookie', sessionCookie.serialize());
    res.json({ success: true });
  } catch (error) {
    res.status(401).json({ error: error.message });
  }
});

// Logout route
app.post('/api/logout', async (req, res) => {
  if (!res.locals.session) {
    return res.status(401).json({ error: 'Not logged in' });
  }

  await lucia.invalidateSession(res.locals.session.id);
  res.appendHeader(
    'Set-Cookie',
    lucia.createBlankSessionCookie().serialize()
  );
  res.json({ success: true });
});
```

### Hono

```typescript
import { Hono } from 'hono';
import { getCookie, setCookie } from 'hono/cookie';

const app = new Hono();

// Session middleware
app.use('*', async (c, next) => {
  const sessionId = getCookie(c, lucia.sessionCookieName) ?? null;

  if (!sessionId) {
    c.set('user', null);
    c.set('session', null);
    return next();
  }

  const { session, user } = await lucia.validateSession(sessionId);

  if (session?.fresh) {
    const cookie = lucia.createSessionCookie(session.id);
    setCookie(c, cookie.name, cookie.value, cookie.attributes);
  }

  if (!session) {
    const cookie = lucia.createBlankSessionCookie();
    setCookie(c, cookie.name, cookie.value, cookie.attributes);
  }

  c.set('user', user);
  c.set('session', session);
  await next();
});

// Protected route helper
const authRequired = async (c, next) => {
  if (!c.get('user')) {
    return c.json({ error: 'Unauthorized' }, 401);
  }
  await next();
};

app.get('/api/me', authRequired, (c) => {
  return c.json({ user: c.get('user') });
});
```

## OAuth Integration

```typescript
import { generateState, generateCodeVerifier } from 'arctic';
import { GitHub } from 'arctic';

const github = new GitHub(
  process.env.GITHUB_CLIENT_ID!,
  process.env.GITHUB_CLIENT_SECRET!
);

// Start OAuth flow
async function startGitHubAuth() {
  const state = generateState();
  const codeVerifier = generateCodeVerifier();

  const url = await github.createAuthorizationURL(state, {
    scopes: ['user:email'],
  });

  return { url, state, codeVerifier };
}

// Handle callback
async function handleGitHubCallback(code: string, state: string) {
  const tokens = await github.validateAuthorizationCode(code);

  // Get user info
  const response = await fetch('https://api.github.com/user', {
    headers: {
      Authorization: `Bearer ${tokens.accessToken}`,
    },
  });
  const githubUser = await response.json();

  // Find or create user
  let user = await prisma.user.findUnique({
    where: { githubId: githubUser.id },
  });

  if (!user) {
    user = await prisma.user.create({
      data: {
        id: generateId(15),
        githubId: githubUser.id,
        email: githubUser.email,
        name: githubUser.name || githubUser.login,
      },
    });
  }

  // Create session
  const session = await lucia.createSession(user.id, {});
  const sessionCookie = lucia.createSessionCookie(session.id);

  return { user, sessionCookie };
}
```

## Password Reset

```typescript
import { generateId } from 'lucia';

// Request reset
async function requestPasswordReset(email: string) {
  const user = await prisma.user.findUnique({ where: { email } });
  if (!user) return; // Don't reveal if user exists

  // Generate token
  const token = generateId(40);
  const expiresAt = new Date(Date.now() + 1000 * 60 * 60); // 1 hour

  await prisma.passwordReset.create({
    data: {
      token,
      userId: user.id,
      expiresAt,
    },
  });

  // Send email with reset link
  await sendEmail({
    to: email,
    subject: 'Password Reset',
    html: `<a href="${process.env.URL}/reset-password?token=${token}">Reset Password</a>`,
  });
}

// Complete reset
async function resetPassword(token: string, newPassword: string) {
  const reset = await prisma.passwordReset.findUnique({
    where: { token },
    include: { user: true },
  });

  if (!reset || reset.expiresAt < new Date()) {
    throw new Error('Invalid or expired token');
  }

  const passwordHash = await hash(newPassword);

  await prisma.$transaction([
    prisma.user.update({
      where: { id: reset.userId },
      data: { passwordHash },
    }),
    prisma.passwordReset.delete({ where: { token } }),
  ]);

  // Invalidate all sessions
  await lucia.invalidateUserSessions(reset.userId);
}
```

## Reference Files

- [oauth-providers.md](references/oauth-providers.md) - OAuth provider setup guides
- [security.md](references/security.md) - Security best practices
