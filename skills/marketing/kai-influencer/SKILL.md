---
name: kai-influencer
description: Plan influencer marketing campaigns — find creators, write briefs, manage partnerships, and measure ROI. Use when "influencer", "influencer marketing", "creator campaign", "UGC campaign", "brand ambassador", "creator partnership", or any request to work with influencers or content creators.
---

# Kai Influencer Skill

Plan influencer marketing campaigns end-to-end: discovery, briefing, management, and measurement.

---

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Discovery

Read from `MARKETING.md`. Only ask about things not covered there:

1. **Campaign goal** — Awareness, conversions, content generation, social proof?
2. **Product/service** — What are we promoting? Price point, differentiator.
3. **Target audience** — Which persona(s)? Load from `E:\Dev2\kai-cmo-harness-work\knowledge\personas\_persona-index.md`
4. **Platforms** — Instagram, TikTok, YouTube, LinkedIn, podcast, other?
5. **Budget** — Total campaign budget and per-creator range
6. **Timeline** — Launch date, campaign duration, key milestones
7. **Past partnerships** — Any previous influencer work? What worked/failed?
8. **Content rights** — Do we need usage rights for ads? How long?

---

## Phase 2: Plan

Build the influencer campaign strategy:

1. **Load influencer playbook**: `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\influencer-MARKETING.md`
2. **Define creator tiers**:
   - **Nano** (1K-10K followers): High engagement, low cost, authentic feel
   - **Micro** (10K-100K): Niche authority, good reach/engagement balance
   - **Mid** (100K-500K): Broader reach, established credibility
   - **Macro** (500K+): Mass awareness, lower engagement rate
3. **Creator selection criteria**:
   - Audience overlap with target persona
   - Engagement rate (not just follower count)
   - Content quality and brand alignment
   - Past brand partnership history
   - Authenticity signals (comment quality, audience demographics)
4. **Compensation model** — Flat fee, performance-based, product exchange, affiliate, hybrid
5. **Content format** — Dedicated post, story series, video integration, review, unboxing
6. **Campaign structure** — One-off, series, ambassador program, affiliate network

---

## Phase 3: Produce

Create campaign deliverables:

1. **Creator brief template**:
   - Campaign overview (what, why, who)
   - Key messages (2-3 talking points, not a script)
   - Do's and don'ts (brand guidelines, competitor mentions)
   - Content specs (format, length, hashtags, mentions)
   - Deliverables and deadlines
   - FTC disclosure requirements (must include #ad or #sponsored)
   - Usage rights and approval process
2. **Outreach templates** — Personalized pitch for each creator tier
3. **Contract essentials** — Deliverables, timeline, payment terms, usage rights, exclusivity
4. **Content approval workflow** — Draft review, revision rounds, final sign-off
5. **Tracking setup** — UTM parameters, promo codes, affiliate links per creator
6. **Measurement framework**:
   - Reach and impressions
   - Engagement (likes, comments, shares, saves)
   - Traffic (UTM-tracked clicks)
   - Conversions (promo code / affiliate link redemptions)
   - Cost per engagement, cost per acquisition
   - Content quality score (reusability for ads)

---

## Phase 4: Quality Gates

Validate before launch:

1. **Four U's Score** (on briefs and outreach): `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\four_us_score.py <file>`
   - Minimum: **10/16**
2. **Banned Word Check**: `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\banned_word_check.py <file>`
3. **FTC compliance check** — All content requires clear disclosure
4. **Platform policy check** — Branded content tags, paid partnership labels
5. **Brief clarity check** — Could a creator execute this without a follow-up call?

Max 2 auto-retry cycles on gate failures.

---

## Phase 5: Output

Deliver the influencer campaign package:

- **Campaign strategy document** (goals, tiers, budget, timeline)
- **Creator brief template** (ready to customize per creator)
- **Outreach email templates** (per tier)
- **Tracking and measurement plan** (UTMs, promo codes, KPIs)
- **Contract checklist** (key terms to include)
- **Gate pass/fail summary**

Write output to `E:\Dev2\kai-cmo-harness-work\workspace\` with filename pattern: `influencer-campaign-YYYY-MM-DD.md`
