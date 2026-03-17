---
name: solid-architecture
description: This skill should be used PROACTIVELY when writing, reviewing, or refactoring code. It provides SOLID principles, composition patterns, module organization, and side-effect boundary guidelines. Use when implementing features, fixing bugs, creating new modules, or reviewing code quality.
---

# SOLID Architecture Guidelines

Apply these principles when writing or modifying code. Use them as tie-breakers when design decisions conflict.

## Core Goals (Priority Order)

1. **Maintainability** - Easy to change without breaking unrelated parts
2. **Testability** - Core logic testable without I/O or UI
3. **Determinism** - Reproducible given same inputs/seeded RNG
4. **Separation of Concerns** - Domain, infrastructure, UI clearly separated

## Composition Over Inheritance

Favor small, focused types composed together rather than deep inheritance trees. When tempted to extend a class, first ask: "Can this be achieved through composition instead?"

## SOLID Principles

### Single Responsibility (SRP)

Each module/type/function has **one reason to change**.

**Violation signals:**
- Cannot describe purpose in one sentence
- Domain logic mixed with infrastructure
- Multiple unrelated reasons to modify the file

**Action:** Split into focused modules with clear, singular purposes.

### Open/Closed (OCP)

Extend via new implementations, not constant modification.

**Violation signals:**
- Adding behavior requires modifying existing code
- Growing switch/if-else chains for new cases
- Frequent changes to stable modules

**Action:** Add behavior through new modules and composition, not conditionals.

### Liskov Substitution (LSP)

Subtypes must work anywhere their base type is expected.

**Violation signals:**
- Subtypes that throw on inherited operations
- Subtypes that ignore/no-op inherited methods
- Deep inheritance hierarchies

**Action:** Prefer interfaces over deep hierarchies. Ensure substitutability.

### Interface Segregation (ISP)

Depend only on the minimal surface needed.

**Violation signals:**
- Large interfaces with many methods
- Consumers only using subset of interface
- "Fat" interfaces forcing empty implementations

**Action:** Create small, specific interfaces. Split large ones.

### Dependency Inversion (DIP)

Depend on abstractions, not concretions.

**Violation signals:**
- Direct imports of concrete implementations
- Global singletons for RNG, config, I/O
- Hard-coded dependencies

**Action:** Inject dependencies. Use explicit context/environment objects passed to systems.

## Module Organization

### File Granularity

- **Non-trivial types** (classes, structs, complex components): Dedicate a file
- **Related utilities/functions**: Group by cohesive purpose in single module
- **Avoid**: Grab-bag "utils" files - group by purpose instead

### Layering

Establish clear dependency directions:

```
core → domain → application → UI
```

**Rules:**
- Lower layers MUST NOT import from higher layers
- Mark any temporary violations and track cleanup
- Use barrel/index files only for public APIs
- Internal modules import directly; external consumers use public API
- Avoid circular dependencies

## Side Effects & Boundaries

### Pure vs Impure Separation

Separate pure computation from side effects.

**Pure (no side effects):**
- Calculations, transformations, business logic
- Receives all inputs as parameters
- Returns results without modifying external state

**Impure (side effects):**
- I/O operations (file, network, database)
- Random number generation
- Time/date operations
- Logging, metrics

### Dependency Injection

Systems receive these via injection for deterministic testing:
- Clocks
- RNG (seeded for reproducibility)
- I/O adapters

### Boundary Modules

Push I/O and external integrations to small, well-named boundary modules at system edges.

**When refactoring:** Bias toward making core logic purer and pushing side effects outward.

## Quick Reference Checklist

Before committing code changes:

- [ ] Can each module's purpose be described in one sentence?
- [ ] Is domain logic free from infrastructure concerns?
- [ ] Are dependencies injected, not hard-coded?
- [ ] Do lower layers avoid importing from higher layers?
- [ ] Are side effects pushed to system boundaries?
- [ ] Is the code testable without mocking I/O?
