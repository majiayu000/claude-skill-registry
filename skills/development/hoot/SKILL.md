---
name: hoot
description: Scheme→WebAssembly compiler (4K lines info).
version: 1.0.0
---


# hoot

Scheme→WebAssembly compiler (4K lines info).

## Compile

```bash
guild compile-wasm -o out.wasm script.scm
```

## Features

- Full tail call optimization
- First-class continuations
- JavaScript interop
- Standalone Wasm modules

## Example

```scheme
(define-module (my-module)
  #:export (greet))

(define (greet name)
  (string-append "Hello, " name "!"))
```

## Runtime

```javascript
import { Hoot } from '@aspect/guile-hoot';
const mod = await Hoot.load('out.wasm');
mod.greet("World");
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