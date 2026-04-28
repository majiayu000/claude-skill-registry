---
name: improve-codebase-architecture
description: Surface deepening opportunities — refactors that turn shallow modules into deep ones — informed by `CONTEXT.md` and `docs/adr/`. Trigger when user asks to improve architecture, find refactor candidates, consolidate tightly coupled modules, raise testability, or make a codebase more agent-navigable. Skip when scope is a single localized fix; this is a survey-then-grill skill, not a bug hunt.
---

Iteration loop: explore for friction, present deepening candidates, grill the chosen one, update domain artifacts inline. Vocabulary is load-bearing — see `references/LANGUAGE.md`.

## Vocabulary [LOAD-BEARING]

Use these terms exactly. Do not substitute "component," "service," "API," or "boundary." Full definitions in `references/LANGUAGE.md`.

- **Module** — anything with an interface and an implementation (function, class, package, slice). Scale-agnostic.
- **Interface** — every fact a caller must know: types, invariants, ordering, error modes, config, performance shape. Not just signature.
- **Depth** — leverage at the interface. Deep = much behaviour behind a small interface. Shallow = interface as complex as implementation.
- **Seam** (Feathers) — where an interface lives; a place behaviour can be altered without editing in place. Use this, not "boundary."
- **Adapter** — a concrete thing satisfying an interface at a seam. Role, not substance.
- **Leverage** — capability callers gain per unit of interface learned.
- **Locality** — concentration of change, bug, and knowledge at one site for maintainers.

## Principles

- **Deletion test:** imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **Interface = test surface.** Tests cross the same seam callers cross. Wanting to test past the interface = wrong shape.
- **One adapter = hypothetical seam. Two adapters = real seam.** No port without two real implementations (production + test).

## Process

### 1. Explore [Dispatch-First]

First tool call MUST be Explore-agent dispatch — not direct reads. The agent's brief:

- Read `CONTEXT.md` (or `CONTEXT-MAP.md` + per-context `CONTEXT.md`) and any `docs/adr/`. If absent, proceed silently.
- Walk the codebase organically; classify friction:
  - Concept understanding requires bouncing across many small modules → shallow cluster.
  - Interface complexity matches implementation complexity → shallow module.
  - Pure functions extracted only for testability while real bugs hide in callers → no locality.
  - Tightly coupled modules leaking across their seams.
- For each suspect, run the deletion test before reporting.

### 2. Present candidates

Numbered list. Each candidate: **Files**, **Problem** (concrete friction; cite deletion test), **Solution** (plain-English description; no interface yet), **Benefits** (locality, leverage, testability deltas).

ADR conflicts: surface only when friction warrants reopening; mark explicitly: _"contradicts ADR-0007 — worth reopening because…"_.

Ask: "Which candidate to explore?" Do not propose interfaces yet.

### 3. Grilling loop

Once user picks, drop into adversarial interview — walk the design tree, resolve dependencies one decision at a time, recommend an answer per question. Side effects happen inline:

- New domain term emerging? Update `CONTEXT.md` immediately (lazy create).
- User rejects with a load-bearing reason that future explorers would need? Offer ADR.
- User wants alternative interfaces for the chosen candidate? Pivot to `references/INTERFACE-DESIGN.md` — parallel sub-agent design twice (Ousterhout).

## Deepening categories (testing strategy per dependency class)

Full treatment in `references/DEEPENING.md`. Summary:

| Class | Deepenable? | Test strategy |
|---|---|---|
| In-process (pure / in-memory) | Always | Merge modules; test through new interface directly. No adapter. |
| Local-substitutable (PGLite, in-memory FS) | Yes if stand-in exists | Stand-in runs in tests; seam stays internal. |
| Remote but owned (microservices) | Yes via Ports & Adapters | Port at seam; HTTP/gRPC adapter prod, in-memory adapter test. |
| True external (Stripe, Twilio) | Yes | Injected port; mock adapter for tests. |

Replace, don't layer: delete shallow-module tests once interface tests exist.

## Language-neutral examples

**Rust** — shallow `validate_address` + `format_address` + `geocode_address` separately called by a `Shipment` aggregator. Deletion test: removing `format_address` concentrates string-handling at one call site → was a pass-through. Deepen into `address::Resolver` with `resolve(raw) -> Result<Resolved, AddressError>`; tests cross the new interface; in-memory `Geocoder` adapter for tests, HTTP adapter for production.

**Python** — module exposes `parse_invoice`, `apply_tax`, `round_total` as separate top-level functions; every caller chains all three. Deepen into `billing.Invoice.finalize(raw) -> Invoice`. Internal seams (tax tables, rounding rules) stay private; the test surface is `Invoice.finalize`.

## Reference docs

- `references/LANGUAGE.md` — full vocabulary, principles, rejected framings.
- `references/DEEPENING.md` — dependency taxonomy, seam discipline, replace-don't-layer testing.
- `references/INTERFACE-DESIGN.md` — parallel sub-agent "Design It Twice" workflow when the chosen candidate's interface needs alternatives.

Forbidden: proposing interfaces in step 2 (premature commitment), bundling unrelated refactors, re-litigating ADRs without a load-bearing reason.
