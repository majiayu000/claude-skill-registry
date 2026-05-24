---
name: dev-tools
description: Developer tools for The Fold - protocols (extensible dispatch), protocol bundles, refactoring toolkit (rename, move, dead code), and template DSL. Use when defining new protocols, refactoring code, or generating S-expressions.
allowed-tools: Bash(./fold:*), Read, Edit, Write, Grep, Glob
---

# Developer Tools

Power-user tools for protocol definition, refactoring, and code generation.

## Open Protocol System

Extensible type dispatch for the Open/Closed Principle (`lattice/fp/protocol.ss`).

Objects must be tagged lists: `(list 'type-tag ...)`. Dispatch is O(1) via hashtable.

```scheme
(load "lattice/fp/protocol.ss")

;; Define a protocol (generic operation)
(define-protocol (draw obj ctx) "Draw object to context")

;; Register implementations per type tag
(implement-protocol! 'draw 'circle
  (lambda (c ctx) (draw-circle (circle-center c) ctx)))
(implement-protocol! 'draw 'rectangle
  (lambda (r ctx) (draw-rect (rect-pos r) ctx)))

;; Use (automatic dispatch via type tag)
(draw my-circle canvas)  ; calls circle implementation
```

### Key Functions

| Function | Purpose |
|----------|---------|
| `define-protocol` | Create a new protocol with signature and docstring |
| `implement-protocol!` | Register implementation for a type tag |
| `protocol-implementations` | List all implementations of a protocol |
| `protocol?` | Check if a symbol names a protocol |

## Protocol Bundles

Reduce boilerplate when implementing multiple related protocols (`lattice/fp/protocol-bundle.ss`).

```scheme
(load "lattice/fp/protocol-bundle.ss")

;; Define a bundle of related protocol pairs (getter, setter)
(define-protocol-bundle body-ops
  ((body-pos body-set-pos) "pos")
  ((body-vel body-set-vel) "vel")
  ((body-mass body-set-mass) "mass"))

;; Derive implementations using naming convention: <prefix>-<field>, <prefix>-with-<field>
(derive-bundle! body-ops 'rigid-body-2d rigid-body)

;; With overrides for slots that don't follow the convention
(derive-bundle! body-ops 'particle particle
  ("mass" (lambda (p) 1.0) (lambda (p m) p)))  ; Particles have implicit mass

;; Explicit implementation when convention doesn't apply
(implement-bundle! body-ops 'custom-body
  ("pos" custom-get-pos custom-set-pos)
  ("vel" custom-get-vel custom-set-vel)
  ("mass" custom-get-mass custom-set-mass))
```

### Introspection

```scheme
(bundle-types bundle)      ; List types implementing this bundle
(bundle-protocols bundle)  ; List protocols in this bundle
(list-bundles)             ; List all defined bundles
```

## Refactoring Toolkit

Unified interface for codebase refactoring (`boundary/tools/refactor-toolkit.ss`).

```scheme
(load "boundary/tools/refactor-toolkit.ss")

;; Help and discovery
(refactor 'help)                           ; Show all operations
```

### Rename Symbols

```scheme
;; Preview rename (shows all affected files)
(refactor 'rename 'old-name 'new-name)

;; Apply staged changes
(refactor 'apply)
```

### Move Symbols

```scheme
;; Preview move (shows source/target changes)
(refactor 'move 'symbol "target-file.ss")

;; Apply staged move
(refactor-move-apply!)
```

### Dead Code Analysis

```scheme
;; Scan entire codebase
(refactor 'dead-code)

;; Scan specific path
(refactor 'dead-code "lattice/fp")
```

### Dependency Analysis

```scheme
;; Show callers and callees
(refactor 'deps 'symbol)
```

### Change Management

```scheme
(refactor 'status)   ; Show pending changes
(refactor 'undo)     ; Undo last operation
(refactor 'clear)    ; Discard pending changes
```

### Quick Aliases

| Alias | Full Command |
|-------|--------------|
| `rr` | `(refactor 'rename ...)` |
| `rm` | `(refactor 'move ...)` |
| `rd` | `(refactor 'deps ...)` |
| `rdc` | `(refactor 'dead-code ...)` |

## Template DSL (AI Code Generation)

Grammar-driven code construction for building S-expressions without tracking parentheses.

**Files:**
- `lattice/dsl/template/template.ss` (core)
- `boundary/tools/template-session.ss` (session)
- `boundary/tools/template-parser.ss` (parser)

### Batch Mode (Recommended)

```scheme
(load "boundary/tools/template-parser.ss")

;; Build quicksort - template with holes, then fill them
(tp-batch "
  define (qs lst) $body
  --- $body := if $cond $then $else
  --- $cond := null? lst
  --- $then := '()
  --- $else := append (qs (filter $pred (cdr lst))) (cons (car lst) (qs (filter $pred2 (cdr lst))))
  --- $pred := lambda (x) (< x (car lst))
  --- $pred2 := lambda (x) (>= x (car lst))
")
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| Holes (`$name`) | Non-terminals that get filled incrementally |
| Implicit parens | Multi-token statements get automatic outer `()` |
| Batch separator | `---` chains definitions/fills in sequence |

### Interactive Mode

```scheme
(load "boundary/tools/template-session.ss")

;; Start a template session
(tp-start)

;; Define template with holes
(tp "define (factorial n) $body")

;; Fill holes incrementally
(tp-fill '$body "if (= n 0) 1 (* n (factorial (- n 1)))")

;; Get result
(tp-result)  ; => (define (factorial n) (if (= n 0) 1 (* n (factorial (- n 1)))))
```

### When to Use Template DSL

- Building complex nested S-expressions
- AI-generated code (avoids parenthesis counting errors)
- Incremental code construction
- Code with repeated patterns
