---
name: design-an-interface
description: Generate radically-different module or API contract designs in parallel, then compare on depth, simplicity, and ease-of-correct-use. Trigger when the user is shaping a new module surface, exploring contract options, comparing module shapes, or applying "design it twice" to a first-pass sketch.
---

Apply "Design It Twice" (Ousterhout, *A Philosophy of Software Design*): the first interface is rarely the best. Generate at least three radically different shapes for the same module, then compare on depth and ease of correct use. Implementation is out of scope — this skill stops at the contract.

Run discovery before generation. When the module already has callers, dispatch an Explore agent to enumerate them (`fd` for files, `git grep`/`ast-grep` for usage sites) so the constraint set reflects real consumers, not imagined ones.

**Modality vs adjacent skills:** This is **divergent generation under enforced contrast**. *Implementation planning* is convergent and execution-oriented. *Clarifying-question protocol* is VS-shaped clarification on a single direction. Pick this skill when the answer is "we don't yet know the right shape" and the value is in deliberate contrast across N candidates.

## Workflow

### 1. Frame the contract

Capture, in this order, before any design work:

- The problem the module solves, in one sentence.
- The callers — peer modules, external consumers, tests — and which one is primary.
- The key operations, ranked by frequency.
- Constraints: performance budget, compatibility surface, existing patterns the module must echo.
- The information boundary: what the module hides versus what it must expose.

If any item is unknown, surface it as a question before proceeding. Designing on assumed callers wastes the parallel-generation budget.

### 2. Generate divergent designs in parallel

Dispatch 3–4 Explore agents simultaneously, each with a distinct constraint that *forces* divergence. Suggested constraint slate:

- Agent A: minimise the surface — 1–3 entry points maximum.
- Agent B: maximise generality — accept many shapes of input.
- Agent C: optimise for the dominant call site at the cost of the rare one.
- Agent D: borrow shape from a named external paradigm (iterator, builder, capability handle, effect handler).

Each agent returns: contract signature, one realistic call-site example, what the design hides internally, and the trade-offs it accepts.

Reject sub-agent outputs that converge — re-dispatch with sharpened constraints if two designs read alike.

### 3. Present designs sequentially

Show each candidate in turn so the user absorbs one shape before the next. For every candidate include the contract signature, a usage example, and the hidden complexity it absorbs. Avoid side-by-side tables at this stage — sequence preserves cognitive contrast.

Parallel examples across language families clarify how a contract translates:

```rust
// Candidate A — minimal surface, Rust trait
pub trait Cache {
    fn get_or_insert<F: FnOnce() -> Vec<u8>>(&self, key: &str, init: F) -> Vec<u8>;
}
```

```typescript
// Candidate A — minimal surface, TypeScript interface
export interface Cache {
  getOrInsert(key: string, init: () => Uint8Array): Uint8Array;
}
```

The same idea, two ecosystems — depth comes from *what the implementation hides*, not from method count alone.

### 4. Compare in prose

Compare the candidates on:

- **Surface simplicity** — entry-point count, parameter shape, type-parameter load.
- **Generality versus focus** — future use cases absorbed without change versus over-generalisation cost.
- **Implementation efficiency** — does the shape permit efficient internals or force awkward bookkeeping?
- **Depth** — small surface hiding significant complexity (deep, preferred) versus broad surface with thin internals (shallow, reject).
- **Correct-use bias** — how easy is it to use the contract correctly versus how easy to misuse.

Discuss in prose, not tables. Highlight the axes where the candidates diverge most sharply — that is where the design decision actually lives.

### 5. Synthesise

The winning design is rarely a single candidate verbatim. Ask which candidate fits the dominant call site, then which elements from the others should grafted in. Surface the synthesis as a fifth named design with explicit lineage ("borrows handle shape from B, error model from C").

## Anti-patterns

- Convergent sub-agent output — defeats the value of parallel generation. Re-dispatch with louder constraint contrast.
- Skipping comparison — the entire point is contrast; presenting candidates without ranking abandons the work.
- Drifting into implementation — this skill ends at the contract.
- Ranking by implementation effort — short-term cost is the wrong axis; depth and ease of correct use are the right ones.
