---
name: vite-2-next
description: Zero-downtime migration playbook for React+Vite+Tailwind apps to Next.js 16 App Router with modern tooling (Radix UI, shadcn/ui, TypeScript). Trigger when asked to migrate, convert, or upgrade from React/Vite to Next.js; it handles router conversion, data fetching transformation, build config migration, component refactoring, and deployment setup.
---

# Migrate React + Vite to Next.js 16

## Overview

This skill helps AI agents:

- **Audit** existing React+Vite projects (routing, state management, data fetching, dependencies)
- **Bootstrap** a parallel Next.js 16 App Router project with Tailwind, shadcn/ui, and modern tooling
- **Translate** routes, layouts, components, and data-fetching patterns into idiomatic Server/Client Components
- **Migrate** environment variables, static assets, and API routes to Next.js 16 conventions (including `proxy.ts`)
- **Optimize & deploy** using React Compiler, Turbopack, and platform-specific deployment guidance

This migration preserves UI components while transforming the underlying architecture to leverage SSR, streaming, and Server Actions.

## FIRST: Verify React Project Structure

Confirm the project is a React application by checking:

1. `react` and `react-dom` in `package.json` dependencies
2. Presence of `vite.config.ts/js`, `craco.config.js`, or `webpack.config.js`
3. Either `src/` directory with components or root-level component files

If none found, **STOP** — this skill does not apply.

Detect the package manager from the lockfile:

| Lockfile                    | Manager | Install       | Uninstall       | Execute    |
| --------------------------- | ------- | ------------- | --------------- | ---------- |
| `pnpm-lock.yaml`            | pnpm    | `pnpm add`    | `pnpm remove`   | `pnpm dlx` |
| `yarn.lock`                 | yarn    | `yarn add`    | `yarn remove`   | `yarn dlx` |
| `bun.lockb` / `bun.lock`    | bun     | `bun add`     | `bun remove`    | `bunx`     |
| `package-lock.json` or none | npm     | `npm install` | `npm uninstall` | `npx`      |

Detect routing system:

- **React Router** — Check for `react-router-dom` in dependencies
- **TanStack Router** — Check for `@tanstack/react-router`
- **Wouter** — Check for `wouter`
- **No router** — Single-page app with manual navigation

## Migration Strategy Overview

| React/Vite Pattern                      | Next.js 16 App Router Equivalent              |
| --------------------------------------- | --------------------------------------------- |
| Client-side routing (`<BrowserRouter>`) | File-system routing (`app/` directory)        |
| `useEffect` data fetching               | Server Components with `async/await`          |
| `useState` for server data              | Server Actions, `useActionState`              |
| `index.html` with `<div id="root">`     | `app/layout.tsx` with `RootLayout`            |
| `import.meta.env.VITE_*`                | `process.env.NEXT_PUBLIC_*`                   |
| `middleware.ts`                         | `proxy.ts` (renamed in Next.js 16)            |
| Vite plugins for CSS/assets             | Built-in optimization + Turbopack             |
| Client-only rendering                   | Hybrid rendering (Server + Client Components) |

## Phase 1: Compatibility Audit

### 1a. Check Critical Dependencies

**Generally Compatible:** Material-UI, Ant Design, Chakra UI, Radix UI, Headless UI, Zustand, Jotai, Valtio, React Hook Form, Formik, Framer Motion, date-fns, lodash, clsx

**Requires Refactoring:** Redux/Redux Toolkit (wrap in `useRef` provider), React Query/TanStack Query (configure for SSR), Apollo Client (SSR setup), SWR (configure for SSR)

**Incompatible / Not Needed:** `react-router-dom`, Vite plugins, `react-helmet`, `dotenv`

See [references/compatibility.md](references/compatibility.md) for the full library compatibility matrix.

### 1b. Analyze Application Architecture

Categorize components by type:

1. **Page Components** — Top-level routes (Home, About, Dashboard)
2. **Layout Components** — Shared structure (Header, Sidebar, Footer)
3. **UI Components** — Reusable elements (Button, Card, Modal)
4. **Data Components** — Components with API calls/side effects
5. **Context Providers** — Global state (Theme, Auth, etc.)

## Phase 2: Project Initialization

### 2a. Create Next.js Project Alongside

> **CRITICAL**: Do not delete or modify the existing React project yet. Create Next.js in a parallel directory for gradual migration and easy rollback.

```bash
npx create-next-app@latest [project-name]-nextjs --typescript --tailwind --app --src-dir --import-alias "@/*"
```

> **Node.js 20.9.0 or later** is required for Next.js 16.

### 2b. Install Core Dependencies

```bash
[package-manager] add @radix-ui/react-slot class-variance-authority clsx tailwind-merge
[package-manager-exec] shadcn@latest init
[package-manager] add lucide-react zod react-hook-form @hookform/resolvers
```

### 2c. Copy Tailwind Configuration

See [references/tailwind-migration.md](references/tailwind-migration.md) for detailed examples.

## Phase 3: Core File Structure Migration

### 3a. Convert Routing Structure

| React Router                                      | Next.js App Router                     |
| ------------------------------------------------- | -------------------------------------- |
| `<Route path="/" element={<Home />} />`           | `app/page.tsx`                         |
| `<Route path="/about" element={<About />} />`     | `app/about/page.tsx`                   |
| `<Route path="/blog/:slug" element={<Post />} />` | `app/blog/[slug]/page.tsx`             |
| `<Route path="/blog/*" element={<Blog />} />`     | `app/blog/[...slug]/page.tsx`          |
| `<Outlet />` in layout                            | `{children}` in `layout.tsx`           |
| `<Navigate to="/" />`                             | `redirect('/')` from `next/navigation` |

> **Next.js 16**: `params` and `searchParams` are **async Promises** — always `await` them.

```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPost({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  return <h1>{slug}</h1>;
}
```

See [references/routing-patterns.md](references/routing-patterns.md) for complex routing scenarios.

### 3b. Convert Root Layout

**Before (React):**

```tsx
// src/App.tsx
function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Header />
        <Routes>{/* routes */}</Routes>
        <Footer />
      </BrowserRouter>
    </ThemeProvider>
  );
}
```

**After (Next.js 16):**

```tsx
// src/app/layout.tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/providers/theme-provider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "My App",
  description: "App description",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
```

### 3c. Migrate Components

**Conversion rules:**

- No hooks, no events, no browser APIs → **Server Component** (no directive needed)
- Has `useState` / `useEffect` / event handlers → Add `'use client'`
- Uses React Context → Wrap in a `'use client'` Provider
- Uses `React.lazy` → Replace with `next/dynamic`
- Uses `<a>` for internal links → Replace with `next/link`
- Uses `useNavigate` → Replace with `useRouter` from `next/navigation`

See [references/component-patterns.md](references/component-patterns.md) for detailed examples.

## Phase 4: Data Fetching Transformation

### 4a. Replace useEffect with Server Components

**Before (React):**

```tsx
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then((res) => res.json())
      .then((data) => {
        setUser(data);
        setLoading(false);
      });
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  return <div>{user.name}</div>;
}
```

**After (Next.js 16 — Server Component):**

```tsx
async function UserProfile({ userId }: { userId: string }) {
  const user = await fetch(`https://api.example.com/users/${userId}`).then(
    (res) => res.json(),
  );
  return <div>{user.name}</div>;
}
```

### 4b. Caching in Next.js 16

Everything is **dynamic by default**. To opt into caching, use the `"use cache"` directive:

```tsx
"use cache";
export default async function ProductsPage() {
  const products = await fetch("https://api.example.com/products").then((r) =>
    r.json(),
  );
  return <ProductList products={products} />;
}
```

> The old `fetch(url, { next: { revalidate: 60 } })` and `cache: 'force-cache'` patterns are **deprecated** in Next.js 16. Use `"use cache"` instead.

### 4c. Server Actions for Mutations

```tsx
// app/posts/create/actions.ts
"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

export async function createPost(formData: FormData) {
  const title = formData.get("title") as string;
  await fetch("https://api.example.com/posts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  revalidatePath("/posts");
  redirect("/posts");
}

// app/posts/create/page.tsx
import { createPost } from "./actions";

export default function CreatePostPage() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <button type="submit">Submit</button>
    </form>
  );
}
```

See [references/data-fetching.md](references/data-fetching.md) for comprehensive patterns.

## Phase 5: Environment Variables

| Vite                           | Next.js 16                        | Scope           |
| ------------------------------ | --------------------------------- | --------------- |
| `import.meta.env.VITE_API_URL` | `process.env.NEXT_PUBLIC_API_URL` | Client + Server |
| `import.meta.env.VITE_*`       | `process.env.NEXT_PUBLIC_*`       | Client + Server |
| `process.env.*` (server)       | `process.env.*`                   | Server only     |

See [references/environment.md](references/environment.md) for detailed configuration.

## Phase 6: Static Assets

Move `src/assets/` → `public/`. See [references/assets.md](references/assets.md) for optimization.

## Phase 7: State Management

Context providers must be `'use client'`. All global stores (Zustand, Redux, Jotai) must use a `useRef`-based provider — never module-level singletons — to prevent state leaking between server requests.

See [references/state-management.md](references/state-management.md) for detailed patterns.

## Phase 8: API Routes and Proxy

### Route Handlers

```ts
// app/api/posts/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function GET() {
  const posts = await db.posts.findMany();
  return NextResponse.json(posts);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const post = await db.posts.create({ data: body });
  return NextResponse.json(post, { status: 201 });
}
```

> Dynamic route `params` are async in Next.js 16: `{ params }: { params: Promise<{ id: string }> }` — always `await params`.

### proxy.ts (replaces middleware.ts)

```ts
// proxy.ts  ← was middleware.ts in Next.js 13–15
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  return NextResponse.next();
}

export const config = { matcher: ["/dashboard/:path*"] };
```

See [references/api-routes.md](references/api-routes.md) for comprehensive examples.

## Phase 9: Build Configuration

### next.config.ts

```ts
import type { NextConfig } from "next";

const config: NextConfig = {
  // React Compiler — stable in Next.js 16
  reactCompiler: true,

  experimental: {
    // Turbopack persistent FS cache — faster cold starts
    turbopackFileSystemCacheForDev: true,
  },

  images: {
    remotePatterns: [{ protocol: "https", hostname: "**.example.com" }],
  },

  async redirects() {
    return [{ source: "/old-path", destination: "/new-path", permanent: true }];
  },
};

export default config;
```

> Turbopack is the **default bundler** in Next.js 16. Custom webpack configs will not work — rewrite for Turbopack or `next.config.ts`.

See [references/config-options.md](references/config-options.md) for all available options.

## Phase 10: Testing and Validation

### Feature Parity Checklist

- [ ] All routes render correctly
- [ ] Navigation between pages works
- [ ] Forms submit and handle validation
- [ ] Data fetching displays correct content
- [ ] Authentication flow works
- [ ] Protected routes redirect properly
- [ ] Search, filtering, and sorting work
- [ ] Dark mode / theme switching works
- [ ] Responsive design intact
- [ ] Third-party scripts load

### Common Migration Issues

See [references/troubleshooting.md](references/troubleshooting.md) for solutions.

## Phase 11: Deployment

**Vercel (Recommended):**

```bash
npm install -g vercel && vercel login && vercel
```

**Alternatives:** Netlify, Cloudflare Pages (`@cloudflare/next-on-pages`), AWS Amplify, Docker, Node.js server.

See [references/deployment.md](references/deployment.md) for platform-specific guides.

## Phase 12: Post-Migration Optimization

Convert Client Components to Server Components where possible. Use `loading.tsx` and `<Suspense>` for streaming. Add `generateMetadata` for SEO. Use parallel `Promise.all()` fetching.

See [references/optimization.md](references/optimization.md) for advanced techniques.

## Anti-Patterns and Common Mistakes

**Do NOT:**

- Use `useEffect` for data fetching in Server Components
- Add `'use client'` to every file by default
- Import Server Components into Client Components
- Use `window`, `localStorage`, `document` in Server Components
- Use `next: { revalidate }` or `cache: 'force-cache'` — use `"use cache"` directive instead
- Call `cookies()` or `headers()` synchronously — they are **async** in Next.js 16
- Use a file named `middleware.ts` — it is now `proxy.ts` in Next.js 16
- Use module-level store singletons — always wrap in `useRef`-based providers

**DO:**

- Default to Server Components
- Add `'use client'` only when needed
- Use Server Actions for mutations
- Leverage `next/image`, `next/font`, `next/script`
- Always `await params`, `await cookies()`, `await headers()`
- Follow App Router conventions: `layout`, `loading`, `error`, `not-found`

## Success Criteria

- All pages accessible via Next.js routes
- Build completes without errors
- Lighthouse scores improved (FCP, LCP, TTFB)
- No console errors
- Production deployment successful

**Complexity estimate:**

- **Simple** — <10 routes, basic data fetching (2–4 hours)
- **Moderate** — Multiple routes, React Query/SWR, some global state (1–2 days)
- **Complex** — 20+ routes, Redux, complex auth, many integrations (3–7 days)
