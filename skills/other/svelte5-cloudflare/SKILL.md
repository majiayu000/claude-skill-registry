---
name: svelte5-cloudflare
description: Deploy and operate Svelte 5 + SvelteKit projects on Cloudflare Workers safely.
Use when adding server routes, configuring adapters, setting Wrangler secrets,
deploying with CLI, or debugging waitlist/form flows that proxy to external services.
Prevents common mistakes: wrong adapter, wrong wrangler command target (Pages vs Worker),
missing entrypoint/assets, missing runtime secrets, and false-positive submission success.

category: hot
user-invocable: true
---

# Svelte5 + Cloudflare

Use this skill for any SvelteKit-on-Cloudflare task.

## What To Do First

1. Identify runtime model before touching config:
- `Worker service`: use `wrangler secret put` and `wrangler deploy`.
- `Pages project`: use `wrangler pages secret put` and Pages build output config.
2. Run `scripts/doctor.sh` from this skill and follow fixes in order.
3. If user asks for “latest” behavior/tools, verify with official docs before advising.

## Guardrails (Do Not Skip)

1. Do not use `mode: 'no-cors'` to hide integration errors.
2. For SvelteKit API routes, prefer same-origin POST from frontend to `/api/...`.
3. Validate server input and treat upstream logical errors as failures.
4. Keep secrets in Cloudflare secrets, never in git or `[vars]` for sensitive values.
5. For Worker deploys of SvelteKit cloudflare output, deploy both worker entry and assets.

## Standard Implementation Pattern

### A) SvelteKit Cloudflare config

- Adapter: `@sveltejs/adapter-cloudflare`
- Build output used for manual worker deploy: `.svelte-kit/cloudflare`
- Worker entry file: `.svelte-kit/cloudflare/_worker.js`

### B) Waitlist/form backend pattern

- Frontend posts to same-origin `/api/waitlist` with `URLSearchParams`.
- API route validates fields, enforces honeypot, forwards upstream server-side.
- API route returns structured errors:
  - `400` validation
  - `503` missing env
  - `502` upstream/network failure

### C) Cloudflare secrets and deploy

- Worker service secret:
  - `npx wrangler secret put GOOGLE_APPS_SCRIPT_URL --name <worker-name>`
- Worker deploy for SvelteKit output:
  - `npx wrangler deploy .svelte-kit/cloudflare/_worker.js --name <worker-name> --assets .svelte-kit/cloudflare`

## Decision Tree: Pages vs Worker

- If dashboard route is `workers.dev` and shows Worker versions, treat as Worker service.
- If using Pages project/deployments pipeline, treat as Pages.
- If unsure, run both list commands and use whichever returns the target.

## Auto-Maintenance Protocol (Living Skill)

Run `scripts/refresh-skill-state.sh` whenever:
- SvelteKit/adapter/wrangler versions change
- Deploy command changes
- Pages/Worker mode changes
- A new incident is discovered

Then update `references/playbook.md` with:
1. New failure symptom
2. Root cause
3. Detection command
4. Minimal fix

When this skill is invoked, agents should proactively run `scripts/doctor.sh` and patch drift before feature work.

## References

- Operational playbook: `references/playbook.md`
- Drift/state snapshot: `references/state.json`