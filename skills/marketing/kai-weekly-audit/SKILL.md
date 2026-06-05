---
name: kai-weekly-audit
description: Weekly marketing audit and operating review. Pulls the last 7 days of source-backed marketing, analytics, content, paid media, lead, watcher, and audit data; compares it to the prior 7 days; flags urgent issues; and produces a weekly scorecard plus action list. Use when "weekly audit", "weekly marketing review", "weekly check-in", "weekly scorecard", "what changed this week", "Friday marketing review", or any request for a recurring 7-day marketing audit.
---

# kai-weekly-audit - Weekly Marketing Audit

Run a fast weekly operating audit. This skill is the cadence layer above `/kai-audit`, `/kai-seo-audit`, `/kai-cro`, `/kai-daily-ad-review`, `/content-report`, and watcher output.

## Non-Negotiable: Data Provenance

Before writing findings, load `E:\Dev2\kai-cmo-harness-work\harness\references\audit-data-provenance.md`.

Declare the data mode:

- `sales_external` for prospect/public-only weekly reviews.
- `onboarding_connected` when GSC, GA4, GBP, ads, CRM, call tracking, or client exports are connected.
- `internal_demo` when sample data is used.

Do not publish review counts, rankings, traffic, conversions, calls, ad metrics, Core Web Vitals, backlinks, or revenue without source, retrieval date, and artifact path. Missing sources become `_data-gaps.md` entries.

Run before handoff:

```bash
python scripts/quality_gates/audit_provenance_lint.py workspace/audits/weekly/<YYYY-MM-DD> --audit-dir
```

## Phase 0: Load Context

1. Read `MARKETING.md`.
2. Identify the brand, URL, active channels, conversion events, offer, business type, and connected sources.
3. Ask only for missing items that block a sourced review: URL, data mode, available connected sources, or target conversion event.

## Phase 1: Collect Weekly Data

Create the weekly audit folder:

```text
workspace/audits/weekly/<YYYY-MM-DD>/
```

Run the shared collector for the target site:

```bash
python -m scripts.audit.collect --url "<url>" --mode <mode> --workflow kai-weekly-audit --out workspace/audits/weekly/<YYYY-MM-DD> --pagespeed
```

Use connected collectors only when access is confirmed:

```bash
python -m scripts.audit.collect --url "<url>" --mode onboarding_connected --workflow kai-weekly-audit --out workspace/audits/weekly/<YYYY-MM-DD> --pagespeed --places --gsc --ga4 --calls --date-from "<YYYY-MM-DD>" --date-to "<YYYY-MM-DD>"
```

Add paid and content pulls when relevant:

```bash
python scripts/ads/pull_all.py
python -m scripts.content.tracker_cli report --format json
python -m scripts.analytics.performance_dashboard weekly
```

If a command cannot run because credentials are missing, record the exact missing source in `_data-gaps.md`.

## Phase 2: Compare Periods

Use last 7 complete days as the primary period and the prior 7 complete days as comparison.

Review these areas when data exists:

| Area | Weekly Question |
|---|---|
| Revenue or pipeline | Did qualified demand, revenue, or pipeline move materially? |
| Website and CRO | Did traffic quality, speed, conversion, or form/call capture degrade? |
| SEO and AEO | Did indexed visibility, crawl health, search queries, or AI-search readiness change? |
| Paid media | Did spend, CPL, ROAS, CPA, CTR, CPC, or frequency drift outside guardrails? |
| Content | Which new or aging pieces need action? |
| Social and community | Did reach, engagement, replies, or audience quality change? |
| Lifecycle and CRM | Did follow-up, reply rate, lead aging, or handoff quality change? |
| Calls and reviews | Did missed calls, after-hours demand, reviews, or reputation signals need action? |
| Watchers | Which alerts repeated or escalated? |

Only score metrics present in `audit-data.json`, connected exports, or raw pull artifacts.

## Phase 3: Scorecard

Produce a short weekly scorecard:

| Score | Meaning |
|---|---|
| Green | On track; no immediate intervention. |
| Yellow | Needs attention this week. |
| Red | Requires immediate owner decision or fix. |
| Gray | Not scored because data is missing. |

Each scored item must include:

```yaml
claim: ""
source_tier: connected | public_observed | user_provided | inferred | missing_data
source_name: ""
source_url: ""
retrieved_at: ""
evidence_artifact: ""
score_eligible: true | false
```

## Phase 4: Weekly Actions

Create three action groups:

- **Do this week** - P0/P1 issues with clear owner and due date.
- **Watch next week** - items with trend risk but insufficient evidence for action.
- **Needs data** - sources or exports required before the next review.

Map recommended fixes to Kai skills:

| Finding | Skill |
|---|---|
| Site or funnel issue | `/kai-cro` or `/kai-landing-page` |
| Search issue | `/kai-seo-audit` or `/kai-surround-sound` |
| Paid issue | `/kai-daily-ad-review` or `/kai-ad-campaign` |
| Content issue | `/content-report`, `/content-retro`, or `/kai-content-calendar` |
| Lifecycle issue | `/kai-email-system` or `/kai-retention` |
| Strategic drift | `/kai-growth-plan` |
| Client-ready deck needed | `/kai-html-presentation` |

## Phase 5: Output

Write:

```text
workspace/audits/weekly/<YYYY-MM-DD>/
+-- _data-sources.md
+-- _data-gaps.md
+-- audit-data.json
+-- kai-data.json
+-- _weekly-scorecard.md
+-- _weekly-findings.md
+-- _weekly-actions.md
+-- _skill-routing.md
+-- html-presentation/
    +-- index.html
```

Use `/kai-html-presentation` to turn the weekly report into `html-presentation/index.html` when the user asks for a client-ready delivery artifact.
