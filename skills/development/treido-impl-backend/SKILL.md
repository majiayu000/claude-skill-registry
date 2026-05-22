---
name: treido-impl-backend
description: "Backend implementer for Treido (patches code). Executes audit findings/tasks for actions/routes/webhooks with caching + Supabase rails. Trigger: BE-IMPL"
---

# Treido Backend Implementer (Writes Code)

You patch files. Only proceed if you are the designated single writer for this batch.

## Workflow

1. Read `TASKS.md` + linked audit artifact under `audit/`.
2. Implement a 1–3 file batch; avoid unrelated refactors.
3. Rails: no secrets/PII in logs; avoid `select('*')`; Stripe webhooks signature-verified + idempotent; cached-server rules.
4. Verify.

## Verification (Always)

```bash
pnpm -s typecheck
pnpm -s lint
```

