---
name: emacs-info
description: Emacs Info documentation system. Navigate and query Info manuals for Emacs, Elisp, and GNU tools.
version: 1.0.0
---


# Emacs Info Skill

**Trit**: 0 (ERGODIC - documentation mediates between learning and doing)  
**Foundation**: GNU Info + Emacs integration  

## Core Concept

Info is the hypertext documentation format for GNU:
- Structured nodes and menus
- Cross-references between manuals
- Index-based search

## Emacs Commands

```elisp
;; Open Info browser
M-x info

;; Go to specific manual
(info "elisp")
(info "emacs")
(info "org")

;; Search index
M-x info-apropos RET <query> RET

;; Navigate
n - next node
p - previous node
u - up
l - back (history)
```

## Standalone Info

```bash
# Read manual
info emacs
info elisp

# Search
info --apropos=regexp
```

## GF(3) Integration

```elisp
(defun gay-info-trit (node)
  "Return trit based on Info node type."
  (cond
   ((string-prefix-p "Function" node) -1)  ; MINUS: constraint
   ((string-prefix-p "Variable" node) 0)   ; ERGODIC: state
   ((string-prefix-p "Command" node) 1)))  ; PLUS: action
```

## Canonical Triads

```
proofgeneral-narya (-1) ⊗ emacs-info (0) ⊗ xenodium-elisp (+1) = 0 ✓
slime-lisp (-1) ⊗ emacs-info (0) ⊗ geiser-chicken (+1) = 0 ✓
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

### Primary Chapter: 7. Propagators

**Concepts**: propagator, cell, constraint, bidirectional, TMS

### GF(3) Balanced Triad

```
emacs-info (○) + SDF.Ch7 (○) + [balancer] (○) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)


### Connection Pattern

Propagators flow constraints bidirectionally. This skill propagates information.
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