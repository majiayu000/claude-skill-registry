---
name: nostrstack-lightning
description: Lightning/LNbits integration for nostrstack, including regtest flows, staging/prod config, observability, and payment/zap behavior. Use when editing payment flows, Lightning provider code, or running LNbits-related tests.
---

# Lightning + LNbits

Use this skill for Lightning/LNbits work in `apps/api` and related docs.

## Workflow

- Read `references/regtest-flows.md` for local payment/zap flows.
- Read `references/env-and-ops.md` for staging/prod notes and observability.
- Check `references/testing.md` for smoke/E2E commands.

## Guardrails

- Do not paste or commit secrets from ops docs.
- Preserve webhook flow and payment state transitions.
- Ensure regtest flags are aligned between API and gallery when testing.
