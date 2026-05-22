---
name: patterns-structural
description: "Implement structural design patterns (Adapter, Decorator, Facade, Proxy, Composite, Bridge, Flyweight). Use when wrapping/composing objects, translating between interfaces, simplifying a complex subsystem, adding caching/auth/lazy-loading via indirection, or building recursive tree structures. NOT for object creation (use patterns-creational); NOT for algorithms/eventing/state machines (use patterns-behavioral)."
metadata: {"stage":"Mechanics","tags":["structural-patterns","adapter","facade","decorator","proxy","composite","bridge","flyweight","wrapper"],"aliases":["adapter","decorator","facade","proxy","wrapper","composite","bridge","flyweight"]}
---

# Patterns (Structural)

## Overview

Shape object relationships to reduce coupling without rewriting everything. Use structural patterns to compose behavior, hide complexity, and add indirection at boundaries.

A note on scope: these guidelines assume **systemic** TypeScript (long‑lived apps/services). In scripts, you may not need full wrapper stacks; prefer the simplest boundary that keeps callers clean.

## Workflow

1. Decide “scriptic vs systemic” and set policies (boundary decoding, error semantics, ownership/lifetimes).
2. Identify the boundary: what do callers want to depend on, and what do you want to hide?
3. Decide if you’re changing:
   - **interface** (Adapter)
   - **abstraction vs implementation axes** (Bridge)
   - **object graph shape** (Composite)
   - **optional behavior stacking** (Decorator)
   - **subsystem surface area** (Facade)
   - **memory footprint** (Flyweight)
   - **access policy/indirection** (Proxy)
4. Keep the public surface small: one interface + a few implementations/wrappers.
5. Add tests around the boundary (callers see stable behavior even as internals change).

## Chooser

- **Adapter**: make incompatible APIs work together (often at third-party/legacy boundaries).
- **Bridge**: two axes vary independently (e.g., “shape” x “renderer”, “transport” x “codec”).
- **Composite**: treat leaf and container uniformly; tree recursion + operations over nodes.
- **Decorator**: add optional responsibilities without subclass explosion; wrappers are stackable.
- **Facade**: shrink a subsystem to a simple, stable API; hide orchestration.
- **Flyweight**: many similar objects; split intrinsic state (shared) vs extrinsic (supplied).
- **Proxy**: control access (lazy init, cache, auth, throttling, remote boundary, logging).

## Implementation Checklist

- Prefer composition; wrappers should delegate almost everything and add one focused concern.
- Make wrappers transparent where appropriate (don’t leak internals via type checks).
- Put facades and adapters at module boundaries; keep core domain clean.
- Translate boundary concerns explicitly: `unknown` inputs → decoded domain types; SDK errors → your error model.
- For proxies: define caching/invalidation, concurrency semantics, and cancellation/timeouts (`AbortSignal`) where applicable.
- If the real subject has a lifetime (`close`/`dispose`), expose and forward it; keep ownership/shutdown explicit.
- For flyweights: prove the memory win and define ownership/lifetime of shared state.

## Snippets (optional)

- TypeScript: [`references/snippets/typescript.md`](references/snippets/typescript.md)
- React: [`references/snippets/react.md`](references/snippets/react.md)

## References

Read the relevant reference file before implementing or refactoring toward the pattern:

- [`references/adapter.md`](references/adapter.md)
- [`references/bridge.md`](references/bridge.md)
- [`references/composite.md`](references/composite.md)
- [`references/decorator.md`](references/decorator.md)
- [`references/facade.md`](references/facade.md)
- [`references/flyweight.md`](references/flyweight.md)
- [`references/proxy.md`](references/proxy.md)

Each reference includes: selection cues, minimal structure, pitfalls, and test ideas.

## Output Template

When applying a structural pattern, return:

- The boundary you’re shaping (callers vs hidden subsystem) and what stays stable.
- The chosen pattern (Adapter/Facade/Proxy/etc.) and the minimal surface area (interface + implementations/wrappers).
- Verification steps (tests at the boundary seam; lifetime/timeout/cancellation behavior where applicable).
