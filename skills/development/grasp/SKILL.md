---
name: grasp
description: Use when the user asks to explain or understand a code change, diff, branch, or PR — or to catch up on a change an agent built before reviewing or shipping it. Triggers on "what changed here", "walk me through what you built", "help me understand this before merging".
---

# grasp

The reader is not verifying — they're staying a participant. Understanding is what lets them have the next idea. Build it the way education does.

## Before writing

Explore the surrounding system, not just the diff.

## Sections, in order

1. **Background** — the system as it was. Two layers: deep context a newcomer needs (marked skippable), then the narrow slice this change touches.
2. **Intuition** — the goal and the core idea before any code. Concrete examples with toy data. A small family of diagrams reused throughout — never ASCII.
3. **Code** — a literate walkthrough: conceptual order, not file order; prose that embeds the key snippets.
4. **Quiz** — five multiple-choice questions on the substance of the change. Medium difficulty: answerable only with real understanding, no gotchas. Every option gets feedback explaining why it's right or wrong — hidden until the reader commits to an answer.

## The quiz is a speed regulator

Invite the reader to hold the change until they pass — shipping past a failed quiz banks cognitive debt. Feedback per question only; never a score, streak, or grade.

## Format

- Medium is the user's call. Default: one self-contained HTML file outside the repo, named `YYYY-MM-DD-<slug>.html` — one long page, never tabs; quiz interactive.
- Write with the clarity and flow of Martin Kleppmann — smooth transitions, callouts for key concepts and edge cases.
- Code blocks keep their newlines: `<pre>`, or `white-space: pre-wrap` on styled divs.
