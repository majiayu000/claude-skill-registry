---
name: proof
description: "Use when the user asks for proofreading or light copy editing while preserving original wording, tone, and order. Triggers: 'proofread', 'fix typos', 'grammar only', 'copy edit only', 'SPAG pass'. Not for rewrites, tone shifts, structural edits, or style upgrades; use good-prose for those requests."
---

# Proof

Proofread and lightly copy edit text while preserving wording, order, tone, and meaning.

## Critical Constraints

- Apply only spelling, punctuation, capitalization, agreement, and minor grammar fixes.
- Do not rewrite, rephrase, reorder, add content, or change tone.
- If a fix requires substantive rewriting for clarity or logic, leave the source text unchanged and flag it with a suggested revision.
- Preserve author voice, formatting, and regional conventions unless the user asks otherwise.

## Routing: `proof` vs `good-prose`

Use `proof` when the request is about correctness without stylistic change.

- "proofread this"
- "fix typos/grammar only"
- "copy edit lightly"
- "do not rewrite"

Use `good-prose` when the request asks for writing-quality changes or substantial edits.

- Rewrite, tighten, polish, or improve flow/clarity.
- Adjust tone for audience (more formal, friendlier, firmer).
- Restructure paragraphs, argument order, or narrative arc.
- Significantly shorten or expand content.

If intent is ambiguous:

1. Start with a proof-only pass.
2. Flag issues that need substantive rewriting.
3. Ask whether to proceed with a `good-prose` rewrite.

## Workflow

1. Read the full text once to preserve meaning and tone.
2. Apply mechanical fixes only: spelling, punctuation, capitalization, subject-verb agreement, pronouns/articles/prepositions, and obvious minor grammar.
3. Apply organization agreement consistently:
   - Use plural verbs when referring to actions by people within the organization (example: "OpenAI are developing new models").
   - Use singular verbs when referring to the organization as a legal entity, owner, or brand (example: "OpenAI is valued at billions").
4. Identify major unresolved issues (clarity gaps, logical breaks, grammar that cannot be fixed without rewriting) and do not apply those edits directly.
5. Return edited text and a short flagged-issues section when major issues remain.

## Output

- Provide revised text first.
- If no major rewrite-needed issues remain, state: `No major rewrite-needed issues found.`
- If major issues remain, add a `Flagged issues` list with: original snippet, reason it was not directly edited, and suggested revision.
