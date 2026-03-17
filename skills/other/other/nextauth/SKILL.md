---
name: nextauth
description: >-
  Configure NextAuth.js v5 authentication with OAuth providers and Prisma adapter.
  Use when setting up login/logout, protecting routes, accessing sessions in components,
  adding OAuth providers, or troubleshooting authentication issues.
license: MIT
compatibility: [Claude Code]
metadata:
  author: ftcmetrics
  version: "1.0.0"
  category: auth
---

# NextAuth.js v5 Authentication Guide

NextAuth.js v5 (Auth.js) is the authentication library for FTC Metrics. It uses OAuth providers (Google, Discord, GitHub) with a Prisma database adapter for session persistence.

## Quick Start

### 1. Install Dependencies

```bash
bun add next-auth@beta @auth/prisma-adapter
```

### 2. Create Auth Configuration

Create `src/lib/auth.ts`:

```typescript
import NextAuth from "next-auth";
import { PrismaAdapter } from "@auth/prisma-adapter";
import Google from "next-auth/providers/google";
import Discord from "next-auth/providers/discord";
import GitHub from "next-auth/providers/github";
import { prisma } from "@ftcmetrics/db";

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    Discord({
      clientId: process.env.DISCORD_CLIENT_ID!,
      clientSecret: process.env.DISCORD_CLIENT_SECRET!,
    }),
    GitHub({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    }),
  ],
  pages: {
    signIn: "/login",
    error: "/login",
  },
  callbacks: {
    async session({ session, user }) {
      if (session.user) {
        session.user.id = user.id;
      }
      return session;
    },
  },
  session: {
    strategy: "database",
  },
});
```

### 3. Create API Route Handler

Create `src/app/api/auth/[...nextauth]/route.ts`:

```typescript
import { handlers } from "@/lib/auth";

export const { GET, POST } = handlers;
```

### 4. Add Session Provider

Create `src/components/providers.tsx`:

```typescript
"use client";

import { SessionProvider } from "next-auth/react";

export function Providers({ children }: { children: React.ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>;
}
```

Wrap your app in `src/app/layout.tsx`:

```tsx
import { Providers } from "@/components/providers";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

## Prisma Schema Requirements

Required models for NextAuth with database sessions:

```prisma
model User {
  id            String    @id @default(cuid())
  name          String?
  email         String?   @unique
  emailVerified DateTime? @map("email_verified")
  image         String?
  createdAt     DateTime  @default(now()) @map("created_at")
  updatedAt     DateTime  @updatedAt @map("updated_at")

  accounts Account[]
  sessions Session[]

  @@map("users")
}

model Account {
  id                String  @id @default(cuid())
  userId            String  @map("user_id")
  type              String
  provider          String
  providerAccountId String  @map("provider_account_id")
  refresh_token     String? @db.Text
  access_token      String? @db.Text
  expires_at        Int?
  token_type        String?
  scope             String?
  id_token          String? @db.Text
  session_state     String?

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([provider, providerAccountId])
  @@map("accounts")
}

model Session {
  id           String   @id @default(cuid())
  sessionToken String   @unique @map("session_token")
  userId       String   @map("user_id")
  expires      DateTime

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@map("sessions")
}
```

## Environment Variables

Add to `.env`:

```bash
# NextAuth
AUTH_SECRET="generate-with-openssl-rand-base64-32"

# Google OAuth
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"

# Discord OAuth
DISCORD_CLIENT_ID="your-discord-client-id"
DISCORD_CLIENT_SECRET="your-discord-client-secret"

# GitHub OAuth
GITHUB_CLIENT_ID="your-github-client-id"
GITHUB_CLIENT_SECRET="your-github-client-secret"
```

Generate AUTH_SECRET:

```bash
openssl rand -base64 32
```

## Session Management Patterns

### Server Components (Recommended)

Use the `auth()` function directly in Server Components:

```tsx
import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await auth();

  if (!session?.user) {
    redirect("/login");
  }

  return <div>Welcome, {session.user.name}</div>;
}
```

### Protected Layouts

Protect entire route groups with layout-level auth:

```tsx
import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";

export default async function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();

  if (!session?.user) {
    redirect("/login");
  }

  return <>{children}</>;
}
```

### Client Components

Use the `useSession` hook in Client Components:

```tsx
"use client";

import { useSession, signOut } from "next-auth/react";

export function UserMenu() {
  const { data: session, status } = useSession();

  if (status === "loading") {
    return <div>Loading...</div>;
  }

  if (!session?.user) {
    return <a href="/login">Sign in</a>;
  }

  return (
    <div>
      <img src={session.user.image} alt={session.user.name} />
      <span>{session.user.name}</span>
      <button onClick={() => signOut({ callbackUrl: "/" })}>
        Sign out
      </button>
    </div>
  );
}
```

### Sign In with Providers

```tsx
"use client";

import { signIn } from "next-auth/react";

export function LoginButtons() {
  return (
    <div>
      <button onClick={() => signIn("google", { callbackUrl: "/dashboard" })}>
        Continue with Google
      </button>
      <button onClick={() => signIn("discord", { callbackUrl: "/dashboard" })}>
        Continue with Discord
      </button>
      <button onClick={() => signIn("github", { callbackUrl: "/dashboard" })}>
        Continue with GitHub
      </button>
    </div>
  );
}
```

## Adding User ID to Session

The session callback extends the session with the database user ID:

```typescript
callbacks: {
  async session({ session, user }) {
    if (session.user) {
      session.user.id = user.id;
    }
    return session;
  },
},
```

Access the user ID in components:

```tsx
// Server Component
const session = await auth();
const userId = session?.user?.id;

// Client Component
const { data: session } = useSession();
const userId = session?.user?.id;
```

## OAuth Provider Setup

### Google

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create OAuth 2.0 credentials
3. Add authorized redirect URI: `http://localhost:3000/api/auth/callback/google`

### Discord

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create application and OAuth2 credentials
3. Add redirect URI: `http://localhost:3000/api/auth/callback/discord`

### GitHub

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Create OAuth App
3. Add callback URL: `http://localhost:3000/api/auth/callback/github`

## Common Pitfalls

### Session Not Available

- Ensure `SessionProvider` wraps your entire app in the root layout
- Ensure the API route exists at `app/api/auth/[...nextauth]/route.ts`

### User ID Missing from Session

- Add the session callback to include `user.id`
- When using database strategy, user info comes from the `user` parameter, not `token`

### Database Session Issues

- Ensure Prisma schema matches NextAuth requirements exactly
- Use `onDelete: Cascade` on relations to handle user deletion
- Run `prisma migrate dev` after schema changes

### OAuth Callback Errors

- Verify redirect URIs match exactly in provider console
- Include the full path: `/api/auth/callback/[provider]`
- For production, update URIs to use HTTPS and your domain

### AUTH_SECRET Missing

- Generate with `openssl rand -base64 32`
- Required in production, auto-generated in development

## TypeScript Type Extensions

Extend session types in `src/types/next-auth.d.ts`:

```typescript
import { DefaultSession } from "next-auth";

declare module "next-auth" {
  interface Session {
    user: {
      id: string;
    } & DefaultSession["user"];
  }
}
```

## File Structure Reference

```
packages/web/src/
  lib/
    auth.ts                           # NextAuth configuration
  components/
    providers.tsx                     # SessionProvider wrapper
  app/
    api/auth/[...nextauth]/
      route.ts                        # API route handler
    layout.tsx                        # Root layout with Providers
    login/
      page.tsx                        # Login page (server)
      login-form.tsx                  # OAuth buttons (client)
    dashboard/
      layout.tsx                      # Protected layout
      page.tsx                        # Uses auth() for session
```

## References

- [NextAuth.js v5 Documentation](https://authjs.dev)
- [Prisma Adapter](https://authjs.dev/getting-started/adapters/prisma)
- [OAuth Providers](https://authjs.dev/getting-started/providers)
