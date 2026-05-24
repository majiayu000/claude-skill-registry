---
name: guile
description: GNU Scheme interpreter (67K lines info).
version: 1.0.0
---


# guile

GNU Scheme interpreter (67K lines info).

```bash
guile [options] [script [args]]

-L <dir>    Add load path
-l <file>   Load source
-e <func>   Apply function
-c <expr>   Evaluate expression
-s <script> Execute script
```

## REPL

```scheme
(define (factorial n)
  (if (<= n 1) 1 (* n (factorial (- n 1)))))

(use-modules (ice-9 match))
(match '(1 2 3) ((a b c) (+ a b c)))
```

## Modules

```scheme
(use-modules (srfi srfi-1))   ; List library
(use-modules (ice-9 receive)) ; Multiple values
(use-modules (ice-9 format))  ; Formatted output
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