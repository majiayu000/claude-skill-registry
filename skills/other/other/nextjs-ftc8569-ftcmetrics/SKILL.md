---
name: nextjs
description: >-
  Next.js 16 App Router patterns for FTC Metrics. Use when creating pages,
  layouts, components, API routes, or implementing authentication flows.
license: MIT
compatibility: [Claude Code]
metadata:
  author: ftcmetrics
  version: "1.0.0"
  category: frontend
---

# Next.js 16 App Router Skill

Patterns for the FTC Metrics Next.js frontend at `packages/web/`.

## Quick Start

```bash
cd packages/web
bun dev          # http://localhost:3000
bun typecheck    # Type check
bun lint         # Lint
```

## Project Structure

```
packages/web/src/
  app/                      # App Router pages and layouts
    layout.tsx              # Root layout with Providers
    page.tsx                # Landing page (Server Component)
    dashboard/layout.tsx    # Auth-protected layout
    analytics/page.tsx      # Client Component with Suspense
    analytics/team/[teamNumber]/  # Dynamic route
    api/auth/[...nextauth]/ # Auth API routes
  components/
    providers.tsx           # Client-side providers wrapper
    header.tsx              # Navigation header
  lib/
    auth.ts                 # NextAuth v5 configuration
    api.ts                  # API client utilities
  types/next-auth.d.ts      # Session type augmentation
```

## Key Concepts

| Concept | Pattern | Location |
|---------|---------|----------|
| Server Components | Default, no directive | `app/page.tsx` |
| Client Components | `"use client"` directive | `components/header.tsx` |
| Protected Routes | `auth()` check in layout | `app/dashboard/layout.tsx` |
| Dynamic Routes | `[param]` folder naming | `app/analytics/team/[teamNumber]/` |
| API Routes | Route handlers | `app/api/auth/[...nextauth]/route.ts` |

## Common Patterns

### 1. Root Layout with Providers

```tsx
// app/layout.tsx
import { Providers } from "@/components/providers";
import "./globals.css";

export const metadata = {
  title: "FTC Metrics",
  description: "Scouting platform for FIRST Tech Challenge",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-background antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

```tsx
// components/providers.tsx
"use client";
import { SessionProvider } from "next-auth/react";

export function Providers({ children }: { children: React.ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>;
}
```

### 2. Protected Layout with Auth Check

```tsx
// app/dashboard/layout.tsx
import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";
import { Header } from "@/components/header";

export default async function DashboardLayout({ children }: { children: React.ReactNode }) {
  const session = await auth();
  if (!session?.user) redirect("/login");

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">{children}</main>
    </div>
  );
}
```

### 3. Server Component with Auth

```tsx
// app/dashboard/page.tsx
import { auth } from "@/lib/auth";

export default async function DashboardPage() {
  const session = await auth();
  return <h1>Welcome, {session?.user?.name?.split(" ")[0] || "Scout"}</h1>;
}
```

### 4. Client Component with useSearchParams (Suspense Required)

```tsx
// app/analytics/page.tsx
"use client";
import { Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";

function AnalyticsContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const eventCode = searchParams.get("event") || "";

  const handleEventChange = (event: string) => {
    router.push(`/analytics?event=${event}`, { scroll: false });
  };

  return <div>{/* Content */}</div>;
}

export default function AnalyticsPage() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <AnalyticsContent />
    </Suspense>
  );
}
```

### 5. Dynamic Route with Params

```tsx
// app/analytics/team/[teamNumber]/page.tsx
"use client";
import { useParams, useSearchParams } from "next/navigation";
import { Suspense } from "react";

function TeamContent() {
  const params = useParams();
  const searchParams = useSearchParams();
  const teamNumber = parseInt(params.teamNumber as string, 10);
  const eventCode = searchParams.get("event") || "";
  return <h1>Team {teamNumber}</h1>;
}

export default function TeamPage() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <TeamContent />
    </Suspense>
  );
}
```

### 6. NextAuth v5 Configuration

```tsx
// lib/auth.ts
import NextAuth from "next-auth";
import { PrismaAdapter } from "@auth/prisma-adapter";
import Google from "next-auth/providers/google";
import { prisma } from "@ftcmetrics/db";

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  pages: { signIn: "/login", error: "/login" },
  callbacks: {
    async session({ session, user }) {
      if (session.user) session.user.id = user.id;
      return session;
    },
  },
  session: { strategy: "database" },
});
```

```tsx
// app/api/auth/[...nextauth]/route.ts
import { handlers } from "@/lib/auth";
export const { GET, POST } = handlers;
```

### 7. Session Type Augmentation

```tsx
// types/next-auth.d.ts
import { DefaultSession } from "next-auth";

declare module "next-auth" {
  interface Session {
    user: { id: string } & DefaultSession["user"];
  }
}
```

### 8. Client Component with useSession

```tsx
// components/header.tsx
"use client";
import { useSession, signOut } from "next-auth/react";
import Link from "next/link";

export function Header() {
  const { data: session } = useSession();

  return (
    <header>
      {session?.user ? (
        <button onClick={() => signOut({ callbackUrl: "/" })}>Sign out</button>
      ) : (
        <Link href="/login">Sign in</Link>
      )}
    </header>
  );
}
```

### 9. Redirect Based on Auth State

```tsx
// app/page.tsx
import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";

export default async function Home() {
  const session = await auth();
  if (session?.user) redirect("/dashboard");
  return <LandingPage />;
}
```

## Anti-Patterns

### Using auth() in Client Components

```tsx
// Server Component - uses auth()
export default async function Page() {
  const session = await auth();
  return <Display user={session?.user} />;
}

// Client Component - uses useSession hook
"use client";
import { useSession } from "next-auth/react";

export function UserProfile() {
  const { data: session, status } = useSession();
  if (status === "loading") return <Skeleton />;
  return <Profile user={session?.user} />;
}
```

### useSearchParams Without Suspense

```tsx
// WRONG: Will cause hydration errors
"use client";
export default function SearchPage() {
  const params = useSearchParams(); // No Suspense wrapper
  return <Results query={params.get("q")} />;
}

// CORRECT: Wrap in Suspense
"use client";
function SearchContent() {
  const params = useSearchParams();
  return <Results query={params.get("q")} />;
}

export default function SearchPage() {
  return (
    <Suspense fallback={<Loading />}>
      <SearchContent />
    </Suspense>
  );
}
```

### Importing signIn/signOut Wrong

```tsx
// Server actions - import from lib/auth
import { signIn, signOut } from "@/lib/auth";

// Client components - import from next-auth/react
"use client";
import { signIn, signOut } from "next-auth/react";
```

## Tailwind Configuration

```ts
// tailwind.config.ts
const config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        ftc: {
          orange: "#f57e25",  // Primary: text-ftc-orange, bg-ftc-orange
          blue: "#0066b3",    // Secondary: text-ftc-blue, bg-ftc-blue
          dark: "#1a1a2e",    // Dark: bg-ftc-dark
        },
      },
    },
  },
};
```

## Next.js Configuration

```ts
// next.config.ts
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ["@ftcmetrics/shared"],  // Monorepo packages
};
```

## Monorepo Integration

```tsx
// Workspace packages
import { prisma } from "@ftcmetrics/db";
import { TeamType } from "@ftcmetrics/shared";

// Local imports with @/ alias
import { auth } from "@/lib/auth";
import { Header } from "@/components/header";
```

## Loading Spinner Pattern

Used throughout the codebase:

```tsx
<div className="flex items-center justify-center py-12">
  <div className="animate-spin rounded-full h-8 w-8 border-2 border-ftc-orange border-t-transparent" />
</div>
```

## References

- [Next.js 16 Docs](https://nextjs.org/docs)
- [NextAuth.js v5](https://authjs.dev)
- [FTC Events API](https://ftc-events.firstinspires.org/services/API)
