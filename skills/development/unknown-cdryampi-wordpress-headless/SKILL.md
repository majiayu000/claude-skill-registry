---
name: astro-frontend-ui
description: Build the Astro frontend with Tailwind CSS v4 via the Vite plugin, a WPGraphQL data layer, and React islands (shadcn/ui) only where needed. Use when implementing or fixing frontend files under frontend/ for this WordPress headless repo.
---

# Astro Frontend UI

## Overview

Implement a fast Astro public site that consumes WordPress via `/graphql`, keeps client JS minimal, and follows the repo’s UI style requirements. Focus on file outputs under `frontend/` and a small GraphQL client.

## Workflow

1. Inspect existing `frontend/` files for Astro + Tailwind v4 setup and adjust only within that subtree.
2. Ensure `frontend/Dockerfile`, `package.json`, and `astro.config.mjs` align with Tailwind v4 via Vite and dev server on `0.0.0.0:4321`.
3. Implement `src/lib/cms.ts` with endpoint resolution and two GraphQL queries.
4. Build pages (`/`, `/blog`, `/blog/[slug]`) in Astro with card-based UI and graceful empty states.
5. Use React islands only for interactive widgets, and keep everything else server-rendered.

## Non-Negotiables

- Use Tailwind CSS v4 via the Vite plugin; do not use deprecated Astro Tailwind integration.
- Keep JS minimal and limit React to islands only.
- UI style: clean, card-based, generous spacing, 2xl radii, subtle shadows.

## Default Stack

- Use `react` + `react-dom` only for islands.
- Use shadcn/ui components (Button/Card/Dialog/Dropdown) when interaction is needed.
- Use `lucide-react` icons as needed.
- Use `sonner` for toasts if useful.
- Use `graphql-request` or an equivalent tiny GraphQL client.

## Required Outputs

- Create or update under `frontend/`:
  - `Dockerfile`
  - `package.json`
  - `astro.config.mjs`
  - `src/lib/cms.ts`
  - `src/pages/index.astro`
  - `src/pages/blog/index.astro`
  - `src/pages/blog/[slug].astro`
  - `src/components/*` (Header, Footer, PostCard, Hero, FeatureGrid, CTA)

## Data Layer

- CMS endpoint is `${PUBLIC_CMS_URL || ASTRO_PUBLIC_CMS_URL}/graphql`.
- Provide queries:
  - list posts: `title`, `slug`, `excerpt`, `date`
  - post by slug: `title`, `content`, `date`
- Handle empty states for no posts.

## Acceptance Checklist

- `http://localhost:8080/` renders home.
- `/blog` renders list or empty state.
- `/blog/<slug>` renders content when posts exist.
- No unnecessary client JS outside islands.
