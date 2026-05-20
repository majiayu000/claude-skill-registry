---
name: web-auth-integrator
description: Integrate authentication and authorization flows with provider-specific setup and RBAC safeguards.
compatibility: codex, claude-code, claude-ai, agent-skills
license: Apache-2.0
allowed-tools:
  - read_file
  - write_file
  - run_terminal_cmd
  - web_search
metadata:
  category: web-builder
  stage: 5-auth
  pipeline: web-builder
---

# Web Auth Integrator

## Objective

Implement authentication and authorization end-to-end based on
`project-config.json`.

## Required Workflow

1. Read `project-config.json` and determine auth provider.
2. For Clerk:
   - install `@clerk/nextjs` or `@clerk/clerk-react`
   - wrap app with `ClerkProvider`
   - protect routes with auth middleware
   - configure Clerk webhooks
3. For Auth.js / NextAuth:
   - configure providers (Google, GitHub, credentials)
   - choose JWT or DB sessions
   - protect API routes and pages
4. For Supabase Auth:
   - use `supabase.auth`
   - configure OAuth providers
   - configure magic links
5. For custom JWT:
   - scaffold `/auth/register`, `/auth/login`, `/auth/refresh`
   - hash passwords with bcrypt
   - sign/verify JWTs (`jose` or `jsonwebtoken`)
   - implement refresh-token rotation
6. Implement RBAC middleware.
7. Add CSRF protection and secure cookie flags (`HttpOnly`, `SameSite=Strict`, `Secure`).
8. Output auth integration artifacts and `auth-report.json`.

## Execution

```bash
python skills/web-auth-integrator/scripts/auth_integrator.py --input <workspace> --output <out.json> --format json
```

## References

- `references/tools.md`
