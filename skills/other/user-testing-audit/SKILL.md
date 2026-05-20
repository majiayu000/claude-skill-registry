---
name: user-testing-audit
description: Run a repeatable two-layer site audit: full sitemap JS-off coverage for complete issue inventory, then focused JS-on flow checks for hydration/booking UX. Emit dated markdown+JSON artifacts with prioritized findings and acceptance criteria.
---

# User Testing Audit

Run a structured, repeatable audit for a live website and produce actionable artifacts.

This skill is now **two-layer by default**:

1. **Layer A (full coverage):** sitemap-wide JS-off crawl for complete machine-readability/indexability inventory.
2. **Layer B (focused behavior):** JS-on audit for booking/hydration/mobile/a11y conversion flows.

## Trigger

Use this skill when the user asks to:

- test a deployed site or URL,
- run QA/user testing,
- find UI/UX defects (broken links/images, contrast, spacing/layout issues),
- produce a bug list with priorities.

## Required Input

If URL is missing, ask exactly one question:

`What URL should I audit?`

Do not proceed without a valid `https://...` URL.

## Output Contract

Always produce:

1. Full-crawl markdown report:
   - `docs/audits/user-testing/YYYY-MM-DD-<slug>-full-js-off-crawl.md`
2. Full-crawl JSON matrix artifact:
   - `docs/audits/user-testing/YYYY-MM-DD-<slug>-full-js-off-crawl.json`
3. Focused JS-on markdown report:
   - `docs/audits/user-testing/YYYY-MM-DD-<slug>.md`
4. Focused JS-on JSON artifact:
   - `docs/audits/user-testing/YYYY-MM-DD-<slug>.json`
5. Focused SEO summary JSON + raw Lighthouse folder:
   - `...-seo-summary.json`
   - `...-seo-artifacts/`
6. Prioritized issue list (`P0/P1/P2`) with acceptance criteria per issue.
7. Explicit no-JS predicate summary for key routes.
8. Explicit hydrated booking transaction summary.
9. Discovery policy summary (`preview noindex`, `hreflang`, `llms.txt`).
10. For reruns: explicit delta vs prior report (`Resolved`, `Still-open`, `Regressions/new`).

## Workflow

### 1) Resolve a fresh immutable staging URL first (required for staging audits)

Never reuse an old `https://<hash>.brikette-website.pages.dev` URL. Those are immutable and can mask whether a fix was deployed.

For Brikette staging, resolve the newest URL from the latest successful `Deploy Brikette` workflow run on `staging`:

```bash
node .claude/skills/user-testing-audit/scripts/resolve-brikette-staging-url.mjs
```

This returns JSON:

- `url` (fresh immutable URL, defaulting to `/en`)
- `runId`
- `runUrl`
- `headSha`

If the latest run is still in progress, the resolver waits and polls until completion (or timeout). Use the returned `url` as `<TARGET_URL>` in all audit steps.

### 2) Run full coverage crawl first (JS-off, sitemap-wide)

```bash
node .claude/skills/user-testing-audit/scripts/run-full-js-off-sitemap-crawl.mjs \
  --url <TARGET_URL> \
  --slug <DEPLOYMENT-OR-BRANCH-SLUG> \
  --max-pages 6000 \
  --max-sitemaps 160 \
  --concurrency 8
```

Notes:

- This is the complete issue inventory layer.
- It should cover all URLs exposed by sitemap(s), not a small sample.
- If sitemap coverage is unexpectedly low, treat that as a blocker before moving on.

### 3) Run focused JS-on audit (booking/hydration/mobile/a11y)

```bash
node .claude/skills/user-testing-audit/scripts/run-user-testing-audit.mjs \
  --url <TARGET_URL> \
  --slug <DEPLOYMENT-OR-BRANCH-SLUG> \
  --max-crawl-pages 140 \
  --max-audit-pages 36 \
  --max-mobile-pages 24
```

This focused run still generates:

- `docs/audits/user-testing/YYYY-MM-DD-<slug>.md`
- `docs/audits/user-testing/YYYY-MM-DD-<slug>.json`
- `docs/audits/user-testing/YYYY-MM-DD-<slug>-screenshots/`
- `docs/audits/user-testing/YYYY-MM-DD-<slug>-seo-summary.json`
- `docs/audits/user-testing/YYYY-MM-DD-<slug>-seo-artifacts/`

### 4) Reconcile layer A + layer B findings (required)

Do not treat the focused report as complete by itself.

Required reconciliation:

- Use full-crawl output as the canonical completeness baseline.
- Merge focused-flow regressions (hydration, booking transaction, mobile/a11y) into the same backlog priority ordering.
- Raise severity when a focused-flow failure appears across many sitemap URLs in full-crawl data.

### 5) Validate critical findings manually

Do targeted repro checks for high-severity findings from the generated report:

- Broken internal routes from full crawl
- High-frequency template failures (canonical/hreflang/SSR shell issues)
- Suspected i18n key leakage and booking CTA fallback failures
- JS-on booking handoff failures and mobile menu/focus issues
- Contrast failures on key conversion CTAs

### 6) Review generated sections/artifacts (required)

From focused report:

- `## No-JS Predicate Summary` in markdown
- `## Booking Transaction Summary` in markdown
- `## Discovery Policy Summary` in markdown
- `## SEO/Lighthouse Summary` in markdown
- `...-seo-summary.json`
- `...-seo-artifacts/`

From full-crawl report:

- full sitemap URL coverage and status histogram
- complete JS-off issue inventory for discovered URLs

If either layer exposes issues not represented in your final backlog, update before finalizing.

### 7) Compare against prior audit when this is a rerun

When re-auditing a previously reported issue set:

- link prior full-crawl and focused reports,
- summarize issue delta (`P0/P1/P2` before vs after),
- call out `resolved`, `regressed/new`, and `still-open` findings explicitly.

### 8) Return concise summary to user

In chat, provide:

- total issues by priority (merged across both layers),
- top blockers first (frequency + conversion impact),
- path to full-crawl report/json,
- path to focused report/json + SEO summary artifact,
- deployment source (immutable URL + workflow run URL + commit SHA when available),
- immediate next fix batch recommendation.

## Prioritization Rules

Use these defaults unless user requests different severity mapping:

- `P0`: blocks core tasks, major broken navigation/content, severe trust failures
- `P1`: materially degraded UX/accessibility but workaround exists
- `P2`: quality polish, minor accessibility/ergonomics, non-blocking noise

## Report Requirements

Each issue entry must include:

- clear title and priority,
- concrete evidence (URLs/selectors/status/error snippets),
- acceptance criteria checklist that is testable.

Keep issue descriptions factual and reproducible.
