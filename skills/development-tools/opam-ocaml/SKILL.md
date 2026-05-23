---
name: opam-ocaml
description: OPAM package manager for OCaml. Switch management, dependency resolution, and OCaml toolchain.
version: 1.0.0
---


# OPAM OCaml Skill

**Trit**: -1 (MINUS - package constraint verification)  
**Foundation**: OPAM + OCaml + dune  

## Core Concept

OPAM manages OCaml development:
- Compiler switches (versions)
- Package dependencies
- Build system integration
- Repository management

## Common Commands

```bash
# Switch management
opam switch create 5.1.0
opam switch list
opam switch 5.1.0

# Package operations
opam install dune merlin ocaml-lsp-server
opam upgrade
opam remove <pkg>

# Environment
eval $(opam env)

# Repository
opam repo add coq-released https://coq.inria.fr/opam/released
```

## Dune Integration

```
; dune-project
(lang dune 3.0)
(name my_project)

; dune
(library
 (name my_lib)
 (libraries core))
```

## GF(3) Integration

```ocaml
type trit = Minus | Ergodic | Plus

let trit_of_build_status = function
  | Build_error _ -> Minus
  | Build_warning _ -> Ergodic
  | Build_success -> Plus

let gf3_conserved trits =
  let sum = List.fold_left (fun acc t ->
    acc + match t with Minus -> -1 | Ergodic -> 0 | Plus -> 1
  ) 0 trits in
  sum mod 3 = 0
```

## Canonical Triads

```
opam-ocaml (-1) ⊗ nickel (0) ⊗ geb (+1) = 0 ✓
opam-ocaml (-1) ⊗ lispsyntax-acset (0) ⊗ free-monad-gen (+1) = 0 ✓
```



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 5. Evaluation

**Concepts**: eval, apply, interpreter, environment

### GF(3) Balanced Triad

```
opam-ocaml (+) + SDF.Ch5 (−) + [balancer] (○) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch4: Pattern Matching
- Ch2: Domain-Specific Languages
- Ch7: Propagators

### Connection Pattern

Evaluation interprets expressions. This skill processes or generates evaluable forms.
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