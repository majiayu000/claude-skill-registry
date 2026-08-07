---
name: explain-concept
description: 'Use when a concept needs making clear rather than practising: build the intuition, explain why it exists and what it replaced, trace where it came from, draw it, or contrast it against what it gets confused with. For exercises and grading, use drill.'
argument-hint: "Which concept — intuition, motivation, origin, picture, or contrast?"
---

One concept, one angle per run. The table picks the angle unless the argument names it directly.

## Pick the angle

An explicit argument overrides the table; no match means **intuition**.

| The user asks | Angle |
|---|---|
| "what is really going on", "I don't get it", "explain it simply" | intuition |
| "why does this exist", "what problem does it solve", "why not just X" | motivation |
| "where did this come from", "who came up with it", "what did it replace" | origin |
| "draw it", "show me", "what does it look like" | picture |
| "what is the difference", "when do I use X instead of Y" | contrast |

## intuition

One analogy drawn from something the learner already owns, the smallest example showing the behaviour, and the one sentence that survives when they forget the rest. Then stop and ask them to restate it in their own words. Done when the restatement exists and has been confirmed or corrected. One screen.

## motivation

What people did before this existed, where that broke, what this buys, what it costs. Leave history to the origin angle. Done when all four are on the page and the cost is real rather than a token concession. One screen.

## origin

Who, when, what it displaced, one citation the learner can go read. The search and approval protocol is in [references/ORIGIN-SEARCH.md](references/ORIGIN-SEARCH.md). Done when a citation is on the page or the user declined the search. Fifteen lines. Asked for alongside the intuition, run the intuition first: the evidence that history teaches is thin, so this is a hook rather than a prerequisite, and saying so when the user opens here is part of the angle.

## picture

One diagram, authored per the `diagram-contract` skill: nomnoml for structure and flow, D2 for architecture, house palette, rendered SVG committed beside its source in `assets/`. Done when the render exits zero and the embed carries its alt text and caption. A concept with no structure, flow, or architecture worth drawing gets one line saying so instead; a box drawn around a definition costs attention and returns nothing.

## contrast

A table whose rows are the properties where the items differ, plus one line per item saying when to reach for it. Done when every row separates rather than shares, and at least one row is a difference with a consequence the learner can act on.

## Rules

- One angle per run. Another angle is another run.
- Ask the learner to say why a step is taken before revealing the reason.
- Cite the corpus anchor for every claim about the concept when `CORPUS.md` exists. When a claim is not in the corpus, say so in the sentence that makes it.
- No `CORPUS.md` means ask which source to ground in, once, then proceed.
