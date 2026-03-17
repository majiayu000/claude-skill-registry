---
name: web-stack-planner
description: Collect project brief and stack choices, then output canonical project-config.json for downstream web-builder skills.
compatibility: codex, claude-code, claude-ai, agent-skills
license: Apache-2.0
allowed-tools:
  - read_file
  - write_file
  - run_terminal_cmd
  - web_search
metadata:
  category: web-builder
  stage: 1-planning
  pipeline: web-builder
---

# Web Stack Planner

## Objective

Capture a complete web project brief and produce a validated `project-config.json`
that all downstream `web-builder` skills consume.

## Required Workflow

1. Ask the user for project name, project type, target audience, authentication needs, and whether any codebase already exists.
2. Present frontend framework choices:
   - React
   - Next.js
   - Vue
   - Nuxt
   - SvelteKit
   - Angular
   - Astro
   - plain HTML/CSS/JS
3. Present backend/API choices:
   - Node.js/Express
   - FastAPI
   - Django
   - Laravel
   - Go/Gin
   - Rails
   - Supabase Edge Functions
   - serverless-only
4. Present database choices:
   - PostgreSQL
   - MySQL
   - MongoDB
   - SQLite
   - Supabase
   - PlanetScale
   - Turso
   - Redis (as cache)
   - Firebase
5. Present CSS/design system choices:
   - Tailwind CSS
   - Shadcn/ui
   - Chakra UI
   - Material UI
   - Ant Design
   - Mantine
   - DaisyUI
   - vanilla CSS
6. Ask if they need integrations for auth, payments, email, file storage, and i18n:
   - Auth: Clerk, Auth.js, Supabase Auth, custom JWT
   - Payments: Stripe, Paddle, LemonSqueezy
   - Email: Resend, SendGrid
   - Storage: S3, Supabase Storage, Cloudflare R2
7. Ask deployment target:
   - Vercel
   - Netlify
   - Fly.io
   - Railway
   - Render
   - AWS
   - GCP
   - Azure
   - DigitalOcean
   - Cloudflare Pages
8. Run `scripts/stack_planner.py` to validate and write the canonical `project-config.json`.

## Execution

```bash
python skills/web-stack-planner/scripts/stack_planner.py --input <brief.json> --output <out.json> --format json
```

## Output

- `project-config.json`
- Script result file (`json`, `md`, or `csv`) with `status`, `summary`, `artifacts`, and `details`

## References

- `references/tools.md`
