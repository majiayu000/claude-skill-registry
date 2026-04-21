---
name: launch-tier
description: "Classify releases into launch tiers and plan go-to-market. Based on Lauchengco's Loved framework."
instruction_budget: 58
---

# Launch Tier Classification

Every release gets classified before planning begins. Source: Lauchengco (Loved).

## Tier Definitions

| Tier | Type | Effort | Examples |
|------|------|--------|---------|
| **1** | Major | Full cross-functional | New product, major pivot, category-defining |
| **2** | Significant | Targeted campaigns | Feature launch, positioning reinforcement |
| **3** | Incremental | Lightweight | Bug fixes, minor improvements, release notes |

## Classification Criteria
- Does this change our positioning? -> Tier 1
- Does this strengthen existing positioning? -> Tier 2
- Is this an incremental improvement? -> Tier 3

## Per-Tier Activities

### Software (default)
**Tier 1**: Press, events, campaigns, sales enablement, analyst briefings, customer advisory
**Tier 2**: Blog post, targeted campaigns, sales enablement update, in-product announcement
**Tier 3**: Release notes, changelog, in-product notification, knowledge base update

### Content Products (courses, publications, media) (v0.11.0)
**Tier 1**: Platform launch (new course on marketplace), PR/media coverage, launch webinar, guest appearances
**Tier 2**: New module/section, cross-promotion, community announcement, guest post
**Tier 3**: Content update, errata fix, supplementary material, minor revision

### AI Tools (v0.11.0)
**Tier 1**: Public launch, ProductHunt/HackerNews, documentation site, demo video
**Tier 2**: New capability/model, integration partnership, case study
**Tier 3**: Prompt improvement, model update, bug fix, eval result improvement

### Service Offerings (v0.11.0)
**Tier 1**: New service line launch, case study PR, conference talk, partnership announcement
**Tier 2**: New package/tier, testimonial campaign, process improvement announcement
**Tier 3**: Pricing update, workflow refinement, expanded availability

## Behavioral Science in Positioning (Shotton)
Use biases ETHICALLY to help users understand value:
- **Social proof**: Reference customers, usage numbers (real, not inflated)
- **Anchoring**: Frame value relative to alternatives
- **Framing**: Position the benefit, not just the feature
- **Never**: Confirmshaming, hidden costs, forced continuity, misdirection

## Canvas Output
Update `canvas/go-to-market.yml` with tier classification and launch plan.

## Ethical Engagement Design (Eyal -- Hook Model + Indistractable)

Eyal's work spans two complementary books: **Hooked** (2014) provides the Hook Model for building habit-forming products; **Indistractable** (2019) provides the user-side framework for managing attention. The Manipulation Matrix below bridges both — ethical engagement design means building hooks that users would choose even with full information.

The Hook Model is most relevant at L3 (Solution design) for engagement architecture, not just L5 (Market). Apply during solution design when the product requires recurring usage.

For products that need user retention, design engagement ethically using the Hook Canvas:

### Hook Canvas
Map the four components of habit formation:
- **Trigger**: What prompts the user to engage? (External: notification, email. Internal: emotion, routine.)
- **Action**: What is the simplest behavior in anticipation of reward? (Must be easier than thinking.)
- **Variable Reward**: What reward satisfies the user's need while leaving them wanting more? (Tribe: social, Hunt: resources, Self: mastery.)
- **Investment**: What bit of work does the user put in that improves the next cycle? (Data, content, reputation, skill.)

### Manipulation Matrix (Ethical Gate — NUDGE)
Before implementing engagement design, answer honestly:
1. **Does it materially improve the user's life?** (Not just "engagement" — actual value.)
2. **Would you use it yourself?** (The maker's test.)

| | User Benefits | User Doesn't Benefit |
|---|---|---|
| **Maker Uses It** | **Facilitator** (ethical) | **Entertainer** (proceed with caution) |
| **Maker Doesn't Use It** | **Peddler** (risky) | **Dealer** (unethical — do not build) |

Only **Facilitator** products should be built without reservation. Entertainers need honest self-assessment. Peddlers and Dealers trigger anti-pattern #10 (Dark Pattern Marketing).

Update `canvas/go-to-market.yml` engagement_design section with Hook Canvas results.

*Source: Eyal (Hooked), with ethical framework from the Manipulation Matrix*

## Pre-Launch Bias Check

Before classifying a launch tier, run `/bias-check` for L5-specific biases:
- **Optimism bias**: Are we overweighting positive signals and ignoring negative ones?
- **Confirmation bias**: Are we seeking validation that "it's ready to ship" rather than honestly assessing market readiness?
- **Anchoring**: Are we fixated on the initial positioning without considering what evidence now suggests?
- **Sunk cost fallacy**: Are we launching because we've invested too much to stop, not because the market signals are positive?

If `/bias-check` reveals significant biases, address them before finalizing the launch tier.

## After Launch: The L5 -> L2 Feedback Loop

**This is critical.** After launch, market feedback must flow back into discovery:

1. **Capture market signals** (within 2-4 weeks post-launch).
   Check the product-type-appropriate metrics canvas via `/dora-check`:

   **Software**: feature usage, retention, conversion, support tickets, NPS/CSAT
   **Content**: refund rate, completion rate, drop-off points, return rate, reviews, NPS
   **AI tool**: task success rate, retention, DAU, refund rate, user feedback
   **Service**: client satisfaction (NPS/CSAT), referral rate, retention, delivery lead time feedback

2. **Validate scenarios against reality** (Hoskins):
   - For each scenario in `canvas/scenarios.yml` linked to this launch: did the persona's story play out?
   - Update `lifecycle.validated_in_market`: confirmed, partial, or invalidated
   - Invalidated scenarios are the most valuable learning — they reveal where the user model was wrong

3. **Evaluate against L2 assumptions**:
   - Do the signals confirm the L2 opportunity we solved for?
   - Are there NEW needs we didn't anticipate?
   - Did users "hire" the product for a different job than expected? (JTBD)
   - Do real user stories suggest NEW scenarios not in `canvas/scenarios.yml`?

4. **Feed back into discovery**:
   - If signals confirm: update confidence scores, mark scenarios as `validated`, celebrate validated learning
   - If signals reveal NEW opportunities: **spawn a new L2 Opportunity diamond** with market evidence as the starting data. Create new scenarios from real user stories.
   - If signals contradict: flag for diamond regression, mark scenarios as `invalidated`, update corrections.md

This closes the full Mycelium loop: Purpose -> Strategy -> Discovery -> Solution -> Delivery -> **Market -> Discovery**.

## Cycle History Recording

After launch feedback is captured (L5 → L2 loop), update the cycle record in `canvas/cycle-history.yml`:

1. Find the cycle record for this leaf (created by `/retrospective` at delivery completion)
2. Add **actual** market outcomes: user metrics, adoption data, NPS/CSAT, revenue impact
   - **Source this data from `/metrics-pull`** where possible (v0.14): 24-48h after launch to capture the bump, then weekly for the first month. Snapshots live at `.claude/evals/metrics/<source>/*.json`. This replaces manual "I checked the dashboard" reports with timestamped evidence.
   - If `active-metrics.yml` has no configured source for the relevant channel, run `/metrics-detect` first.
3. Update the calibration section: compare predicted value/usability risk against actual market reception
4. If market signals contradict the original L2 opportunity assumptions, note this as calibration data

If no cycle record exists yet (leaf went directly to market without retrospective), create one now.

This closes the data loop: predicted ICE → actual delivery metrics → actual market outcomes → calibration for future scoring.

## Decision Log (MANDATORY per G-P4)
**APPEND** a `### Launch Tier Classification` entry to `harness/decision-log.md` with: tier assigned, positioning rationale, key risks, go-to-market approach.

## Theory Citations
- Lauchengco: Loved (launch tier classification, positioning)
- Shotton: Choice Factory (ethical behavioral science in positioning)
- Kim: Three Ways (Second Way -- amplify feedback loops right-to-left)
- Torres: Continuous Discovery (market signals feed back into OST)
