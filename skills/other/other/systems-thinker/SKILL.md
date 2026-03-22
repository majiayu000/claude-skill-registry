---
name: systems-thinker
description: Understand complex systems, interconnections, and emergent behaviors
category: Thinking Analysis
---

# Skill: systems-thinker

## What I do

I analyse software and organisations as interconnected systems. I identify feedback loops, second-order effects, and leverage points to ensure that changes improve the system as a whole rather than just optimising a single part.

## When to use me

- When designing distributed systems or microservices
- To analyse the root cause of systemic issues or performance bottlenecks
- When evaluating the impact of a change on downstream systems
- To identify and mitigate unintended consequences of a proposal

## Core principles

1. **Feedback loops** — Identify reinforcing (amplifying) and balancing (stabilising) loops that drive system behaviour.
2. **Second-order effects** — Ask "and then what?" to anticipate the downstream consequences of a change.
3. **Leverage points** — Find the small changes that can lead to large improvements in system performance.
4. **Emergent behaviour** — Understand that complex systems exhibit behaviours that cannot be predicted by looking at individual components in isolation.

## Patterns & examples

**Causal Loop Diagram (Simplified):**
- **Action:** Increase test coverage.
- **Immediate Effect:** More bugs found early.
- **Second-order Effect:** Fewer production incidents.
- **Long-term Effect:** Higher developer confidence and faster feature delivery (Reinforcing Loop).

**System Leverage Points:**
- **Low Leverage:** Tweaking parameters (e.g. changing a timeout value).
- **Medium Leverage:** Changing system structure (e.g. moving from synchronous to asynchronous communication).
- **High Leverage:** Changing the goals of the system (e.g. prioritising resilience over raw throughput).

## Anti-patterns to avoid

- ❌ **Siloed optimisation** — Improving one component at the expense of the overall system (e.g. making a service extremely fast by overloading the database).
- ❌ **Linear thinking** — Assuming that every effect has a single, direct cause.
- ❌ **Ignoring delays** — Failing to account for the time it takes for a change to ripple through the system.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Thinking-Analysis/Systems Thinker.md`

## Related skills

- `critical-thinking` — Foundation for system analysis
- `retrospective` — Learning from systemic failures
- `architecture` — Applying systems thinking to design
- `trade-off-analysis` — Weighing system-wide impacts
