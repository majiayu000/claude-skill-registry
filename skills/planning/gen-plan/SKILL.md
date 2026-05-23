---
name: gen-plan
description: Generate iterative `plan-N.md` files in the repo root (max N=5). Use only when asked; clarify before `plan-1.md`; stop at `plan-5.md`.
---

# Gen-Plan

## Contract

- Scope: operate in the repo root; manage files named `plan-N.md` where `N` is an integer.
- Define `N` as the maximum numeric suffix among files matching `plan-(\d+).md` (ignore non-matching filenames, including legacy `plan-N-E.md` / `plan-N-R.md`).
- If any matching file has `N > 5`: do nothing; reply exactly: "Plan is ready."
- If `plan-5.md` exists (case-insensitive): do nothing; reply exactly: "Plan is ready."
- If no matching `plan-(\d+).md` exists: run the clarification flow, then create `plan-1.md`.
- Otherwise: create `plan-(N+1).md`. Source plan markdown: `plan-N.md`.
- When loading plan markdown from a source file, insert the full contents of `plan-N.md` at the `<INCLUDE CONTENTS OF PLAN FILE>` placeholder in the plan template.
- Never overwrite an existing target file; stop and report the conflict.
- Ask questions only when unresolved judgment calls block the next iteration.

## Clarification flow (when needed)

- Research first; ask only judgment-call questions.
- Use the `CLARIFICATION EXPERT: HUMAN INPUT REQUIRED` block with numbered questions.
- After questions are answered, determined if another round of questions is needed; if so continue asking questions until there are no more then write the next plan file.

## Iterate on the plan

Use the following to generate a plan

```md
---
Carefully review this entire plan for me and come up with your best revisions in terms of better architecture, new features, changed features, etc. to make it better, more robust/reliable, more performant, more compelling/useful, etc.

For each proposed change, give me your detailed analysis and rationale/justification for why it would make the project better along with the git-diff style changes relative to the original markdown plan shown below:

<INCLUDE CONTENTS OF PLAN FILE>
---
```
