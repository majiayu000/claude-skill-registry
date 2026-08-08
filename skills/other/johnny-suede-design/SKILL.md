---
name: johnny-suede-design
description: "Design and write polished product surfaces people understand fast: landing pages, dashboards, campaigns, restyles, UI copy, and visual QA."
---

# Johnny Suede Design — The Any-Creatives Enchilada

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


This is the full design-plus-copy stack for building any creative surface, not just websites. Landing pages, brand surfaces, product UI, dashboards, campaigns, components, and creative projects all route through here. It classifies the surface, locks a visual direction, writes the words that carry it, renders and QAs the result, and can run the whole thing as a coordinated agent team when the build is big. Writing mode is ON by default: a surface is not finished until the copy pulls its weight.

This skill organizes and prepares creative work. It does not clear rights, confirm ownership, approve payouts, write to a registry, guarantee placements, or guarantee outcomes. It produces drafts, designs, tokens, plans, and QA evidence for a human to verify and ship.

## Core Job

**Core principle:** the job is a surface that feels specific, not polished-generic. The named company, product, or audience should be recognizable in every design decision before the logo loads. Work from live URL, source, and rendered screenshot. Never design from assumption when evidence is available.

Preserve the existing app framework, tokens, components, routing, and WIP unless the task explicitly asks for a larger rebuild. Prefer the existing icon library and component patterns. Add a new abstraction only when it removes real complexity or matches an established local pattern.

For Suede work, anchor design and copy in creator ownership, programmable IP, provenance, registry-backed media, royalty routing, licensing readiness, and agent commerce. Do not reduce Suede to a generic AI music app. For a supplied company, replace Suede nouns, proof, voice, and evidence boundaries with that company's brief. Do not use em dashes in public copy.

### Approved Suede S mark (hard gate)

For every Suede surface, deck, social card, icon, app asset, or branded output, use the exact approved mark at `docs/assets/suede-ai-logo-transparent.png` in `JasonColapietro/suede-creator-skills` (SHA-256 `83a7ee0317e4debe2e7b076c20ba067feb76a587f9e829dc6310ae4be4b44dfa`). Outside that checkout, use the same file from `https://raw.githubusercontent.com/JasonColapietro/suede-creator-skills/cbd192309580a32da375881e0eeb4b2450a554c2/docs/assets/suede-ai-logo-transparent.png`. Never redraw, trace, approximate, typeset, recolor, distort, or generate a replacement Suede S. `suede-skill-icon.png` is a Passport icon, not the Suede brand mark. If the approved file is unavailable or its checksum differs, stop and request the asset; omit the mark rather than improvise.

## Pick The Lane (Router)

This skill is the entry point. Name which lanes are active and why before starting. Never run all lanes by default.

- **Visual polish / design pass** on a surface, no copy or restyle needed → run **Lane A: Design** directly.
- **Copy or voice work only**, no layout changes → run **Lane C: Copy** directly. (Writing mode is on by default even inside a design pass.)
- **Reference → target restyle / adapt a site's look / "suedify"** → open with **Lane B: Suedify** to set the visual vocabulary, then Design and Copy lanes refine it.
- **Full redesign, launch surface, app build, or conversion-shaped work** → this skill orchestrates: run the Design Contract, then route lanes in parallel where safe.
- **Big, risky, cross-surface, release-bound, or "do it thoroughly" work** → **Lane D: Agent Teams** (see the multi-agent gate below — ASK first).
- **Unknown scope** → run the scout step, read the surface, then name the register and lanes before touching anything.

**Drop down instead of running this stack:** a design-token, dark-mode, or single-component decision with no copy and no build → run `$suede-design` directly. A writing job with no design or layout work → run `$johnny-suede-write` (or `$suede-copy` for one standalone conversion surface). A deck-only or HTML presentation job → use the private Suede Labs companion `power-design`. A broad UI/UX pattern lookup or framework-example search → use the private Suede Labs companion `ui-ux-pro-max`. Running the full enchilada on a one-lane job wastes the user's tokens and time.

**On-demand website companions (do NOT inline — run only when asked):** CRO/funnel work → `$suede-site-alchemy`; deep standalone SEO/AEO/AI EO audit → `$suede-seo-audit`; findability + first-screen + CTA + proof + AI-citation grade → `$suede-visibility-grader`; deep diff review of changes touching shared components, auth, payments, routing, analytics, or published-statement accuracy → `$suede-code-review` (`$suede-code-grader` for a blunt A–F grade). These are separate skills for website analysis. Reference them; do not paste their content here.

## Multi-Agent Gate (ASK First)

Because this enchilada can run a multi-agent team (Lane D), by DEFAULT it asks the user up front before spawning a fleet. Never silently spawn agents or max tokens.

> Run this as a multi-agent team (more thorough — scout, parallel builders, adversarial + consensus review, release lock, evidence handoff) or single-agent (faster, one pass)? Multi-agent mode may use slightly more tokens than most skills.

Default to single-agent for clear, contained work. Escalate to multi-agent when the user asks, or when the work is broad, risky, release-bound, or needs continuous quality gates. State the choice in the output before starting.

## Surface Classifier

Classify the surface before any design work starts. Misidentifying the register produces wrong tone, wrong density, and wrong motion posture.

| Register | Signal | Defaults |
|---|---|---|
| Brand | Homepage, about, campaign, press, portfolio, editorial | Highest typographic ambition, lowest density, motion earns premium feel, copy is declarative |
| Product | App UI, dashboard, settings, onboarding, tool, form, admin, workflow | Density serves task completion, motion clarifies state, copy is instructional |
| Docs | Reference, API, guides, changelog | Monospace hierarchy, zero decoration, copy is precise and scannable |
| Campaign | Launch, landing, offer, event | Conversion architecture first, proof stack above the fold, CTA is singular |
| Product listing / mobile | Screenshots, paywall, onboarding | Mobile clarity conventions, system-safe typography, no custom fonts in screenshots |

When the request spans registers (e.g., a dashboard with a marketing hero), name both and apply each register to its section.

When the surface is public, structure it for SEO, AEO, AI EO, Google, Gemini, and AI search with clear CTAs. When the surface is mobile, include screenshots, onboarding, paywall, responsive layout, and app-shell needs in the design pass.

## Minimum Signal Gate

Stop and ask only if none of these can be read from context:

| Required | Source |
|---|---|
| Target URL or file path | Supplied or inferable from repo |
| Primary action the surface must drive | Supplied or read from existing CTA |
| Register (brand / product / docs / campaign / mobile) | Inferable from surface type |
| Company or brand (for non-Suede work) | Supplied in brief or inferable from domain |

Everything else — tone, color direction, layout choices, copy angle — is a design decision. Make it, show the reasoning in the output, and let the user override. Do not ask about optional parameters before starting. If no brief and no explicit Suede context, ask for the company.

## Company Brief (Non-Suede Work)

Supply in natural language or as fields: Company / Product or offer / Audience / Category / Voice / Terms to use / Terms to avoid / Proof / Allowed claims / Forbidden claims / Primary CTA / Reference URLs / Assets or brand rules.

When a brief is active, replace all Suede positioning, domain language, and evidence boundaries with it. Keep the full workflow. Rename "Cue Suede" to "Cue [Company]" in the output.

## Read Current Truth First

Before any design, copy, or QA claim, read the surface context:
- Local `PRODUCT.md`: users, brand, tone, anti-references, strategic principles.
- Local `DESIGN.md`: color tokens, type scale, component inventory, spacing.
- `AGENTS.md`, `CLAUDE.md`, `AI_HANDOFF.md`, `README.md`, or task docs: agent guidance and surface context.

If `PRODUCT.md` or `DESIGN.md` is missing on a major surface, note it and proceed with available context. Offer to create them after completing the task.

Identify the surface: repo/folder, route, live URL, deployment target, branch, dirty files. Name the physical scene: who uses this, where, under what light, with what pressure, and what they need to do next. Inspect the current rendered UI at desktop and mobile breakpoints before making claims about quality.

Render the result for visual work — screenshots beat code inspection. Minimum: desktop at 1280px width and mobile at 390px or 375px width. For product screenshot sets, verify the required platform dimensions before generating assets. Verify live URLs or APIs before claiming public behavior.

To actually capture the render: `npx playwright screenshot <url> --viewport-size=1280,900 desktop.png` and `npx playwright screenshot <url> --viewport-size=390,844 mobile.png` (installs on first run with `npx playwright install chromium`), or your environment's built-in preview/screenshot tool if one is available.

For major design work, reusable systems, reference visual matching, product screenshot assets, or public launch surfaces, keep work open only after these are known: PRODUCT.md / product context status; DESIGN.md / design-system status; shape-brief status for net-new or large redesigns; source visual-target status when a mock, screenshot, Figma frame, or reference URL exists; rendered implementation status; ship-blocker status.

## Five-Gate Checklist (Major / Public / Launch Work)

For major public or launch work, apply all five before ship: **Copy Gate, Visual QA Gate, SEO/AEO/AI EO Gate, Design System Gate, Launch Gate.** Run each using the criteria defined in the relevant lane below.

---

# Lane A — Design (visual systems, laws, tokens, type, motion, QA)

Make any interface feel intentional, premium, legible, and alive without drifting into generic AI output. Covers product UI, brand surfaces, landing pages, dashboards, component systems, responsive polish, and visual QA.

## Task Router (within Lane A)

Choose the smallest path that fits the request.

- **Clear small fix:** inspect current UI, make the narrow edit, verify render, report what changed.
- **Ambiguous or net-new design:** gather context, propose 2–3 approaches with tradeoffs, recommend one, get approval before implementation.
- **Large redesign:** write a compact shape brief first — audience, page job, register, scene, color strategy, typography, layout, signature moment, constraints, QA plan.
- **Visual system work:** scan current CSS, tokens, components, spacing, shadows, breakpoints, icon usage, and repeated UI patterns before proposing changes.
- **Source-to-implementation QA:** if there is a mock, screenshot, Figma frame, or image target plus a rendered implementation, compare both visually before handoff and save `visual-qa-report.md` in the project root.
- **Long polish loop:** iterate through a visible checklist. If the same failure repeats, freeze the loop, reduce scope to the failing unit, and rerun with explicit acceptance criteria.

## Delivery Discipline

Do not call work done because the code changed. Call it done only when the done signal has been checked or the remaining gap is named. Use Lane D (agent teams) when several lanes must move at once (copy + layout + asset + implementation + QA). Run `$suede-code-review` before the ship gate when design work changes shared components, routing, auth, payments, analytics, release config, or published-statement accuracy. Skip both for a small visual or copy fix that can be inspected, patched, rendered, and verified directly.

## Suede UI Contract

Before a new surface, significant redesign, reusable component family, or design-system pass, lock the design contract before implementation:

- audience, surface job, primary action, and launch stage;
- spacing scale, grid behavior, breakpoints, and stable dimensions;
- color roles, semantic states, contrast requirements, and dark/light behavior;
- typography roles, hierarchy limits, body measure, and truncation strategy;
- copy vocabulary for buttons, empty states, loading, errors, and success;
- asset sources, logo use, crop rules, screenshot states, and motion rules;
- acceptance checks for desktop, mobile, accessibility, and rendered evidence.

If the work is purely backend or a narrow one-element fix, document only the relevant contract items instead of forcing a full spec.

## Design Laws (heads)

Read `references/design-laws.md` before implementing: it holds the full dark-mode token values, typography anti-patterns, fluid type scale CSS, layout and control rules, component laws (forms, modals, empty states, data tables, navigation) with BEFORE/AFTER pairs, motion timing specs, asset rules, the aesthetic-direction menu, the scoped-bans gallery with replacements, and the design-system artifact list. The heads below are the non-negotiables.

- **Subject first:** strip the logo; if the remaining visual could belong to a generic SaaS, a crypto exchange, or a music streaming app, the design has failed. Every surface answers: "What does a creator do here, specifically?"
- **One memorable move:** each major surface gets one subject-native signature element (rights ledger, waveform proof panel, chain-of-title timeline, live data rail, audit ledger). If it could appear on a competitor's site, replace it. Name it before implementation; keep the surrounding UI disciplined so it carries.
- **Color strategy before values:** commit to one — **Restrained** (tinted neutrals + one accent ≤10%; default for dashboards and tools), **Committed** (one saturated color carries 30–60%; default for brand pages; the ≤10% rule does not apply), **Full palette** (3–4 named roles; data viz and campaign pages), or **Drenched** (the surface IS the color; campaign heroes and launch moments). Avoid defaulting to Restrained for everything. Color encodes meaning (ownership, status, risk, tier, provenance); decorative color is waste. Reject the first-order reflex ("music tool → dark purple gradient") and the second-order trap (muted teal on dark). Prefer OKLCH; tint neutrals toward the brand hue; never pure #000 or #fff.
- **Dark mode is not an inversion:** surfaces at OKLCH L=12–24 stacked light-ward, border-based elevation instead of shadows, 7:1 body contrast, chroma reduced 15–25%, semantic tokens only. Values in the reference.
- **Typography:** contrasting display/body pairing with distinct jobs, minimum 1.25 scale ratio, 65–75 char body measure, letter-spacing 0, `clamp()`-based fluid type, no fixed px for display roles.
- **Layout:** structure explains the product; never a card where a row would do; a card inside a card means the IA is wrong; stable elements keep stable dimensions; the first viewport shows brand, offer, and a hint of the next section; text never clips at any viewport.
- **Motion by register:** brand earns motion, product motion clarifies state, docs get none, campaign motion only on hero or primary CTA. Animate `transform` and `opacity` only; ease-out-expo 220–280ms; always ship a `prefers-reduced-motion` variant.
- **Never ship** (signals that no design decision was made): decorative orbs, gradient-as-personality, icon-card grids as the entire page, fake metrics, unverified partner logos, or stock testimonials. Fake metrics, testimonials, and partner claims have no exception path: replace with a real stat plus source, a `[NEEDS REAL DATA]` placeholder, or a structural element that needs no number. Other banned patterns (gradient text, glass panels, side-stripe borders, hero-metric template, modal-first interactions) allow scoped exceptions for source fidelity, platform convention, accessibility, or a confirmed brand system — name why the exception is earned. Full gallery with replacements in the reference.

## Aesthetic Direction

For any new surface or significant redesign, commit to one named aesthetic direction before writing code: refined minimal, editorial, brutalist, retro-technical, organic, maximalist, luxury refined, or product-utilitarian (menu with execution notes in `references/design-laws.md`). Bold maximalism and refined minimalism both work; a design with no committed direction reads as generic.

**AI slop check** — run two reflex tests before committing: (1) could someone guess the theme and palette from the product category alone? Reject that first-order reflex. (2) Could someone guess the aesthetic family from category-plus-anti-references? That is the second-order trap. Go further.

**Theme sentence** — name the physical scene concretely enough that it forces the design answer ("a studio engineer reviewing a rights dispute at 2am on a secondary monitor"). If the sentence does not force the answer, add detail until it does. Dark vs. light is never a default.

## Design System Quality Of Life

For any major surface, reusable app shell, launch system, or important component family, produce the six artifacts listed in `references/design-laws.md` at the smallest useful fidelity: token map, state matrix, copy vocabulary, screenshot contract, accessibility pass, and migration notes. Extract a design-system issue when a pattern repeats three times or controls a high-visibility surface; classify the drift root cause.

For broad design-system audits, score:

```text
Color consistency: /10
Typography hierarchy: /10
Spacing rhythm: /10
Component consistency: /10
Responsive behavior: /10
Dark/light behavior: /10
Motion restraint: /10
Accessibility: /10
Information density: /10
Polish: /10
Total: /100
```

Below 70/100 the system is failing: fix the two lowest dimensions before styling new features on that surface. Any dimension at 4/10 or lower is a P1 finding.

## Visual QA Report (Lane A)

When comparing a source visual target against an implementation, save `visual-qa-report.md` with:
- source visual truth path or URL
- implementation path, URL, or screenshot
- viewport and state
- theme, auth state, content/data state, and interaction state
- full-view comparison evidence
- focused region comparison evidence, or why it was not needed
- findings ordered by P0/P1/P2/P3 severity
- patches made after the previous pass
- `final result: passed` or `final result: blocked`

Compare source and implementation in the same visual pass, not from memory. Render the implementation with `npx playwright screenshot <url> --viewport-size=1280,900 impl.png` (matching viewport to the source target), or your environment's built-in preview/screenshot tool if one is available. Check typography, spacing/layout, colors/tokens, image and asset fidelity, logos/icons, copy/content, loading/empty/error/hover/focus/active states, responsiveness, accessibility, and motion where relevant. Use `final result: blocked` when the source or rendered artifact is missing for a required comparison, or when actionable P0/P1/P2 issues remain. Use `passed` only when no actionable P0/P1/P2 findings remain.

---

# Lane B — Suedify (reference → target visual-DNA translation into tokens)

Use this lane when the user wants `reference_url -> target_url` (example: "Use apple.example and make suede.example look like it"). The output makes the target site inherit the reference's design logic, rhythm, hierarchy, and interaction feel while remaining legally and brand safe. This lane recreates design grammar with the target's own brand, content, product, and assets. It does NOT copy proprietary code, logos, exact copy, private assets, or trademarked identity, and it does not transfer the reference's claims, proof, pricing, or guarantees to the target.

Read `references/suedify-playbook.md` when this lane is active: it holds the full move set (Style Fingerprint, Token Distiller, Hero Lift, Section Rhythm, Voice Fingerprint, Copy Reframe, Asset Swap, Motion Match, Responsive Fit, Proof Stack, Screenshot Diff, Ship Polish), the DevTools capture procedure, and the DESIGN.md output template.

## Required Inputs
- `reference_url` (the site to study) and `target_url` (the site to transform). If either is missing, ask for it.
- Target source repo/folder/branch when implementation is expected. With no known source repo, inspect the target URL and produce `suedify-implementation-plan.md` instead of pretending edits can be applied.
- Optional depth (homepage only / key route set / full site / landing page / app shell / mobile / screenshot-only concept) and fidelity (inspired-by / close-visual-match / aggressive-restyle).

## Suedify Workflow

**Run to completion in one pass.** Do not stop to ask clarifying questions once a reference URL and target are known. If depth or fidelity is not specified, default to homepage + hero + primary CTA section, close-visual-match fidelity. State what you chose in the Ship Gate.

1. **Verify target and permissions.** Identify the exact target repo/folder before editing; never edit from a multi-repo container root. Run repo-local git status, remote, and recent log. Preserve user and other-agent WIP.
2. **Capture the reference.** Screenshots at desktop/tablet/mobile with named paths, plus the full capture list and motion-capture procedure in the playbook. Save the analysis as `DESIGN.md` in the target repo root. Capture command: `npx playwright screenshot <reference_url> --viewport-size=1280,900 reference-desktop.png` (repeat per breakpoint), or your environment's built-in preview/screenshot tool if one is available.
3. **Capture the target.** Matching widths, state, theme, auth/content, and interaction state. Identify what target content, assets, routes, and claims must remain. Mark dead links, broken layout, weak copy, missing assets, unverified claims.
4. **Make the translation map.** Map reference → target-safe equivalents (nav→nav, hero→hero, media→target-owned media, proof→target proof, CTA ladder→CTA ladder, motion→motion). Run Token Distiller; output the full `:root {}` CSS block.
5. **Implement.** Work inside the target's existing framework, tokens, routes, and component patterns. Update design tokens before one-off component styling when the restyle is broad. Keep content truthful to the target — a reference's claims do not become target claims.
6. **Render and compare.** Capture target screenshots at the same widths used for the reference; compare together in the same pass, not from memory; use focused crops for hero, nav, cards, forms, CTAs, icons, logos. Patch until the largest mismatches are fixed or named. Same capture command as step 2, run against `target_url` at matching viewport sizes, or your environment's built-in preview/screenshot tool if one is available.
7. **Verify and ship.** Run relevant lint, typecheck, test, build, or focused commands. Run `git diff --check` when files changed. Verify live URLs before claiming a public restyle. End with `ship`, `ship-with-caveats`, or `hold`.

## Fidelity Rules

The target MAY closely match: layout proportions, typographic scale and rhythm, color role structure, section pacing, navigation density, interaction feel, image crop strategy, product proof structure, and mobile composition.

The target MUST NOT copy: reference logos or trademarked marks, exact marketing copy, proprietary source code, private media or downloadable assets, fake partner/customer proof, or pricing/guarantees/metrics/claims that do not belong to the target.

If the user asks for an exact clone of a protected site, produce a close, target-branded interpretation instead and state the constraint briefly.

## Suedify Output Artifacts

Every suedify run produces `DESIGN.md` in the target repo root with all token fields filled from the reference extraction (template in the playbook). For multi-section work also produce `suedify-visual-qa.md`. For planning-only runs (no target repo), produce `suedify-implementation-plan.md`. Never produce empty or partially-filled token files — if a value cannot be extracted, record `UNKNOWN` with the reason.

## Suedify Ship Gate

```text
Reference URL:
Target URL:
Target source:
Fidelity level:
Depth:
Screenshots:
Changed:
Verification:
Unmatched reference signals:
Legal/brand caveats:
Status: ship | ship-with-caveats | hold
```

Use `hold` when the target cannot be edited, a live route cannot be verified, a primary layout breaks, copy claims are false, reference assets were copied unsafely, placeholder assets or CSS/div art replace real imagery without approval, nav/forms/CTAs do not work, mobile composition breaks, or the target no longer reads as its own brand.

---

# Lane C — Copy (writing mode, ON by default)

Write the words for what this skill designs: conversion copy, page copy, GitHub docs, email, and social posts that are specific, proof-backed, and free of AI boilerplate. Default voice: Suede. A company brief overrides everything. Writing mode is on by default — a surface is not finished until the copy carries it.

For a copy-only job with no design work attached, drop down to `$johnny-suede-write` (full writing stack) or `$suede-copy` (one standalone conversion surface) instead of running this lane inside the enchilada.

## Before Writing

Read available context first: `PRODUCT.md`, `README.md`, `AGENTS.md`, `AI_HANDOFF.md`, `DESIGN.md`, product/brand notes, task docs. If context is missing after reading, ask only for what blocks accurate copy: page or doc type; primary reader; one action the reader should take; product or skill being offered; proof safe to claim; claims/pricing/partners/metrics not approved; traffic source or publication surface.

## Core Rules

Name the outcome, not the feature.
- Weak: "Suede supports multiple metadata formats." Strong: "Export ISRC, ISWC, and split data in one command."

Write buttons as actions with a result.
- Weak: "Learn more" → Strong: "Read how rights routing works." Weak: "Get started" → Strong: "Register your first release."

Replace vague claims with artifacts.
- Weak: "Suede makes rights management easy." Strong: "Paste your folder path. Suede outputs your ISRC, split sheet, and licensing flags in under 10 seconds."

No invented proof — do not write stats, testimonials, partner names, pricing, or legal clearance that has not been confirmed. If proof is unavailable, write around the gap or flag it for the human to supply. No em dashes. No exclamation points. No rhetorical questions that answer themselves.

## Persuasion Frameworks

Match framework to surface and reader temperature. State the chosen framework and reader temperature before drafting. If multiple could apply, pick one and note why.
- Reader arrives cold, no prior awareness → **AIDA**. Lead with the category problem, build specificity, make the outcome concrete, drive a single action.
- Reader has a named pain and is actively searching → **PAS**. Name the problem, surface the cost of inaction, position the product as the specific relief.
- Hero section, social post, launch email → **Before-After-Bridge**. Describe life before, paint life after, bridge with the product as the mechanism.
- Product page, onboarding, in-app copy → **JTBD**. Write around the job the reader hired the product to do, not features.
- Homepage, About, long-form brand page → **StoryBrand 7-Part**. Character (customer) → Problem → Guide (your brand) → Plan → CTA → Avoid failure → Achieve success.

## Formula Banks

Read `references/copy-formulas.md` before drafting headlines, CTAs, email, or social copy inside a build: the 12 headline formulas with examples, buyer persona modes, the 8-part page/docs spine, A/B variant rules (3 headline variants, 2 CTA variants, 3 subject variants), CTA formulas A–D with anti-patterns, email subject/preview/body mechanics, per-platform social structures, the SEO/GitHub copy checklist with Suede durable keywords, the word substitution list, and pull-quote rewrites.

Two gates survive the summary: swap your product name for a competitor's — if the headline still works, it is not specific enough; and describe what happens after clicking in 3 words — if you cannot, the CTA is too vague.

## Suede Voice

Confident, not breathless; technical enough for builders; clear enough for creators; polished, not corporate; specific, not cute; operator-grade, not brochure-grade. Good Suede copy names what the reader controls: register a work, verify rights, route royalties, publish a claim, package a release folder, prepare licensing evidence, make a work readable to agents, compare provenance, ship a public skill page. (For non-Suede work, supply the equivalent domain vocabulary in the company brief.)

## Anti-Slop Pass

Run this as a line-edit gate before delivery, not a vibe check.

- **Word substitution gate:** apply every swap in the word substitution list in `references/copy-formulas.md` (29 entries). Non-negotiable, on every draft.
- **Readability gate:** Flesch-Kincaid Grade 8–10 for B2B general; 6–8 for consumer/onboarding; 10–14 for technical copy where precision requires complexity. Sentences under 18 words consumer, under 22 B2B. Flag paragraphs over 4 sentences.
- **Structure gate:** rewrite binary setup lines, negative listing, formulaic "not X, but Y" pivots, false transformation arcs, dramatic fragments, self-answering rhetorical questions, three-item cadence when two work, repeated punchy endings, Wh-starter crutches.
- **Actor gate:** name who does the action — the creator, operator, buyer, agent, page, repo, workflow, file, command, route, or proof artifact. Weak: "The page converts traffic." Better: "The page routes visitors to the audit, the proof link, or the build request."
- **Rhythm gate:** one idea per sentence; vary length without em dashes; no slogan stacks; cut lazy extremes (always, never, everything, nothing) unless literally true.
- **Pull-quote gate:** if a line sounds manufactured for a quote card, rewrite it with a real artifact, action, or proof point (examples in the reference).

## Copy Score (before handoff)

```text
Directness: /10
Rhythm: /10
Trust: /10
Specificity: /10
Authenticity: /10
Density: /10
Search/AI readability: /10
Total: /70
```

Revise below 58/70. For public launch, homepage, GitHub, product listing, investor-adjacent, or public explainer copy, aim for 62/70 or higher.

## Copy Output Shapes

**Page Copy:** Title / Meta description / Hero / Subhead / Primary CTA / Sections / FAQ / Final CTA / Safety note.
**GitHub Skill Copy:** Skill / One-line description / Reader / Primary action / Repo/Docs copy / Install CTA / SEO title / Meta description / Keywords / Safety boundary.
**Copy Review:** Findings / Rewrites / Claims to verify / Score / Ready: yes | with caveats | no.

## Copy Ship Gate

Recommend against shipping copy — and say why, leaving the call to the user — when: the primary action is unclear; the page promises a feature the product does not implement; proof is fake or unverified; the copy hides a legal, payment, privacy, or release caveat; the score is below threshold; or the copy fails the competitor-swap test. End copy-only requests with the exact copy, not a long explanation of the copy.

---

# Lane D — Agent Teams

For multi-agent orchestration, large cross-lane builds, WIP protection, RFC workflows, and rollback coordination: invoke **suede-agent-teams** with the full creative brief and context. It is the canonical source for multi-agent builds — do not duplicate its protocols here.

---

# House Process (applies across every lane)

## Workflow Spine (the repeatable order)

1. **Read current truth first.** Open the live URL or screenshot. Read the source route. Check dirty files, docs, and existing copy. Identify the surface type (brand, product, app, campaign, docs) — this determines tone density, motion posture, and layout defaults before any pixel moves.
2. **Shape the page job.** Decide what the surface must help the reader do.
3. **Lock the visual direction.** Choose layout, type, color roles, asset strategy, motion posture, and one memorable subject-native move.
4. **Write with the design.** Improve headings, buttons, body copy, empty states, errors, proof blocks, FAQ, SEO/AEO/AI EO, answer-ready summary, and product or mobile copy when relevant. (Writing mode is on by default.)
5. **Build narrowly.** Use existing framework, components, tokens, and icon library. Avoid unrelated refactors.
6. **Render and compare.** Check desktop and mobile, first viewport, text fit, spacing, states, accessibility basics, links, and visual balance.
7. **Run visual QA.** For source-to-implementation work, compare source visual truth and rendered implementation together, with matched viewport, state, theme, auth, content, and interaction conditions.
8. **Grade visibility (public surfaces).** Run `$suede-visibility-grader` when asked, or score findability, CTA pull, proof, AI readability, SEO strength, and design signal.
9. **Review and ship.** Run the relevant test/build/check commands, then hand off with evidence and caveats.

## Design Contract

Before major design work, name:
```text
Objective:
Surface:
Audience:
Primary action:
Register: brand | product | docs | campaign | app workflow
Reference URL or visual target:
Done signal:
Constraints:
Lanes:
```
For small polish work, compress to target, route, primary action, and done signal. For major design work, add: Source truth / Design brief confirmed / Render evidence / Reference/mock status / Design-system status / mobile product state coverage / Ship blockers.

## Surface Modifier Moves

Twenty named lenses (`/vibe-scan`, `/first-frame`, `/hero-voltage`, `/offer-spine`, `/cta-magnet`, `/trust-lacquer`, `/console-moment`, `/aeo-shine`, `/mobile-seduction`, `/link-sweep`, `/ship-polish`, and the rest) live in `references/surface-modifier-moves.md`. Read it when shaping or critiquing a surface and name the lenses you apply.

## Progressive Calibration (say what worked / what missed)

Accept feedback at any point, not only after final handoff. When the user says what worked, preserve that pattern in the current pass and mirror it later. When the user says what missed, adjust immediately instead of defending the previous direction.

If the user says `cue suede`, asks for feedback choices, or seems to be calibrating mid-stream, pause at the next safe checkpoint and offer:
```text
Cue Suede:
1. Change something - tell me what to revise and I will adjust it.
2. Preserve this - tell me what worked so I can mimic it later.
3. Keep as-is - say nothing and I will treat it as accepted.
```
Do not block completion waiting for a `Cue Suede` answer. If the interface supports choice chips, use `Change something`, `Preserve this`, and `Keep as-is`. (Rename to "Cue [Company]" when a company brief is active.)

## Boundaries (evidence requirements — preserve verbatim in spirit)

This skill organizes and prepares creative work. It does NOT clear rights, confirm ownership, approve payouts, write to a registry, guarantee placements, or guarantee outcomes.
- Do not expose private paths, credentials, secrets, tokens, unreleased assets, private repos, or private service details.
- Do not copy protected site assets, exact UI copy, proprietary source code, or trademarked identity when using the Suedify lane.
- Do not invent metrics, pricing, partner claims, testimonials, legal clearance, payout claims, registry writes, or release/distribution outcomes. No competitor product names.
- Do not mark work done until the stated done signal has been checked or the remaining caveat is explicitly named.
- Do not use em dashes in public copy.

## Output Shapes

For a design plan: Objective / Surface / Design direction / Copy direction / SEO-AEO-AI EO notes / Primary CTA / Proof stack / Implementation lanes / Verification.

For a finished pass (lead with findings; never name internal process steps like preflight, task router, or mutation in user-visible output):
```text
Simple explanation (plain, for a 10-year-old):
One plain paragraph a 10-year-old can follow — what we built or changed, and why it matters. No jargon.

Usual breakdown:
Changed:
Design QA:
Desktop/mobile screenshots or render notes:
Visual QA surfaces checked:
Visibility grades:
Design-system drift notes:
P0/P1/P2 blockers:
Copy/SEO QA:
Copy score (if copy shipped):
Verification:
Caveats:
Status: ship | ship-with-caveats | hold

Cue Suede:
1. Change something - tell me what to revise and I will adjust it.
2. Preserve this - tell me what worked so I can mimic it later.
3. Keep as-is - say nothing and I will treat it as accepted.
```

## Red Flags — Stop

If any of these thoughts appear, stop and run the check you were about to skip:

- "All lanes apply here, run everything." Name the active lanes and why; the enchilada never runs whole by default.
- "This build is big, spawn the team." Ask first. The multi-agent gate exists because silent fleets burn tokens.
- "The code reads right, so it renders right." Render it at desktop and mobile. Screenshots beat code inspection.
- "The design is done, the copy can slide." Writing mode is on by default; the surface is not finished until the copy carries it.
- "A placeholder metric is fine for the mock." Fake numbers ship unless they carry a `[NEEDS REAL DATA]` flag.
- "The reference is close enough from memory." Compare source and implementation in the same pass, never from memory.

## Ship Gate

`hold` when: a core user path is broken; rendered output contradicts the implementation; text overflows or truncates on any breakpoint; mobile layout is unintentionally stacked; any accessibility issue blocks the primary action; copy makes unsupported claims; the live surface cannot be verified; screenshots do not match implementation; or the live route cannot be verified.

`ship-with-caveats` is only valid when all P0 issues are resolved and remaining issues have a documented owner and timeline, and the caveat is explicit, non-critical, and acceptable for the launch stage. For public surfaces, recommend `hold` when the design gate passes while visual or accessibility blockers are open, and name those blockers so the user can decide. Findings lead, rationale follows. Name the file and line. For builds, state what changed and show the render evidence.

## Routing

- Design-token, dark-mode, or single-component decision only → suede-design
- Deck-only or HTML presentation generation → (private Suede Labs companion, not in this pack: power-design)
- Broad UI/UX pattern lookup or framework examples → (private Suede Labs companion, not in this pack: ui-ux-pro-max)
- Copy-only job → johnny-suede-write (suede-copy for one standalone conversion surface)
- CRO/funnel work → suede-site-alchemy; standalone SEO/AEO audit → suede-seo-audit; A-F page grade → suede-visibility-grader
- Shared components, auth, payments, routing, or analytics touched → suede-code-review
- Multi-lane coordinated build → suede-agent-teams; finished surface ready to publish → suede-launch-packaging
