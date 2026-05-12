# anchor-derivation.md — evidence to anchor pipeline

This pipeline converts local evidence into five generated anchors. Use it in order. Do not start from favorite influences. Start from evidence.

## Pipeline overview

Evidence -> Signal -> Influence candidate -> Concept -> Failure modes -> Anchor entry -> Preview rationale

## 1. Evidence

Collect compact evidence units:

- Quoted phrase or paraphrase with exact wording when short.
- Source class: memory, indexed ICM, indexed session history, Claude Code transcript, Codex transcript, Gemini CLI transcript, OpenCode transcript, Amp transcript, Pi transcript, Cursor transcript, project instruction.
- Path, index label, or session identifier when available.
- Date or recency when available.
- Domain: prose, code, design, decision, meta-process, or mixed.

Keep evidence units short. Never dump full transcripts.

## 2. Signal

Convert evidence into a normalized signal:

- Positive influence: named person, school, work, artifact, or method the user repeatedly endorses.
- Side A ban: slop/default convergence the user repeatedly rejects.
- Side B ban: overkill/compensatory excess the user repeatedly rejects.
- Process constraint: write safety, verification, no scope creep, atomicity, evidence-first behavior.
- Register constraint: tone, rhythm, directness, naming, compactness, or anti-flattery.

Mark signal strength:

- **Strong:** repeated across source classes or repeated with corrections.
- **Medium:** appears once in durable memory or project instruction.
- **Weak:** appears once in a transcript without correction or recurrence.

Weak signals can support but should not select an anchor alone.

## 3. Influence candidate

Map each signal to one or more candidates from `influence-catalogue.md`. Then apply the five inclusion criteria:

1. Portable principle across at least two domains.
2. Recognizable Side A and Side B failure modes.
3. Concrete exemplar.
4. Contrast value.
5. Non-fandom operational framing.

Reject candidates that fail any criterion. If two candidates explain the same signal, prefer the one with better contrast against the current anchor set.

## 4. Concept

Write the concept as an imperative discipline, not an admiration statement.

Good concept shapes:

- "Name the invariant before adding guardrails."
- "One visual gesture carries the surface."
- "Reduce by concentrating meaning."
- "Enter the reader's frame before leading."

Bad concept shapes:

- "The user likes Dieter Rams."
- "This is inspired by high-quality design."
- "Be elegant and thoughtful."

## 5. Failure modes

For every anchor, derive both sides:

- **Side A:** What default, vague, timid, under-committed version violates the concept?
- **Side B:** What excessive, compensatory, ornate, over-abstracted version violates the concept?

Both sides must be concrete enough to audit. If one side cannot be named, the anchor is not ready.

## 6. Anchor entry

A generated anchor entry contains:

- Anchor name: `{Influence}-{Concept}` or a compact equivalent.
- Influence: person/work/method with one-line identification.
- Concept: portable principle in one paragraph.
- Evidence rationale: why this anchor belongs in this user's skill.
- Canonical exemplar: concrete artifact or method.
- Failure modes: Side A and Side B.
- Cross-domain manifestations: prose, code, design, decision.

Anchor names must be stable, readable, and operational. Avoid private jokes and fandom labels.

## 7. Preview rationale

Before writing, preview a table with exactly five rows:

| Anchor | Influence | Concept | Evidence rationale |
|---|---|---|---|

Evidence rationale should cite source classes, not dump content. Example:

"Memory bans generic validation openers; session corrections repeatedly demand direct recommendations; maps to Feynman-Clarity over Orwell because the dominant signal is explanation clarity across code and prose."

## Ranking rules

Rank candidates by:

1. Repeated evidence across source classes.
2. Strength of correction signal from the user.
3. Cross-domain portability.
4. Contrast with already selected anchors.
5. Ability to generate concrete Side A and Side B bans.

Do not use numeric weights. Use ordinal ranking and written rationale.

## Collision and update derivation

When updating an existing `spine` or `*-taste` skill:

1. Treat existing anchors as evidence, not as immutable truth.
2. Preserve anchors with strong current evidence and high contrast.
3. Replace anchors whose only support is historical or redundant.
4. Preserve unowned files.
5. Generate exactly five anchors unless update-in-place explicitly keeps a different count.

## Generated-output checks

Before final write, scan generated output for:

- Slot markers from templates.
- Generic openers.
- Hedge prefaces.
- Weighted-rubric language.
- Exhaustive transcript excerpts.
- Missing Side A or Side B for any anchor.
- More or fewer than five anchors, except when update-in-place explicitly preserves an existing owned skill's different anchor count.
