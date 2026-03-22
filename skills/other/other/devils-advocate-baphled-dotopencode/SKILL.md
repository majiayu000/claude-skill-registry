---
name: devils-advocate
description: Challenge ideas, find weaknesses, and stress-test solutions before implementation
category: Thinking Analysis
---

# Skill: devils-advocate

## What I do

I deliberately challenge proposals, designs, and decisions to uncover hidden flaws. I use adversarial thinking to stress-test solutions and ensure they are robust enough to survive real-world conditions.

## When to use me

- During architectural reviews to find failure modes
- Before committing to a specific design or library
- To combat groupthink or "happy path" bias in planning
- When a proposal seems too good to be true

## Core principles

1. **Adversarial thinking** — Assume the design will fail. How does it happen?
2. **Steelmanning first** — Understand the proposal perfectly before trying to break it.
3. **Pre-mortem analysis** — Project into the future: the project failed. What were the causes?
4. **YAGNI enforcement** — Challenge whether a feature or complexity is actually necessary right now.

## Patterns & examples

**Pre-mortem Template:**
- **Scenario:** The new microservice deployment caused a total system outage.
- **Probable Causes:** Circular dependencies, lack of circuit breakers, incorrect timeout settings.
- **Mitigation:** Implement Hystrix-style patterns, audit dependency graph.

**Challenge Patterns:**
- **Scale:** "What happens if traffic increases by 100x?"
- **Partial Failure:** "What if the database is up but extremely slow?"
- **Security:** "How could an authenticated user abuse this endpoint?"
- **Complexity:** "Could we achieve 80% of this with 20% of the code?"

## Anti-patterns to avoid

- ❌ **Being a blocker** — Critiquing without offering paths to improvement.
- ❌ **Nits over substance** — Focusing on trivial details instead of fundamental design flaws.
- ❌ **Personal bias** — Challenging ideas based on preference rather than objective risk.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Thinking-Analysis/Devils Advocate.md`

## Related skills

- `critical-thinking` — Foundation for rigorous analysis
- `assumption-tracker` — Surfacing what needs to be challenged
- `systems-thinker` — Understanding how challenges ripple through the system
- `trade-off-analysis` — Weighing the costs of robustness
