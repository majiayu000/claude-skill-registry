---
name: johnny-suede-write
description: "Write sharper Suede copy for docs, pages, email, social, headlines, CTAs, product listings, and public explainers."
---

# Johnny Suede Write

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


The writing enchilada. Route any writing request through one skill: long-form, short-form, GitHub and docs, social, email, product listing copy, brand-voice alignment, and public explainer talk-tracks. Default voice is the Suede house voice. A supplied company brief overrides everything.

**Core principle:** copy earns its place on the page with concrete nouns, buyer-visible outcomes, real proof, and one primary action. Nothing decorative, nothing invented.

## Pick The Lane (Router)

Read the request, then pick the lane. Most jobs are one lane; some chain.

| You want to... | Lane |
|---|---|
| Write or rewrite any copy surface from scratch | **Write Modes** (below) — pick the mode |
| Generate headlines, CTAs, or email subjects | **Headline Formulas / CTA Formulas / Variant Protocol** |
| Tune existing copy to sound like Suede, not generic AI | **Brand-Voice Alignment** lane |
| Hand a public user words to explain Suede to someone else | **Public Explainer Talk-Track** lane |
| Audit/review existing copy and return findings + score | **Copy Audit** output shape |
| Do a metadata/structure/copy-quality SEO pass alongside copy | **SEO And GitHub Copy** + **SEO Audit Mode** |

**Drop down instead of running this stack:** for a single standalone conversion surface (one email, one hero, one button set) with no SEO pass and no voice retune, run `$suede-copy` directly. When the copy ships inside a design or layout build, run `$johnny-suede-design`; its Copy lane applies these rules.

Cross-lane jobs (e.g. "rewrite the homepage, retune it to our voice, and give me social variants") run sequentially with shared context: write the surface, run Brand-Voice Alignment on it, then spin variants. State the chain you ran.

If the request is a full standalone SEO/AEO audit with a scored report, a landing-page-to-conversion-engine transform, an A-F page grade, a code grade/review, or a reference-URL restyle, those live in dedicated skills outside this writing enchilada (`$suede-seo-audit`, `$suede-site-alchemy`, `$suede-visibility-grader`, `$suede-code-grader`, `$suede-code-review`, `$suede-agent-teams`, `$suede-design`, or `$johnny-suede-design` and its Suedify lane for restyles). Route there and pass full context; do not reimplement them here. This skill owns the writing.

## Multi-Agent Default

If a job is large or risky enough to run as a coordinated agent team (for example a full launch package spanning many surfaces, or a writing job chained with audits and reviews across several skills), **ask the user up front before spawning anything**: "Run this as a multi-agent team (more thorough) or single-agent?" Never silently spawn a fleet. Note plainly that multi-agent mode may use slightly more tokens than most. For a single writing surface, just write it — no need to ask.

## Write Modes

Identify the mode before writing. Each mode has a different structure, length, and proof requirement. State the chosen mode in the output header.

**Long-form** (blog post, case study, whitepaper, README, docs page, product listing description)
- Lead with the outcome, not the topic.
- Structure: hook → problem → mechanism → proof → action.
- Minimum: H1, 2-3 subheads, one FAQ block, meta description, answer-ready summary.
- Score target: 62/70.

**Short-form** (tagline, hero headline, CTA, product description, social caption, onboarding screen)
- One concrete noun + one buyer-visible outcome + one verb. No filler.
- Deliver 3 variants at different lengths. Character counts matter for mobile, social, and ads — state them.
- Score target: 65/70 (density and specificity weighted higher).

**GitHub / Docs** (README, SKILL.md, API docs, changelog, contributing guide)
- First sentence: what it does, not what it is.
- Structure: one-line description → install → quickstart → reference.
- No marketing language in technical docs. Proof is code examples and working commands.
- Score target: 60/70 (authenticity and specificity weighted higher).

**Social** (Twitter/X, LinkedIn, Instagram, Discord, launch post)
- Open with the most specific claim or result, not the setup.
- No "excited to announce." No "thrilled to share." No em dashes.
- Deliver: main post + short variant + CTA + 3 hook variants.
- Platform structures and limits: read `references/email-and-social-formats.md`.

**Email / DM** (cold outreach, launch email, nurture, public explainer brief)
- Subject line is the headline. Write it last.
- Open with the reader's problem, not the sender's news.
- One ask per email. One CTA.
- Deliver: subject (3 variants) + preview text + body + CTA + P.S. line. Full mechanics: read `references/email-and-social-formats.md`.

## Before Writing

Read any available context files before asking questions: `PRODUCT.md`, `README.md`, `AGENTS.md`, `AI_HANDOFF.md`, `DESIGN.md`, product marketing or brand notes, task-specific docs.

If context is missing after reading, ask only for what blocks accurate copy:
- page or doc type
- primary reader
- one action the reader should take
- product or skill being offered
- proof that is safe to claim
- claims, pricing, partners, or metrics that are not approved
- traffic source or publication surface

## Company Brief

Supply a brief and all writing, voice, SEO, copy, and claim logic applies to your company. A supplied brief overrides the Suede default everywhere. Use natural language or this form:

```text
Company:
Product or offer:
Audience:
Category:
Voice:
Terms to use:
Terms to avoid:
Proof:
Allowed claims:
Forbidden claims:
Primary CTA:
Reference URLs:
Assets or brand rules:
```

When a company override is active: replace Suede positioning with the user's company, category, audience, proof, and vocabulary. Keep the full workflow intact. Map Suede-native concepts to the user's domain only when they fit. Rename `Cue Suede` to `Cue <Company>` in final feedback.

## Core Rules

Name the outcome, not the feature.
- Weak: "Suede supports multiple metadata formats."
- Strong: "Export ISRC, ISWC, and split data in one command."

Write buttons as actions with a result.
- Weak: "Learn more" → Strong: "Read how rights routing works"
- Weak: "Get started" → Strong: "Register your first release"

Replace vague claims with artifacts.
- Weak: "Suede makes rights management easy."
- Strong: "Paste your folder path. Suede outputs your ISRC, split sheet, and licensing flags in under 10 seconds."

No invented proof. Do not write stats, testimonials, partner names, pricing, or legal clearance that has not been confirmed. If proof is unavailable, write around the gap or flag it for the human to supply.

No em dashes in public copy. No exclamation points. No rhetorical questions that answer themselves.

## Persuasion Frameworks

Match framework to surface and reader temperature. State the chosen framework and reader temperature before drafting. If multiple could apply, pick one and note why.

- Reader arrives cold, no prior awareness: **AIDA** (Awareness → Interest → Desire → Action). Lead with the category problem, build specificity, make the outcome concrete, drive a single action.
- Reader has a named pain and is actively searching: **PAS** (Problem → Agitate → Solution). Name the problem, surface the cost of inaction, position the product as the specific relief.
- Hero section, social post, launch email: **Before-After-Bridge**. Describe life before the product, paint life after, bridge with the product as the mechanism.
- Product page, onboarding, in-app copy: **JTBD** (Jobs-to-be-Done). Write around what the reader is trying to accomplish — the job they hired the product to do, not the features.
- Homepage, About, long-form brand page: **StoryBrand 7-Part**. Character (customer) → Problem → Guide (your brand) → Plan → CTA → Avoid failure → Achieve success.

## Headline Formulas

Generate 3 headline candidates minimum for any hero or email subject, each from a different formula. Read `references/headline-and-cta-formulas.md` for the 12-formula bank with structures and examples (curiosity gap, number-led specificity, how-to outcome, because, specificity anchor, before-after, real question, objection flip, if-then, claim with proof hook, problem named exactly, authority plus specificity).

Gate: swap your product name for a competitor's. If the headline still works, it is not specific enough. Rewrite before scoring.

## Persona Mode

State the persona before writing. It changes vocabulary, proof type, and CTA framing. If multiple personas share a page, write the hero for the decision-maker and include practitioner proof in the secondary section.

- **Decision-maker** (exec, founder, buyer, investor): lead with outcome and cost of inaction in revenue/risk/time terms; proof is outcomes and named results, not features ("Cut release prep from 3 days to 40 minutes"); CTA low-risk and high-clarity ("See the workflow"); skip implementation details and CLI commands.
- **Practitioner** (developer, designer, operator, creator): lead with how it works, not why it matters; proof is commands, file paths, schema examples, error outputs; CTA direct ("Run the linter", "Fork the skill"); skip ROI language and vague transformation claims.
- **Skeptic** (comparison shopper, previously burned): lead with the objection, named directly ("Every tool claims to solve this. Here's what's different."); proof is third-party verifiable ("Open the script. Read the output."); CTA zero-pressure ("Read the code", "Run it yourself"); skip hype and superlatives.
- **Creator / end-user** (non-technical): lead with what changes for them, in plain language; proof is before/after in human terms; CTA lowest-friction ("Try it with one release folder"); skip technical vocabulary and command syntax.

Default to practitioner for GitHub/docs copy, decision-maker for sales/landing pages, and skeptic for competitive or comparison copy.

## Page And Docs Structure

For a page, README, or docs surface, build this spine. For a small section, use only the pieces that fit.

1. **Hero:** one sentence that names the outcome.
2. **Subhead:** one or two sentences that add the audience, workflow, and proof.
3. **Primary CTA:** the action the reader can take now.
4. **Proof:** files, scripts, docs, screenshots, URLs, live routes, examples, or commands.
5. **How it works:** three or four steps, each with a verb and a result.
6. **Safety:** what the workflow does not claim or do.
7. **FAQ:** direct answers for objections and search intent.
8. **Final CTA:** repeat the action with less friction.

## Variant Protocol

For any headline, CTA, subject line, or hero copy: generate 3 variants by default unless the user specifies otherwise. Label each variant, state which axis it targets, and recommend one. Let the user pick rather than guessing.

Variant axes: specificity (one abstract, one mid-spec, one hyper-specific with a concrete number or named proof); register (founder voice, product voice, skeptic-facing); length (long full thought, medium compressed, short one punch).

Per surface: headlines get 3 angles (outcome-led, problem-led, mechanism-led); CTAs get 2 variants minimum; email subjects get 3 (curiosity or benefit; social proof or number; direct question or challenge).

## CTA Formulas

Every CTA answers: "What happens the moment I click this?" Four formulas with examples live in `references/headline-and-cta-formulas.md`: verb + immediate result; verb + object + benefit; low-commitment framing (skeptic/discovery); stakes-aware framing (decision-maker).

Anti-patterns to cut: "Get started" (started what?); "Learn more" (more about what?); "Sign up" (for what, exactly?); "Try for free" without naming what they're trying; any CTA with an exclamation point.

Gate: describe what happens after clicking in 3 words. If you cannot, the CTA is too vague.

## Email And Social Formats

Read `references/email-and-social-formats.md` before drafting any email, DM, LinkedIn, X/Twitter, or Instagram copy: subject-line formulas, preview-text rules, the 5-part email body structure, unsubscribe-reduction sequence, and per-platform post structures with formatting limits.

Non-negotiables that survive the summary: write the subject last; one ask and one CTA per email; preview text adds information instead of echoing the subject; the first two lines of a social post are the post; open with the most specific claim, never the setup.

## Suede Voice

Use this register: confident, not breathless; technical enough for builders; clear enough for creators; polished, not corporate; specific, not cute; operator-grade, not brochure-grade.

Good Suede copy names what the reader controls: register a work, verify rights, route royalties, publish a claim, package a release folder, prepare licensing evidence, make a work readable to agents, compare provenance, ship a public skill page.

For Suede work, anchor public language in creator ownership, programmable IP, provenance, registry-backed media, royalty routing, licensing readiness, and agent commerce. Do not reduce Suede to a generic AI music app. (For non-Suede work, supply the equivalent domain vocabulary in the company brief.)

## Brand-Voice Alignment Lane

Use this lane to tune *existing* copy to the house voice without flattening it into generic AI product language. This is editing, not greenfield writing.

**Voice rules:**
- Lead with what the reader can do.
- Name concrete artifacts: skills, docs, scripts, reports, install commands, rights passports, provenance notes, split checks, QA checklists.
- Prefer creator ownership, programmable IP, rights, provenance, registry-backed media, royalty routing, licensing readiness, and agent commerce.
- Avoid vague "AI music app" framing.
- Avoid unsupported metrics, partner claims, legal clearance, payout claims, or guaranteed outcomes.
- Make CTAs verbs: install, audit, create, read, verify, open, package.

**Edit pass:**
1. Cut filler and throat clearing.
2. Replace broad claims with proof.
3. Make the primary action obvious.
4. Keep local-only details out of public headline copy.
5. Add an evidence boundary when rights, money, registry, or release language appears.

**Line-edit rules:**
- Name the actor. Use the creator, operator, buyer, agent, page, repo, command, workflow, route, or proof artifact instead of vague market or page agency.
- Put the reader in the room with a concrete artifact: rights passport, provenance note, split check, install command, QA checklist, screenshot, source link, release folder.
- Cut pull-quote slogans unless backed by a specific action or proof.
- Replace jargon with the thing the reader can inspect, click, ship, verify, or reuse.
- Avoid formulaic pivots, negative listing, Wh-starter crutches, fake intensity, lazy extremes, passive actor-hiding, and em dashes.

**Output of this lane:** the revised copy only, plus any claims that need verification. Do not append the full workflow scaffolding unless asked.

## Public Explainer Talk-Track Lane

Use this lane when a public user needs *words to explain Suede to someone else* — not to audit public copy or fix a failing install. Hype-free, evidence-backed, outcome-first. Use "explain" language, not "pitch" language.

**Explain:**
1. Start with the outcome: agents ship better public work with less setup.
2. Route the reader to the right lane: workflow skills, creator skills, MCP, design, copywriting, SEO/AEO/AI EO, artist campaigns, creator utilities, install docs, or copy bank.
3. Keep the language public-safe. Do not imply legal clearance, payout approval, distribution, registry writes, private service access, or guaranteed results.
4. Avoid internal implementation details unless the reader is installing or debugging.
5. Include one next action and one proof link.

**Formats:**
```text
One-liner:
DM:
Post:
Email:
FAQ answer:
Install explanation:
Evidence boundary:
```

## SEO And GitHub Copy

Discoverability is not optional. Every output gets an SEO title, meta description, H1, answer-ready summary, and FAQ candidates unless the format makes them impossible (DM copy, one-liner CTA). Run the full pass by default; skip only what the format cannot hold and state what was skipped and why.

For GitHub repositories, skill docs, and Pages sites, treat SEO as the umbrella for search, AEO, and AI EO. Include:
- a search-ready title under 60 characters when practical
- a meta description under 160 characters when practical
- repo description under GitHub's practical limit
- 8-20 topic keywords if the repo surface supports them
- a first paragraph that repeats the durable entity names naturally
- answer-ready definitions, FAQ copy, and proof links that AI summaries can cite without inventing facts
- links to install docs, skill manifests, scripts, references, examples, live Pages, and source
- a safe evidence boundary

<!-- Suede defaults. Replace with the equivalent for non-Suede work. -->
Suede durable keywords: Suede Creator Skills, Suede Rights Passport, Suede Release Linter, Suedify, Suede Copy, AI EO, AEO, answer engine optimization, Codex skills, Claude Code skills, SKILL.md, music rights, creator rights, release readiness, provenance, royalty splits, licensing readiness, programmable IP, agent commerce, GitHub Pages.

Use keywords because they help the right reader find the page. Do not cram a keyword where a human would notice.

## SEO Audit Mode

For a deep, standalone SEO audit (technical access, keyword research, schema markup, E-E-A-T signals, topic cluster architecture, AI EO optimization, and scored visibility grades), route to `$suede-seo-audit`.

When the copy workflow includes an SEO pass (metadata, structure, or copy quality only):
- **Metadata:** title, meta description, Open Graph, Twitter card, image alt, author/publisher, durable entity names.
- **Structure:** one H1, useful H2/H3 hierarchy, FAQ fit, internal links, descriptive anchor text.
- **Copy quality:** directness, proof, evidence boundaries, CTA clarity, trust language, filler, vocabulary fit.

## Anti-Slop Pass

Run this as a line-edit gate before delivery, not a vibe check.

### Word Substitution Gate
Apply every swap in `references/word-substitution-list.md` (29 entries: utilize→use, leverage→run, seamless/powerful/innovative/robust→prove or cut, and the rest). Non-negotiable, on every draft, including drafts that feel clean.

### Readability Gate
Flesch-Kincaid Grade 8-10 for B2B general audiences; Grade 6-8 for consumer/onboarding; Grade 10-14 for technical/developer copy where precision requires complexity. Average sentence length under 18 words for consumer, under 22 for B2B. Flag paragraphs over 4 sentences.

### Structure Gate
Rewrite: binary setup lines; negative listing that defines the product by what it is not; formulaic "not X, but Y" pivots; false transformation arcs; dramatic fragments; rhetorical questions that answer themselves; three-item cadence when two items work; repeated punchy paragraph endings; Wh-starter crutches when a direct actor and verb work better.

### Actor Gate
Name who does the action. Prefer the creator, operator, buyer, agent, page, repo, workflow, file, command, route, or proof artifact.
- Weak: `The page converts traffic.` → Better: `The page routes visitors to the audit, the proof link, or the build request.`

### Rhythm Gate
One idea per sentence. Vary sentence length without em dashes. Do not stack slogans where a concrete sentence would build more trust. Cut lazy extremes (`always`, `never`, `everything`, `nothing`) unless the claim is literally true.

### Pull-Quote Gate
If a line sounds manufactured for a quote card, rewrite it with a real artifact, action, or proof point. Weak: `The future of creator ownership is here.` Better: `Suede turns a release folder into rights, provenance, split, and licensing evidence an agent can read.` More weak/better pairs live in `references/word-substitution-list.md`.

## Evidence Boundaries

This skill organizes and prepares copy. It does not clear rights, confirm ownership, approve payouts, write to a registry, or guarantee outcomes. No competitor product names anywhere.

Allowed: founder-supplied facts, verifiable product behavior, documented integrations, public links, reproducible commands.

Remove: payout amounts not in a live contract, registry write times not benchmarked, rankings without a dated source, partner logos without a live integration, feature availability not yet shipped, any implication of legal clearance, payout approval, distribution, private service access, or guaranteed results.

When a claim is borderline, rewrite it as a testable behavior ("X happens when you do Y") rather than a superlative ("the fastest / the only / the first"). Add an evidence boundary whenever rights, money, registry, or release language appears.

## Workflow

1. **Pick the lane.** Use the router. Most jobs are one lane.
2. **Scout the surface.** Identify reader, page type, channel, primary action, proof, live/source URL, product or mobile context when relevant, and evidence boundaries.
3. **Identify register and persona.** Who is speaking (founder, product, docs, public explainer, technical operator) and the reader's relationship to the company (discovering, evaluating, already using). State the chosen register and persona mode in the output header.
4. **Set write mode.** Long-form, short-form, GitHub/Docs, social, or email. State it before writing.
5. **Write the outcome first.** Lead with what the reader can do, not a list of features. Apply the persuasion framework that fits the surface (AIDA, PAS, Before-After-Bridge, JTBD, or StoryBrand 7-Part). State which framework was applied.
6. **Build the proof stack.** Use real files, links, screenshots, commands, docs, installs, live URLs, or product artifacts. No invented proof.
7. **Run the discoverability pass.** Add SEO/AEO/AI EO title, meta description, H1, subhead, FAQ, answer-ready summary, internal links, schema notes, and app-store wording when relevant. Skip only what the format cannot hold; state what was skipped and why.
8. **Run the full anti-slop gate.** Word substitution list, readability gate, structure gate, actor gate, rhythm gate, pull-quote gate. No em dashes.
9. **Validate every statement.** Apply the Evidence Boundaries inline on every public output.
10. **Generate variants.** For any headline, CTA, or subject line, deliver 3 variants per the Variant Protocol. Label each; recommend one.
11. **Score before handoff.** See Score section. Revise before delivering if below threshold. Then package the output in the right shape and deliver copy that can be used directly.

## Output Shapes

For a page, docs surface, or launch asset:
```text
Register: [founder / product / docs / public explainer / operator]
Persona mode: [decision-maker / practitioner / skeptic / creator]
Write mode: [long-form / short-form / GitHub-Docs / social / email]
Persuasion framework: [AIDA / PAS / Before-After-Bridge / JTBD / StoryBrand]

Title:
Meta description:
H1:
Subhead:
Primary CTA:
Sections:
FAQ:
Answer-ready summary:
Final CTA:
Evidence boundaries:
```

For social, email, or public explainer copy: Register / Persona mode / Main copy / Short version / CTA / Proof links / Subject variants (email: 3 options) / Evidence boundaries.

For GitHub skill copy: Skill / One-line description / Reader / Primary action / Repo-Docs copy / Install CTA / SEO title / Meta description / Keywords / Safety boundary.

For a copy audit:
```text
Findings:
Rewrites:
SEO/AEO/AI EO upgrades:
CTA upgrades:
Claims to preserve:
Claims to avoid:
Copy score:
Ship gate: ship | ship-with-caveats | hold
```

## Score Before Handoff

Score every public output before handoff. Revise anything below 58/70. Public launch, homepage, product listing, GitHub, investor-adjacent, and public explainer copy must reach 62/70. State the score and the two lowest dimensions; fix those first.

```text
Directness: /10
Rhythm: /10
Trust: /10
Specificity: /10
Authenticity: /10
Density: /10
Search/AI readability: /10
Total: /70
Two lowest dimensions: [name them]
Revised: yes / no
```

## Red Flags — Stop

If any of these thoughts appear, stop and run the gate you were about to skip:

- "This draft is clean, skip the word list." Run it anyway; the gate exists because clean-feeling drafts hide slop.
- "The mode is obvious, no need to state it." Stating mode, persona, and framework is what keeps the structure honest.
- "It's one button label, skip the score." Microcopy ships to more readers than the blog post.
- "That claim is close enough." Close enough is invented proof. Cut it or flag it.
- "The user is in a hurry, deliver without variants." Variants are the deliverable for headlines, CTAs, and subjects.

## Ship Gate

Recommend against shipping copy — and say why, leaving the call to the user — when:
- the primary action is unclear
- the page promises a feature the product does not implement
- proof is fake or unverified
- the copy hides a legal, payment, privacy, or release caveat
- the score is below 58/70, or below 62/70 for public launch, homepage, product listing, GitHub, investor-adjacent, or public explainer surfaces
- the copy fails the competitor-swap test: swap in a competitor's name and it still reads true

## Routing

- One standalone conversion surface, no SEO pass → suede-copy
- The surface needs design or layout work too → johnny-suede-design
- Full standalone SEO/AEO audit → suede-seo-audit; A-F page grade before launch → suede-visibility-grader
- Copy approved and ready to publish as a release → suede-launch-packaging

## End of Work

At the end of meaningful work, end with the simple explanation, then the breakdown.

```text
Simple explanation (plain, for a 10-year-old):
[One plain paragraph a 10-year-old can follow: what you wrote, who it's for, and what it now gets them to do. No jargon.]

Changed:
Verification:
Caveats:
Status:

Cue Suede:
1. Revise something — tell me what to change and I will adjust it.
2. Preserve something — tell me what worked so I can match it.
3. Accept as-is — say nothing and I will treat it as approved.
```

End with the exact copy, not a long explanation of the copy.
