---
name: assumption-buster
description: Flip, remove, or exaggerate assumptions to unlock new solution angles.
license: MIT
command: /ctx:assumption-buster
---

# `/collaboration:assumption-buster`

Use when the team feels boxed in or every idea sounds the same.

## Inputs
- Topic or problem statement
- Known assumptions/constraints (even if informal)
- Optional mode flag: `--opposite`, `--zero`, or `--10x`

## Steps
1. List core assumptions (facts, beliefs, constraints).
2. Transform each via chosen operator (opposite/zero/10x).
3. Generate 1–2 reframed ideas per transformed assumption.
4. Capture evidence to collect and a fast test for each idea.
5. Pick the most promising 2–3 and move to `/ctx:plan` or Tasks.

## Output Template
```
### Assumptions
### Transforms (opposite/zero/10x)
### Reframed Ideas
- Idea … (evidence, fast test)
### Top Picks
```

## Pairings
- Run before `/collaboration:idea-lab` if you need to loosen constraints.
- Feed winners into `/collaboration:concept-forge` to score/prioritize.
