---
name: suede-marketing-plan
description: "Suede-affiliated comprehensive marketing planning across acquisition, activation, retention, referral, and revenue, sized to the actual team, budget, evidence, and stage. Use when the user needs a 90-day plan, 12-month roadmap, growth plan, or go-to-market operating document. NOT FOR: isolated channel execution (use the relevant public Suede skill), uncommitted tactic brainstorming (use suede-marketing-ideas), or positioning discovery alone (use suede-product-marketing)."
---

# Suede Marketing Operating Plan

Suede produces a comprehensive marketing operating plan across Acquisition, Activation, Retention, Referral, and Revenue. Build the 12-month plan from the client's verified budget, team, stage, evidence, constraints, and public Suede execution routes, then cross-reference the `suede-marketing-ideas` library and embedded 17-section current-state rubric.

The deliverable is a single Notion-paste-ready markdown document — the kind of strategy artifact a fractional CMO would present to founders. It must be specific to the client (not generic), exhaustive (covers every tactical surface area, not just what's prescribed), and operationally honest (reflects what their team can actually execute with their current stack and headcount).

## When to use

Invoke this skill when:

- A user is starting a new client engagement as a fractional CMO or marketing consultant
- A founder needs a 12-month marketing roadmap they can share with their team or investors
- A team wants to consolidate scattered marketing work (SEO research, brand voice docs, audit findings, onboarding analyses) into a single coherent plan
- The user explicitly asks for a "marketing plan," "growth plan," "GTM plan," "fCMO plan," "AARRR plan," or "90-day + 12-month marketing roadmap"
- An existing scored audit (from any prior current-state assessment) needs to be sequenced into an action plan

**Do not use** when the user wants a tactical execution document for a single channel (use the channel-specific skill instead — `suede-emails`, `suede-ads`, `suede-seo-audit`, `suede-onboarding`, etc.), or when the user just wants marketing ideas without commitment to a plan (use `suede-marketing-ideas`).

## How this skill is invoked

```
/suede-marketing-plan {client-name-or-domain}
```

Examples:
- `/suede-marketing-plan quietude.app`
- `/suede-marketing-plan acme-saas`
- `/suede-marketing-plan` (will prompt for client name)

On invocation, the skill reads `.agents/suede-marketing-plans/{client-slug}/progress.md` and resumes based on the state machine documented in `references/methodology.md` Step 1.1.2 (fresh → INIT → REVIEW → FINALIZE → finalized). Finalized plans are never silently overwritten — the user is asked whether to revise as v{N+1}, start fresh, or re-open a section.

## The three phases

The full workflow lives in `references/methodology.md`. Quick summary:

### Phase 1 — INIT (research + intake)

Read all available materials about the client. Pull data from any wired tools (Ahrefs, GA4 MCP, Stripe MCP, etc.). Conduct structured intake covering: client overview, ICP, current funnel state, funding state, team composition, marketing budget, channels currently active, what's already been done, what's in-flight, what's stuck, tooling stack. Save to `research.md`.

Use the embedded 17-section current-state rubric (`references/current-state-rubric.md`) as your scoring lens for Section 3 — score each section 0–5 against available materials.

### Phase 2 — REVIEW (walk through each of 13 sections interactively)

Present each section's draft in chat. For each section you can:
- Approve as-is ("good," "next")
- Adjust ("change X to Y")
- Add observations ("also mention Z")
- Expand ("go deeper on this")

Persist each confirmed section with the recoverable write-intent transaction in
`references/methodology.md`: record section number and content hash, promote
`sections/NN.md`, reconcile its checkbox/artifact/current-section/timestamp
metadata, verify, then clear the intent. If interrupted, run
`/suede-marketing-plan client-name` to reconcile the intent before continuing.

### Phase 3 — FINALIZE (compile + verify + publish)

Compile all 13 sections into `final_plan.md`. Run a verification pass: confirm `suede-marketing-ideas` idea numbers, public Suede routes, and named integrations are accurate; check for machine-specific paths that should not ship; ensure the brand voice matches what was captured in the strategic frame.

Optionally offer to publish to a shared GitHub repo (e.g., `{client-org}/{client-context}/marketing/plan.md`) if the user wants to share it with the team.

## The 13-section plan structure

Full template lives in `references/plan-template.md`. The structure:

1. **Executive summary** — 3 big bets, 90-day priorities, 12-month outcome. Written so it can be lifted into an investor or board update.
2. **Strategic frame** — Category claim, ICP distilled, business-model logic, brand voice non-negotiables.
3. **Current state** — Team, budget, what's done, what's in-flight, what's stuck. Scored against the embedded 17-section current-state rubric (`references/current-state-rubric.md`).
4. **Acquisition** — How strangers become aware. Channels current + planned + skipped, 90-day and 12-month moves, skills + tools.
5. **Activation** — How a new user has an experience that converts. Onboarding, first session, App Store / signup, paywall, lifecycle setup.
6. **Retention** — How a converted user stays and deepens. Lifecycle flows, churn prevention, win-back, support-as-marketing.
7. **Referral** — How retained users bring more users. Ambassador / affiliate / Guides / WOM mechanics.
8. **Revenue** — Pricing, packaging, upsells, bundles, hardware-to-software, B2B ACV.
9. **90-day roadmap** — Weeks 1–2 (Unblock), 3–4 (Foundation), 5–8 (Velocity), 9–12 (Compound). AARRR-tagged, owner-assigned.
10. **12-month outlook** — Quarterly decision checkpoints tied to verified resource, evidence, owner, and approval conditions.
11. **Marketing operations stack** — Available marketing skills and authorized integrations mapped to each AARRR stage, owner, review gate, and fallback.
12. **Tactical idea bank** — All 139 ideas from `suede-marketing-ideas` cross-referenced to AARRR + an evidence-based status: Current / Approved test / Conditional / Deferred / Skip.
13. **Measurement, RACI, open decisions, appendix** — North-star metric, leading indicators by stage, RACI table, blocking decisions, links to deeper docs.

## The AARRR framing

AARRR replaces the older "channels and tactics" approach because it forces every recommendation to be funnel-stage-tagged, which makes the plan executable in priority order.

Full primer in `references/aarrr-framework.md`. Quick rule:

- **Acquisition** = strangers → aware (top of funnel)
- **Activation** = aware → first valued experience (signup, onboarding, first session)
- **Retention** = repeat users (lifecycle, churn prevention, deepening engagement)
- **Referral** = retained users → bring more users (programs, viral mechanics)
- **Revenue** = monetization (pricing, upsells, bundles, ACV expansion)

Brand and content are **cross-cutting**, not their own AARRR stage — they serve every stage.

## The current-state rubric

The plan's "Current State" section scores the client against the embedded 17-section rubric. Full rubric in `references/current-state-rubric.md` — it's the source of truth, not a derivative of any external skill.

If the user already has a separately scored audit, preserve it as dated
evidence and reuse only scores whose sources, scope, cohort/window, and
definitions still match the current state. Otherwise, score from current
materials using the rubric's evidence gate; mark unsupported rows `Unknown`.

## Cross-references — skills this plan integrates with

1. **`suede-marketing-ideas`** — 139 proven marketing tactics. Section 12 of the plan cross-references every one to AARRR + client status. Detail in `references/idea-cross-reference.md`.
2. **`suede-product-marketing`** — Sets up the foundational `.agents/product-marketing.md` context file (positioning, ICP, voice). Read this first; Section 2 (Strategic frame) builds on it.
3. **AARRR-stage-specific skills** — `suede-onboarding`, `suede-signup`, `suede-emails`, `suede-referrals`, `suede-pricing`, etc. The "Marketing operations stack" (Section 11) maps these to AARRR stages.

The plan is **opinionated about which skills serve which stages.** Full mapping in `references/ops-stack-mapping.md`.

## The marketing operations stack

This is the differentiator of an fCMO-style plan vs. a generic marketing plan. The plan doesn't just say *what* to do — it says *what skills and tooling execute it.*

The public Suede skill pack and verified integrations can make approved workflows more repeatable for a small team. The plan must show the stack explicitly, AARRR-stage by AARRR-stage, without claiming that tooling replaces headcount or guarantees throughput; capacity still depends on the client's data, owners, review process, and operating constraints.

Full mapping in `references/ops-stack-mapping.md`.

## Conditional capability unlocks

Every plan must explain what changes when budget becomes available, but funding
stage alone never determines spend or hiring. Use
`references/funding-stage-unlocks.md` as a question set. Derive each unlock from
verified cash, runway, board-approved burn, measured acquisition capacity,
current owners, and category constraints.

## Setting the budget with traceable assumptions

Use the client's dated finance and funnel inputs to build scenarios, then have
the accountable finance owner approve the maximum spend, review date, and stop
conditions. Full limitations live in `references/budget-planning.md`:

1. **Capacity-based** — start from the approved cash/runway ceiling and measured
   channel capacity; model an outcome range.
2. **Goal-based scenario** — work backward from a target using sourced ARPC,
   retention, gross margin, blended CAC, and delivery capacity. Treat the result
   as a sensitivity model, not a forecast or funding recommendation.

Do not append a universal experiment percentage or stage-based growth multiple.
The accountable owner chooses a bounded test amount the company can lose without
breaching runway.

## Growth patterns — the real shape of SaaS growth

Use `references/growth-patterns.md` to compare linear, step-function, and layered
curve hypotheses against dated client evidence. ARR and funding stage are
context, not universal phases. The plan must name uncertainty, capacity, review
dates, and stop conditions rather than promise a curve.

## Team and agency model

Use `references/team-and-agency-model.md` to map outcomes, current owners,
capacity, access, risk, and duration before choosing an employee, contractor,
agency, automation, or deferral. Do not infer the first hire, title, vendor type,
or outsource ratio from stage or company size.

## What every plan must customize

A generic plan is a failed plan. Every plan must explicitly customize for:

1. **Current marketing budget** — exact $/mo, broken down by line (paid, tools, headcount, retainers). Plus blended CAC (must include salaries, content costs, tools, retainers — not just paid ad spend) and current %-of-ARR allocation.
2. **Unit economics** — ARPC, annual retention rate, LTV. These feed the budget math in Section 8 and Section 10.
3. **Team composition and surface area** — every person who touches marketing,
   their outcome, capacity, skills, access, and approval boundary.
4. **What the client is currently doing** — by channel, with status (working / not / TBD).
5. **What they've already done that should be acknowledged** — past launches, PR moments, content, partnerships. Don't write a plan that ignores work they're proud of.
6. **Observed growth pattern** — evidence for linear, step-function, or layered
   behavior, plus uncertainty and the current constraint.
7. **Conditional capability milestones** — the exact evidence, resources,
   approval, and stop conditions that would unlock a hire, channel, or vendor.
8. **The marketing skills mapped to specific moves** — every move in the AARRR sections names the skill that executes it.
9. **The execution method and access state** — every move names its owner, current capacity, manual or tool-assisted method, review gate, and fallback. A tool is optional and never evidence that hiring is unnecessary.

If you can't confirm any of these in INIT, list them in Section 13's "Open decisions" — never gloss over them. **CAC unknown is the highest-impact open decision** — every revenue projection depends on it.

## Common client-type variations

Plan structure stays consistent, but a business-model label does not select
channels, spend, cadence, or staffing. Use `references/client-types.md` to ask:

- Which dated funnel evidence identifies the current constraint?
- Which audience, intent, or behavior evidence makes a channel test plausible?
- Which cohort economics and delivery constraints bound the exposure?
- Who owns the work, approval, review date, and stop decision?
- Which legal, platform, claims, consent, or rights gates apply?

Treat every archetype pattern as a candidate to verify, not a default to copy.

## Quality bar

What separates a good plan from a generic one:

**Good plan signals:**
- Every move names the AARRR stage it serves
- Every recommendation is anchored in real client data (their actual budget, their actual team, their actual current channels)
- The 90-day roadmap has owners, not just actions
- Conditional capabilities name the verified resource, evidence, owner, approval, review date, and stop conditions required to unlock them
- The ops stack section names specific skills + MCPs per move
- The idea bank shows what we're *not* doing and why (skipped ideas with rationale)
- The exec summary can stand alone — could be lifted into an investor update
- Open decisions are explicit, not glossed over

**Failure modes to avoid:**
- Listing tactics without sequencing
- Recommending things the team can't execute at current size
- Pretending paid budget, channel readiness, or approval exists before current
  evidence and an accountable decision confirm it
- Glossing over uncomfortable metrics (e.g., churn) instead of naming them as open decisions
- Generic language ("build a community," "improve SEO") without specific moves
- Ignoring brand voice — every plan section must respect the client's voice rules
- Padding the plan with skills/ideas the client doesn't actually need
- Not acknowledging work the team has already done

## Output format

The final deliverable is a single markdown file: `.agents/suede-marketing-plans/{client-slug}/final_plan.md`.

Headers (`## 1. Executive summary`, etc.) are H2 for clean Notion paste. Tables for any structured comparison (RACI, idea bank, ops stack). Status legend for the idea bank. Internal references to other sections use `§N` (e.g., "see §5 for Activation detail").

Length expectation: ~8,000–12,000 words for a comprehensive plan. Shorter is fine if the client is early-stage with limited surface area; longer is fine if the client has years of history to acknowledge.

## File layout per plan

```
.agents/suede-marketing-plans/
└── {client-slug}/
    ├── materials/         # Client-provided files (decks, audit output, brand-voice doc, etc.)
    ├── research.md        # Research record written during INIT
    ├── progress.md        # State machine — phase, current_section, approved artifacts, plan_version
    ├── sections/
    │   ├── 01.md          # Each approved section saved as a canonical artifact
    │   └── ...            # Zero-padded so they sort in order
    └── final_plan.md      # Compiled deliverable (FINALIZE output)
```

The full schema for `progress.md` and the resumption decision tree live in `references/methodology.md` Steps 1.1.1 and 1.1.2.

## Related skills

- **`suede-product-marketing`** — Run first. Captures positioning, ICP, voice in `.agents/product-marketing.md` so every section of the plan references the same foundation.
- **`suede-marketing-ideas`** — Source of the 139 tactics in Section 12.
- **`suede-customer-research`** — Deepens the ICP and voice-of-customer inputs that feed Section 2 (Strategic frame).
- **`suede-onboarding`** — Deep work on Section 5 (Activation).
- **`suede-emails`** — Deep work on Section 6 (Retention) + onboarding emails in Section 5.
- **`suede-referrals`** — Deep work on Section 7 (Referral).
- **`suede-pricing`** — Deep work on Section 8 (Revenue).
- **`suede-seo-audit`** / **`suede-programmatic-seo`** — Deep work on the SEO portion of Section 4 (Acquisition).
- **`suede-ads`** / **`suede-ad-creative`** — Deep work on an approved paid test after evidence, tracking, creative capacity, exposure, review, and stop gates pass.
- **`suede-launch-packaging`** — Deep work on launch moments inside Section 4 / Section 9.

## Task-specific questions (used during INIT)

The full intake questionnaire lives in `references/methodology.md`. The most important questions:

1. **Financial context** — What cash, runway floor, approved burn, commitments, financing conditions, and decision dates constrain the plan? A round label is context only.
2. **Team** — Who are all the people who touch marketing? What does each own? Where are the gaps?
3. **Budget** — What's the current monthly marketing spend, broken down by paid acquisition, tools, retainers, and headcount? What exact evidence, capacity, approval, maximum exposure, review date, and stop conditions govern any increase?
4. **Current channels** — Which dated source, cohort, metric definition, and
   attribution window support "working," "not working," or "unknown"? Which
   untried channel hypotheses have audience evidence and an approved test?
5. **Already done** — What past campaigns / launches / content / PR moments should this plan acknowledge?
6. **In-flight** — What's drafted but not shipped? What's blocking each item?
7. **Tooling stack** — What's wired? Customer.io / Mailchimp / Resend? Shopify / Stripe / App Store Connect? GA4 / Mixpanel / Amplitude? GitHub / Notion / Figma?
8. **Beta or GA?** — If product is in beta, what's the GA timeline? Throttling? What gates exist?
9. **The most important thing to fix this quarter** — founder's read.
10. **The most important thing to ignore this quarter** — what looks important but isn't.

## How exhaustive should the plan be?

Default to comprehensive. Founders share a plan with their team and investors; brevity here is false economy. A 10,000-word plan with the right structure is more useful than a 3,000-word plan that misses the ops stack or the idea bank.

That said: don't pad. Every section should be **dense, not bloated**. If a
section has nothing to say, write that explicitly — "Deferred — no approved
test or owner in the current planning window" is honest and useful.

## A note on tone

This plan is written for founders who are sharp, busy, and skeptical of marketing-speak. Write like a thoughtful colleague, not a deck-slide-writer. No jargon for jargon's sake. Direct claims, named tradeoffs, explicit assumptions. When unsure, name the open question rather than guessing.

The exec summary should be short enough to read in 60 seconds. The rest should reward deep reading.

## Boundaries

- Do not invent market evidence, customer research, budget, team capacity, conversion data, funding, or implementation status.
- Do not publish a plan, allocate spend, contact vendors, create campaigns, or change operating systems without explicit authorization.
- Do not present forecasts, comparators, scenarios, or conditional capabilities
  as guarantees.
- Do not decide legal, financial, hiring, brand-risk, or executive trade-offs when the required owner has not approved them.

## Routing

- Use `suede-product-marketing` for positioning and `suede-customer-research` for voice-of-customer evidence.
- Use `suede-marketing-ideas` for a wider option set and `suede-marketing-loops` for approved recurring operations.
- Use `suede-onboarding`, `suede-emails`, `suede-referrals`, or `suede-pricing` for lifecycle execution.
- Use `suede-seo-audit`, `suede-programmatic-seo`, `suede-ads`, or `suede-ad-creative` for acquisition execution.
- Use `suede-launch-packaging` for the launch moment.
