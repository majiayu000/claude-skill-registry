---
name: additive-bias-defense
description: >-
  Cross-cutting contract that inverts burden of proof
  for code additions. Use when reviewing proposed
  additions or detecting LLM additive-bias patterns.
version: 1.9.3
alwaysApply: false
category: quality-contract
tags:
- additive-bias
- burden-of-proof
- scrutiny
- cross-cutting
- defense
dependencies: []
tools: []
provides:
  contract:
  - additive-bias-scrutiny
  - burden-of-proof-verdict
usage_patterns:
- plan-review
- pr-review
- code-refinement
- unbloat
complexity: foundational
model_hint: standard
estimated_tokens: 800
role: library
---

> The default answer to "should we add this?" is no.
> The burden of proof is on the addition.

# Additive Bias Defense

## The Problem

LLMs are additive by nature. They reinvent wheels, add
unnecessary complexity, hallucinate issues and modify
tests to justify them, and deviate from priorities. This
contract provides a systemic defense.

## The Scrutiny Questions

Applied to every proposed addition -- code, files,
abstractions, error handling, configuration:

1. **Priority alignment**: Is this a deviation from the
   current priority?
2. **Criticality**: Is it critical to implement at this
   juncture?
3. **Simplicity**: Does a simpler or more elegant
   solution exist?
4. **Evidence**: What evidence proves this is needed
   (not assumed)?
5. **Consequence**: What breaks if we do not add this?

If the proposer cannot answer questions 4 and 5 with
concrete evidence, the addition is unjustified.

## Anti-Pattern Detection

| Pattern | Signal | Challenge |
|---------|--------|-----------|
| Wheel reinvention | New utility/helper overlapping existing code | "Does X already do this?" |
| Hallucinated issues | Fix for a bug with no reproduction evidence | "Show the failing test before the fix" |
| Test manipulation | Test changed to match behavior rather than spec | "Did the spec change, or did you change the test?" |
| Complexity creep | Abstraction introduced for single use case | "Is this the 3rd use, or the 1st?" |
| Priority deviation | Work not traceable to current task/spec | "Which requirement does this serve?" |
| Gold plating | Error handling or flexibility beyond need | "What breaks without this?" |

## Burden of Proof Verdict

After applying scrutiny questions and anti-pattern
detection, produce a verdict:

| Verdict | Meaning | Action |
|---------|---------|--------|
| `justified` | Evidence supports the addition | Proceed |
| `needs_evidence` | Plausible but unproven | Provide evidence or remove |
| `unjustified` | No evidence, likely bias | Remove or justify |

## Integration Contract

Review-oriented skills MUST consult this contract by:

1. Applying the 5 scrutiny questions to each addition
2. Scanning for the 6 anti-patterns
3. Producing a burden-of-proof verdict
4. Including the verdict in their output

### Consuming Skills

| Skill | Integration Point |
|-------|-------------------|
| `attune:war-room` | Prosecution Counsel role uses scrutiny questions |
| `sanctum:pr-review` | Every added file/function challenged |
| `pensive:code-refinement` | Refactors pass "3rd use" test |
| `conserve:unbloat` | Findings feed removal candidates |
| `attune:mission-orchestrator` | Plan sections scanned before user review |
| `imbue:justify` | Scrutiny questions extend audit protocol |

## Related Skills

- `imbue:karpathy-principles` - "Simplicity First" and "Surgical Changes" principles invoke this contract from a higher-level four-principle synthesis
- See `docs/quality-gates.md#skill-level-quality-gate-composition` for the full gate-skill federation graph

## The Subtraction Principle

> Rely less on AI and initial lines of thinking.
> Challenge yourself to think of a more elegant
> implementation or a simpler solution.

Before accepting any addition, ask: "Could I achieve
this by removing code instead of adding it?" If yes,
prefer the subtractive approach.
