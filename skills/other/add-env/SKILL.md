---
name: add-env
description: Add an environment variable to .env.example and provide guidance for env.ts and CLAUDE.md
---

# Add Environment Variable Skill

Add a new environment variable to `.env.example` and provide instructions for the manual updates needed in `env.ts` and `CLAUDE.md`.

## Arguments

The user provides:

- Variable name (SCREAMING_SNAKE_CASE, e.g., `STRIPE_SECRET_KEY`)
- Description of what it's for
- Whether it's required or optional
- Default value (if any)
- Validation constraints (URL, min length, starts with prefix, etc.)

## What This Skill Edits

**Only `.env.example`** — add the variable with a descriptive comment and placeholder value.

```bash
# Description of what this variable does
MY_VAR=your-value-here

# Stripe secret key (starts with sk_)
STRIPE_SECRET_KEY=sk_test_...

# Optional: Analytics tracking ID
# ANALYTICS_ID=
```

For optional variables, comment out the line so it's visible but not active by default.

## What to Tell the User (do NOT edit these files)

After updating `.env.example`, inform the user they need to manually update two more files:

### 1. `apps/api/src/lib/env.ts` — Zod Validation

Tell the user to add the variable to the `envSchema` object. Provide the exact Zod line:

```typescript
// Required string
MY_VAR: z.string().min(1),

// Required with constraint
STRIPE_SECRET_KEY: z.string().startsWith('sk_'),

// Required URL
WEBHOOK_URL: z.string().url(),

// Optional
ANALYTICS_ID: z.string().optional(),

// With default
MY_URL: z.string().url().default('http://localhost:3000'),

// Coerce to number
MAX_CONNECTIONS: z.coerce.number().default(10),
```

### 2. `CLAUDE.md` — Environment Variables Table

Tell the user to add a row:

```markdown
| `MY_VAR` | Description | Yes/No |
```

## Important Notes

- `env.ts` validates eagerly at import time — the app crashes immediately if a required variable is missing
- Tests must set `process.env.VAR ??= 'dummy'` BEFORE importing any module that imports `env.ts`
- If the variable is required, the test preload file also needs updating

## Workflow

1. Read `.env.example` to see existing format
2. Add the variable with a descriptive comment and placeholder
3. Tell the user the exact lines to add to `env.ts` and `CLAUDE.md`
4. If variable is required, remind the user to update test preload too
