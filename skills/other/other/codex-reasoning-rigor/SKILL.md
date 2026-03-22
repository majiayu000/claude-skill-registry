---
name: codex-reasoning-rigor
description: Force deliberate, evidence-backed, non-generic reasoning for complex engineering work. Use when the user asks for deeper thinking, less generic output, higher specificity, better workflow discipline, monitoring plans, or stronger quality-oriented delivery instead of shallow best-practice answers.
---

# Codex Reasoning Rigor

## Overview

Use this skill to turn vague or generic model behavior into explicit decision-making, repo-grounded evidence gathering, and output contracts that are concrete enough to verify.
Activate it when the task is important enough that "sounds right" is not good enough.

## Activation

Activate on explicit `$codex-reasoning-rigor` or `$rigor`.

Activate when the user says or implies:

- "don't be generic"
- "think harder" or "go deeper"
- "make it specific"
- "I need better workflow / monitoring / output quality"
- "give me tradeoffs, not vague advice"
- "show evidence"
- "use the repo, not generic training data"

Also activate for:

- architecture or refactor decisions with hidden risk
- reviews that need actionable findings instead of summaries
- operational plans that need monitoring signals and stop/ship criteria
- repeated tasks where model output has drifted or become bland

## Core Protocol

Run this protocol before answering or implementing:

### 1. Task Contract

Lock these fields explicitly:

- `goal`: what outcome must change
- `constraints`: what cannot change
- `non_goals`: what should stay out of scope
- `evidence_required`: what proof would make the answer credible
- `quality_bar`: what would make the output clearly non-generic

If the task is complex, generate a brief with `scripts/build_reasoning_brief.py`.
By default the brief generator now requires those reasoning fields; use `--allow-placeholders` only when you intentionally want a scaffold.

### 2. Decision Surface

Do not jump straight to one answer.
Frame at least 2 options whenever the task has hidden tradeoffs.

For each option, compare:

- why it could work here
- cost or blast radius
- failure modes
- what evidence would confirm or reject it

### 3. Repo Grounding

Anchor the answer in concrete artifacts whenever possible:

- real file paths
- real commands
- actual counts, versions, or dates
- existing scripts, references, or templates
- diffable outputs instead of abstract advice

Use [references/evidence-ladder.md](references/evidence-ladder.md) to keep evidence quality high.

### 4. Monitoring Lens

Every serious workflow or recommendation should state:

- what to watch
- what "healthy" looks like
- what drift or failure looks like
- what to do next if the signal goes red

Use [references/monitoring-loops.md](references/monitoring-loops.md) when the task affects delivery, release quality, or repeated execution.

### 5. Output Contract

Before finishing, make the output earn its credibility.
Use [references/output-contracts.md](references/output-contracts.md) and check that the result includes:

- the chosen path
- evidence or commands that support it
- risks or open questions
- next steps or exit criteria

## Anti-Generic Rules

Never end at "best practices", "ensure", "optimize", "improve quality", or similar filler unless you immediately attach:

- a named artifact
- a concrete command
- a specific file or boundary
- a measurable condition
- a reason this matters in this repo or workflow

Use [references/anti-generic-patterns.md](references/anti-generic-patterns.md) when the answer starts sounding interchangeable with any other project.

## Working Pattern

For medium or high-stakes work:

1. Build a reasoning brief.
2. Name the decision surface.
3. Ground the answer in repo artifacts.
4. State the monitoring loop.
5. Run an output-quality pass with `$output-guard` before declaring the work complete.
6. For plans, reviews, and handoffs, add an editorial pass with `$editorial-review` so the result reads like a human-made engineering deliverable instead of safe model prose.

For plans, reviews, and handoffs, treat strict output validation as the default quality bar, not an optional extra.

## Resources

- `scripts/build_reasoning_brief.py`: generate a structured execution brief for complex, high-signal work.
- `references/anti-generic-patterns.md`: common signs of generic output and concrete repair moves.
- `references/evidence-ladder.md`: how to rank evidence from weak intuition to strong verification.
- `references/monitoring-loops.md`: how to attach health signals and follow-up actions to workflows.
- `references/output-contracts.md`: response shapes that push outputs toward specificity and accountability.
- `assets/reasoning-brief-template.md`: markdown template used by the brief generator.
- `assets/output-review-template.md`: template for reviewing whether a deliverable is specific enough.
- `assets/output-review-template.md`: template for reviewing whether a deliverable is specific, accountable, and editorially strong enough.
- `assets/monitoring-checklist-template.md`: template for tracking healthy vs drifting workflow signals.
