---
name: kai-partnership
description: Partnership and co-marketing campaign planner — partner selection criteria, joint content strategy, cross-promotion plans, and co-branded assets. Use when "partnership", "co-marketing", "partner program", "cross-promotion", "joint venture", "co-branded", "partner campaign", or any request to plan or execute a marketing partnership.
---

# kai-partnership — Partnership & Co-Marketing Campaigns

Plan and execute co-marketing partnerships: partner evaluation, joint content, cross-promotion strategy, and shared campaign assets.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## References

Load these files as context before starting:

- `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\partnership-coMARKETING.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\personas\_persona-index.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\channels\email-lifecycle.md`

## Phase 1 — Discovery

1. Read from `MARKETING.md`. Only ask about things not covered there:
   - Their product/service and target audience
   - Partnership goal (audience growth, credibility, lead gen, content, distribution)
   - Any existing partnerships or candidates in mind
   - Budget constraints (cash, time, content capacity)
   - Timeline and key dates
2. Clarify partnership type:
   - Content co-creation (webinar, guide, report)
   - Cross-promotion (email swaps, social mentions)
   - Bundle/integration (product-level partnership)
   - Event collaboration (co-hosted workshop, conference)
   - Affiliate/referral (revenue share)

## Phase 2 — Plan

### Partner Selection Scorecard

Evaluate each candidate on:

| Criteria | Weight | Score 1-5 |
|----------|--------|-----------|
| Audience overlap (shared ICP) | 25% | |
| Audience size / reach | 20% | |
| Brand alignment (values, tone) | 20% | |
| Content quality | 15% | |
| Responsiveness / ease of working with | 10% | |
| Competitive risk (do they compete?) | 10% | |

**Minimum threshold**: 3.5 weighted average to proceed.

### Campaign Architecture

1. Define the shared value prop — why this partnership benefits both audiences.
2. Map the funnel: awareness (social) -> consideration (content) -> conversion (offer).
3. Assign ownership: who creates what, who distributes where.
4. Set shared KPIs: impressions, leads captured, conversion rate, revenue attributed.

## Phase 3 — Produce

Build these deliverables:

### Partnership Brief
- Partner name + description
- Shared audience profile
- Campaign concept (1-2 sentences)
- Content deliverables with owners and deadlines
- Distribution plan (channels, dates, frequency)
- Success metrics with targets

### Co-Branded Content Plan
- Asset list: what gets created (blog, email, social, landing page, webinar)
- Brand guidelines for co-branding (logo placement, voice merge rules)
- Approval workflow: who signs off, how many rounds

### Cross-Promotion Schedule
- Week-by-week calendar of promotional activities
- Channel assignments per partner
- Email swap specs (list size, send date, subject line approval)

### Outreach Templates
- Partner pitch email (cold)
- Partner pitch email (warm intro)
- Follow-up sequence (3 touches)

## Phase 4 — Output

1. Deliver the partnership brief and campaign plan as structured documents.
2. Run all outreach copy through quality gates:
   - `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\banned_word_check.py <file>`
   - `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\four_us_score.py <file>`
3. Flag any co-branded content that needs legal review (claims, testimonials, data sharing).
4. Present the complete package with a timeline summary.

## Constraints

- No banned Tier 1 words in any outreach or co-branded copy.
- All partner claims must be verifiable — no inflated audience numbers.
- Email outreach must comply with CAN-SPAM (reference: `E:\Dev2\kai-cmo-harness-work\harness\references\cold-email-rules.md`).
- Cross-promotion emails require clear sender identification.
- Max 2 auto-retry cycles on quality gate failures.
