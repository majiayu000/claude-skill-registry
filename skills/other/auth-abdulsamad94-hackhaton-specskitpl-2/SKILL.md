---
name: Authentication Logic
description: Guide to using Better Auth for client and server-side authentication.
---

# Authentication Logic

## Overview
We use **Better Auth** (`better-auth`) for identifying users.

## Config
- **Client**: `lib/auth-client.ts` exports `authClient`.
- **Server**: `lib/auth.ts` exports `auth`.

## Client-Side Usage
Use `authClient` for signing in, signing out, and checking session state in Client Components.

```tsx
import { authClient } from "@/lib/auth-client";

// Sign In
await authClient.signIn.email({
  email,
  password,
});

// Social Sign In
await authClient.signIn.social({
  provider: "google",
  callbackURL: "/onboarding", 
});

// Sign Out
await authClient.signOut();
```

## Server-Side Usage
Use `auth.api.getSession` for protecting API routes or Server Actions.

```ts
import { auth } from "@/lib/auth";
import { headers } from "next/headers";

const session = await auth.api.getSession({
  headers: await headers()
});

if (!session) {
  return new Response("Unauthorized", { status: 401 });
}
```

## AuthBar Component
- Located at `textbook/src/components/AuthBar/index.tsx`.
- Displays user avatar or login button.
- Fetches session from `/api/auth/session` (Next.js API route proxying Better Auth).
