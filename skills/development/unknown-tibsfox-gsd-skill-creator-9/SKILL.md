---
name: env-setup
description: Environment configuration and secrets management. Use when setting up .env files, managing secrets, or configuring environments.
version: 1.0.0
format: 2025-10-02
triggers:
  - setting up
updated: 2026-04-25
status: ACTIVE
---

# Environment Configuration

## Non-Negotiable Rules

| Rule | Why |
|------|-----|
| NEVER commit .env to git | Secrets persist in history forever |
| NEVER log secret values | Logs stored in plain text, forwarded |
| NEVER hardcode secrets | Source code is widely shared |
| ALWAYS use .env.example | Documents vars without exposing values |
| ALWAYS add .env* to .gitignore FIRST | Prevents accidental commit |
| ALWAYS validate config at startup | Fail fast, not hours into production |

## .gitignore (add before creating .env)

```gitignore
.env
.env.*
!.env.example
*.pem
*.key
credentials.json
```

## Naming Conventions

- UPPER_SNAKE_CASE: `DATABASE_URL`, `JWT_SECRET`
- Prefix by service: `DB_`, `REDIS_`, `AWS_`
- Booleans: `ENABLE_CACHE=true` (not 1/yes)
- Feature flags: `FEATURE_*`

## Key Patterns

- **No defaults for secrets** — force explicit configuration
- **Validate at startup** with Zod/Joi/Pydantic, not at first use
- **Unique secrets per environment** — one leak shouldn't compromise all
- **Rotate leaked secrets immediately** — check git history, audit access logs
- **Process env always wins** — CI/CD overrides file-based config
