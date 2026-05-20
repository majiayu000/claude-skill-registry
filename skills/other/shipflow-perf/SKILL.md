---
name: shipflow-perf
description: Deep performance audit — bundle analysis, rendering, Core Web Vitals, data fetching, database optimization. Single file, full project, or global.
disable-model-invocation: true
argument-hint: [file-path | "global"] (omit for full project)
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -120 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- Package.json: !`cat package.json 2>/dev/null | head -80 || echo "no package.json"`
- Build config: !`cat astro.config.* next.config.* vite.config.* 2>/dev/null | head -60 || echo "no build config"`
- Framework detection: !`cat package.json 2>/dev/null | grep -oE '"(astro|next|react|vue|expo|fastapi|flask)"' | head -5 || echo "unknown"`
- Image/font assets: !`find . -maxdepth 3 \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.webp" -o -name "*.avif" -o -name "*.woff" -o -name "*.woff2" -o -name "*.ttf" \) 2>/dev/null | grep -v node_modules | wc -l`
- Third-party scripts: !`grep -r "script.*src=" src/ 2>/dev/null | grep -v node_modules | head -10 || echo "none"`
- Project structure: !`find . -maxdepth 3 -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.astro" -o -name "*.vue" -o -name "*.py" -o -name "*.sh" \) 2>/dev/null | grep -v node_modules | grep -v .git | grep -v dist | sort | head -40`

## Mode detection

- **`$ARGUMENTS` is "global"** → GLOBAL MODE: performance audit across ALL projects.
- **`$ARGUMENTS` is a file path** → FILE MODE: deep performance review of that single file.
- **`$ARGUMENTS` is empty** → PROJECT MODE: full performance audit.

---

## GLOBAL MODE

Audit performance across ALL projects in the workspace.

1. Read `/home/claude/shipflow_data/PROJECTS.md` — check the **Domain Applicability** table. Identify projects with ✓ in the Perf column.

2. Use **AskUserQuestion** to let the user choose:
   - Question: "Which projects should I audit for performance?"
   - `multiSelect: true`
   - One option per applicable project: label = project name, description = stack from PROJECTS.md

3. Use the **Task tool** to launch one agent per **selected** project — ALL IN A SINGLE MESSAGE (parallel). Each agent: `subagent_type: "general-purpose"`.

   Agent prompt must include:
   - `cd [path]` then read `CLAUDE.md` for project context
   - The complete **PROJECT MODE** section from this skill (all 6 phases)
   - The **Tracking** section from this skill

4. After all agents return, compile a **cross-project performance report**:

   ```
   GLOBAL PERFORMANCE AUDIT — [date]
   ═══════════════════════════════════════
   PROJECT SCORES
     [project]    [A/B/C/D]  —  summary
     ...
   CROSS-PROJECT PATTERNS
     [Shared perf issues: duplicate large deps, common anti-patterns]
   ALL ISSUES BY SEVERITY
     🔴 [project] file:line — description
     🟠 [project] file:line — description
     🟡 [project] file:line — description
   Total: X critical, Y high, Z medium across N projects
   ═══════════════════════════════════════
   ```

5. Update `/home/claude/shipflow_data/AUDIT_LOG.md` (one row per project, Perf column) and `/home/claude/shipflow_data/TASKS.md` (each project's `### Audit: Perf` subsection).

6. Ask: **"Which projects should I fix?"** — list projects with scores. Fix only approved projects, one at a time.

---

## FILE MODE

### Step 1: Gather context

1. Read the target file (`$ARGUMENTS`).
2. Read files it imports/depends on (follow the imports, 1 level deep).
3. Identify the file's role: component, page, API route, utility, layout.

### Step 2: Audit the file

Score each category **A/B/C/D**.

#### 1. Bundle Impact
- [ ] No large dependencies imported for a small feature (e.g., lodash for one function)
- [ ] Imports use tree-shakeable paths (named imports, not full-library imports)
- [ ] Dynamic imports / lazy loading for heavy components
- [ ] No barrel file re-exports pulling in unused code

#### 2. Rendering Performance
- [ ] No unnecessary re-renders (React: stable callbacks, proper deps arrays, memo where needed)
- [ ] No expensive computations on every render cycle
- [ ] CSS-in-JS not generating new class names on every render
- [ ] Conditional rendering for expensive subtrees
- [ ] Lists use proper keys (not index for dynamic lists)

#### 3. Data Fetching
- [ ] No waterfall requests (sequential when could be parallel)
- [ ] Data fetched at the right level (not too high, not too low)
- [ ] No over-fetching (requesting fields that aren't used)
- [ ] Proper loading/error states
- [ ] Caching or deduplication for repeated queries

#### 4. Memory & Cleanup
- [ ] Event listeners removed on unmount
- [ ] Intervals/timeouts cleared
- [ ] Subscriptions unsubscribed
- [ ] AbortController for fetch requests on unmount
- [ ] No closures capturing stale state

### Step 3: Fix

Fix issues rated B or worse. Explain each change.

### Step 4: Report

```
PERFORMANCE REVIEW: [file name]
─────────────────────────────────────
Bundle Impact       [A/B/C/D] — one-line summary
Rendering           [A/B/C/D] — one-line summary
Data Fetching       [A/B/C/D] — one-line summary
Memory & Cleanup    [A/B/C/D] — one-line summary
─────────────────────────────────────
OVERALL             [A/B/C/D]

Fixed: X issues | Needs decision: Y
```

---

## PROJECT MODE

### Workspace root detection

If the current directory has no project markers (no `package.json`, no `requirements.txt`, no `src/` dir, no `lib.sh`) BUT contains multiple project subdirectories — you are at the **workspace root**, not inside a project.

Use **AskUserQuestion**:
- Question: "You're at the workspace root. Which project(s) should I audit for performance?"
- `multiSelect: true`
- Options:
  - **All projects** — "Run performance audit across every project" (Recommended)
  - One option per project from `/home/claude/shipflow_data/PROJECTS.md`: label = project name, description = stack

Then proceed to **GLOBAL MODE** with the selected projects.

### PHASE 1: BUNDLE & LOADING

Analyze the project's build output and dependency weight.

#### 1.1 Dependency Weight
- [ ] Identify top 10 largest dependencies by install size
- [ ] Flag oversized dependencies with lighter alternatives (moment→dayjs, lodash→lodash-es or native)
- [ ] Detect duplicate packages in the dependency tree (same package, different versions)
- [ ] Check for barrel exports (`index.ts`) re-exporting entire modules — bundle bloat

#### 1.2 Code Splitting
- [ ] Route-level code splitting configured
- [ ] Heavy components lazily loaded (`React.lazy`, `defineAsyncComponent`, dynamic imports)
- [ ] No single bundle containing rarely-used features

#### 1.3 Asset Optimization
- [ ] Images use modern formats (WebP/AVIF with fallbacks)
- [ ] Images have `srcset` / responsive sizing
- [ ] SVGs optimized (no unnecessary metadata)
- [ ] Fonts use WOFF2 format
- [ ] `font-display: swap` or `optional` configured
- [ ] Font subsetting applied (only needed character ranges)

#### 1.4 Script Loading
- [ ] Third-party scripts use `async` or `defer`
- [ ] Analytics/tracking not blocking render
- [ ] No synchronous `<script>` tags in `<head>`
- [ ] Prefetch/preload for critical resources

---

### PHASE 2: RENDERING

#### 2.1 Rendering Strategy
- [ ] Static pages use SSG (not SSR or CSR)
- [ ] Dynamic pages use appropriate strategy (SSR for SEO, CSR for app-like)
- [ ] Client-side hydration is minimal (Astro islands, React Server Components)

#### 2.2 Client Hydration Analysis
- [ ] Components that could be server-only are not hydrated client-side
- [ ] `client:load` vs `client:visible` vs `client:idle` used appropriately (Astro)
- [ ] No full-page client hydration for mostly-static content

#### 2.3 Re-render Issues
- [ ] No parent re-renders cascading to all children unnecessarily
- [ ] Context providers scoped (not wrapping entire app for local state)
- [ ] Expensive renders behind React.memo / computed / memoization
- [ ] Event handlers are stable references (useCallback where needed)

#### 2.4 Virtualization
- [ ] Long lists (>50 items) use virtualization (react-window, @tanstack/virtual)
- [ ] Tables with many rows are virtualized
- [ ] Infinite scroll uses proper windowing

---

### PHASE 3: CORE WEB VITALS READINESS

#### 3.1 LCP (Largest Contentful Paint)
- [ ] Hero image/video has `fetchpriority="high"` and `loading="eager"`
- [ ] LCP element is in initial HTML (not injected by JS)
- [ ] No render-blocking CSS/JS delaying LCP
- [ ] Fonts preloaded if they affect LCP text
- [ ] `<Image>` component used with priority prop for above-fold images

#### 3.2 CLS (Cumulative Layout Shift)
- [ ] Images and videos have explicit `width` and `height` attributes
- [ ] No FOUT (Flash of Unstyled Text) — `font-display` configured
- [ ] No content injected above the fold after load (ads, banners, lazy content)
- [ ] Skeleton screens match actual content dimensions
- [ ] No layout-shifting animations

#### 3.3 INP (Interaction to Next Paint)
- [ ] Click/tap handlers respond under 200ms
- [ ] Heavy computations offloaded to Web Workers
- [ ] No long tasks blocking the main thread (>50ms)
- [ ] Input handlers debounced appropriately
- [ ] Optimistic UI updates for perceived speed

#### 3.4 TTFB (Time to First Byte)
- [ ] Static pages served from CDN/edge
- [ ] SSR pages have efficient data fetching (no waterfalls)
- [ ] Database queries for page data are indexed
- [ ] Caching headers configured (Cache-Control, ETag)

---

### PHASE 4: DATA FETCHING

#### 4.1 Request Patterns
- [ ] No waterfall requests (use `Promise.all` or parallel loaders)
- [ ] No N+1 query patterns (fetching related data in loops)
- [ ] No over-fetching (GraphQL: use fragments; REST: use sparse fieldsets or dedicated endpoints)
- [ ] Request deduplication for same data needed in multiple components

#### 4.2 Caching Strategy
- [ ] API responses cached appropriately (SWR, React Query, Convex reactive queries)
- [ ] Stale-while-revalidate pattern for non-critical data
- [ ] Cache invalidation on mutations
- [ ] Static data pre-fetched at build time where possible

#### 4.3 Optimistic Updates
- [ ] Write operations update UI immediately (don't wait for server response)
- [ ] Rollback on failure with user feedback
- [ ] Convex: use optimistic updates for mutations

#### 4.4 Prefetching
- [ ] Next page data prefetched on link hover/focus
- [ ] Critical API calls initiated early (not waiting for component mount)
- [ ] Route prefetching configured for likely next pages

---

### PHASE 5: DATABASE & BACKEND

#### 5.1 Query Optimization
- [ ] Indexes defined for common query patterns
- [ ] No full table scans for filtered queries
- [ ] Compound indexes for multi-field queries
- [ ] Convex: indexes defined in `schema.ts` for all `withIndex` queries

#### 5.2 Unbounded Queries
- [ ] All list queries have limits (`.take(n)` / `LIMIT`)
- [ ] Pagination implemented for large datasets
- [ ] No `SELECT *` or equivalent fetching all fields
- [ ] Cursor-based pagination for large datasets (not offset)

#### 5.3 Connection & Resource Management
- [ ] Connection pooling configured for database
- [ ] No connection leaks (connections always returned to pool)
- [ ] Timeouts configured for external API calls
- [ ] Rate limiting respected for third-party APIs

#### 5.4 Caching Layer
- [ ] Frequently accessed data cached (in-memory, Redis, or CDN)
- [ ] Cache invalidation strategy defined
- [ ] Cache TTL appropriate for data freshness requirements
- [ ] No stale cache served for critical data (auth, payments)

---

### PHASE 6: FIX + REPORT

#### Fix Priority
1. **Critical** — N+1 queries, missing indexes, unbounded queries, memory leaks
2. **High** — Missing code splitting, no image optimization, waterfall requests
3. **Medium** — Missing lazy loading, suboptimal caching, minor CWV issues
4. **Low** — Prefetching, optimistic updates, minor bundle size improvements

#### Report

```
PERFORMANCE AUDIT: [project name] — [stack detected]
═══════════════════════════════════════════════════

BUNDLE & LOADING                     [A/B/C/D]
  Dependency Weight                  [A/B/C/D]
  Code Splitting                     [A/B/C/D]
  Asset Optimization                 [A/B/C/D]
  Script Loading                     [A/B/C/D]

RENDERING                            [A/B/C/D]
  Strategy                           [A/B/C/D]
  Client Hydration                   [A/B/C/D]
  Re-render Issues                   [A/B/C/D]

CORE WEB VITALS                      [A/B/C/D]
  LCP Readiness                      [A/B/C/D]
  CLS Readiness                      [A/B/C/D]
  INP Readiness                      [A/B/C/D]
  TTFB Readiness                     [A/B/C/D]

DATA FETCHING                        [A/B/C/D]
  Request Patterns                   [A/B/C/D]
  Caching                            [A/B/C/D]
  Optimization                       [A/B/C/D]

DATABASE & BACKEND                   [A/B/C/D]
  Query Optimization                 [A/B/C/D]
  Resource Management                [A/B/C/D]
═══════════════════════════════════════════════════
OVERALL                              [A/B/C/D]

Fixed: X issues | Needs decision: Y
```

---

## Stack-specific notes

Apply the relevant section based on detected framework:

**Astro**: Focus on islands pattern — verify `client:*` directives are minimal. Static pages should have zero JS. Check `astro:assets` Image component usage. View Transitions API perf impact.

**Next.js**: Check RSC (React Server Components) boundaries — `"use client"` only where needed. Streaming SSR for slow data. `next/image` with `priority` for above-fold. `next/font` for zero-layout-shift fonts.

**React Native / Expo**: List virtualization (FlatList vs FlashList). Image caching (expo-image). Bundle size with `npx expo-doctor`. Hermes engine optimizations. Avoid inline styles in render loops.

**Python (FastAPI)**: Async I/O for all external calls. Connection pooling (SQLAlchemy async). Background tasks for heavy operations. Response model filtering (don't return full ORM objects).

**Bash/Shell**: Script execution time. Subshell avoidance where possible. Caching of expensive operations (BuildFlowz 5s TTL pattern). Avoid repeated file reads in loops.

---

## Tracking (all modes)

After generating the report and applying fixes:

### Log the audit

Append a row to two files:

1. **Global `/home/claude/shipflow_data/AUDIT_LOG.md`**: append a row filling the Perf column, `—` for other domains.
2. **Project-local `./AUDIT_LOG.md`**: same but without the Project column.

Create either file if missing, using the table header from the master `/shipflow-audit` skill format.

### Update TASKS.md

1. **Local TASKS.md** (project root): add/replace a `### Audit: Perf` subsection with critical (🔴), high (🟠), and medium (🟡) issues.
2. **Master `/home/claude/shipflow_data/TASKS.md`**: find the project's section, add/replace a `### Audit: Perf` subsection with the same tasks.

---

## Important

- audit-seo keeps its own SEO-specific performance checks (render-blocking resources, LCP for SEO ranking). This skill does **deep** performance analysis.
- Be specific about file paths and line numbers for every issue.
- Detect the stack automatically. Only audit relevant sections (e.g., skip CWV for React Native).
- For Bash/Shell projects, focus on script efficiency and caching patterns.
- Performance issues are never optional — a slow site is a broken site.
