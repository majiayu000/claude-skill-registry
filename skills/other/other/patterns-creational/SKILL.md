---
name: patterns-creational
description: "Implement creational design patterns (Factory Method, Abstract Factory, Builder, Prototype, Singleton). Use when object construction is complex, varies by type/environment, needs decoupling from callers, or you're introducing dependency injection for testability. NOT for wrapping/composing objects (use patterns-structural); NOT for algorithms/eventing/state machines (use patterns-behavioral); NOT for choosing which pattern family (use design)."
metadata: {"stage":"Mechanics","tags":["creational-patterns","factory","builder","object-creation","dependency-injection","abstract-factory","prototype","singleton"],"aliases":["factory","builder","singleton","prototype","abstract-factory","object-creation","DI","dependency-injection"]}
---

# Patterns (Creational)

## Overview

Create objects without hard-coding concrete classes into callers. Use these patterns to isolate construction, support multiple variants, and keep object creation testable.

A note on scope: these guidelines assume **systemic** TypeScript (long‑lived apps/services). For short‑lived scripts, you can simplify (inline construction, fewer layers) as long as tests and change-cost stay acceptable.

## Workflow

1. Decide “scriptic vs systemic” and set policies (boundary decoding, error semantics, ownership/lifetimes).
2. Identify the creation pressure: variant explosion, complex setup, environment wiring, or lifecycle constraints.
3. Decide what must be stable for callers (interface and invariants), and what may vary (implementation, configuration, dependencies).
4. Pick the smallest creational pattern that matches the pressure (see chooser).
5. Implement with DI-friendly constructors or factory functions; keep creation as pure as possible.
6. Add tests that assert:
   - correct type selection for each variant
   - invariants validated during creation
   - callers depend only on interfaces/abstractions

## Chooser

- **Factory Method**: subclasses/modules decide which product to create for a common interface.
- **Abstract Factory**: select a “family” (e.g., platform/vendor) and create compatible products together.
- **Builder**: stepwise construction with validation; many optional parts or multiple representations.
- **Prototype**: clone existing instances to avoid complex constructors; preserve runtime types.
- **Singleton** (caution): one instance truly required; prefer passing dependencies explicitly or container-managed singletons.

## Implementation Checklist

- Make factories return interfaces/abstract types; hide concrete constructors in one place.
- Keep variant selection logic near configuration boundaries (composition root).
- Avoid “stringly-typed factories”; use typed keys (`as const` maps / unions) where possible.
- Validate invariants at creation time; fail fast with actionable errors.
- Avoid import-time wiring in systemic code; create/wire dependencies in a composition root so lifetimes are explicit.
- If created objects own resources, make lifetimes explicit (`start/stop/dispose`) and define ownership (who shuts it down).
- Keep object graphs shallow in tests by injecting fakes/mocks (avoid global state).

## Snippets (optional)

- TypeScript: [`references/snippets/typescript.md`](references/snippets/typescript.md)
- React: [`references/snippets/react.md`](references/snippets/react.md)

## References

Read the relevant reference file before implementing or refactoring toward the pattern:

- [`references/factory-method.md`](references/factory-method.md)
- [`references/abstract-factory.md`](references/abstract-factory.md)
- [`references/builder.md`](references/builder.md)
- [`references/prototype.md`](references/prototype.md)
- [`references/singleton.md`](references/singleton.md)

Each reference includes: selection cues, minimal structure, pitfalls, and test ideas.

## Output Template

When applying a creational pattern, return:

- The creation pressure (variants/complex setup/lifecycle constraints) and what must stay stable for callers.
- The chosen pattern and the proposed seam (factory/builder/prototype) + wiring point (composition root).
- Verification steps (tests for variant selection, invariant validation, and lifetime ownership).
