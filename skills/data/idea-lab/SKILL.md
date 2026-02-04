---
name: idea-lab
description: Timeboxed divergent ideation that outputs ranked options plus day-one experiments.
license: MIT
command: /ctx:idea-lab
---

# `/collaboration:idea-lab`

Use this when you need many angles fast and want to leave with 1-day experiments queued.

## Inputs
- Topic or problem statement
- Constraints (time, platform, compliance, budget)
- Any existing assets to reuse

## Steps
1. State the timebox (default 15m).\n2. Capture goal, success signals, constraints, assets.\n3. Generate 5–7 distinct concepts with Wow-Factor, Feasibility (S/M/L), Dependency to check.\n4. Select Top 3 to test today; assign a 1-day experiment to each.\n5. Seed Task view or hand off to `/ctx:plan`.

## Output Template
```
### Problem / Goal
### Success Signals
### Constraints
### Existing Assets
### Options (table)
| Concept | Wow-Factor | Feasibility | Dependency to Check |
|---------|------------|-------------|---------------------|
### Top 3 Experiments
### Next Steps
```

## Resources
- See `modes/Idea_Lab.md` for tone cues.\n- Pair with `/ctx:plan` after choosing the top experiment.\n- Use `/collaboration:assumption-buster` first if the problem is sticky.
