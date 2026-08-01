---
name: grow-website
description: 'Guided journey from a website with traffic it under-converts to a research-driven growth engine that captures more leads, persuades more buyers, sells a sharper offer, and earns referrals. Orchestrates eight skills phase by phase - cro-methodology, scorecard-marketing, storybrand-messaging, made-to-stick, influence-psychology, hundred-million-offers, contagious, one-page-marketing - asking the user questions at every decision point and recording results in the project docs/ folder (WEBSITE.md, OFFER.md, MARKETING.md, GROW-WEBSITE-PLAN.md) so the journey resumes across sessions. Use when the user wants to raise conversion on a site that already has traffic, capture more leads, sharpen a weak offer, add referral loops, or says ''my site gets visitors but nobody buys''. If a broken funnel or usability friction is the real blocker, run improve-website first; if there is no site yet, use create-website. For one framework in isolation, invoke that skill directly.'
license: MIT
metadata:
  author: wondelai
  version: "1.0.0"
---

# Grow a Website

Take a site that already has traffic and under-monetizes it, and turn it into a research-driven growth engine: more leads captured, more buyers persuaded, a sharper offer, and visitors who bring more visitors. This journey runs eight phases — the agent asks before it decides at every fork, and all state lives in `docs/` so you can stop and resume across sessions. It sequences the work; it does not redesign the site on a hunch.

## Core Principle

**Most traffic problems are conversion problems in costume: capture and convert the visitors you have before buying more.** This skill sequences the phases, asks the decision questions, and records every choice in `docs/`. The constituent skills carry the method — invoke them rather than improvising their frameworks. Research comes before optimization, and the offer comes before the page polish, always.

## Journey Map

| Phase | Skill | Question it answers | Artifact |
|---|---|---|---|
| 1. Discover why visitors leave | cro-methodology | Why do visitors not convert, and what is worth testing? | Extends docs/WEBSITE.md, docs/METRICS.md, docs/EXPERIMENTS.md |
| 2. Capture the not-ready 97% | scorecard-marketing | How do we keep the leads who aren't ready to buy? | Extends docs/WEBSITE.md, docs/MARKETING.md |
| 3. Clarify the message | storybrand-messaging | Can a stranger tell what we do in five seconds? | Extends docs/POSITIONING.md |
| 4. Make the message stick | made-to-stick | Will they remember it when they are ready to buy? | Extends docs/POSITIONING.md, docs/WEBSITE.md |
| 5. Add proof and triggers | influence-psychology | Why should they believe us, and act now? | Extends docs/WEBSITE.md |
| 6. Rebuild the offer | hundred-million-offers | Is the thing we sell irresistible? | Extends docs/OFFER.md, docs/EXPERIMENTS.md |
| 7. Engineer shareability | contagious | Will visitors bring us more visitors? | Extends docs/MARKETING.md, docs/WEBSITE.md |
| 8. Connect the lifecycle | one-page-marketing | Do the wins link into one compounding engine? | Extends docs/MARKETING.md, docs/METRICS.md |

## Operating Rules

1. **Resume first.** Before anything else, read `docs/GROW-WEBSITE-PLAN.md` and every artifact in the Journey Map. If the tracker exists, summarize the journey state in 3-5 lines and ask which phase to enter. Done when the user has confirmed an entry point. A journey with a tracker is resumed, never restarted.
2. **Intake on first run only.** No tracker: run the Intake below, then create `docs/GROW-WEBSITE-PLAN.md` with every phase statused `pending | in-progress | awaiting-evidence | done | deferred: reason | skipped: reason`. Done when the tracker exists and the user has confirmed the phase plan.
3. **Phase entry.** Announce: what the phase does, the decision it forces, the artifact it produces, rough effort. Offer proceed / skip / defer — phases marked GATE may be deferred, never skipped. Mark the phase `in-progress` on proceed. Done when the user chose.
4. **Skill invocation and fallback.** Invoke the phase's skill by its slug. If it is not available, offer: `npx skills add wondelai/skills/<slug> --global`. If the user declines, run the phase from its Brief — the minimum viable method. State which mode you are in.
5. **In-phase decisions.** Ask every question under "Decide with the user" — with concrete options and your recommendation. Record the choice in the tracker's Key Decisions. A decision made silently is a defect.
6. **Phase exit.** Present the draft artifact content for sign-off before writing. On approval: write or extend the docs/ files, update the tracker (status, Key Decisions, Next Actions). Done when the files are written and the phase row shows `done`.
7. **Artifact discipline.** Read before writing; create a file only if missing, otherwise extend — add or update your sections, preserve everyone else's. Files are UPPERCASE in `docs/`. Every recommendation lands as a checkbox or a table row with owner and priority. See [references/artifact-templates.md](references/artifact-templates.md) when creating a docs/ file for the first time — create it from the full skeleton (all section headings), then fill the sections your phase names.
8. **Every scarcity claim, testimonial, and share incentive must be true.** When a persuasion tactic needs inventing evidence, replace it with a tactic that uses evidence you have. A countdown that resets, a "only 2 left" that never changes, or a fabricated review poisons every honest claim that follows it.

## Intake

Ask these before creating the tracker:

1. What is the site, and what is its primary conversion action — signup, purchase, booking, lead form? (Anchors every phase and defines where the funnel ends.)
2. What traffic and conversion numbers do you have — sessions, bounce rate, conversion rate, worst-performing high-traffic page? (Gates Phase 1's funnel map and whether A/B testing can reach significance.)
3. What visitor research already exists — exit surveys, support tickets, chat logs, reviews? (Raw material for the O/CO table; if none, Phase 1 starts by gathering it.)
4. Do you already capture leads (list, lead magnet), and how well does it convert? (Gates Phase 2.)
5. What are you selling, at what price, and do visitors call it "too expensive"? (Gates Phase 6's offer rebuild.)
6. Is there existing positioning or messaging — a POSITIONING.md, a brand script, a one-liner? (Gates Phases 3-4; reuse rather than redo.)
7. What is your monthly traffic volume? (Decides Phase 1's testing approach: enough for bold A/B tests to reach significance, or lean on qualitative research and reason from principles.)

Skip heuristics: skip Phase 2 when a lead-capture funnel already converts well; skip Phases 3-4 when a stranger already passes the five-second test on the message; skip Phase 6 when the offer converts and price is not an objection; skip Phase 7 when there is no naturally shareable asset and referral is not a realistic channel.

Then create `docs/GROW-WEBSITE-PLAN.md` from the template and confirm the plan. Done when `docs/GROW-WEBSITE-PLAN.md` exists with every phase statused and the user has confirmed the plan.

## Phases

### Phase 1 — Discover why visitors do not convert (cro-methodology)

**Purpose:** Replace guesses about why visitors leave with evidence, and turn it into a ranked test queue.

**Brief (fallback):** Don't guess, discover. Map the funnel to find blocked arteries (high-traffic
pages that drop off) and missing links. Research visitors on three axes: who they are, what blocks
them (UX), what stops them (objections). Build an Objection / Counter-Objection table in the visitor's
own words, place each counter at its point of friction, and inventory proof you have but do not show.
Queue bold experiments — not button colors — scored by ICE.

**Invoke:** `cro-methodology` with the primary conversion action, traffic numbers, and any research (exit surveys, support tickets, chat logs, reviews) from intake. Ask for a funnel map, an O/CO table sourced from real visitor language, an audit of the worst high-traffic page scored 0-10, and 3-5 ICE-scored experiment ideas with a hypothesis for the top two.

**Decide with the user:** (1) Which page is the blocked artery to attack first — highest traffic times worst conversion? (2) Is there enough research to source objections, or do we run exit surveys first (status awaiting-evidence)? (3) Which two experiments enter the queue — recommend the highest ICE that could plausibly double conversion, not a meek tweak.

**Artifact:** Extend docs/WEBSITE.md `## Audit Findings` and `## Conversion Elements` (the O/CO table with placement); docs/METRICS.md `## Funnel` (stages, drop-off, benchmark, bottleneck); docs/EXPERIMENTS.md `## Experiment Backlog` (ICE) and `## Experiment Cards` for the top two. Update the tracker.

**Done when:** the funnel is mapped with the blocked artery named, WEBSITE.md holds an O/CO table with counters placed at their friction point, and two ICE-scored experiment cards exist with pre-committed primary, secondary, and guardrail metrics.

### Phase 2 — Capture the 97% who are not ready to buy (scorecard-marketing)

**Purpose:** Keep the visitors who will not buy today with an interactive assessment instead of losing them at exit.

**Brief (fallback):** About 3% of a market is ready now; capture the rest. A scorecard or quiz
converts 30-50% versus 3-10% for a PDF. Four steps: a landing page built on the 3 Cs (Clarity,
Credibility, Connection); a questionnaire that captures the email before the questions, then 8-15
scored questions in 2-7 categories; a results page with dynamic content per tier that creates
tension between where the visitor is and could be; a follow-up engine segmented by score.

**Invoke:** `scorecard-marketing` with the audience and the primary conversion action. Ask for the concept hook (pressure-test several), the scored questions and their categories, the tiered results copy, the pre-question capture form, and tier-segmented follow-up emails.

**Decide with the user:** (1) The concept hook — pick a "moving toward" framing that taps the strongest dormant desire over a fear-based one. (2) How many tiers and where the score cutoffs sit. (3) Does an adequate capture funnel already exist, in which case skip?

**Artifact:** Extend docs/WEBSITE.md `## Lead Capture` (scorecard funnel design: hook, questions, tiers, capture-first form); docs/MARKETING.md `## Nurture Sequences` (the tier-segmented follow-up tracks). Update the tracker.

**Done when:** WEBSITE.md documents a scorecard that captures email before question one with dynamic results by tier, and MARKETING.md holds a separate follow-up track for each tier.

### Phase 3 — Make the message clear before clever (storybrand-messaging)

**Purpose:** Ensure a stranger can tell what you do, for whom, and why to care within five seconds.

**Brief (fallback):** Make the customer the hero and the brand the guide — Yoda, not Luke. Run SB7: a
Character who wants one thing; a Problem named at three levels (external, internal, philosophical —
sell to the internal); a Guide with empathy and authority; a 3-4 step Plan; a direct and repeated
Call to Action; the stakes of Failure; a picture of Success. Produce a one-liner: "We help [character]
who struggle with [problem] to [solution] so they can [result]." Clear beats clever.

**Invoke:** `storybrand-messaging` with the objections and proof inventory from Phase 1 — they are the raw material for the Problem and the Guide's authority — plus any existing positioning. Ask for a full brand script, a homepage hero rewrite, and 2-3 one-liner options.

**Decide with the user:** (1) Which internal problem to lead with. (2) Which one-liner a stranger could repeat after hearing it once. (3) The direct plus transitional CTA wording.

**Artifact:** Extend docs/POSITIONING.md `## Brand Script (StoryBrand)`, `## One-Liner`, and `## Key Messages` (surface | message | status). Update the tracker.

**Done when:** POSITIONING.md holds a completed brand script, a chosen one-liner, and key messages mapped to surfaces — and the hero passes the five-second test.

### Phase 4 — Make the message stick in memory (made-to-stick)

**Purpose:** Make the clear message memorable so a visitor who is not ready yet still recalls you when they are.

**Brief (fallback):** Apply SUCCESs: Simple, Unexpected, Concrete, Credible, Emotional, Stories. Beat
the Curse of Knowledge — replace jargon and abstraction with concrete, human-scale specifics ("orders
arrive in 30 minutes, still hot"; "saves 16 hours a month"). Lead with the counterintuitive thing,
not the expected one. Wrap the transformation in one specific customer's story: if I look at the one,
I will act.

**Invoke:** `made-to-stick` with the Key Messages and page copy from Phase 3. Ask for a Curse-of-Knowledge audit flagging every abstract claim, concrete rewrites with real numbers, and one flagship case study turned into a sticky story.

**Decide with the user:** (1) Which claims to make concrete first — the highest-traffic pages. (2) Which case study becomes the flagship story.

**Artifact:** Extend docs/POSITIONING.md `## Key Messages` with a `### Sticky Rewrites` subsection (concrete, de-jargoned versions), and docs/WEBSITE.md `## Page Briefs` copy blocks. Update the tracker.

**Done when:** every abstract claim on the priority pages has a concrete rewrite recorded, and one sticky customer story exists.

### Phase 5 — Add the proof and triggers that move people to yes (influence-psychology)

**Purpose:** Answer "why should I believe you?" and "why act now?" with placed, ethical persuasion.

**Brief (fallback):** Seven principles: Reciprocity, Commitment and Consistency, Social Proof,
Authority, Liking, Scarcity, Unity. For an existing site, social proof and authority usually carry
the most weight. Specific numbers beat vague claims ("2,347 founders" over "thousands"); similar-other
proof beats celebrity proof; admitting a small weakness before your strengths raises trust. Stack
several principles on the highest-value pages. Real numbers, real deadlines, real scarcity only.

**Invoke:** `influence-psychology` with the O/CO table and proof inventory from Phase 1. Ask for a principle-by-principle audit, a redesigned trust-signal section that stacks social proof plus authority plus genuine scarcity, and a micro-commitment rewrite of the signup flow — flagging anything that crosses into manipulation.

**Decide with the user:** (1) Which principles to prioritize by the objections research surfaced. (2) Which proof is real and displayable now versus which must be gathered. (3) Remove any fake scarcity currently on the site — confirm.

**Artifact:** Extend docs/WEBSITE.md `## Conversion Elements` (add proof and trigger rows with placement and status). Update the tracker.

**Done when:** WEBSITE.md's conversion elements stack real social proof, authority, and genuine scarcity at their point of friction, and no fake scarcity remains on the site.

### Phase 6 — Rebuild the thing you are actually selling (hundred-million-offers)

**Purpose:** Make the underlying offer irresistible before optimizing the page around it — the most upstream lever in the stack.

**Brief (fallback):** A Grand Slam Offer sells despite mediocre marketing. Value = (Dream Outcome
times Perceived Likelihood) divided by (Time Delay times Effort and Sacrifice) — raise the top, cut
the bottom. List every obstacle to the dream outcome and solve each; Trim and Stack (cut
low-value/high-cost, stack high-value/low-cost); add named bonuses that each kill an objection; attach
a risk-reversing guarantee; add ethical scarcity; name it with MAGIC. A strong guarantee reduces
refunds; raising price can raise conversion.

**Invoke:** `hundred-million-offers` with the current offer and price, and whether visitors call it "too expensive." Ask for a Value-Equation score, an obstacle list with a solution for each, named bonuses, a guarantee, and MAGIC name options.

**Decide with the user:** (1) Is "too expensive" a price problem or a value-perception problem? (2) Which bonuses and which guarantee to commit to. (3) Price and tier structure. (4) Queue the new offer as a bold experiment — a new offer is exactly what CRO says is worth testing.

**Artifact:** Extend docs/OFFER.md `## Offer Stack`, `## Tiers (Good / Better / Best)`, and `## Price Metric`; add a card to docs/EXPERIMENTS.md `## Experiment Cards` to test the new offer. Update the tracker.

**Done when:** OFFER.md holds a Grand Slam Offer (value equation, named bonuses, real guarantee, MAGIC name) and it is queued as an experiment card with pre-committed metrics.

### Phase 7 — Make visitors bring you more visitors (contagious)

**Purpose:** Turn each satisfied visitor into a source of new ones by design, not by luck.

**Brief (fallback):** Virality is engineered. STEPPS: Social Currency, Triggers, Emotion, Public,
Practical Value, Stories. A personalized scorecard result is high Social Currency — a remarkable stat
about themselves. Practical Value (a calculator, a genuinely useful resource) gets forwarded; frame
promotions with the Rule of 100. Public ("Powered by [you]", behavioral residue) markets after use.
Stories must pass the Trojan Horse test. Only ~7% of word-of-mouth is online — design things worth
talking about, not just share buttons.

**Invoke:** `contagious` with the scorecard results page from Phase 2 and the site's highest-value asset. Ask for a STEPPS audit scored out of 10, a shareable redesign of the results page with a share card that passes the Trojan Horse test, and Public / behavioral-residue features.

**Decide with the user:** (1) Which asset is the shareable one. (2) Which two or three STEPPS drivers to engineer in. (3) The share incentive — must be a real benefit, never a fabricated reward.

**Artifact:** Extend docs/MARKETING.md `## Word-of-Mouth (STEPPS)` and `## Referral & Invite Mechanics`; extend docs/WEBSITE.md `## Lead Capture` with the shareable results-page design. Update the tracker.

**Done when:** MARKETING.md's STEPPS table names the two-to-three drivers engineered in against a specific shareable asset, and the referral mechanics are documented.

### Phase 8 — Tie the lifecycle together so wins compound (one-page-marketing)

**Purpose:** Connect acquisition, nurture, conversion, and referral into one engine so wins do not leak out the back.

**Brief (fallback):** Marketing is a process, not an event. The 3x3 grid: BEFORE (Target Market,
Message, Media), DURING (Capture Leads, Nurture, Convert), AFTER (Experience, Lifetime Value,
Referrals). The AFTER column is usually where the money hides — retention costs 5-25x less than
acquisition, and a 5% retention gain lifts profit 25-95%. The number-one reason customers do not
refer is that nobody asked.

**Invoke:** `one-page-marketing` as an audit tying Phases 1-7 together — the scorecard fills Capture, the offer fills Convert, Contagious powers Referrals. Ask for the 9-square plan scored 0-10 per square, flagging empty AFTER squares, and a lead-nurture sequence at a 3-to-1 value-to-ask ratio.

**Decide with the user:** (1) Which empty squares to fill first — usually Experience, Lifetime Value, Referrals. (2) The ascension model for best customers. (3) Retention and LTV targets to track.

**Artifact:** Extend docs/MARKETING.md `## Target Market & Avatar`, `## Before / During / After Grid`, `## Referral & Invite Mechanics`, and `## Nurture Sequences`; extend docs/METRICS.md `## Baselines & Targets` (retention, LTV). Update the tracker.

**Done when:** MARKETING.md's Before / During / After grid has no empty AFTER squares, and retention and LTV targets are recorded in METRICS.md.

## Optional Phases

| Skill | Add when | Artifact |
|---|---|---|
| lean-analytics | growth work has no single metric keeping it honest | Extends docs/METRICS.md |
| high-perf-browser | slow pages bleed the traffic you already earn | Extends docs/WEBSITE.md |
| hooked-ux | return visits should become a habit loop | Extends docs/PRODUCT.md |
| ux-heuristics | friction, not persuasion, blocks the funnel | Extends docs/WEBSITE.md |

Optional phases follow the same operating rules; insert where the Add-when condition first becomes true.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Optimizing before researching | Run cro-methodology's visitor research first; change only what the evidence flags, not what a meeting brainstormed. |
| Testing meek tweaks (button colors) | Queue bold changes — a new offer, value prop, or full-page rewrite — ICE-score them, and run each to significance over a full business cycle. |
| Capturing email after the quiz | Fire the lead form before question one (scorecard-marketing) so an abandoned assessment still leaves you a lead to recover. |
| Faking scarcity or proof | Use only true numbers, deadlines, and testimonials; one fake claim (influence-psychology / hundred-million-offers) poisons every honest one after it. |
| Polishing the page while ignoring the offer | Rebuild the offer upstream with hundred-million-offers before more page tests; "too expensive" is usually a value-perception problem. |
| Ignoring the AFTER phase | Fill the empty Experience / Lifetime Value / Referrals squares with one-page-marketing — retention and referral are the cheapest growth there is. |

## Completing the Journey

Exit checklist:

- [ ] WEBSITE.md has an O/CO table with each counter placed at its point of friction, and audit findings resolved or queued.
- [ ] A scorecard captures email before the questions, with tier-segmented follow-up recorded in MARKETING.md.
- [ ] OFFER.md holds a Grand Slam Offer (value equation, named bonuses, real guarantee) queued as a bold experiment in EXPERIMENTS.md.
- [ ] MARKETING.md's Before / During / After grid has no empty AFTER squares (Experience, Lifetime Value, Referrals).
- [ ] At least one bold experiment is running to significance with pre-committed metrics.

Close the tracker: every phase `done` or `skipped: reason`, and any open Next Actions carried into the artifacts they belong to. Then route forward:

- When the growth loops belong inside the product, continue with `grow-app`.
- When the site is beyond saving and a rebuild is cheaper, continue with `create-website`.
