---
name: drill
description: 'Use when a concept needs practising: the user asks for an exercise, quiz, recall, or gap probe. Runs one scaffolded practice move and records every attempt in PROGRESS.md. Not for explanations — use explain-concept.'
---

# Drill

## Contract

| Field | Bound contract |
|---|---|
| Trigger | give me an exercise, quiz me, keep it fresh, what am I missing / where are my gaps, or explicit practice/quiz/recall/probe |
| Authority | Write only `PROGRESS.md` at the workspace root and read `CORPUS.md` there. Rollback is deleting the lines this run appended; the file is append-only, never rewritten. |
| Side effect | Appends one line per attempt to `PROGRESS.md` at the workspace root; drives spaced recall and probes gaps. |
| Done | The named move completed; every attempt recorded; cleared concepts marked no-hints-independent. |

## Inputs

- A concept name (required) and a move (optional): `practice`, `quiz`, `recall`, or `probe`.
- The move is optional: the routing table picks it, an explicit argument overrides, and no match defaults to `practice`.
- Optional: item count for `quiz` (default 5–8).
- `probe` requires `CORPUS.md` at the workspace root. `recall` requires prior `PROGRESS.md` history. State which is missing rather than inventing it.

## Procedure

1. Read `PROGRESS.md` at the workspace root (create it on first write) and, for `probe`, `CORPUS.md`. If neither `PROGRESS.md` nor `CORPUS.md` exists, say once that nothing is being recorded, ask which concept to work on, and run in-session only. Done when: `PROGRESS.md` is read or confirmed absent, and for `probe`, `CORPUS.md` is read or confirmed absent.
2. Pick the move. An explicit argument overrides the table; no match means `practice`. Table: "give me an exercise" / "let me practise X" / "walk me through one" → `practice`; "quiz me" / "test me on X" → `quiz`; "what should I review" / "keep it fresh" → `recall`; "what am I missing" / "where are my gaps" / "am I ready for X" → `probe`. Done when: the move is picked and stated.
3. Run one move per run. Another move is another run. Done when: one move is selected for this run.
4. `practice` — three rungs in this order, one rung per run: **worked** (the agent solves it and narrates why each step is taken; done when the full solution is narrated and the learner has answered one self-explanation prompt); **faded** (the agent solves everything but the last step and the learner finishes it; each further faded run removes one more step, always from the end backward, so the learner performs the final step every time; done when the learner has produced the step the rung asks and the attempt is recorded); **independent** (the learner solves it whole; done when the learner has produced the step the rung asks and the attempt is recorded). Advance a rung only when the current one was cleared without hints. Done when: the current rung is completed and the attempt is recorded.
5. `quiz` — five to eight items unless the user asks for a different count, mixed between recall and application, over concepts already explained or cleared. The learner commits to an answer before anything is revealed. Done when: every item is graded and each miss names the misconception it reveals.
6. `recall` — a concept is due on an interval ladder counted from the date its independent rung was cleared: 1 day, 3 days, 7 days, 21 days, then every 60 days. Due means today is at or past the next interval with no retrieval recorded since. A missed retrieval resets that concept to the start of the ladder. Interleave across cleared concepts only. Two consecutive misses on one concept send it back to a faded rung. Done when: every due concept has been retrieved once and recorded.
7. `probe` — take what the learner says they want to do next, walk `CORPUS.md` back through the concepts it needs, ask one discriminating question per concept, then rank the confirmed gaps by how many downstream concepts each blocks. Done when: the ranked list is reported and every confirmed gap is recorded.
8. Hints — three tiers, released one at a time and on request: **nudge** (names the concept in play, no structure); **strategy** (the shape of the solution, no answer); **bottom out** (the step itself). Once a concept's independent rung is cleared with no hints, withdraw hints for that concept. Done when: hints are released on request and withdrawn for cleared concepts.
9. Grading — name the specific misconception an answer reveals rather than scoring it right or wrong. Say what the answer got right before what it missed. Release the solution once the learner has committed to an attempt. Done when: each answer is graded with its misconception named and the solution released.
10. Record every attempt in `PROGRESS.md` with this line shape: `- <YYYY-MM-DD> · <move>[/<rung>] · <cleared|missed>, hints <none|1|1-2|1-3>[, <misconception>]`. A concept is **cleared** when its `practice/independent` line reads `cleared, hints none`. Missed concepts are not cleared. Use the words **rung** and **cleared** and no synonyms. Done when: every attempt is recorded in `PROGRESS.md` with the correct line shape.

## Failure and recovery
- No `PROGRESS.md` and no `CORPUS.md`: say once that nothing is being recorded, ask which concept to work on, and run in-session. Do not create files for a `probe` that needs `CORPUS.md`.
- `probe` without `CORPUS.md`: blocked. Report the missing file; do not invent gaps or rank an empty list.
- `recall` with no cleared concepts: nothing is due. Report that and stop; do not fabricate a due set.
- Rung not cleared: do not advance. Record the miss with its misconception; do not rewrite `PROGRESS.md` (append only).
- Hints used on an independent rung: that concept is not cleared; record `hints 1` through `1-3` as used.
- Rollback: `PROGRESS.md` is append-only; recovery is deleting the lines this run appended. Never swallow a miss or mark cleared when hints were used.

## Output
One completed move plus one appended `PROGRESS.md` line per attempt (or in-session only when no files exist), with the rung outcome for `practice`, graded items for `quiz`, due concepts retrieved for `recall`, or a ranked gap list for `probe`.
