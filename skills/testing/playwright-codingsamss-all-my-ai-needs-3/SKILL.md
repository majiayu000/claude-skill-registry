---
name: "playwright"
description: "Use when the task requires automating a real browser. This skill is MCP-only and uses `playwright-ext` (`@playwright/mcp --extension`) to attach to the browser extension session."
---


# Playwright MCP Skill

Use Playwright as the reliable browser execution layer in a three-layer stack:
- Scrapling: extraction-first
- PinchTab: low-token browser inspection and lightweight interaction
- `playwright-ext`: reliable browser execution

Use a single channel only:
- Always use `playwright-ext` MCP.
- Do not use `playwright-cli` wrapper in this skill.
- Do not pivot to `@playwright/test` unless the user explicitly asks for test files.

## Role In The Stack

Prefer Scrapling when:
- the task is mainly scraping, parsing, or structured extraction.
- HTTP or dynamic fetchers can solve the page without a browser-first workflow.

Prefer PinchTab when:
- the user mainly needs quick browser inspection, page text, or lightweight tab/session steps.
- low-token page probing is enough to make the next decision.

Choose Playwright when:
- the workflow is interaction-heavy and must be verified step by step.
- success depends on stable refs, precise DOM transitions, or repeated re-snapshot control.
- upstream tools already proved that a lighter layer is not reliable enough for the current task.

## Prerequisite check (required)

Before proposing browser actions, verify MCP and runtime dependency:

```bash
codex mcp get playwright-ext
command -v npx >/dev/null 2>&1
```

If `playwright-ext` is missing, configure it with extension token:

```bash
codex mcp add playwright-ext \
  --env PLAYWRIGHT_MCP_EXTENSION_TOKEN=<token> \
  -- npx @playwright/mcp@latest --extension
```

If `npx` is missing, ask the user to install Node.js/npm:

```bash
node --version
npm --version
brew install node
```

## Core workflow

1. Confirm that the task truly needs reliable browser execution rather than lighter extraction or inspection layers.
2. Open the page.
3. Snapshot to get stable element refs.
4. Interact using refs from the latest snapshot.
5. Re-snapshot after navigation or significant DOM changes.
6. Verify page state after each important action.
7. Capture artifacts (screenshot, pdf, traces) when useful.

## Takeover Rules

Take over from Scrapling or PinchTab when:
- the current layer cannot prove that the intended page state change really happened.
- login/session flow, modal flow, or multi-step navigation needs strong ref discipline.
- the workflow has become complex enough that repeated browser verification is cheaper than continued fallback guessing.

When Playwright takes over, say why it is now required and keep the flow inside Playwright until the critical interaction is verified.

If taking over from PinchTab failure, require brief triage evidence before takeover:
- `pinchtab health`, `pinchtab instances`, and one smoke test result (or equivalent evidence)
- categorize the switch reason as one of: `service-down`, `auth-blocked`, `capability-gap`, `higher-repair-cost`
- include one concise handoff note in user-facing progress updates

## When to snapshot again

Snapshot again after:

- navigation
- clicking elements that change the UI substantially
- opening/closing modals or menus
- tab switches

Refs can go stale. When a command fails due to a missing ref, snapshot again.

## Troubleshooting: extension bridge failures

If `playwright-ext` fails with `Extension connection timeout`:

1. Check whether Chrome opened `chrome-extension://.../connect.html`.
2. If the page shows `Invalid token provided`, the extension token in config does not match the installed extension session token (or has expired/rotated).
3. Reconfigure the MCP server with the correct `PLAYWRIGHT_MCP_EXTENSION_TOKEN`.
4. Important: if you changed token/config mid-conversation, existing MCP connections can stay stale. Start a fresh Hermes process/session (or restart) before judging whether the fix worked.
5. Validate in two layers:
   - `hermes mcp test playwright-ext` verifies server startup and tool discovery only.
   - Execute a real bridge tool call (for example `mcp_playwright_ext_browser_tabs` in a fresh session) to verify extension handshake actually works.
6. If browser-side bridge is unavailable, do not keep retrying blindly; switch to non-browser methods when the task does not require UI interaction.

## Guardrails

- Do not position Playwright as the default first hop when Scrapling or PinchTab can solve the task more cheaply.
- For repository understanding tasks (e.g., "what is this GitHub repo about"), prefer non-browser methods first (`git clone` + README/metadata inspection). Only escalate to Playwright if page interaction is actually required.
- Always snapshot before referencing element ids like `e12`.
- Re-snapshot when refs seem stale.
- Prefer explicit commands over `eval` and `run-code` unless needed.
- When you do not have a fresh snapshot, use placeholder refs like `eX` and say why; do not bypass refs with `run-code`.
- State the takeover reason when inheriting a task from Scrapling or PinchTab.
- Use `--headed` when a visual check will help.
- When capturing artifacts in this repo, use `output/playwright/` and avoid introducing new top-level artifact folders.
- Default to MCP actions and workflows, not Playwright test specs.
