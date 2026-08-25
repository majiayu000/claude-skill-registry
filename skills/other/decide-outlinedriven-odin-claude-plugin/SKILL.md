---
name: decide
description: 'Use when the user has a fork and wants it resolved and applied, not explored: "help me decide", "just decide this", "what should I do here", "decide and fix it". Frames each fork as one single-select with a recommended default, takes the pick, and applies it. Requirement exploration that ends in a document goes to askme; a verdict on adopting a technology goes to pov.'
argument-hint: "What is the fork?"
---

# Decide

The user owns the pick, you own the framing and the execution. Two failure modes sit on either side: deciding for them, which is `pov`, and asking without ever acting, which is `askme`. This skill closes the seam between them, and nothing shipped does the whole loop, because `askme`, `clarify`, and `brainstorm` all terminate in an artifact while `fix` acts without asking.

## Ground the fork before framing it

Resolve from evidence first with `grep`, `glob`, `read`, or `lsp`. A fork the code already answers is not a fork: read it, say what it answers, and do not ask. Never ask what a search settles.

## Frame it

Question contract: `skills/askme/SKILL.md:64-127`. One single-select per axis, two to four options, `(Recommended)` first with the consequence in its description. Never `multiSelect` for override semantics, an antipattern spelled out at `skills/askme/SKILL.md:68-101`.

## Options carry consequences, not labels

Each option names what the code looks like afterwards. Where two options differ visibly, put the difference in `preview` as a diff or a tree.

## Take the pick and act in the same turn

A pick applied in one edit gets the edit. A pick needing a verify, keep, or revert loop goes to `fix`, with the pick restated as its goal. A pick that removes an observable surface or cannot be reverted from git gets one concern stated, then a yes.

## Chained forks

When applying one pick opens the next, ask it immediately with the settled decision restated in one line. Never bank a queue of questions to fire at the end.

## When the user picks what you would not

Execute the pick, state the concern once, never re-litigate.

## Close

One line naming the fork, the pick, and what changed.

## Boundaries

- A verdict of your own goes to `pov`.
- An exploration ending in a document goes to `askme`.
- A whole-session director-executor posture goes to `duet`.
- A wide design tree in batched rounds goes to `batch-ask-me`.
- Ambiguity inside a stated request rather than a fork goes to `clarify`.
