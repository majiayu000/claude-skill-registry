---
name: improve-app
description: 'Guided journey from a shipped app that works but feels rough to a product that fits the job, flows without friction, reads clearly, and persuades honestly. Orchestrates nine skills phase by phase - jobs-to-be-done, ux-heuristics, design-everyday-things, refactoring-ui, microinteractions, made-to-stick, influence-psychology, high-perf-browser, steve-jobs-design-review - asking the user questions at every decision point and recording results in the project docs/ folder (CUSTOMER.md, DESIGN.md, POSITIONING.md, IMPROVE-APP-PLAN.md) so the journey resumes across sessions. Use when the user wants to fix a clunky product, cut UX friction, sharpen in-app copy and prompts, or says ''the app works but feels rough''. Do not use for code, tests, or production hardening - use improve-code-quality (fresh prototype) or remove-technical-debt (aged codebase); no app yet, create-app; needs growth loops, grow-app; marketing-site friction, improve-website. For one framework in isolation, invoke that skill directly.'
license: MIT
metadata:
  author: wondelai
  version: "2.0.0"
---

# Improve an App

The app already ships and works — users, screens, a real flow — but the experience feels rough where it
should feel effortless. Across nine phases this journey fixes what users feel, in evidence order: re-anchor
on the job, remove friction, polish the look and the moments, sharpen the words, persuade honestly, and end
with a review brutal enough to cut. It is interactive (the agent asks before deciding) and resumable (state
lives in `docs/`). Code-level causes route out to the code journeys — this pass fixes the product experience.

## Core Principle

**Fix what users feel, in evidence order: re-anchor on the job the app is hired for, remove friction before
polish, sharpen the words, persuade honestly, and end with a review brutal enough to cut.** A prettier
screen on a confusing flow loses users at the same rate — the order of the phases is the whole game.

This skill sequences the phases, asks the decision questions, and records what you decide. The nine
constituent skills carry the method — invoke them rather than improvising their frameworks.

## Journey Map

| Phase | Skill | Question it answers | Artifact |
|---|---|---|---|
| 1 | jobs-to-be-done | What job is the app hired for, and where does it underdeliver? | Extends docs/CUSTOMER.md — GATE |
| 2 | ux-heuristics | Where does the interface make users stop and think? | Extends docs/DESIGN.md, docs/EXPERIMENTS.md |
| 3 | design-everyday-things | Where do users act wrong because the design misled them? | Extends docs/DESIGN.md, docs/EXPERIMENTS.md |
| 4 | refactoring-ui | Does the app look as clear as it works? | Extends docs/DESIGN.md, docs/EXPERIMENTS.md |
| 5 | microinteractions | Does every action feel alive, or dead? | Extends docs/DESIGN.md, docs/EXPERIMENTS.md |
| 6 | made-to-stick | Do the in-app words land, or read as jargon? | Extends docs/POSITIONING.md, docs/EXPERIMENTS.md |
| 7 | influence-psychology | Do the paywall and upgrade moments persuade honestly? | Extends docs/POSITIONING.md, docs/EXPERIMENTS.md |
| 8 | high-perf-browser | Does the app feel fast where users touch it? | Extends docs/DESIGN.md, docs/EXPERIMENTS.md |
| 9 | steve-jobs-design-review | Is the whole experience insanely great, or just better? | Extends docs/PRODUCT.md, docs/DESIGN.md, docs/EXPERIMENTS.md |

## Operating Rules

1. **Resume first.** Before anything else, read `docs/IMPROVE-APP-PLAN.md` and every artifact in the Journey Map. If the tracker exists, summarize the journey state in 3-5 lines and ask which phase to enter. Done when the user has confirmed an entry point. A journey with a tracker is resumed, never restarted.
2. **Intake on first run only.** No tracker: run the Intake below, then create `docs/IMPROVE-APP-PLAN.md` with every phase statused `pending | in-progress | awaiting-evidence | done | deferred: reason | skipped: reason`. Done when the tracker exists and the user has confirmed the phase plan.
3. **Phase entry.** Announce: what the phase does, the decision it forces, the artifact it produces, rough effort. Offer proceed / skip / defer — phases marked GATE may be deferred, never skipped. Mark the phase `in-progress` on proceed. Done when the user chose.
4. **Skill invocation and fallback.** Invoke the phase's skill by its slug. If it is not available, offer: `npx skills add wondelai/skills/<slug> --global`. If the user declines, run the phase from its Brief — the minimum viable method. State which mode you are in.
5. **In-phase decisions.** Ask every question under "Decide with the user" — with concrete options and your recommendation. Record the choice in the tracker's Key Decisions. A decision made silently is a defect.
6. **Phase exit.** Present the draft artifact content for sign-off before writing. On approval: write or extend the docs/ files, update the tracker (status, Key Decisions, Next Actions). Done when the files are written and the phase row shows `done`.
7. **Artifact discipline.** Read before writing; create a file only if missing, otherwise extend — add or update your sections, preserve everyone else's. Files are UPPERCASE in `docs/`. Every recommendation lands as a checkbox or a table row with owner and priority. See [references/artifact-templates.md](references/artifact-templates.md) when creating a docs/ file for the first time — create it from the full skeleton (all section headings), then fill the sections your phase names.
8. **Evidence before redesign; persuasion stays honest.** No UI or copy change ships without an audit or evidence row from Phases 1-3 behind it — a change with no finding behind it goes back to the audits. Every shipped change lands in docs/EXPERIMENTS.md with a pre-committed metric. Every in-app scarcity cue, social-proof claim, and upgrade promise must be true — replace any tactic that needs invented evidence with one that uses evidence you have.

## Intake

Ask these before creating the tracker:

1. **What is the app, and what job did users hire it to do — in their words?** (Anchors Phase 1; gates every later phase.)
2. **Where does it feel roughest** — confusing screens, dead interactions, amateur UI, weak copy, pushy upgrade prompts, or sluggishness? (Sets the entry phase and front-loads a fix phase.)
3. **What evidence do you have** — recordings, support tickets, reviews, funnel drop-off, usage analytics? ("None" routes to the optional continuous-discovery phase.)
4. **What platform(s) does the app run on** — web, native iOS, both? (Gates Phase 8 and optional ios-hig-design; no browser surface with smooth native perf skips Phase 8.)
5. **Which in-app surfaces sell or upsell** — paywall, upgrade prompt, trial nudge, badges — and are the scarcity and social-proof claims true today? (Scopes Phase 7 and the honesty guardrail.)
6. **Which flow leaks the most users or draws the most tickets?** (Targets Phases 2-3, 5, and 8.)
7. **Do you already have positioning, design, or customer docs** (POSITIONING.md, DESIGN.md, CUSTOMER.md)? (Phases 1, 4, 6, 7 build on them.)

Phase-skip heuristics: skip Phase 8 with no browser surface and smooth native speed; skip Phase 7 with no
in-app upsell surfaces; skip Phase 4 when the UI already reads cleanly in grayscale on a consistent token
scale; skip Phase 6 when in-app copy is already concrete and jargon-free. Never skip Phase 1 — it aims every
other phase (defer it, don't skip it). Then create `docs/IMPROVE-APP-PLAN.md` from the template and confirm
the plan. Done when `docs/IMPROVE-APP-PLAN.md` exists with every phase statused and the user has confirmed the plan.

## Phases

### Phase 1 — Re-anchor on the job the app is hired for (jobs-to-be-done) — GATE

**Purpose:** Name the job users hire the app for and where it underdelivers, before any screen changes; Phases 2-9 may only fix what an audit or finding in Phases 1-3 flags.

**Brief (fallback):** Customers hire a product to make progress in a circumstance. State the job as "When [situation], I want to [motivation], so I can [outcome]" — never naming the app; every job has three dimensions (functional, emotional, social), and omitting one loses why users stay. Track first use vs repeated use (Big Hire vs Little Hire), and map alternatives including non-consumption and improvised workarounds.

**Invoke:** `jobs-to-be-done` with the app, its usage data, and the roughest flow from intake. Ask for the job statement, the three dimensions with where the app underdelivers on each, and the alternatives users switch to.

**Decide with the user:** (1) Confirm the job statement reads without the product name. (2) Which underdelivered dimension is worst — functional, emotional, or social? (3) Is the leak a Big Hire (onboarding) or Little Hire (daily use) failure?

**Artifact:** Extend docs/CUSTOMER.md `## Job Statement`, `## Job Dimensions` (functional/emotional/social, each with its underdelivery note), and `## Competing Alternatives` (alternative | why hired | weakness, incl. non-consumption). Update the tracker.

**Done when:** the job is stated without the product name, all three dimensions carry an underdelivery note, alternatives are logged, and Phase 1 shows done — only then are Phases 2-9 unlocked.

### Phase 2 — Remove the friction that makes users think (ux-heuristics)

**Purpose:** Cut cognitive load on the flows that leak users — find where the interface makes people stop and puzzle.

**Brief (fallback):** "Don't Make Me Think" — users scan, satisfice, and muddle through. Run a heuristic evaluation against Nielsen's 10 heuristics; rate each issue 0-4 and order by severity × how often users hit it, so catastrophes outrank cosmetics. Apply the Trunk Test to key screens (what app, what screen, my options, where am I, where's search?), cut half the words then half again, and fix forms with inline validation and error messages that say what, why, and how.

**Invoke:** `ux-heuristics` on the highest-leak flow with the Phase 1 job and dimensions. Ask for a severity-rated evaluation, a Trunk Test result per key screen, and rewritten label, form, and error copy.

**Decide with the user:** Which severity-4 and -3 issues get fixed now versus backlogged? Confirm fixes run by severity × frequency, not by ease.

**Artifact:** Extend docs/DESIGN.md `## UX Audit Findings` (issue | heuristic | severity 0-4 | fix | status); append each fix to docs/EXPERIMENTS.md `## Experiment Backlog` with ICE. Update the tracker.

**Done when:** every issue carries a 0-4 severity and a fix, the Trunk Test passes on each key screen or is logged, and severity-4 issues have an owner.

### Phase 3 — Design out the errors (design-everyday-things)

**Purpose:** Make the wrong action hard and every outcome legible — where users act wrong, the design misled them, not the user.

**Brief (fallback):** There is no human error, only bad design. Bridge two gulfs: Execution ("how do I do this?") with clear signifiers and constraints (date picker over free text, Submit disabled until valid); Evaluation ("what happened?") with feedback under 0.1s and visible system state. Distinguish slips (right intent, wrong action) from mistakes (wrong intent); prefer undo over are-you-sure dialogs, and write error messages that say what went wrong and how to fix it, never blame.

**Invoke:** `design-everyday-things` on the core flows (onboarding, the primary action, destructive actions). Ask for weak signifiers, where a constraint makes an error impossible, feedback gaps, and message rewrites.

**Decide with the user:** Where should a constraint replace an error message, and where should undo replace a confirmation dialog?

**Artifact:** Extend docs/DESIGN.md `## UX Audit Findings` (heuristic = Norman gulf; issue | severity 0-4 | fix | status); append fixes to docs/EXPERIMENTS.md `## Experiment Backlog`. Update the tracker.

**Done when:** each core flow has signifier/constraint/feedback fixes logged, error messages meet the what/why/how checklist, and destructive actions offer undo.

### Phase 4 — Make it look as clear as it works (refactoring-ui)

**Purpose:** Give the screens a professional visual hierarchy so nothing amateur undercuts the flows you just fixed.

**Brief (fallback):** Great UI is systems, not talent. Design in grayscale first: establish hierarchy with size, weight, and contrast before any color — combine levers, don't multiply (all three only for the one hero element). Enforce a spacing scale (4/8/16/24/32/48/64) where gaps between groups exceed gaps within them; constrain text to 45-75 chars and forms to 300-500px. Add color last: 5-9 shades per hue, grays tinted, not pure black.

**Invoke:** `refactoring-ui` on the key screens with the Phase 2-3 findings and current design tokens. Ask for a grayscale hierarchy pass, spacing-scale corrections, a systematic palette, and the exact token/CSS changes.

**Decide with the user:** Fix within the current design system or introduce new tokens? Confirm color work waits until the grayscale layout reads.

**Artifact:** Extend docs/DESIGN.md `## Tokens` (spacing scale · palette shades · shadows) and `## Components` (component | decision | status); append fixes to docs/EXPERIMENTS.md `## Experiment Backlog`. Update the tracker.

**Done when:** the key screens read in grayscale, the spacing scale is applied, one primary action dominates each screen, and the token decisions are recorded.

### Phase 5 — Make every action feel alive (microinteractions)

**Purpose:** Give the moments users touch every day the feedback that separates a product they tolerate from one they love.

**Brief (fallback):** Every microinteraction has four parts — Trigger, Rules, Feedback, Loops & Modes. The common failure is missing or late feedback: direct manipulation needs a response under 100ms, usually by animating the element the user touched (a button depresses to "Saving…"), not a separate toast. Map every state — empty, loading, partial, full, error, disabled — and use the least feedback that communicates, scaled to the event's significance.

**Invoke:** `microinteractions` on the most-used interactions (save, submit, toggle, delete, load). Ask for a Trigger/Rules/Feedback/Loops audit, the exact feedback each needs, a full state map, and one signature moment.

**Decide with the user:** (1) Which interactions to polish first. (2) The one signature moment worth extra craft — apply the removal test: would the product feel materially worse without it?

**Artifact:** Extend docs/DESIGN.md `## Microinteraction Inventory` (interaction | trigger/rules/feedback/loops | fix | status); append fixes to docs/EXPERIMENTS.md `## Experiment Backlog`. Update the tracker.

**Done when:** each audited interaction has its four parts and required feedback logged, every state is mapped, the signature moment passes the removal test, and fixes are rows with status.

### Phase 6 — Sharpen the in-app words (made-to-stick)

**Purpose:** Make the copy users read inside the app — onboarding, empty states, errors, CTAs, tooltips — concrete, clear, and jargon-free.

**Brief (fallback):** Beat the Curse of Knowledge: once you know the product you can't imagine not knowing it. Score key in-app copy on SUCCESs (Simple, Unexpected, Concrete, Credible, Emotional, Stories). Concrete beats abstract: "Users open the app 8 times a day," not "increase engagement." Simple is the Commander's Intent — the one thing a screen must land; if a label needs a manual, rewrite the label.

**Invoke:** `made-to-stick` with the onboarding copy, empty states, error strings, CTAs, and tooltips plus the Phase 1 job language. Ask for a SUCCESs score per surface with concrete de-jargoned rewrites and the Commander's Intent for each screen.

**Decide with the user:** Which abstractions become which concrete specifics, and what is the one thing each screen must land?

**Artifact:** Extend docs/POSITIONING.md `## Key Messages` (surface = the in-app screen | message | status) with SUCCESs scores and concrete rewrites; append copy tests to docs/EXPERIMENTS.md `## Experiment Backlog`. Update the tracker.

**Done when:** each in-app surface has a SUCCESs score and a concrete rewrite, jargon is gone, the Commander's Intent per screen is named, and the messages are logged by surface.

### Phase 7 — Persuade honestly at the decision points (influence-psychology)

**Purpose:** Make the in-app marketing surfaces — paywalls, upgrade prompts, trial nudges, social proof, badges — persuade with true evidence, not tricks.

**Brief (fallback):** People decide with mental shortcuts — seven principles trigger "yes": reciprocity, commitment, social proof, authority, liking, scarcity, unity. Apply them where the user decides (paywall, upgrade, trial end); layer principles, keep every claim truthful, keep the decision reversible. Ethics gate: any fabricated proof, fake scarcity, or hidden-cost dark pattern is disqualifying — a tactic that only works if the user doesn't know the strategy is manipulation, not persuasion.

**Invoke:** `influence-psychology` on the upsell surfaces from intake. Ask which principles fit each decision point, the honest copy for each, and a reversibility check — flag any cue that needs evidence you don't have.

**Decide with the user:** (1) Which principle leads at each surface. (2) For each scarcity or social-proof cue: is it true today? If not, cut it or make it true before shipping.

**Artifact:** Extend docs/POSITIONING.md `## Key Messages` (surface | message | status) with the persuasion copy; queue each change in docs/EXPERIMENTS.md `## Experiment Backlog` with the metric it should move. Update the tracker.

**Done when:** each upsell surface names its lead principle and honest copy, every scarcity/social-proof claim is verified true or cut, decisions are reversible, and changes are queued as experiments.

### Phase 8 — Make it feel fast where users touch it (high-perf-browser)

**Purpose:** Fix perceived slowness on the interactions and entry views users feel — speed is part of the experience, not a back-end afterthought.

**Brief (fallback):** Latency, not bandwidth, is the bottleneck — most pain is too many round trips. Target the field metrics: INP under 200ms on key interactions (break long tasks, defer non-critical JS), LCP under 2.5s on entry views (preload the hero, raise fetchpriority), CLS under 0.1 (reserve space with explicit dimensions). Where real latency remains, hide it with skeleton screens and optimistic UI so the interface responds before the server does.

**Invoke:** `high-perf-browser` on the slowest key interaction and entry view with a trace or Lighthouse run if available. Ask for the INP long tasks, the LCP element, layout-shift sources, and an impact-ordered fix list including where skeletons or optimistic UI apply.

**Decide with the user:** Which interactions and views to measure first, and confirm the field-metric targets as the lines in the sand.

**Artifact:** Extend docs/DESIGN.md `## UX Audit Findings` (heuristic = performance; issue | severity 0-4 | fix | status) with INP/LCP/CLS rows; append fixes to docs/EXPERIMENTS.md `## Experiment Backlog`. Update the tracker.

**Done when:** INP/LCP/CLS baselines are recorded as performance rows, targets are set (INP < 200ms, LCP < 2.5s, CLS < 0.1), and each fix is ordered by impact with skeleton/optimistic-UI fallbacks noted where latency remains.

### Phase 9 — Submit it to a brutal, honest review (steve-jobs-design-review)

**Purpose:** Judge the whole experience cold against "insanely great, or not done" — and decide what to subtract.

**Brief (fallback):** Start from the customer experience and work back. Experience the product cold as a new user, name the One Thing it must do, count steps-to-value, and deliver a binary verdict with a ranked cut list and fix list. Focusing is saying no — every feature is a candidate for deletion. Audit the back of the fence: empty states, error copy, 404, billing, cancellation, receipt email — held to the hero-screen bar.

**Invoke:** `steve-jobs-design-review` on the whole app after Phases 1-8. Ask for a cold walkthrough, the One Thing, the step count to core value, a binary verdict, a ranked cut and fix list, and a back-of-the-fence audit.

**Decide with the user:** (1) Accept the cut list — which features to actually remove. (2) Which back-of-the-fence fixes ship now versus later.

**Artifact:** Extend docs/PRODUCT.md `## Outcome Roadmap` (outcome/problem | job served | priority | status) with the cuts and fixes as prioritized rows; append any back-of-the-fence fixes to docs/DESIGN.md `## UX Audit Findings`; queue fixes that will ship in docs/EXPERIMENTS.md `## Experiment Backlog`. Update the tracker.

**Done when:** the verdict is recorded, the cut list is agreed with each item's disposition, cuts and fixes are prioritized rows in `## Outcome Roadmap`, and the tracker closes Phase 9.

## Optional Phases

| Skill | Add when | Artifact |
|---|---|---|
| ios-hig-design | the app ships natively on iOS | Extends docs/DESIGN.md |
| lean-ux | a risky fix deserves a cheap experiment before a full build | Extends docs/EXPERIMENTS.md |
| continuous-discovery | improvement ideas come from opinions, not weekly user contact | Extends docs/CUSTOMER.md |
| improve-retention | first-run activation friction shows up in the audits (full retention engine: grow-app) | Extends docs/PRODUCT.md |
| web-typography | the app is text-heavy and reading comfort drives the experience | Extends docs/DESIGN.md |
| inspired-product | the backlog is a feature list with no outcomes behind it | Extends docs/PRODUCT.md |

Optional phases follow the same operating rules; insert where the Add-when condition first becomes true.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Polishing visuals before removing friction — a beautiful screen on a confusing flow loses users at the same rate. | Run Phases 2-3 (ux-heuristics, design-everyday-things) first; no visual change ships without a Phase 1-3 finding behind it. |
| Adding color before the grayscale layout works. | Grayscale first, color last; if the screen fails desaturated, no palette saves it (refactoring-ui). |
| Treating "user error" as the user's fault and stacking on more warnings. | Prevent slips with constraints and forgive them with undo, not are-you-sure dialogs (design-everyday-things). |
| Rewriting copy from internal language nobody outside the team tested. | De-jargon against the SUCCESs pass, then ship the rewrite as an EXPERIMENTS card, not a guess (made-to-stick). |
| Fake scarcity or invented social proof in upgrade prompts. | Every scarcity cue and testimonial must be true; replace any tactic that needs invented evidence with one that uses evidence you have (influence-psychology). |
| Shipping the fixes and skipping the brutal end-to-end review. | Run Phase 9 cold as a new user; a binary verdict with a ranked cut list catches what phase-by-phase fixes miss (steve-jobs-design-review). |

## Completing the Journey

Exit checklist:

- [ ] Every phase in `docs/IMPROVE-APP-PLAN.md` is `done`, `skipped: reason`, or `deferred: reason`.
- [ ] CUSTOMER.md re-anchors the job and names where the app underdelivers on each dimension.
- [ ] DESIGN.md carries the UX audit findings, tokens/components, microinteraction inventory, and performance rows with owner and priority.
- [ ] POSITIONING.md `## Key Messages` holds the in-app copy and persuasion surfaces, every scarcity and social-proof claim true.
- [ ] Each shipped change is an EXPERIMENTS.md card or backlog row with a pre-committed metric, and PRODUCT.md `## Outcome Roadmap` holds the steve-jobs cut and fix list.

Close the tracker: every phase `done` / `skipped: reason` / `deferred: reason`, and Next Actions carried into
the owning artifacts rather than left in the plan.

Forward routing: when the experience holds up and the goal shifts to habit, retention, and growth loops,
continue with `grow-app`. When the audits keep hitting code-level causes (slow queries, crashes, untestable
modules), continue with `improve-code-quality` or `remove-technical-debt`. When the marketing site is the
next weakest surface, continue with `improve-website`.
