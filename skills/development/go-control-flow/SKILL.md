---
name: go-control-flow
description: Use when writing conditionals, loops, or switch statements in Go — including if with initialization, early returns, for loop forms, range, switch, type switches, and blank identifier patterns. Also use when writing a simple if/else or for loop, even if the user doesn't mention guard clauses or variable scoping. Does not cover error flow patterns (see go-error-handling).
license: Apache-2.0
metadata:
  sources: "Effective Go, Google Style Guide"
---

# Go Control Flow

> Read [references/SWITCH-PATTERNS.md](references/SWITCH-PATTERNS.md) when using switch statements, type switches, or break with labels

> Read [references/BLANK-IDENTIFIER.md](references/BLANK-IDENTIFIER.md) when using `_`, blank identifier imports, or compile-time interface checks

---

## If with Initialization

`if` and `switch` accept an optional initialization statement. Use it to scope
variables to the conditional block:

```go
if err := file.Chmod(0664); err != nil {
    log.Print(err)
    return err
}
```

If you need the variable beyond a few lines after the `if`, declare it
separately and use a standard `if` instead:

```go
x, err := f()
if err != nil {
    return err
}
// lots of code that uses x
```

## Indent Error Flow (Guard Clauses)

When an `if` body ends with `break`, `continue`, `goto`, or `return`, omit the
unnecessary `else`. Keep the success path unindented:

```go
f, err := os.Open(name)
if err != nil {
    return err
}
d, err := f.Stat()
if err != nil {
    f.Close()
    return err
}
codeUsing(f, d)
```

Never bury normal flow inside an `else` when the `if` already returns.

---

## Redeclaration and Reassignment

The `:=` short declaration allows redeclaring variables in the same scope:

```go
f, err := os.Open(name)  // declares f and err
d, err := f.Stat()       // declares d, reassigns err
```

A variable `v` may appear in a `:=` declaration even if already declared,
provided:

1. The declaration is in the **same scope** as the existing `v`
2. The value is **assignable** to `v`
3. At least **one other variable** is newly created by the declaration

### Variable Shadowing

**Warning**: If `v` is declared in an outer scope, `:=` creates a **new**
variable that shadows it — a common source of bugs:

```go
// Bug: ctx inside the if block shadows the outer ctx
if *shortenDeadlines {
    ctx, cancel := context.WithTimeout(ctx, 3*time.Second)
    defer cancel()
}
// ctx here is still the original — the shadowed ctx didn't escape

// Fix: use = instead of :=
var cancel func()
ctx, cancel = context.WithTimeout(ctx, 3*time.Second)
```

---

## For Loops

Go's `for` is its only looping construct, unifying `while`, `do-while`, and
C-style `for`:

```go
// Condition-only (Go's "while")
for x > 0 {
    x = process(x)
}

// Infinite loop
for {
    if done() { break }
}

// C-style three-component
for i := 0; i < n; i++ { ... }
```

### Range

`range` iterates over slices, maps, strings, and channels:

```go
for i, v := range slice { ... }   // index + value
for k, v := range myMap { ... }   // key + value (non-deterministic order)
for i, r := range "héllo" { ... } // byte index + rune (not byte)
for v := range ch { ... }         // receives until channel closed
```

**Key rules:**
- Range over strings yields **runes**, not bytes — `i` is the byte offset
- Range over maps has **non-deterministic order** — don't rely on it
- Use `_` to discard the index or value: `for _, v := range slice`

### Parallel Assignment

Go has no comma operator. Use parallel assignment for multiple loop variables:

```go
for i, j := 0, len(a)-1; i < j; i, j = i+1, j-1 {
    a[i], a[j] = a[j], a[i]
}
```

`++` and `--` are statements, not expressions — they cannot appear in parallel
assignment.

---

## Switch: Labeled Break

`break` inside a `switch` within a `for` loop only breaks the switch.
Use a labeled `break` to exit the enclosing loop:

```go
Loop:
    for _, v := range items {
        switch v.Type {
        case "done":
            break Loop  // breaks the for loop
        }
    }
```

For type switches, see **go-interfaces**: Type Switch.

---

## The Blank Identifier

**Never discard errors carelessly** — a nil dereference panic may follow.

Verify interface compliance at compile time: `var _ io.Writer = (*MyType)(nil)`.
See **go-interfaces** for the interface satisfaction check pattern.

---

## Quick Reference

| Pattern | Go Idiom |
|---------|----------|
| If initialization | `if err := f(); err != nil { }` |
| Early return | Omit `else` when if body returns |
| Redeclaration | `:=` reassigns if same scope + new var |
| Shadowing trap | `:=` in inner scope creates new variable |
| Parallel assignment | `i, j = i+1, j-1` |
| Expression-less switch | `switch { case cond: }` |
| Comma cases | `case 'a', 'b', 'c':` |
| No fallthrough | Default behavior (explicit `fallthrough` if needed) |
| Break from loop in switch | `break Label` |
| Discard value | `_, err := f()` |
| Side-effect import | `import _ "pkg"` |
| Interface check | `var _ Interface = (*Type)(nil)` |

---

## Related Skills

- **Error flow**: See [go-error-handling](../go-error-handling/SKILL.md) when structuring guard clauses, early returns, or error-first patterns
- **Type switches**: See [go-interfaces](../go-interfaces/SKILL.md) when using type switches, the comma-ok idiom, or interface satisfaction checks
- **Nesting reduction**: See [go-style-core](../go-style-core/SKILL.md) when reducing nesting depth or resolving formatting questions
- **Variable scoping**: See [go-declarations](../go-declarations/SKILL.md) when using if-init, `:=` redeclaration, or reducing variable scope
