---
name: principles
description: Guiding principles and decision-making patterns for the ikigai project
---

# Principles

Foundational beliefs that guide recommendations. When proposing solutions, align with these principles.

## Philosophy

**Correctness is non-negotiable.** 90% test coverage, every branch, no exceptions. Quality gates exist because willpower fails - systems enforce standards.

**Explicit over implicit.** Ownership is visible. Errors are typed. Naming is precise. Decisions are documented. If it's not obvious, make it obvious.

**Simplicity through discipline, not cleverness.** Single-threaded. Hierarchical memory. Crash on impossible states. Complexity is a cost - pay it only when forced.

## Decision Patterns

**When uncertain, fail loudly.** PANIC over silent corruption. Assert liberally. Unknown states are unacceptable.

**Choose battle-tested foundations.** C, PostgreSQL, talloc, direct terminal rendering. Solid platforms over trendy tooling.

**Split rather than sprawl.** 16KB file limits. One module, one responsibility. Refactor before it hurts.

**Validate at boundaries, trust internal code.** External input is suspect. Internal invariants are asserted. No defensive coding inside trust boundaries.

**Spend generously preparing, save ruthlessly executing.** Research phase is thorough. Task files are complete. Execution loops are mechanical and cheap.

## Anti-Patterns

Reject: feature flags for hypothetical futures, backwards-compat hacks, "hard to test" excuses, implicit ownership, documentation as afterthought, clever code, over-engineering.

## Tradeoff Tendencies

- Favor crash over recovery in ambiguous states
- Favor explicit boilerplate over magic abstractions
- Favor mechanical verification over manual review
- Favor complete upfront work over iteration during execution
- Favor deleting code over maintaining compatibility shims
