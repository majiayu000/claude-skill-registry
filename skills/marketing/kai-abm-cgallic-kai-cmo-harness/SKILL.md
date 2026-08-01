---
name: kai-abm
description: Plan and execute account-based marketing campaigns for enterprise targets — account selection, personalized outreach, multi-channel touch sequences, and deal acceleration. Use when "ABM", "account-based marketing", "enterprise marketing", "target accounts", "named accounts", "enterprise outreach", "key accounts", or any request to build personalized campaigns for specific companies.
---

# /kai-abm — Named Accounts Moved Into Pipeline

## Objective

A running account-based program against a specific list of named companies: accounts tiered by fit and intent, the buying committee mapped per account, and personalized touch sequences on the channels those accounts actually use. The deliverable is the working material — account briefs, sequences, ad copy, sales enablement — not a document explaining ABM.

Personalization depth is the load-bearing variable. A Tier 1 message that could have been sent to any company in the industry is a Tier 3 message at a Tier 1 cost.

## Done when

Work type `campaign` — floor **E5/C3/O4** (`harness/eco-floors.yaml`). Campaign is composite: CLOSED only when every child asset is CLOSED and the program-level threshold is met. One unshipped sequence keeps the whole thing open.

- **E5** — each asset lands at its real target with provider evidence: ESP send receipts reconciled against the approved account list, ad object ids read back field-for-field against the approved bundle, LinkedIn provider ids. Drafts sitting in `workspace/` are E1.
- **C3** — every asset clears its machine gates (below) and a named non-producer reads the Tier 1 material end to end. Cold outreach inside this program inherits the `cold-email` C4 field standard — CAN-SPAM/GDPR/CASL identity, opt-out, and consent basis verified before send, not a C2 lint.
- **O4** — engagement score, pipeline influence, and deal velocity read at the declared window against thresholds recorded before the first touch. No baseline before launch means no outcome credit later.

## Constraints

- **Read `MARKETING.md` from the project root first.** It carries product, ICP, value prop, monetization, voice, current channels, and competitive landscape. If it does not exist, build it from the codebase — CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, email/ad/analytics config — using the template from `/kai-email-system`, and confirm the draft. Do not open with discovery questions the repo can answer.
- **Nine things must be known before any asset gets written:** ICP definition (industry, size, revenue, tech stack, signals); the named account list or the criteria that build it; the buying committee (decision-makers, influencers, blockers, by title); the offer, price point, deal size, and sales cycle length; existing warm relationships at target accounts; sales alignment and the handoff point; which channels are available (email, LinkedIn, ads, direct mail, events, phone); per-account budget; and which harness persona(s) map to the committee.
- **Load the platform policy reference before writing any ad copy** — LinkedIn `harness/references/linkedin-ads-rules.md`, Google Display `harness/references/google-ads-policy-reference.md`. Policy compliance is checked in addition to quality gates, not instead of them.
- **Cold email compliance is a hard gate.** `harness/references/cold-email-rules.md` governs every outbound sequence.
- **Gate minimums:** Four U's ≥ **10/16** for emails and outreach, ≥ **12/16** for content and landing pages (`python scripts/quality_gates/four_us_score.py <file>`); zero banned words (`python scripts/quality_gates/banned_word_check.py <file>`); zero AI slop. Max 2 auto-retry cycles, each naming the specific failing dimension.
- **Personalization depth check is binding:** every Tier 1 message references something specific and verifiable about that account. Fail it and the asset does not ship at Tier 1.
- **Writing rules apply to every asset:** conditions after the main clause, instructions start with verbs, short sentences, bold the answer.
- **No live-channel mutation without recorded human approval** — sends, ad launches, and connection requests are approval-gated regardless of how good the copy scores.

## Context

| Need | Load |
|---|---|
| ABM tiering, plays, measurement | `knowledge/playbooks/account-based-marketing.md` |
| Persona mapping for the buying committee | `knowledge/personas/_persona-index.md` |
| LinkedIn ad policy | `harness/references/linkedin-ads-rules.md` |
| Google Display ad policy | `harness/references/google-ads-policy-reference.md` |
| Cold outreach law and rules | `harness/references/cold-email-rules.md` |
| Product, ICP, voice, channels | `MARKETING.md` (project root) |

**Account tiers** — the tier decides how much research and personalization each account earns:

| Tier | Model | Volume | Personalization |
|---|---|---|---|
| Tier 1 | 1:1 | Top 10–25 accounts | Fully personalized, high-touch |
| Tier 2 | 1:few | 25–100 accounts | Clustered by industry or use case, semi-personalized |
| Tier 3 | 1:many | 100–500 accounts | Programmatic with light personalization |

**Tier 1 account research** pulls five things: company priorities (earnings calls, press releases, job postings), current technology stack, key personnel (profiles, what they publish, mutual connections), pain signals (hiring patterns, tech changes, review complaints), and who else is selling to them.

**Touch sequence shape** — warm-up (weeks 1–2: engagement, content sharing, ad impressions), direct outreach (weeks 3–4: personalized email, LinkedIn message), value delivery (weeks 5–6: relevant content, case study, event invite), conversion push (weeks 7–8: meeting request, demo, executive intro). Compress or extend against the real sales cycle length.

**Deliverables:** ABM strategy document (ICP, tiers, channels, timeline, budget), Tier 1 account briefs, email sequences per tier, LinkedIn outreach templates, per-platform ad copy, content map against buying stages, sales enablement cheat sheets, measurement framework, and the gate pass/fail summary. Existing assets get mapped to stages before new ones get written. A sales/marketing SLA — response times, follow-up rules, feedback loop — ships with the plan.

**Output** goes to `workspace/` as `abm-campaign-YYYY-MM-DD.md`.

## Escalate when

- The account list cannot be built because ICP criteria or intent signals are unavailable — say so rather than inventing fit.
- Sales has not agreed to the handoff point or the SLA. An ABM program with no sales counterpart produces engagement and no pipeline.
- Per-account budget cannot support the tier count proposed; ask which tier to cut rather than thinning all three.
- Contact data provenance or consent basis for a region is unclear.
- The target industry is regulated and the obvious channel carries compliance risk.
