---
name: fft-farm-bootstrap
description: Bootstrap farm mode in demo or production, including Home Assistant startup, token onboarding, env wiring, and handoff to onboarding/validation.
---

# FFT Farm Bootstrap

Use this skill when a user wants first-time farm setup to be frictionless.

## Guardrails

- Never run destructive git commands unless explicitly requested.
- Preserve unrelated worktree changes.
- Do not expose tokens in logs or chat responses.

## Workflow

1. Run:
   - `./scripts/farm-bootstrap.sh --mode demo`
   - or `./scripts/farm-bootstrap.sh --mode production`
2. If mode is production, bootstrap will hand off to onboarding + validation scripts.
3. Confirm `.env` has:
   - `FARM_MODE`
   - `FARM_PROFILE_PATH`
   - `FARM_STATE_ENABLED=true`
   - `HA_URL`, `HA_TOKEN`, `FFT_DASHBOARD_REPO_PATH`

## Notes

- Home Assistant stack is Docker/Compose-based.
- FFT_nano agent runtime remains Apple Container/Docker auto detection.
- Browser-assisted token generation is expected.
