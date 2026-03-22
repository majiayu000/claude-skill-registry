---
name: "frontend-ui"
description: "Enterprise SaaS frontend — Tailwind v4, shadcn/ui, Next.js App Router or Vite SPA, accessibility, responsive design, component patterns. Use when: React component, Next.js page, frontend UI, Tailwind, shadcn, accessibility, a11y, responsive design, form validation, server component, client component, design system, dark mode, SaaS UI, dashboard, pricing page, enterprise UI, data table, landing page, Vite, React Router, SPA, single page app."
---

<objective>
Enterprise-grade frontend skill for auditing and building world-class SaaS UIs. Covers Tailwind CSS v4 (CSS-first config), shadcn/ui (2026), Next.js 15+ App Router **or Vite SPA** with React 19.

Production SaaS: dashboards, pricing pages, data tables, onboarding, role-based UI — with WCAG 2.1 AA accessibility and Core Web Vitals performance baked in.
</objective>

<quick_start>
## Setup: Tailwind v4 + shadcn/ui

```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir
cd my-app && npx shadcn@latest init
npx shadcn@latest add button card dialog table form
```

### Tailwind v4 — CSS-First (No tailwind.config.js)

```css
/* app/globals.css */
@import "tailwindcss";
@theme inline {
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.145 0 0);
  --color-primary: oklch(0.205 0.042 264.695);
  --color-primary-foreground: oklch(0.985 0 0);
  --radius-lg: 0.5rem;
  --radius-md: calc(var(--radius-lg) - 2px);
  --radius-sm: calc(var(--radius-lg) - 4px);
}
```

### Component Anatomy (shadcn/ui 2026)

```tsx
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors",
  {
    variants: {
      variant: { default: "bg-primary text-primary-foreground", outline: "border border-input" },
      size: { default: "h-10 px-4 py-2", sm: "h-9 px-3", lg: "h-11 px-8" },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
)

// React 19: ref is a regular prop — no forwardRef
// data-slot: styling hook for parent overrides
function Button({ className, variant, size, ref, ...props }:
  React.ComponentProps<"button"> & VariantProps<typeof buttonVariants>) {
  return <button ref={ref} data-slot="button"
    className={cn(buttonVariants({ variant, size, className }))} {...props} />
}
```

### cn() Utility

```ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)) }
```

### Vite SPA Alternative

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app && npm i -D @tailwindcss/vite && npx shadcn@latest init
```

Key differences from Next.js:
- `@tailwindcss/vite` plugin (not postcss) — faster HMR, native Vite integration
- `VITE_` env prefix (not `NEXT_PUBLIC_`), accessed via `import.meta.env`
- Client-only — no Server Components, use React Query for data fetching
- `React.lazy()` + `<Suspense>` replaces `dynamic()` for code splitting
- Routing via React Router v7 or TanStack Router (not file-based)

Tailwind v4, shadcn/ui, component patterns, accessibility, forms, and performance guidance all apply equally to Vite SPAs. Only routing and data fetching genuinely differ.

See `reference/vite-react-setup.md` and `reference/spa-routing.md`.
</quick_start>

<success_criteria>
Enterprise SaaS frontend is production-ready when:
- **Accessible:** WCAG 2.1 AA — keyboard nav, screen reader, focus management, 4.5:1 contrast
- **Performant:** LCP < 2.5s, INP < 200ms, CLS < 0.1 on 4G mobile
- **Responsive:** Mobile-first, works 320px-2560px, container queries for components
- **Secure:** No XSS vectors, CSP headers, sanitized user content
- **Themed:** Dark mode via CSS, design tokens in @theme, consistent spacing/color
- **Composable:** Server Components default, client boundary pushed to leaves
- **Typed:** TypeScript strict, Zod validation on all forms, no `any`
</success_criteria>

<core_principles>
1. **Server-First** — Default to Server Components. Add `"use client"` only for interactivity. Push client boundaries to leaf components.
2. **Accessible-by-Default** — Semantic HTML first (`<nav>`, `<main>`, `<article>`). ARIA only when native semantics insufficient.
3. **Composition Over Configuration** — Small composable components. Compound pattern for complex UI. Context at boundaries.
4. **Progressive Disclosure** — Essential info first. Reveal complexity on demand. Reduce cognitive load.
5. **Mobile-First** — Design for smallest screen, enhance upward. Container queries for components. Touch targets >= 44px.
6. **Design Tokens** — All visual values in CSS `@theme`. Never hardcode. OKLCH for perceptual uniformity.
7. **Type Safety E2E** — Zod schemas shared client/server. `React.ComponentProps<>` over manual interfaces.
</core_principles>

<tailwind_v4>
## Tailwind CSS v4 — Key Changes from v3

- **No `tailwind.config.js`** — All config via CSS `@theme` directive
- **`@import "tailwindcss"`** — Replaces `@tailwind base/components/utilities`
- **OKLCH colors** — Perceptually uniform, replaces hex/HSL
- **Container queries built-in** — `@container`, `@md:`, `@lg:` prefixes
- **`@source`** — CSS-native file scanning (replaces `content` array)
- **70% smaller CSS** — Automatic unused style elimination
- **`@theme inline`** — shadcn/ui bridge: tokens without generated utilities

```css
@theme {
  --color-brand-500: oklch(0.55 0.15 250);
  --font-sans: "Inter", system-ui, sans-serif;
  --breakpoint-xs: 475px;
  --animate-slide-in: slide-in 0.2s ease-out;
}
```

```tsx
// Container queries — component-level responsive
<div className="@container">
  <div className="grid grid-cols-1 @md:grid-cols-2 @lg:grid-cols-3 gap-4">
    {items.map(item => <Card key={item.id} {...item} />)}
  </div>
</div>
```

**Migration:** `npx @tailwindcss/upgrade` — See `reference/tailwind-v4-setup.md`.
</tailwind_v4>

<shadcn_ui>
## shadcn/ui 2026

- **`@theme inline`** — Bridges tokens with Tailwind v4
- **`data-slot`** — Attribute-based styling hooks (replaces className overrides)
- **No `forwardRef`** — React 19 ref as prop
- **`tw-animate-css`** — Replaces `tailwindcss-animate` for v4 compat
- **Radix or Base UI** — Choose primitive library

```tsx
// data-slot: parent can target child styles
function Card({ className, ref, ...props }: React.ComponentProps<"div">) {
  return <div ref={ref} data-slot="card" className={cn("rounded-xl border bg-card", className)} {...props} />
}

// Style from parent:
<div className="[&_[data-slot=card]]:shadow-lg">
  <Card>...</Card>
</div>
```

**Dark mode:** CSS custom property swap with `.dark` class. See `reference/shadcn-setup.md`.
</shadcn_ui>

<component_architecture>
## Server vs Client Components

| Server Component (default) | Client Component (`"use client"`) |
|---|---|
| Async data fetching, DB access | useState, useEffect, event handlers |
| Zero JS bundle, access to secrets | Browser APIs, third-party client libs |

**Rule:** Push `"use client"` to smallest leaf possible.

```tsx
// Server page with client island
export default async function DashboardPage() {
  const metrics = await getMetrics()
  return (
    <main>
      <KPICards data={metrics} />       {/* Server-rendered */}
      <RevenueChart data={metrics} />   {/* Client island */}
    </main>
  )
}
```

### Key Patterns

- **Compound components** — `<Table>/<TableRow>/<TableCell>` namespace composition
- **cva variants** — Type-safe style variants with `class-variance-authority`
- **React.ComponentProps** — Replace manual interfaces, ref as regular prop
- **data-slot** — External styling hooks for parent-child overrides
- **Polymorphic (asChild)** — `Slot` pattern for rendering as different elements
- **SPA code splitting** — `React.lazy()` + `<Suspense>` replaces Next.js `dynamic()`

See `reference/component-patterns.md` for complete examples.
</component_architecture>

<saas_patterns>
## Enterprise SaaS Patterns

### Dashboard: Sidebar + Header + Main

```tsx
<div className="flex h-screen">
  <Sidebar className="w-64 hidden lg:flex" />
  <div className="flex-1 flex flex-col">
    <Header />  {/* Search, user menu, notifications */}
    <main className="flex-1 overflow-auto p-6">
      <KPIGrid metrics={metrics} />
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <RevenueChart data={revenue} />
        <ActivityFeed items={activities} />
      </div>
    </main>
  </div>
</div>
```

### Pricing (3-Tier Conversion)

Anchor (low) | **Conversion target** (highlighted, "Most Popular") | Enterprise (custom)

Monthly/annual toggle, feature comparison table, social proof. See `templates/pricing-page.tsx`.

### Data Tables — shadcn Table + TanStack Table for sort/filter/paginate

### State Trio — Every data component needs: Loading (Skeleton) | Error (retry action) | Empty (guidance)

### Role-Based UI — `hasPermission(user, "scope")` guard for conditional rendering

See `reference/saas-dashboard.md` and `reference/saas-pricing-checkout.md`.
</saas_patterns>

<accessibility>
## WCAG 2.1 AA

**Semantic HTML first** — `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`

| Pattern | Implementation |
|---------|---------------|
| Keyboard nav | Tab/Shift+Tab, Arrow keys in menus/tabs, Escape to close |
| Focus management | Trap in dialogs, restore on close, skip link |
| ARIA live regions | `aria-live="polite"` for dynamic content |
| Form errors | `aria-invalid`, `aria-describedby`, `role="alert"` |
| Loading states | `aria-busy={true}` on loading buttons |
| Contrast | 4.5:1 text, 3:1 UI components (OKLCH lightness channel) |

```tsx
// Skip link
<a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:z-50">
  Skip to main content
</a>
```

See `reference/accessibility-checklist.md` for per-component ARIA patterns.
</accessibility>

<state_management>
## State Decision Tree

| State Type | Solution | Example |
|-----------|----------|---------|
| URL state | `nuqs` / `useSearchParams` | Filters, pagination, tabs |
| Server data | React Query / SWR | API data, user profile |
| Local UI | `useState` | Form inputs, toggles |
| Shared parent-child | Lift state / Context | Accordion groups |
| Complex cross-cutting | Zustand | Cart, wizard, notifications |

**Prefer URL state** — shareable, bookmarkable, survives refresh.
</state_management>

<data_fetching>
## Data Fetching

| Pattern | When | How |
|---------|------|-----|
| Server Components | Default | `async function Page() { const data = await db.query() }` |
| Suspense streaming | Slow data | `<Suspense fallback={<Skeleton/>}><SlowComponent/></Suspense>` |
| Server Actions | Mutations | `"use server"` + `revalidatePath()` |
| React Query | Client real-time | `useQuery({ queryKey, queryFn, refetchInterval })` |
| React Query (SPA) | Client-only apps | `useQuery({ queryKey, queryFn })` with loaders — replaces Server Components |
</data_fetching>

<forms>
## Forms: RHF + Zod + shadcn Form + Server Actions

1. **Shared Zod schema** — Single source of truth for client validation and server action
2. **React Hook Form** — `useForm` with `zodResolver`, `mode: "onBlur"`
3. **shadcn Form** — `<Form>/<FormField>/<FormItem>/<FormLabel>/<FormMessage>`
4. **Server Action** — `safeParse` on server, return field errors, `revalidatePath`

```tsx
const schema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
})
```

See `reference/form-patterns.md` and `templates/form-with-server-action.tsx`.
</forms>

<performance>
## Core Web Vitals

| Metric | Target | Quick Win |
|--------|--------|-----------|
| LCP < 2.5s | Main content visible | `next/image` with `priority`, `next/font` |
| INP < 200ms | Responsive interactions | Code-split heavy components with `dynamic()` |
| CLS < 0.1 | No layout shift | Reserve space for images/fonts, Skeleton loaders |

Tailwind v4 produces 70% smaller CSS automatically. See `reference/performance-optimization.md`.
</performance>

<references>
| Topic | Reference File | When to Load |
|-------|----------------|--------------|
| Tailwind v4 setup | `reference/tailwind-v4-setup.md` | New project, v3 migration |
| shadcn/ui setup | `reference/shadcn-setup.md` | Component library setup |
| Component patterns | `reference/component-patterns.md` | Building custom components |
| SaaS dashboard | `reference/saas-dashboard.md` | Dashboard layouts, KPI cards |
| Pricing + checkout | `reference/saas-pricing-checkout.md` | Pricing pages, Stripe UI |
| Accessibility | `reference/accessibility-checklist.md` | WCAG audit, ARIA patterns |
| Form patterns | `reference/form-patterns.md` | Multi-step forms, file upload |
| Performance | `reference/performance-optimization.md` | Core Web Vitals, Lighthouse |
| Vite + React setup | `reference/vite-react-setup.md` | New Vite SPA project |
| SPA routing | `reference/spa-routing.md` | React Router, TanStack Router |
</references>

<checklist>
## Enterprise SaaS Pre-Ship Audit

### Accessibility
- [ ] Keyboard navigation for all interactive elements
- [ ] Screen reader announces content meaningfully
- [ ] Focus indicators visible, skip link present
- [ ] Color contrast >= 4.5:1 (text), >= 3:1 (UI)

### Performance
- [ ] LCP < 2.5s, INP < 200ms, CLS < 0.1
- [ ] Images via next/image, fonts via next/font
- [ ] Heavy components code-split with dynamic()

### Responsive
- [ ] Works 320px-2560px, touch targets >= 44px
- [ ] Container queries for reusable components

### Security
- [ ] No raw HTML injection without sanitization
- [ ] CSP headers, Zod validation client AND server

### UX
- [ ] Loading / error / empty states for all data views
- [ ] Toast for mutations, confirm for destructive actions
</checklist>
