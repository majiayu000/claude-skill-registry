---
name: fft-setup
description: Setup and bootstrap FFT_nano on macOS or Linux, including container runtime checks, dependency install/build, env wiring for Pi provider credentials, and first-run startup validation.
---

# FFT Setup

Use this skill when the task is to install, bootstrap, or verify FFT_nano runtime setup.

## Scope

- Host prerequisites (Node 20+, npm, container runtime)
- First-time bootstrap via project scripts
- Provider/env setup for Pi runtime inside the container
- First run validation for Telegram and/or WhatsApp

## Guardrails

- Never run destructive git commands (`git reset --hard`, `git checkout --`, force-push) unless explicitly requested.
- Preserve unrelated worktree changes.
- Keep admin/delegation operations constrained to the main chat only.

## Setup Flow

1. Verify prerequisites:
   - `node -v` (must be v20+)
   - `npm -v`
   - macOS: `container --version` (Apple Container) or `docker --version`
   - Linux: `docker --version`
2. Bootstrap with project script:
   - `./scripts/setup.sh`
3. Populate `.env` from `.env.example` and fill provider vars.
4. If WhatsApp is enabled, run one-time auth:
   - `npm run auth`
5. Start service:
   - Dev: `./scripts/start.sh dev`
   - Dev Telegram-only: `./scripts/start.sh dev telegram-only`
   - Prod: `./scripts/start.sh start`

## Provider Wiring (Pi runtime in container)

Preferred variables in `.env`:

- `PI_API`
- `PI_MODEL`
- `PI_API_KEY` (or provider-specific keys like `ZAI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`)
- Optional: `PI_BASE_URL`

Example (Z.AI/GLM):

```dotenv
PI_API=zai
PI_MODEL=glm-4.7
ZAI_API_KEY=replace-me
```

## Platform Notes

### macOS

- Runtime auto-prefers Apple Container when available.
- If Apple Container is installed but stopped, run:
  - `container system start`
- If networking stalls/timeouts occur:
  - `container system stop && container system start`

### Linux

- Runtime uses Docker by default.
- Ensure daemon is running before start:
  - `docker info`

## Setup Verification Checklist

- `npm run typecheck` passes.
- `npm test` passes.
- Service starts without startup exceptions.
- Telegram mode: `/status` responds.
- Main chat behavior is correct:
  - main chat responds to normal messages
  - non-main chat requires `@FarmFriend` (or configured `@<ASSISTANT_NAME>`)

## Farm Mode Handoff

For farm bridge onboarding, use the dedicated dual-mode bootstrap:

- Demo (simulated telemetry + showcase): `./scripts/farm-bootstrap.sh --mode demo`
- Production (real devices + mapping + validation): `./scripts/farm-bootstrap.sh --mode production`
