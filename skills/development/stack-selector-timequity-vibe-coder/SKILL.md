---
name: stack-selector
description: |
  Automatically choose the best tech stack based on requirements. User never sees this.
  Use when: starting a new project after idea validation.
  Triggers: internal use only, called by build pipeline.
---

# Stack Selector

Choose tech stack automatically. User doesn't decide.

## Decision Tree

```
What type of app?
├─ Web app with auth/db
│  ├─ Needs real-time? → nextjs-supabase (Supabase realtime)
│  ├─ Heavy backend logic? → fastapi-postgres
│  └─ Default → nextjs-supabase
│
├─ API/Backend only
│  ├─ Python/ML focus? → fastapi-postgres
│  └─ Edge/serverless? → hono-drizzle
│
├─ Landing page / Marketing
│  └─ → landing-page (static)
│
└─ Unsure → nextjs-supabase (most flexible)
```

## Templates

| Template | Stack | Best For |
|----------|-------|----------|
| nextjs-supabase | Next.js 15, Supabase, Tailwind | Web apps, SaaS, dashboards |
| fastapi-postgres | FastAPI, PostgreSQL, SQLAlchemy | APIs, ML backends |
| hono-drizzle | Hono, Drizzle, Cloudflare | Edge, serverless |
| landing-page | Astro, Tailwind | Marketing, portfolios |

## Selection Criteria

| Requirement | Template |
|-------------|----------|
| "auth", "login", "users" | nextjs-supabase |
| "api", "backend", "python" | fastapi-postgres |
| "fast", "edge", "serverless" | hono-drizzle |
| "landing", "marketing", "simple" | landing-page |
| "dashboard", "admin" | nextjs-supabase |
| "ml", "ai", "data" | fastapi-postgres |

## Usage

Called internally by `/mvp:build`:

1. Analyze PRD from idea-validation
2. Match requirements to criteria
3. Select template
4. Generate project from template

User sees: "Setting up your project..." (not the decision)
