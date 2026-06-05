---
name: kai-analytics
description: Analytics and attribution setup — tracking plan, UTM conventions, dashboard design, and attribution model selection. Use when "analytics setup", "attribution", "tracking plan", "UTM", "marketing analytics", "dashboard setup", "measurement strategy", "how do I track", "which metrics", or any request to set up or improve marketing measurement and attribution.
---

# kai-analytics — Analytics & Attribution Setup

Design a complete marketing measurement system: tracking plan, UTM conventions, attribution model, and dashboard specifications.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## References

Load these files as context before starting:

- `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\analytics-attribution.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\technical-marketing-tracking.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\saas-metrics-guide.md`

## Phase 1 — Discovery

1. Read from `MARKETING.md`. Only ask about things not covered there:
   - Business model and primary conversion event (signup, purchase, demo request)
   - Current analytics tools (GA4, Mixpanel, PostHog, Amplitude, etc.)
   - Ad platforms in use (Meta, Google, LinkedIn, TikTok, etc.)
   - CRM or email tool (HubSpot, Salesforce, Loops, etc.)
   - Current tracking status (nothing, partial, broken, outdated)
   - Key questions they need answered ("where do customers come from?", "which ads work?")
   - Sales cycle type (self-serve, sales-assisted, enterprise)
2. Identify the measurement maturity level:
   - **Level 0**: No tracking beyond platform defaults
   - **Level 1**: Basic GA4 + ad platform pixels
   - **Level 2**: UTMs + event tracking + basic attribution
   - **Level 3**: Multi-touch attribution + cohort analysis + LTV tracking

## Phase 2 — Analysis

### Measurement Gap Audit
1. Map the current customer journey: first touch -> conversion -> retention.
2. Identify blind spots — where do you lose visibility?
3. Flag conflicting data sources (ad platform vs. GA4 discrepancies).
4. Assess data quality: are events firing correctly? Are UTMs consistent?

### Attribution Model Selection
Recommend the right model based on their business:

| Model | Best For | Limitation |
|-------|----------|------------|
| Last-click | Short sales cycles, ecommerce | Ignores awareness channels |
| First-click | Brand-heavy businesses | Ignores nurture channels |
| Linear | Multi-channel, even contribution | Oversimplifies |
| Time-decay | Long sales cycles, B2B | Complex to implement |
| Position-based (U-shaped) | Most B2B SaaS | Requires multi-touch data |
| Data-driven (GA4) | High-volume businesses | Needs 600+ conversions/month |

### Attribution Caveats

State caveats beside every attribution recommendation:

- Platform dashboards optimize for their own pixel, identity graph, attribution window, and modeled conversions.
- GA4, CRM, payment, and ad-platform revenue will disagree when UTMs, consent mode, offline conversions, refunds, or sales-cycle delays differ.
- Last-click is useful for capture channels, not proof that awareness or nurture did nothing.
- Multi-touch models describe observed journeys; they do not prove incrementality without holdouts, geo tests, lift studies, or matched-market tests.
- Use directional attribution for budget conversations until event QA, UTM hygiene, consent coverage, and CRM joins are verified.

## Phase 3 — Produce

Build these deliverables:

### Tracking Plan
Structured event taxonomy:

| Event Name | Trigger | Properties | Tool |
|------------|---------|------------|------|
| `page_view` | Every page load | url, referrer, utm_* | GA4 |
| `signup_started` | Form opened | source, plan_type | GA4 + Product |
| `signup_completed` | Account created | method, plan, value | GA4 + Product + CRM |
| [custom events per business] | | | |

### UTM Convention Guide
Standardized naming rules:
- `utm_source`: platform name, lowercase (google, meta, linkedin)
- `utm_medium`: traffic type (cpc, email, social, organic, referral)
- `utm_campaign`: campaign name with date prefix (2026-03_spring-launch)
- `utm_content`: ad variant or content identifier (cta-v1, hero-image-b)
- `utm_term`: keyword or targeting (only for paid search)

Include a UTM builder template and naming convention doc.

### Dashboard Specifications
Design dashboards for three audiences:

**Executive Dashboard** (weekly glance)
- Revenue attributed by channel
- Blended CAC trend
- Conversion rate by stage
- Top 5 performing campaigns

**Marketing Ops Dashboard** (daily operations)
- Traffic by source/medium
- Conversion funnel with drop-off rates
- UTM campaign performance table
- Ad spend vs. revenue by platform

**Channel-Specific Dashboards** (per platform)
- Platform metrics (CTR, CPC, ROAS)
- Audience segment performance
- Creative/copy variant performance
- Budget pacing

### Pixel & Tag Setup Guide
- Which pixels/tags to install per platform
- Implementation method (GTM, direct, server-side)
- Consent management requirements (GDPR/CCPA)
- Testing and validation steps

## Phase 4 — Output

1. Deliver the tracking plan as a structured table.
2. Deliver the UTM convention guide as a reference document.
3. Deliver dashboard specs with metric definitions and data sources.
4. Provide an implementation checklist ordered by priority.
5. Include a "data quality audit" checklist for monthly review.

## Constraints

- Never recommend tracking that violates GDPR or CCPA without consent mechanisms.
- Always include a consent management note for EU/CA audiences.
- UTM conventions must be consistent — no mixed case, no spaces, no special characters.
- Dashboard metrics must have clear definitions (e.g., "conversion rate = signups / unique visitors").
- Attribution model must match the user's data volume — don't recommend data-driven with 50 conversions/month.
- All event names must follow a consistent naming convention (snake_case preferred).
