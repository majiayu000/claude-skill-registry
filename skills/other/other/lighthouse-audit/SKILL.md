---
name: lighthouse-audit
description: Run Lighthouse performance audits against locally served pages and summarize key metrics. Use when the user asks to check Lighthouse scores, Core Web Vitals, or performance regressions for new or specified routes (local dev/preview), or to complement DevTools MCP performance traces.
---

# Lighthouse Audit

## Overview
Audit one or more local routes with Lighthouse, then summarize key metrics and optional DevTools MCP performance traces.

## Inputs to confirm
- baseUrl: default `http://localhost:3000`
- routes: list of paths (e.g. `/pricing`) or full URLs
- preset: `mobile` (default) or `desktop`
- runs: optional repeat count for more stable scores
- mode: dev (`pnpm dev`) or prod (`pnpm build && pnpm start`)

If the user says "new page", ask for the route if it is not already known.

## Workflow
1. Ensure the local server is running
   - Prefer production-like results: `pnpm build && pnpm start`
   - Quick iteration: `pnpm dev`
2. Run Lighthouse CLI via the bundled script
   - Single route:
     `python3 .claude/skills/lighthouse-audit/scripts/run_lighthouse.py --route "/pricing"`
   - Multiple routes:
     `python3 .claude/skills/lighthouse-audit/scripts/run_lighthouse.py --routes "/,/pricing,/blog" --preset desktop --runs 3`
   - Full URL:
     `python3 .claude/skills/lighthouse-audit/scripts/run_lighthouse.py --url "http://localhost:3000/pricing"`
   - Reports are written under `/.lighthouse/<slug>/<preset>/<timestamp>/report.json`
3. Optional: capture a DevTools MCP performance trace for deeper analysis
   - `mcp__chrome-devtools__new_page` to open the URL
   - `mcp__chrome-devtools__performance_start_trace` with `reload: true`, then `mcp__chrome-devtools__performance_stop_trace`
   - Use trace insights to explain bottlenecks that align with Lighthouse findings
4. Report results
   - Provide performance score and key metrics (FCP, LCP, CLS, TBT, Speed Index, TTI/INP)
   - Call out regressions vs previous runs when available
   - Suggest fixes tied to the worst metrics

## Resources
- `scripts/run_lighthouse.py`: runs Lighthouse locally and prints a metric summary
