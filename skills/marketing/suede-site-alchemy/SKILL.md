---
name: suede-site-alchemy
description: "Turn a page into a conversion path: hero, friction, proof, CTA, pricing, A/B ideas, quick wins, and mobile CRO."
---

# Suede Site Alchemy

## Gate policy — advisory, not blocking

Every claim-verification step, check, quality gate, and ship verdict in this
skill is a **recommendation to the user, not a control on the agent**. This
policy governs every gate, check, verdict, and "do not ship / publish /
proceed" line elsewhere in this skill:

- Run every check and report the results honestly. Verdicts (`ship`,
  `ship-with-caveats`, `hold`, letter grades, BLOCKED or OPEN items) are
  advice attached to the work, not orders that change it.
- Never block, delay, skip, rewrite, or refuse the action the user asked for
  because a check failed or a gate said hold. Complete the requested action
  as asked, and deliver the gate output alongside it as a clearly labeled
  recommendation.
- A failed gate changes what you report, never what you do.
- Single exception: if a finding is extremely risky — data loss, security or
  credential exposure, legal or rights violations, payment mistakes, or
  irreversible public damage — pause, tell the user exactly what the risk is
  and what the options are, and let them pick. Their choice is final.


**Core principle:** evidence before certainty. Diagnose friction, verify the
measurement, and turn design ideas into falsifiable hypotheses. Do not present
a heuristic, benchmark, or scenario as observed impact.

## Operating Stance

Use your company name, voice, and positioning throughout.

- Work from the live page and current source. Verify the exact repo, route, and
  git state before edits.
- For Promo/Sites work, position Suede as a brand growth platform: creator
  campaigns create demand; Suede Sites converts it with pages, SEO/AEO/AI EO,
  visitor signals, CRM follow-up, and campaign attribution.
- Module pricing without backing in current product docs or source is an
  extreme-risk claim: pause, show the user what is and is not authorized, and
  let them decide whether it publishes.
- "Sexy" means precise, visual, confident, and conversion-aware. Avoid vague
  hype, fake numbers, fake testimonials, and generic SaaS fog.
- For public pages, use the visibility grade when the page needs an A-F read on
  findability, first-screen clarity, CTA pull, proof, AI readability, and
  design signal.

## Delivery Contract

For a meaningful page, campaign, or conversion pass, define this before edits:

- objective: the one buyer action the page should earn;
- source truth: live URL, repo/folder, branch, route, and deployment target;
- done signal: local preview, desktop/mobile screenshots, CTA/link sweep, build,
  deploy readback, or live URL verification;
- constraints: claims, pricing, assets, and routes that are not approved;
- lanes: copy, layout, SEO/AEO/AI EO, assets, CTA plumbing, and QA. Run lanes in
  parallel only when they do not write the same files. Add a visibility grading
  lane when the page will be promoted publicly.

Use exact status words: inspected, changed locally, verified locally, deployed,
verified live, or blocked. Do not summarize a page as fixed until the stated
done signal has been checked.

## Page Contract

For a major page or campaign, lock this before implementation:

- buyer and one action the page must earn;
- offer spine, proof stack, CTA ladder, and route targets;
- visual system: type, color, spacing, imagery, motion, and mobile rhythm;
- SEO/AEO/AI EO target, title/meta angle, schema needs, answer-ready copy, and
  internal links;
- source-truth limits for pricing, claims, partners, metrics, and testimonials;
- acceptance checks: desktop/mobile render, link sweep, copy fit, accessibility,
  build, deploy readback, and live verification when public.

For a small page fix, use only the relevant contract lines and keep the edit
narrow.

## Scope Router

Handle as Suede Site Alchemy:

- Campaign landing pages.
- Launch pages.
- Link-in-bio or creator profile pages.
- Product microsites.
- Static site builds.
- SEO, AEO, or AI EO page upgrades.
- Conversion fixes tied to an active campaign.
- Suede Sites positioning, cross-sells, CTAs, and module menus.

Route to Suede's proprietary app-builder workflow:

- Open-ended custom apps.
- Backend systems.
- Auth, payments, data, or integration-heavy products.
- Dashboards, marketplaces, portals, mobile apps, or agent products.
- Long-lived engineering retainers.

When the request crosses that line, preserve the best landing-page work as the
front door, then route the build with copy like:

- "Build the campaign page now."
- "Open the Suede app-builder workflow."
- "Build the product with Suede."
- "Bring this into Suede's proprietary app builder."

Never invent a dead route. If the current repo does not expose an app-builder
URL, CTA to `https://suedeai.ai` or use the current verified Suede app route.

## Funnel Analysis

Map the page's role in the buyer journey before optimizing it. A page that serves the wrong funnel stage will fail regardless of CRO polish.

**TOFU (Top of Funnel — Awareness)**
Reader: doesn't know about the product yet. Needs: problem education, category definition, credibility signal.
Copy job: make the problem vivid, not the solution. Don't ask for commitment.
CTA: download, read, explore, learn.

**MOFU (Middle of Funnel — Consideration)**
Reader: aware of the problem, comparing solutions. Needs: differentiation, proof, objection handling.
Copy job: show why THIS solution, not just any solution. Comparison content, case studies, deep dives.
CTA: demo, trial, detailed docs, comparison guide.

**BOFU (Bottom of Funnel — Decision)**
Reader: ready to buy, looking for permission to pull the trigger. Needs: risk reduction, guarantee, testimonials, pricing clarity.
Copy job: remove friction and doubt. Urgency if genuine, guarantee if real, social proof from peers.
CTA: start now, get started, buy, talk to sales.

State the funnel stage before running any slash tool. Then optimize for that stage, not just for generic "conversion."

## Friction Audit

Count every source of friction on the page before fixing anything. A friction audit reveals WHERE the page loses visitors, not just that it does.

**Cognitive friction** (mental load):
- [ ] How many decisions does the visitor face before the primary CTA?
- [ ] How many value propositions compete on the first screen?
- [ ] Is the primary action obvious without reading?

**Physical friction** (effort):
- [ ] How many form fields before the first value delivery?
- [ ] How many clicks to reach the primary action?
- [ ] Does the mobile user have to scroll past the fold before seeing a CTA?

**Trust friction** (doubt):
- [ ] Is there a fear or objection that isn't answered before the CTA?
- [ ] Is the proof visible before the ask?
- [ ] Is the risk reversal (guarantee, cancel anytime, free trial) near the CTA?

Treat the friction list as an inventory, not a validated score. For each item,
record the affected population, evidence (analytics, replay, usability test,
support signal, or direct observation), severity, and the event that would show
improvement. A raw count does not prove impact.

**Mobile and accessibility checks (required for every public page)**

- Target size: meet WCAG 2.2 target-size requirements. Use at least 24×24 CSS
  pixels or compliant spacing for the minimum criterion; treat 44×44 as an
  enhanced house target, not a universal pass/fail rule.
- Text and zoom: test browser zoom, text scaling, reflow, and form focus on real
  mobile browsers. Do not disable pinch zoom to preserve a layout.
- CTA visibility: capture the first viewport and task path at representative
  device sizes. Test placement instead of assuming a fixed fold percentage or
  one universal thumb zone.
- Forms: request only data needed for the stated task, explain why sensitive
  data is needed, and measure field-level abandonment before attributing a
  numeric cost to any field.
- Overflow: test at narrow widths and large text. Fix the element causing
  horizontal overflow; do not conceal the defect with blanket
  `overflow-x: hidden`.

## Measurement and Decision Math

Before ranking hypotheses, define the decision and verify the event chain. Use
observed values from a named date range, population, and source. Leave a field
`unknown` when it is not measured; do not silently fill it with a generic
industry benchmark.

**Descriptive model:**
`observed_revenue = eligible_visitors × observed_CTA_rate × observed_close_rate × observed_order_value`

Use the model to locate leverage and instrumentation gaps. It is not a causal
forecast. If stakeholders need a planning range, show a sensitivity table with
each assumption labeled; call it a scenario, never an expected lift.

Before an A/B test, read `references/experiment-design.md` and create or copy
`assets/cro-hypothesis-ledger.csv`. Define the randomization unit, exposure,
primary metric, guardrails, data-quality checks, minimum detectable effect
(MDE), power, sample requirement, and stopping rule before launch. Treat MDE
as the smallest effect worth detecting, not the uplift the treatment is
expected to produce.

When reliable data is unavailable, request analytics exports or instrument the
funnel first. Validate event definitions, denominators, duplicate events,
consent effects, and bot/internal traffic before using the numbers.

## Slash Tools

Use slash tools as named design moves, not shell commands. Start with
`/vibe-scan`, then pick the smallest set that fits the page.

For the full menu, read `references/aesthetic-slash-tools.md` in this skill's
`references/` folder.

Default stack for a fast polish pass:

1. `/vibe-scan` - name the current feeling and the feeling the page should sell.
2. `/hero-voltage` - make the first viewport impossible to misunderstand.
3. `/offer-spine` - lock the page to one promise, one buyer, one action.
4. `/proof-stack` - turn trust from decoration into a conversion argument.
5. `/cta-magnet` - make the next click feel obvious and worth it.
6. `/mobile-seduction` - make the small-screen version feel composed, not
   collapsed.
7. `/ship-polish` - verify links, responsiveness, copy fit, and live behavior.

## Candidate Hypotheses

When the brief is only "make it convert better," inspect these common surfaces.
They are prompts for diagnosis, not a ranked list of guaranteed quick wins:

1. **Broken paths and measurement**: repair dead CTAs, validation traps, lost
   state, and missing or duplicate conversion events first.
2. **Hero clarity**: test a concrete buyer, outcome, and next action against the
   current version without introducing an unsupported promise.
3. **CTA specificity**: test an action-and-outcome label against a generic label.
4. **Proof relevance**: place verified proof near the claim or objection it
   supports; do not assume one fixed pixel distance or section.
5. **Form necessity**: remove or defer a field only when downstream operations,
   security, legal, and qualification needs still hold.
6. **Navigation focus**: test hierarchy and visual weight. Do not remove routes
   required for trust, accessibility, consent, or task completion.
7. **Pricing presentation**: test comprehension, total-cost clarity, plan fit,
   and cancellation terms; do not presume a pricing order or decoy wins.
8. **Mobile task path**: make the primary action discoverable without a sticky
   control obscuring content, consent, or platform UI.
9. **Image-copy alignment**: verify the visual demonstrates the same product,
   audience, and outcome as the copy.
10. **Performance**: measure field Core Web Vitals and key task latency; fix a
    confirmed bottleneck and monitor conversion and experience guardrails.

Prioritize by evidence strength, affected traffic, decision value, effort, and
risk. If impact is unknown, say so and design the measurement that will resolve
it.

## Workflow

1. Identify the surface: live URL, source folder, route, deploy target, current
   git branch, dirty files, and relevant handoff/spec docs.
2. Run **Funnel Analysis** — name the page's funnel stage (TOFU/MOFU/BOFU). Optimize for that stage throughout.
3. Run **Friction Audit** — inventory cognitive, physical, and trust friction,
   then attach evidence and severity. Fix launch blockers before visual work.
4. Read the page like a buyer. Capture the current offer, primary CTA, trust
   evidence, visual system, remaining friction points, and dead links.
5. Run the aesthetic slash tools. Keep the notes short and actionable.
6. Rewrite the page spine before touching components:
   - Headline: the sharpest promise.
   - Subhead: what changes for the buyer.
   - Primary CTA: the action that starts the workflow.
   - Secondary CTA: proof, demo, grader, or site/app routing.
7. Sharpen the visual system without redesigning it. For each surface type, "premium" means:
   - **Hero**: one dominant type weight, one color for the CTA, nothing competing at the same visual size.
   - **Social proof sections**: real photos over stock, real numbers over vague claims, name + title + company over anonymous quotes.
   - **Pricing/offer sections**: generous whitespace, price isolated in visual hierarchy, guarantee text printed adjacent to CTA not buried in footer.
   - **Mobile**: readable type, WCAG-compliant target size/spacing, tested CTA
     discovery, text scaling, and no unintended horizontal scroll.
   - **Motion**: motion clarifies state, respects reduced-motion settings, and
     does not block reading or interaction. Choose duration from context and
     test it rather than enforcing one universal threshold.
   Operate inside the existing color and type system. Introduce a new visual choice only when the current system has a direct conversion penalty.
8. Build the CTA ladder. Every page needs three exits:
   - **Primary action**: the one thing this page was built to earn. One button. Obvious placement. No competing CTA at the same visual weight.
   - **Secondary action**: proof, demo, or deeper content for visitors not ready to convert. Lower visual weight, same screen.
   - **Escape valve**: where does a visitor go when this page isn't right for them? Name the route (Suede: `https://suedeai.ai` after route verification; non-Suede: home, alternative product, or contact). A missing escape valve doesn't hold visitors — it loses them.
9. Verify like the page is already public:
   - Local preview.
   - Desktop and mobile browser QA.
   - Text fit and no overlap.
   - CTA/link sweep.
   - Visibility grade when public promotion or GitHub Pages discoverability is
     part of the ask.
   - `git diff --check`.
   - Live URL/API verification before claiming a production fix.
10. For any experiment, pre-register the ledger row, validate assignment and
    exposure, check sample-ratio mismatch (SRM) before interpreting outcomes,
    and report the effect estimate with uncertainty and guardrail results.
11. Recommended ship gate:
    - `ship`: page passes the done signal and no launch-critical gaps remain.
    - `ship-with-caveats`: only non-critical caveats remain and they are named.
    - `hold`: core CTA, visible layout, false claim, accessibility, build, or
      live verification is blocked.
12. Leave a concise handoff with target, files changed, commands, verification,
    caveats, and the exact next step.

## Worked Example

Read `references/evidence-boundary-worked-example.md` for a compact before/after pass.
Its "after" block is a set of hypotheses and proof slots, not publishable copy.

## A/B Test Hypothesis Generator

For any CTA, headline, or section that needs improvement, generate a testable
hypothesis before rewriting. Read `references/experiment-design.md` and copy a
row into `assets/cro-hypothesis-ledger.csv` before launch.

Format:
```
For [eligible population], if we change [specific element] from [control] to
[treatment], we hypothesize [primary metric] will change because [mechanism].
Randomization unit: [visitor, account, session, or other justified unit].
Guardrails: [harm metrics]. Data quality: [SRM, exposure, event health].
MDE: [smallest business-useful effect, not expected uplift].
Decision rule: [pre-registered rule using estimate, uncertainty, guardrails,
and operational constraints].
```

Examples:

```
For eligible new visitors, if we change the hero CTA from "Learn more" to the
verified action-and-outcome label, we hypothesize qualified CTA starts will
change because the treatment reduces ambiguity.
Randomization unit: visitor ID. Guardrails: completion rate, error rate, and
support contacts. Data quality: allocation, SRM, exposure, and event parity.
MDE/sample/duration: calculate from the observed baseline, business threshold,
alpha, power, traffic, and the chosen analysis plan before launch.
```

After the Friction Audit, generate at most three hypotheses. Rank them by the
quality of the underlying evidence, size of the affected population, decision
value, effort, and risk. Do not rank by invented projected lift. A directional
result is inconclusive until assignment, exposure, SRM, metric health,
uncertainty, and guardrails have been checked.

## Social Proof Framework

Match proof to the claim or objection it can actually support. Placement is a
testable design choice, not a universal conversion rule.

**Types and when to use:**

| Type | Best for | Example |
|---|---|---|
| Peer testimonials | Emotional objections ("will this work for me?") | Quote from someone with the same job title or problem |
| Case studies with metrics | ROI objections ("is this worth it?") | "Company X increased Y by Z% in N weeks" |
| Social numbers | Scale objections ("do enough people use this?") | "10,000+ creators", "4.9★ from 2,300 reviews" |
| Expert endorsements | Authority objections ("who says this is legit?") | Industry name, publication, or credential |
| Certifications / trust marks | Trust objections ("is this safe/legit?") | SOC 2, GDPR, security badges, app store ratings |

**Placement hypotheses:**
- Put peer testimony near the relevant audience or objection.
- Put case-study metrics where the methodology and source can be inspected.
- Put scale evidence near a scale claim, if scale matters to the decision.
- Put endorsements beside the claim they endorse and disclose material ties.
- Put certification or security evidence where a visitor assesses that risk.

Choose placement from user research and page context, then verify it with
usability evidence or a pre-registered experiment when the decision matters.

**Proof check**: every proof claim must be verifiable. Remove or rewrite vague claims like "used by thousands" without a number, "industry-leading" without a comparison, or "fast" without a metric.

## Pricing Psychology

For pages with pricing, optimize comprehension and informed choice before
persuasion. Verify currency, billing interval, taxes/fees, renewal, usage limits,
cancellation, refund terms, eligibility, and feature truth.

- **Order and emphasis**: anchoring can affect judgments, but it does not prove
  a particular plan order will improve qualified conversion or retention. Test
  order with revenue quality and cancellation/refund guardrails.
- **Plan architecture**: do not add a decoy or manufacture an "obvious" tier.
  Each plan must serve a real segment and remain understandable on its own.
- **Guarantee framing**: display only an approved guarantee and its material
  terms. Test placement; do not imply it is universally superior.
- **Gain/loss framing**: treat framing as a hypothesis. Never manufacture loss,
  scarcity, or a deadline, and monitor trust and post-purchase outcomes.
- **Trial/freemium**: choose from activation path, marginal cost, abuse risk,
  support load, retention evidence, and billing constraints. Measure downstream
  activation and retention, not signup rate alone.

## Scarcity and Urgency Framework

Urgency works when it is true. It backfires when the visitor realizes it's manufactured — trust recovers slowly.

**Ethical urgency (use):**
- Real deadlines: event date, price increase date, enrollment close date. State the date explicitly: "Price increases July 1" not "Offer ends soon."
- Real inventory: "4 spots remaining in the June cohort" when the cohort has a verified seat cap.
- Real time-sensitivity: early-access pricing that provably expires, seasonal promotions tied to actual calendar events.
- Behavioral triggers: "You've been looking at this for a while — here's the case study that usually answers the last question."

**Dark patterns (never use):**
- Countdown timers that reset on page refresh.
- "Only 3 left in stock" for digital products.
- "Offer expires tonight" when the offer is permanent.
- Implied scarcity with no mechanism: "limited slots" without a seat cap.
- Urgency language in automated email sequences with no actual deadline.

**Test:** Before adding urgency to a page, answer: "If a visitor waited 30 days and came back, would this urgency claim still be accurate?" If no — it's a dark pattern. Cut it or make the deadline real.

When genuine urgency exists, make the mechanism explicit. "This cohort closes July 1 because we cap at 20 students for live Q&A" is more persuasive than "Offer ends July 1" — it explains why the scarcity is real.

## Copy Bank

Starter fragments for when the page needs raw material fast. Every fragment is
raw input — run the anti-slop gate (no throat-clearing, fake intensity,
unsupported claims, passive actor-hiding, generic SaaS fog, or em dashes)
before any line ships.

Headline shapes:
- Name the buyer and the outcome: "Campaign pages that close the fans your drops create."
- One falsifiable promise: "Grade your brand page in 60 seconds."
- Kill the category label, state the change: "Your release, registered, routed, and ready to license."

Subhead starters:
- "Built for [specific buyer] who need [specific outcome] without [named cost]."
- "[Proof artifact] included — see exactly what you get before you commit."

CTA fragments (action + object, never "Learn more"):
- "Run the release audit" / "Grade my brand" / "Build the campaign page" /
  "Start the free trial" / "See the live demo"

For deeper copy work (formulas, frameworks, variants), route to `suede-copy`.

## Red Flags — Stop

If you catch yourself thinking any of these, stop and run the required step:

- "The page just needs visual polish." — Run the Friction Audit and render the
  current experience before deciding what kind of change is warranted.
- "This change feels high-impact." — Identify the evidence, affected
  population, primary metric, guardrails, and decision the evidence would
  change.
- "Urgency will lift conversions." — Only use truthful urgency, and treat any
  effect as a hypothesis with trust and post-purchase guardrails.
- "Source inspection is enough for visual work." — Render the page; check desktop and mobile.
- "I'll estimate their traffic to fill in the model." — Ask for analytics exports; never invent numbers.

## Output Contract

Close every meaningful conversion pass with this block:

```text
Surface: [URL or route + repo/branch]
Funnel stage: TOFU | MOFU | BOFU
Friction inventory: [items with evidence, affected population, and severity]
Changed: [files or sections touched]
Measurement readiness: [events/denominators/assignment/exposure verified or gaps]
Hypotheses: [1–3, prioritized by evidence, population, decision value, effort, risk]
Experiment plan: [primary metric, guardrails, MDE, sample/duration, SRM check, or not applicable]
Verification: [exact status words — inspected, changed locally, verified locally, deployed, verified live, blocked]
Caveats: [or "none"]
Ship gate: ship | ship-with-caveats | hold
```

## Routing

- Page needs an A-F promotion-readiness verdict → `suede-visibility-grader` before any paid or public promotion.
- Search, schema, crawl, or AI-citation depth → `suede-seo-audit`.
- Page converts and the release is ready to announce → `suede-launch-packaging`.
- Suede projects: multiple independent lanes, a campaign deadline, or SEO plus implementation plus QA → `suede-agent-teams`.
- Suede projects: work touches CTA plumbing, forms, auth, payments, analytics, API routes, deployment config, shared components, or claims that must match product behavior → `suede-code-review`.

Skip the extra gates for pure copy or layout polish after live/source inspection and rendered QA.

## Boundaries

- Do not reduce Suede to a generic AI music app.
- Do not hide creator/community services behind agency language.
- Do not blur `community`, `suede_studio`, and `brand_direct` fulfillment.
- Do not add pricing, guarantees, traffic claims, or visitor-ID percentages
  unless they already exist in the current approved source.
- Do not claim a CRO benchmark, prior, uplift, or revenue projection without a
  dated source, comparable population, metric definition, and clear label.
- Do not interpret an experiment before assignment, exposure, event health,
  sample-ratio mismatch, uncertainty, and guardrail checks pass.
- Do not stop at source inspection for visual work. Render the page.
