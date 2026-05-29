---
name: launch-tier
description: "Classify releases into launch tiers and plan go-to-market. Based on Lauchengco's Loved framework."
metadata:
  instruction_budget: "62"
  framework_dependency: "mycelium"
  framework_dependency_note: "This skill is designed to run within the Mycelium framework (https://github.com/haabe/mycelium). Standalone use will skip the canvas state, theory gates, and harness behavior the skill assumes. Install: /plugin install mycelium@haabe/mycelium."
---

# Launch Tier Classification

Every release gets classified before planning begins. Source: Lauchengco (Loved).

## Preflight: Read target canvas file(s) before any Write/Edit

**Hard rule.** Before issuing `Write` or `Edit` against any `.claude/canvas/*.yml`, use the **Read tool** on that file in this session. Claude Code's Read-before-Write check requires the `Read` tool specifically — `cat`/`head`/`grep` via Bash do NOT satisfy it.

**Edit vs Write — different cost profiles** (verified 2026-05-14):
- **`Edit`** (exact-string replacement): `Read` with `limit: 1` satisfies the check at ~50 tokens. State-tracking is per-file, not per-byte — subsequent `Edit` calls work anywhere in the file. Use this for partial updates against large canvas files (e.g., `purpose.yml` at 800+ lines).
- **`Write`** (full replacement): do a **full Read** first. Write obliterates the file; you should see what you're about to replace. The `limit:1` shortcut is *not* appropriate here.

**ID-bearing entries — scan the ID space before assigning** (added 2026-05-15, v0.23.19): When adding a new component, opportunity, solution, or any other ID-bearing entry to a canvas file, run a Bash grep first to confirm the next ID in your prefix sequence is actually free:

```
grep "^  - id: <prefix>-" .claude/canvas/<file>.yml | sort -u
```

Replace `<prefix>` with the canvas's ID prefix (`comp` for landscape, `opp` for opportunities, `sol` for solutions, `ht` for human-tasks, etc.). Then pick the next free integer. `validate_canvas.py` has a duplicate-ID check (lines 230-239) that catches the failure on CI, but a duplicate can persist in the working tree for days if CI isn't run between edit and discovery — see roadmap-repo `corrections.md` 2026-05-15 "Duplicate canvas ID created in landscape.yml" for the worked example.

Original failure mode: anti-pattern #7 instance #5, 2026-05-09 — agent conflated Bash `head` with the Read tool, lost ~14k tokens to a Write-fail → remedial-full-Read → re-Write loop. The `limit:1` discipline (graduated 2026-05-14, v0.23.18) prevents the second-order cost where the agent *correctly* follows the rule but full-Reads every time. The ID-scan discipline (graduated 2026-05-15, v0.23.19) prevents the related class where the agent reads enough of the file to satisfy the Edit check but not enough to see existing ID assignments — kin to anti-pattern #8 (Stale State Read).

If this skill writes to multiple canvas files, register each one first (limit:1 for Edit-only paths; full Read for Write paths) AND ID-scan any prefix you intend to assign.

See `CLAUDE.md` *Canvas writes — Read before Write* for the canonical rule.

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
Update `.claude/canvas/go-to-market.yml` with tier classification and launch plan.

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

Update `.claude/canvas/go-to-market.yml` engagement_design section with Hook Canvas results.

*Source: Eyal (Hooked), with ethical framework from the Manipulation Matrix*

## Pre-Launch Bias Check

Before classifying a launch tier, run `/mycelium:bias-check` for L5-specific biases:
- **Optimism bias**: Are we overweighting positive signals and ignoring negative ones?
- **Confirmation bias**: Are we seeking validation that "it's ready to ship" rather than honestly assessing market readiness?
- **Anchoring**: Are we fixated on the initial positioning without considering what evidence now suggests?
- **Sunk cost fallacy**: Are we launching because we've invested too much to stop, not because the market signals are positive?

If `/mycelium:bias-check` reveals significant biases, address them before finalizing the launch tier.

## After Launch: The L5 -> L2 Feedback Loop

**This is critical.** After launch, market feedback must flow back into discovery:

1. **Capture market signals** (within 2-4 weeks post-launch).
   Check the product-type-appropriate metrics canvas via `/mycelium:dora-check`:

   **Software**: feature usage, retention, conversion, support tickets, NPS/CSAT
   **Content**: refund rate, completion rate, drop-off points, return rate, reviews, NPS
   **AI tool**: task success rate, retention, DAU, refund rate, user feedback
   **Service**: client satisfaction (NPS/CSAT), referral rate, retention, delivery lead time feedback

2. **Validate scenarios against reality** (Hoskins):
   - For each scenario in `.claude/canvas/scenarios.yml` linked to this launch: did the persona's story play out?
   - Update `lifecycle.validated_in_market`: confirmed, partial, or invalidated
   - Invalidated scenarios are the most valuable learning — they reveal where the user model was wrong

3. **Evaluate against L2 assumptions**:
   - Do the signals confirm the L2 opportunity we solved for?
   - Are there NEW needs we didn't anticipate?
   - Did users "hire" the product for a different job than expected? (JTBD)
   - Do real user stories suggest NEW scenarios not in `.claude/canvas/scenarios.yml`?

4. **Feed back into discovery**:
   - If signals confirm: update confidence scores, mark scenarios as `validated`, celebrate validated learning
   - If signals reveal NEW opportunities: **spawn a new L2 Opportunity diamond** with market evidence as the starting data. Create new scenarios from real user stories.
   - If signals contradict: flag for diamond regression, mark scenarios as `invalidated`, update corrections.md

This closes the full Mycelium loop: Purpose -> Strategy -> Discovery -> Solution -> Delivery -> **Market -> Discovery**.

## Cycle History Recording

After launch feedback is captured (L5 → L2 loop), update the cycle record in `.claude/canvas/cycle-history.yml`:

1. Find the cycle record for this leaf (created by `/mycelium:retrospective` at delivery completion)
2. Add **actual** market outcomes: user metrics, adoption data, NPS/CSAT, revenue impact
   - **Source this data from `/mycelium:metrics-pull`** where possible (v0.14): 24-48h after launch to capture the bump, then weekly for the first month. Snapshots live at `.claude/evals/metrics/<source>/*.json`. This replaces manual "I checked the dashboard" reports with timestamped evidence.
   - If `.claude/jit-tooling/active-metrics.yml` has no configured source for the relevant channel, run `/mycelium:metrics-detect` first.
3. Update the calibration section: compare predicted value/usability risk against actual market reception
4. If market signals contradict the original L2 opportunity assumptions, note this as calibration data

If no cycle record exists yet (leaf went directly to market without retrospective), create one now.

This closes the data loop: predicted ICE → actual delivery metrics → actual market outcomes → calibration for future scoring.

## Decision Log (MANDATORY per G-P4)
**APPEND** a `### Launch Tier Classification` entry to `.claude/harness/decision-log.md` with: tier assigned, positioning rationale, key risks, go-to-market approach.

## Theory Citations
- Lauchengco: Loved (launch tier classification, positioning)
- Shotton: Choice Factory (ethical behavioral science in positioning)
- Kim: Three Ways (Second Way -- amplify feedback loops right-to-left)
- Torres: Continuous Discovery (market signals feed back into OST)

## Counter-Argument Check (Bias Mitigation)

Before finalizing the launch tier classification AND before drafting any positioning copy, draft a one-line counter-argument: *"What's the strongest case that this is a smaller tier than I'm claiming? That this positioning is overstating impact? That market readiness is weaker than the evidence suggests?"* If you can't articulate one, run `/mycelium:devils-advocate` before proceeding.

This addresses the bias cluster documented in corrections.md (L5 sycophancy 2026-04-20 — promotional language in decision logs at L5 — explicitly named this skill's domain; eval overfitting 2026-04-30; sharper-framing-isn't-righter 2026-05-03). L5 work is the highest-risk context for bias because the framing pressure is explicit ("we're going to market"). G-M1 catches the WORST language, but bias appears in subtler tier-classification and positioning choices that G-M1 doesn't see. The counter-argument is the upstream check.
