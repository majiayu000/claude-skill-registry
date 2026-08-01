---
name: kai-brief
description: Create a structured content brief using the Kai CMO Harness brief schema. Selects persona, defines angle, sets quality targets. Use when "create a brief", "content brief", "plan this content", "brief for [topic]", "what persona should I use", or before any content creation to define the strategy. Outputs a brief that /kai-write and /kai-email-system consume.
---

# /kai-brief — A Brief `/kai-write` Can Execute Without Asking Anything

## Objective

A structured content brief that fixes the strategy before drafting starts: format, keyword set, persona, the specific angle, three hook options, the audience pain, the proof on hand, the CTA, word count, and publish date. It is the handoff contract `/kai-write` and `/kai-email-system` consume. The angle is the load-bearing field — "AI for law firms" is a topic; "Why law firms lose 40% of leads after 5pm" is an angle.

## Done when

Work type `strategy-plan` — floor **E3/C3/O1** (`harness/eco-floors.yaml`).

- **E3** — the brief conforms to `harness/brief-schema.md` and the requester accepted it; `/kai-write` does not proceed on an unapproved brief.
- **C3** — `banned_word_check` clean, and the three validation rules below hold under a read by someone other than the brief's author.
- **O1** — the brief names the piece it spawns and its publish date. A brief nothing gets written from is not finished.

## Constraints

- **Read `MARKETING.md` from the project root first.** It carries product, ICP, value prop, monetization, voice, current channels, and competitive landscape. If it does not exist, build it from the codebase — CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, email/ad/analytics config — using the template from `/kai-email-system`, and confirm the draft. Do not ask the user what the product is.
- **Six things must be known before the brief is written:** the format (blog, email, LinkedIn, ad, press), the topic or keyword, who it is for, the angle, what the reader should do next, and what proof or data exists to use.
- **Load the full persona file, not just the one-line hook** — it carries the language patterns, pain points, and hooks that shape the angle. **The brief then follows the schema in `harness/brief-schema.md`**, which is the format contract: fields are neither invented nor dropped.
- **Three rules must hold before handoff:** `hook_options` has exactly 3 variants; `angle` is differentiated from `target_keyword` rather than restating it; `proof_available` names real data or a named example, never a vague gesture at proof.

## Context

| Need | Load |
|---|---|
| Brief field schema and format contract | `harness/brief-schema.md` |
| Full persona profiles, language, pain points | `knowledge/personas/_persona-index.md` |
| Product, ICP, voice, channels | `MARKETING.md` (project root) |

**Persona selection** — pick one from the set below, then load its full file:

| Persona | Core hook | Best for |
|---|---|---|
| Competent Cog | "The system treats you like a child" | B2B SaaS, enterprise |
| Shock Absorber | "Accountability without authority" | Middle management |
| Ghosted Applicant | "The game is rigged" | Job seekers, HR tech |
| Subscription Serf | "They bet you won't fight back" | Consumer SaaS |
| System Manager | "No village, only vendors" | Parents, household managers |
| Admin Martyr | "Death by a thousand tasks" | Admin and ops roles |
| Obsolescence Anxious | "Working hard isn't the variable" | Career-concerned professionals |
| Credibility Fighter | "You're not crazy" | Experts fighting misinformation |

## Escalate when

- No proof, data, or named example exists for the angle — a brief promising specificity the writer cannot deliver moves the failure downstream.
- The requested topic maps to no persona in the set, or the angle needs a claim the business cannot substantiate.
- Format and word count conflict with the skill contract for that format.
