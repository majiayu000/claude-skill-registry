---
name: kai-analytics
description: Analytics and attribution setup — tracking plan, UTM conventions, dashboard design, and attribution model selection. Use when "analytics setup", "attribution", "tracking plan", "UTM", "marketing analytics", "dashboard setup", "measurement strategy", "how do I track", "which metrics", or any request to set up or improve marketing measurement and attribution.
---

# /kai-analytics — A Measurement System Whose Numbers Can Be Trusted

## Objective

A marketing measurement system the team can operate: an event taxonomy with defined triggers and properties, a UTM convention nobody has to guess at, an attribution model matched to the actual data volume, dashboard specs for three audiences, and a pixel/tag plan that survives a consent check. The result is that "where do customers come from" and "which ads work" have answers someone can reproduce.

Matching the model to the data is the load-bearing judgment. A data-driven attribution model on 50 conversions a month produces confident nonsense.

## Done when

Work type `strategy-plan` — floor **E3/C3/O1** (`harness/eco-floors.yaml`).

- **E3** — a named human approved the exact tracking plan, UTM guide, and dashboard specs.
- **C3** — the deliverables clear `banned_word_check`, and someone other than the author read them end to end. Every metric in every dashboard spec carries a written definition ("conversion rate = signups / unique visitors"); an undefined metric is a craft failure.
- **O1** — each P0 implementation item names the blind spot it closes, its owner, and how anyone will know the event is firing correctly. The plan's own outcome is instrumentation proven, not documents delivered.

A tracking plan nobody implements is not CLOSED. Its first work item is named in the implementation checklist.

## Constraints

- **Read `MARKETING.md` from the project root first.** It carries product, ICP, value prop, monetization, voice, current channels, and competitive landscape. If it does not exist, build it from the codebase — CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, email/ad/analytics config — using the template from `/kai-email-system`, and confirm the draft. Do not ask the user what the product is.
- **Seven things must be known before recommending a model or a stack:** the business model and primary conversion event; current analytics tools (GA4, Mixpanel, PostHog, Amplitude); ad platforms in use; the CRM or email tool; current tracking status (nothing, partial, broken, outdated); the questions they actually need answered; and the sales cycle type (self-serve, sales-assisted, enterprise).
- **Never recommend tracking that violates GDPR or CCPA without a consent mechanism.** Every plan touching EU or California audiences carries a consent-management note.
- **UTM values are consistent or they are useless** — lowercase, no spaces, no special characters, no mixed case.
- **Event names follow one convention** (snake_case preferred), and each event declares its trigger, its properties, and the tools it lands in.
- **Attribution model must match data volume.** Data-driven needs 600+ conversions/month. Recommending above the data is a craft failure, not a stretch goal.
- **Every attribution recommendation ships with its caveats** (below). Attribution language that implies proof of causation without a counterfactual does not ship.
- **Dashboard metrics carry definitions**, not just names.

## Context

| Need | Load |
|---|---|
| Attribution mechanics and model tradeoffs | `knowledge/playbooks/analytics-attribution.md` |
| Pixels, tags, server-side, event plumbing | `knowledge/playbooks/technical-marketing-tracking.md` |
| Which metrics matter and their benchmarks | `knowledge/playbooks/saas-metrics-guide.md` |
| Business model, channels, tools in use | `MARKETING.md` (project root) |

**Measurement maturity** — diagnose this before prescribing anything:

| Level | State |
|---|---|
| 0 | No tracking beyond platform defaults |
| 1 | Basic GA4 + ad platform pixels |
| 2 | UTMs + event tracking + basic attribution |
| 3 | Multi-touch attribution + cohort analysis + LTV tracking |

**Attribution model selection:**

| Model | Best for | Limitation |
|---|---|---|
| Last-click | Short sales cycles, ecommerce | Ignores awareness channels |
| First-click | Brand-heavy businesses | Ignores nurture channels |
| Linear | Multi-channel, even contribution | Oversimplifies |
| Time-decay | Long sales cycles, B2B | Complex to implement |
| Position-based (U-shaped) | Most B2B SaaS | Requires multi-touch data |
| Data-driven (GA4) | High-volume businesses | Needs 600+ conversions/month |

**Attribution caveats — state these beside every recommendation:**

- Platform dashboards optimize for their own pixel, identity graph, attribution window, and modeled conversions.
- GA4, CRM, payment, and ad-platform revenue will disagree when UTMs, consent mode, offline conversions, refunds, or sales-cycle delays differ.
- Last-click is useful for capture channels; it is not proof that awareness or nurture did nothing.
- Multi-touch models describe observed journeys. They do not prove incrementality without holdouts, geo tests, lift studies, or matched-market tests.
- Attribution stays directional in budget conversations until event QA, UTM hygiene, consent coverage, and CRM joins are verified.

**UTM convention:** `utm_source` = platform name, lowercase (google, meta, linkedin) · `utm_medium` = traffic type (cpc, email, social, organic, referral) · `utm_campaign` = campaign name with date prefix (`2026-03_spring-launch`) · `utm_content` = ad variant or content identifier (`cta-v1`, `hero-image-b`) · `utm_term` = keyword or targeting, paid search only. Ship a builder template alongside the rules.

**Dashboards, three audiences.** Executive (weekly glance): revenue attributed by channel, blended CAC trend, conversion rate by stage, top 5 campaigns. Marketing ops (daily): traffic by source/medium, funnel with drop-off rates, UTM campaign table, ad spend vs revenue by platform. Channel-specific (per platform): platform metrics, audience segment performance, creative variant performance, budget pacing.

**Deliverables:** tracking plan, UTM convention guide, dashboard specs with metric definitions and data sources, pixel/tag setup guide (which tags, GTM vs direct vs server-side, consent requirements, validation steps), a priority-ordered implementation checklist, and a monthly data-quality audit checklist.

## Escalate when

- Data sources disagree materially and the user wants one number to report upward.
- Consent infrastructure does not exist and the requested tracking requires it.
- Conversion volume cannot support the model the user has already decided on.
- Implementation requires engineering time nobody has committed.
- The user asks for an incrementality claim the current setup cannot support.
