---
name: fft-farm-validate
description: Validate production readiness for farm control: HA connectivity/auth, required mappings, service availability, and dashboard path checks.
---

# FFT Farm Validate

Use this skill to enforce control safety gate in production.

## Workflow

1. Run:
   - `./scripts/farm-validate.sh`
2. Review pass/fail output.
3. If failed, fix listed issues and rerun.

## Gate Behavior

- In `FARM_MODE=production`, host-side control actions are blocked unless profile `validation.status` is `pass`.
- Read-only actions remain available before validation.
