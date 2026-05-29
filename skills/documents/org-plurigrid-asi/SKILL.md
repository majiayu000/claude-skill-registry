---
name: org
description: Org-mode manual (25K lines info).
version: 1.0.0
---


# org

Org-mode manual (25K lines info).

## Structure

```org
* Heading 1
** Heading 2
*** TODO Task [#A]
    DEADLINE: <2025-12-25>
    :PROPERTIES:
    :CUSTOM_ID: task-1
    :END:
```

## Markup

```org
*bold* /italic/ _underline_ =verbatim= ~code~
[[https://example.com][Link]]
#+BEGIN_SRC python
print("hello")
#+END_SRC
```

## Keys

```
TAB       Cycle visibility
C-c C-t   Toggle TODO
C-c C-s   Schedule
C-c C-d   Deadline
C-c C-c   Execute/toggle
C-c '     Edit src block
```

## Export

```elisp
(org-export-dispatch)  ; C-c C-e
```

## Conceptual distinction and mapping

The logical leap is from the concrete org-mode syntax to the abstract Org category: org-mode is an Emacs implementation, while Org is the categorical structure the syntax realizes.

- Org (Category): abstract category of outline structures.
- org-mode (Emacs): concrete implementation and interaction layer.
- Analogy: org-mode : Org :: justfile : just (Just monad as execution context).
- Structure / Outliner: headings define a tree; links add cross-edges.
- Cat-enriched operad: headings act as operations; nesting composes operations.
- Morphisms: links between headings; Poly(p₁⊗...⊗pₘ, q) types a heading from m inputs to one output.



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 9. Generic Procedures

**Concepts**: dispatch, multimethod, predicate dispatch, generic

### GF(3) Balanced Triad

```
org (○) + SDF.Ch9 (○) + [balancer] (○) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch1: Flexibility through Abstraction
- Ch2: Domain-Specific Languages
- Ch6: Layering

### Connection Pattern

Generic procedures dispatch on predicates. This skill selects implementations dynamically.
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