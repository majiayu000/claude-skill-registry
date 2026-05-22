---
name: draft-outreach
description: Draft sales and partnership outreach scripts (DMs, cold emails, follow-ups, objection handlers) for 1:1 relationship building.
---

# Draft Outreach Scripts

Create high-quality outreach artifacts for sales and partnership execution in S6B (Channels).

## When to Use

Use this skill when a task deliverable is 1:1 outreach communication (cold DM, cold email, partnership proposal, follow-up sequence) and you need a reusable artifact in-repo.

For marketing broadcast emails (newsletters, campaigns, segment blasts), prefer `/draft-email`.

For inbox triage workflows, prefer `/ops-inbox`.

## Operating Mode

**ARTIFACT DRAFTING ONLY — SALES & PARTNERSHIP OUTREACH**

**Allowed:** draft/edit outreach scripts, create follow-up sequences, write objection handlers, save artifacts under `docs/comms/outreach/`.

**Not allowed:** sending live messages automatically, inventing facts, bypassing explicit constraints, confusing outreach (1:1 sales) with marketing (1:many broadcast).

**Key distinction from draft-email:**
- **draft-outreach** = 1:1 sales/partnership outreach (cold DM, cold email, partnership proposals, follow-up sequences)
- **draft-email** = marketing broadcast (newsletters, campaigns, sequences to segments)

## Inputs

- **Objective** (what this outreach should achieve: demo booking, partnership meeting, early adopter signup)
- **Audience/recipient profile** (ICP segment, partner type, influencer tier)
- **Offer or value prop** (from S2B lp-offer positioning)
- **Outreach type** (dm, email, follow-up sequence)
- **Channel constraints** (character limits for DMs, platform-specific etiquette)
- **Objection map** (from S2B lp-offer)
- **Tone and brand constraints**
- **CTA and response deadline** (if any)
- **Channel ops context** when outreach is retailer, stockist, boutique, distributor, hotel-shop, or partner-facing:
  - `docs/business-os/strategy/<BIZ>/stockist-target-list.user.md` for target notes and prioritization
  - `docs/business-os/strategy/<BIZ>/channel-policy.user.md` for term and conflict constraints
  - `docs/business-os/strategy/<BIZ>/channel-health-log.user.md` for live-account context if the outreach is a reorder, check-in, or recovery message
  - `docs/business-os/strategy/<BIZ>/message-variants.user.md` for the pitch frames already being tested or retired

## Output

Create/update:

`docs/comms/outreach/<slug>-outreach.md`

Structure:

```markdown
# <Title> Outreach Script

**Type:** [DM | Email | Follow-up Sequence]
**Audience:** [ICP segment or partner profile]
**Objective:** [Specific goal]
**Channel:** [LinkedIn DM | Twitter DM | Cold Email | etc.]

## Primary Script

[Main outreach message optimized for clarity, personalization hook, and clear CTA]

## Follow-up Sequence

### Follow-up 1 (Day 3)
[Gentle reminder with additional value or social proof]

### Follow-up 2 (Day 7)
[Final touchpoint with alternative CTA or breakup message]

## Objection Handlers

### "[Common objection 1]"
**Response:** [Empathetic acknowledgment + reframe + value reinforcement]

### "[Common objection 2]"
**Response:** [...]

## Alternate Versions

[Optional: tone variants for different recipient personas]

## Review Checklist

- [ ] Opens with personalized hook (no generic spray-and-pray)
- [ ] Clearly states value prop in first 2 sentences
- [ ] CTA is specific and low-friction
- [ ] Respects channel constraints (character limits, etiquette)
- [ ] Objection handlers align with S2B positioning
- [ ] Follow-ups add incremental value (not just "bumping")
- [ ] Tone matches brand voice and audience expectations
- [ ] No unsubstantiated claims or invented facts

## Send Context

[Recommended timing, frequency, personalization variables to fill before sending]
```

## Workflow

1. **Restate objective and audience** — confirm outreach type (dm/email/follow-up) and recipient profile.
   - If this is retailer/stockist outreach, load the relevant target row or slot from `stockist-target-list.user.md` before drafting.
   - If a message-variants ledger exists, align the outreach with an active frame or explain why a new frame is needed.
2. **Draft primary script** — optimize for personalization hook, clarity, and action.
3. **Build follow-up sequence** — 2-3 touchpoints that add value (not just reminders).
4. **Write objection handlers** — map to S2B offer objections, keep responses concise.
5. **Add alternate versions** — when tone/strategy uncertainty exists (formal vs casual, value-first vs curiosity-first).
6. **Run checklist and revise** — verify personalization, CTA clarity, channel fit.
7. **Save artifact** — commit to `docs/comms/outreach/` and summarize recommended send context.

## Quality Checks

- **Personalization depth:** Does the hook reference specific recipient context (company, role, recent work)?
- **Value-first framing:** Does the script lead with what the recipient gains, not what you want?
- **CTA friction:** Is the ask specific, low-commitment, and easy to act on?
- **Channel appropriateness:** Does the script respect platform norms (LinkedIn formality, Twitter brevity, email structure)?
- **Objection pre-emption:** Are common blockers addressed proactively in the script or handled explicitly in objection responses?
- **Follow-up cadence:** Does the sequence avoid aggressive "bumping" and provide incremental value at each touchpoint?

## Integration

**Upstream:**
- `lp-channels` (S6B) identifies outreach channels and platform-specific tactics
- `lp-offer` (S2B) provides positioning, value props, and objection map
- GTM standing artifacts provide operator context for partner-specific outreach:
  - `stockist-target-list.user.md`
  - `channel-policy.user.md`
  - `channel-health-log.user.md`
  - `message-variants.user.md`

**Downstream:**
- Outreach scripts are used directly in sales execution (founder-led or delegated)
- Scripts inform partnership proposals and early adopter recruitment campaigns

## Completion Message

> "Outreach artifact ready: `docs/comms/outreach/<slug>-outreach.md`. Includes primary script, 2-touchpoint follow-up sequence, and objection handlers for [key objections]. Recommended send context: [timing/personalization notes]."
