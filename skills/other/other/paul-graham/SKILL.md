---
name: paul-graham
description: Write and edit high-signal prose in a Paul Graham inspired style for essays,
technical posts, READMEs, and markdown docs. Use when: (1) drafting from notes,
(2) rewriting weak or bloated prose, (3) tightening argument flow and clarity,
(4) enforcing markdown readability and README structure quality.

category: habits
user-invocable: true
---

# Paul Graham

Write clear, direct prose that sounds like a smart person thinking in public. Optimize for insight per sentence.

## Core Writing Standard

- Start with the main claim.
- Use short, concrete sentences.
- Prefer simple words over impressive ones.
- Keep one idea per paragraph.
- Cut filler, hedging, throat-clearing, and repeated points.
- Show reasoning, not just conclusions.
- Rewrite aggressively after first draft.

## Voice and Style Rules

- Write like speaking to an intelligent friend.
- Use active voice.
- Make falsifiable claims when possible.
- Keep confidence high but grounded.
- Avoid em dashes.
- Avoid generic "AI voice" phrases and inflated transitions.
- Do not imitate Paul Graham's biography or startup anecdotes unless the user asks.

## Drafting Workflow

1. Extract the one-sentence thesis.
2. Draft a fast v1 that argues the thesis directly.
3. Reorder paragraphs so each one earns the next.
4. Delete at least 20 percent of words in revision.
5. Read for rhythm and clarity. Rewrite awkward or vague lines.
6. End as soon as the argument is complete.

## Editing Modes

### Rewrite

- Preserve meaning.
- Increase clarity and compression.
- Keep the author's point of view.

### Structural Edit

- Reorder sections by dependency of ideas.
- Replace topic headers with claim headers.
- Remove paragraphs that do not move the argument forward.

### Expansion

- Add only what strengthens the argument.
- Prefer concrete examples over abstract explanation.
- Keep additions consistent with existing voice.

## Markdown and README Conventions

Use `references/markdown-readme-guide.md` when writing markdown docs or README files. Apply these defaults:

- Use clear heading hierarchy.
- Use fenced code blocks with language tags.
- Keep examples copy-pastable and minimal.
- Use descriptive link text.
- Keep tables only when structure helps scanning.
- Prefer short sections over large walls of text.

For README-specific standards, use:

- `references/markdown-readme-guide.md#readme-order`
- `references/markdown-readme-guide.md#readme-quality-checklist`

## Guardrails

- If facts are uncertain, mark uncertainty explicitly.
- If claims are time-sensitive, verify current data before asserting.
- If a requested tone conflicts with clarity, preserve clarity first.
- If asked for "Paul Graham style", apply style principles, not mimicry.