---
name: "nextjs-routes-and-layouts"
description: "Use this skill whenever the user wants to design, refactor, or extend Next.js App Router routes, layouts, and navigation patterns (including route groups, dynamic routes, and server/client component boundaries) in a TypeScript + Tailwind + shadcn/ui project."
---

# Next.js Routes and Layouts

## Purpose

You are a specialized assistant for **designing and maintaining routing and layout structure** in modern Next.js apps that use:

- Next.js App Router (`app/` directory, Next 13+ / 14+)
- TypeScript
- Tailwind CSS
- shadcn/ui (or a similar headless component setup)
- The user's existing project conventions as defined in `CLAUDE.md` when present

Use this skill to:

- Plan and implement **new routes** and nested routes
- Introduce or refactor **layouts**, route groups, and shared UI shells (e.g. dashboards)
- Correctly choose between **server and client components**
- Add supporting files: `layout.tsx`, `page.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`, `template.tsx`, `default.tsx` for parallel routes
- Set up or adjust **dynamic routes**, **catch-all routes**, **parallel routes**, and **intercepting routes**
- Wire up **navigation** using `Link`, `useRouter`, and server actions where appropriate
- Integrate routing structure with shadcn/ui layouts and navigation components (navbars, sidebars, tabs, breadcrumbs)

Do **not** use this skill for:

- Non-Next.js frameworks or legacy `pages/`-router-only apps
- Pure API or backend-only services with no routes/layouts
- Styling-only changes that do not affect routes, layouts, or navigation hierarchy

If `CLAUDE.md` exists, follow its rules and conventions over anything written here.

---

## When to Apply This Skill

Trigger this skill when the user asks for any of the following (or similar) actions in a Next.js project:

- “Add a new route/section/page at path `/x` or nested under `/parent/x`”
- “Create a dashboard layout with a sidebar and nested pages”
- “Split marketing vs app routes using route groups”
- “Add dynamic routing for `[slug]`, `[id]`, or nested param segments”
- “Set up parallel routes or intercepting routes for this feature”
- “Refactor the routing structure, it’s a mess”
- “Organize routes by domain (marketing/app/admin) without changing URLs”
- “Make the routing follow best practices for App Router”

Avoid applying this skill when:

- The user is only changing logic inside a single component without affecting route structure
- The project clearly uses only the legacy `pages/` router and the user did not ask to migrate
- The user explicitly requests a framework-specific pattern that conflicts with Next.js App Router semantics

---

## Routing & Layout Principles

When using this skill, follow these core principles for Next.js App Router:

1. **File-system routing is the source of truth**
   - Each folder under `app/` is a route segment.
   - Nest folders to create nested routes (e.g. `app/dashboard/settings/page.tsx` → `/dashboard/settings`).
   - Use descriptive folder names that reflect domain concepts, not just UI names.

2. **Use the App Router by default**
   - Prefer `app/` directory semantics over legacy `pages/` API unless the project is explicitly pages-only.
   - Use **server components** by default for pages and layouts.
   - Use `"use client"` only where necessary (interactivity, hooks like `useState`, `useEffect`, `useRouter`, browser APIs).

3. **Layouts are for shared shell and structure**
   - Place persistent UI (headers, sidebars, shells, top-nav, footers) in `layout.tsx` files.
   - Use nested layouts for nested sections (e.g. `/dashboard` has its own layout wrapping child routes).
   - Keep layouts mostly presentational and avoid embedding heavy business logic.

4. **Route groups for organization, not URLs**
   - Use `(group-name)` folders to organize routes or to scope shared layouts without affecting URL paths.
   - Typical high-level groups:
     - `(marketing)` → landing pages, public marketing site
     - `(app)` → authenticated app experience
     - `(admin)` → admin-only tools
   - Do not rely on group folder names appearing in URLs.

5. **Dynamic and catch-all segments**
   - Use `[slug]`, `[id]`, `[...slug]`, `[[...slug]]` appropriately for dynamic routes.
   - Prefer dynamic segments over ad-hoc route-handling logic where URL semantics match resource IDs or slugs.
   - When generating static params, use `generateStaticParams` where SSG is appropriate.

6. **Parallel and intercepting routes (advanced)**
   - Use parallel routes when different UI regions need independent content for the same canonical URL (e.g. a sidebar with independent content).
   - Use intercepting routes for modal or overlay patterns that “intercept” navigation to another route.
   - Only introduce these when simpler patterns (nested routes + layouts) are insufficient.

7. **Metadata & SEO**
   - Use `generateMetadata` or `metadata` export in route segments to control per-route SEO, Open Graph, etc.
   - Keep metadata generation co-located with the route segment that owns the content.
   - Avoid heavy async work in metadata unless needed.

8. **Combining with shadcn/ui and Tailwind**
   - Use shadcn/ui primitives (e.g. `Button`, `Card`, `ScrollArea`, `Sheet`, `Tabs`) in layouts and navigation shells.
   - Keep branding and layout primitives in shared components under `src/components/layout` or `src/components/shell`.
   - Ensure navigation structure (sidebar items, top nav links, breadcrumbs) is driven by a **single source of truth** where feasible.

---

## Step-by-Step Workflow

When this skill is active, follow this process:

### 1. Inspect and classify the request

- Determine whether the user is:
  - Adding new routes
  - Refactoring existing routes/layouts
  - Adding advanced routing patterns (dynamic, parallel, intercepting)
- Check the current project structure:
  - Is there an `app/` directory?
  - Are there route groups like `(marketing)` / `(app)` / `(admin)`?
  - Is there an existing `CLAUDE.md` with routing conventions?

If the project uses only the `pages/` router and the user has not asked to migrate, either:
- Respect the pages router and give guidance accordingly, or
- Propose an explicit migration path if the user wants App Router benefits.

### 2. Propose or confirm a route hierarchy

- Sketch a **file/folder tree** under `app/` that reflects the desired URLs.
- Group routes according to domain:
  - Public marketing vs authenticated app
  - User vs admin areas
- Example pattern:

  ```text
  app/
    (marketing)/
      layout.tsx
      page.tsx          # /
      pricing/
        page.tsx        # /pricing
      blog/
        page.tsx
        [slug]/
          page.tsx
    (app)/
      layout.tsx        # authenticated shell
      dashboard/
        layout.tsx
        page.tsx        # /dashboard
        settings/
          page.tsx      # /dashboard/settings
  ```

- When refactoring, show a **before/after** structure to make changes clear.

### 3. Decide server vs client components

For each route segment (`page.tsx`, `layout.tsx`, and important nested components):

- Prefer **server components** for:
  - Static or dynamic data fetching
  - Heavy computation or secure logic
  - Components that do not need browser APIs or React hooks

- Use **client components** when:
  - Using React state/effect/hooks
  - Handling user interactions that require browser APIs
  - Using `useRouter`, `usePathname`, `useSearchParams`

- When in doubt:
  - Compose: keep outer shell as server component, and nest small client components inside as needed.

### 4. Add or adjust special files

For each relevant folder/segment, consider adding:

- `layout.tsx` — wraps child routes with shared UI.
- `page.tsx` — the main route content.
- `loading.tsx` — skeleton/loading UI while server components/data load.
- `error.tsx` — error boundary for that segment; keep it a client component.
- `not-found.tsx` — for 404 within that segment’s scope.
- `template.tsx` — to control how children are re-rendered when navigating.
- `default.tsx` — for default content in parallel routes.

Always explain briefly **why** you add each special file and what its scope is.

### 5. Implement navigation structure

- Use `Link` components for standard navigations.
- Use `useRouter` only in client components when you truly need imperative navigation (e.g. after a mutation).
- Encourage using shadcn/ui primitives for navigation:
  - Sidebars, navbars, menus, breadcrumbs, tabs.
- Ensure active states and accessibility are handled correctly (ARIA attributes, keyboard navigation).

### 6. Keep routes cohesive and predictable

- Avoid deeply nested segment hierarchies unless necessary.
- Prefer meaningful path segments: `/settings/profile` instead of `/s/p`.
- If a route structure becomes complex, consider a brief **route map**:

  ```text
  /                 → marketing home
  /pricing          → marketing pricing
  /blog             → blog listing
  /blog/[slug]      → blog article
  /dashboard        → app home (authenticated)
  /dashboard/settings/profile
  /dashboard/settings/security
  ```

- Use this map as a reference for both humans and for future skill runs.

### 7. Integrate with tests and dev ergonomics

- When adding new routes, suggest adding or updating tests:
  - Unit/component tests for critical pages and layout logic.
  - E2E tests (Playwright) that assert navigation works as expected.
- Ensure `README` or project docs mention how to navigate and where key layouts live.

### 8. Summarize changes and next steps

- After modifying or proposing a structure, summarize:
  - New or changed folders and files.
  - New URLs introduced.
  - Any advanced routing patterns used (dynamic, parallel, intercepting).
- Suggest further improvements when relevant (e.g. extracting shared layout pieces, adding metadata, adding E2E coverage).

---

## Examples of Prompts That Should Use This Skill

- “Create a separate marketing and app layout, but keep URLs the same.”
- “Add `/account/billing` under the app dashboard with its own sublayout.”
- “Introduce dynamic routes for blog posts at `/blog/[slug]` with proper 404 handling.”
- “Set up parallel routes so I can show a list and a detail view side by side.”
- “Refactor my app directory; the layouts are duplicated everywhere.”
- “Organize the routes so the sidebar navigation structure is clear and matches the URL hierarchy.”

When handling these kinds of requests, rely on this skill for routing and layout decisions, then collaborate with other skills (e.g. app scaffold, UI component skill, testing skill) for implementation details, styling, and tests.
