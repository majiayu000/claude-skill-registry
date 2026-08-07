---
name: drill
description: 'Use when a concept needs practising rather than explaining: run a scaffolded exercise from worked example to independent problem, quiz the learner, run spaced recall over what they cleared, or probe for the gaps blocking what they want next. For explanation, use explain-concept; for an end-to-end build, use capstone.'
argument-hint: "Which concept — practice, quiz, recall, or probe?"
---

One concept, one move per run. The table picks the move unless the argument names it.

## Pick the move

An explicit argument overrides the table; no match means **practice**.

| The user asks | Move |
|---|---|
| "give me an exercise", "let me practise X", "walk me through one" | practice |
| "quiz me", "test me on X" | quiz |
| "what should I review", "keep it fresh" | recall |
| "what am I missing", "where are my gaps", "am I ready for X" | probe |

## practice

Three rungs per concept, in this order, one rung per run:

1. **worked** — you solve it and narrate why each step is taken. Done when the full solution is narrated and the learner has answered one self-explanation prompt ("why this step here?").
2. **faded** — you solve everything but the last step and the learner finishes it. Each further faded run removes one more step, always from the end backward, so the learner performs the final step every time. Done when the learner has produced the step the rung asks of them and the attempt is recorded.
3. **independent** — the learner solves it whole. Done when the learner has produced the step the rung asks of them and the attempt is recorded.

Advance a rung only when the current one was cleared without hints.

## quiz

Five to eight items unless the user asks for a different count, mixed between recall and application, over concepts already explained or cleared. The learner commits to an answer before anything is revealed. Done when every item is graded and each miss names the misconception it reveals.

## recall

A concept is due on an interval ladder counted from the date its independent rung was cleared: 1 day, 3 days, 7 days, 21 days, then every 60 days. Due means today is at or past the next interval with no retrieval recorded since. A missed retrieval resets that concept to the start of the ladder. Interleave across cleared concepts only. Two consecutive misses on one concept send it back to a faded rung. The ladder is the whole model; the dates stay readable in `PROGRESS.md`. Done when every due concept has been retrieved once and recorded.

## probe

Take what the learner says they want to do next, walk `CORPUS.md` back through the concepts it needs, ask one discriminating question per concept, then rank the confirmed gaps by how many downstream concepts each blocks. Done when the ranked list is reported and every confirmed gap is recorded.

## Hints

Three tiers, released one at a time and on request:

1. **nudge** — names the concept in play, no structure.
2. **strategy** — the shape of the solution, no answer.
3. **bottom out** — the step itself.

Once a concept's independent rung is cleared with no hints, withdraw hints for that concept. Scaffolding that helped the novice costs the learner who no longer needs it.

## Grading

Name the specific misconception an answer reveals rather than scoring it right or wrong. Say what the answer got right before what it missed. Release the solution once the learner has committed to an attempt.

## PROGRESS.md

One file at the workspace root, created on first write, appended never rewritten:

```md
# Progress

## Deadlock

- 2026-08-06 · practice/worked · cleared, hints none
- 2026-08-07 · practice/faded · cleared, hints 1
- 2026-08-09 · quiz · missed, hints none, confused deadlock with livelock
- 2026-08-12 · practice/independent · cleared, hints none
- 2026-09-02 · recall · cleared, hints none
```

Line shape: `- <YYYY-MM-DD> · <move>[/<rung>] · <cleared|missed>, hints <none|1|1-2|1-3>[, <misconception>]`. A concept is **cleared** when its `practice/independent` line reads `cleared, hints none`. This file and this shape belong to `drill`; other skills read them and add nothing.

No `PROGRESS.md` and no `CORPUS.md` means say once that nothing is being recorded, ask which concept to work on, and run in-session.

## Rules

- One move per run. Another move is another run.
- The **rung** is a position on the worked → faded → independent ladder; **cleared** means the independent rung passed with no hints. Use these words and no synonyms.
- Record every attempt in `PROGRESS.md` with the line shape above. Missed concepts are not cleared.

Reference detail for item shape and rubrics is in [references/DRILL-FORMAT.md](references/DRILL-FORMAT.md).
