---
name: kai-influencer
description: Plan influencer marketing campaigns — find creators, write briefs, manage partnerships, and measure ROI. Use when "influencer", "influencer marketing", "creator campaign", "UGC campaign", "brand ambassador", "creator partnership", or any request to work with influencers or content creators.
---

# /kai-influencer — Creator Spend That Reads Back as Attributed Reach

## Objective

A creator campaign a brand can actually run: the right tier of creators for the goal, a brief each one can execute without a follow-up call, contract terms that settle usage rights before anyone films, per-creator tracking that makes ROI readable, and a material-connection disclosure on every piece of content. The deliverable is the campaign package — strategy, briefs, outreach, tracking plan, contract checklist — not a list of creator names. Follower count is the cheapest and least predictive input; audience overlap and engagement quality carry the campaign.

## Done when

Work type `campaign` — floor **E5/C3/O4** (`harness/eco-floors.yaml`, contract `harness/skill-contracts/campaign.yaml`). Composite: the campaign is CLOSED only when every creator deliverable is CLOSED. One creator who never posted keeps it open.

- **E5** — every creator post read back at its public permalink by someone other than its producer, confirming the approved content *and* a visible disclosure. A post nobody re-read has not shipped.
- **C3** — briefs and outreach clear `four_us_score` at **10/16** and `banned_word_check` at zero, and a named non-producer reads the brief pack end to end.
- **O4** — the per-creator threshold (cost per engagement, CPA, or conversion count) is recorded *before* the first post goes live, then read from UTM and promo-code data at the declared window. A baseline written after launch is not a baseline. Attribution is required at the campaign level.

## Constraints

**FTC disclosure is a launch blocker, not a line item.**

- Every piece of creator content carries a clear material-connection disclosure (`#ad` or `#sponsored`). It appears in the brief, in the contract, and in the pre-launch check.
- Disclosure may not be buried — not below the fold, not at the end of a hashtag block, not in a caption the platform truncates. Load `harness/references/creator-disclosure.md` and `harness/references/creator-disclosure-presets.json` before writing any brief.
- Use the platform's own branded-content tooling where it exists: paid partnership label, branded content tag. Platform labelling does not replace the in-content disclosure.
- Endorsement, testimonial, and claim law applies to what the creator says on the brand's behalf: `harness/references/advertising-compliance.md`. Load it before writing key messages.
- Content that ships without disclosure is a compliance failure. Do not launch it, and do not treat a creator's "I'll add it later" as approval.

**Other binding rules:**

- Key messages are 2-3 talking points, never a script. A scripted creator reads as an ad and converts like one.
- Select on engagement quality, audience overlap, and authenticity signals — not follower count. Never quote an audience metric the creator or the platform did not report.
- Usage rights (scope and duration), exclusivity, deliverables, deadlines, and payment terms are contract terms. The campaign is not approved until they are settled in writing.
- Gates: `python scripts/quality_gates/four_us_score.py <file>` (min 10/16) and `python scripts/quality_gates/banned_word_check.py <file>` on briefs and outreach. Max 2 retry cycles, each naming the specific failing dimension. After 2 failures, escalate to a human with the failures listed and log the diagnosis in `memory/lessons.md`.
- Brief clarity bar: a creator must be able to execute it without a follow-up call.
- Kai does not sign contracts, release payment, or send outreach. Human approval precedes every live action and every dollar.
- Paying for undisclosed endorsements, bought followers, or astroturfed comment activity is a stop, not an escalation.
- **Read `MARKETING.md` from the project root before asking the user anything.** If it does not exist, build it from the codebase — README, manifests, landing pages, route files, analytics and email config — and confirm the draft. Do not open with discovery questions the repo can answer.

**Know these before producing anything** (from `MARKETING.md` first; ask only for what it cannot answer): campaign goal (awareness, conversions, content generation, social proof) · product, price point, differentiator · target persona(s) · platforms · total budget and per-creator range · timeline and milestones · what past partnerships did · required content usage rights and their duration.

## Context

| Need | Load |
|---|---|
| Tiering, campaign structures, creator management | `knowledge/playbooks/influencer-marketing.md` |
| Which persona the creator's audience must match | `knowledge/personas/_persona-index.md` |
| Disclosure format per platform | `harness/references/creator-disclosure.md` + `harness/references/creator-disclosure-presets.json` |
| FTC, endorsement, and claim law | `harness/references/advertising-compliance.md` |
| What creators may and may not do on each platform | `harness/references/*-organic-posting-rules.md` + `harness/references/social-automation-rules.md` |
| Multi-asset campaign contract | `harness/skill-contracts/campaign.yaml` |
| Product, ICP, voice, current channels | `MARKETING.md` (project root) |

**Creator tiers** — what each tier actually buys:

| Tier | Followers | What it buys |
|------|-----------|--------------|
| Nano | 1K–10K | High engagement, low cost, authentic feel |
| Micro | 10K–100K | Niche authority, best reach/engagement balance |
| Mid | 100K–500K | Broader reach, established credibility |
| Macro | 500K+ | Mass awareness, lowest engagement rate |

**Selection criteria:** audience overlap with the target persona · engagement rate (not follower count) · content quality and brand alignment · past brand partnership history · authenticity signals (comment quality, audience demographics).

**Design choices to make explicitly:** compensation model (flat fee, performance-based, product exchange, affiliate, hybrid) · content format (dedicated post, story series, video integration, review, unboxing) · campaign structure (one-off, series, ambassador program, affiliate network).

**Measurement plan must cover:** reach and impressions · engagement (likes, comments, shares, saves) · UTM-tracked clicks · conversions from promo codes and affiliate links · cost per engagement and cost per acquisition · content quality score (is it reusable as paid creative?). Tracking is set up per creator before launch, not reconstructed after.

**Package contents:** campaign strategy document · creator brief template · outreach templates per tier · tracking and measurement plan · contract checklist (deliverables, timeline, payment terms, usage rights, exclusivity) · content approval workflow (draft review, revision rounds, final sign-off) · gate results. **Output** goes to `workspace/` with the filename pattern `influencer-campaign-YYYY-MM-DD.md`.

**The creator brief carries:** campaign overview (what, why, who) · key messages · do's and don'ts (brand guidelines, competitor mentions) · content specs (format, length, hashtags, mentions) · deliverables and deadlines · FTC disclosure requirements · usage rights and the approval process.

## Escalate when

- Required usage rights exceed what the budget or the creator's terms allow.
- A platform offers no disclosure mechanism that satisfies the FTC requirement for the planned format.
- The campaign needs spend the user has not authorized, or per-creator rates exceed the stated range.
- A candidate creator shows authenticity red flags (purchased followers, engagement pods) or an undisclosed competing partnership.
- The product sits in a regulated category (health, financial, supplements) where creator claims carry substantiation risk.
- Past-partnership results are unavailable and the budget assumes a performance level nothing supports.
