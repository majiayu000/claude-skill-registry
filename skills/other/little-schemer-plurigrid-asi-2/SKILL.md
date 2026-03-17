---
name: little-schemer
description: 'Little Schemer Skill'
version: 1.0.0
---

# Little Schemer Skill

> *"The Law of Car: The primitive car is defined only for non-empty lists."*
> — Friedman & Felleisen

The Friedman/Felleisen pedagogical tradition: learn by asking questions, build understanding through recursion.

## Overview

The "Little" book series by Daniel P. Friedman and collaborators teaches programming through Socratic dialogue—questions and answers that build understanding layer by layer, like peeling an onion.

## The Books

### The Little LISPer (1974, 1986, 1989) [MINUS]
**Authors**: Daniel P. Friedman, Matthias Felleisen
**Focus**: Original LISP foundations

The precursor—introduced the Q&A pedagogical style.

### The Little Schemer (1995) [PLUS]
**Authors**: Daniel P. Friedman, Matthias Felleisen
**Foreword**: Gerald Jay Sussman
**Focus**: Recursive thinking and the nature of computation

Ten Commandments + Five Laws:
1. **Car**: Only defined for non-empty lists
2. **Cdr**: Only defined for non-empty lists  
3. **Cons**: Takes two arguments, second must be list
4. **Null?**: Only defined for lists
5. **Eq?**: Takes two non-numeric atoms

Key concepts: `atom?`, `lat?`, recursion, `cond`, the Y combinator

### The Seasoned Schemer (1995) [ERGODIC]
**Authors**: Daniel P. Friedman, Matthias Felleisen
**Focus**: Continuations, state, and the nature of computation

Nineteen Commandments extending the original ten:
- **set!** and mutation
- **letcc** (call/cc)
- **letrec** for local recursion
- Collectors and continuation-passing style

Key concepts: `letcc`, `try`, collectors, the `Y!` combinator

### The Reasoned Schemer (2005, 2018) [PLUS]
**Authors**: Daniel P. Friedman, William E. Byrd, Oleg Kiselyov
**Focus**: Logic programming in Scheme (miniKanren)

Introduces relational programming:
- `run`, `fresh`, `conde`, `==`
- Unification and search
- Relations vs functions

Key concepts: miniKanren, `defrel`, `appendo`, relational arithmetic

### A Little Java, A Few Patterns (1998) [MINUS]
**Authors**: Matthias Felleisen, Daniel P. Friedman
**Focus**: Visitor pattern and OO design in Java

Pizza → Java translation of Schemer concepts:
- Abstract classes as datatypes
- Visitor pattern for recursion
- Interpreters and protocols

### The Little MLer (1997) [ERGODIC]
**Authors**: Matthias Felleisen, Daniel P. Friedman
**Focus**: Type systems and ML

Types as contracts:
- Pattern matching
- Algebraic data types
- Parametric polymorphism

### The Little Prover (2015) [PLUS]
**Authors**: Daniel P. Friedman, Carl Eastlund
**Focus**: Inductive proofs with ACL2/J-Bob

Total functions and induction:
- `defun` with termination
- `dethm` for theorems
- Rewriting and induction

Key concepts: J-Bob theorem prover, inductive proofs, totality

### The Little Typer (2018) [MINUS]
**Authors**: Daniel P. Friedman, David Thrane Christiansen
**Foreword**: Robert Harper
**Focus**: Dependent types with Pie

Types as propositions:
- `Π` (Pi) and `Σ` (Sigma) types
- `=` (equality types)
- `ind-Nat` (induction principle)

Key concepts: Pie language, Curry-Howard, normalization

### The Little Learner (2023) [ERGODIC]
**Authors**: Daniel P. Friedman, Anurag Mendhekar
**Focus**: Deep learning from first principles

Tensors and gradients:
- Scalar, tensor operations
- Automatic differentiation
- Neural networks as compositions

Key concepts: Malt DSL, backpropagation, gradient descent

## Extended Family

### How to Design Programs (HtDP) [PLUS]
**Authors**: Matthias Felleisen, Robert Bruce Findler, Matthew Flatt, Shriram Krishnamurthi
**Focus**: Systematic program design

Design recipes:
1. Data definitions
2. Signature, purpose, header
3. Examples
4. Template
5. Definition
6. Tests

### Essentials of Programming Languages (EOPL) [PLUS]
**Authors**: Daniel P. Friedman, Mitchell Wand
**Focus**: Interpreters and language implementation

Chapters: Expressions, environment-passing, continuation-passing, types, modules, objects

### Semantics Engineering with PLT Redex [ERGODIC]
**Authors**: Matthias Felleisen, Robert Bruce Findler, Matthew Flatt
**Focus**: Operational semantics modeling

Reduction semantics, context-sensitive rewriting, testing language definitions

### Software Design for Flexibility [MINUS]
**Authors**: Chris Hanson, Gerald Jay Sussman
**Focus**: Extensible systems design

Continuations of SICP's spirit: combinators, generic operations, propagators

## GF(3) Distribution

```
MINUS (-1): Little LISPer, A Little Java, Little Typer, Software Design
ERGODIC (0): Seasoned Schemer, Little MLer, Little Learner, Semantics Engineering
PLUS (+1): Little Schemer, Reasoned Schemer, Little Prover, HtDP, EOPL

Total: 12 books, balanced across GF(3)
```

## The Pedagogical Pattern

All books follow the "onion" structure:

```scheme
(define learning
  (lambda (concept)
    (cond
      ((atom? concept) (ask-question concept))
      (else
        (cons (learning (car concept))
              (learning (cdr concept)))))))
```

Each chapter builds on the previous, with questions that:
1. Test understanding of primitives
2. Build toward complex recursion
3. Culminate in a powerful abstraction (Y, letcc, unification, etc.)

## Cross-References to SICP

| Little Schemer | SICP |
|----------------|------|
| Chapter 9 (Y combinator) | 4.1 (Metacircular evaluator) |
| Chapter 10 (collector) | 3.5 (Streams) |
| Seasoned Ch. 13 (letcc) | 4.3 (amb evaluator) |
| Reasoned (miniKanren) | 4.4 (Logic programming) |
| Little Typer (Pie) | — (beyond SICP scope) |
| Little Learner | — (modern ML) |

## Integration with bevy-tile-walk

The recursive substitution rules in `hat_spectre.rs` mirror the Little Schemer's approach:

```rust
// Metatile substitution ≈ recursive list processing
fn substitute(metatile: MetatileType, depth: usize) -> Vec<MetatileType> {
    if depth == 0 {
        return vec![metatile];  // Base case (atom?)
    }
    let children = match metatile { ... };  // Recursive case
    children.into_iter()
        .flat_map(|m| substitute(m, depth - 1))
        .collect()
}
```

## Commands

```bash
# Run Scheme REPL with Little Schemer exercises
chez-scheme --libdirs lib/scheme

# miniKanren for Reasoned Schemer
(import (minikanren))
(run* (q) (appendo '(a b) '(c d) q))

# Pie for Little Typer
pie repl

# Malt for Little Learner
racket -l malt
```

## References

- [felleisen.org/matthias/books.html](https://felleisen.org/matthias/books.html)
- [The Little Schemer Google Group](mailto:schemer-books@googlegroups.com)
- [HtDP Online](https://htdp.org/)
- [miniKanren.org](http://minikanren.org/)
- [The Pie Language](https://github.com/the-little-typer/pie)
