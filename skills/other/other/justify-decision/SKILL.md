---
name: justify-decision
description: Provide evidence-based justification for architectural and design decisions
category: Thinking Analysis
---

# Skill: justify-decision

## What I do

I provide clear, structured rationale for technical choices. I focus on evidence, context, and consequences, ensuring that decisions are documented and defensible rather than based on mere opinion or habit.

## When to use me

- When proposing a significant change to the architecture
- When choosing between multiple competing libraries or frameworks
- During the creation of Architectural Decision Records (ADRs)
- When explaining a complex design choice to stakeholders

## Core principles

1. **Evidence over opinion** — Use benchmarks, documentation, or historical data to support claims.
2. **Context is king** — Explain the specific constraints and requirements that led to the decision.
3. **Consequence awareness** — Explicitly state what we are gaining AND what we are giving up (technical debt, complexity, etc.).
4. **Distinguish reversibility** — Identify if a decision is a "one-way door" (hard to undo) or a "two-way door" (easy to pivot).

## Patterns & examples

**ADR-Style Justification:**
- **Context:** We need to handle 10k concurrent WebSocket connections on a single node.
- **Decision:** Use Elixir/Phoenix instead of Node.js.
- **Evidence:** BEAM VM's lightweight process model and built-in distribution primitives.
- **Consequences:** Team needs to learn a new language; better fault tolerance; lower operational overhead.

**Decision Confidence Matrix:**
- **High Confidence:** Backed by production data or extensive spike results.
- **Medium Confidence:** Backed by industry standard practices and documentation.
- **Low Confidence:** Based on theoretical advantages; requires early validation.

## Anti-patterns to avoid

- ❌ **Post-hoc rationalisation** — Making a choice based on preference then looking for evidence to support it.
- ❌ **Ignoring alternatives** — Presenting a decision as the only option without acknowledging valid competitors.
- ❌ **Vague justifications** — Using terms like "industry standard" or "best practice" without explaining why they apply here.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Thinking-Analysis/Justify Decision.md`

## Related skills

- `trade-off-analysis` — Weighing options before justifying
- `documentation-writing` — Recording the justification clearly
- `critical-thinking` — Validating the logic of the justification
- `architecture` — Applying justifications to system design
