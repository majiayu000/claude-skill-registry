---
name: mova-workflow-author-v0
description: Use for creating new packs/workflows, adding domains/workers, or adding quality/neg suites with station-compatible scripts.
allowed-tools: Bash, Read, Grep, Glob
---

## Creation
- Pack skeleton: define ds/env/runtime/examples, scripts, and quality pos/neg suites.
- Keep structure minimal and deterministic; reuse existing conventions.

## Integration
- Add npm scripts for A/B runs, compare, and quality suites.
- If a domain worker is added, include E2E smoke through gateway where applicable.
- External actions in examples/demos must go through a Gateway path using `mova_run_envelope_v0`, not direct SDK/HTTP calls.

## Definition of Done
- `npm run validate`
- `npm test`
- If available: `npm run smoke:*`
- Evidence artifacts saved under `artifacts/**` and referenced in output.
