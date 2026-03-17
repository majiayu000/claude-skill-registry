---
name: tanstack-start
description: "Build a full-stack TanStack Start app on Cloudflare Workers from scratch — SSR, file-based routing, server functions, D1+Drizzle, better-auth, Tailwind v4+shadcn/ui. No template repo — Claude generates every file fresh per project."
compatibility: claude-code-only
---

# TanStack Start on Cloudflare

Build a complete full-stack app from nothing. Claude generates every file — no template clone, no scaffold command. Each project gets exactly what it needs.

## What You Get

| Layer | Technology |
|-------|-----------|
| Framework | TanStack Start v1 (SSR, file-based routing, server functions) |
| Frontend | React 19, Tailwind v4, shadcn/ui |
| Backend | Server functions (via Nitro on Cloudflare Workers) |
| Database | D1 + Drizzle ORM |
| Auth | better-auth (Google OAuth + email/password) |
| Deployment | Cloudflare Workers |

## Workflow

### Step 1: Gather Project Info

Ask for:

| Required | Optional |
|----------|----------|
| Project name (kebab-case) | Google OAuth credentials |
| One-line description | Custom domain |
| Cloudflare account | R2 storage needed? |
| Auth method: Google OAuth, email/password, or both | Admin email |

### Step 2: Initialise Project

Create the project directory and all config files from scratch.

**See `references/architecture.md`** for the complete file tree, all dependencies, and config templates.

Create these files first:

1. **`package.json`** — all runtime + dev dependencies with version ranges from architecture.md
2. **`tsconfig.json`** — strict mode, `@/*` path alias mapped to `src/*`
3. **`vite.config.ts`** — plugins in correct order: `cloudflare()` → `tailwindcss()` → `tanstackStart()` → `viteReact()`
4. **`wrangler.jsonc`** — `main: "@tanstack/react-start/server-entry"`, `nodejs_compat` flag, D1 binding placeholder
5. **`.dev.vars`** — generate `BETTER_AUTH_SECRET` with `openssl rand -hex 32`, set `BETTER_AUTH_URL=http://localhost:3000`, `TRUSTED_ORIGINS=http://localhost:3000`
6. **`.gitignore`** — node_modules, .wrangler, dist, .output, .dev.vars, .vinxi, .DS_Store

Then:

```bash
cd PROJECT_NAME
pnpm install
```

Create D1 database and update wrangler.jsonc:

```bash
npx wrangler d1 create PROJECT_NAME-db
# Copy the database_id into wrangler.jsonc d1_databases binding
```

### Step 3: Database Schema

Create the Drizzle schema with D1-correct patterns.

**`src/db/schema.ts`** — Define all tables:

- **better-auth tables**: `users`, `sessions`, `accounts`, `verifications` — these are required by better-auth
- **Application table**: `items` (or whatever the project needs) for CRUD demo

D1-specific rules:
- Use `integer` for timestamps (Unix epoch), NOT Date objects
- Use `text` for primary keys (nanoid/cuid2), NOT autoincrement
- Keep bound parameters under 100 per query (batch large inserts)
- Foreign keys are always ON in D1

**`src/db/index.ts`** — Drizzle client factory:

```typescript
import { drizzle } from "drizzle-orm/d1";
import { env } from "cloudflare:workers";
import * as schema from "./schema";

export function getDb() {
  return drizzle(env.DB, { schema });
}
```

**CRITICAL**: Use `import { env } from "cloudflare:workers"` — NOT `process.env`. This is a per-request binding, so create the Drizzle client inside each server function, not at module level.

**`drizzle.config.ts`**:

```typescript
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./src/db/schema.ts",
  out: "./drizzle",
  dialect: "sqlite",
});
```

Add migration scripts to `package.json`:

```json
{
  "db:generate": "drizzle-kit generate",
  "db:migrate:local": "wrangler d1 migrations apply PROJECT_NAME-db --local",
  "db:migrate:remote": "wrangler d1 migrations apply PROJECT_NAME-db --remote"
}
```

Generate and apply the initial migration:

```bash
pnpm db:generate
pnpm db:migrate:local
```

### Step 4: Configure Auth

**`src/lib/auth.server.ts`** — Server-side better-auth configuration:

```typescript
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { drizzle } from "drizzle-orm/d1";
import { env } from "cloudflare:workers";
import * as schema from "../db/schema";

export function getAuth() {
  const db = drizzle(env.DB, { schema });
  return betterAuth({
    database: drizzleAdapter(db, { provider: "sqlite" }),
    secret: env.BETTER_AUTH_SECRET,
    baseURL: env.BETTER_AUTH_URL,
    trustedOrigins: env.TRUSTED_ORIGINS?.split(",") ?? [],
    emailAndPassword: { enabled: true },
    socialProviders: {
      // Add Google OAuth if credentials provided
    },
  });
}
```

**CRITICAL**: `getAuth()` must be called per-request (inside handler/loader), NOT at module level. The `env` import from `cloudflare:workers` is only available during request handling.

**`src/lib/auth.client.ts`** — Client-side auth hooks:

```typescript
import { createAuthClient } from "better-auth/react";

export const { useSession, signIn, signOut, signUp } = createAuthClient();
```

**`src/routes/api/auth/$.ts`** — API catch-all route for better-auth:

```typescript
import { createAPIFileRoute } from "@tanstack/react-start/api";
import { getAuth } from "../../../lib/auth.server";

export const APIRoute = createAPIFileRoute("/api/auth/$")({
  GET: ({ request }) => getAuth().handler(request),
  POST: ({ request }) => getAuth().handler(request),
});
```

**CRITICAL**: Auth MUST use an API route (`createAPIFileRoute`), NOT a server function (`createServerFn`). better-auth needs direct request/response access.

### Step 5: App Shell + Theme

**`src/routes/__root.tsx`** — Root layout with HTML document:

- Render full HTML document with `<HeadContent />` and `<Scripts />` from `@tanstack/react-router`
- Add `suppressHydrationWarning` on `<html>` for SSR + theme toggle compatibility
- Import the global CSS file
- Include theme initialisation script inline to prevent flash of wrong theme

**`src/styles/app.css`** — Tailwind v4 + shadcn/ui:

- `@import "tailwindcss"` (v4 syntax)
- CSS variables for shadcn/ui tokens in `:root` and `.dark`
- Neutral/monochrome palette (stone, slate, zinc)
- Use semantic tokens only — never raw Tailwind colours

**`src/router.tsx`** — Router configuration:

```typescript
import { createRouter as createTanStackRouter } from "@tanstack/react-router";
import { routeTree } from "./routeTree.gen";

export function createRouter() {
  return createTanStackRouter({ routeTree });
}

declare module "@tanstack/react-router" {
  interface Register {
    router: ReturnType<typeof createRouter>;
  }
}
```

**`src/client.tsx`** and **`src/ssr.tsx`** — Entry points (standard TanStack Start boilerplate).

Install shadcn/ui components needed for the dashboard:

```bash
pnpm dlx shadcn@latest init --defaults
pnpm dlx shadcn@latest add button card input label sidebar table dropdown-menu form separator sheet
```

**Note**: Configure shadcn to use `src/components` as the components directory.

Theme toggle: three-state (light → dark → system → light). Store preference in localStorage. Apply `.dark` class on `<html>`. Use JS-only system preference detection — NO CSS `@media (prefers-color-scheme)` queries.

### Step 6: Routes + Dashboard

Create the route files:

```
src/routes/
├── __root.tsx           # Root layout (HTML shell, theme, CSS)
├── index.tsx            # Landing → redirect to /dashboard if authenticated
├── login.tsx            # Login form (email/password + Google OAuth button)
├── register.tsx         # Registration form
├── _authed.tsx          # Auth guard layout (beforeLoad checks session)
└── _authed/
    ├── dashboard.tsx    # Stat cards overview
    ├── items.tsx        # Items list (table with actions)
    ├── items.$id.tsx    # Edit item form
    └── items.new.tsx    # Create item form
```

**Auth guard pattern** (`_authed.tsx`):

```typescript
import { createFileRoute, redirect } from "@tanstack/react-router";
import { getSessionFn } from "../server/auth";

export const Route = createFileRoute("/_authed")({
  beforeLoad: async () => {
    const session = await getSessionFn();
    if (!session) {
      throw redirect({ to: "/login" });
    }
    return { session };
  },
});
```

**Components** (in `src/components/`):

- `app-sidebar.tsx` — shadcn Sidebar with navigation links (Dashboard, Items)
- `theme-toggle.tsx` — three-state theme toggle button
- `user-nav.tsx` — user dropdown menu with sign-out action
- `stat-card.tsx` — reusable stat card for the dashboard

**See `references/server-functions.md`** for `createServerFn` patterns used in route loaders and mutations.

### Step 7: CRUD Server Functions

Create server functions for the items resource:

| Function | Method | Purpose |
|----------|--------|---------|
| `getItems` | GET | List all items for current user |
| `getItem` | GET | Get single item by ID |
| `createItem` | POST | Create new item |
| `updateItem` | POST | Update existing item |
| `deleteItem` | POST | Delete item by ID |

Each server function:
1. Gets auth session (redirect if not authenticated)
2. Creates per-request Drizzle client via `getDb()`
3. Performs the database operation
4. Returns typed data

Route loaders call GET server functions. Mutations call POST server functions then `router.invalidate()` to refetch.

### Step 8: Verify Locally

```bash
pnpm dev
```

Verification checklist:

- [ ] App loads at http://localhost:3000
- [ ] Register a new account (email/password)
- [ ] Login and logout work
- [ ] Dashboard page loads with stat cards
- [ ] Create a new item via /items/new
- [ ] Items list shows the new item
- [ ] Edit item via /items/:id
- [ ] Delete item from the list
- [ ] Theme toggle cycles: light → dark → system
- [ ] Sidebar collapses on mobile viewports
- [ ] No console errors

### Step 9: Deploy to Production

```bash
# Set production secrets
openssl rand -hex 32 | npx wrangler secret put BETTER_AUTH_SECRET
echo "https://PROJECT.SUBDOMAIN.workers.dev" | npx wrangler secret put BETTER_AUTH_URL
echo "http://localhost:3000,https://PROJECT.SUBDOMAIN.workers.dev" | npx wrangler secret put TRUSTED_ORIGINS

# If using Google OAuth
echo "your-client-id" | npx wrangler secret put GOOGLE_CLIENT_ID
echo "your-client-secret" | npx wrangler secret put GOOGLE_CLIENT_SECRET

# Migrate remote database
pnpm db:migrate:remote

# Build and deploy
pnpm build && npx wrangler deploy
```

**After first deploy**: Update `BETTER_AUTH_URL` with your actual Worker URL. Add production URL to Google OAuth redirect URIs: `https://your-app.workers.dev/api/auth/callback/google`.

**See `references/deployment.md`** for the full production checklist and common mistakes.

## Common Issues

| Symptom | Fix |
|---------|-----|
| `env` is undefined in server function | Use `import { env } from "cloudflare:workers"` — must be inside request handler, not module scope |
| D1 database not found | Check wrangler.jsonc `d1_databases` binding name matches code |
| Auth redirect loop | `BETTER_AUTH_URL` must match actual URL exactly (protocol + domain, no trailing slash) |
| Auth silently fails (redirects to home) | Set `TRUSTED_ORIGINS` secret with all valid URLs (comma-separated) |
| Styles not loading in dev | Ensure `@tailwindcss/vite` plugin is in vite.config.ts |
| SSR hydration mismatch | Add `suppressHydrationWarning` to `<html>` element |
| Build fails on Cloudflare | Check `nodejs_compat` in compatibility_flags, `main` field in wrangler.jsonc |
| Secrets not taking effect | `wrangler secret put` does NOT redeploy — run `npx wrangler deploy` after |
