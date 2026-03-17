---
name: ocaml
description: OCaml ecosystem = opam + dune + merlin + ocamlformat.
metadata:
  trit: 0
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
