---
name: nostrstack-dev-workflow
description: Local development workflow for nostrstack, including running API/gallery with logs, regtest stack usage, MCP Chrome DevTools verification, QA fallback, and environment/setup troubleshooting. Use when starting dev, debugging, reproducing issues, or validating UI/console/network behavior in the nostrstack repo.
---

# Nostrstack Dev Workflow

Follow this workflow when working in the nostrstack repo.

## Core workflow

- Read `references/dev-workflow.md` for the required log + UI verification steps.
- Keep API + gallery logs visible while reproducing and fixing.
- For UI changes, verify in Chrome DevTools MCP; if MCP is unavailable, run the Playwright QA fallback.

## Commands checklist

- Start logs: `pnpm dev:logs` (or `make dev`) and tail `.logs/dev/api.log` + `.logs/dev/gallery.log`.
- MCP Chrome bridge: `./scripts/mcp-devtools-server.sh` + `./scripts/mcp-chrome.sh`.
- QA fallback: `pnpm qa:regtest-demo`.

## When to read more

- Troubleshooting MCP: `references/mcp-setup.md`.
- Local demo/regtest flows: `references/local-demo.md`.
- Testing matrix and env: `references/testing.md`.
