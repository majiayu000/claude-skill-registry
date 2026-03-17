---
name: miniapp-edit-testing
description: Test and debug the Dashboard “Edit with AI” mini-app editor flow (start edit session, build, history, close session) and write automated tests that simulate agent-driven mini-app edits like adding dark mode.
---

# Mini-app editor testing (Edit with AI)

Use this when you need to validate that mini-app editing works end-to-end (or via integration tests) from the Dashboard’s “Edit with AI” action, including common changes like adding **dark mode**.

## What to test

- The Dashboard client calls the mini-app editor endpoints (example: `POST /api/apps/:appName/edit`) with the user prompt.
- The server validates inputs (app name format, prompt length) and forwards to the edit-service.
- The response contains `sessionId`, `commitHash`, `portalUrl`, and `buildStatus`.

## Recommended test strategy (fast + deterministic)

- Prefer **route-level integration tests** with a mocked edit service:
  - Mock `startEditSession(appName, prompt, createNew)` and `continueEdit(sessionId, prompt)`
  - Assert the route returns the expected JSON shape and HTTP status codes
  - Avoid requiring a real OpenCode server or real git worktrees for CI stability

## Useful repo pointers

- Dashboard frontend API client functions live in `packages/dashboard/frontend/src/api.ts` (look for `editApp`, `buildApp`, `getHistory`, `closeSession`).
- The “Edit with AI” UI lives under `packages/dashboard/frontend/src/components/MiniAppEditor/`.
- Mini-app edit routes may be disabled/stubbed in the Dashboard server; if editor endpoints return 404/503, check the Dashboard router wiring in `packages/dashboard/src/server/routes.ts`.

## Debug checklist (when edits fail)

- If you see **502** from `/api/apps/:appName/edit`, verify the upstream service is running and the Dashboard route is mounted.
- If the editor modal errors immediately, check browser console + network response body for `{ error, message }`.
