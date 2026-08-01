---
name: kai-case-study
description: Produce customer case studies from interviews or data — Problem, Solution, Results structure with perception engineering and quality gates. Use when "case study", "customer story", "testimonial", "success story", "client results", or any request to document a customer win.
---

# /kai-case-study — A Customer Win Told In Numbers The Customer Approved

## Objective

A publishable customer case study built on a Problem / Solution / Results arc, led by the result rather than the logo, carrying real numbers and the customer's own language — plus the derived assets that make it usable: a sales one-pager, standalone pull quotes, and headline variants per channel.

Permission is the gate everything else waits behind. Named use requires the customer's approval; without it, the study is anonymized or it does not ship.

## Done when

Work type `blog-post` — floor **E5/C3/O3** (`harness/eco-floors.yaml`).

- **E5** — the live page returns 200 and matches the approved body, verified by someone other than the writer. Approval from the customer for named use is recorded before publication, not after.
- **C3** — Four U's ≥ **12/16** (`python scripts/quality_gates/four_us_score.py <file>`), zero Tier 1 banned words (`python scripts/quality_gates/banned_word_check.py <file>`), zero AI slop phrases, `seo_lint` clean where the study publishes as a search-facing page, and a named non-producer reads it end to end. Max 2 auto-retry cycles, each naming the specific failing dimension; after two, surface to a human with the failures listed.
- **O3** — organic clicks, impressions, indexation, or assisted conversions read from Search Console at the declared window. Sales-deck usage counts as a second declared metric when the study's primary job is enablement.

## Constraints

- **Read `MARKETING.md` from the project root first.** It carries product, ICP, value prop, monetization, voice, current channels, and competitive landscape. If it does not exist, build it from the codebase — CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, email/ad/analytics config — using the template from `/kai-email-system`, and confirm the draft. Do not ask the user what the product is.
- **Seven things must be known before drafting:** customer details (company, industry, size, role of the contact); the source material on hand (interview transcript, survey responses, data points, screenshots); the quantified before-state; what was actually done, specifically; the hard results (revenue, time saved, conversion lift, cost reduction); which harness persona the customer maps to; and **whether the customer approved named use or requires anonymization**.
- **Every claim carries a number or a named example.** Vague praise is a gate failure, not a stylistic preference.
- **Numbers come from the customer's own data or the source material.** No modeled, rounded-up, or inferred results.
- **Quotes are verbatim.** Two to three, chosen for emotion plus specificity, not smoothed into marketing prose.
- **No named use, logo, or identifying detail without recorded permission.**

## Context

| Need | Load |
|---|---|
| Content quality bar and structure checks | `knowledge/checklists/content-checklist.md` |
| Perception, context, permission layers | `knowledge/frameworks/content-copywriting/perception-engineering.md` |
| Persona mapping for the customer | `knowledge/personas/_persona-index.md` |
| Product, ICP, voice, channels | `MARKETING.md` (project root) |

**Narrative arc:** before-state (the specific pain, in the customer's words) → turning point (the decision trigger — why us) → after-state (measurable transformation).

**Structure:**

1. **Headline** leads with the result, not the company name — "73% Faster Onboarding: How [Company] Rebuilt Their Workflow".
2. **Snapshot box** — company, industry, challenge, result, scannable.
3. **The Challenge** — 2–3 paragraphs painting the before state in customer language.
4. **The Solution** — 2–3 paragraphs, concrete about what was done and how it worked.
5. **The Results** — biggest number first, in a data table or callout boxes.
6. **Customer quote** — their strongest line, closing.
7. **CTA** — the next action for the reader.

**Perception engineering layers apply throughout:** re-index the old way as the problem rather than merely the lesser option (perception); make the new approach feel inevitable (context); remove the risk of acting (permission).

**Deliverables:** the full case study (800–1500 words), a one-page sales summary (250 words max), 2–3 standalone pull quotes for social and email, 3 headline variants for different channels, the Four U's scorecard, and the gate pass/fail summary. A distribution plan names where it will live — website, sales deck, email, social.

**Output** goes to `workspace/` as `case-study-[company]-YYYY-MM-DD.md`.

## Escalate when

- Customer permission for named use is missing, ambiguous, or was given verbally with no record.
- The results cannot be substantiated from source material, or the customer's number and the internal number disagree.
- The customer's industry is regulated and the claimed outcome implies a prohibited promise.
- The only available numbers are percentages with no base, making the result unverifiable.
- The customer wants approval over the final copy and that review has not happened.
