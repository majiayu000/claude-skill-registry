---
name: web-backend-builder
description: Scaffold backend API, data models, ORM setup, and endpoint inventory with OpenAPI output.
compatibility: codex, claude-code, claude-ai, agent-skills
license: Apache-2.0
allowed-tools:
  - read_file
  - write_file
  - run_terminal_cmd
  - web_search
metadata:
  category: web-builder
  stage: 4-backend
  pipeline: web-builder
---

# Web Backend Builder

## Objective

Scaffold a backend foundation from `project-config.json` including data model
planning, ORM recommendations, API endpoint inventory, and OpenAPI output.

## Required Workflow

1. Read `project-config.json`.
2. Scaffold the selected backend framework (FastAPI, Express, Django, Gin, and other configured options).
3. Define data models from project type and ask for missing entities when unclear.
4. Configure ORM/query layer guidance:
   - Prisma (Node.js)
   - Drizzle ORM (TypeScript)
   - SQLAlchemy (FastAPI/Python)
   - Mongoose (MongoDB)
5. Scaffold CRUD endpoints, auth middleware, and file upload handlers.
6. If Supabase is selected, include `@supabase/supabase-js`, RLS policy planning, and Edge Function notes.
7. Enforce environment variable setup with `.env.example` and no committed secrets.
8. Generate `openapi.yaml` covering all endpoints.
9. Output backend scaffold artifacts, `openapi.yaml`, and `backend-report.json`.

## Execution

```bash
python skills/web-backend-builder/scripts/backend_builder.py --input <workspace> --output <out.json> --format json
```

## References

- `references/tools.md`
