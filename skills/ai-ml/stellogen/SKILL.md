---
name: stellogen
description: Stellogen Skill
version: 1.0.0
---

# Stellogen Skill

**Trit**: 0 (ERGODIC - logic-agnostic mediation)  
**Source**: [engboris/stellogen](https://github.com/engboris/stellogen) + [bmorphism/stellogen](https://github.com/bmorphism/stellogen)  
**License**: MIT

---

## Overview

**Stellogen** is a logic-agnostic programming language based on term unification, designed from Girard's transcendental syntax. It provides:

1. **Constellations** - Logic programs as elementary computation bricks
2. **Galaxies** - Structured collections of constellations
3. **Interaction Nets** - Lafont-style parallel graph rewriting
4. **Proof-as-Program** - Coq-like tactics without fixed type system

## Key Characteristics

- **Logic-agnostic typing**: No primitive types; uses assert-like expressions
- **Term unification**: Everything reduces to unification
- **Multi-paradigm**: Logic, functional, imperative, object-oriented

## Syntax

### Polarized Rays

```stellogen
' Positive ray (output/producer)
+output(term)

' Negative ray (input/consumer)  
-input(term)

' Constellation (logic program)
spec nat =
  -i(z) ok;
  -i(s(X)) +i(X).
```

### Galaxies (Structured Constellations)

```stellogen
fsm = galaxy
  initial = -i(W) +state(W q0).
  final = -state(e qf) accept.
  transitions =
    -state(0:W q0) +state(W q1);
    -state(1:W q1) +state(W q0).
end
```

### Process Execution

```stellogen
show process #input. #galaxy. &kill. end
```

## GF(3) Integration

Stellogen rays map naturally to GF(3) trits:

| Ray | Trit | Semantic |
|-----|------|----------|
| `+ray(X)` | +1 | Production/Generation |
| `-ray(X)` | -1 | Consumption/Verification |
| `ok` / neutral | 0 | Balance/Success |

### Conservation in Constellations

```stellogen
' GF(3) conserved: (-1) + (+1) = 0
spec balanced =
  -input(X) +output(f(X)).

' Verification via interaction
show process #data. #balanced. &kill. end
```

## Quantum Operads Extension

From [bmorphism/stellogen-quantum-operads](https://github.com/bmorphism/stellogen-quantum-operads):

```stellogen
' Operad structure
(:= (operad-structure P) {
  [(+arity P N) (== N (num-inputs P))]
  [(+composition P Q R) (== R (compose-ops P Q))]
  [(+associativity P Q R) 
    (== (compose-ops P (compose-ops Q R)) 
        (compose-ops (compose-ops P Q) R))]
})

' ZX-calculus spiders
(:= (qubit-op Type Phase) {
  [(+z-spider Phase) (== Type z-op)]
  [(+x-spider Phase) (== Type x-op)]
  [(+hadamard) (== Type h-op)]
})

' Bell state preparation
(:= bell-state-prep {
  [(+bell-prep) (== Circuit
    (compose-ops
      (h-op 0)
      (cnot 0 1)))]
})
```

## Interaction Nets Foundation

Stellogen implements Lafont's interaction nets:

```
    ┌───────┐
    │ Agent │ ← Principal port
    └───┬───┘
   ╱    │    ╲
  p₁   p₂   p₃  ← Auxiliary ports
```

**Interaction rules**: When two principal ports connect, rewrite fires.

```stellogen
' Addition via interaction
spec add =
  -add(z Y) +result(Y);
  -add(s(X) Y) +add(X s(Y)).
```

## Installation

### Via Nix

```bash
cd /path/to/stellogen
nix develop
dune build
```

### Via OPAM

```bash
opam pin tsyntax https://github.com/engboris/stellogen.git
```

## Commands

```bash
# Run stellogen file
dune exec sgen -- examples/nat.sg

# Interactive mode
dune exec sgen -- --interactive

# Just commands (if available)
just stellogen-run file.sg
just stellogen-test
```

## Examples

### Lambda Calculus

```stellogen
' Church encoding
spec church =
  -lam(V B A) +app(lam(V B) A);
  -app(lam(V B) A) +subst(V A B).

zero = +lam(f +lam(x +var(x))).
succ = +lam(n +lam(f +lam(x +app(var(f) +app(app(var(n) var(f)) var(x)))))).
```

### Linear Lambda Calculus

```stellogen
' Linear logic: each variable used exactly once
spec linear_lambda =
  -lam!(V B) +lin_abs(V B);
  -app!(F A) +lin_app(F A);
  -var!(X) +lin_var(X).
```

### Turing Machine

```stellogen
tm = galaxy
  tape = -read(S Pos) +write(S' Pos' State').
  halt = -state(halt) done.
end
```

## Integration with Gay.jl

From [GAY.md](https://github.com/bmorphism/stellogen/blob/main/GAY.md):

```julia
using Gay

# Stellogen repo color
gay_seed!(0x7d202e3bf2aafbb0)
color = color_at(427)  # => #c22851

# Verify SPI across stellogen examples
chain = [next_color() for _ in 1:69]
fp = reduce(⊻, [color_to_u64(c) for c in chain])
```

## GF(3) Triads

```
interaction-nets (-1) ⊗ stellogen (0) ⊗ operad-compose (+1) = 0 ✓
bisimulation-game (-1) ⊗ stellogen (0) ⊗ gay-mcp (+1) = 0 ✓
proofgeneral-narya (-1) ⊗ stellogen (0) ⊗ discopy (+1) = 0 ✓
```

## Influences

| Source | Contribution |
|--------|--------------|
| Prolog/Datalog | Unification-based computation |
| Smalltalk | Message-passing, minimalism |
| Coq | Proof-as-program, tactics |
| Scheme/Racket | Metaprogramming |
| Girard | Transcendental syntax, linear logic |

## References

- [Girard's Transcendental Syntax](https://girard.perso.math.cnrs.fr/trsy1.pdf)
- [Lafont's Interaction Nets (1990)](https://www.sciencedirect.com/science/article/pii/089054019090191H)
- [French Guide](https://tsguide.refl.fr/)
- [English Guide](https://tsguide.refl.fr/en/)

## See Also

- `interaction-nets` - Lafont's parallel λ-reduction
- `operad-compose` - Colored operad composition
- `discopy` - DisCoPy string diagrams
- `gay-mcp` - Deterministic color generation
- `proofgeneral-narya` - Proof assistant integration

---

**Skill Name**: stellogen  
**Type**: Logic-Agnostic Programming / Interaction Nets  
**Trit**: 0 (ERGODIC - mediates between proof and computation)  
**Repo Color**: #c22851  
**Status**: ✅ Available



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

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
