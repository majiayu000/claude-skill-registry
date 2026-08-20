---
name: prd-v09-cold-outreach-tiered
description: >
  Build Tier 1/2/3 cold outreach sequences differentiated by personalization depth and research
  signal strength during PRD v0.9 Go-to-Market. Triggers on requests to plan cold outreach,
  founder-led sales, or when user asks "cold email sequence", "outbound campaign", "founder
  outreach", "LinkedIn outreach", "Tier 1 personalization", "predictable revenue", "sales
  cadence", "BDR sequence". Outputs GTM-OUT-* sequence entries and lead-list references.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
  - WebFetch

execution_modes:
  default: standard
  supports: [quick, standard, deep]
---

# Cold Outreach (Tiered: 1:1 / 1:few / 1:many)

Position in workflow: v0.9 Offer Construction → **v0.9 Cold Outreach (Tiered)** → v0.9 Launch Metrics

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | One tier (typically Tier 2); 3-touch sequence; lead-list scoring rubric |
| **standard** | All three tiers; 3–5 touches each; lead-list scoring + tier-assignment logic; reply-handling guide |
| **deep** | All tiers + A/B subject lines per tier; channel mix (email + LinkedIn + voicemail); reply-rate baselines; objection library |

## What This Does

Builds three differentiated cold-outreach sequences, each calibrated to a different ratio of research-per-lead:

- **Tier 1 (1:1, founder-led)** — Hand-researched. Highly personalized. Each touch references something specific. Volume: 10–30 contacts.
- **Tier 2 (1:few, semi-automated)** — Segment-personalized. Template with 3–5 dynamic variables per recipient. Volume: 100–500 contacts.
- **Tier 3 (1:many, automated)** — Broad-fit. Template only, minimal personalization. Volume: 1,000–10,000+ contacts.

The tiers are **not "good/better/best"** — each has its place. Tier 3 fills the top of the funnel cheaply. Tier 2 carries the bulk. Tier 1 closes the highest-value targets that templates can never reach.

## How It Works

1. **Source lead lists from ICP** — Pull from the Positioning best-fit characteristics. Use enrichment tools (Apollo, Clay, Clearbit) or LinkedIn Sales Nav search anchored on firmographic + behavioral signals from PER-.
2. **Score each lead's signal strength** (1–5):
   - **Trigger signal** — Recent funding, hiring, product launch, public pain (5)
   - **Fit signal** — Strong firmographic/behavioral match without specific trigger (3–4)
   - **Cold signal** — Broad-fit only; no specific signal (1–2)
3. **Tier assignment**:
   - Signal 4–5 + opportunity size ≥ threshold → **Tier 1**
   - Signal 3–4 → **Tier 2**
   - Signal 1–2 → **Tier 3** (or drop if list is large enough)
4. **Build per-tier sequences** — Each tier gets its own template structure (see Output Template). Tier 1 is hand-drafted; Tier 2 is template + variables; Tier 3 is template only.
5. **End every sequence on the guarantee** — The guarantee from [prd-v09-offer-construction-hormozi](../prd-v09-offer-construction-hormozi/SKILL.md) is the reply-friction killer. Don't ask for a meeting cold; ask them to invoke the guarantee.
6. **Plan reply handling** — Define what counts as a reply (positive, ask, objection, unsubscribe), and have a response cadence for each. Tier 1 replies go to founder immediately. Tier 3 replies route through a templatized objection library.

## Example

B2B SaaS founder launching, ICP = Series A SaaS PMs.

**Tier 1** (20 hand-picked targets):
- Touch 1 (Day 0, email): Reference specific recent blog post + offer specific insight on their problem
- Touch 2 (Day 4, LinkedIn): Connect with a one-line follow-up referencing the email
- Touch 3 (Day 10, email): Share a relevant case study from a similar company; mention the guarantee
- Touch 4 (Day 18, email): Soft breakup — "want me to circle back in a quarter?"

**Tier 2** (200 mid-signal leads):
- Touch 1 (Day 0, email): Template with 3 variables ({company}, {pain point}, {peer company}). 6–10 sentences max.
- Touch 2 (Day 3, email): One-line bump
- Touch 3 (Day 7, email): Case study + guarantee mention
- Touch 4 (Day 14, email): Breakup

**Tier 3** (2,000 broad-fit leads):
- Touch 1 (Day 0, email): Template only. 4–6 sentences. Lead with category insight, not pitch.
- Touch 2 (Day 5, email): Case study
- Touch 3 (Day 12, email): Breakup ("last note from me")

Expected reply rates: Tier 1 = 30–50%; Tier 2 = 8–15%; Tier 3 = 1–3%.

## What You Get Back

- **GTM-OUT-\* entries** (one per tier sequence) — Tier metadata, per-touch templates, channel mix, timing
- **GTM-OUT-touch-\*** entries — Individual touch templates with subject line, body, channel
- **Lead-list scoring rubric** (single GTM-*) — How to assign tier
- **Reply-handling guide** — What counts as a reply; routing rules

## When to Use It

| Trigger | Mode |
|---------|------|
| B2B / founder-led sales motion | standard |
| Post-launch acquisition push | standard |
| Paid channels too expensive (high CAC) | standard |
| Specific ABM-style campaign against named accounts | deep, Tier 1 only |
| Mass-market consumer product with no individual-buyer relationship | **do not use** — wrong channel |

## Consumes

- **GTM-\* positioning** + **PER-\* best-fit characteristics** — Source for ICP and message anchoring
- **GTM-\* offer card** + **GTM-\* guarantee** (from v0.9 Offer Construction) — Sequences end on the guarantee, not a meeting ask
- **CFD-\* customer stories** (from v0.1–v0.4 + post-launch) — Case studies for touch 3
- **BR-POS-\* constraints** — Tier targeting must honor "not for" rules
- **KPI-\* targets** (from v0.3 + v0.9 Launch Metrics) — Reply rate and meeting-booked targets per tier

## Produces

- **GTM-OUT-\* tier entries** — One per tier with sequence metadata
- **GTM-OUT-touch-\* entries** — Per-touch templates (subject, body, channel, timing)
- **GTM-\* lead-list scoring rubric**
- **CFD-\* gaps** — When sequences reveal objections we can't answer, log as CFD- research gaps

## Output Template

```
GTM-OUT-XXX: Tier [1 | 2 | 3] Sequence
Type: Outreach
Tier: [1 | 2 | 3]
Volume: [target lead count]
Owner: [Person / role]
Status: [Planned | Active | Paused]

Lead profile:
  Signal strength: [4–5 | 3–4 | 1–2]
  Source: [Apollo | LinkedIn Sales Nav | Clay | Manual]
  Best-fit criteria: [Anchored in PER- characteristics]

Sequence:
  Touch 1: GTM-OUT-touch-AAA — Day 0, [channel]
  Touch 2: GTM-OUT-touch-BBB — Day [N], [channel]
  Touch 3: GTM-OUT-touch-CCC — Day [N], [channel]
  Touch 4: GTM-OUT-touch-DDD — Day [N], [channel]

Reply handling:
  Positive: [Routing]
  Ask: [Routing]
  Objection: [Routing — point to objection library]
  Unsubscribe: [Action]

KPI targets:
  Reply rate: [Tier 1: 30–50% | Tier 2: 8–15% | Tier 3: 1–3%]
  Meeting-booked rate: [varies]

Linked IDs: PER-XXX, GTM-YYY (positioning), GTM-ZZZ (offer), GTM-AAA (guarantee), KPI-BBB
```

```
GTM-OUT-touch-XXX: Touch [N] — Tier [1|2|3]
Channel: [Email | LinkedIn | Voicemail | SMS]
Subject: "[Subject line — A/B variants for deep mode]"

Body:
  [Template body, with {variable} markers for tiers 2 and 3]

Personalization tier:
  Tier 1: Hand-drafted; each touch references something specific
  Tier 2: Template + 3–5 variables — {company}, {pain_point}, {peer_company}
  Tier 3: Template only

Ends on: [Guarantee mention | Case study | Soft ask | Breakup]

Linked IDs: GTM-OUT-XXX (parent sequence), GTM-AAA (guarantee)
```

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Same template for all tiers** | Tier 1 reply rate < 10% | Tier 1 must be hand-drafted; templates are the floor, not the ceiling |
| **Fake personalization** | "{first_name}, I love what {company} is doing" | Either personalize for real (Tier 1) or stop pretending (Tier 3) |
| **Ask for meeting cold** | "Got 15 min next week?" in touch 1 | Lead with value; ask for guarantee invocation or content engagement instead |
| **No breakup** | Sequence runs forever, hurting deliverability | Always include a final-touch breakup |
| **No tier assignment logic** | All leads in same tier | Build the scoring rubric before sending anything |
| **Outreach without offer** | Sequence runs before Offer Construction is complete | Wait — without the guarantee, the sequence ends on weak CTAs |
| **Outreach without positioning** | Generic value claims | Reply rates die; honor the Dunford positioning |

## Quality Gates

Before launching:

- [ ] All three tiers defined (or quick-mode single tier with documented reason)
- [ ] Per-touch templates exist and respect BR-POS-* constraints
- [ ] Sequences end on the guarantee (or explicit reason why not)
- [ ] Reply-handling rules documented
- [ ] KPI- targets set per tier (reply rate + meeting-booked rate)
- [ ] Unsubscribe path is one-click and honored
- [ ] Spam-compliance check (CAN-SPAM, GDPR if applicable) done

## Downstream Connections

| Consumer | What it uses | Example |
|----------|--------------|---------|
| **Launch Channels (ORB)** | Cold outreach is a Borrowed channel; rolls into mix matrix | Tier 1 = Borrowed-time; Tier 2/3 = Borrowed-volume |
| **Launch Metrics** | Per-tier reply rates become KPI- entries | KPI-tier1-reply-rate |
| **Feedback Loop Setup** | Reply objections feed CFD- | "Why we passed" replies → CFD- pattern |
| **v1.0 Continuous Discovery** | High-engagement Tier 1 replies = founder interviews | Reply → CFD- interview with confidence ≥ 3/5 |

## Detailed References

- Aaron Ross, *Predictable Revenue* (2011) — Tier 2/3 outbound structure
- Aaron Ross, *From Impossible to Inevitable* (2016) — Sequencing
- BrianRWagner's `cold-outreach-sequence` skill (ai-marketing-claude-code-skills)
- (No bundled `references/` — sequences are templates, not theory)
