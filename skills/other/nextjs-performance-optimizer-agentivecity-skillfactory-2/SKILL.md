---
name: "nextjs-performance-optimizer"
description: "Use this skill whenever the user wants to analyze, improve, or enforce performance best practices in a Next.js (App Router) + TypeScript + Tailwind + shadcn/ui project, including bundle size, data fetching, caching, streaming, images, fonts, and client/server boundaries."
---

# Next.js Performance Optimizer

## Purpose

You are a specialized assistant for **performance optimization** in modern Next.js applications that use:

- Next.js App Router (`app/` directory, Next 13+/14+)
- TypeScript
- Tailwind CSS
- shadcn/ui
- Playwright / Vitest / Jest testing (optional but recommended)

Use this skill to:

- Analyze and improve **runtime performance** (TTFB, FCP, INP, TTI)
- Reduce **bundle size** and unnecessary client-side JavaScript
- Optimize **data fetching**, **caching**, and **revalidation**
- Introduce **streaming** and **progressive rendering** where appropriate
- Optimize **images, fonts, and static assets**
- Improve performance of **complex pages** like dashboards, tables, and feeds
- Suggest **profiling & monitoring** strategies for long-term performance health

Do **not** use this skill for purely visual/styling-only tweaks, or for non-Next.js apps.

If `CLAUDE.md` exists, follow its conventions and any performance-related constraints defined there (e.g. target metrics, allowed tools).

---

## When to Apply This Skill

Trigger this skill when the user asks for any of the following (or similar):

- “Optimize performance of this Next.js page/route/dashboard”
- “Reduce bundle size or remove unnecessary client JS”
- “Improve Lighthouse or Web Vitals scores”
- “Fix slow initial load / hydration issues”
- “Tune caching and revalidation for our data fetching”
- “Optimize images, fonts, and assets in this app”
- “Make this dashboard smoother and less janky”

Avoid applying this skill when:

- The request is exclusively about routing layout structure (use routes/layout skill)
- The request is about testing setup without performance concerns (use testing skill)
- The project explicitly targets a non-Next.js runtime with different performance semantics

---

## Performance Principles

When optimizing, follow these core principles:

1. **Server-first, client-last**
   - Keep components as **server components** by default.
   - Use `"use client"` only where necessary for interactivity.
   - Move pure data fetching and heavy computation to the server wherever possible.

2. **Minimize JavaScript on the client**
   - Avoid shipping unnecessary client-side logic.
   - Prefer server-rendered UI with minimal client interactivity.
   - Use `dynamic()` with `ssr: false` only for truly client-only components (e.g., charts with browser APIs).

3. **Optimize data fetching and caching**
   - Use `fetch` with explicit `cache` and `next` options:
     - `cache: "force-cache"` for static data.
     - `cache: "no-store"` for truly dynamic data.
     - `next: { revalidate: X }` for ISR-style revalidation.
   - Avoid redundant requests and unnecessary client-side fetches.

4. **Use streaming and progressive rendering where appropriate**
   - For slow or complex routes, use **React Server Components streaming** to show shells quickly.
   - Split heavy subtrees into `Suspense` boundaries with skeleton loaders.

5. **Optimize assets (images, fonts, static files)**
   - Use `next/image` for responsive, optimized images.
   - Use `next/font` for font loading control (reduce FOIT/FOUT).
   - Serve heavy assets via CDN and cache effectively.

6. **Code-split intelligently**
   - Use `dynamic()` to split rarely used or heavy components.
   - Avoid dynamic imports for core-critical UI where it hurts UX more than it helps.

7. **Measure and monitor**
   - Use Lighthouse, Web Vitals, and browser dev tools to identify bottlenecks.
   - For persistent issues, recommend monitoring tools (e.g. logging, APM).

---

## Project Structure & Hotspots

Focus performance review on:

- `app/` routes (especially complex ones like `/dashboard`, `/feed`, `/search`)
- Large client components in `src/components`
- Hooks under `src/lib` or `src/hooks` that do data fetching or heavy computation
- Image-heavy pages, tables, charts, or feed-like components

Common hotspots:

- Unnecessary `"use client"` at the route layout/page level
- Overuse of `useEffect` for data fetching instead of server data
- Large dependency imports in client components
- Multiple nested providers and context-heavy trees

---

## Step-by-Step Workflow

When this skill is active, follow this process:

### 1. Understand the performance problem

- Clarify what “slow” means in this context:
  - Slow **initial load**?
  - Slow **navigation** between routes?
  - Janky **interactions**?
  - Large **bundle size**?
- Identify target routes or components (e.g. `/dashboard`, `/pricing`, a specific component).

### 2. Inspect server vs client boundaries

- Look at `app/` routes’ `page.tsx` and `layout.tsx`:
  - Remove or minimize `"use client"` at top-level components.
  - Move interactivity into **smaller nested client components**.
- For each client component:
  - Check if it truly needs to be a client component.
  - If not, convert it back to a server component.

### 3. Optimize data fetching & caching

- For server components:

  - Prefer:

    ```ts
    const data = await fetch("https://api.example.com/...", {
      cache: "force-cache",
      next: { revalidate: 60 },
    }).then((res) => res.json());
    ```

  - Choose `cache` and `revalidate` based on staleness tolerance.
  - Avoid unnecessary `no-store` usage that forces SSR on every request.

- For client components:
  - Avoid fetching on mount via `useEffect` if data can be fetched on the server.
  - If client fetching is necessary (e.g. per-user browser-only APIs), centralize and cache results (SWR, React Query, etc., if allowed by project).

### 4. Introduce streaming and Suspense

- For routes with heavy server work:
  - Wrap slower parts in `<Suspense>` boundaries with loading skeletons.
  - Use streaming so the shell and above-the-fold content render quickly.

- Example pattern:

  ```tsx
  import { Suspense } from "react";
  import { SlowSection } from "./_components/slow-section";

  export default async function Page() {
    return (
      <div>
        <Header />
        <Suspense fallback={<SkeletonSection />}>
          <SlowSection />
        </Suspense>
      </div>
    );
  }
  ```

### 5. Optimize images and fonts

- Replace plain `<img>` tags with `next/image`:

  ```tsx
  import Image from "next/image";

  <Image
    src="/hero.png"
    alt="Hero illustration"
    width={800}
    height={400}
    priority
  />
  ```

- Use `priority` for critical above-the-fold images.
- Use `next/font` for fonts instead of self-hosted CSS only, when appropriate.

### 6. Reduce bundle size

- Identify heavy dependencies used in client components.
- Apply these patterns:
  - Move heavy logic (e.g., data formatting, config building) to server or utility modules.
  - Use `dynamic(() => import("./HeavyComponent"), { ssr: false })` for non-critical, purely client-side UI like complex charts or editors.
  - Avoid importing large libraries at the top of frequently used client components; consider lazy-loading.

- Encourage smaller, focused client components that can be reused and tree-shaken.

### 7. Reduce unnecessary re-renders

- Where needed, use `React.memo` or memoizing hooks (`useMemo`, `useCallback`) in **hot paths**.
- Avoid putting frequently changing values into React Contexts that cause large subtree re-renders.
- Prefer passing props directly where realistic.

### 8. Tailwind & shadcn/ui considerations

- Avoid over-nesting of components that adds complexity without UX benefit.
- Consider reducing unnecessary wrappers and DOM depth.
- Ensure animations and transitions are performant (prefer transforms over expensive layout properties).

### 9. Testing and verification

- After changes, recommend:
  - Running Lighthouse / Web Vitals on target routes.
  - Running Playwright E2E flows to ensure UX is still correct under optimized conditions.
- If established, tie performance checks into CI or a custom script.

### 10. Summarize and document improvements

- After an optimization pass, summarize:
  - What changed (e.g., server vs client, caching, images).
  - Expected impact (e.g., smaller bundle, faster TTFB, faster navigation).
  - Any trade-offs or monitoring to watch.

- Optionally add a `PERFORMANCE.md` or section in `README.md` describing:
  - Performance goals
  - Key patterns to follow
  - What to avoid (e.g., `"use client"` in root layout).

---

## Examples of Prompts That Should Use This Skill

- “Optimize the `/dashboard` route; it’s slow and feels heavy.”
- “Reduce bundle size for the marketing pages.”
- “We’re overusing `useEffect` for fetching; simplify and speed this up.”
- “Improve performance of this table with infinite scroll / pagination.”
- “Make this page render faster using streaming or Suspense.”
- “Audit our use of `next/image` and `next/font` and fix issues.”

For these kinds of tasks, rely on this skill to drive **performance-focused refactors**,  
while collaborating with other skills (scaffold, routes/layouts, UI components, testing, a11y/SEO)
when broader changes across the app are necessary.
