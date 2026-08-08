---
name: suede-copy
description: "Write conversion copy that earns the click: landing sections, email, microcopy, buttons, headlines, CTAs, variants, and anti-slop edits."
---

# Suede Copy

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


## When to use this skill instead of related skills
- **suede-copy** (this skill): standalone conversion email, landing page copy, CTAs, microcopy, button labels
- **johnny-suede-write**: full writing stack (copy + SEO + AI Engine Optimization)
- Multi-email campaign sequences and campaign performance reporting: (private Suede Labs companion, not in this pack: suede-growth)
- Post-production pass to strip AI writing patterns from already-written copy: (private Suede Labs companion, not in this pack: suede-deslop)

Write conversion copy, page copy, GitHub docs, email, and social posts that are specific, proof-backed, and free of AI boilerplate. Default voice: Suede. Supply a company brief to override everything.

**Core principle:** every claim is verifiable or it gets cut, and nothing ships below its score threshold.

## Company Brief

Supply a brief and all copy, voice, and claim logic applies to your company. Use natural language or this form:

```text
Company:
Product or offer:
Audience:
Voice:
Terms to use:
Terms to avoid:
Proof:
Allowed claims:
Forbidden claims:
Primary CTA:
```

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

## Core Rules

Name the outcome, not the feature.
- Weak: "Suede supports multiple metadata formats."
- Strong: "Export ISRC, ISWC, and split data in one command."

Write buttons as actions with a result.
- Weak: "Learn more"
- Strong: "Read how rights routing works"
- Weak: "Get started"
- Strong: "Register your first release"

Replace vague claims with artifacts.
- Weak: "Suede makes rights management easy."
- Strong: "Paste your folder path. Suede outputs your ISRC, split sheet, and licensing flags in under 10 seconds."

No invented proof. Do not write stats, testimonials, partner names, pricing, or legal clearance that has not been confirmed. If proof is unavailable, write around the gap or flag it for the human to supply.

No em dashes. No exclamation points. No rhetorical questions that answer themselves.

## Persuasion Frameworks

Match framework to surface and reader temperature:

- Reader arrives cold, no prior awareness: **AIDA** (Awareness → Interest → Desire → Action). Lead with the category problem, build specificity, make the outcome concrete, drive a single action.
- Reader has a named pain and is actively searching: **PAS** (Problem → Agitate → Solution). Name the problem, surface the cost of inaction, position the product as the specific relief.
- Hero section, social post, launch email: **Before-After-Bridge**. Describe life before the product, paint life after, bridge with the product as the mechanism.
- Product page, onboarding, in-app copy: **JTBD**. Write around what the reader is trying to accomplish: the job they hired the product to do, not around features.
- Homepage, About, long-form brand page: **StoryBrand 7-Part**. Character (customer) → Problem → Guide (your brand) → Plan → CTA → Avoid failure → Achieve success.

State the chosen framework and reader temperature before drafting. If multiple frameworks could apply, pick one and note why.

## Headline Formulas

Generate 3 headline candidates minimum for any hero or email subject. Pick the formula that matches the reader's state and the page's job.

| # | Formula | Structure | Example |
|---|---------|-----------|---------|
| 1 | Curiosity gap | [Intriguing partial claim] | "Most release folders fail the first licensing check. Here's why." |
| 2 | Number-led specificity | [#] [specific thing] [timeframe/condition] | "12 rights fields missing from your release. Suede finds them in 60 seconds." |
| 3 | How-to outcome | How to [achieve outcome] [without/with condition] | "How to package a release folder that licensing teams can actually use" |
| 4 | Because | [Result] because [mechanism] | "Agents can read your music rights because Suede structures the provenance first." |
| 5 | Specificity anchor | [Exact number or name] + [claim] | "47 fields. One linter. No guessing." |
| 6 | Before-After | [Before state] → [After state] | "Scattered files and a split sheet in a Google Doc → a machine-readable rights package" |
| 7 | Question (real, not rhetorical) | [Question reader actually asks] | "What does a licensing team check before they sign?" |
| 8 | Objection flip | [Common objection] + [reframe] | "Rights metadata sounds like legal work. It's a 10-minute audit." |
| 9 | If-then conditional | If [specific situation], then [specific outcome] | "If your release goes to a sync library, this is the metadata they'll reject first." |
| 10 | Direct claim with proof hook | [Bold claim] + [verifiable detail] | "Suede reads your folder. You get ISRC, split, and flags before you pitch." |
| 11 | Problem named exactly | [Specific failure mode the reader fears] | "Your ISRC is assigned. Your split sheet is a PDF. Neither is machine-readable." |
| 12 | Authority + specificity | [Who trusts this] + [for what exact task] | "The metadata structure sync licensing teams check on day one." |

Test: swap your product name for a competitor's. If the headline still works, it is not specific enough.

## Buyer Persona Modes

State the persona before writing. If multiple personas share a page, write the hero for the decision-maker and include practitioner proof in the secondary section.

**Decision-maker** (exec, founder, buyer)
- Lead: outcome and cost of inaction
- Proof: outcomes, not features ("Cut release prep from 3 days to 40 minutes")
- CTA: low-risk, high-clarity ("See the workflow" not "Transform your process")
- Skip: implementation details, CLI commands

**Practitioner** (developer, designer, operator)
- Lead: how it works, not why it matters
- Proof: commands, file paths, schema examples, error outputs
- CTA: direct action ("Run the linter" / "Fork the skill")
- Skip: ROI language, vague transformation claims

**Skeptic** (comparison shopper, previously burned)
- Lead: the objection, named directly ("Every tool claims to solve this. Here's what's different.")
- Proof: third-party verifiable, not internal ("Open the script. Read the output.")
- CTA: zero-pressure ("Read the code" / "Run it yourself")
- Skip: hype, superlatives, bold claims without evidence

**Creator / end-user** (non-technical)
- Lead: what changes for them, in plain language
- Proof: before/after in human terms ("Your release looks like this. After Suede, it looks like this.")
- CTA: lowest-friction path ("Try it with one release folder")
- Skip: technical vocabulary, command syntax, implementation framing

## Page And Docs Structure

For a page, README, or docs surface, build this spine:

1. **Hero:** one sentence that names the outcome.
2. **Subhead:** one or two sentences that add the audience, workflow, and proof.
3. **Primary CTA:** the action the reader can take now.
4. **Proof:** files, scripts, docs, screenshots, URLs, live routes, examples, or commands.
5. **How it works:** three or four steps, each with a verb and result.
6. **Safety:** what the workflow does not claim or do.
7. **FAQ:** direct answers for objections and search intent.
8. **Final CTA:** repeat the action with less friction.

For a small section, use only the pieces that fit.

## A/B Variant Generation

For high-stakes copy (hero headline, primary CTA, email subject, ad copy), always generate variants.

**Headlines**: 3 variants, different angles:
1. Outcome-led: what the reader achieves
2. Problem-led: what the reader escapes
3. Mechanism-led: what makes this different

**CTAs**: 2 variants minimum. See CTA Formulas below.

**Email subjects**: 3 variants:
1. Curiosity or benefit
2. Social proof or number
3. Direct question or challenge

Label each variant with its angle. Let the user pick rather than guessing.

## CTA Formulas

CTAs fail when they describe the button, not the outcome. Every CTA answers: "What happens the moment I click this?"

**Formula A: Verb + immediate result**
[Action verb] + [what they get or see right now]
- "Run the audit. Get your grade in 60 seconds."
- "Fork the skill. Live in your Codex in under a minute."
- "Paste your folder path. See your rights gaps."

**Formula B: Verb + object + benefit**
[Verb] + [specific object] + [value unlocked]
- "Register a release. Make it readable to licensing agents."
- "Install the skill. Audit any repo from your terminal."
- "Download the schema. Stop building it by hand."

**Formula C: Low-commitment framing** (skeptic / discovery stage)
[Passive discovery verb] + [what they'll see, not what they'll do]
- "See how rights routing works"
- "Read the spec"
- "Open the repo"
- "Watch a 90-second demo"

**Formula D: Stakes-aware framing** (decision-maker)
[Verb] + [outcome in their language]
- "Start the audit before the pitch"
- "Get the split sheet the label actually needs"
- "Ship the release with provenance attached"

**Anti-patterns to cut:**
- "Get started" (started what?)
- "Learn more" (more about what?)
- "Sign up" (for what, exactly?)
- "Try for free" without naming what they're trying
- Any CTA with an exclamation point

The 3-word test: describe what happens after clicking in 3 words. If you cannot, the CTA is too vague.

## Email Copy

### Subject Line Formulas

Subject lines win opens on three mechanics: curiosity, self-interest, or specificity. Pick one per subject line.

**Curiosity:**
- "[Specific thing most people miss]"
- "The [category] rule that [counterintuitive result]"
- "What happens when [specific scenario]"

**Self-interest:**
- "[Outcome] in [time] without [obstacle]"
- "How [audience segment] [achieved result]"
- "Your [specific thing] is [state]. Here's the fix."

**Specificity anchor:**
- "[#] [specific mistakes/fields/steps] in your [thing]"
- "[Exact name of thing]: [what it becomes]"

**Avoid:**
- Rhetorical questions ("Are you ready to take your music to the next level?")
- All-caps words
- "Re:" faking a reply thread
- Emojis in subject lines for B2B or technical audiences

### Preview Text

Preview text is a second subject line. Write it to add information, not echo the subject.
- Subject: "12 metadata fields your release is missing"
- Preview: "The ones sync libraries check before they respond."

Keep preview text under 90 characters. If the client truncates at 40, the first 40 characters must stand alone.

### Body Structure

```text
Hook (1-2 sentences): Name the problem or opportunity at the exact moment the reader is experiencing it.
Proof or evidence (2-4 sentences): Specific, not general. One example beats three claims.
Bridge (1 sentence): Connect the proof to the offer.
CTA (1 sentence + link): One action, one link. No secondary options in the primary CTA block.
P.S. (optional): Use for a single secondary offer or a time constraint. Not both.
```

**Unsubscribe-reduction:**
- Match email content to the opt-in promise. Topic or frequency drift is the primary unsubscribe driver.
- Segment before sending. A technical how-to sent to decision-makers who opted in for strategy reads as list mismanagement.
- Run a re-engagement sequence before suppressing inactive subscribers: three emails over 30 days (one value, one direct question, one break-up). Suppress non-openers after the sequence.

## Social Post Formats

### LinkedIn

**Hook line (first 2 lines before "see more"):**
The hook is the post. If the first two lines do not earn the click to expand, the rest does not matter.
- Works: specific observation, counterintuitive claim, single concrete number, named failure mode.
- Fails: vague industry wisdom, rhetorical questions, inspirational openers, "I'm excited to share."

**Post structure:**
```text
[Hook: one specific claim, observation, or question]
[2-4 line break]
[Insight or story: 3-6 short paragraphs, one idea each]
[Takeaway: what the reader does with this]
[CTA: one, low-friction. "What's your experience?" or a link, not both]
```

**Formatting rules:**
- Short paragraphs: 1-2 sentences maximum.
- No bullet lists longer than 5 items.
- One link maximum (in comments if the algo penalizes in-post links).
- 1-2 targeted hashtags maximum, placed at the end.

### X / Twitter

**Standalone tweet:**
```text
[Specific observation or fact] + [one implication or action]
```
Max 240 characters. If it reads like a self-contained thought from someone who knows something, it is working.

**Thread opener:**
```text
[Bold specific claim]

[Thread: number + what the reader gets]
"Here's how it works, step by step:"
```
The thread opener must be the strongest tweet in the thread. Do not save the best point for tweet 5.

**Reply to trend or news:**
```text
[Acknowledge the news in 1 sentence]
[Specific take from your vantage point]
[Optional: link to your related resource]
```

### Instagram

**Caption structure by content type:**

Product / feature reveal:
```text
[Name what it does in one sentence (the hook)]
[Why that matters for this specific audience]
[One specific proof point or use case]
[CTA in bio or link sticker]
```

Behind-the-scenes / process:
```text
[Name the specific moment or decision shown]
[What you learned or chose and why]
[Invitation: "What would you have done?"]
```

Testimonial / social proof:
```text
[Lead with the result, not the quote]
[Quote or paraphrase the proof]
[Bridge to your offer]
[CTA]
```

**Caption rules:**
- First line must read as a complete thought. Instagram shows 1-2 lines before "more."
- Hashtags go in the first comment or at the end after a line break. Never inside body copy.
- No more than 10 hashtags per post.

## Suede Voice

Use this register: confident, not breathless; technical enough for builders; clear enough for creators; polished, not corporate; specific, not cute; operator-grade, not brochure-grade.

Good Suede copy names what the reader controls: register a work, verify rights, route royalties, publish a claim, package a release folder, prepare licensing evidence, make a work readable to agents, compare provenance, ship a public skill page.

(For non-Suede work, supply the equivalent domain vocabulary in the company brief.)

## SEO And GitHub Copy

For GitHub repositories, skill docs, and Pages sites, treat SEO as the umbrella for search, AEO, and AI EO. Include:

- a search-ready title under 60 characters when practical
- a meta description under 160 characters when practical
- repo description under GitHub's practical limit
- 8-20 topic keywords if the repo surface supports them
- a first paragraph that repeats the durable entity names naturally
- answer-ready definitions, FAQ copy, and proof links that AI summaries can cite without inventing facts
- links to install docs, skill manifests, scripts, references, examples, live Pages, and source
- a safe evidence boundary

<!-- Suede defaults. Replace with equivalent for non-Suede work. -->
Suede durable keywords: Suede Creator Skills, Suede Rights Passport, Music Release Metadata Linter, Suedify, Suede Copy, AI EO, AEO, answer engine optimization, Codex skills, Claude Code skills, SKILL.md, music rights, creator rights, release readiness, provenance, royalty splits, licensing readiness, programmable IP, agent commerce, GitHub Pages.

Use keywords because they help the right reader find the page. Do not cram a keyword where a human would notice.

## SEO Audit Mode

For a deep, standalone SEO audit (technical access, keyword research, schema markup, E-E-A-T signals, topic cluster architecture, AI EO optimization, and scored visibility grades), use `$suede-seo-audit` instead.

When the copy workflow includes an SEO pass (metadata, structure, or copy quality only):

- **Metadata**: title, meta description, Open Graph, Twitter card, image alt, author/publisher, and durable entity names.
- **Structure**: one H1, useful H2/H3 hierarchy, FAQ fit, internal links, and descriptive anchor text.
- **Copy quality**: directness, proof, evidence boundaries, CTA clarity, trust language, filler, and Suede vocabulary fit.

## Anti-Slop Pass

Run this as a line-edit gate before delivery, not a vibe check.

### Word Substitution List

Make these swaps. Non-negotiable.

| Cut | Replace with |
|-----|-------------|
| utilize | use |
| leverage (as verb) | use, apply, run |
| seamless | remove or prove it: "no export step", "one command" |
| powerful | prove it: "processes 10k records in 4 seconds" |
| innovative | cut; name the innovation instead |
| revolutionary | cut entirely |
| game-changing | cut entirely |
| solution | name what it actually does |
| ecosystem | platform, system, toolchain (pick the accurate one) |
| empower | cut; say what the person now controls |
| unlock | cut; say what was blocked and is now accessible |
| streamline | speed up, cut the step, reduce from X to Y |
| intuitive | cut; prove it with a UX detail |
| robust | cut; name the specific capability |
| best-in-class | cut; or supply the benchmark |
| next-generation | cut; name what changed |
| cutting-edge | cut entirely |
| world-class | cut; or name the credential |
| end-to-end | name the actual start and end |
| holistic | cut; describe the scope instead |
| scalable | prove it: "handles X at Y load" |
| simple / simply / just / easy | cut or prove it with a step count |
| we believe / we think | cut; make the assertion directly |
| in order to | to |
| due to the fact that | because |
| at this point in time | now |
| going forward | cut; state the new behavior directly |
| synergy / synergistic | cut entirely |
| value-add | name the value |
| best practices | name the practice |

### Readability Gate

Aim for Flesch-Kincaid Grade Level 8-10 for B2B general audiences, Grade 6-8 for consumer audiences and onboarding, Grade 10-14 for technical/developer audiences where precision requires complexity.

Average sentence length under 18 words for consumer; under 22 words for B2B. Flag paragraphs over 4 sentences.

### Structure Gate

Rewrite:

- binary setup lines
- negative listing that defines the product by what it is not
- formulaic "not X, but Y" pivots
- false transformation arcs
- dramatic fragments
- rhetorical questions that answer themselves
- three-item cadence when two items work
- repeated punchy paragraph endings
- Wh-starter crutches when a direct actor and verb work better

### Actor Gate

Name who does the action. Prefer the creator, operator, buyer, agent, page, repo, workflow, file, command, route, or proof artifact.

- Weak: `The page converts traffic.`
- Better: `The page routes visitors to the audit, the proof link, or the build request.`
- Weak: `The market rewards provenance.`
- Better: `Licensing teams can inspect the provenance trail before they ask for the split sheet.`

### Rhythm Gate

- Keep one idea per sentence.
- Vary sentence length without using em dashes.
- Do not stack slogans where a concrete sentence would build more trust.
- Cut lazy extremes such as `always`, `never`, `everything`, and `nothing` unless the claim is literally true.

### Pull-Quote Gate

If a line sounds manufactured for a quote card, rewrite it with a real artifact, action, or proof point.

- Weak: `The future of creator ownership is here.`
- Better: `Suede turns a release folder into rights, provenance, split, and licensing evidence an agent can read.`
- Weak: `We're changing how music rights work.`
- Better: `Paste a folder path. Suede returns your ISRC status, missing fields, and a split-ready JSON file.`
- Weak: `Built for the next generation of creators.`
- Better: `A sync licensing team can open your release folder and read every rights claim without calling you.`

Score the copy before handoff:

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

Revise below 58/70. For public launch, homepage, GitHub, App Store, investor-adjacent, or public explainer copy, aim for 62/70 or higher.

## Output Shapes

### Page Copy

```text
Title:
Meta description:
Hero:
Subhead:
Primary CTA:
Sections:
FAQ:
Final CTA:
Safety note:
```

### GitHub Skill Copy

```text
Skill:
One-line description:
Reader:
Primary action:
Repo/Docs copy:
Install CTA:
SEO title:
Meta description:
Keywords:
Safety boundary:
```

### Copy Review

```text
Findings:
Rewrites:
Claims to verify:
Score:
Ready: yes | with caveats | no
```

## Red Flags — Stop

If any of these thoughts appear, stop and run the gate you were about to skip:

- "This draft is already clean, skip the word list." Run the substitution table anyway; slop hides in clean-feeling drafts.
- "It's only microcopy, no need to score it." Buttons and empty states get more reads than blog posts. Score everything that ships.
- "That stat is probably right." Probably is not proof. Cut it or flag it for the human.
- "The score feels like a 60." Score each dimension in writing or the total is fiction.
- "The client wants more energy." Energy fails the gate; specificity converts and still reads confident.

## Ship Gate

Recommend against shipping copy — and say why, leaving the call to the user — when:

- the primary action is unclear
- the page promises a feature the product does not implement
- proof is fake or unverified
- the copy hides a legal, payment, privacy, or release caveat
- the score is below 58/70, or below 62/70 for public launch, homepage, GitHub, App Store, or investor-adjacent surfaces
- the copy fails the competitor-swap test: swap in a competitor's name and it still reads true

End with the exact copy, not a long explanation of the copy.

## Progressive Calibration (say what worked / what missed)

Accept feedback at any point, not only after final handoff. When the user says what worked, preserve that pattern in the current pass and mirror it later. When the user says what missed, adjust immediately instead of defending the previous direction.

If the user says `cue suede`, asks for feedback choices, or seems to be calibrating mid-stream, pause at the next safe checkpoint and offer:
```text
Cue Suede:
1. Change something - tell me what to revise and I will adjust it.
2. Preserve this - tell me what worked so I can mimic it later.
3. Keep as-is - say nothing and I will treat it as accepted.
```
Do not block completion waiting for a `Cue Suede` answer. If the interface supports choice chips, use `Change something`, `Preserve this`, and `Keep as-is`.

## Routing

- Copy needs the full stack (SEO/AEO pass, multi-surface job, voice retune) → johnny-suede-write
- Copy ships inside a design build → johnny-suede-design (suede-design for token or component decisions)
- Words are done but the page still underperforms → suede-site-alchemy
- Public launch surface → suede-visibility-grader for the A-F grade before it goes live
