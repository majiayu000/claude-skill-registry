---
name: "scrapling"
description: "Use Scrapling for web extraction (HTTP, async, dynamic, stealth fetchers). Prefer Scrapling for scraping pipelines; fallback to `playwright-ext` when blocked."
---

# Scrapling Skill

Use Scrapling as the primary extraction layer in a three-layer stack:
- Scrapling: extraction-first
- PinchTab: low-token browser inspection and lightweight interaction
- `playwright-ext`: reliable browser execution

Keep `playwright-ext` as the final fallback for blocked or unsupported scenarios, and hand off to PinchTab first when a real browser is helpful but full Playwright rigor is not needed.

## When to Use This Skill

Triggered by:
- "scrape this site"
- "extract structured data from pages"
- "anti-bot scraping"
- "dynamic page extraction"
- "batch crawling pipeline"

## Prerequisite Check

```bash
python3 --version
python3 -c "from scrapling.fetchers import Fetcher, AsyncFetcher, DynamicFetcher, StealthyFetcher"
claude mcp list | rg "playwright-ext"
```

If you need to fetch packages or sources from GitHub/PyPI, use local proxy env:

```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 <download-command>
```

## Core Workflow

1. Start with `Fetcher` / `AsyncFetcher` for standard HTTP extraction.
2. Escalate to `DynamicFetcher` / `StealthyFetcher` for JS-heavy or anti-bot pages.
3. If the task now needs browser state inspection, text verification, or a small amount of interaction, hand off to PinchTab first when available.
4. If the flow needs reliable ref-based interaction, strict post-action verification, or browser state that PinchTab cannot complete safely, fallback to `playwright-ext`.
5. Report clearly which layer was used for the final output and why the switch happened.

## Collaboration Boundaries

Prefer Scrapling when:
- the goal is extraction, parsing, or structured data collection.
- deterministic selectors and reproducible HTTP requests matter more than browser realism.
- the page can be solved by HTTP fetchers or Scrapling's dynamic fetchers without human-like browser control.

Switch to PinchTab when:
- you need a quick browser read on page state before choosing selectors or extraction strategy.
- the user mainly needs readable page text, low-token snapshots, or lightweight tab/session operations.
- a short browser probe is cheaper than committing to full Playwright control.

Switch directly to `playwright-ext` when:
- the task is fundamentally interaction-heavy rather than extraction-heavy.
- success depends on stable refs, repeated re-snapshot cycles, or precise DOM transitions.
- login/session/captcha/risk-control handling requires a real browser workflow that must be verified step by step.

## Fallback Rules (Mandatory)

Fallback away from Scrapling when:
- fetcher returns persistent anti-bot/captcha blocks.
- target requires interaction that Scrapling fetchers cannot complete reliably.
- credentialed browser state is required for final extraction.

Prefer PinchTab as the first browser handoff when the user still mainly needs inspection or lightweight interaction. Go straight to `playwright-ext` when the task already requires reliable end-to-end browser execution.

Minimal fallback check:

```bash
claude mcp list | rg "playwright-ext"
```

## Guardrails

- Prefer the lightest fetcher that can complete the task.
- Keep extraction reproducible (explicit URL/input and deterministic selectors where possible).
- Do not stay in Scrapling once real browser interaction becomes the primary task.
- Do not route to PinchTab or `playwright-ext` silently; state why the switch is necessary.
- Do not claim HTTP-only extraction when fallback browser automation was actually used.
