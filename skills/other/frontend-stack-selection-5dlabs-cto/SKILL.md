---
name: frontend-stack-selection
description: Decision framework for choosing between shadcn (SSR/SEO) and TanStack (real-time/client-first) frontend stacks
agents: [morgan]
triggers: [frontend, stack, blaze, shadcn, tanstack, dashboard, marketing]
---

# Frontend Stack Selection

The CTO platform supports two frontend stack philosophies. Use this skill to choose the appropriate stack when generating Blaze tasks.

## Quick Reference

| Stack | Best For | Router | Data Layer | Tables | Forms |
|-------|----------|--------|------------|--------|-------|
| **shadcn** (Default) | Marketing, SEO, SSR, e-commerce | Next.js App Router | Server Actions + React Query | shadcn Table | React Hook Form |
| **tanstack** | Dashboards, real-time, local-first | TanStack Router | TanStack DB + Query | TanStack Table | TanStack Form |

---

## Option A: shadcn Stack (Default)

**Best for**: Marketing sites, SEO-focused apps, content-heavy sites, e-commerce, SSR applications

**Core Technologies**:
- **Router**: Next.js App Router (SSR, file-based routing, RSC)
- **Data**: Server Actions + React Query for client-side caching
- **UI**: shadcn/ui components (Radix primitives + Tailwind)
- **Forms**: React Hook Form + Effect Schema validation
- **Animation**: anime.js for motion design
- **Type System**: Effect (type-safe errors, Schema, services)

**Strengths**:
- Excellent SEO with server-side rendering
- Built-in image optimization, fonts, and metadata
- Streaming and progressive enhancement
- Mature ecosystem with extensive documentation

**Task XML Example**:

```xml
<task id="1">
    <meta>
        <title>Build Marketing Landing Page</title>
        <agent>blaze</agent>
        <frontend_stack>shadcn</frontend_stack>
    </meta>
    <context>
        <overview>Create SEO-optimized landing page with lead capture form</overview>
        <stack_rationale>shadcn selected for SSR, SEO, and Server Actions</stack_rationale>
    </context>
</task>
```

---

## Option B: TanStack Stack

**Best for**: Dashboards, admin panels, real-time apps, collaborative tools, offline-first, local-first applications

**Core Technologies**:
- **Router**: TanStack Router (type-safe, client-first, search params)
- **Data**: TanStack DB (collections, live queries, optimistic updates)
- **Query**: TanStack Query (always included, server-state management)
- **Tables**: TanStack Table (sorting, filtering, pagination, virtualization)
- **Forms**: TanStack Form + Effect Schema validation
- **Lists**: TanStack Virtual (100k+ items at 60fps)
- **Full-Stack**: TanStack Start (optional, for greenfield projects)
- **UI**: shadcn/ui components (compatible with both stacks)
- **Type System**: Effect (type-safe errors, Schema, services)

**Strengths**:
- Sub-millisecond live queries (~0.7ms for 100k items)
- Optimistic mutations with automatic rollback
- Type-safe routing with search param validation
- Client-first architecture for instant UI feedback
- Normalized collections prevent data duplication
- Sync modes: eager, on-demand, progressive

**Task XML Example**:

```xml
<task id="2">
    <meta>
        <title>Build Analytics Dashboard</title>
        <agent>blaze</agent>
        <frontend_stack>tanstack</frontend_stack>
    </meta>
    <context>
        <overview>Create real-time analytics dashboard with live data updates</overview>
        <stack_rationale>TanStack selected for live queries and sub-millisecond reactivity</stack_rationale>
    </context>
</task>
```

---

## Stack Selection Keywords

Use these keyword patterns to determine the appropriate stack:

| PRD Keywords | Recommended Stack | Rationale |
|--------------|-------------------|-----------|
| dashboard, admin panel, data grid, data-heavy | `tanstack` | TanStack Table + live queries excel at data-dense UIs |
| real-time, live updates, collaborative | `tanstack` | TanStack DB provides sub-ms live query reactivity |
| offline-first, local-first, sync | `tanstack` | TanStack DB collections support multiple sync strategies |
| optimistic UI, instant feedback | `tanstack` | Built-in optimistic mutations with rollback |
| marketing, landing page, brochure | `shadcn` | SSR and SEO optimization |
| SEO, search engine, metadata | `shadcn` | Next.js RSC with streaming |
| blog, content, CMS | `shadcn` | Server-side rendering for content |
| e-commerce, checkout, payment | `shadcn` | Server Actions for secure transactions |
| forms-heavy, wizard, multi-step | Either | Both have excellent form libraries |

---

## Frontend Stack in Task XML

When generating tasks for Blaze, include the `<frontend_stack>` element in the task meta:

```xml
<task id="{{task_id}}" priority="high">
    <meta>
        <title>Task Title</title>
        <agent>blaze</agent>
        <job_type>coder</job_type>
        <frontend_stack>tanstack</frontend_stack>  <!-- or "shadcn" -->
    </meta>
    <context>
        <overview>Task description</overview>
        <stack_rationale>Why this stack was selected</stack_rationale>
    </context>
    <!-- ... rest of task -->
</task>
```

If `frontend_stack` is omitted, Blaze defaults to the **shadcn** stack.

---

## Mixed Stack Projects

For projects requiring both stacks (e.g., marketing site with dashboard):

1. **Separate Next.js routes**: Use Next.js for marketing (`/`) and TanStack for dashboard (`/app/*`)
2. **Micro-frontends**: Separate deployments communicating via shared state
3. **Progressive migration**: Start with shadcn, add TanStack for specific features

Document the approach in the task context when mixed stacks are needed.
