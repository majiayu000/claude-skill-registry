---
name: elegant-code
description: Language-agnostic rulebook for producing, reviewing, and improving elegant code. Use when writing new code, refactoring existing code, reviewing code quality, or when user asks for "elegant", "clean", "maintainable", or "well-structured" code. Applies to any programming language or framework.
---

# Elegant Code

Elegant code = **Correctness + Clarity + Minimal complexity + Natural efficiency + Easy change.**

Not "shortest" or "cleverest." The solution that makes readers think: *"Of course. That's simple, right, and hard to mess up."*

## Optimization Priority (in order)

1. **Correctness & safety** — does what it claims, handles edge cases
2. **Clarity of intent** — reader answers "what/why/how" from code itself
3. **Simplicity** — minimal concepts that still solve the problem
4. **Changeability** — modifications are localized and low-risk
5. **Efficiency** — good algorithms; performance from good design, not micro-optimizations

## Elegant vs "Smart" Code

| Elegant | Smart/Clever |
|---------|--------------|
| Clarity & solution | Cleverness & brevity |
| Humans first | Machine first (humans decode) |
| Low complexity | High complexity |
| Easy to debug/change | Fragile and opaque |
| "Of course!" | "Wait… how?" |

## The Workflow

Use this sequence when writing or refactoring:

### 1. Clarify the problem
- Define inputs, outputs, invariants, constraints, failure modes
- Identify postconditions (what must be true after)
- List edge cases and "gotchas"

### 2. Choose simplest correct approach
- Pick simplest algorithm/data structure meeting constraints
- Prefer fewer concepts over more layers
- If adding abstraction, state what complexity it removes

### 3. Design shape before details
- Outline modules/functions and responsibilities
- Decide boundaries: pure logic vs side effects (I/O, database, network)

### 4. Write readable-by-default code
- Clear names, small units, straightforward control flow
- Make "happy path" obvious; handle errors intentionally

### 5. Add guardrails
- Validation, assertions (where appropriate), tests
- Define invalid input handling

### 6. Refine (remove, simplify, clarify)
- Remove duplication, tighten interfaces, reduce nesting
- Each unit should read like a single thought

### 7. Verify against reality
- Run tests; benchmark if performance matters
- Confirm behavior matches original problem statement

## Core Rules

### Rule 1 — Preserve intent above everything

Reader must answer: What does this do? Why? What constraints? What can go wrong?

- Comments explain **why**, tradeoffs, constraints—not what code does
- If you need comments to explain *what*, the code is unclear

### Rule 2 — Minimize concepts, not lines

Keep distinct "ideas" (types, abstractions, layers, config knobs) minimal.

- Prefer one good function over a mini-framework
- No "future-proofing" without concrete known need
- If abstraction adds indirection without removing complexity, remove it

### Rule 3 — Common case simple; edge cases explicit

- Happy path easy to follow
- Edge cases via early returns, guard clauses, explicit validation
- Avoid deep nesting hiding the main story

### Rule 4 — Small, cohesive units

- One primary responsibility per function/module/class
- Group related logic; separate unrelated concerns
- If name needs "and" (parseAndSave), it's doing too much

### Rule 5 — Explicit data flow over hidden state

- Data through parameters and return values, not globals/singletons/mutable shared state
- If you can't test without elaborate setup, hidden context exists
- If call order matters, make it explicit

### Rule 6 — DRY knowledge, not syntax

- Unify if two places must change together
- Allow small obvious repetition if abstraction is harder to read
- Duplicate code sometimes cheaper than leaky abstraction

### Rule 7 — Right algorithmic shape

- Choose algorithms/data structures appropriate to constraints
- Prefer clarity unless profiling demands complexity
- Prefer asymptotic wins over micro-optimizations

### Rule 8 — Make invalid states unrepresentable

- Represent domain constraints in types/structures so illegal combinations are impossible
- Validate at boundaries, convert to trusted internal representations

### Rule 9 — Local reasoning

- Understand a unit without chasing definitions across codebase
- Small interfaces, directness over indirection
- Configuration close to usage or centralized with clear naming

### Rule 10 — Idiomatic but readable

- Follow language/project conventions
- Don't use obscure tricks only experts recognize
- If idiom is compact but unclear, choose clearer form

## Micro-Rules

### Naming
- **DO**: Names encode intent and domain meaning, not mechanics
- **DO**: Concrete nouns/verbs: `calculate_total`, `is_valid`, `parse_header`
- **AVOID**: Vague names: `data`, `process`, `handle`, `doThing`, `tmp`, `manager`
- **DO**: One concept → one term (consistent vocabulary)

### Functions
- Short enough for working memory
- Inputs/outputs obvious and stable
- Side effects clear from name or context
- Favor pure functions for core logic
- I/O at edges ("functional core, imperative shell")

### Control Flow
- Avoid deep nesting; use guard clauses
- Early exits for invalid conditions
- Straightforward over clever

### Error Handling
- Decide: recover, retry, fallback, or fail fast—then implement consistently
- Errors carry enough context to debug
- Validate at boundaries
- Never swallow errors silently

### Dependencies
- Depend on stable interfaces, not unstable internals
- Minimal and purposeful dependencies
- Inject dependencies where it improves testability

## Self-Review Checklist

Before finalizing code, verify:

- [ ] **Correctness**: Meets requirements; edge cases handled; failures intentional
- [ ] **Clarity**: Names meaningful; reads top-to-bottom; minimal mental jumps
- [ ] **Simplicity**: No unnecessary abstractions; minimal moving parts
- [ ] **Cohesion**: Each unit has one job; responsibilities not mixed
- [ ] **Coupling**: Dependencies minimal; interfaces small and stable
- [ ] **Data flow**: Inputs/outputs explicit; minimal hidden state
- [ ] **Error handling**: Consistent strategy; errors include context
- [ ] **Efficiency**: Algorithm/data structures fit constraints; no obvious waste
- [ ] **Consistency**: Patterns match codebase norms
- [ ] **Testability**: Core logic testable easily; tests exist for tricky parts

## Refactor Decision Rules

**Refactor if:**
- Function/module cannot be summarized in one sentence
- Must read twice to trust it
- One change requires edits in many unrelated places
- Bugs cluster in same area repeatedly
- Keep adding special cases ("just one more flag")

**Avoid refactoring if:**
- No tests and behavior unclear (add tests first)
- Code stable and rarely changed, improvements purely aesthetic
- Near deadline and risk is high (smallest safe improvements only)

## Detailed References

- **Measuring elegance**: See [references/scorecard.md](references/scorecard.md) for the elegance scorecard, objective metrics, and improvement checklist
- **Anti-patterns**: See [references/anti-patterns.md](references/anti-patterns.md) for what kills elegance and "smart code" smells
- **Continuous improvement**: See [references/continuous-improvement.md](references/continuous-improvement.md) for the Continuous Elegance Loop and practices
