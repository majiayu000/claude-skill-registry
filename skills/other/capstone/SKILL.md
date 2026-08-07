---
name: capstone
description: 'Use when the user is ready to apply what they learned to something real: scope a project sized to what they have cleared, write the brief with milestones and a done test, then judge the finished work against it. For single-concept exercises and quizzes, use drill.'
argument-hint: "What should the project build?"
---

Turn what the learner has cleared into something runnable, readable, or usable. One project per run.

## Scope it

Read `PROGRESS.md` for what is **cleared** (its independent rung passed with no hints). The project may use only cleared concepts plus at most one unfamiliar one; two or more and it is a tutorial. Ask for the domain when the argument does not carry it. No `PROGRESS.md` means ask what the user can already do, once, and size to the answer.

## The brief

Write the brief to `capstone-<slug>.md` at the workspace root, per [references/BRIEF-FORMAT.md](references/BRIEF-FORMAT.md). The brief carries the done test, the milestones, and the concepts exercised.

## Review it

When the learner brings the finished work back, judge it against the done test and the concept list item by item, then name the concepts the work shows they have not cleared. Hand those to `drill`, which owns the record; this skill writes no progress lines.

## Rules

- The done test is observable by someone else. "Understand X" is not a done test.
- The project produces something runnable, readable, or usable. Anything smaller is an exercise; send it to `drill`.
- Review against the brief's done test and concept list, item by item.
- Order milestones so each one leaves something that works.
