---
name: scheme
description: GNU Scheme ecosystem = guile + goblins + hoot + fibers.
version: 1.0.0
---


# scheme

GNU Scheme ecosystem = guile + goblins + hoot + fibers.

## bmorphism Contributions

> *"We are building cognitive infrastructure for the next trillion minds"*
> — [Plurigrid: the story thus far](https://gist.github.com/bmorphism/a400e174b9f93db299558a6986be0310)

**Spritely Goblins as Active Inference**: The Goblins actor model implements distributed [Active Inference in String Diagrams](https://arxiv.org/abs/2308.00861) where each vat is an agent with its own Markov blanket. The async message passing (`<-`) is perception; the behavior update (`bcom`) is action.

**Object Capabilities as Cybernetic Boundary**: The capability pattern aligns with bmorphism's cybernetic immune system concept — capabilities define what an agent CAN perceive/act upon, implementing the statistical boundary between self and world.

**Hoot WebAssembly**: Compiling Scheme to Wasm enables portable cognitive agents — the same skill can run in browser, server, or embedded contexts while maintaining behavioral identity.

## Atomic Skills

| Skill | Lines | Domain |
|-------|-------|--------|
| guile | 67K | Interpreter |
| goblins | 6.5K | Distributed objects |
| hoot | 4K | WebAssembly |
| fibers | 2K | Concurrent ML |
| r5rs | 1K | Standard |

## Compose

```scheme
;; guile + goblins + hoot
(use-modules (goblins)
             (goblins actor-lib methods)
             (hoot compile))

(define-actor (counter bcom count)
  (methods
    ((get) count)
    ((inc) (bcom (counter bcom (+ count 1))))))
```

## Wasm Pipeline

```bash
guile -c '(compile-to-wasm "app.scm")'
```

## FloxHub

```bash
flox pull bmorphism/effective-topos
flox activate -d ~/.topos
```



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Cheminformatics
- **rdkit** [○] via bicomodule
  - Hub for chemistry

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.