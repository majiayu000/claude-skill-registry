---
name: autonomous-ui-inspection
description: Autonomous UI inspection using a dual channel: (1) visual screenshots via Playwright MCP tools, (2) numeric layout metrics via Puppeteer scripts. Includes server --check standardization so agents can start/stop reliably.
---

# Autonomous UI Inspection

## Scope

Use this Skill when you need a **reliable, agent-friendly view of what the UI renders**:

- **Visual**: screenshots + accessibility snapshots (Playwright via MCP)
- **Numeric**: bounding boxes, computed styles, text overflow, and connection geometry (Puppeteer)

This Skill is about **inspection and evidence collection**. It intentionally avoids styling tweaks unless the inspection workflow itself is broken.

## Inputs

- Which UI surface (server path + URL route)
- Whether the UI is SSR-only or needs client activation
- A stable selector that indicates “ready” (e.g. `.dt-node`, `[data-role="diagram-shell"]`)
- Desired viewport and whether you need a clipped screenshot

## Procedure

### A) Standardize server start/stop (mandatory)

1. Prefer server `--check` for quick validation:

- `node src/ui/server/<feature>/server.js --check`

2. If `--check` is missing or hangs, implement it using:

- `src/ui/server/utils/serverStartupCheck.js`

Canonical workflow + implementation guidance lives in:

- `docs/COMMAND_EXECUTION_GUIDE.md` → "🚨 Server Verification - CRITICAL FOR AGENTS 🚨"

Why: agents must be able to validate startup **without** long-lived processes blocking.

### B) Visual inspection (Playwright MCP)

Goal: get screenshots that an agent can “see”, plus a structural snapshot.

1. Start the UI server (one of):

- Preferred: run the feature server in a dedicated terminal (or background task)
- For Decision Tree Viewer: `node scripts/ui/start-decision-tree-for-mcp.js`

2. Navigate via MCP browser tool to the URL.

3. Capture:

- Full-page screenshot (baseline)
- Optional clipped screenshot (if a stable container selector exists)
- Accessibility snapshot for structure + quick DOM sanity

Notes:
- Use consistent viewport dimensions (example: 1600x1200) to reduce diff noise.
- If the UI is interactive, capture “before” and “after” screenshots for a single canonical interaction.

### C) Numeric inspection (Puppeteer)

Goal: compute layout facts agents can diff and enforce.

Run a dedicated Puppeteer script that:

- Starts the server on a random or fixed dev port
- Waits for a deterministic “ready” selector
- Extracts metrics:
  - `getBoundingClientRect()` for key elements
  - `scrollWidth/Height` vs `clientWidth/Height` for overflow
  - computed styles for typography + spacing

For Decision Tree Viewer:

- `node scripts/ui/inspect-decision-tree-layout.js`

Typical invariants to enforce:
- Node label text is not overflowing (`isOverflowing === false`)
- Bounding boxes are within expected ranges
- Connection endpoints exist for all connectors

### D) Escalation: single-browser scenario suites

If you need multiple interactions but want fast runs:

- Use a scenario suite runner (single browser, many scenarios) rather than N× Jest/Puppeteer startups.

## Validation / Evidence Checklist

- Server `--check` exits with 0
- At least one screenshot captured and stored under `screenshots/` or `.playwright-mcp/`
- Numeric JSON output captured (stdout or written artifact)
- A “ready selector” exists and is documented for the UI

## References

- Workflow guide: `docs/workflows/ui-inspection-workflow.md`
- Startup check utility: `src/ui/server/utils/serverStartupCheck.js`
- Puppeteer efficient verification: `docs/agi/skills/puppeteer-efficient-ui-verification/SKILL.md`
- Puppeteer scenario suites: `docs/guides/PUPPETEER_SCENARIO_SUITES.md`
- One-shot console capture: `docs/guides/PUPPETEER_UI_WORKFLOW.md`
- Hanging prevention: `docs/guides/TEST_HANGING_PREVENTION_GUIDE.md`
