---
name: improve-business
description: 'Guided journey from a stalled, plateaued business to one with an honest diagnosis, a working operating rhythm, and offers repriced to real value. Orchestrates eight skills phase by phase - good-strategy-bad-strategy, traction-eos, high-output-management, team-topologies, drive-motivation, lean-analytics, negotiation, monetizing-innovation - asking the user questions at every decision point and recording results in the project docs/ folder (STRATEGY.md, OPERATIONS.md, METRICS.md, IMPROVE-BUSINESS-PLAN.md) so the journey resumes across sessions. Use when the user wants to fix a business that has plateaued, diagnose why growth stalled, tighten strategy and execution, re-motivate a team, or says ''revenue is flat and I do not know why''. Starting from scratch with no customers: use create-business. Once the fundamentals work and the goal is expansion: use grow-business. When the product itself drags the business down: use improve-app. For one framework in isolation, invoke that skill directly.'
license: MIT
metadata:
  author: wondelai
  version: "1.0.0"
---

# Improve a Business

An interactive, resumable journey for a business that already runs but has stopped moving — real revenue, real customers, a flat line. Across eight phases it works the layers in order (strategy, execution, management, structure, motivation, metrics, margin, pricing), diagnosing before treating rather than chasing one tactic at a time. The agent asks before every decision and records each choice in `docs/` so the turnaround survives across sessions.

## Core Principle

**A plateau is a diagnosis failure: diagnose before treating, and work the layers in order — strategy, execution, management, structure, motivation, metrics, margin, pricing.** Poking one tactic at a time never breaks a plateau because the constraints compound. This skill sequences the phases, asks the decision questions, and records what was decided; the constituent skills carry the actual method — invoke them rather than improvising their frameworks.

## Journey Map

| Phase | Skill | Question it answers | Artifact |
|---|---|---|---|
| 1 | good-strategy-bad-strategy | What single challenge is capping the business? | Creates docs/STRATEGY.md — GATE |
| 2 | traction-eos | How do we execute the strategy every week? | Creates docs/OPERATIONS.md |
| 3 | high-output-management | How does the operator multiply the team, not bottleneck it? | Extends docs/OPERATIONS.md |
| 4 | team-topologies | Is the org structure itself the constraint? | Extends docs/OPERATIONS.md |
| 5 | drive-motivation | Why has the team quietly checked out? | Extends docs/OPERATIONS.md |
| 6 | lean-analytics | Which one number tells us the truth? | Creates docs/METRICS.md |
| 7 | negotiation | Where are we leaking margin, and what do customers truly value? | Extends docs/CUSTOMER.md |
| 8 | monetizing-innovation | Are we charging for the value we deliver? | Extends docs/OFFER.md |

## Operating Rules

1. **Resume first.** Before anything else, read `docs/IMPROVE-BUSINESS-PLAN.md` and every artifact in the Journey Map. If the tracker exists, summarize the journey state in 3-5 lines and ask which phase to enter. Done when the user has confirmed an entry point. A journey with a tracker is resumed, never restarted.
2. **Intake on first run only.** No tracker: run the Intake below, then create `docs/IMPROVE-BUSINESS-PLAN.md` with every phase statused `pending | in-progress | awaiting-evidence | done | deferred: reason | skipped: reason`. Done when the tracker exists and the user has confirmed the phase plan.
3. **Phase entry.** Announce: what the phase does, the decision it forces, the artifact it produces, rough effort. Offer proceed / skip / defer — phases marked GATE may be deferred, never skipped. Mark the phase `in-progress` on proceed. Done when the user chose.
4. **Skill invocation and fallback.** Invoke the phase's skill by its slug. If it is not available, offer: `npx skills add wondelai/skills/<slug> --global`. If the user declines, run the phase from its Brief — the minimum viable method. State which mode you are in.
5. **In-phase decisions.** Ask every question under "Decide with the user" — with concrete options and your recommendation. Record the choice in the tracker's Key Decisions. A decision made silently is a defect.
6. **Phase exit.** Present the draft artifact content for sign-off before writing. On approval: write or extend the docs/ files, update the tracker (status, Key Decisions, Next Actions). Done when the files are written and the phase row shows `done`.
7. **Artifact discipline.** Read before writing; create a file only if missing, otherwise extend — add or update your sections, preserve everyone else's. Files are UPPERCASE in `docs/`. Every recommendation lands as a checkbox or a table row with owner and priority. See [references/artifact-templates.md](references/artifact-templates.md) when creating a docs/ file for the first time — create it from the full skeleton (all section headings), then fill the sections your phase names.
8. **Diagnosis before treatment.** No new initiative, reorg, or pricing change starts before `docs/STRATEGY.md` holds a written Diagnosis the user has confirmed. When asked to jump straight to Phase 4, 7, or 8, complete Phase 1 first (or confirm it is already done and recorded). Done when a confirmed Diagnosis exists before any treatment phase writes its artifact.

## Intake

Ask these before creating the tracker:

1. What is the plateau — flat revenue, rising churn, a team working hard with nothing moving? (Frames the Phase 1 diagnosis and the Phase 6 OMTM.)
2. What passes for your current strategy today — a deck, OKRs, a goal list, nothing written? (Feeds Phase 1; if none exists the diagnosis work is larger.)
3. How big is the team and how is it structured? (Sizes the Rocks and 1:1 system in Phases 2-3; gates Phase 4.)
4. Do you run technology teams, or is this a services / brick-and-mortar business? (`team-topologies` is engineering-specific — skip Phase 4 for non-tech orgs.)
5. When was pricing last set, and on what basis — cost-plus, competitor, or value? (Gates Phase 8; cost/competitor pricing signals margin left on the table.)
6. What is your sales win rate, and do you hear price objections? (Near-100% win rate with no pushback signals minivation — Phase 8.)
7. Where does work get stuck — within teams or between them? (Between-team stalls point at Phase 4; within-team points at Phases 3 and 5.)

Phase-skip heuristics: skip Phase 4 when you don't run technology teams or teams already deliver cleanly; skip Phase 5 when morale is engaged and not the constraint; skip Phase 7 when no large renewals or vendor contracts are in play; skip Phase 8 only if pricing was recently repriced from validated willingness to pay.

Then create `docs/IMPROVE-BUSINESS-PLAN.md` from the template and confirm the phase plan. Done when `docs/IMPROVE-BUSINESS-PLAN.md` exists with every phase statused and the user has confirmed the plan.

## Phases

### Phase 1 — Diagnose the real challenge (good-strategy-bad-strategy) — GATE

**Purpose:** Name the single critical challenge capping the business, so every later layer works the right constraint. Phases 2-8 may not start before this Diagnosis is confirmed.

**Brief (fallback):** Good strategy has a kernel — an honest diagnosis of the critical challenge, a
guiding policy, and coherent actions. Bad strategy is fluff, goals dressed as strategy, and forty
"priorities" that concentrate nothing. Treat the funnel as a chain-link system and find the one
binding link; investing in strong links is wasted until the weak one is fixed. Set a proximate
objective close enough that the team can see how to hit it, and force a no-list.

**Invoke:** `good-strategy-bad-strategy` with the current annual plan, OKRs, or deck pasted in. Ask
it to (a) audit the plan as strategy and score it 0-10, (b) write a proper kernel, (c) name the
binding chain-link constraint and one proximate objective for the quarter.

**Decide with the user:** Does the diagnosis name the real obstacle, not a symptom? Which single link (lead-gen / activation / retention / expansion) is the binding constraint, and what is the proximate objective? What goes on the no-list — what will you deliberately stop doing?

**Artifact:** Create docs/STRATEGY.md with `## Diagnosis` (critical challenge + binding constraint), `## Guiding Policy` (including the proximate objective), `## Coherent Actions` (Action | Owner | Due | Status), and `## No-List`. Update the tracker.

**Done when:** STRATEGY.md holds a confirmed Diagnosis, a Guiding Policy, 3-5 Coherent Actions with owners, and a No-List — only then are Phases 2-8 unlocked.

### Phase 2 — Install an execution rhythm (traction-eos)

**Purpose:** Convert the strategy into a weekly operating rhythm that survives Monday.

**Brief (fallback):** Vision without traction is hallucination. Set 3-7 quarterly Rocks — each with
one owner, SMART, binary (done or not, no partial credit) — aimed at the proximate objective.
Install the Level 10 Meeting: same day and time, 90 minutes, fixed agenda ending in 60 minutes of
IDS (Identify, Discuss, Solve) driven to root cause. Never cancel it.

**Invoke:** `traction-eos` with STRATEGY.md's guiding policy and proximate objective. Ask for (a)
5-7 quarterly Rocks with owners and binary criteria, flagging any that are business-as-usual, (b) a
Level 10 agenda with time boxes, (c) an IDS pass on the top recurring issue.

**Decide with the user:** Which 5-7 Rocks make the quarter (cap at seven)? Who owns each? What weekly cadence for the Level 10, and who facilitates?

**Artifact:** Create docs/OPERATIONS.md with `## Vision/Traction Summary`, `## Rocks (this quarter)` (Rock | Owner | Binary done-condition | Status), and `## Meeting Cadence` (Meeting | Rhythm | Agenda). Update the tracker.

**Done when:** OPERATIONS.md holds 5-7 owned binary Rocks tied to the proximate objective and a scheduled Level 10 cadence the user has committed to.

### Phase 3 — Manage for output, not activity (high-output-management)

**Purpose:** Multiply the team's output by getting the operator off the critical path.

**Brief (fallback):** A manager's output equals the output of their organization plus the
neighboring teams they influence. Negative-leverage habits — meddling, waffling, being the approval
bottleneck — multiply downward. High-leverage tools: subordinate-owned 1:1s at a cadence set by
task-relevant maturity (TRM), and delegation-with-monitoring — delegate what you know best, monitor
at task level, sample deeper when TRM is low, lighter as it rises.

**Invoke:** `high-output-management` with the operator's last two weeks of calendar and the tasks
they keep grabbing back. Ask for a leverage audit, a redesigned week built around forecasted key
events, and a 1:1 plus delegation system for direct reports.

**Decide with the user:** Which negative-leverage habits to cut? The 1:1 cadence per report (set by TRM, not seniority)? Which tasks to delegate-with-monitoring off the critical path?

**Artifact:** Extend docs/OPERATIONS.md: add `## Management Leverage` (1:1 cadence per report, delegation decisions, monitoring depth). Update the tracker.

**Done when:** OPERATIONS.md records a 1:1 cadence for every direct report and at least one delegation decision that removes the operator as a bottleneck.

### Phase 4 — Reshape teams around value streams (team-topologies)

**Purpose:** Remove structural friction when work keeps getting stuck between teams rather than within them.

**Brief (fallback):** Conway's law — you ship your communication structure. Reduce every team to one
of four types: stream-aligned (the default), enabling, complicated-subsystem, platform. Cap
cognitive load: at most one complicated domain per team; never split a single domain across two
teams. Shed domains or remove extraneous load before adding headcount. Define each interaction mode:
collaboration, X-as-a-service, or facilitating.

**Invoke:** `team-topologies` with each current team and what it does day to day. Ask it to classify
teams, flag anti-patterns (shared-services ticket queue, teams split by function not value stream),
diagnose cognitive load, and propose value-stream-aligned boundaries with explicit interaction
modes.

**Decide with the user:** First — is the plateau structural (handoffs dominate lead time, recurring coordination meetings, everyone's-and-no-one's ownership)? If not, skip. If yes: which domains to shed, which extraneous load to platform-ize.

**Artifact:** Extend docs/OPERATIONS.md: add `## Team Structure` (team topology, per-team type, cognitive-load notes, interaction modes). Update the tracker.

**Done when:** either the phase is skipped with a recorded reason, or OPERATIONS.md holds a four-type classification and a proposed value-stream structure with interaction modes.

### Phase 5 — Re-motivate the people who checked out (drive-motivation)

**Purpose:** Rebuild intrinsic motivation instead of throwing money at disengagement.

**Brief (fallback):** For any task needing cognitive effort, if-then rewards degrade performance —
they crowd out intrinsic motivation, narrow focus, foster short-term thinking. What sustains it is
Autonomy (task, time, technique, team), Mastery (visible progress at a challenge between boredom and
anxiety), and Purpose (serving something larger than the quarter). Pay enough to take money off the
table, then stop using it as the lever; replace if-then bonuses with now-that recognition.

**Invoke:** `drive-motivation` with how incentives, reviews, and goals currently run. Ask for an AMP
audit scored 0-10, the places controlling if-then rewards crowd out motivation, and specific
autonomy / mastery / purpose fixes including a shift to now-that recognition.

**Decide with the user:** Which if-then rewards to retire? Which autonomy levers (the four T's) to grant? How to convert recognition from if-then to now-that?

**Artifact:** Extend docs/OPERATIONS.md: add `## Motivation (Autonomy / Mastery / Purpose)` (Lever | Finding | Fix). Update the tracker.

**Done when:** OPERATIONS.md holds an AMP audit with at least one concrete fix per pillar, and the decision on if-then versus now-that rewards is recorded.

### Phase 6 — Measure the one number that tells the truth (lean-analytics)

**Purpose:** Replace a dashboard of vanity metrics with one honest number tied to the riskiest assumption.

**Brief (fallback):** Good metrics are comparative, understandable, ratios or rates (not
ever-growing totals), and behavior-changing — if a number won't change what you do next, stop
watching it. The cumulative up-and-to-the-right chart is the top vanity tell. Pick one OMTM for the
riskiest part of the business right now, guard it with a counter-metric so it can't be gamed, and
draw a line in the sand: a target, a date, and a pre-committed miss response decided before results
arrive.

**Invoke:** `lean-analytics` with the current dashboard and the business model and stage. Ask it to
purge vanity metrics into actionable ratios, name the OMTM plus counter-metric, and build cohort
retention tables to test the stickiness gate.

**Decide with the user:** What business model and stage are we in? Which single OMTM and counter-metric? The line in the sand — target, date, and pre-committed action if we miss?

**Artifact:** Create docs/METRICS.md with `## Stage & One Metric That Matters`, `## KPI Definitions` (Metric | Definition | Actionable ratio? | Owner), `## Baselines & Targets` (including the line in the sand), `## Funnel`, and `## Cohort Notes`. Update the tracker.

**Done when:** METRICS.md names one OMTM with a counter-metric and a line in the sand, and the vanity metrics are rewritten as actionable ratios.

### Phase 7 — Stop leaking margin in negotiations (negotiation)

**Purpose:** Protect price in renewals and vendor contracts, and capture what customers truly value.

**Brief (fallback):** The path to a good deal runs through making the other side feel understood; no
deal beats a bad deal. Tools: the accusation audit (preemptively voice their objections), calibrated
questions ("how am I supposed to do that?"), labeling ("it sounds like…"), and the Ackerman plan
(decreasing increments ending on a precise non-round number plus a non-monetary sweetener). Hunt the
Black Swans — secret constraints, hidden motivations, unknown context — behind any competing bid; it
is rarely the real story.

**Invoke:** `negotiation` with the specific renewal or vendor contract (numbers, the threat, your
instinct). Ask for an accusation audit, five calibrated questions to surface the Black Swan, and an
Ackerman plan with a non-monetary concession — never concede without getting something back.

**Decide with the user:** For each big negotiation: the target and walk-away, the concessions you will trade (never for free), and the real driver (Black Swan) behind the price threat.

**Artifact:** Extend docs/CUSTOMER.md: add to `## Competing Alternatives` (the competing bids customers cite and their real weaknesses) and `## Interview Evidence` (concrete facts and Black Swans surfaced in the renewal — what the customer actually values). Update the tracker.

**Done when:** the negotiation is prepped with an accusation audit, calibrated questions, and an Ackerman plan, and CUSTOMER.md records the real drivers surfaced.

### Phase 8 — Reprice around delivered value (monetizing-innovation)

**Purpose:** Recover margin by repricing from validated willingness to pay, not cost or competitors.

**Brief (fallback):** Price is a diagnostic of value. Name the monetization failure: feature shock,
minivation (right product priced too timidly — signature: near-100% win rate, no price pushback),
hidden gem, or undead. Segment by willingness to pay, not demographics. Class every feature leader /
filler / killer; never give the leader away in the cheapest tier or bundle a killer that makes
buyers reject the package. Validate with acceptable / expensive / prohibitive probes before shipping
any change.

**Invoke:** `monetizing-innovation` with current pricing, tiers, win rates, and deal data, plus the
WTP signals from Phase 7. Ask it to diagnose the monetization failure, run leader-filler-killer on
the tiers, and design a WTP conversation to run before any price change ships.

**Decide with the user:** Which monetization failure fits the evidence? The tier restructure (which tier you actually want to sell, the premium anchor)? Whether to run WTP conversations before repricing.

**Artifact:** Extend docs/OFFER.md: add `## Offer Stack`, `## Willingness-to-Pay Evidence` (Segment | Acceptable | Expensive | Prohibitive | Source), `## Leader / Filler / Killer Features`, `## Tiers (Good / Better / Best)`, and `## Price Metric`. Update the tracker.

**Done when:** OFFER.md names the monetization failure, a leader-filler-killer classification, and a repriced tier structure backed by WTP evidence (or a scheduled WTP conversation).

## Optional Phases

| Skill | Add when | Artifact |
|---|---|---|
| blue-ocean-strategy | the market is commoditized and competition is on price | Extends docs/STRATEGY.md (`## Strategy Canvas & ERRC Grid`) |
| hundred-million-offers | the offer itself is weak, not just the pricing | Extends docs/OFFER.md (`## Offer Stack`) |
| jobs-to-be-done | customers churn and nobody knows which job the product lost | Extends docs/CUSTOMER.md (`## Job Statement`, `## Job Dimensions`) |
| obviously-awesome | the market misunderstands what the business is | Extends docs/POSITIONING.md |
| 37signals-way | the org overplans and underships | Extends docs/OPERATIONS.md |

Optional phases follow the same operating rules; insert where the Add-when condition first becomes true.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Jumping to tactics before the diagnosis | Complete Phase 1 first — the chain-link constraint tells you which single link to work; effort on strong links is wasted. |
| Treating the strategy offsite as the finish line | Install the Level 10 cadence (Phase 2) and never cancel it — the weekly rhythm is what changes behavior. |
| Confusing being busy with creating output | Apply Grove's equation (Phase 3): delegate what you know best, monitor by TRM, and get off the critical path. |
| Reorganizing when the problem isn't structure | Run Phase 4 only when handoffs dominate lead time; if teams already deliver cleanly, skip it. |
| Throwing money at disengagement | Pay fairly, then rebuild autonomy, mastery, and purpose (Phase 5); replace if-then bonuses with now-that recognition. |
| Repricing from cost or competitors, not value | A high win rate with no price pushback signals undercharging — reprice from validated WTP and segment by it (Phase 8). |

## Completing the Journey

Exit checklist:

- [ ] docs/STRATEGY.md holds a confirmed Diagnosis, Guiding Policy, Coherent Actions, and No-List
- [ ] docs/OPERATIONS.md holds owned Rocks, a Level 10 cadence, management leverage, and (where structural) team structure and motivation fixes
- [ ] docs/METRICS.md names one OMTM, a counter-metric, and a line in the sand
- [ ] docs/OFFER.md is repriced from validated WTP, and docs/CUSTOMER.md records the real drivers surfaced in renewals

Close the tracker: every phase `done` or `skipped: reason`, and carry each open Next Action into the relevant artifact as a checkbox or table row with an owner. Then route forward:

- When the fundamentals work again and the goal shifts to expansion, continue with `grow-business`.
- When the product itself is what drags the business down, continue with `improve-app`.
