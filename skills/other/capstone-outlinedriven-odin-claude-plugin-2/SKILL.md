---
name: capstone
description: 'Use when the learner is ready to apply cleared concepts in a real project. Not for exercises or quizzes: use drill.'
---

# Capstone

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The learner is ready to apply cleared concepts in a real project and invokes this skill. |
| Authority | Reversible local: writes only `capstone-<slug>.md` at the workspace root; rollback is deleting the brief file. No remote mutation. |
| Side effect | Creates or updates `capstone-<slug>.md` at the workspace root and nothing else; never writes progress lines or edits any progress record. |
| Done | The brief exists at `capstone-<slug>.md` and follows the format; after the learner returns, the work is judged per item against the brief; concepts the work does not demonstrate are named for practice. |

## Inputs

- `PROGRESS.md` at the workspace root listing cleared concepts. Required for scoping; a concept counts as cleared only when its independent rung passed with no hints.
- The domain or goal the project serves. Required; take it from the invocation argument when the argument carries it, otherwise ask once.
- The learner's finished work. Required only for the review stage, which happens when the learner returns with it.

## Procedure

1. Scope one project. Read `PROGRESS.md` and collect the cleared concepts. If `PROGRESS.md` does not exist, ask once what the learner can already do without help, treat the answer as the cleared set, and do not ask again. **Done when:** the cleared concept set is collected from PROGRESS.md or the learner's one answer.
2. Bound the project before writing anything. It may use only cleared concepts plus at most one unfamiliar concept; with two or more unfamiliar concepts it is a tutorial, so cut scope until at most one remains. The deliverable must be something runnable, readable, or usable; anything smaller is an exercise, so say so and stop rather than write a brief. **Done when:** the project is bounded to cleared concepts plus at most one unfamiliar, and the deliverable is runnable, readable, or usable.
3. Order the milestones so each one leaves something that works. **Done when:** milestones are ordered with each leaving a working intermediate.
4. Write `capstone-<slug>.md` at the workspace root, `<slug>` derived from the project name, carrying these things: the concepts exercised (the cleared set plus the one unfamiliar concept, if any), the ordered milestones, and the done test. The done test is observable by someone else; "Understand X" is not a done test; state a result another person can check. **Done when:** the brief file exists with concepts, milestones, and an observable done test.
5. Yield to the learner. After the brief is written, stop and hand the learner the brief file path and the done test. The learner leaves to do the project; no further work happens in this session. The review stage begins only when the learner returns in a later turn or session with finished work. **Done when:** the brief path and done test are handed to the learner and the turn ends.
6. Review on return. When the learner brings the finished work back, judge it against the brief's done test and concept list item by item, one verdict per concept and per milestone, no overall impression in place of items. **Done when:** every concept and milestone has a per-item verdict.
7. Name every concept the work does not demonstrate as not cleared and give that list to the learner as practice items. Record nothing: this skill writes no progress lines, and ownership of any progress record stays outside it. **Done when:** the not-cleared concepts are named and handed to the learner as practice items.

## Failure and recovery
- Cannot scope: no cleared concepts and no usable answer to the one question about what the learner can do. Stop and report that a capstone cannot be sized; write nothing and invent no syllabus.
- Tutorial cutoff: scoping needs two or more unfamiliar concepts. Stop, report the cutoff, and propose a smaller project or classify the request as an exercise; do not write a tutorial brief.
- Unusable deliverable: the returned work cannot be run, read, or used. Report the done test as failed per item; do not pass it or soften the verdict.
- Partial judgment: if review stops partway through the item list, keep the per-item verdicts already reached and report exactly those; never report the whole work passed or failed without per-item evidence.
- Rollback: delete `capstone-<slug>.md`. If scoping or bounding failed after the brief was written, delete it rather than leave a brief that violates the bounds.

## Output
`capstone-<slug>.md` at the workspace root with the concepts exercised, working milestones, and an observable done test; then, on the review visit, a per-item verdict against that done test and concept list and the named not-cleared concepts handed to the learner as practice items. No progress record is written by this skill.
