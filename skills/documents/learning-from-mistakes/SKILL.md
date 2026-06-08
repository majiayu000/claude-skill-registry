---
name: learning-from-mistakes
description: Record a hard-won engineering lesson after a bug or mistake is resolved. Use when a bug resisted ATLAS until Boss's guidance cracked it, or when a long debugging hunt ended in an aha moment worth never relearning.
---

Capture the lesson so future-ATLAS does not pay the same debugging cost twice.

## When to write an entry

Write one — without being asked — when either is true:

- **Boss had to step in.** A bug or mistake ATLAS could not solve alone; Boss's guidance is what cracked it.
- **Aha moment after a long hunt.** A debugging session that ran long and ended in a non-obvious realization.

Skip routine fixes. The bar is *surprise*: would this genuinely save someone — likely future-ATLAS — from a hard time? If the cause was obvious in hindsight to anyone, it is not worth an entry. Apply the same high-entropy filter as `NOTES.md`: record what is surprising, not what is expected.

## Where

One file per lesson: `docs/learning-from-mistakes/<kebab-case-slug>.md`. The slug names the problem, so the folder is self-indexing — e.g. `stale-closure-in-useeffect.md`, `timezone-off-by-one-on-date-parse.md`.

## Format

Keep it brief — important information only. Four short sections:

```markdown
# <Lesson title — the problem in one line>

**Date**: YYYY-MM-DD · **Area**: <project / module / domain>

## Symptom
What looked wrong — the observable behavior or the assumption that failed.

## Root cause
The non-obvious truth. Why it actually happened.

## Resolution
The fix, or the insight that cracked it. Credit Boss's guidance if that is what unblocked it.

## Lesson
The transferable rule — how to recognize or avoid this next time.
```

A few tight sentences per section beats a padded template. If a section adds nothing, drop it.

## Recall

Before concluding a hard bug is unsolvable, scan `docs/learning-from-mistakes/` — a past lesson may already name the cause.
