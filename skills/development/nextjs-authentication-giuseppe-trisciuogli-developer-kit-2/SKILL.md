---
name: nextjs-authentication
description: Provides authentication implementation patterns for Next.js 15+ App Router using Auth.js 5 (NextAuth.js). Use when setting up authentication flows, implementing protected routes, managing sessions in Server Components and Server Actions, configuring OAuth providers, implementing role-based access control, or handling sign-in/sign-out flows in Next.js applications.
allowed-tools: Read, Write, Edit, Bash
---

# Next.js Authentication

## Overview

This skill provides comprehensive authentication patterns for Next.js 15+ applications using the App Router architecture and Auth.js 5. It covers the complete authentication lifecycle from initial setup to production-ready implementations with role-based access control.

Key capabilities include:
- Auth.js 5 setup with Next.js App Router
- Protected routes using Middleware
- Session management in Server Components
- Authentication checks in Server Actions
- OAuth provider integration (GitHub, Google, etc.)
- Role-based access control (RBAC)
- JWT and database session strategies
- Comprehensive testing patterns

## When to Use

Use this skill when implementing authentication for Next.js 15+ with App Router:

- Setting up Auth.js 5 (NextAuth.js) from scratch
- Implementing protected routes with Middleware
- Handling authentication in Server Components
- Securing Server Actions with auth checks
- Configuring OAuth providers (Google, GitHub, Discord, etc.)
- Implementing role-based access control (RBAC)
- Managing sessions with JWT or database strategy
- Creating credential-based authentication
- Handling sign-in/sign-out flows
- Testing authentication flows

## Instructions

### 1. Install Dependencies

Install Auth.js v5 (beta) for Next.js App Router:

```bash
npm install next-auth@beta
```

### 2. Configure Environment Variables

Create `.env.local` with required variables:

```bash
# Required for Auth.js
AUTH_SECRET="your-secret-key-here"
AUTH_URL="http://localhost:3000"

# OAuth Providers (add as needed)
GITHUB_ID="your-github-client-id"
GITHUB_SECRET="your-github-client-secret"
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"
```

Generate `AUTH_SECRET` with:
```bash
openssl rand -base64 32
```

### 3. Create Auth Configuration

Create `auth.ts` in the project root with providers and callbacks:

```typescript
import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";
import Google from "next-auth/providers/google";

export const {
  handlers: { GET, POST },
  auth,
  signIn,
  signOut,
} = NextAuth({
  providers: [
    GitHub({
      clientId: process.env.GITHUB_ID!,
      clientSecret: process.env.GITHUB_SECRET!,
    }),
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      if (token) {
        session.user.id = token.id as string;
      }
      return session;
    },
  },
  pages: {
    signIn: "/login",
    error: "/error",
  },
});
```

### 4. Create API Route Handler

Create `app/api/auth/[...nextauth]/route.ts`:

```typescript
export { GET, POST } from "@/auth";
```

### 5. Add Middleware for Route Protection

Create `middleware.ts` in the project root:

```typescript
import { auth } from "@/auth";
import { NextResponse } from "next/server";

export default auth((req) => {
  const { nextUrl } = req;
  const isLoggedIn = !!req.auth;
  const isApiAuthRoute = nextUrl.pathname.startsWith("/api/auth");
  const isPublicRoute = ["/", "/login", "/register"].includes(nextUrl.pathname);
  const isProtectedRoute = nextUrl.pathname.startsWith("/dashboard");

  if (isApiAuthRoute) return NextResponse.next();

  if (!isLoggedIn && isProtectedRoute) {
    return NextResponse.redirect(new URL("/login", nextUrl));
  }

  if (isLoggedIn && nextUrl.pathname === "/login") {
    return NextResponse.redirect(new URL("/dashboard", nextUrl));
  }

  return NextResponse.next();
});

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|.*\\.png$).*)"],
};
```

### 6. Access Session in Server Components

Use the `auth()` function to access session in Server Components:

```tsx
import { auth } from "@/auth";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await auth();

  if (!session) {
    redirect("/login");
  }

  return (
    <div>
      <h1>Welcome, {session.user.name}</h1>
    </div>
  );
}
```

### 7. Secure Server Actions

Always verify authentication in Server Actions before mutations:

```tsx
"use server";

import { auth } from "@/auth";

export async function createTodo(formData: FormData) {
  const session = await auth();

  if (!session?.user) {
    throw new Error("Unauthorized");
  }

  // Proceed with protected action
  const title = formData.get("title") as string;
  await db.todo.create({
    data: { title, userId: session.user.id },
  });
}
```

### 8. Handle Sign-In/Sign-Out

Create a login page with server action:

```tsx
// app/login/page.tsx
import { signIn } from "@/auth";
import { redirect } from "next/navigation";

export default function LoginPage() {
  async function handleLogin(formData: FormData) {
    "use server";

    const result = await signIn("credentials", {
      email: formData.get("email"),
      password: formData.get("password"),
      redirect: false,
    });

    if (result?.error) {
      return { error: "Invalid credentials" };
    }

    redirect("/dashboard");
  }

  return (
    <form action={handleLogin}>
      <input name="email" type="email" placeholder="Email" required />
      <input name="password" type="password" placeholder="Password" required />
      <button type="submit">Sign In</button>
    </form>
  );
}
```

For client-side sign-out:

```tsx
"use client";

import { signOut } from "next-auth/react";

export function SignOutButton() {
  return <button onClick={() => signOut()}>Sign Out</button>;
}
```

### 9. Implement Role-Based Access

Check roles in Server Components:

```tsx
import { auth } from "@/auth";
import { unauthorized } from "next/navigation";

export default async function AdminPage() {
  const session = await auth();

  if (session?.user?.role !== "admin") {
    unauthorized();
  }

  return <AdminDashboard />;
}
```

### 10. Extend TypeScript Types

Create `types/next-auth.d.ts` for type-safe sessions:

```typescript
import { DefaultSession } from "next-auth";

declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      role: "user" | "admin";
    } & DefaultSession["user"];
  }

  interface User {
    role?: "user" | "admin";
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    id?: string;
    role?: "user" | "admin";
  }
}
```

## Examples

### Example 1: Complete Protected Dashboard

**Input:** User needs a dashboard accessible only to authenticated users

**Implementation:**

```tsx
// app/dashboard/page.tsx
import { auth } from "@/auth";
import { redirect } from "next/navigation";
import { getUserTodos } from "@/app/lib/data";

export default async function DashboardPage() {
  const session = await auth();

  if (!session?.user?.id) {
    redirect("/login");
  }

  const todos = await getUserTodos(session.user.id);

  return (
    <main>
      <h1>Welcome, {session.user.name}</h1>
      <p>Email: {session.user.email}</p>
      <TodoList todos={todos} />
    </main>
  );
}
```

**Output:** Dashboard renders only for authenticated users, with their specific data.

### Example 2: Role-Based Admin Panel

**Input:** Admin panel should be accessible only to users with "admin" role

**Implementation:**

```tsx
// app/admin/page.tsx
import { auth } from "@/auth";
import { unauthorized } from "next/navigation";

export default async function AdminPage() {
  const session = await auth();

  if (session?.user?.role !== "admin") {
    unauthorized();
  }

  return (
    <main>
      <h1>Admin Panel</h1>
      <p>Welcome, administrator {session.user.name}</p>
    </main>
  );
}
```

**Output:** Only admin users see the panel; others get 401 error.

### Example 3: Secure Server Action with Form

**Input:** Form submission should only work for authenticated users

**Implementation:**

```tsx
// app/components/create-todo-form.tsx
"use server";

import { auth } from "@/auth";
import { revalidatePath } from "next/cache";

export async function createTodo(formData: FormData) {
  const session = await auth();

  if (!session?.user?.id) {
    throw new Error("Unauthorized");
  }

  const title = formData.get("title") as string;

  await db.todo.create({
    data: {
      title,
      userId: session.user.id,
    },
  });

  revalidatePath("/dashboard");
}

// Usage in component
export function CreateTodoForm() {
  return (
    <form action={createTodo}>
      <input name="title" placeholder="New todo..." required />
      <button type="submit">Add Todo</button>
    </form>
  );
}
```

**Output:** Todo created only for authenticated user; unauthorized requests throw error.

### Example 4: OAuth Sign-In Button

**Input:** User should be able to sign in with GitHub

**Implementation:**

```tsx
// components/auth/sign-in-button.tsx
"use client";

import { signIn, signOut, useSession } from "next-auth/react";

export function AuthButton() {
  const { data: session, status } = useSession();

  if (status === "loading") {
    return <button disabled>Loading...</button>;
  }

  if (session) {
    return (
      <button onClick={() => signOut()}>
        Sign out {session.user?.name}
      </button>
    );
  }

  return (
    <button onClick={() => signIn("github")}>
      Sign in with GitHub
    </button>
  );
}
```

**Output:** Button shows "Sign in with GitHub" for unauthenticated users, "Sign out {name}" for authenticated users.

### Example 5: Credentials Provider Login

**Input:** Implement email/password login

**Implementation:**

```tsx
// auth.ts
import Credentials from "next-auth/providers/credentials";
import bcrypt from "bcryptjs";

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    Credentials({
      name: "credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null;
        }

        const user = await db.user.findUnique({
          where: { email: credentials.email },
        });

        if (!user || !user.password) {
          return null;
        }

        const isValid = await bcrypt.compare(
          credentials.password,
          user.password
        );

        return isValid
          ? { id: user.id, email: user.email, name: user.name }
          : null;
      },
    }),
  ],
});
```

**Output:** Users can authenticate with email/password against your database.

## Best Practices

1. **Use Server Components by default** - Access session directly without client-side JavaScript
2. **Minimize Client Components** - Only use `useSession()` for reactive session updates
3. **Cache session checks** - Use React's `cache()` for repeated lookups in the same render
4. **Middleware for optimistic checks** - Redirect quickly, but always re-verify in Server Actions
5. **Treat Server Actions like API endpoints** - Always authenticate before mutations
6. **Never hardcode secrets** - Use environment variables for all credentials
7. **Implement proper error handling** - Return appropriate HTTP status codes
8. **Use TypeScript type extensions** - Extend NextAuth types for custom fields
9. **Separate auth logic** - Create a DAL (Data Access Layer) for consistent checks
10. **Test authentication flows** - Mock `auth()` function in unit tests

## Constraints and Warnings

### Critical Limitations

- **Middleware runs on Edge runtime** - Cannot use Node.js APIs like database drivers
- **Server Components cannot set cookies** - Use Server Actions for cookie operations
- **Session callback timing** - Only called on session creation/access, not every request

### Common Mistakes

```tsx
// ❌ WRONG: Setting cookies in Server Component
export default async function Page() {
  cookies().set("key", "value"); // Won't work
}

// ✅ CORRECT: Use Server Action
async function setCookieAction() {
  "use server";
  cookies().set("key", "value");
}
```

```typescript
// ❌ WRONG: Database queries in Middleware
export default auth(async (req) => {
  const user = await db.user.findUnique(); // Won't work in Edge
});

// ✅ CORRECT: Use only Edge-compatible APIs
export default auth(async (req) => {
  const session = req.auth; // This works
});
```

### Security Considerations

- Always verify authentication in Server Actions - middleware alone is not enough
- Use `unauthorized()` for unauthenticated access, `redirect()` for other cases
- Store sensitive tokens in `httpOnly` cookies
- Validate all user input before processing
- Use HTTPS in production
- Set appropriate cookie `sameSite` attributes

## References

- [references/authjs-setup.md](references/authjs-setup.md) - Complete Auth.js 5 setup guide with Prisma/Drizzle adapters
- [references/oauth-providers.md](references/oauth-providers.md) - Provider-specific configurations (GitHub, Google, Discord, Auth0, etc.)
- [references/database-adapter.md](references/database-adapter.md) - Database session management with Prisma, Drizzle, and custom adapters
- [references/testing-patterns.md](references/testing-patterns.md) - Testing authentication flows with Vitest and Playwright
