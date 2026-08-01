---
name: kai-brand
description: Brand positioning workshop — define messaging framework, voice/tone, differentiation strategy, and taglines. Use when "brand positioning", "messaging framework", "brand voice", "how should we position ourselves", "differentiation", "tagline", or any request to define or refine brand identity and messaging.
---

# /kai-brand — A Position Only This Brand Can Claim

## Objective

A brand positioning system the team can write from tomorrow: a positioning statement anchored in white space no competitor owns, three value-prop pillars with proof, voice and tone rules with do/don't examples, a differentiation map against named competitors, and a shortlist of taglines with the reasoning for each.

The white-space call is the load-bearing judgment. A position every competitor could also claim is a description, not a position.

## Done when

Work type `strategy-plan` — floor **E3/C3/O1** (`harness/eco-floors.yaml`).

- **E3** — a named human approved the exact messaging document.
- **C3** — `banned_word_check` clean on every deliverable, Four U's ≥ **12/16** on the positioning statement (`python scripts/quality_gates/four_us_score.py <file>`), and someone other than the author read the package end to end.
- **O1** — the package names the first asset that will be rewritten against it (site hero, sales deck, ad set) with an owner and a date. Positioning nobody rewrites anything with is not finished.

## Constraints

- **Read `MARKETING.md` from the project root first.** It carries product, ICP, value prop, monetization, voice, current channels, and competitive landscape. If it does not exist, build it from the codebase — CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, email/ad/analytics config — using the template from `/kai-email-system`, and confirm the draft. Do not ask the user what the product is.
- **Five things must be known before positioning anything:** what the product does and who it serves, the current positioning or tagline if one exists, the top three competitors, what actually makes this brand different (founder story, technology, approach, audience), and which harness persona(s) the audience maps to.
- **If a URL is provided, fetch and analyze the live site messaging** before proposing new messaging, and name the gap between what the market says and what the user believes.
- **Every claim must be substantiable.** No empty superlatives.
- **Taglines are under 8 words.**
- **Zero Tier 1 banned words and zero AI slop phrases** — enforced by `python scripts/quality_gates/banned_word_check.py <file>` on new copy, and flagged where they already appear in the brand's existing copy.
- Positioning that cannot survive a competitor saying the same sentence does not ship.

## Context

| Need | Load |
|---|---|
| Positioning method, white space, category choice | `knowledge/playbooks/brand-positioning.md` |
| Audience personas and their language | `knowledge/personas/_persona-index.md` |
| Perception, context, and permission layers for messaging | `knowledge/frameworks/content-copywriting/perception-engineering.md` |
| Product, ICP, competitors, current voice | `MARKETING.md` (project root) |

**Deliverables and their shape:**

- **Messaging framework** — positioning statement in the form *For [audience] who [need], [product] is the [category] that [key benefit] because [reason to believe]*; three value-prop pillars, each a headline plus a supporting proof point; an elevator pitch in a 30-second and a 10-second version.
- **Voice and tone guidelines** — three voice attributes stated as tensions ("Direct, not blunt"), do/don't examples for each, and how tone shifts across website, email, social, and support.
- **Differentiation map** — a table of Feature / Us / Competitor A / B / C, with the winning rows marked and the losing rows flagged rather than hidden.
- **Taglines** — 10 candidates scored on memorability, clarity, and differentiation; top 3 recommended with the reasoning.

The competitive landscape gets mapped before any of this: who claims what position, and which positions nobody owns. Existing messaging is scored against the Four U's — Unique (can only this brand say it), Useful (does it promise a clear outcome), Ultra-specific (are there concrete details), Urgent (is there a reason to care now) — and the gaps drive the rewrite.

## Escalate when

- The claimed differentiator is not verifiable, or the same claim appears on a competitor's homepage.
- Positioning would require a product change the user has not agreed to.
- Competitor material is unavailable and the white-space call would be a guess.
- The user's belief about their market conflicts with what the site, reviews, and competitor set show — surface the conflict rather than positioning around it.
- A regulated category constrains the claims the strongest position would require.
