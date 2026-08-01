---
name: kai-partnership
description: Partnership and co-marketing campaign planner — partner selection criteria, joint content strategy, cross-promotion plans, and co-branded assets. Use when "partnership", "co-marketing", "partner program", "cross-promotion", "joint venture", "co-branded", "partner campaign", or any request to plan or execute a marketing partnership.
---

# /kai-partnership — A Co-Marketing Deal Both Sides Can Execute

## Objective

A partnership plan a second company could read and agree to: candidate partners scored against a weighted rubric, a shared value proposition that explains what each audience gets, a funnel with named owners for every asset, a week-by-week cross-promotion schedule, and outreach copy ready to send. Shared KPIs are defined before the first asset is built, not reconstructed afterward. Partner selection is the load-bearing judgment — a well-run campaign with a mismatched audience produces reach and no pipeline.

## Done when

Work type `strategy-plan` (`also_covers: campaign-plan`) — floor **E3/C3/O1** (`harness/eco-floors.yaml`).

- **E3** — a named human approved the exact partnership brief and campaign plan. Where a partner is committed, the approval covers what each side owes and by when.
- **C3** — `banned_word_check` and `four_us_score` pass on all outreach and co-branded copy, and a named non-producer reads the plan end to end.
- **O1** — the shared KPIs (impressions, leads captured, conversion rate, attributed revenue) each carry a baseline, a threshold, and an owner, and the plan names the first work item it spawns.

Each asset the partnership later produces carries its own floor. Outreach that actually sends is `cold-email` (E5/C4/O3) and needs its own compliance pass; a co-hosted webinar landing page is `landing-page` (E5/C3/O4).

## Constraints

- **Partner claims must be verifiable.** No inflated audience numbers, no unverified list sizes, no borrowed metrics. A partner-supplied number is cited as partner-supplied.
- **Email outreach complies with CAN-SPAM** — see `harness/references/cold-email-rules.md`. Cross-promotion emails require clear sender identification, so the recipient knows whose list they are on and who is promoting.
- **Zero Tier 1 banned words** in any outreach or co-branded copy. Run `python scripts/quality_gates/banned_word_check.py <file>` and `python scripts/quality_gates/four_us_score.py <file>`. Max 2 auto-retry cycles on gate failures, each naming the specific failing dimension.
- **Flag for legal review** any co-branded content involving claims, testimonials, or data sharing between the parties. Flag it explicitly in the delivered package rather than resolving it in copy.
- **The scorecard threshold is binding:** a candidate below a 3.5 weighted average does not proceed to a brief.
- Every asset in the plan has one named owner and one deadline. Shared ownership with no name is how co-marketing dies.
- Kai plans and drafts. It does not send outreach, sign an agreement, commit list access, or share subscriber data. Human approval precedes every live action.
- **Read `MARKETING.md` from the project root before asking the user anything.** If it does not exist, build it from the codebase — README, manifests, landing pages, route files, analytics and email config — and confirm the draft. Do not open with discovery questions the repo can answer.

**Know these before planning** (from `MARKETING.md` first; ask only for what it cannot answer): the product and target audience on both sides · the partnership goal (audience growth, credibility, lead gen, content, distribution) · existing partnerships or candidates already in mind · budget constraints in cash, time, and content capacity · timeline and key dates · which partnership type applies.

**Partnership types:** content co-creation (webinar, guide, report) · cross-promotion (email swaps, social mentions) · bundle or integration (product-level) · event collaboration (co-hosted workshop, conference) · affiliate or referral (revenue share).

## Context

| Need | Load |
|---|---|
| Partnership structures, deal shapes, co-marketing mechanics | `knowledge/playbooks/partnership-comarketing.md` |
| Shared ICP definition and persona hooks | `knowledge/personas/_persona-index.md` |
| Email swap and sequence mechanics | `knowledge/channels/email-lifecycle.md` |
| CAN-SPAM, sender identity, consent basis | `harness/references/cold-email-rules.md` |
| Product, ICP, voice, current channels | `MARKETING.md` (project root) |

**Partner selection scorecard** — score each candidate 1-5 per criterion, weight, and sum:

| Criteria | Weight | Score 1-5 |
|----------|--------|-----------|
| Audience overlap (shared ICP) | 25% | |
| Audience size / reach | 20% | |
| Brand alignment (values, tone) | 20% | |
| Content quality | 15% | |
| Responsiveness / ease of working with | 10% | |
| Competitive risk (do they compete?) | 10% | |

**Minimum threshold: 3.5 weighted average to proceed.**

**Campaign architecture** covers four things: the shared value proposition (why this benefits both audiences) · the funnel map from awareness (social) through consideration (content) to conversion (offer) · ownership assignment (who creates what, who distributes where) · shared KPIs with targets.

**Deliverables** — structured documents plus a timeline summary. v1 declares no fixed workspace path, so write them where the user directs.

- **Partnership brief** — partner name and description, shared audience profile, campaign concept in 1-2 sentences, content deliverables with owners and deadlines, distribution plan (channels, dates, frequency), success metrics with targets.
- **Co-branded content plan** — asset list (blog, email, social, landing page, webinar), co-branding guidelines (logo placement, voice merge rules), approval workflow (who signs off, how many rounds).
- **Cross-promotion schedule** — week-by-week promotional calendar, channel assignments per partner, email swap specs (list size, send date, subject line approval).
- **Outreach templates** — cold partner pitch, warm-intro pitch, and a 3-touch follow-up sequence.

## Escalate when

- The best candidate competes with the business in a segment the user has not acknowledged.
- A partner's audience numbers cannot be verified and the campaign's targets depend on them.
- The partnership involves sharing subscriber or customer data — consent basis and data-processing terms are a legal decision, not a marketing one.
- Co-branded content carries claims or testimonials that need substantiation neither party has supplied.
- No candidate clears the 3.5 threshold.
- The partnership requires cash, list access, or content capacity the user has not authorized.
