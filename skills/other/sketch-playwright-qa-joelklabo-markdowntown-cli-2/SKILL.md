---
name: sketch-playwright-qa
description: Playwright QA workflow for Sketch Magic. Use when running mobile flow tests, visual baselines, snapshot updates, or debugging flaky WebKit/Chromium runs and port conflicts.
---

# Sketch Playwright QA

## Overview
Standardize Playwright test runs for mobile flow and visual baselines, including snapshot updates and trace review.

## Quick Start
- Mobile flow: `PLAYWRIGHT_PORT=3020 pnpm test:e2e tests/e2e/mobile-flow.spec.ts`
- Visual baselines: `PLAYWRIGHT_PORT=3021 pnpm test:e2e tests/e2e/visual.spec.ts`
- Update snapshots: append `--update-snapshots`

## Workflow

### 1) Pick a port
- Use a clean port (e.g., 3020–3030) to avoid conflicts.
- Set `PLAYWRIGHT_PORT` in the command.

### 2) Run required suites
- Mobile flow: `tests/e2e/mobile-flow.spec.ts`
- Visual baselines: `tests/e2e/visual.spec.ts`

### 3) Handle failures
- Review trace/video artifacts under `test-results/`.
- If a snapshot mismatch is expected, re-run with `--update-snapshots`.
- If flakiness appears, check animations or timing.

### 4) Record evidence
- Keep a short log of commands + ports used.
- Capture failing screenshots/videos when needed.
- Use `qa-verification` for the standard evidence format.

## References
- `references/playwright-workflow.md` — exact commands, snapshot guidance, and troubleshooting.
