---
name: grow-business
description: 'Guided journey from a business with lucky months to a repeatable growth engine that produces a forecast. Orchestrates nine skills phase by phase - one-page-marketing, hundred-million-offers, predictable-revenue, contagious, influence-psychology, crossing-the-chasm, cold-start-problem, lean-analytics, negotiation - asking the user questions at every decision point and recording results in the project docs/ folder (MARKETING.md, OFFER.md, METRICS.md, GROW-BUSINESS-PLAN.md) so the journey resumes across sessions. Use when the user wants to build a marketing and sales system, manufacture predictable pipeline, engineer word-of-mouth and referrals, or says ''revenue is real but lumpy and I need growth that repeats''. If the offer, retention, or operations underneath are broken, run improve-business first; with no paying customers yet, start with create-business; when the product itself must carry the growth loops, use grow-app. For one framework in isolation, invoke that skill directly.'
license: MIT
metadata:
  author: wondelai
  version: "1.0.0"
---

# Grow a Business

You already have the hard part: a product people pay for. Revenue is real but lumpy — a good month came from a conference you happened to attend or a referral that happened to land, and none of it repeats on demand. This journey turns that traction into a repeatable growth engine across nine phases: a marketing map, an irresistible offer, an outbound motion, engineered word-of-mouth, persuasion on every surface, a mainstream go-to-market, a compounding network, one honest metric, and the discipline to hold price. It is interactive — the agent asks before every decision — and resumable, because every decision and asset is recorded in `docs/`. Install the whole stack at once with `npx skills add wondelai/skills --all --global`, or let each phase pull its skill on demand.

## Core Principle

**Build a repeatable growth engine: each phase produces an asset the next phase consumes — offer feeds pipeline, pipeline feeds word-of-mouth, metrics keep it honest.** The order is load-bearing; a skipped Phase 1 leaves the later phases with no shared target. This skill sequences the phases, asks the decision questions, and records the answers. The constituent skills carry the method — invoke them rather than improvising their frameworks.

The offer comes before every channel on purpose: sending traffic to a weak offer is the most expensive mistake in growth, so Phase 2 is fixed before outbound, virality, or repositioning turn on.

## Journey Map

| Phase | Skill | Question it answers | Artifact |
|---|---|---|---|
| 1 | one-page-marketing | Which niche, and which square of the machine is empty? | Creates docs/MARKETING.md |
| 2 | hundred-million-offers | Why should they buy this instead of the alternative? | Extends docs/OFFER.md |
| 3 | predictable-revenue | How do we manufacture pipeline on demand? | Extends docs/MARKETING.md |
| 4 | contagious | Why would anyone share this? | Extends docs/MARKETING.md |
| 5 | influence-psychology | Why do they say yes on the page? | Extends docs/OFFER.md |
| 6 | crossing-the-chasm | How do we reach the mainstream buyer? | Extends docs/STRATEGY.md + docs/CUSTOMER.md |
| 7 | cold-start-problem | How does the network do the acquiring? | Extends docs/MARKETING.md |
| 8 | lean-analytics | Which one number tells us it is working? | Extends docs/METRICS.md |
| 9 | negotiation | How do we capture the value instead of discounting it? | Extends docs/OFFER.md |

Four of the nine phases write to MARKETING.md — the flagship this journey creates. OFFER.md, STRATEGY.md, METRICS.md, and CUSTOMER.md are extended, so files a prior create-business journey already owns are reused and augmented, never overwritten.

The tracker `docs/GROW-BUSINESS-PLAN.md` is private to this journey and never shared with another; it is the resume point that carries state across sessions.

## Operating Rules

1. **Resume first.** Before anything else, read `docs/GROW-BUSINESS-PLAN.md` and every artifact in the Journey Map. If the tracker exists, summarize the journey state in 3-5 lines and ask which phase to enter. Done when the user has confirmed an entry point. A journey with a tracker is resumed, never restarted.
2. **Intake on first run only.** No tracker: run the Intake below, then create `docs/GROW-BUSINESS-PLAN.md` with every phase statused `pending | in-progress | awaiting-evidence | done | deferred: reason | skipped: reason`. Done when the tracker exists and the user has confirmed the phase plan.
3. **Phase entry.** Announce: what the phase does, the decision it forces, the artifact it produces, rough effort. Offer proceed / skip / defer — phases marked GATE may be deferred, never skipped. Mark the phase `in-progress` on proceed. Done when the user chose.
4. **Skill invocation and fallback.** Invoke the phase's skill by its slug. If it is not available, offer: `npx skills add wondelai/skills/<slug> --global`. If the user declines, run the phase from its Brief — the minimum viable method. State which mode you are in.
5. **In-phase decisions.** Ask every question under "Decide with the user" — with concrete options and your recommendation. Record the choice in the tracker's Key Decisions. A decision made silently is a defect.
6. **Phase exit.** Present the draft artifact content for sign-off before writing. On approval: write or extend the docs/ files, update the tracker (status, Key Decisions, Next Actions). Done when the files are written and the phase row shows `done`.
7. **Artifact discipline.** Read before writing; create a file only if missing, otherwise extend — add or update your sections, preserve everyone else's. Files are UPPERCASE in `docs/`. Every recommendation lands as a checkbox or a table row with owner and priority. See [references/artifact-templates.md](references/artifact-templates.md) when creating a docs/ file for the first time — create it from the full skeleton (all section headings), then fill the sections your phase names.
8. **Every scarcity claim, testimonial, and guarantee must be true, and referral incentives must reward real value delivered.** When a tactic needs inventing evidence, replace it with a tactic that uses evidence you have.

## Intake

Ask these before creating the tracker:

1. Current revenue, customer count, and what "lumpy" looks like month to month (baselines feed Phase 8; volume sizes the Phase 3 pipeline math).
2. Where does new business come from today, and which single channel carries most of it (reveals the empty marketing square in Phase 1; over-reliance is your risk).
3. Which segments could you focus on (feeds the Phase 1 PVP Index and the Phase 6 beachhead).
4. Current offer and price — and was pricing ever tested against willingness to pay (gates Phase 2; if never tested, add the monetizing-innovation optional phase).
5. Does the product get better as more people or teams use it — shared workspaces, referrals, a directory (gates Phase 7; skip it if there is no network dimension).
6. Existing `docs/` artifacts from a prior journey — CUSTOMER.md, POSITIONING.md, STRATEGY.md — to read and reuse (avoids re-deriving; sets extend vs create).
7. The single most painful growth constraint right now (lets you reorder — if the offer is the constraint, lead with Phase 2).

Skip heuristics: skip Phase 3 when the motion is pure self-serve and no sales-assisted motion is wanted; skip Phase 6 when you already sell to the mainstream pragmatist majority; skip Phase 7 when the product has no multiplayer or network dimension; skip Phase 9 when pricing is fixed self-serve checkout with no negotiated deals.

Then create `docs/GROW-BUSINESS-PLAN.md` from the template and confirm the plan. Done when `docs/GROW-BUSINESS-PLAN.md` exists with every phase statused and the user has confirmed the plan.

## Phases

Run the phases in order unless intake reordered them. Each phase's Invoke reads what earlier phases wrote to `docs/`; if an upstream phase was skipped, its reader falls back to the intake facts and flags the missing input rather than inventing it.

### Phase 1 — Install the marketing operating system (one-page-marketing)

**Purpose:** Lay out the whole marketing machine on one page so the missing square is visible before spending on any tactic.

**Brief (fallback):** A 3x3 grid across the customer journey — Before (target market, message, media), During (capture leads, nurture, convert), After (deliver the experience, increase lifetime value, orchestrate referrals). Marketing is a process, not an event; random tactics fail because they fill one square while eight stay empty. Score 0-10 on how completely and specifically all nine are filled. Run the PVP Index (Personal fulfillment, Value to market, Profitability) to pick one niche to dominate.

**Invoke:** `one-page-marketing` with the intake facts (revenue, customers, current channels, candidate segments). Ask for (a) all nine squares filled and scored out of 10 with the single weakest square plus three fixes, and (b) a PVP Index across the candidate segments recommending one niche and writing its avatar.

**Decide with the user:** Which niche to dominate first (the PVP winner — this becomes the Phase 6 beachhead candidate)? Which weakest square to attack first? Confirm the avatar is one named persona, not "everyone".

**Artifact:** Create docs/MARKETING.md with `## Target Market & Avatar` (PVP niche + avatar), `## Before / During / After Grid` (phase | square | current state | plan), and `## Channels`. Update the tracker.

**Done when:** MARKETING.md exists, the grid is filled and scored, the PVP niche and avatar are recorded, and the user chose the niche and the weakest square.

### Phase 2 — Make the offer impossible to refuse (hundred-million-offers)

**Purpose:** Turn the core product into a Grand Slam Offer so conversion stops being a fight before any traffic is turned on.

**Brief (fallback):** Value = (Dream Outcome x Perceived Likelihood) / (Time Delay x Effort and Sacrifice) — maximize the top, minimize the bottom. Assemble core product + named bonuses that each kill one objection + a risk-reversing guarantee + ethical (real) scarcity, until the stack dwarfs the price. Name it with MAGIC (Magnetic reason, Avatar, Goal, time Indicator, Container). Premium pricing attracts committed customers who churn less.

**Invoke:** `hundred-million-offers` with the current offer and price from intake (and docs/OFFER.md if it exists). Ask for a score out of 10, the weakest Value-Equation lever, three objection-killing bonuses with defensible dollar values, a guarantee type, and a MAGIC name.

**Decide with the user:** Is "too expensive" a price problem or a value-construction problem? Raise the price and add a done-for-you bonus, or hold? Which three bonuses ship?

**Artifact:** Create or extend docs/OFFER.md: `## Offer Stack` (element | description | honest value | objection it kills) and `## Price Metric`. Update the tracker.

**Done when:** OFFER.md holds a scored Grand Slam Offer with named bonuses, a guarantee, real scarcity, and a MAGIC name, and the pricing decision is recorded.

### Phase 3 — Manufacture pipeline with outbound (predictable-revenue)

**Purpose:** Build a sales motion you can throttle — turn up to make deals, turn down to pause — instead of waiting for luck.

**Brief (fallback):** Lead types: Seeds (referrals — highest conversion, slow to build), Nets (inbound — medium), Spears (outbound — predictable, you control volume). Most under-invest in Spears. Specialize roles: SDRs prospect, AEs close, CSMs retain — never the same person prospecting and closing. Cold Calling 2.0: email above the decision-maker for a referral in, no pitch; response runs 9-15% vs 1-3%. Qualify with ANUM (Authority, Need, Urgency, Money). Run pipeline math backward from the revenue goal.

**Invoke:** `predictable-revenue` with the revenue goal, average deal, and win rate from intake, plus the USP and niche from MARKETING.md. Ask for (a) backward pipeline math to emails and SDR count, (b) a four-touch Cold Calling 2.0 sequence, and (c) an ANUM SDR-to-AE handoff.

**Decide with the user:** Is the revenue goal reachable at current conversion, or adjust the goal or hire? Specialize roles now or stay generalist a while longer? What Seeds/Nets/Spears mix to target?

**Artifact:** Extend docs/MARKETING.md: `## Outbound Process` (roles, sequences, ANUM qualification, handoff format) with the pipeline math. Update the tracker.

**Done when:** MARKETING.md holds the pipeline math, the cold-email sequence, and the qualification-plus-handoff, and the goal, hiring, and role decisions are recorded.

### Phase 4 — Engineer word-of-mouth (contagious)

**Purpose:** Manufacture Seeds on purpose — design shareability into a feature or campaign instead of hoping referrals happen.

**Brief (fallback):** STEPPS — Social Currency (sharing makes them look good), Triggers (everyday cues that keep you top-of-mind), Emotion (high-arousal: awe, anger, excitement drive sharing; contentment suppresses it), Public (visible usage others imitate), Practical Value (useful enough to pass on), Stories (a narrative retold with the brand baked in). Only ~7% of word-of-mouth is online. Trojan Horse test: if the story survives without your brand named, it failed. Triggers and Practical Value are usually highest-leverage for an existing business.

**Invoke:** `contagious` with a candidate campaign, feature, or the quarterly customer email, plus the niche and avatar from MARKETING.md. Ask for a STEPPS audit scored out of 10 and a redesign that engineers the two weakest-but-highest-leverage drivers.

**Decide with the user:** Which asset to engineer first? Which one or two STEPPS levers to strengthen (Triggers and Practical Value usually win)?

**Artifact:** Extend docs/MARKETING.md: `## Word-of-Mouth (STEPPS)` (lever | idea | status), including the chosen Trigger and a Trojan-Horse story that passes the retell test. Update the tracker.

**Done when:** MARKETING.md holds a STEPPS table with at least one engineered Trigger and a brand-embedded story, and the user chose the asset and levers.

### Phase 5 — Build persuasion into every surface (influence-psychology)

**Purpose:** Lift conversion on the surfaces that already have traffic — pricing page, testimonials, checkout — without spending more on acquisition.

**Brief (fallback):** Seven principles layer: Reciprocity, Commitment and Consistency, Social Proof, Authority, Liking, Scarcity, Unity. Specifics matter: exact numbers beat vague ("2,347 firms" beats "thousands"), negative social proof backfires, admitting a weakness raises authority, newly-scarce beats always-scarce (loss framing). Persuasion helps people see value they would appreciate anyway; manipulation tricks them against their interest — the line the skill enforces.

**Invoke:** `influence-psychology` with the pricing page, testimonial block, or checkout flow, plus the offer from docs/OFFER.md. Ask for an audit naming which of the seven principles are present and missing, a score out of 10, rewritten weak spots, and an ethics check on every tactic.

**Decide with the user:** Which surface to fix first? Which principles to add where? Confirm every scarcity and proof claim is real — a tactic that fails the ethics check gets replaced with one using evidence you have, never faked.

**Artifact:** Extend docs/OFFER.md: under `## Offer Stack` add `### Persuasion Audit` (principle | present? | fix) and `### Proof & Social Proof` (concrete testimonials + placement where objections peak). Update the tracker.

**Done when:** OFFER.md holds a scored persuasion audit, rewritten proof placed where objections peak, and every claim verified true.

### Phase 6 — Cross the chasm to the mainstream (crossing-the-chasm)

**Purpose:** Make the jump from enthusiasts to pragmatists — target one beachhead, assemble the whole product, and reposition for "it just works."

**Brief (fallback):** Early adopters (visionaries) tolerate rough edges and buy the vision; the early majority (pragmatists) want proven solutions, references from peers, and a complete product. The D-Day strategy: dominate one narrow beachhead — urgent expensive pain, reachable channel, members who talk to each other — then expand from strength. Assemble the whole product (integrations, onboarding, migration, support), partnering for gaps. "Revolutionary" becomes "proven solution for [problem]"; "be first" becomes "join 500 firms like yours."

**Invoke:** `crossing-the-chasm` with the PVP niche from MARKETING.md as the beachhead candidate. Ask for a go-to-market score out of 10, a whole-product gap analysis, and positioning rewritten for pragmatists using Moore's formula.

**Decide with the user:** Confirm the beachhead (urgent pain, reachable channel, members who talk to each other)? Which whole-product gaps to build vs partner for? Adopt the pragmatist repositioning?

**Artifact:** Extend docs/STRATEGY.md: `## Beachhead` and `## Whole-Product Checklist` (- [ ] gap (owner, priority)); and extend docs/CUSTOMER.md: `## Segments & Best-Fit Customer` with the pragmatist beachhead. Update the tracker.

**Done when:** STRATEGY.md names the beachhead and a checklisted whole-product gap list, CUSTOMER.md records the pragmatist segment, and the build/partner and repositioning decisions are recorded.

### Phase 7 — Turn customers into a compounding network (cold-start-problem)

**Purpose:** Formalize the referral square and word-of-mouth into a self-reinforcing loop where the network does the acquiring.

**Brief (fallback):** Network effects are a liability before an asset; they grow by saturating one tiny complete network at a time, not by launching broadly. Atomic network: the smallest self-sustaining unit (one firm, one city) — over-deliver until dense, then replicate with a playbook. The hard side: the minority who do the disproportionate work and are hardest to keep — build for them first. Tipping playbook: invite-only mechanics and two-sided referral incentives import each new user along an existing relationship.

**Invoke:** `cold-start-problem` with the product's multiplayer or shared dimension and the referral square from MARKETING.md. Ask for a defined atomic network, the hard side and what retains them, and a two-sided referral/invite loop with real (never faked) incentives, scored out of 10.

**Decide with the user:** Which atomic-network unit (firm / city / practice area)? Who is the hard side and why do they stay? What real incentive does each side of the referral get?

**Artifact:** Extend docs/MARKETING.md: `## Referral & Invite Mechanics` with the atomic network, the hard side, and the two-sided loop. Update the tracker.

**Done when:** MARKETING.md holds a defined atomic network, the hard side, and a two-sided referral loop with real incentives, and density (not signup) metrics are named for Phase 8.

### Phase 8 — Point everything at the one metric that matters (lean-analytics)

**Purpose:** Cut the dashboard to the single number that says whether the riskiest part of the business is working, and let it gate every experiment.

**Brief (fallback):** A good metric is comparative, a ratio or rate (not an ever-growing total), and behavior-changing — if it will not change a decision, stop measuring it. Cumulative up-and-to-the-right charts are the vanity tell. OMTM = intersection of business model (SaaS: churn, MRR, LTV:CAC, time-to-value) and stage (Empathy, Stickiness, Virality, Revenue, Scale). Pair it with a counter-metric so it cannot be gamed; draw a line in the sand — target, date, pre-committed miss-response. Cohort and segment, because blended averages hide the truth.

**Invoke:** `lean-analytics` with the current metric list, business model, and stage. Ask for which metrics are vanity, the OMTM derived from model and stage, a counter-metric, and a one-screen dashboard (OMTM big, 4-6 supporting metrics small).

**Decide with the user:** Which stage are we in? What is the OMTM and its counter-metric? What line in the sand — target number, date, and what we do if we miss?

**Artifact:** Create or extend docs/METRICS.md: `## Stage & One Metric That Matters`, `## KPI Definitions`, `## Baselines & Targets`, `## Funnel`, and `## Cohort Notes`. Update the tracker.

**Done when:** METRICS.md names the OMTM, its counter-metric, the line in the sand, and a cohorted funnel, and vanity metrics are flagged.

### Phase 9 — Stop discounting, capture the value you create (negotiation)

**Purpose:** Hold price in high-stakes conversations so the value the engine built lands in the bank instead of being discounted away.

**Brief (fallback):** The path to yes runs through empathy and being understood, not logic or compromise — and never split the difference: no deal beats a bad deal, because a pressured discount trains every future customer to ask. Tactical empathy and labeling name the other side's concern first; calibrated questions ("how am I supposed to do that at that price?") make them solve your problem; the accusation audit preempts objections; the Ackerman method holds price in decreasing increments to precise non-round numbers, closing with a non-monetary concession.

**Invoke:** `negotiation` with a specific upcoming high-stakes conversation (a renewal at risk, a procurement squeeze, an enterprise deal). Ask for an accusation audit, five calibrated questions, an Ackerman plan (target, decreasing increments, non-monetary concession), and Black-Swan hypotheses.

**Decide with the user:** Which conversation to prepare? What is the Ackerman target and the walk-away? Which non-monetary concessions can substitute for a discount?

**Artifact:** Extend docs/OFFER.md: under `## Price Metric` add `### Price-Holding Playbook` (accusation audit, calibrated questions, Ackerman plan). Update the tracker.

**Done when:** OFFER.md holds a reusable price-holding playbook, the next negotiation is prepped, and the target, walk-away, and concession list are recorded.

## Optional Phases

| Skill | Add when | Artifact |
|---|---|---|
| monetizing-innovation | pricing was never tested against willingness to pay | Extends docs/OFFER.md |
| good-strategy-bad-strategy | growth efforts scatter because there is no kernel | Extends docs/STRATEGY.md |
| traction-eos | execution rhythm cannot keep up with growth plans | Extends docs/OPERATIONS.md |
| scorecard-marketing | lead generation needs a quiz or assessment funnel | Extends docs/MARKETING.md |
| made-to-stick | the referral message is forgettable | Extends docs/POSITIONING.md |

Optional phases follow the same operating rules; insert where the Add-when condition first becomes true.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Optimizing the funnel before fixing the offer | Run Phase 2 (`hundred-million-offers`) against pricing before touching the funnel — the offer is the bigger lever. |
| Treating the nine skills as a buffet | Keep the order; Phase 1 sets the shared target every later phase reads (PVP niche → beachhead, USP → cold email, referral square → network loop). |
| Marketing to pragmatists like early adopters | Reframe as proven evolution via Phase 6 (`crossing-the-chasm`) — "proven solution", "join 500 firms", not "revolutionary". |
| Faking scarcity, social proof, or guarantees | Use real inventory, real numbers, real deadlines; the frameworks work without the fake version (Operating Rule 8). |
| Celebrating vanity metrics | Watch the one ratio that matters — Phase 8 (`lean-analytics`) flags cumulative up-and-to-the-right charts as decoration. |
| Building outbound on a leaky bucket | Let Phase 8's stickiness metric gate acquisition spend; if retention is broken, run improve-business first. |

## Completing the Journey

Exit checklist:

- [ ] MARKETING.md: nine squares filled and scored, with the outbound process, STEPPS levers, and a two-sided referral loop
- [ ] OFFER.md: a scored Grand Slam Offer, a persuasion audit, and the price-holding playbook
- [ ] STRATEGY.md names a beachhead with a whole-product checklist; CUSTOMER.md records the pragmatist segment
- [ ] METRICS.md names the OMTM, its counter-metric, and the line in the sand
- [ ] GROW-BUSINESS-PLAN.md: every phase `done` or `skipped: reason`, with Key Decisions logged

Close the tracker: every phase `done` or `skipped: reason`, and Next Actions carried into the artifacts as owned checkboxes. Growth without retention is a leaky bucket — before pouring more pipeline in, confirm Phase 8's stickiness metric is holding. Then route forward:

- When growth stalls because the fundamentals underneath it are broken — retention, churn, operational drag — continue with `improve-business`.
- When the product itself must carry the growth loops — in-app referrals, network features, instrumentation — continue with `grow-app`.
