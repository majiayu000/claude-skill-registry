---
name: emacs
description: Emacs ecosystem = elisp + org + gnus + tramp + eglot.
version: 1.0.0
---


# emacs

Emacs ecosystem = elisp + org + gnus + tramp + eglot.

## Atomic Skills

| Skill | Lines | Domain |
|-------|-------|--------|
| elisp | 106K | Programming |
| org | 25K | Documents |
| gnus | 15K | Mail/News |
| tramp | 8K | Remote files |
| eglot | 2K | LSP |
| transient | 3K | Menus |

## Info Access

```
C-h i           Info browser
C-h i m elisp   Elisp manual
C-h i m org     Org manual
C-h f           Describe function
C-h v           Describe variable
```

## Init

```elisp
(use-package org
  :config
  (setq org-directory "~/org"))

(use-package eglot
  :hook ((python-mode . eglot-ensure)))
```

## FloxHub

```bash
flox pull bmorphism/effective-topos
emacs --with-profile topos
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