---
name: frontend
description: |
    Frontend architecture approaches — from Multi-Page Apps through Single Page Apps, Server-Side Rendering, Islands Architecture, and Micro-Frontends. Covers the full spectrum of client-side concerns: routing, state management, data fetching, code splitting, and hydration.
    USE FOR: frontend architecture selection, comparing SPA vs SSR vs micro-frontends, choosing frontend frameworks, client-side architecture decisions
    DO NOT USE FOR: specific rendering approach details (use sub-skills: spa, pwa, micro-frontends, ssr), backend architecture (use dev/backend), design system components (use design-system)
license: MIT
metadata:
  displayName: "Frontend Architecture"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "MDN Web Docs — Web Technology for Developers"
    url: "https://developer.mozilla.org/en-US/docs/Web"
  - title: "web.dev — Building for the Modern Web"
    url: "https://web.dev/"
---

# Frontend Architecture

## Overview
Frontend architecture has evolved far beyond "put jQuery on the page." Modern frontend development is a spectrum of rendering strategies, each with distinct tradeoffs for performance, SEO, developer experience, and user experience. Choosing the right architecture is one of the most consequential decisions in a web project — it affects everything from time-to-interactive to team structure.

## The Frontend Architecture Spectrum

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Frontend Architecture Spectrum                     │
│                                                                      │
│  MPA ────▶ SPA ────▶ SSR ────▶ SSG ────▶ Islands ────▶ Micro-FEs   │
│                                                                      │
│  Server      Client       Server+Client    Build-Time   Partial     │
│  Rendered    Rendered     Hybrid           Pre-render   Hydration   │
│  Full page   Single       HTML+Hydrate     Static HTML  Interactive │
│  reloads     shell+API    on every req     + CDN        islands     │
└──────────────────────────────────────────────────────────────────────┘
```

### Multi-Page Application (MPA)
Traditional server-rendered HTML pages. Each navigation is a full page request. Simple, SEO-friendly, but no client-side interactivity without additional JavaScript.

### Single Page Application (SPA)
A single HTML shell with client-side routing and rendering. The server provides JSON APIs; the browser handles everything else. Rich interactivity but challenges with SEO, initial load, and bundle size.

### Server-Side Rendering (SSR)
HTML is rendered on the server for each request, then hydrated on the client for interactivity. Best of both worlds — SEO-friendly first paint with SPA-like interactivity after hydration.

### Static Site Generation (SSG)
Pages are pre-rendered at build time and served as static HTML from a CDN. Fastest possible TTFB, but content is only as fresh as the last build.

### Islands Architecture
The page is mostly static HTML with isolated "islands" of interactivity that hydrate independently. Only interactive components ship JavaScript. Astro pioneered this approach.

### Micro-Frontends
Multiple independently deployed frontend applications composed into a single user experience. Each team owns a vertical slice of the UI with its own tech stack, build pipeline, and deployment.

## Comparison Table

| Criteria | SPA | SSR | SSG | Islands |
|----------|-----|-----|-----|---------|
| **First Contentful Paint** | Slow (JS must load) | Fast (server HTML) | Fastest (CDN) | Fast (static + partial JS) |
| **Time to Interactive** | Moderate | Moderate (hydration) | Fast | Fast (minimal JS) |
| **SEO** | Poor (without SSR/prerender) | Excellent | Excellent | Excellent |
| **Dynamic Content** | Excellent (API-driven) | Excellent (per-request) | Limited (build-time) | Moderate |
| **JS Bundle Size** | Large | Large (hydration) | Small-Medium | Minimal |
| **Caching** | API-level | Page-level (CDN w/ ISR) | Full CDN | Full CDN + selective |
| **Complexity** | Moderate | High | Low | Low-Moderate |
| **Best For** | Dashboards, apps | Content + interactivity | Blogs, docs, marketing | Content-heavy + some interactivity |

## Core Frontend Concerns

### Routing
- **Client-side**: React Router, Vue Router, Angular Router — URL changes without full page reloads
- **File-based**: Next.js, Nuxt, SvelteKit, Remix — filesystem structure defines routes
- **Server-side**: Traditional MPA routing — each URL is a server request

### State Management
- **Local state**: React useState/useReducer, Vue ref/reactive, Svelte stores, Angular signals
- **Global state**: Redux, Zustand, Pinia, NgRx, Jotai, Valtio
- **Server state**: TanStack Query, SWR, Apollo Client — treats server data as a cache
- **URL state**: Search params as state (Remix philosophy)

### Data Fetching
- **Client-side**: fetch/axios from useEffect, TanStack Query, SWR
- **Server-side**: Next.js Server Components, Remix loaders, Nuxt useFetch, SvelteKit load
- **GraphQL**: Apollo Client, urql, Relay
- **Real-time**: WebSockets, Server-Sent Events, tRPC subscriptions

### Code Splitting
- **Route-based**: React.lazy + Suspense, dynamic import()
- **Component-based**: Loadable Components, Vue async components
- **Framework-managed**: Next.js automatic splitting, Vite's chunk optimization

### Hydration
- **Full hydration**: Entire page re-rendered on client (React SSR, Next.js)
- **Partial hydration**: Only interactive parts hydrate (Astro Islands)
- **Progressive hydration**: Components hydrate on visibility/interaction
- **Resumability**: Skip hydration entirely, serialize state (Qwik)

## Framework Landscape

| Framework | Type | Rendering | Language |
|-----------|------|-----------|----------|
| **React** | Library | SPA, SSR (via Next.js) | TypeScript/JSX |
| **Vue** | Framework | SPA, SSR (via Nuxt) | TypeScript/SFC |
| **Angular** | Framework | SPA, SSR (Angular Universal) | TypeScript |
| **Svelte** | Compiler | SPA, SSR (via SvelteKit) | TypeScript/Svelte |
| **Solid** | Library | SPA, SSR (via SolidStart) | TypeScript/JSX |
| **Astro** | Meta-framework | Islands, SSG, SSR | Any (React, Vue, Svelte, etc.) |
| **Next.js** | Meta-framework | SSR, SSG, ISR, RSC | TypeScript/React |
| **Nuxt** | Meta-framework | SSR, SSG, ISR | TypeScript/Vue |
| **Remix** | Meta-framework | SSR, SPA mode | TypeScript/React |
| **SvelteKit** | Meta-framework | SSR, SSG, SPA | TypeScript/Svelte |

## Architecture Decision Guide

| When You Need... | Choose |
|-----------------|--------|
| Rich interactivity, dashboard-style UI | SPA (see `dev/frontend/spa`) |
| SEO + interactivity, content sites | SSR (see `dev/frontend/ssr`) |
| Static content with occasional interactivity | Islands (Astro) |
| Offline support, native-like experience | PWA (see `dev/frontend/pwa`) |
| Multiple teams, independent deployment | Micro-frontends (see `dev/frontend/micro-frontends`) |
| Blog, documentation, marketing pages | SSG (Next.js, Astro, or Hugo) |
| Full-stack with tight server integration | Remix or SvelteKit |

## Performance Budgets

A well-architected frontend should target:
- **Largest Contentful Paint (LCP)**: < 2.5s
- **First Input Delay (FID)**: < 100ms
- **Cumulative Layout Shift (CLS)**: < 0.1
- **Total JS bundle (initial)**: < 200KB gzipped
- **Time to Interactive (TTI)**: < 3.5s on 4G

## Best Practices
- Choose the simplest architecture that meets your requirements — not every app needs SSR or micro-frontends.
- Measure performance with real user metrics (Core Web Vitals), not just Lighthouse scores.
- Use code splitting aggressively — no user should download JavaScript they will never execute.
- Treat server state and client state differently — use TanStack Query or SWR for server state, not Redux.
- Design for progressive enhancement — the page should be usable before JavaScript loads.
- Consider the Islands Architecture for content-heavy sites that need sprinkles of interactivity.

## Sub-Skills
- `dev/frontend/spa` — Single Page Applications: client-side routing, state management, bundle optimization
- `dev/frontend/pwa` — Progressive Web Apps: service workers, offline support, installability
- `dev/frontend/micro-frontends` — Micro-Frontend Architecture: Module Federation, single-spa, composition
- `dev/frontend/ssr` — Server-Side Rendering: SSR, SSG, ISR, Islands, React Server Components
