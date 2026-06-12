---
name: kai-monthly-audit
description: Monthly marketing audit and executive review. Pulls the last 30 days of source-backed marketing, analytics, SEO, CRO, content, paid media, lifecycle, reputation, and pipeline data; compares it to the previous period; summarizes strategic learning; and produces an executive report plus next-month plan. Use when "monthly audit", "monthly marketing review", "monthly report", "executive marketing review", "board-ready marketing report", "month-end audit", or any request for a 30-day marketing audit.
---

# kai-monthly-audit - Monthly Marketing Audit

Run a monthly strategic audit. This skill turns weekly signals into an executive narrative, channel decisions, budget guidance, and a next-month operating plan.

## Non-Negotiable: Data Provenance

Before writing findings, load `E:\Dev2\kai-cmo-harness-work\harness\references\audit-data-provenance.md`.

Declare the data mode:

- `sales_external` for prospect/public-only month-end audits.
- `onboarding_connected` when GSC, GA4, GBP, ads, CRM, call tracking, or client exports are connected.
- `internal_demo` when sample data is used.

Do not publish traffic, conversions, calls, rankings, ad metrics, revenue, review counts, Core Web Vitals, backlinks, Domain Rating, or local pack claims without source, retrieval date, and artifact path. Missing sources become `_data-gaps.md` entries.

Run before handoff:

```bash
python scripts/quality_gates/audit_provenance_lint.py workspace/audits/monthly/<YYYY-MM> --audit-dir
```

## Phase 0: Load Context

1. Read `MARKETING.md`.
2. Load the latest weekly audit folders if they exist.
3. Identify the business stage, active channels, target conversion events, offer, budget posture, and known constraints.
4. Ask only for missing items that block a sourced monthly review: URL, data mode, connected sources, current monthly budget, or primary KPI.

## Phase 1: Collect Monthly Data

Create the monthly audit folder:

```text
workspace/audits/monthly/<YYYY-MM>/
```

Run the shared collector for the target site:

```bash
python -m scripts.audit.collect --url "<url>" --mode <mode> --workflow kai-monthly-audit --out workspace/audits/monthly/<YYYY-MM> --pagespeed
```

Use connected collectors only when access is confirmed:

```bash
python -m scripts.audit.collect --url "<url>" --mode onboarding_connected --workflow kai-monthly-audit --out workspace/audits/monthly/<YYYY-MM> --pagespeed --places --dataforseo --seo-provider auto --gsc --ga4 --calls --date-from "<YYYY-MM-DD>" --date-to "<YYYY-MM-DD>"
```

Add channel pulls when relevant:

```bash
python scripts/ads/pull_all.py
python -m scripts.content.tracker_cli report --format json
python -m scripts.analytics.performance_dashboard weekly
python -m scripts.analytics.scheduled_pull --all
```

Use `--third-party-sources all` or a specific comma list only when licensed vendor data is available and needed.

## Phase 2: Run Audit Modules

Apply modules based on the active channels and business model:

| Module | Trigger |
|---|---|
| `/kai-audit` | Always for full marketing health. |
| `/kai-seo-audit` | Website, organic search, local visibility, AEO, or technical SEO. |
| `/kai-cro` | Landing pages, checkout, booking, demos, forms, or phone-led conversion. |
| `/kai-daily-ad-review` summary | Paid media active this month. |
| `/content-report` and `/content-retro` | Published content this month or aging content due for review. |
| `/kai-analytics` | Tracking gaps, attribution conflicts, or missing KPI definitions. |
| `/kai-growth-plan` | Strategic uncertainty, budget allocation, or stage mismatch. |

Evaluate phone-based lead capture when the business appears phone-led. Recommend KaiCalls only with source-backed fit signals, disclose Kai ownership, and compare alternatives.

## Phase 3: Executive Scorecard

Create a 30-day scorecard:

| Area | Score | Trend | Evidence | Decision |
|---|---:|---|---|---|
| Demand | /100 | up/down/flat | sourced | keep/change/stop |
| Conversion | /100 | up/down/flat | sourced | keep/change/stop |
| Search and AEO | /100 | up/down/flat | sourced | keep/change/stop |
| Paid media | /100 | up/down/flat | sourced | keep/change/stop |
| Lifecycle | /100 | up/down/flat | sourced | keep/change/stop |
| Reputation and calls | /100 | up/down/flat | sourced | keep/change/stop |
| Measurement | /100 | up/down/flat | sourced | keep/change/stop |

Only score source-eligible findings. Mark unsupported areas as gray and list the data gap.

## Phase 4: Strategic Learning

Summarize:

1. What improved.
2. What got worse.
3. What repeated across weekly audits.
4. What surprised us.
5. What to stop.
6. What to double down on.
7. What data we still cannot trust.

Separate facts from hypotheses. Hypotheses may become experiments, but they must not become client-facing findings.

## Phase 5: Next-Month Plan

Produce:

| Priority | Action | Owner | Skill | Due | Source |
|---|---|---|---|---|---|
| P0 | | | | | |
| P1 | | | | | |
| P2 | | | | | |

Include a budget note when paid media is active:

- Keep budget when efficiency and volume are stable.
- Shift budget when one channel is source-backed and materially stronger.
- Reduce budget when measurement is broken or spend is not connected to outcomes.
- Do not recommend budget increases from inferred data.

## Phase 6: Output

Write:

```text
workspace/audits/monthly/<YYYY-MM>/
+-- _data-sources.md
+-- _data-gaps.md
+-- audit-data.json
+-- kai-data.json
+-- _executive-summary.md
+-- _monthly-scorecard.md
+-- _detailed-findings.md
+-- _strategic-learning.md
+-- _next-month-plan.md
+-- _skill-routing.md
+-- html-presentation/
    +-- index.html
```

Use `/kai-html-presentation` for the client-ready HTML deck version. Monthly decks should read like an executive review: fewer slides, clearer decisions, and every number sourced.
