---
name: assumption-tracker
description: Explicitly track, test, and validate assumptions - prevent blind spots
category: Thinking Analysis
---

# Skill: assumption-tracker

## What I do

I surface and manage hidden assumptions. I ensure that every leap of faith in a design or plan is documented, tiered by risk, and systematically validated through evidence or testing.

## When to use me

- Before starting a new feature or architectural change
- When requirements are ambiguous or "common sense" is invoked
- During technical planning sessions to identify "we think" vs "we know"
- When evaluating third-party libraries or external API behaviours

## Core principles

1. **Surface the hidden** — If it isn't proven, it's an assumption.
2. **Tier by risk** — Focus validation on assumptions with high impact and low certainty.
3. **Validate early** — Use spikes, prototypes, or data lookups to turn assumptions into facts.
4. **Document outcomes** — Record whether an assumption was proven true or false.

## Patterns & examples

**Assumption Logging Format:**
| Assumption | Impact (H/M/L) | Certainty (H/M/L) | Validation Method | Status |
| :--- | :--- | :--- | :--- | :--- |
| "The legacy API supports concurrent writes." | High | Low | Run concurrency spike test | Pending |
| "Users prefer the sidebar over the top nav." | Medium | Medium | Review GA click maps | Validated |

**Validation Techniques:**
- **Spike:** Write a small, throwaway script to test a technical hypothesis.
- **Prototype:** Build a minimal UI to verify user interaction assumptions.
- **Data Lookup:** Query logs or databases to confirm usage patterns.

## Anti-patterns to avoid

- ❌ **"Trust me" logic** — Relying on seniority instead of evidence.
- ❌ **Validation lag** — Building a full system on unverified, high-risk assumptions.
- ❌ **Silent assumptions** — Failing to voice doubts during the planning phase.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Thinking-Analysis/Assumption Tracker.md`

## Related skills

- `critical-thinking` — Rigorous analysis of claims
- `epistemic-rigor` — Distinguishing belief from knowledge
- `prove-correctness` — Evidence-based validation
- `pre-action` — Deliberate thinking before execution
