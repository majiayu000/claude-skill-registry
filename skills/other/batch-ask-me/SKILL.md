---
name: batch-ask-me
description: 'Use when the user wants to walk a complex design space round by round: map the decision tree, fire the current frontier as batched single-select questions, and loop until shared understanding is reached. Triggers: multi-fork decisions, ambiguous requirements, unresolved prerequisites, "batch ask me", "clarify the design space".'
---

# Batch Ask Me

Walk a complex decision space with the user in **rounds**, using a **design tree** to keep every question dependency-respecting. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask *now* without guessing at answers you haven't heard yet.

Each round, ask the whole frontier as a batch of single-select questions, each with a recommended answer. Wait for the user's answers, then recompute the frontier and ask the next round. A question whose answer depends on another open question belongs to a later round, not this one.

Finding *facts* is your job, not the user's. When a frontier question needs an environmental fact (filesystem, tools, codebase, etc.), dispatch a sub-agent to find it; never ask the user for something you could look up yourself. A running exploration is an unsettled prerequisite; only its downstream questions wait, so ask the rest of the frontier now.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on the result until the user confirms you have reached a shared understanding.

## Verbalized Sampling

Before round one, run Verbalized Sampling (VS) to ground the design tree:
1. Sample multiple intent hypotheses, each with an explicit weight (0 to 1 scale) and a concrete falsifier.
2. Present the weighted hypotheses and falsifiers visibly immediately before the first question batch.
3. Seed the roots of the design tree and the initial frontier using the surviving hypotheses.

Do not resample VS on subsequent rounds unless user answers materially change the survivor set. If resampling is triggered, update the survivor set, adjust the design-tree roots, and recompute the frontier.

## Question shape

Follow the `AskUserQuestion` contract and override-checklist antipattern from `skills/askme/SKILL.md`: one single-select question per axis, mark the recommended option first with `(Recommended)`, at most four questions per fire, and never use `multiSelect` for override semantics.

## Distinction from `askme`

Both start with Verbalized Sampling. `askme` uses the survivor set for one bounded clarifying batch; `batch-ask-me` uses it to seed a design tree, then walks every frontier until the user confirms shared understanding.
