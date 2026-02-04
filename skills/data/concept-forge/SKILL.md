---
name: concept-forge
description: Score concepts on impact/delight/effort and pick a 1-day spike.
license: MIT
command: /ctx:concept-forge
---

# `/collaboration:concept-forge`

Use after you have a handful of ideas and need to pick what to test first.

## Inputs
- Problem statement
- Scoring axis (impact|delight|effort)
- Constraints to honor

## Steps
1. Capture problem, success signals, constraints.\n2. Generate 4–6 concept cards with Impact (1–5), Delight (1–5), Effort (S/M/L), Risks, 1-day Spike.\n3. Rank by chosen axis (tie-breaker: lowest effort).\n4. Recommend top card + spike and list verification steps.\n5. Seed Tasks or hand off to `/ctx:plan` for execution.

## Output Template
```
### Problem
### Success Signals
### Constraints
### Concept Cards (ranked)
- Concept … (impact, delight, effort, risks, 1-day spike)
### Recommended Spike
### Verification Checklist
```

## Pairings
- Precede with `/collaboration:idea-lab` or `/collaboration:mashup` to generate options.
- Follow with `/collaboration:pre-mortem` to de-risk the chosen concept.
