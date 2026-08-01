---
name: grow-app
description: 'Guided journey from an app people sign up for and then quietly abandon to a sealed retention engine with a habit loop, an activated first run, and one metric the whole team trusts. Orchestrates eight skills phase by phase - hooked-ux, improve-retention, continuous-discovery, lean-ux, inspired-product, lean-analytics, microinteractions, drive-motivation - asking the user questions at every decision point and recording results in the project docs/ folder (PRODUCT.md, METRICS.md, GROW-APP-PLAN.md) so the journey resumes across sessions. Use when the user wants to lift activation and retention, design a habit loop, fix a leaky onboarding funnel, or says ''users sign up then disappear''. Do not use to fix broken UX or performance that no engagement mechanic can paper over - run improve-app first; if there is no app yet, use create-app. For one framework in isolation, invoke that skill directly.'
license: MIT
metadata:
  author: wondelai
  version: "1.0.1"
---

# Grow an App

Your app has users who sign up and then quietly disappear — cohorts decay, daily actives are flat, the activation funnel leaks where it always has, and nothing looks obviously broken. This journey seals the bucket: it turns first-time users into activated, then habitual, then would-miss-it users across eight interactive phases. The agent asks before every decision and records the outcome in `docs/`, so the work resumes across sessions instead of restarting. Growth here is an engineering and design problem, not a bigger ad budget.

## Core Principle

**Fix the leaky bucket before pouring in acquisition: habit, activation, and retention come before any growth spend.** This skill sequences the eight phases, asks every decision question, and records each choice in `docs/`. The constituent skills carry the method — invoke them rather than improvising their frameworks.

## Journey Map

| Phase | Skill | Question it answers | Artifact |
|---|---|---|---|
| 1 | hooked-ux | Why do users come back without us paying? | Extends docs/PRODUCT.md |
| 2 | improve-retention | Why don't new users reach the loop? | Extends docs/PRODUCT.md |
| 3 | continuous-discovery | What do our own users actually need? | Extends docs/PRODUCT.md + docs/CUSTOMER.md |
| 4 | lean-ux | Which bet is worth building? | Extends docs/EXPERIMENTS.md |
| 5 | inspired-product | Is the team building the right things? | Extends docs/PRODUCT.md |
| 6 | lean-analytics | Which single number tells the truth? | Creates docs/METRICS.md — sets the Rule 8 bar |
| 7 | microinteractions | Does it feel alive in the hand? | Extends docs/DESIGN.md |
| 8 | drive-motivation | Will engagement last, or curdle? | Extends docs/PRODUCT.md |

Phases 1-2 seal the loop and the funnel; 3-5 steer with evidence; 6 is the instrument panel; 7-8 are the finish and the ethical backstop. Take the lean-analytics baseline (Phase 6) early — before the Phase 1-2 fixes land — so every change is read against a pre-change number, then keep updating it. Habit formation is slow: read Phase 1's success against the "5% rule" (a habit has formed when 5%+ of users return unprompted), not a single cohort.

## Operating Rules

1. **Resume first.** Before anything else, read `docs/GROW-APP-PLAN.md` and every artifact in the Journey Map. If the tracker exists, summarize the journey state in 3-5 lines and ask which phase to enter. Done when the user has confirmed an entry point. A journey with a tracker is resumed, never restarted.
2. **Intake on first run only.** No tracker: run the Intake below, then create `docs/GROW-APP-PLAN.md` with every phase statused `pending | in-progress | awaiting-evidence | done | deferred: reason | skipped: reason`. Done when the tracker exists and the user has confirmed the phase plan.
3. **Phase entry.** Announce: what the phase does, the decision it forces, the artifact it produces, rough effort. Offer proceed / skip / defer — phases marked GATE may be deferred, never skipped. Mark the phase `in-progress` on proceed. Done when the user chose.
4. **Skill invocation and fallback.** Invoke the phase's skill by its slug. If it is not available, offer: `npx skills add wondelai/skills/<slug> --global`. If the user declines, run the phase from its Brief — the minimum viable method. State which mode you are in.
5. **In-phase decisions.** Ask every question under "Decide with the user" — with concrete options and your recommendation. Record the choice in the tracker's Key Decisions. A decision made silently is a defect.
6. **Phase exit.** Present the draft artifact content for sign-off before writing. On approval: write or extend the docs/ files, update the tracker (status, Key Decisions, Next Actions). Done when the files are written and the phase row shows `done`.
7. **Artifact discipline.** Read before writing; create a file only if missing, otherwise extend — add or update your sections, preserve everyone else's. Files are UPPERCASE in `docs/`. Every recommendation lands as a checkbox or a table row with owner and priority. See [references/artifact-templates.md](references/artifact-templates.md) when creating a docs/ file for the first time — create it from the full skeleton (all section headings), then fill the sections your phase names.
8. **Retention before acquisition.** Acquisition-oriented phases — the optional cold-start-problem, contagious, and crossing-the-chasm, plus any paid-growth work — stay locked while activation and retention sit below the bar set at intake; unlock them only once the cohort curve clears that bar. Every habit loop and reward must pass the Manipulation Matrix: build only what the maker would use and honestly believes materially improves users. When a tactic needs manufactured anxiety or loss aversion, replace it with one built on real value.

## Intake

Run only on first start (no tracker). Ask:

1. What does the app do, and what core action does a retained user repeat? (defines the Hook loop and the OMTM)
2. What are the current retention numbers — day-1/7/30 or week-4 cohorts? (sets the Rule 8 acquisition bar; feeds lean-analytics)
3. Where does the activation funnel leak, and what is the first-run flow? (gates improve-retention)
4. Solo/small team or a full product trio (PM, designer, engineer)? (scales continuous-discovery and inspired-product)
5. Is the app a network/marketplace product, and do engaged users fail to convert to revenue? (flags optional cold-start-problem / monetizing-innovation)
6. What analytics and instrumentation exist today? (gates lean-analytics and every experiment)
7. Is retention broken by UX or performance rather than missing engagement? (if yes, route to improve-app first)

Skip heuristics: skip Phase 5 for a solo founder with no team to realign; defer Phase 7 until the loop and activation clear their bars; run Phase 3's cadence degraded if no user access exists yet. Then create the tracker from references/artifact-templates.md with every phase statused, and confirm the plan.

Done when `docs/GROW-APP-PLAN.md` exists with every phase statused and the user has confirmed the plan.

## Phases

### Phase 1 — Design the habit loop that brings users back (hooked-ux)

**Purpose:** Build the engine of return — a Hook loop strong enough that users come back on an internal trigger, not a paid notification.

**Brief (fallback):** The Hook Model runs Trigger → Action → Variable Reward → Investment. Migrate external triggers (push, email) to internal ones (an emotion — boredom, FOMO, anxiety). Make the action trivially simple. Make the reward variable across tribe/hunt/self. Sequence investment *after* the reward so it raises switching cost and loads the next trigger. A loop with one weak phase stalls, not half-works.

**Invoke:** `hooked-ux` with the core loop and how daily-active users return today. Ask it to (a) map the loop across all four phases, rate each 0-10, and name the weakest, and (b) design honest variable-reward concepts powered by data you already have, each checked against the Manipulation Matrix.

**Decide with the user:**
- Which internal trigger (emotion) should pull users back — confirm one.
- Which single phase is weakest and gets the highest-leverage fix now — or defer if the loop is already forming (5%+ unprompted return).
- Which reward type to strengthen — tribe (social), hunt (resources), or self (mastery) — rejecting any concept that fails the Manipulation Matrix.

**Artifact:** Extend docs/PRODUCT.md `## Hook Model` (trigger → action → variable reward → investment; weakest phase named). Update the tracker.

**Done when:** PRODUCT.md names the internal trigger and all four phases, the weakest phase and its fix are recorded, onboarding is re-engineered so a new user completes one full Hook cycle in the first session, and the user picked the fix to ship.

### Phase 2 — Fix activation by making the first action almost effortless (improve-retention)

**Purpose:** Get new users to the loop by making the first meaningful action almost effortless.

**Brief (fallback):** B=MAP — behavior fires only when Motivation, Ability, and a Prompt converge. Motivation is unreliable; raise Ability instead. Simplicity is capped by the *scarcest* of six resources: time, money, physical effort, mental effort, social deviance, non-routineness. Shrink the target to a Starter Step that delivers value in under 30s, anchor it to an existing routine, and celebrate the win immediately.

**Invoke:** `improve-retention` with the real activation flow step by step and the day-1/7/30 drop-offs. Ask for a B=MAP friction audit rating all six Ability-Chain factors, the scarcest resource named, a Starter Step redesign, and event-based prompt rules.

**Decide with the user:**
- Which is the scarcest Ability resource for the first action — fix that link first, not the obvious one.
- The Starter Step (tiniest valuable action) and its celebration moment.
- Which time-based prompts convert to event-based, dropping any that fail "would I appreciate this now?".

**Artifact:** Extend docs/PRODUCT.md `## Activation & Retention Plan` (friction/moment | fix | owner | status). Update the tracker.

**Done when:** the scarcest resource is named, the Starter Step, celebration, and prompt changes are rows with owners, each day-1/7/30 drop-off is mapped to its likely B=MAP failure, and the user approved the fix list.

### Phase 3 — Run continuous discovery so you stop guessing (continuous-discovery)

**Purpose:** Replace generic best-practice with a weekly stream of evidence about your own users.

**Brief (fallback):** Aim for at least one customer touchpoint per week. Build an Opportunity Solution Tree: outcome at the top → customer opportunities (needs/pains in the customer's words) → candidate solutions/experiments. Never leap outcome→solution. Interviews are story-based ("tell me about the last time you…"), captured as one-page snapshots. Test the riskiest leap-of-faith assumption first, cheaply.

**Invoke:** `continuous-discovery` with the retention outcome and known churn patterns. Ask for an Opportunity Solution Tree, a current-state experience map of how churned users try to succeed today, a weekly story-based interview snapshot template, and an assumption map for the next planned feature.

**Decide with the user:**
- The single outcome at the top of the tree.
- Which two or three opportunities to pursue first.
- The weekly cadence and recruitment mechanism the team can actually sustain — set it now or run degraded.
- The riskiest leap-of-faith assumption inside the next feature (desirability, viability, feasibility, usability) and the cheapest test for it.

**Artifact:** Extend docs/PRODUCT.md `## Opportunity Solution Tree Notes`, `## Outcome Roadmap` (outcome/problem | job served | priority | status), and `## Discovery Cadence`; extend docs/CUSTOMER.md `## Interview Evidence` (date | who | facts | commitment). Update the tracker.

**Done when:** the tree's outcome and top opportunities are recorded, the cadence is scheduled, the first interview snapshot template exists, and the riskiest assumption has a cheap test designed.

### Phase 4 — Replace debate with cheap experiments (lean-ux)

**Purpose:** Turn opportunities into falsifiable bets settled by behavior, not meetings.

**Brief (fallback):** Outcomes over outputs — value is the behavior change, not the deliverable. Write a hypothesis: "We believe [outcome] will happen if [persona] achieves [action] with [feature]," with the metric and threshold committed *before* the test. Match fidelity to risk (a paper prototype with five users finds ~85% of usability issues); reserve A/B tests for tuning a proven concept. When invalidated, remove from the backlog — don't defer.

**Invoke:** `lean-ux` with the biggest current design debate or a top discovery opportunity. Ask for three hypothesis statements in the standard format, the lowest-fidelity experiment that could validate the top one, and its pre-committed metric, threshold, and timebox.

**Decide with the user:**
- Which hypothesis to test first.
- The experiment fidelity — the lowest that answers the actual question.
- The pass/fail line and what leaves the backlog if it fails.

**Artifact:** Extend docs/EXPERIMENTS.md `## Experiment Cards` (hypothesis, type, primary metric + threshold, guardrail, decision rule) and `## Experiment Backlog` (idea | ICE | status). Update the tracker.

**Done when:** at least one experiment card has a pre-committed threshold and decision rule, the backlog is triaged, and the user chose the first test.

### Phase 5 — Build the right things with an empowered team (inspired-product)

**Purpose:** Move the team from feature factory to outcome ownership — problems to solve, not features to ship.

**Brief (fallback):** Empowered teams get problems, not backlogs, and answer for outcomes. Dual-track: discovery (what's worth building — addressing value, usability, feasibility, viability) runs continuously alongside delivery. Expect 10-20 discovery iterations per shipped feature. Give the team a product vision and an outcome-based roadmap so it can decide autonomously.

**Invoke:** `inspired-product` with the top three backlog requests and the current roadmap. Ask for an opportunity assessment of each (objective, target user, problem, success measure, alternatives) and a one-paragraph vision plus a quarter of outcome-based roadmap items.

**Decide with the user:**
- Which backlog request has the strongest evidence — and which to kill before it reaches a sprint.
- The one-paragraph product vision.
- Whether the roadmap is reframed as problems + key results rather than dated features.

**Artifact:** Extend docs/PRODUCT.md `## Vision` and `## Outcome Roadmap` (outcome/problem | job served | priority | status). Update the tracker.

**Done when:** the vision paragraph exists, each of the three requests has a build/kill verdict, and the roadmap rows are outcomes, not features.

### Phase 6 — Measure the one number that actually matters (lean-analytics)

**Purpose:** Point the whole team at the One Metric That Matters and expose the vanity metrics hiding the decay.

**Brief (fallback):** A good metric is comparative, a ratio/rate (not a cumulative total), and behavior-changing. Business model dictates which metrics matter; stage dictates sequencing (Empathy → Stickiness → Virality → Revenue → Scale). Weak retention = Stickiness stage, so retention is the OMTM — working a later stage first is the canonical mistake. Draw a line in the sand (target, date, miss response), pair the OMTM with a counter-metric, and cohort the data.

**Invoke:** `lean-analytics` with the current dashboard/metrics and the business model. Ask it to flag vanity metrics, pick the Stickiness-stage OMTM plus a counter-metric, design a one-screen dashboard (OMTM big, ≤6 supporting), and a cohorted retention view.

**Decide with the user:**
- The OMTM and its counter-metric.
- The line in the sand — target, date, pre-committed miss response.
- Which current metrics are retired as vanity.

**Artifact:** Create docs/METRICS.md with `## Stage & One Metric That Matters`, `## KPI Definitions`, `## Baselines & Targets`, `## Funnel`, and `## Cohort Notes`. Update the tracker.

**Done when:** METRICS.md names the OMTM + counter-metric, records the line in the sand with a date, lists cohorted baselines, the vanity metrics are marked retired, the one-screen dashboard is specified, and the retention bar for the Rule 8 acquisition gate is set.

### Phase 7 — Polish the micro-moments that make it feel alive (microinteractions)

**Purpose:** Close the gap between an app people tolerate and one they love, in the moments they touch daily.

**Brief (fallback):** Every microinteraction has Trigger → Rules → Feedback → Loops & Modes. Feedback is immediate (<100ms for direct manipulation) and proportionate; animate the element the user touched over a separate toast. Map every state: empty, loading, partial, error, disabled, double-tap. Invest in one or two signature moments that pass the removal test; use long loops to retire hints for power users.

**Invoke:** `microinteractions` with the five most-used interactions. Ask for a Trigger/Rules/Feedback/Loops audit of each, the sub-100ms feedback and missing edge-case states, and one signature moment implemented in real code.

**Decide with the user:**
- Which five interactions to audit.
- Which one becomes the signature moment (removal test applied).
- Which edge-case states to implement first.

**Artifact:** Extend docs/DESIGN.md `## Microinteraction Inventory` (interaction | trigger/rules/feedback/loops | fix | status). Update the tracker.

**Done when:** the five interactions are in the inventory with their missing states and fixes, the signature moment is chosen, and each fix has a status.

### Phase 8 — Sustain engagement with intrinsic motivation (drive-motivation)

**Purpose:** Keep the loops from curdling — engagement that runs on Autonomy, Mastery, and Purpose instead of exploitation.

**Brief (fallback):** For any task needing cognitive effort, "if-then" rewards crush intrinsic motivation. Lasting engagement is Autonomy (choice over what/when/how/with whom), Mastery (visible progress, flow-calibrated challenge), and Purpose (why it matters). Autonomy killers: forced tutorials, unskippable steps, mandatory notifications. Reserve rewards for meaningful milestones; prefer "now-that" recognition over "if-then" bargains.

**Invoke:** `drive-motivation` with the app's gamification, streaks, points, and notification patterns. Ask for an AMP audit rated 0-10, every autonomy violation flagged, the point at which streaks tipped into loss aversion, and a progression redesign around real mastery and purpose.

**Decide with the user:**
- Which autonomy violations to remove (forced/unskippable steps).
- Which "if-then" rewards convert to "now-that" recognition.
- Whether any streak/points mechanic exploits loss aversion and must change.

**Artifact:** Extend docs/PRODUCT.md `## Activation & Retention Plan` with AMP-audit rows (violation/finding | fix | owner | status). Update the tracker.

**Done when:** the AMP score and every autonomy violation are recorded, the reward/streak fixes are rows with owners, and the loops pass the Manipulation Matrix from Rule 8.

## Optional Phases

| Skill | Add when | Artifact |
|---|---|---|
| cold-start-problem | the app is a network or marketplace product | Extends docs/PRODUCT.md |
| monetizing-innovation | engaged users do not translate into revenue | Extends docs/OFFER.md |
| contagious | users love the app but never mention it | Extends docs/MARKETING.md |
| crossing-the-chasm | growth stalls at the early-adopter boundary | Extends docs/STRATEGY.md |
| jobs-to-be-done | usage patterns say the app is hired for a different job | Extends docs/CUSTOMER.md |

Optional phases follow the same operating rules; insert where the Add-when condition first becomes true. The acquisition-leaning ones — cold-start-problem, contagious, crossing-the-chasm — stay locked behind Rule 8 until retention clears the bar.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Buying growth before fixing retention | Pass the Stickiness gate (a flattening cohort curve) before any acquisition spend; keep acquisition phases locked per Rule 8. |
| Relying on external triggers forever | Migrate to an internal trigger via hooked-ux; treat notifications as scaffolding, not the load-bearing wall. |
| Optimizing the wrong Ability-Chain link | Rate all six factors in improve-retention and fix the scarcest resource, not the most obvious one. |
| Jumping from outcome straight to solution | Build the Opportunity Solution Tree in continuous-discovery first; the obvious feature is often the worst of five. |
| Measuring outputs, not outcomes | Instrument every release; in lean-ux and inspired-product, success is a change in user behavior, not stories shipped. |
| Gamifying with points for everything | Reserve rewards for meaningful milestones and run the drive-motivation AMP audit; "if-then" rewards crowd out your power users. |

## Completing the Journey

- [ ] PRODUCT.md holds a Hook loop with the weakest phase fixed, an activation Starter Step, a living Opportunity Solution Tree, and an AMP-clean engagement design.
- [ ] METRICS.md names the Stickiness-stage OMTM plus a counter-metric with a line in the sand (target, date, miss response).
- [ ] At least one lean-ux experiment has resolved with a recorded verdict, and invalidated ideas are out of the backlog.
- [ ] The retention bar set at intake is met — or the remaining gap is quantified — before any acquisition phase runs.

Close the tracker: every phase `done` or `skipped`, with Next Actions carried into PRODUCT.md, METRICS.md, and EXPERIMENTS.md. Then route forward:

- When engagement mechanics cannot fix a product held back by broken UX or performance, continue with `improve-app`.
- When the app is sticking and the business around it must keep pace — revenue, channels, operations — continue with `grow-business`.
