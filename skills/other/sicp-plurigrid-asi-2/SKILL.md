---
name: sicp
description: "SICP: Structure and Interpretation of Computer Programs - computational processes, abstraction, and metalinguistic design"
license: CC-BY-SA-4.0
metadata:
  source: info-geometric-morphism
  trit: -1
  gf3_conserved: true
  xenomodern: true
  ironic_detachment: 0.42
---

# SICP Skill

> *"Programs must be written for people to read, and only incidentally for machines to execute."*
> — Abelson & Sussman

Geometric morphism translation from sicp.info preserving the hierarchical node structure as an ACSet with GF(3) coloring for trifurcated processing.

## Overview

**Structure and Interpretation of Computer Programs** (Second Edition)  
by Harold Abelson and Gerald Jay Sussman, with Julie Sussman  
Foreword by Alan J. Perlis  
© 1996 Massachusetts Institute of Technology

The wizard book for computational thinking—procedures as abstractions, data as abstractions, and the interpreter as the ultimate abstraction.

## Chapters

### Chapter 1: Building Abstractions with Procedures [PLUS]

- **1-1**: The Elements of Programming (expressions, naming, evaluation)
- **1-2**: Procedures and the Processes They Generate (recursion, iteration, orders of growth)
- **1-3**: Formulating Abstractions with Higher-Order Procedures (λ, returned values)

Key concepts: Substitution model, lexical scoping, fixed points, Newton's method

### Chapter 2: Building Abstractions with Data [ERGODIC]

- **2-1**: Introduction to Data Abstraction (rational numbers, barriers)
- **2-2**: Hierarchical Data and the Closure Property (sequences, trees, picture language)
- **2-3**: Symbolic Data (quotation, differentiation, sets, Huffman encoding)
- **2-4**: Multiple Representations for Abstract Data (tagged data, data-directed programming)
- **2-5**: Systems with Generic Operations (type coercion, symbolic algebra)

Key concepts: Pairs, cons/car/cdr, closure property, abstraction barriers, message passing

### Chapter 3: Modularity, Objects, and State [PLUS]

- **3-1**: Assignment and Local State (set!, costs of assignment)
- **3-2**: The Environment Model of Evaluation (frames, procedure objects)
- **3-3**: Modeling with Mutable Data (queues, tables, digital circuits, constraints)
- **3-4**: Concurrency: Time Is of the Essence (serializers, deadlock)
- **3-5**: Streams (delayed evaluation, infinite streams, signal processing)

Key concepts: State, identity, time, streams vs objects duality

### Chapter 4: Metalinguistic Abstraction [PLUS]

- **4-1**: The Metacircular Evaluator (eval/apply, syntax procedures, environments)
- **4-2**: Variations on a Scheme (lazy evaluation, normal vs applicative order)
- **4-3**: Variations on a Scheme: Nondeterministic Computing (amb, backtracking)
- **4-4**: Logic Programming (unification, pattern matching, query systems)

Key concepts: eval/apply loop, special forms, thunks, amb evaluator, Prolog-style logic

### Chapter 5: Computing with Register Machines [ERGODIC]

- **5-1**: Designing Register Machines (data paths, controllers, subroutines)
- **5-2**: A Register-Machine Simulator (the machine model, assembler)
- **5-3**: Storage Allocation and Garbage Collection (vectors, stop-and-copy)
- **5-4**: The Explicit-Control Evaluator (machine code for Scheme)
- **5-5**: Compilation (structure of compiler, lexical addressing, interfacing)

Key concepts: Register allocation, continuation-passing, tail recursion, compilation

## GF(3) Conservation

The Info file nodes distribute perfectly across GF(3) trits:

```
Total nodes: 138
MINUS (-1):  46  ████████████████
ERGODIC (0): 46  ████████████████
PLUS (+1):   46  ████████████████
Sum mod 3:   0
Conserved:   ✓ BALANCED
```

This perfect 46/46/46 distribution enables optimal trifurcated parallel processing.

## ACSet Schema (Geometric Morphism)

The translation from Info to Skill uses a geometric morphism `f: InfoTopos → SkillTopos`:

```
Objects (Ob):
  Node      - Info nodes (sections, subsections)
  Edge      - Navigation and reference links
  Content   - Extracted text and code blocks

Morphisms (Hom):
  next: Node → Node     - Sequential navigation
  prev: Node → Node     - Backward navigation  
  up:   Node → Node     - Hierarchical parent
  menu: Node → Node     - Chapter/section containment
  xref: Node → Node     - Cross-references (*Note)

Attributes:
  trit: Node → GF(3)    - Deterministic color assignment
  text: Node → String   - Node content
```

## Integration with Gay.jl

The GF(3) coloring uses the same SplitMix64 hash as Gay.jl:

```julia
using Gay

# Color SICP nodes deterministically
for node in sicp_nodes
    seed = hash(node.id)
    color = gay_color(seed)  # Returns palette with GF(3) trit
    node.trit = color.trit
end

# Verify conservation
@assert sum(n.trit for n in sicp_nodes) % 3 == 0
```

## Commands

```bash
# Read in Emacs
info sicp

# Re-translate with geometric morphism
bb info_to_skill_morphism.bb translate sicp.info

# Verify grammar and GF(3) conservation
bb info_to_skill_morphism.bb verify sicp.info

# Parse to CRDT-style sexp
bb info_to_skill_morphism.bb parse sicp.info > sicp.sexp
```

## References

- [Full text online](https://mitpress.mit.edu/sites/default/files/sicp/full-text/book/book.html)
- [MIT OCW 6.001](https://ocw.mit.edu/courses/6-001-structure-and-interpretation-of-computer-programs-spring-2005/)
- [SICP Distilled](https://www.sicpdistilled.com/) (Clojure version)
