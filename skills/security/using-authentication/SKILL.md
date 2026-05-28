---
name: using-authentication
description: Use Better Auth for client and server-side authentication. Covers session access, protected routes, sign in/out, and fetching user data.
---

# Working with Authentication

Use Better Auth for client and server-side authentication. Covers session access, protected routes, sign in/out, and fetching user data.

## Implement Working with Authentication

Use Better Auth for client and server-side authentication. Covers session access, protected routes, sign in/out, and fetching user data.

**See:**

- Resource: `using-authentication` in Fullstack Recipes
- URL: https://fullstackrecipes.com/recipes/using-authentication

---

### Client-Side Authentication

Use the auth client hooks in React components:

```tsx
"use client";

import { useSession, signOut } from "@/lib/auth/client";

export function UserMenu() {
  const { data: session, isPending } = useSession();

  if (isPending) return <div>Loading...</div>;
  if (!session) return <a href="/sign-in">Sign In</a>;

  return (
    <div>
      <span>{session.user.name}</span>
      <button onClick={() => signOut()}>Sign Out</button>
    </div>
  );
}
```

### Server-Side Session Access

Get the session in Server Components and API routes:

```typescript
import { auth } from "@/lib/auth/server";
import { headers } from "next/headers";

// In a Server Component
export default async function Page() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) {
    return <div>Not signed in</div>;
  }

  return <div>Hello, {session.user.name}</div>;
}
```

```typescript
// In an API route
export async function POST(request: Request) {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) {
    return new Response("Unauthorized", { status: 401 });
  }

  // Use session.user.id for queries...
}
```

### Protected Pages Pattern

Redirect unauthenticated users:

```tsx
import { redirect } from "next/navigation";
import { headers } from "next/headers";
import { auth } from "@/lib/auth/server";

export default async function ProtectedPage() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) {
    redirect("/sign-in");
  }

  return <Dashboard user={session.user} />;
}
```

### Auth Pages Pattern

Redirect authenticated users away from auth pages:

```tsx
import { redirect } from "next/navigation";
import { headers } from "next/headers";
import { auth } from "@/lib/auth/server";

export default async function SignInPage() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (session) {
    redirect("/chats"); // Already signed in
  }

  return <SignIn />;
}
```

### Signing In

```typescript
import { signIn } from "@/lib/auth/client";

// Email/password
await signIn.email({
  email: "user@example.com",
  password: "password",
  callbackURL: "/chats",
});

// Social provider
await signIn.social({
  provider: "google",
  callbackURL: "/chats",
});
```

### Signing Up

```typescript
import { signUp } from "@/lib/auth/client";

await signUp.email({
  email: "user@example.com",
  password: "password",
  name: "John Doe",
  callbackURL: "/verify-email",
});
```

### Signing Out

```typescript
import { signOut } from "@/lib/auth/client";

await signOut({
  fetchOptions: {
    onSuccess: () => {
      router.push("/");
    },
  },
});
```

### Fetching User Data After Auth

In protected pages, fetch user-specific data after validating the session:

```tsx
export default async function DashboardPage() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) {
    redirect("/sign-in");
  }

  const [chats, profile] = await Promise.all([
    getUserChats(session.user.id),
    getUserProfile(session.user.id),
  ]);

  return <Dashboard chats={chats} profile={profile} />;
}
```

---

## References

- [Better Auth React](https://www.better-auth.com/docs/react)
- [Better Auth Server](https://www.better-auth.com/docs/server)
