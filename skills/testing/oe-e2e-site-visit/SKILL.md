---
name: oe-e2e-site-visit
description: End-to-end verification for the site-visit (Step 7) flow. Use when you need to reproduce or validate that the system reaches the site-visit prompt/options and can proceed to confirmation, either via deterministic backend-only traces (manual_ux_scenario_I/H) or via browser UI checks (Playwright/MCP).
---

# oe-e2e-site-visit

## Deterministic lane (fast, backend-only)

Use this lane first to prove workflow correctness without UI variability.

1. Generate a trace that includes the site-visit flow:
   - `python3 scripts/manual_ux_scenario_I.py > /tmp/ux_site_visit_I.json`
   - (optional variant) `python3 scripts/manual_ux_scenario_H.py > /tmp/ux_site_visit_H.json`

2. Validate the trace invariants (fails fast with a precise message):
   - `python3 scripts/validate_manual_ux_run.py /tmp/ux_site_visit_I.json --require_site_visit`

3. If validation fails:
   - Identify the first record whose `action` indicates the break (search `confirmation_site_visit` / `confirmation_site_visit_sent` in the trace).
   - Correlate with Step 7 routing and state machine:
     - `backend/workflows/steps/step7_confirmation/trigger/step7_handler.py`
     - `backend/workflows/runtime/pre_route.py`

## Browser lane (UI correctness)

Use this when you need to confirm the frontend shows the site-visit message/options.

1. Start backend:
   - `./scripts/dev_server.sh start`

2. Start frontend:
   - `cd atelier-ai-frontend && npm run dev`

3. Drive the UI until the site-visit step appears:
   - Prefer Playwright MCP (agent can inspect DOM, click actions, and capture screenshots).
   - Otherwise, do manual browser steps and capture screenshots in `.playwright-mcp/`.

## Evidence capture (for PRs / debugging agents)

- Attach:
  - the trace file (`/tmp/ux_site_visit_*.json`)
  - the validator output
  - a UI screenshot when using the browser lane.

