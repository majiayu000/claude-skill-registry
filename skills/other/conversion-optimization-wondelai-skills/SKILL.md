---
name: conversion-optimization
description: 'Guided journey from a leaking conversion flow - landing page, signup, checkout, or in-app onboarding - to a measured, tested funnel. Orchestrates six skills phase by phase - lean-analytics, cro-methodology, storybrand-messaging, hundred-million-offers, influence-psychology, design-everyday-things - each phase carries its full method inline so it runs standalone, asking the user questions at every decision point and recording results in the project docs/ folder (FUNNEL.md, METRICS.md, EXPERIMENTS.md, CONVERSION-OPTIMIZATION-PLAN.md) so the journey resumes across sessions. Use when the user wants to raise conversion on a specific flow, fix checkout or signup abandonment, diagnose onboarding drop-off, or says ''people start but never finish''. With no site yet, use create-website; for a whole-site look, message, and speed audit, improve-website; if the flow converts but needs traffic, grow-website; for in-product engagement and retention, improve-app. For one framework in isolation, invoke that skill directly.'
license: MIT
metadata:
  author: wondelai
  version: "1.0.0"
---

# Conversion Optimization

Turn one leaking conversion flow — a landing page, a signup, a checkout, an in-app onboarding — into a
measured, tested funnel. This is an interactive, resumable journey of seven phases: the agent asks
before every decision and records the outcome in your project's `docs/` folder, so you can stop after
any phase and pick up later. It works on websites and inside products alike; the unit of work is the
flow and its ONE action, not the whole site.

## Core Principle

**Find the leak with numbers, learn the reason from customers, fix message → offer → proof → friction
in that order, and prove every fix with a pre-committed test.** The order is causal: a number tells
you *where*, only research tells you *why*, motivation must be raised before friction-cutting pays,
and an untested fix is a guess that compounds. This skill sequences the phases, asks the decision
questions, and records every choice in `docs/`. The constituent skills carry the method — invoke them
rather than improvising their frameworks.

## Journey Map

| Phase | Skill | Question it answers | Artifact |
|---|---|---|---|
| 1 | lean-analytics | Where does the flow actually leak, and what is the one metric? | Extends docs/METRICS.md — GATE |
| 2 | cro-methodology | Why do people drop at the leak — which objections and friction? | Creates docs/FUNNEL.md; extends docs/EXPERIMENTS.md — GATE |
| 3 | storybrand-messaging | Does the leaking step promise the visitor's own desired outcome in five seconds? | Extends docs/POSITIONING.md + docs/FUNNEL.md + docs/EXPERIMENTS.md |
| 4 | hundred-million-offers | Is the offer at the conversion point worth acting on now? | Extends docs/OFFER.md + docs/EXPERIMENTS.md |
| 5 | influence-psychology | Is there honest proof at every point of doubt? | Extends docs/FUNNEL.md + docs/EXPERIMENTS.md |
| 6 | design-everyday-things | Can a visitor who decided to act complete the flow without stumbling? | Extends docs/FUNNEL.md + docs/DESIGN.md + docs/EXPERIMENTS.md |
| 7 | cro-methodology | Will we know the fix worked — pre-committed metric, sample size, no peeking? | Extends docs/EXPERIMENTS.md + docs/METRICS.md |

## Operating Rules

1. **Resume first.** Before anything else, read `docs/CONVERSION-OPTIMIZATION-PLAN.md` and every artifact in the Journey Map. If the tracker exists, summarize the journey state in 3-5 lines and ask which phase to enter. Done when the user has confirmed an entry point. A journey with a tracker is resumed, never restarted.
2. **Intake on first run only.** No tracker: run the Intake below, then create `docs/CONVERSION-OPTIMIZATION-PLAN.md` with every phase statused `pending | in-progress | awaiting-evidence | done | deferred: reason | skipped: reason`. Done when the tracker exists and the user has confirmed the phase plan.
3. **Phase entry.** Announce: what the phase does, the decision it forces, the artifact it produces, rough effort. Offer proceed / skip / defer — phases marked GATE may be deferred, never skipped. Mark the phase `in-progress` on proceed. Done when the user chose.
4. **Skill invocation and fallback.** Load the phase's skill and use it: each phase's Invoke line names the skill by slug — use that skill to run the phase. If it is not available, offer: `npx skills add wondelai/skills/<slug> --global`. If the user declines, run the phase from its Brief — the minimum viable method. State which mode you are in.
5. **In-phase decisions.** Ask every question under "Decide with the user" — with concrete options and your recommendation. Record the choice in the tracker's Key Decisions. A decision made silently is a defect.
6. **Phase exit.** Present the draft artifact content for sign-off before writing. On approval: write or extend the docs/ files, update the tracker (status, Key Decisions, Next Actions). Done when the files are written and the phase row shows `done`.
7. **Artifact discipline.** Read before writing; create a file only if missing, otherwise extend — add or update your sections, preserve everyone else's. Files are UPPERCASE in `docs/`. Every recommendation lands as a checkbox or a table row with owner and priority. See [references/artifact-templates.md](references/artifact-templates.md) when creating a docs/ file for the first time — create it from the full skeleton (all section headings), then fill the sections your phase names.
8. **Measure, research, then change — and every change is a test.** No fix ships without a Phase 1 leak and a Phase 2 researched reason behind it, and every shipped change lands in docs/EXPERIMENTS.md with a pre-committed primary metric and a guardrail. A fix with no research behind it goes back to Phase 2; a bold change with no test attached stays in the backlog until it has one.

## Intake

Ask these before creating the tracker:

1. **Which flow are we optimizing, and what is the ONE action at its end?** (Scopes every phase — a flow with three competing CTAs has no goal.)
2. **Where do the numbers say people drop** — analytics, funnel steps, cohort data? Paste what you have. (Feeds the Phase 1 leak diagnosis; no instrumentation means Phase 1 starts by adding it.)
3. **Roughly how much traffic or volume enters the flow per week?** (Gates Phase 7 — decides whether A/B tests can reach significance or the journey leans on qualitative evidence and before/after windows.)
4. **What voice-of-customer sources exist or can be gotten** — exit surveys, session recordings, support tickets, sales calls, reviews — and can you paste or export the raw text of the best one? (Phase 2 objections must quote the customer's own words, so the phase needs the content, not just the source name.)
5. **What is the current offer at the conversion point** — price, guarantee, bonuses — and can it change? (Gates Phase 4; a contractually fixed offer narrows it to presentation.)
6. **Do docs/POSITIONING.md or docs/OFFER.md already exist from another journey?** (Phases 3-4 build on them rather than restarting.)
7. **How much of the journey do you want now?** (Phases 1-2 are the mandatory diagnosis; 3-6 are the fix passes aimed by it; 7 turns fixes into proof.)

Skip heuristics: skip Phase 3 when messaging was already validated (e.g. an improve-website journey completed its message phases); skip Phase 4 when the offer is fixed by contract — record `skipped: reason`. Phase 7 may be `deferred: reason` at very low traffic in favor of before/after evidence with an explicit revert trigger, never silently skipped. Never skip Phases 1-2 — an unfound leak and an unresearched reason turn every later phase into guessing.

Then create `docs/CONVERSION-OPTIMIZATION-PLAN.md` from the template and confirm the plan. Done when the tracker exists with every phase statused and the user has confirmed the plan.

## Phases

Phases run in the listed order — each assumes the previous phase's artifact exists. Any phase can be entered, skipped, or deferred per the Operating Rules, but Phases 1-2 gate them all: nothing downstream fixes a problem that isn't a measured leak with a researched reason. When running any phase from its Brief (constituent skill not installed), read [references/methods.md](references/methods.md) first — it carries each phase's full method, checklists, formulas, and benchmarks; the Brief is only the summary.

### Phase 1 — Find the leak (lean-analytics) — GATE

**Purpose:** Locate where the flow actually loses people and pick the one metric this journey moves — before any opinion about why.

**Brief (fallback):** A good metric is a comparative ratio that changes what you do next; totals and
cumulative charts are vanity. Express each step of the flow as a conversion rate, compare against your
own history and published benchmarks (e-commerce converts ~1-3% of visitors; landing pages on paid
traffic low single digits), and find the biggest absolute drop on the highest-value path. Pick the One
Metric That Matters for this journey, pair it with a counter-metric so it can't be gamed (signup rate
× 30-day retention), and draw a line in the sand: target, date, pre-committed miss response. Cohort
and segment (channel, device, plan) — one collapsing segment hides inside a flat average.

**Invoke:** Use the `lean-analytics` skill with the flow steps and analytics from intake. Ask for a step-by-step funnel table with baselines and benchmarks, the OMTM plus counter-metric for this journey, and the biggest leak ranked by absolute lost value.

**Decide with the user:** (1) Confirm the OMTM and its counter-metric. (2) Which leak to attack first — biggest absolute loss on the money path, not the easiest percentage. (3) If instrumentation is missing, which minimal events to add first — the phase stays `awaiting-evidence` until the numbers exist.

**Artifact:** Extend docs/METRICS.md `## Funnel` (stage | conversion | benchmark | bottleneck?), `## Stage & One Metric That Matters`, and `## Baselines & Targets`. Update the tracker.

**Done when:** the funnel is measured at the coarsest granularity that still localizes the leak to a single step, the OMTM and counter-metric are recorded with a line in the sand, and the leak is named — only then are Phases 2-7 unlocked. Finer sub-steps awaiting instrumentation stay `awaiting-evidence` in Next Actions and do not block the journey, provided the named leak does not depend on them.

### Phase 2 — Research why they leave (cro-methodology) — GATE

**Purpose:** Replace guesses about the leak with evidence from real visitors. Phases 3-6 may only fix problems traceable to a finding here.

**Brief (fallback):** Don't guess — discover. Mine primary sources (a one-question exit survey:
"What's preventing you from [action] today?"; post-conversion: "What almost stopped you?"; chat logs,
tickets, sales calls) and secondary sources (reviews, competitors) for the customer's own words. Sort
objections into the Big 5 — Trust, Price, Fit, Timing, Effort — and build the O/CO table: every
objection gets an evidence-backed counter placed at the exact step the doubt arises, never in an FAQ.
Diagnose each step with the LIFT lenses (value proposition ± clarity, relevance, urgency, minus
anxiety and distraction — Goward) and the MECLABS heuristic (conversion rises with motivation and
value clarity, falls with friction and anxiety). Rank fix hypotheses by ICE and apply the 10x screen:
if a change couldn't plausibly double the step, don't queue it.

**Invoke:** Use the `cro-methodology` skill with the Phase 1 leak, the flow, and the voice-of-customer sources from intake. Ask for the researched objection list in customer words, the O/CO table with placements, missing persuasion assets, and an ICE-ranked hypothesis backlog.

**Decide with the user:** (1) Which researched objection is the primary leak driver. (2) Low traffic: accept qualitative plus heuristic evidence — explicitly. (3) Which implicit objections need CO-Only counters (countered without being stated).

**Artifact:** Create docs/FUNNEL.md with `## Flow Map & ONE Action`, `## Leak Diagnosis`, and `## Objections & Counters (O/CO)`; extend docs/EXPERIMENTS.md `## Experiment Backlog` (ICE-ranked). METRICS.md `## Funnel` stays canonical for the conversion numbers — Leak Diagnosis cites them and adds the researched reason and severity. Update the tracker.

**Done when:** the flow map names the ONE action per step, every researched objection has an evidence-backed counter and a placement, and the backlog is ICE-ranked.

### Phase 3 — Fix the message at the leak (storybrand-messaging)

**Purpose:** Make the leaking step say what the visitor gets, in their words, in five seconds — clarity converts before persuasion can.

**Brief (fallback):** The customer is the hero; you are the guide. Run SB7 on the leaking step: a
Character who wants one thing, their Problem at three levels (external, internal — the frustration the
copy must name, philosophical), you as the Guide (empathy + authority), a 3-step Plan that makes
acting feel safe, one Direct plus one Transitional CTA, and named failure/success stakes. Rewrite the
step's headline in customer language pulled straight from Phase 2 — customer words outperform
copywriter words. Then make it stick (Made to Stick): concrete beats abstract ("save 16 hours a
month," not "boost productivity"), and pick the single Commander's Intent message the visitor must
still remember tomorrow.

**Invoke:** Use the `storybrand-messaging` skill with the step's current copy, the Phase 2 objection evidence, and POSITIONING.md if it exists. Ask for above-the-fold rewrites that name the internal problem, a one-liner, and one Direct plus one Transitional CTA.

**Decide with the user:** Which rewrite passes the 5-second test (a stranger can say what's offered and why it matters); which internal problem the copy names; whether the step keeps a transitional CTA or goes single-CTA.

**Artifact:** Extend docs/POSITIONING.md `## Brand Script (StoryBrand)`, `## One-Liner`, and `## Key Messages` (surface | message | status); record the rewrite in the `Proposed message/CTA` column of docs/FUNNEL.md `## Flow Map & ONE Action`, leaving `Current message/CTA` intact as the before-state Phase 7 measures against; append copy tests to docs/EXPERIMENTS.md `## Experiment Backlog`. Update the tracker.

**Done when:** the leaking step has a rewritten message that names the internal problem, one primary CTA, and a logged test hypothesis.

### Phase 4 — Make the offer worth acting on (hundred-million-offers)

**Purpose:** Strengthen what is actually exchanged at the conversion point — the best flow cannot sell a weak offer, and the offer is the biggest single lever.

**Brief (fallback):** Value = (Dream Outcome × Perceived Likelihood) ÷ (Time Delay × Effort &
Sacrifice). Raise the numerator with outcome language and proof; crush the denominator with speed
("first result in 5 minutes") and done-for-you framing. Reverse the risk with a guarantee aimed at the
top Phase 2 objection — it raises perceived likelihood and lowers anxiety at once. Stack named,
honestly-valued bonuses that each kill one objection; present price after value, anchored against the
stack. Scarcity and urgency only when real — fake deadlines convert once and churn forever.

**Invoke:** Use the `hundred-million-offers` skill with the current offer from intake and the Phase 2 Price/Timing/Effort objections. Ask for a Value Equation score per lever, a guarantee design matched to the top objection, and a trim-and-stack pass on the offer components.

**Decide with the user:** Which guarantee the business can actually honor; which bonuses are real and sustainable; whether price presentation changes (anchoring, payment plans) — pricing itself may be out of scope; record that.

**Artifact:** Extend docs/OFFER.md `## Offer Stack` (element | description | honest value | objection it kills), `## Price Metric` when the flow raises what the price is charged per, plus `## Willingness-to-Pay Evidence` if new evidence surfaced; append offer tests to docs/EXPERIMENTS.md `## Experiment Backlog`. Update the tracker.

**Done when:** each Value Equation lever has a concrete change or a reason it stays, the guarantee targets the top researched objection, and every offer change carries a test hypothesis.

### Phase 5 — Put proof at every doubt (influence-psychology)

**Purpose:** Answer each remaining objection with honest evidence placed at the exact step the doubt arises.

**Brief (fallback):** Under uncertainty people use shortcuts: social proof (specific numbers — "2,347
teams" — and similar-others beat generic praise), authority (credentials, certifications), commitment
(a small first yes makes the big yes consistent — ask for the card after the value moment, not
before), reciprocity (give the useful thing first), and scarcity (real only). Audit the flow for proof
gaps: every O/CO row needs its counter actually rendered — testimonial, data point, logo bar,
guarantee seal — at its placement. Proof hierarchy: specific results with context > named testimonials
with faces > case studies > statistics > logos. The transparency test gates everything: if knowing the
technique would make the visitor feel tricked, it fails. Fabricated proof and hidden costs are
defects, not tactics.

**Invoke:** Use the `influence-psychology` skill with the FUNNEL.md O/CO table and the flow's current proof. Ask for a per-step proof audit, which principle answers each open objection, and copy for the two highest-impact placements.

**Decide with the user:** Which proof assets exist versus must be acquired (testimonial requests, case studies — log acquisition as Next Actions); where scarcity or urgency claims are genuinely true; which steps get a commitment micro-ask.

**Artifact:** Extend docs/FUNNEL.md `## Proof Inventory` (asset | type | placement | status) and complete the `## Objections & Counters (O/CO)` placements; append proof tests to docs/EXPERIMENTS.md `## Experiment Backlog`. Update the tracker.

**Done when:** every open objection row has a real proof asset placed or an acquisition task with an owner, and no claim in the flow is unverifiable.

### Phase 6 — Remove the friction (design-everyday-things)

**Purpose:** Protect the visitors who decided to act. B=MAP: behavior happens when Motivation, Ability, and a Prompt converge — Phases 3-5 raised motivation; this phase raises ability and sharpens prompts.

**Brief (fallback):** Bridge Norman's two gulfs. Execution: clear signifiers (buttons look pressable,
fields look editable) and constraints that make errors impossible (date picker over free text, submit
disabled until valid). Evaluation: feedback within 0.1s of every action, progress indication on
multi-step flows. Forms (Baymard): every field costs conversions — cut to the minimum, ask for payment
as late as possible, show all costs before the final step (surprise shipping and taxes is the #1
checkout killer), offer guest checkout, validate inline with messages that say how to fix. Error
messages state what went wrong and how to fix it, without blame; slips get undo, not are-you-sure
dialogs.

**Invoke:** Use the `design-everyday-things` skill with the conversion-critical steps (form, payment, confirmation). Ask for weak signifiers, where constraints replace error messages, feedback gaps, field-by-field form cuts, and message rewrites.

**Decide with the user:** Which fields are truly required now versus collectable later; where a constraint replaces a warning; whether the flow shows total cost earlier; which severity-4 friction items ship immediately as a logged before/after card versus wait for a full test.

**Artifact:** Extend docs/FUNNEL.md `## Flow Friction Audit` (step | issue | severity 0-4 | fix | status); extend docs/DESIGN.md `## UX Audit Findings` for reusable component fixes, naming the Norman gulf (execution or evaluation) in the `Heuristic` column; append fixes to docs/EXPERIMENTS.md `## Experiment Backlog`. Update the tracker.

**Done when:** every step has a friction audit row, forms are cut to minimum fields, severity-4 items have owners, and error messages meet the checklist. Where money changes hands in this flow, all costs are visible before the final step and guest checkout is offered; in a flow that takes no payment, mark those two rows `n/a`.

### Phase 7 — Prove it (cro-methodology)

**Purpose:** Turn the high-ICE fixes into trustworthy experiments — without rigor you cannot tell a real lift from noise, and a false winner compounds forever.

**Brief (fallback):** Pre-commit everything (Kohavi): primary metric, guardrail metrics (the Phase 1
counter-metric, revenue per visitor, support volume), sample size computed from baseline rate and
minimum detectable effect at 95% significance / 80% power, and a duration of at least one full
business cycle covering weekdays and weekends. Never peek and stop early — it manufactures false
positives; never rerun until you like the answer. Test bold changes — meek tweaks rarely reach
significance. Low traffic: run a before/after window with qualitative confirmation, or ship as a
reversible bet with an explicit revert trigger — and say which you are doing. Practical significance
gates rollout: a statistically significant 0.1% lift may not pay for its complexity. Winners become
the new control; losers become learnings written down.

**Invoke:** Use the `cro-methodology` skill with the top ICE hypotheses from the backlog. Ask for full experiment designs: hypothesis in "If [change], then [metric] because [research]" form, pre-committed sample size and duration, and the decision rule.

**Decide with the user:** Which 1-3 hypotheses run first (highest ICE on the money path); the guardrail metrics; what happens on a flat result — iterate the fix, or return to Phase 2 for better research.

**Artifact:** Promote backlog rows to docs/EXPERIMENTS.md `## Experiment Cards`, adding the pre-committed sample size per arm, planned duration, and the minimum lift worth keeping as extra bullets on the card (the skeleton's bullets carry hypothesis, metrics, and decision rule; extra bullets are additive and allowed); record results and verdicts as they land; extend docs/METRICS.md `## Baselines & Targets` with a new dated row per tested metric, leaving the pre-test baseline row intact. Update the tracker.

**Done when:** each shipped fix is a card with a pre-committed metric, sample size, and decision rule; results carry verdicts; and the OMTM's new baseline is written down.

## Optional Phases

| Skill | Add when | Artifact |
|---|---|---|
| ux-heuristics | the whole page confuses, not just the flow — visitors stumble before reaching the conversion steps | Extends docs/DESIGN.md `## UX Audit Findings` |
| microinteractions | the flow's moments feel dead — silent taps, unexplained waits, abrupt state changes | Extends docs/DESIGN.md `## Microinteraction Inventory` |
| scorecard-marketing | the flow needs a lower-commitment entry — a quiz or assessment as the transitional conversion | Extends docs/WEBSITE.md `## Lead Capture` |
| hooked-ux | the conversion sticks but the next visit doesn't — post-conversion activation is the real leak | Extends docs/PRODUCT.md `## Hook Model` |

Optional phases follow the same operating rules — load and use each listed skill exactly as a core phase would; insert where the Add-when condition first becomes true. They carry no inline Brief: standalone, run ux-heuristics as a severity-rated pass over Nielsen's 10 heuristics, microinteractions as a trigger/rules/feedback/loops inventory, scorecard-marketing as a quiz-funnel design ending in a personalized result, and hooked-ux as a trigger → action → variable reward → investment loop audit — or install the named skill for its full framework.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Redesigning the step before measuring where the leak is | Run Phase 1 first — the biggest drop is rarely where opinion points; optimize the money path, not the loudest complaint. |
| Guessing objections instead of mining customer words | Exit surveys, tickets, and sales calls (cro-methodology) — teams are almost always wrong about why visitors leave. |
| Polishing persuasion on top of an unclear message | Clarity before psychology: pass the 5-second test (storybrand-messaging) before adding proof and urgency. |
| Treating the offer as fixed and testing only cosmetics | The offer is the biggest lever (hundred-million-offers); a guarantee change outlifts a button change by orders of magnitude. |
| Faking scarcity or cherry-picking proof | Converts once, churns forever, caps trust permanently — real scarcity and verifiable proof only (influence-psychology). |
| Adding form fields "while we're at it" | Every field costs conversions (Baymard); collect later what you don't need now (design-everyday-things). |
| Peeking at test results and stopping early | Pre-commit sample size and duration, then report whatever comes back (cro-methodology, Kohavi). |

## Completing the Journey

A funnel always has a next-biggest leak: when the Phase 7 verdicts land, re-enter Phase 1 with fresh numbers rather than declaring victory — the journey is a loop with an exit condition, and the exit condition is the line in the sand from Phase 1, not exhaustion.

Exit checklist — every box tied to an artifact:

- [ ] Every phase in `docs/CONVERSION-OPTIMIZATION-PLAN.md` is `done`, `deferred: reason`, or `skipped: reason`.
- [ ] The OMTM, counter-metric, and line in the sand are recorded with pre- and post-test baselines (METRICS.md).
- [ ] Every researched objection has a placed, verifiable counter (FUNNEL.md O/CO and Proof Inventory — no open rows on the money path).
- [ ] The flow's forms and steps carry no severity-4 friction without an owner (FUNNEL.md Flow Friction Audit).
- [ ] Each shipped change is an Experiment Card with a pre-committed metric and a recorded verdict (EXPERIMENTS.md).

Close the tracker: remaining Next Actions carried into FUNNEL.md and EXPERIMENTS.md so nothing is lost. Then route forward: when the flow converts and needs more qualified traffic, continue with the `grow-website` skill; when the leak has moved past conversion into engagement and retention, continue with the `improve-app` skill; when the whole site — look, typography, speed, message — needs the broader pass, continue with the `improve-website` skill.
