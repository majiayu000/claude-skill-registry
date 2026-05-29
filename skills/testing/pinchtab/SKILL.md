---
name: "pinchtab"
description: "Use PinchTab for browser automation flows (tab/session operations, low-token snapshots). Prefer PinchTab first; fallback to `playwright-ext` when PinchTab is unavailable or blocked."
---

# PinchTab Skill

Use PinchTab as the lightweight browser layer in a three-layer stack:
- Scrapling: extraction-first
- PinchTab: low-token browser inspection and lightweight interaction
- `playwright-ext`: reliable browser execution

Keep `playwright-ext` as the final fallback path, and hand simpler extraction-heavy tasks back to Scrapling when a real browser is no longer necessary.

## When to Use This Skill

Triggered by:
- "pinchtab"
- "browser automation with low token usage"
- "multi-step website operation"
- "tab/session management"
- "agent browser control"

## Prerequisite Check

```bash
pinchtab --version
curl -fsS --max-time 3 http://127.0.0.1:9867/health
codex mcp get playwright-ext
```

If you need to fetch installation assets from GitHub, use local proxy env:

```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 <download-command>
```

## Core Workflow

1. Verify PinchTab binary and health endpoint.
2. Use PinchTab first for navigation, snapshots, page text reads, and lightweight browser steps.
3. After meaningful actions, verify actual page state with URL/title/text/snapshot checks instead of trusting a transport-level success response.
4. If the task becomes pure extraction work, hand it to Scrapling for cheaper and more reproducible data collection.
5. If the first PinchTab action fails, run quick triage before considering fallback.
6. Compare repair cost vs fallback cost, then choose repair or `playwright-ext`.
7. In responses, explicitly mention the final layer used and the reason for any handoff.

## Collaboration Boundaries

Prefer PinchTab when:
- browser context matters, but the task is still mostly inspection, reading, or lightweight interaction.
- low-token snapshots or quick tab/session checks are more valuable than full DOM-level control.
- you want to probe a page before deciding whether Playwright is necessary.

Hand off to Scrapling when:
- the user primarily needs structured extraction or repeatable scraping rather than browser automation.
- HTTP fetchers or dynamic fetchers can finish the job more cheaply and more deterministically.

Escalate to `playwright-ext` when:
- success depends on stable refs, complex navigation, repeated re-snapshot cycles, or precise DOM transitions.
- command success is not enough and the workflow requires strict business-state verification after each action.
- the task is interaction-heavy enough that PinchTab's lightweight path becomes harder to trust than Playwright.

## Quick Failure Triage (Required Before Fallback)

On first failure, run this lightweight triage first (target: <= 3 minutes):

```bash
pinchtab health
pinchtab instances
pinchtab profiles
pinchtab connect default || true
pinchtab quick https://example.com
```

Interpretation guide:
- `health` fails: service is down/unreachable, fallback is allowed.
- instance exists but returns `context canceled`: likely stale browser context; do one reconnect + one smoke test before fallback.
- smoke test succeeds: continue with PinchTab, do not fallback.
- smoke test still fails after one recovery attempt: fallback is allowed.

## Fallback Rules (Mandatory)

Do not fallback on first failure without triage evidence.

Fallback to `playwright-ext` only when one of these is true:
- PinchTab service is unreachable after triage.
- PinchTab returns authentication/authorization errors that require user re-login or manual action.
- Required browser action is not supported in the current PinchTab flow.
- post-action verification shows the page state did not actually change as required.
- Estimated repair cost is higher than fallback cost.

Cost heuristic:
- Prefer repair when expected cost is <= 3 minutes and <= 2 low-risk commands.
- Prefer fallback when expected cost is > 3 minutes, root cause is uncertain, or failures repeat after one recovery attempt.

Minimal fallback check:

```bash
codex mcp get playwright-ext
```

When falling back, report:
- triage commands executed
- observed errors
- reason fallback is cheaper/safer than further repair

## Guardrails

- Do not claim PinchTab succeeded when execution has already switched to `playwright-ext`.
- Do not treat `click`, `fill`, or `press` success as proof that the business action completed.
- Keep action sequence explicit and auditable (navigate -> inspect -> interact -> verify).
- Prefer Scrapling over PinchTab when the browser is only being used to extract page data.
- Do not switch channels silently; include a short handoff note with decision rationale.
- Follow user intent boundaries; do not perform unrelated side-effect operations.
