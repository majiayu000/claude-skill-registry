---
name: kai-abm
description: Plan and execute account-based marketing campaigns for enterprise targets — account selection, personalized outreach, multi-channel touch sequences, and deal acceleration. Use when "ABM", "account-based marketing", "enterprise marketing", "target accounts", "named accounts", "enterprise outreach", "key accounts", or any request to build personalized campaigns for specific companies.
---

# Kai ABM Skill

Plan and execute account-based marketing campaigns: account selection, personalization, multi-channel touches, and measurement.

---

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Discovery

Read from `MARKETING.md`. Only ask about things not covered there:

1. **ICP definition** — What does the ideal target company look like? (industry, size, revenue, tech stack, signals)
2. **Target account list** — Named accounts or criteria for building the list?
3. **Buying committee** — Who are the decision-makers, influencers, and blockers? (titles, roles)
4. **Product/offer** — What are we selling? Price point, deal size, sales cycle length.
5. **Current pipeline** — Any existing relationships or warm contacts at target accounts?
6. **Sales alignment** — Is sales involved? What's the handoff point?
7. **Channels available** — Email, LinkedIn, ads, direct mail, events, phone?
8. **Budget** — Per-account spend range
9. **Persona alignment** — Which harness persona(s) map to the buying committee? Load from `E:\Dev2\kai-cmo-harness-work\knowledge\personas\_persona-index.md`

---

## Phase 2: Plan

Build the ABM campaign architecture:

1. **Load ABM playbook**: `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\account-based-MARKETING.md`
2. **Tier accounts by fit and intent**:
   - **Tier 1** (1:1): Top 10-25 accounts. Fully personalized. High-touch.
   - **Tier 2** (1:few): 25-100 accounts. Cluster by industry/use case. Semi-personalized.
   - **Tier 3** (1:many): 100-500 accounts. Programmatic with light personalization.
3. **Account research template** (Tier 1):
   - Company priorities (earnings calls, press releases, job postings)
   - Technology stack (what they use today)
   - Key personnel (LinkedIn profiles, content they publish, mutual connections)
   - Pain signals (hiring patterns, tech changes, complaints in reviews)
   - Competitive landscape (who else is selling to them)
4. **Multi-channel touch sequence**:
   - **Week 1-2**: Warm-up (LinkedIn engagement, content sharing, ad impressions)
   - **Week 3-4**: Direct outreach (personalized email, LinkedIn message)
   - **Week 5-6**: Value delivery (relevant content, case study, invite to event)
   - **Week 7-8**: Conversion push (meeting request, demo offer, executive intro)
5. **Content mapping** — Map existing assets to buying stages and personas
6. **Ad targeting** — Account-level targeting on LinkedIn, programmatic display
7. **Sales/marketing SLA** — Response times, follow-up rules, feedback loops

---

## Phase 3: Produce

Create ABM campaign assets:

1. **Account briefs** (Tier 1) — One-page dossier per account with research, contacts, and approach
2. **Personalized email sequences** — 4-6 touches per tier, customized by account/cluster
3. **LinkedIn outreach templates** — Connection request + message sequence
4. **Targeted ad copy** — Account-aware messaging for LinkedIn and display ads
5. **Custom content** (Tier 1) — Account-specific landing pages, case studies, or presentations
6. **Event invitations** — Personalized invites to webinars, dinners, or roundtables
7. **Sales enablement** — Account cheat sheets for sales team with talking points

Apply harness writing rules:
- Conditions AFTER main clause
- Instructions start with verbs
- Short sentences, high specificity
- Bold the answer

---

## Phase 4: Quality Gates

Validate before launch:

1. **Four U's Score**: `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\four_us_score.py <file>`
   - Minimum: **10/16** for emails and outreach
   - Minimum: **12/16** for content and landing pages
2. **Banned Word Check**: `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\banned_word_check.py <file>`
3. **AI Slop Check** — Zero filler. ABM demands precision.
4. **Personalization depth check** — Does each Tier 1 message reference something specific to the account?
5. **Platform policy compliance** — Check ad copy against platform rules:
   - LinkedIn: `E:\Dev2\kai-cmo-harness-work\harness\references\linkedin-ads-rules.md`
   - Google Display: `E:\Dev2\kai-cmo-harness-work\harness\references\google-ads-policy-reference.md`
6. **CAN-SPAM / cold email compliance**: `E:\Dev2\kai-cmo-harness-work\harness\references\cold-email-rules.md`

Max 2 auto-retry cycles on gate failures.

---

## Phase 5: Output

Deliver the ABM campaign package:

- **ABM strategy document** (ICP, tiers, channels, timeline, budget)
- **Account briefs** (Tier 1 dossiers)
- **Email sequences** (per tier)
- **LinkedIn outreach templates**
- **Ad copy** (per platform)
- **Content map** (existing assets mapped to buying stages)
- **Sales enablement materials** (account cheat sheets)
- **Measurement framework** (engagement score, pipeline influence, deal velocity)
- **Gate pass/fail summary**

Write output to `E:\Dev2\kai-cmo-harness-work\workspace\` with filename pattern: `abm-campaign-YYYY-MM-DD.md`
