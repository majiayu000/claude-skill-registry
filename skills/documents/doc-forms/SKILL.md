---
name: doc-forms
description: Reference for The Fold's typed comments and doc forms system. Use when adding type annotations, documentation, todos, or other metadata to Scheme code. Covers (doc ...) syntax, standard tags, search commands, and type checker integration.
allowed-tools: Bash(./fold:*), Read, Edit, Grep, Glob
---

# Doc Forms (Typed Comments)

The Fold uses `(doc ...)` forms for searchable, introspectable annotations that survive in source code.

## Basic Syntax

### Contextual (belongs to enclosing definition)

```scheme
(define (add x y)
  (doc 'type (-> Int Int Int))
  (doc 'description "Adds two numbers")
  (+ x y))
```

### Targeted (names what it documents)

```scheme
(doc factorial 'type (-> Int Int))
(define (factorial n)
  (if (= n 0) 1 (* n (factorial (- n 1)))))
```

## Semantics

| Property | Behavior |
|----------|----------|
| Arguments | NOT evaluated (pure metadata) |
| Return value | `void` — use in sequences, not value positions |
| Normalization | Stripped — code with/without docs hashes identically |
| Extraction | Tooling reads from source (`lf-todo`, `lf-types`) |
| Type authority | **Authoritative** — `(doc f 'type ...)` takes precedence over inference |

## Standard Tags

| Tag | Purpose | Example |
|-----|---------|---------|
| `'type` | Type signature | `(doc 'type (-> Int Int))` |
| `'description` | Human-readable description | `(doc 'description "Adds two numbers")` |
| `'param` | Parameter documentation | `(doc 'param 'x "The first operand")` |
| `'returns` | Return value description | `(doc 'returns "The sum")` |
| `'todo` | Work to be done | `(doc 'todo "Optimize for large inputs")` |
| `'fixme` | Known issue | `(doc 'fixme "Edge case with negative numbers")` |
| `'deprecated` | Deprecation notice | `(doc 'deprecated "Use add-safe instead")` |
| `'since` | Version introduced | `(doc 'since "1.2.0")` |
| `'see` | Related items | `(doc 'see 'subtract)` |
| `'note` | Implementation note | `(doc 'note "Uses memoization internally")` |

## Search Commands

After loading `lattice/meta/docs.ss`:

```scheme
(lf-todo)           ; Find all todos in codebase
(lf-types)          ; Find all type annotations
(docs-for 'symbol)  ; Find docs for specific target
(doc-stats)         ; Count docs by tag
```

## Type Checker Integration

Doc type annotations integrate with both the LSP and type inference:

| Component | Behavior |
|-----------|----------|
| LSP hover | Shows doc-declared types with highest priority |
| Type inference | Uses declared types via `lookup-declared-type` in `core/types/infer.ss` |
| Bridge | `load-doc-types-into-checker!` populates type checker from doc index |

### Example: Declaring Types for Inference

```scheme
;; The type checker will trust this annotation
(doc my-complex-fn 'type (-> (List Int) (Maybe Int)))
(define (my-complex-fn lst)
  ;; Complex implementation...
  )
```

## Todos vs BBS Issues

| Use Case | When to Use |
|----------|-------------|
| `(doc 'todo ...)` | Colocated with code, for localized improvements (performance, refactoring, cleanup) |
| BBS issue | Tracked work items, features, bugs, cross-cutting concerns, things needing scheduling |

**Rule of thumb:** If it needs to be scheduled or tracked across sessions, use BBS. If it's a note-to-self next to the code, use `(doc 'todo ...)`.

## Examples

### Full Function Documentation

```scheme
(define (binary-search vec target)
  (doc 'type (-> (Vector Int) Int (Maybe Int)))
  (doc 'description "Binary search for target in sorted vector")
  (doc 'param 'vec "Sorted vector of integers")
  (doc 'param 'target "Value to find")
  (doc 'returns "Index wrapped in Just, or Nothing if not found")
  (doc 'todo "Add bounds checking")
  ;; implementation...
  )
```

### Deprecation

```scheme
(doc old-api 'deprecated "Use new-api instead. Will be removed in 2.0")
(define (old-api x) (new-api x))
```

### Module-Level Documentation

```scheme
;; At top of file
(doc 'description "Matrix operations for linear algebra")
(doc 'since "1.0.0")
(doc 'see 'linalg/vec)
```
