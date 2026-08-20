---
name: prd-v09-launch-channels-orb
description: >
  Allocate launch channels using the Owned / Rented / Borrowed (ORB) framework during PRD v0.9
  Go-to-Market. Triggers on requests to pick launch channels, distribute the offer, build a
  channel portfolio, or when user asks "where do we launch?", "what channels?", "ORB",
  "owned vs rented vs borrowed", "channel allocation", "channel mix", "Corey Haines launch".
  Outputs GTM-* entries with Type=Channel, a channel-mix matrix, and a launch sequence.
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

# Launch Channels (ORB: Owned / Rented / Borrowed)

Position in workflow: v0.9 Offer Construction (Hormozi) → **v0.9 Launch Channels (ORB)** → v0.9 Launch Metrics

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | 1 channel per layer (3 channels total); single-week sequence |
| **standard** | 2–3 channels per layer; pre-launch / launch / post-launch sequence; attribution plan per channel |
| **deep** | Full portfolio; per-channel content strategy; budget allocation; per-channel ROI projection; channel-mix risk register |

## Framework: Owned / Rented / Borrowed (ORB)

ORB classifies every distribution channel by **who controls the audience**. The rule: **own the relationship, rent the platform, borrow the reach** — and balance the portfolio so no single channel can take you out.

| Layer | Definition | Examples | Cost | Compounding |
|-------|------------|----------|------|-------------|
| **Owned** | You control the audience and the channel | Email list, website, product itself, blog you host, customer base | Time + tools | High — every additional list member compounds future launches |
| **Rented** | You build presence on someone else's platform | Twitter/X, LinkedIn, YouTube, Slack/Discord communities, podcasts you host | Time | Medium — platform changes rules; audience is portable but messy |
| **Borrowed** | You access someone else's audience temporarily | Press, podcast guesting, influencers, paid acquisition, integrations, partnerships, affiliate | Money or favor | Low — one-time reach unless converted to Owned/Rented |

### The Channel Allocation Principles

1. **Build Owned before launch, rent through launch, borrow at launch.** Without an owned audience, the launch is a one-shot dependent on borrowed reach.
2. **Pick channels your best-fit segment already uses.** Pulled from the Positioning best-fit characteristics — not from "what's popular this quarter."
3. **One channel per layer to start.** Too many channels at once = no signal which is working. Add channels by tier 2–3 only once tier-1 attribution is clean.
4. **Convert Borrowed → Owned aggressively.** Every press hit, podcast guest spot, or partnership should funnel to an owned channel (email signup, demo request) — otherwise it's vanity reach.
5. **Borrowed scales reach; Owned scales repeat.** A launch is a moment; the goal is a list.

## Consumes

- **GTM-\* positioning statement** (from v0.9 Positioning) — Best-fit characteristics define where this segment actually spends time
- **GTM-\* offer card** (from v0.9 Offer Construction) — The unit being distributed; channels must accommodate the offer's complexity
- **PER-\* personas** (sharpened by Positioning) — Channel behavior data
- **BR-\* product type** (from v0.2) — Clone/Innovation/Slice/Wrapper channel mixes differ: Clone leans Borrowed-paid, Innovation leans Owned-content, Slice leans Rented-community
- **KPI-\* baseline targets** (from v0.3 Outcome Definition) — Per-channel attribution targets must roll up to baseline KPIs
- **DEP-\* release readiness** (from v0.8) — Channels only fire after DEP- criteria met

## Produces

- **GTM-\* with Type=Channel** (one per channel) — Channel name, layer (O/R/B), best-fit fit rationale, content plan, attribution plan, owner, timeline phase
- **GTM-\* channel-mix matrix** (one entry) — Portfolio summary: which channels in which phase, with budget/effort allocation
- **GTM-\* with Type=Sequence** — Pre-launch / launch / post-launch channel firing order

## Execution

### Step 1: Map the best-fit segment's channels

From the Positioning best-fit characteristics, list **where this segment is right now**. Be specific:

- Owned channels they already subscribe to (newsletters, podcasts)
- Rented platforms they actively use (with handles / community names)
- Borrowed sources they trust (publications, influencers, conferences)

Do not guess. If you don't know, that's a CFD- research gap.

### Step 2: Audit your existing assets

What do you already have in each ORB layer?

| Layer | Asset | Reach (est.) | Activation | Notes |
|-------|-------|--------------|------------|-------|
| Owned | Email list | | | |
| Owned | Existing customers | | | |
| Rented | Founder Twitter | | | |
| Rented | Company LinkedIn | | | |
| Borrowed | Press relationships | | | |
| Borrowed | Partner integrations | | | |

This audit reveals leverage — most launches over-rely on Borrowed because they have no Owned to lean on. Honest audit prevents that.

### Step 3: Pick channels per layer [standard+]

| Mode | Owned | Rented | Borrowed |
|------|-------|--------|----------|
| quick | 1 | 1 | 1 |
| standard | 2–3 | 2–3 | 2–3 |
| deep | Full portfolio | Full portfolio | Full portfolio |

For each candidate channel, score:
- **Fit**: Does best-fit segment actually use this? (1–5)
- **Reach**: How many of them does this channel touch? (Est.)
- **Effort**: What's the time cost per launch wave? (Hours)
- **Cost**: Direct $ cost?
- **Attribution**: Can we measure conversion from this channel?

Drop any candidate below **Fit 3/5** — no channel is worth it if best-fit doesn't show up there.

### Step 4: Sequence the launch

Three phases:

| Phase | Timeline | Channels active | Purpose |
|-------|----------|-----------------|---------|
| **Pre-launch** | T-30 to T-1 | Owned + Rented (warm) | Build anticipation, grow list |
| **Launch** | T-0 to T+7 | All three (Borrowed peaks here) | Maximum reach |
| **Post-launch** | T+7 to T+30 | Owned + Rented (sustain) | Convert reach to relationship |

Quick mode collapses this to a single week. Deep mode extends to 90 days with explicit content per phase.

### Step 5: Plan per-channel attribution

Every channel gets an attribution plan that ties to KPI-:

| Channel | UTM / tracking | KPI- attribution target | Conversion event |
|---------|----------------|-------------------------|------------------|
| Owned: Email | utm_source=email | KPI-XX signup | clicked email → reached offer page |
| Rented: Twitter | utm_source=twitter | KPI-XX signup | clicked tweet → reached offer page |
| Borrowed: PH | utm_source=producthunt | KPI-XX signup | PH referrer → reached offer page |

If a channel can't be attributed, demote it to "supporting" status (still useful for context, but don't count it).

### Step 6: Convert Borrowed → Owned [standard+]

For every Borrowed channel, define the **next step that converts to Owned**. Examples:
- Press hit → article includes "join our list for [bonus]"
- Podcast guest → custom URL with email opt-in
- Product Hunt launch → "early-access list" signup as primary CTA, not "buy now"

If a Borrowed channel has no conversion-to-Owned plan, the launch is leaking value.

### Step 7: Build the channel-mix matrix

A single GTM-* entry summarizing the portfolio. See output template below.

## Output Template

```
GTM-XXX: Channel — [Channel Name]
Type: Channel
Layer: [Owned | Rented | Borrowed]
Owner: [Person / team]
Status: [Planned | Active | Live]

Channel: [Specific platform or property]
Best-fit fit: [Why this channel reaches PER-XXX — anchored in Positioning best-fit characteristics]
Fit score: X/5
Reach estimate: [#]
Effort per wave: [Hours]
Cost: [$]
Attribution: [Tracking method, e.g., utm_source=...]

Content plan:
  Pre-launch: [What goes out, when, what messaging]
  Launch: [...]
  Post-launch: [...]

Conversion-to-Owned [if Borrowed]: [How this channel funnels to email list / signup]

Linked IDs: PER-XXX (segment), GTM-YYY (positioning), GTM-ZZZ (offer), KPI-AAA (attribution target)
```

```
GTM-XXX: Channel-Mix Matrix
Type: Sequence
Status: Approved

Pre-launch (T-30 to T-1):
  Owned: GTM-AAA (email), GTM-BBB (blog)
  Rented: GTM-CCC (Twitter)
  Borrowed: — (none active yet)

Launch (T-0 to T+7):
  Owned: GTM-AAA, GTM-BBB
  Rented: GTM-CCC, GTM-DDD (LinkedIn)
  Borrowed: GTM-EEE (Product Hunt), GTM-FFF (Press)

Post-launch (T+7 to T+30):
  Owned: GTM-AAA (drip sequence)
  Rented: GTM-CCC (results / social proof posts)
  Borrowed: GTM-FFF (case study placements)

Total budget: $X (Borrowed: $X; Rented tools: $Y; Owned: $Z)
Total effort: X hours/week pre-launch; Y hours during launch week

Linked IDs: GTM-YYY (positioning), GTM-ZZZ (offer), DEP-AAA (release readiness), KPI-BBB (attribution rollup)
```

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Borrowed-only launch** | "We'll launch on Product Hunt and Twitter" with no email list | Build Owned for 30+ days pre-launch or accept the one-shot risk |
| **All channels at once** | 8 channels in launch week, no idea which worked | Cut to 1 per layer until attribution is clean |
| **Channels not used by best-fit** | "We should be on TikTok" when segment is on LinkedIn | Drop the channel; segment fit > channel popularity |
| **No conversion path** | Press hit drives traffic to a homepage with no CTA | Every Borrowed channel needs an email-capture CTA |
| **Sequence flattening** | All channels fire on launch day | Pre-launch matters — borrow only after Owned and Rented are warm |
| **Vanity reach** | "We got 50k impressions" but no signups | Drop the channel or fix attribution |

## Quality Gates

Before proceeding to Launch Metrics:

- [ ] At least one channel per layer (Owned + Rented + Borrowed), each with Fit ≥ 3/5
- [ ] Every channel traces to best-fit characteristics from Positioning
- [ ] Every channel has an attribution plan (UTM or equivalent)
- [ ] Every Borrowed channel has a defined conversion-to-Owned path
- [ ] Sequence covers pre-launch, launch, post-launch phases (standard+)
- [ ] Channel-mix matrix GTM-* entry exists and references all channel GTM-* entries

## Downstream Connections

| Consumer | What it uses | Example |
|----------|--------------|---------|
| **Launch Metrics** | Per-channel attribution targets become KPI- entries | Per-channel UTM → KPI-channel-signups |
| **Feedback Loop Setup** | Active channels become feedback sources | Twitter mentions → CFD- entries |
| **v0.9 Tactical playbooks** | AEO audit, alternatives pages, cold outreach, HN/Reddit launch all attach to specific channels named here | Channel = AEO target |
| **v1.0 Crossing the Chasm (Moore)** | Channel mix shifts per adoption stage | Early-adopter channels ≠ early-majority channels |

## Detailed References

- Corey Haines, *Marketing Skills* repo — `launch` skill (ORB classification)
- Joe Pulizzi, *Content Inc.* (Owned-first compounding)
- (No bundled `references/` — read source skills for depth)
