---
name: goblins
description: Distributed object capability system (6.5K lines info).
version: 1.0.0
---


# goblins

Distributed object capability system (6.5K lines info).

## bmorphism Contributions

> *"Autopoiesis refers to the self-maintenance of a system, where the system is capable of reproducing and maintaining itself."*
> — [vibes.lol gist](https://gist.github.com/bmorphism/c41eaa531be774101c9d9b082bb369eb)

**Goblins as Autopoietic Agents**: Each Goblins actor is an autopoietic system — it maintains its own state via `bcom` (become), reproducing itself with updated behavior. This embodies the self-maintenance principle at the core of cognitive architecture.

**Active Inference via CapTP**: The OCapN protocol implements distributed [Active Inference in String Diagrams](https://arxiv.org/abs/2308.00861) where:
- **Sturdyref** → Reference to external world (perception)
- **`<-` async call** → Action that generates expected sensory response
- **Promise resolution** → Prediction error minimization

**GF(3) in Actor Triads**: Actor systems naturally form triads: sender (+1, generator) → message (0, coordinator) → receiver (-1, validator). The async semantics preserve GF(3) conservation across distributed computation.

## Model

```
peer → vat → actormap → {refr: behavior}
```

## Operators

```scheme
($  obj method args...)   ; Sync (near only)
(<- obj method args...)   ; Async (near/far)
```

## Vat

```scheme
(define vat (spawn-vat))
(define greeter
  (vat-spawn vat
    (lambda (bcom)
      (lambda (name)
        (format #f "Hello, ~a!" name)))))

($ greeter "World")  ; => "Hello, World!"
```

## OCapN

Object Capability Network for secure p2p via CapTP.



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
goblins (−) + SDF.Ch10 (+) + [balancer] (○) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch1: Flexibility through Abstraction

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
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