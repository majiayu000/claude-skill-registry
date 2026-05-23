---
name: ocaml
description: OCaml ecosystem = opam + dune + merlin + ocamlformat.
version: 1.0.0
---


# ocaml

OCaml ecosystem = opam + dune + merlin + ocamlformat.

## Atomic Skills

| Skill | Commands | Domain |
|-------|----------|--------|
| opam | 45 | Package manager |
| dune | 20 | Build system |
| merlin | 1 | Editor support |
| ocamlformat | 1 | Formatter |

## Workflow

```bash
opam switch create 5.1.0
eval $(opam env)
opam install dune merlin
dune init project myapp
cd myapp
dune build
dune test
```

## dune-project

```lisp
(lang dune 3.0)
(name myapp)

(library
 (name mylib)
 (libraries str unix))

(executable
 (name main)
 (libraries mylib))
```

## REPL

```bash
utop
dune utop
```



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