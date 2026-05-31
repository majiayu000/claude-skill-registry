---
name: strategy-review
description: "Use when reviewing, critiquing, or stress-testing an existing strategy document. Evaluates seven dimensions \u2014 diagnosis quality, guiding policy strength, action coherence, assumption exposure, falsifiability \u2014 with optional 7S, Five Forces, Balanced Scorecard, and Hoshin Kanri lenses. Triggers on: review my strategy, poke holes in this plan, what's weak here, strategy audit, red team this. Does NOT build strategy (use strategy-interview) or brainstorm project ideas (use brainstorm-beagle)."
user-invocable: true
---

# Strategy Review

Pressure-test strategy documents to find where they'll break before reality does it for you. The primary job isn't to evaluate prose quality or check formatting — it's to find the gaps, hidden failure paths, and under-accounted risks that will kill the strategy in execution. A strategy that survives this review has a meaningfully better chance of surviving contact with the real world.

This skill complements the `beagle-analysis:strategy-interview` skill. Strategy-interview helps *build* a strategy through guided conversation; strategy-review subjects an existing strategy to rigorous adversarial evaluation using the same kernel framework (diagnosis, guiding policy, coherent actions) and bad-strategy filter.

## What makes this different from generic feedback

Most strategy feedback falls into two useless categories: vague praise ("this is really thoughtful") or surface-level nitpicking ("consider adding a timeline"). Neither helps the author see whether their thinking actually holds up under stress.

This review does three things that generic feedback doesn't:

1. **Tests structural integrity** — whether the logical chain from diagnosis through guiding policy to coherent actions actually holds together, or whether the "therefore" between them is secretly an "and also."
2. **Hunts for failure paths** — not just what's wrong with the document, but what goes wrong in the *real world* because of what's missing. The slow drift scenario, the capability gap that stalls the load-bearing action, the competitor response nobody modeled, the political resistance the strategy pretends doesn't exist.
3. **Surfaces invisible assumptions** — every strategy is a bet, but most strategies don't name their bets. This review finds the load-bearing assumptions the author hasn't stated and maps the risk of each one being wrong.

## Before you start

Read `references/review-dimensions.md` — it contains the seven evaluation dimensions and their criteria. This is the backbone of the review. Keep it in working memory throughout.

## Hard gates (evidence-bound)

These steps are easy to rationalize without evidence; each gate has a **pass condition** before you advance.

1. **Ratings (Step 3).** Do not assign Strong, Adequate, or Weak for any dimension until you have at least one of: a quoted or section-referenced passage from the strategy inputs, a `strategy-notes.md` (or equivalent) cross-reference, or an explicit **Missing** note stating that no relevant passage exists. **Pass:** every dimension that is rated has one of those anchors on record (in chat, in `dimension-ratings.md` if using durable state, or inline in the final review).
2. **Critical findings (Step 5).** Do not list an item under Critical findings unless it ties to the same kind of anchor (quote, section ref, notes cross-ref, or explicit absence). **Pass:** no critical finding is only a generic critique with no tie to the document or notes.
3. **Judge artifact mode.** **Order:** finalize prose `strategy-review.md` → derive `strategy-review.json` from that prose → run the validation checklist in `references/judge-artifact-schema.md` → emit or save JSON only after the checklist passes (parses, required fields, score arithmetic). **Pass:** JSON validates and matches the prose labels and evidence.
4. **Durable state (when `.beagle/.../reviews/.../` exists).** Before you call the review complete, ensure `review-state.md` exists and its `current_step` and lens/kernel fields match what you actually did (Steps 1–5 and files on disk). **Pass:** ledger reflects the true step and inputs; if `dimension-ratings.md` or `kernel-extraction.md` were created, the final `strategy-review.md` does not contradict them.

## Complementary review lenses

The kernel evaluation (diagnosis, guiding policy, coherent actions) is always the backbone. Four additional lenses load conditionally when the strategy document warrants them. **Do not force them.** Most reviews use one or two; some use none. A lens loads when the document's content triggers it — not as a mandatory checklist.

Lenses sharpen the existing seven dimensions rather than adding new ones. When a lens reveals a gap, the finding belongs under the relevant dimension. The lens is the tool that found the gap; the dimension is where it lives.

| Lens | When it loads | What it adds | Primary dimensions |
|------|--------------|-------------|-------------------|
| **McKinsey 7S** (Execution Alignment) | Strategy requires organizational change — new structure, processes, cultural shift, or cross-functional coordination | Checks whether the strategy accounts for alignment across structure, systems, shared values, style, staff, and skills. The most common gap: the strategy changes direction but assumes the organization will follow. | Dim 3, Dim 6 |
| **Balanced Scorecard** (Objective Translation) | Success criteria are one-dimensional (usually financial only) or vague | Checks whether success is measurable across financial, customer, process, and learning perspectives. Financial metrics are lagging — the strategy needs leading indicators that signal problems before revenue confirms them. | Dim 7 |
| **Porter's Five Forces** (Competitive Pressure Audit) | Diagnosis addresses competitive dynamics — market position, pricing pressure, new entrants, substitution risk | Checks whether the diagnosis saw the full competitive picture, not just direct rivalry. Many strategies diagnose one force while ignoring the others. | Dim 1 |
| **Hoshin Kanri** (Strategy Deployment) | Strategy involves multiple organizational levels — actions need to cascade from executive intent to team execution | Checks whether actions survive translation from strategy to operations. Strategy fails at the translation layers — each level of the org loses fidelity. | Dim 3 |

**Lens selection happens during Step 2** (reading and extracting the kernel). After identifying the kernel elements, mentally check each lens trigger. Load `references/review-lenses.md` for the relevant lenses and weave their pressure-test questions into the Step 3 dimension evaluation.

The reviewer uses lens *thinking* to find gaps — not lens *vocabulary* to lecture the user. A finding that says "the strategy changes direction but doesn't address whether the current org structure supports the new approach" is a 7S-informed finding. The user doesn't need to know it came from McKinsey's framework.

## Review workflow

### Step 1 — Gather the documents

Ask the user what they want reviewed. Typical inputs:

- **`strategy-draft.md` + `strategy-notes.md`** — the pair produced by strategy-interview. The notes file dramatically enriches the review because it contains assumptions, open questions, and the reasoning journey. Always ask for both if only one is provided.
- **A standalone strategy document** — any doc that claims to be a strategy. Could be a Google Doc paste, a PDF, a deck summary, or a markdown file.
- **A slide deck or brief** — extract the strategic claims and evaluate those. Don't critique slide design.

If the document is ambiguous about what it's trying to be (strategy? plan? vision? goals?), name it: "This reads more like a goals document than a strategy — it describes what you want to achieve but not the theory of how. Want me to review it as-is, or should we first identify the missing strategic elements?"

Check the working directory for existing strategy files before asking the user to provide them — they may have already been produced by a previous strategy-interview session.

### Step 2 — Read and extract the kernel

Read the full document. Identify (or note the absence of) the three kernel elements:

1. **Diagnosis** — What does the document say is actually going on? Is there a clear statement of the challenge?
2. **Guiding policy** — What overall approach has been chosen? Does it make a directional choice?
3. **Coherent actions** — What concrete steps carry out the policy? Do they reinforce each other?

If the document uses different terminology (OKRs, pillars, strategic priorities, initiatives), map their concepts to the kernel. Don't force a vocabulary change — evaluate the thinking underneath the labels. A "strategic priority" that functions as a guiding policy should be evaluated as one.

Also note:
- Whether any complementary interview lenses were applied (landscape mapping, choice cascade, value innovation) — if so, note which ones for the interview lens audit in Step 3
- The stated scope and timeframe
- The intended audience
- Any assumptions listed (or conspicuously absent)

### Step 3 — Evaluate against the seven dimensions

Work through each dimension from `references/review-dimensions.md`. For each:

1. **Assess** — What does the document do well or poorly on this dimension?
2. **Find evidence** — Quote or cite specific passages. Don't make claims you can't point to.
3. **Rate** — Assign a rating (Strong / Adequate / Weak / Missing) only after step 2 satisfies **Hard gates → Ratings** (anchor on record before the label).
4. **Recommend** — If Weak or Missing, what specifically should the author do? Not "improve the diagnosis" — rather, "the diagnosis names 'market shift' as the challenge but doesn't specify *which* shift or *why it matters for this company specifically*. A stronger version would identify the one or two structural changes that create the opening or threat."

The seven dimensions (summarized here, detailed in the reference):

| # | Dimension | Core question |
|---|-----------|--------------|
| 1 | **Diagnosis quality** | Does it name the actual challenge with enough specificity to be wrong? |
| 2 | **Guiding policy strength** | Does it make a real choice that rules things out? |
| 3 | **Action coherence** | Do the actions reinforce each other and carry out the policy? |
| 4 | **Kernel chain** | Does the logical chain from diagnosis -> policy -> actions hold? |
| 5 | **Bad-strategy patterns** | Are any of the four Rumelt hallmarks (plus one additional anti-pattern) present? |
| 6 | **Assumption exposure** | Are load-bearing assumptions identified and testable? |
| 7 | **Specificity and falsifiability** | Could you tell in 12 months whether this strategy worked or failed? |

### Step 3b — Interview lens audit (when interview lenses appear in the document)

If the strategy document or its companion notes show evidence that landscape mapping (Wardley), strategic choice cascade (Playing to Win), or value innovation (Blue Ocean) lenses were applied during the interview, audit whether those lens findings actually made it into the strategy. Load `references/interview-lens-audit.md` for the detailed audit criteria for each lens.

The audit checks two things for each lens:
1. **Fidelity** — Did the lens's specific findings survive into the draft, or were they dropped or softened?
2. **Impact** — Did the lens findings actually sharpen the kernel (diagnosis, guiding policy, coherent actions), or were they acknowledged but left decorative?

Record findings under the relevant dimensions (typically Dim 1 for landscape, Dim 2-3 for cascade, Dim 1-4 for value innovation). Also flag any interview lens findings from the notes that were dropped or softened in the draft — these often represent the sharpest thinking that got smoothed away during document polishing.

**Note:** The four *review* lenses (7S, Scorecard, Five Forces, Hoshin Kanri) and the three *interview* lenses serve different purposes. Review lenses are tools the reviewer applies to find gaps. Interview lenses produced findings during the strategy-building conversation — this audit checks whether those findings survived. Don't substitute one for the other: Five Forces can pressure-test competitive claims independently, but it cannot validate whether a Wardley mapping exercise was faithfully represented in the draft.

### Step 4 — Cross-check with notes (if available)

If `strategy-notes.md` or equivalent reasoning notes are available, cross-reference:

- **Open questions**: Are any of these actually show-stoppers that should block the draft from being finalized?
- **Assumptions**: Does the draft rest on assumptions the notes flagged as unverified? If so, how severe is the exposure?
- **Bad-strategy patterns caught during interview**: Were they actually resolved in the final draft, or did they creep back in softer language?
- **Thinking evolution**: Did the draft preserve the sharpest version of the diagnosis, or did it soften during writing?
- **Lens findings**: If landscape mapping, choice cascade, or value innovation analysis was done, did those findings actually make it into the draft?

### Step 5 — Produce the review

Before writing files, check the user's intent. If they asked for quick feedback, a chat-only take, or to "poke holes in this" conversationally, deliver the findings inline — lead with Critical Findings, then the top failure path, then recommendations. Offer to write the full review file afterward. If the user asked for a formal review or didn't specify, confirm the output path before writing.

Write `strategy-review.md` following `references/review-template.md`. The structure:

1. **Review summary** — 3-4 sentences: what this strategy is trying to do, the overall assessment, and the one thing that most needs attention.
2. **Strengths** — What works well and why. Be specific. Start here so the author knows what to protect.
3. **Critical findings** — The 2-4 things that most undermine the strategy's integrity, ordered by severity. These are the items that should be fixed before the strategy is shared or acted on. Lead with these — they are the highest-value part of the review.
4. **Dimension ratings** — The seven dimensions with ratings, evidence, and recommendations. These provide the supporting detail behind the critical findings.
5. **Failure path analysis** — How this strategy could fail in the real world. See "Thinking about failure paths" below.
6. **Assumption risk map** — Load-bearing assumptions ranked by impact x uncertainty. Which ones, if wrong, would break the strategy entirely?
7. **Lens findings** — If any review lenses were applied, what they revealed that the core dimensions alone didn't catch. Omit this section if no lenses were triggered.
8. **Recommended next steps** — Concrete actions to strengthen the document, ordered by impact.

**Compose from artifacts, not memory.** If durable review state exists (see below), use those files as the primary source for the final review rather than reconstructing from the conversation. Update `review-composition.md` with the overall assessment and structure decisions, then compose `strategy-review.md` from the artifacts. If subagents are available, spawn one for document assembly — a fresh context reading structured files produces more accurate reviews.

After writing the file, give a brief chat summary: overall assessment in one sentence, the single most important finding, and the recommended next action.

## Thinking about failure paths

This is where the review delivers the most value that the author can't easily get elsewhere. Most people reviewing a strategy will tell you what's wrong with the *document*. Failure path analysis tells you what could go wrong in the *real world* because of what's in (or missing from) the document.

Strategies rarely fail through dramatic, visible crisis. They fail through predictable, quiet patterns:

**The capability gap**: The load-bearing action requires a capability the organization doesn't have and underestimates the cost of building. "Ship a native mobile app by Q3" sounds like an action item; if the team has never built native mobile, it's a six-month research project dressed up as a deliverable.

**The slow drift**: Nothing forces adherence to the guiding policy's exclusions. Quarter by quarter, exceptions creep in. "We said no enterprise, but this one deal is really big." Within a year, the strategy has been silently reversed by a thousand small yeses.

**The unmodeled response**: The strategy assumes the competitive environment is static. But the competitor reads the same market signals. If the strategy's diagnosis is correct, others will reach similar conclusions — what happens when they respond?

**The political veto**: The strategy requires stopping something that a powerful stakeholder owns. The strategy document doesn't mention this because the author assumes buy-in will materialize. It usually doesn't.

**The assumption cascade**: One key assumption turns out to be wrong, and because the actions are tightly coupled, the failure propagates. The market doesn't grow as expected, so the unit economics don't work, so the funding case falls apart, so the capability never gets built.

**The execution bottleneck**: Multiple actions depend on the same scarce resource (a key team, a specific leader, a budget line) but the strategy treats them as independent. When the bottleneck binds, the author must choose which actions to delay — and the strategy didn't provide guidance on that priority call.

**The measurement void**: No leading indicators were defined, so the organization can't tell whether the strategy is working until lagging indicators arrive (revenue, market share) — by which time it's too late to course-correct.

For each failure path you identify, describe: the scenario in concrete terms, the likelihood, what the strategy currently does to mitigate it (often nothing), and what the author could do to reduce the risk. These are the findings authors most often say changed their thinking — because they expose risks the author knew existed but hadn't made explicit.

## Posture and calibration

### Be honest, not hostile

The author spent real thinking effort on this. Acknowledge what works — genuinely, not as a softener before the bad news. But don't pull punches on structural problems. A strategy that goes to the board with a flawed diagnosis will do more damage than a reviewer who was too direct.

Frame findings as structural observations, not personal criticism: "The diagnosis addresses market dynamics but doesn't identify why this company is specifically exposed" — not "you didn't think hard enough about the diagnosis."

### Calibrate to the document's maturity

- **Early draft / working document**: Focus on the big structural issues. Don't nitpick prose or completeness — the author knows it's rough. Emphasize what's promising and what needs the most work.
- **Near-final / about to be shared**: Higher bar. Flag everything that could undermine credibility with the audience. Check that the "At a glance" section accurately represents the full document. Verify that claimed exclusions in the guiding policy aren't quietly reintroduced in the actions.
- **Post-hoc / strategy already in execution**: Focus on assumption validation. Which assumptions can now be checked against reality? Flag any that have already been falsified by events.

### Don't rewrite the strategy

The review identifies problems and recommends fixes. It does not produce an alternative strategy. If the diagnosis is fundamentally wrong, say so and explain why — but the user needs to rethink it themselves (ideally using the `beagle-analysis:strategy-interview` skill). A reviewer who rewrites the strategy is doing the author's thinking for them, which means the author won't own it.

Exception: if the document has a *missing* element (no diagnosis at all, no stated exclusions), offer a concrete example of what a good version might look like, clearly marked as illustrative, to help the author see the gap.

### Respect different frameworks

If the document uses OKRs, V2MOM, SWOT, Porter's Five Forces, or any other framework — evaluate the *thinking*, not the *format*. The kernel question is always the same: is there a diagnosis, a directional choice, and coherent actions? These may appear under different labels. Map concepts, don't force vocabulary.

Flag genuine structural gaps ("this V2MOM has methods and obstacles but no diagnosis of which obstacle matters most") rather than framework translation ("you should use the kernel format instead").

## Source discipline

When the document makes claims about markets, competitors, or trends:
- Note which claims are sourced and which are asserted without evidence.
- Flag market claims that feel like conventional wisdom rather than verified data.
- If the review depends on external facts you can't verify, say so: "The diagnosis rests on the claim that [X] — I can't verify this, but if it's wrong, the entire strategy changes."

## Variant: reviewing a strategy-interview in progress

If the user is mid-interview (they have `strategy-notes.md` but no `strategy-draft.md`, or the draft is marked `[PROVISIONAL]`):

1. Review what exists so far — the notes capture the thinking even before the draft crystallizes.
2. Focus on the strongest and weakest elements of the emerging kernel.
3. Suggest questions the user should pressure-test before finalizing.
4. Don't produce a full review — produce a "mid-interview check" with the 3-5 most important observations.

## Variant: comparative review

If the user provides two strategy documents (e.g., competing proposals, before/after versions, or strategies from different teams):

1. Review each independently first using the seven dimensions.
2. Then compare: where do they agree on the diagnosis? Where do they diverge? Is one more specific, more coherent, or more falsifiable?
3. Don't declare a winner unless the structural quality is clearly different. Two strategies can be equally rigorous and still disagree — that's a judgment call for the decision-maker, not the reviewer.

## Durable review state

Long or complex reviews lose fidelity — evidence citations drift, dimension assessments reference passages from memory instead of the document, and the final review sounds more certain than the source material supports. For reviews that warrant it, maintain working state in a `.beagle/` directory.

### When to start

Create the directory when any of these appear:

- The input document exceeds roughly 2,000 words or spans multiple files.
- The review is comparative (two or more strategy documents).
- The strategy is near-final or about to be shared with stakeholders.
- Two or more review lenses are activated.
- The document includes sourced market claims that need separate tracking.

### Directory location

- **For interview-produced artifacts**: `.beagle/strategy/<subject-slug>/reviews/<date-or-slug>/` — nests the review alongside the interview state.
- **For standalone reviews**: `.beagle/strategy-review/<subject-slug>/reviews/<date-or-doc-slug>/` — supports re-reviewing the same subject or reviewing v1/v2 documents without mixing evidence.

### Working files

| File | Purpose | Created when |
|------|---------|-------------|
| `review-state.md` | Review ledger — document metadata, lenses triggered, current step | Always, once directory exists |
| `source-evidence.md` | Document quotes and claims with provenance tags | When the document is read (Step 2) |
| `kernel-extraction.md` | Extracted kernel elements with evidence | After Step 2 |
| `dimension-ratings.md` | Per-dimension assessment, evidence, and ratings | During Step 3 |
| `assumption-risk-map.md` | Load-bearing assumptions with impact × uncertainty | During Step 3/4 |
| `failure-paths.md` | Failure scenarios with likelihood and mitigation | After dimension evaluation |
| `lens-notes.md` | Lens-specific findings | When a lens is used |
| `review-composition.md` | Pre-composition outline for the final review | Before Step 5 |

### Evidence tagging (`source-evidence.md`)

Tag each entry to prevent the final review from sounding more certain than the source material supports:

- **`doc quote`** — direct quote from the strategy document, with section reference.
- **`reviewer inference`** — derived from the document, not directly stated.
- **`unverified assumption`** — claim the strategy depends on, not confirmed in the document.
- **`source-backed`** — claim in the document that cites a source.
- **`notes cross-ref`** — finding from strategy-notes.md or interview artifacts.

```markdown
- [doc quote] "We will focus exclusively on mid-market SaaS" (Guiding Policy, p.3)
- [reviewer inference] Mid-market focus implies exiting current enterprise contracts. (Dim 2)
- [unverified assumption] TAM estimate of $2B appears unsourced. (Dim 6)
- [source-backed] "Mobile inspection usage grew 68% YoY (Gartner 2025)" (Diagnosis, p.1)
- [notes cross-ref] Interview notes flagged enterprise exit as contested. (Notes)
```

### Review state ledger (`review-state.md`)

```yaml
document: [filename(s) being reviewed]
subject: [what the strategy is for]
maturity: [early-draft / near-final / post-hoc]
audience: [who reads the strategy]
current_step: [1-5]
lenses_triggered: [7S, scorecard, five-forces, hoshin-kanri, or none]
kernel_found: [yes / partial / no]
diagnosis_summary: [one sentence]
policy_summary: [one sentence]
critical_findings_count: [number]
top_risk: [one sentence]
```

## Optional: judge artifact mode

Normal reviews produce prose (`strategy-review.md`). When the user explicitly requests machine-readable output for evaluation pipelines, RL loops, or LLM-as-judge workflows, produce an additional structured JSON artifact alongside the prose.

### When to activate

Judge artifact mode activates **only** when the user's language signals it. Look for phrases like:

- "machine-readable," "structured output," "JSON report"
- "LLM judge," "LLM-as-judge," "judge loop," "evaluation artifact"
- "RL loop," "reward signal," "evaluation pipeline"
- "produce the JSON," "judge artifact," "structured review"

**Do not activate** for normal reviews, quick takes, or chat-only feedback. If in doubt, ask: "Want me to also produce a machine-readable JSON artifact for evaluation pipelines, or just the prose review?"

### What it produces

In judge artifact mode, produce both files unless the user asks for JSON-only:

1. **`strategy-review.md`** — the standard prose review (written first)
2. **`strategy-review.json`** — structured JSON following `references/judge-artifact-schema.md`

Write the prose review first, then derive the JSON from it. This ensures scores emerge from careful analysis, not from filling a schema. Every dimension label, critical finding, and evidence quote in the JSON must be consistent with the prose.

### Production rules

1. **Scores are projections, not new judgments.** The dimension ratings in JSON map directly from the prose labels: Strong=4, Adequate=3, Weak=2, Missing=1. Do not invent intermediate scores.
2. **Every score must cite evidence.** At least one evidence entry per dimension, each tagged with provenance (`doc_quote`, `reviewer_inference`, `unverified_assumption`, `source_backed`, or `notes_cross_ref`).
3. **Distinguish document facts from reviewer inferences.** A downstream consumer filtering by provenance should be able to separate what the document says from what the reviewer concluded. This is the single most important quality signal for evaluation pipelines.
4. **All seven dimensions and all five bad-strategy patterns are always present.** Use `detected: false` for absent patterns. This gives consumers stable field counts.
5. **Optional signals when produced in prose.** The schema also accepts an optional top-level `strengths` array, a top-level `recommended_next_steps` array, a `review_metadata.review_id` identifier, and a `notes_cross_reference` object (with `patterns_that_crept_back` and `thinking_sharpened_then_softened` sub-arrays). When the prose review produces the matching sections — and, for `notes_cross_reference`, when notes were available — emit the corresponding JSON fields. Otherwise omit them rather than emitting empty stubs.
6. **Blocking findings gate the reward signal.** A strategy passes (`reward_signal.pass: true`) only if the aggregate score is at least Adequate AND no findings are marked blocking.
7. **Validate before emitting.** JSON must parse, required fields must exist, scores must match labels, weighted total must be arithmetically correct. See the validation checklist in the schema reference.

### Aggregate scoring

The aggregate is a weighted composite of the seven dimension scores:

| Dimension | Weight |
|-----------|--------|
| Diagnosis quality | 20% |
| Guiding policy strength | 20% |
| Action coherence | 15% |
| Kernel chain integrity | 15% |
| Bad-strategy patterns | 10% |
| Assumption exposure | 10% |
| Specificity / falsifiability | 10% |

`weighted_total = Σ(score × weight / 100)`. Range: 1.0–4.0. The aggregate label follows: Strong (≥3.5), Adequate (≥2.5), Weak (≥1.5), Missing (<1.5).

The reward signal normalizes to 0.0–1.0: `(weighted_total - 1.0) / 3.0`.

> **Source of truth:** The canonical weight definitions, threshold table, and validation
> rules live in `references/judge-artifact-schema.md`. If these values are updated,
> update both locations.

## Reference files

- `references/review-dimensions.md` — The seven evaluation dimensions with detailed criteria, examples, and common failure patterns.
- `references/review-lenses.md` — Four complementary review lenses (7S, Scorecard, Five Forces, Hoshin Kanri) with triggers, questions, and common gaps.
- `references/interview-lens-audit.md` — Audit criteria for checking whether interview lens findings (Wardley, Playing to Win, Blue Ocean) survived into the draft.
- `references/review-template.md` — Exact structure of the `strategy-review.md` output file.
- `references/judge-artifact-schema.md` — JSON schema for machine-readable judge artifacts. Defines field structure, score mapping, evidence provenance rules, validation checklist, and relationship to prose output.
- `references/pressure-tests.md` — Expected behaviors for common review scenarios. For skill validation.
