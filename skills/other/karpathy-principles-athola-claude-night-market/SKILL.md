---
name: karpathy-principles
description: Pre-implementation gate covering think-first, simplicity, surgical edits, and verifiable goals. Use when starting implementation to verify the approach.
alwaysApply: false
category: discipline
tags:
- karpathy
- coding-pitfalls
- synthesis
- entry-point
- discipline
- anti-overengineering
- TDD
dependencies:
- imbue:scope-guard
- imbue:proof-of-work
- imbue:rigorous-reasoning
- leyline:additive-bias-defense
- conserve:code-quality-principles
tools: []
usage_patterns:
- pre-implementation-gate
- code-review
- diff-hygiene
- task-reformulation
complexity: foundational
model_hint: standard
estimated_tokens: 900
modules:
- modules/anti-patterns.md
- modules/senior-engineer-test.md
- modules/verifiable-goals.md
- modules/tradeoff-acknowledgment.md
references:
- references/source-attribution.md
role: entrypoint
---

> The models make wrong assumptions on your behalf and
> just run along with them without checking. They don't
> manage their confusion, don't seek clarifications,
> don't surface inconsistencies, don't present
> tradeoffs, don't push back when they should.
>
> -- Andrej Karpathy, on agentic coding failure modes

## What This Is

A four-principle contract for reducing the most common
LLM coding pitfalls. Compact entry-point. Each
principle has a deeper-dive skill in night-market;
this skill is the index, not the encyclopedia.

Derivation: distilled by Forrest Chang
(forrestchang/andrej-karpathy-skills, MIT) from
Karpathy's observations. Full attribution in
`references/source-attribution.md`.

## When to Use

- Before starting any coding task larger than a typo
- During code review, to name the failure mode you see
- After writing a diff, to self-audit before claiming
  done
- When training a junior engineer to read agent diffs

## When NOT to Use

These principles bias toward caution over speed. For
cases listed in `modules/tradeoff-acknowledgment.md`,
use judgment: trivial fixes, exploratory spikes,
documentation-only edits, and time-boxed prototypes.

## The Four Principles

### 1. Think Before Coding

**State assumptions. Surface confusion. Match tone to
evidence.**

- If multiple interpretations of the request exist,
  list them. Do not silently pick.
- If a simpler approach exists, name it. Push back
  when the simpler path is correct.
- If something is unclear, stop and ask. Hidden
  assumptions are the cheapest bug to prevent and the
  most expensive to find later.
- Make claims no stronger than the evidence supports.
  Calibrated tone beats confident hand-waving.

Deep dives: `Skill(imbue:rigorous-reasoning)` for the
sycophancy guard, `Skill(superpowers:brainstorming)`
for option generation, `/spec-kit:speckit-clarify`
command for ambiguity drilldown.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing
speculative.**

> They really like to overcomplicate code and APIs,
> bloat abstractions.
>
> -- Andrej Karpathy, on the same agentic-coding thread



- No features beyond what was asked
- No abstractions for single-use code
- No flexibility or configurability that wasn't
  requested
- No error handling for impossible scenarios
- If you wrote 200 lines and it could be 50, rewrite
  it

Self-check: would a senior engineer say this is
overcomplicated? See `modules/senior-engineer-test.md`.

Deep dives: `Skill(imbue:scope-guard)` for the
worthiness formula and branch budgets,
`Skill(leyline:additive-bias-defense)` for burden of
proof on every addition,
`Skill(conserve:code-quality-principles)` for the
KISS / YAGNI / SOLID foundation.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own
mess.**

- Do not improve adjacent code, comments, or
  formatting
- Do not refactor things that aren't broken
- Match existing style even when you would do it
  differently
- If you notice unrelated dead code, mention it; do
  not delete it
- When your changes orphan imports or variables,
  remove the orphans you created. Pre-existing dead
  code stays unless asked.

The trace-back test: every changed line should trace
directly to the user's request.

Deep dives: `Skill(imbue:justify)` for additive-bias
audits on diffs, `Skill(leyline:additive-bias-defense)`
for the burden-of-proof contract, the
`bounded-discovery.md` rule for read-budget caps.

### 4. Goal-Driven Execution

**Define verifiable success criteria. Loop until
verified.**

Transform vague tasks into checkable goals:

- "Add validation" becomes "tests for invalid inputs
  pass"
- "Fix the bug" becomes "test reproducing the bug,
  then make it pass"
- "Refactor X" becomes "tests pass before and after"
- "Make it faster" becomes "benchmark Y under N ms"

For multi-step tasks, state a brief plan with
verification per step. Strong success criteria let
you loop independently. Weak criteria require
constant clarification.

See `modules/verifiable-goals.md` for the full
reformulation template.

Deep dives: `Skill(imbue:proof-of-work)` for the Iron
Law (no implementation without a failing test first),
`Skill(superpowers:test-driven-development)` for the
RED-GREEN-REFACTOR loop.

## The Karpathy Self-Check

Before you ship, four questions:

| Principle | Question |
|-----------|----------|
| Think Before Coding | Did I list assumptions, or did I guess silently? |
| Simplicity First | Would a senior engineer call this overcomplicated? |
| Surgical Changes | Does every changed line trace to the request? |
| Goal-Driven Execution | Can I prove this is done with a check, not a feeling? |

Four "yes" answers means ship. Anything else means
iterate.

## Modules

- `modules/anti-patterns.md` - eight named drift rails
  with before/after diffs
- `modules/senior-engineer-test.md` - the
  three-question self-check battery
- `modules/verifiable-goals.md` - vague-to-verifiable
  reformulation template with worked examples
- `modules/tradeoff-acknowledgment.md` - when the four
  principles do not apply

## References

- `references/source-attribution.md` - Karpathy
  primary citation, Forrest Chang derivation, license,
  adjacent prior art

## Related Skills

- `Skill(imbue:scope-guard)` - worthiness formula and
  branch budgets
- `Skill(imbue:proof-of-work)` - Iron Law TDD gate
- `Skill(imbue:rigorous-reasoning)` - sycophancy and
  hidden-assumption guard
- `Skill(imbue:justify)` - additive-bias diff audit
- `Skill(leyline:additive-bias-defense)` - burden of
  proof on every addition
- `Skill(conserve:code-quality-principles)` - KISS,
  YAGNI, SOLID
- `Skill(superpowers:test-driven-development)` -
  RED-GREEN-REFACTOR
- `Skill(superpowers:brainstorming)` - generate
  options before committing
- See `docs/quality-gates.md#skill-level-quality-gate-composition`
  for the full gate-skill federation graph (this skill
  is the synthesis hub)

## Required TodoWrite Items

When invoked as a pre-flight gate, create:

- `karpathy:assumptions-listed` - principle 1 satisfied
- `karpathy:simplicity-checked` - principle 2 satisfied
- `karpathy:trace-back-verified` - principle 3 satisfied
- `karpathy:success-criteria-defined` - principle 4
  satisfied

## Exit Criteria

- Each of the four principles has been answered with a
  concrete artifact (assumption list, scope rationale,
  diff trace, verification plan).
- The senior-engineer test was applied at least once.
- Verifiable success criteria are written down before
  the implementation begins.
