---
name: srfi
description: SRFI Skill
version: 1.0.0
---

# SRFI Skill

> *"SRFIs extend the Scheme programming language. You can help."*
> — srfi.schemers.org

Scheme Requests for Implementation: portable library specifications with GF(3) categorization.

## Overview

SRFIs are community-driven specifications that extend Scheme beyond R5RS/R6RS/R7RS. Each SRFI has a unique number, status (draft/final/withdrawn), and reference implementation.

## Core SRFIs by Category

### Data Structures [MINUS: -1]

| SRFI | Name | Status | Key Exports |
|------|------|--------|-------------|
| 1 | List Library | Final | `fold`, `unfold`, `filter`, `partition` |
| 4 | Homogeneous Vectors | Final | `u8vector`, `f64vector`, typed arrays |
| 9 | Defining Record Types | Final | `define-record-type` |
| 14 | Character Sets | Final | `char-set`, `char-set-contains?` |
| 69 | Basic Hash Tables | Final | `make-hash-table`, `hash-table-ref` |
| 113 | Sets and Bags | Final | `set`, `bag`, `set-contains?` |
| 125 | Intermediate Hash Tables | Final | `hash-table-map`, comparators |
| 128 | Comparators (Reduced) | Final | `make-comparator`, `comparator-hash` |
| 133 | Vector Library | Final | `vector-map`, `vector-fold` |
| 146 | Mappings | Final | `mapping`, functional maps |
| 158 | Generators and Accumulators | Final | `make-coroutine-generator` |

### Control Flow [ERGODIC: 0]

| SRFI | Name | Status | Key Exports |
|------|------|--------|-------------|
| 2 | AND-LET* | Final | `and-let*` short-circuit binding |
| 8 | receive | Final | `receive` for multiple values |
| 11 | let-values | Final | `let-values`, `let*-values` |
| 18 | Multithreading | Final | `make-thread`, `mutex`, `condition-variable` |
| 34 | Exception Handling | Final | `guard`, `raise` |
| 39 | Parameter Objects | Final | `make-parameter`, `parameterize` |
| 45 | Primitives for Lazy Eval | Final | `delay`, `force`, `lazy` |
| 124 | Ephemerons | Final | `make-ephemeron`, weak references |
| 154 | First-Class Dynamic Extents | Final | `dynamic-extent`, delimited continuations |
| 155 | Promises | Final | `delay-force`, iterative lazy |
| 226 | Control Features | Final | `call/cc`, `values`, `dynamic-wind` |

### Syntax & Macros [PLUS: +1]

| SRFI | Name | Status | Key Exports |
|------|------|--------|-------------|
| 0 | Feature-Based Conditionals | Final | `cond-expand` |
| 6 | Basic String Ports | Final | `open-input-string`, `get-output-string` |
| 26 | Cut/Cute | Final | `cut`, `cute` partial application |
| 42 | Eager Comprehensions | Final | `list-ec`, `sum-ec`, `do-ec` |
| 46 | Syntax for Multiple Values | Final | `values->list`, `values->vector` |
| 57 | Records | Withdrawn | (superseded by 99, 136) |
| 72 | Hygienic Macros | Final | `syntax-case` compatible |
| 139 | Syntax Parameters | Final | `define-syntax-parameter` |
| 147 | Custom Macro Transformers | Final | `er-macro-transformer` |
| 149 | Basic Syntax-Rules Extensions | Final | `_`, `...` patterns |
| 211 | Scheme Macros for Definitions | Final | `define-macro` |

### I/O & System [MINUS: -1]

| SRFI | Name | Status | Key Exports |
|------|------|--------|-------------|
| 6 | Basic String Ports | Final | in-memory I/O |
| 28 | Basic Format Strings | Final | `format` |
| 38 | External Representation with Cycles | Final | `write/ss`, `read/ss` |
| 48 | Intermediate Format Strings | Final | `format` with more directives |
| 106 | Basic Socket Interface | Final | `make-client-socket`, `socket-send` |
| 170 | POSIX API | Final | `file-info`, `set-file-mode!` |
| 180 | JSON | Final | `json-read`, `json-write` |
| 192 | Port Positioning | Final | `port-position`, `set-port-position!` |
| 193 | Command Line | Final | `command-line`, `option-processor` |

### Numeric [ERGODIC: 0]

| SRFI | Name | Status | Key Exports |
|------|------|--------|-------------|
| 27 | Sources of Random Bits | Final | `random-integer`, `random-real` |
| 60 | Integers as Bits | Final | `bitwise-and`, `bit-set?` |
| 94 | Type-Restricted Numerics | Final | `fx+`, `fl*` |
| 141 | Integer Division | Final | `floor/`, `ceiling/`, `truncate/` |
| 143 | Fixnums | Final | `fx+`, `fxarithmetic-shift` |
| 144 | Flonums | Final | `fl+`, `flsin`, `flexp` |
| 151 | Bitwise Ops on Arbitrary Integers | Final | `bitwise-ior`, `integer-length` |
| 166 | Monadic Formatting | Final | `format` with monadic composition |

### Testing & Debugging [PLUS: +1]

| SRFI | Name | Status | Key Exports |
|------|------|--------|-------------|
| 64 | A Scheme API for Test Suites | Final | `test-begin`, `test-equal`, `test-assert` |
| 78 | Lightweight Testing | Final | `check`, `check-ec` |
| 219 | Define Higher-Order Lambda | Final | `define` with curry |

### Pattern Matching [PLUS: +1]

| SRFI | Name | Status | Key Exports |
|------|------|--------|-------------|
| 204 | Wright-Cartwright-Shinn Pattern Matcher | Final | `match`, `match-lambda` |

## GF(3) Distribution

```
MINUS (-1):  Data Structures, I/O & System
ERGODIC (0): Control Flow, Numeric
PLUS (+1):   Syntax & Macros, Testing, Pattern Matching

Conservation: Σ(categories) ≡ 0 (mod 3) when balanced usage
```

## R7RS-Large Libraries (Red/Tangerine Editions)

R7RS-Large incorporates SRFIs as standard libraries:

### Red Edition (2019)
- `(scheme list)` ← SRFI 1
- `(scheme vector)` ← SRFI 133
- `(scheme sort)` ← SRFI 132
- `(scheme set)` ← SRFI 113
- `(scheme charset)` ← SRFI 14
- `(scheme hash-table)` ← SRFI 125
- `(scheme ilist)` ← SRFI 116
- `(scheme rlist)` ← SRFI 101
- `(scheme ideque)` ← SRFI 134
- `(scheme text)` ← SRFI 135
- `(scheme generator)` ← SRFI 158
- `(scheme lseq)` ← SRFI 127
- `(scheme stream)` ← SRFI 41
- `(scheme box)` ← SRFI 111
- `(scheme list-queue)` ← SRFI 117
- `(scheme comparator)` ← SRFI 128

### Tangerine Edition (2021)
- `(scheme bitwise)` ← SRFI 151
- `(scheme fixnum)` ← SRFI 143
- `(scheme flonum)` ← SRFI 144
- `(scheme division)` ← SRFI 141
- `(scheme bytevector)` ← R6RS
- `(scheme mapping)` ← SRFI 146
- `(scheme regex)` ← SRFI 115

## Implementation Support Matrix

| SRFI | Chez | Chicken | Gauche | Guile | Racket |
|------|------|---------|--------|-------|--------|
| 1 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 9 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 18 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 27 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 64 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 125 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 158 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 180 | ✓ | ✓ | ✓ | ✓ | ✓ |

## SRFI-27: Random Sources (Key for Gay.jl Bridge)

```scheme
;; SRFI-27 provides the abstraction layer for splittable RNG
(import (srfi 27))

;; Create a random source with specific seed
(define my-source (make-random-source))
(random-source-pseudo-randomize! my-source 1069 42)

;; Get integers and reals
(define rand-int (random-source-make-integers my-source))
(define rand-real (random-source-make-reals my-source))

;; GF(3) trit from random source
(define (random-trit source)
  (- ((random-source-make-integers source) 3) 1))
```

## SRFI-171: Transducers

```scheme
;; Composable sequence transformations
(import (srfi 171))

;; Filter, map, take composed
(define xform
  (compose
    (tfilter even?)
    (tmap (lambda (x) (* x x)))
    (ttake 5)))

;; Apply to list
(list-transduce xform rcons '(1 2 3 4 5 6 7 8 9 10))
;; => (4 16 36 64 100)
```

## SRFI-204: Pattern Matching

```scheme
(import (srfi 204))

;; Destructuring with guards
(match '(1 2 3)
  ((x y z) (guard (< x y z)) (list z y x))
  (_ 'no-match))
;; => (3 2 1)

;; Quasiquote patterns
(match '(lambda (x) (+ x 1))
  (`(lambda (,var) (+ ,var 1)) var)
  (_ #f))
;; => x
```

## Integration with Little Schemer

| SRFI | Little Schemer Concept |
|------|------------------------|
| 1 | `member?`, `rember`, `firsts` |
| 9 | Atoms as records |
| 27 | Y combinator with random exploration |
| 45 | Lazy evaluation (Seasoned Ch. 16) |
| 154 | Continuations (Seasoned Ch. 13) |
| 171 | Collectors as transducers |
| 204 | Pattern matching vs cond |

## Commands

```bash
# Search SRFIs by keyword
srfi search "hash table"

# Show SRFI abstract
srfi show 125

# Clone SRFI implementation
srfi clone 171

# Open in browser
srfi open 204

# List all final SRFIs
srfi list --status final
```

## References

- [srfi.schemers.org](https://srfi.schemers.org/) - Official SRFI home
- [docs.scheme.org/srfi/support](https://docs.scheme.org/srfi/support/) - Implementation matrix
- [R7RS-Large](https://github.com/johnwcowan/r7rs-work/blob/master/R7RSHomePage.md) - Standard incorporation
- [Practical Scheme SRFI Cross-Reference](https://practical-scheme.net/wiliki/schemexref.cgi?SRFI)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 3. Variations on an Arithmetic Theme

**Concepts**: generic arithmetic, coercion, symbolic, numeric

### GF(3) Balanced Triad

```
srfi (○) + SDF.Ch3 (○) + [balancer] (○) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch1: Flexibility through Abstraction
- Ch5: Evaluation
- Ch4: Pattern Matching
- Ch2: Domain-Specific Languages
- Ch6: Layering

### Connection Pattern

Generic arithmetic crosses type boundaries. This skill handles heterogeneous data.
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