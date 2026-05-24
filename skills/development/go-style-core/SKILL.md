---
name: go-style-core
description: Use when working with Go formatting, line length, nesting, naked returns, semicolons, or core style principles. Also use when a style question isn't covered by a more specific skill, even if the user doesn't reference a specific style rule. Does not cover domain-specific patterns like error handling, naming, or testing (see specialized skills). Acts as fallback when no more specific style skill applies.
license: Apache-2.0
metadata:
  sources: "Effective Go, Google Style Guide, Uber Style Guide, Go Wiki CodeReviewComments"
---

# Go Style Core Principles

## Style Principles (Priority Order)

When writing readable Go code, apply these principles in order of importance:

### Priority Order

1. **Clarity** — Can a reader understand the code without extra context?
2. **Simplicity** — Is this the simplest way to accomplish the goal?
3. **Concision** — Does every line earn its place?
4. **Maintainability** — Will this be easy to modify later?
5. **Consistency** — Does it match surrounding code and project conventions?

> Read [references/PRINCIPLES.md](references/PRINCIPLES.md) when resolving conflicts between clarity, simplicity, and concision, or when you need concrete examples of how each principle applies in real Go code.

---

## Formatting

Run `gofmt` — no exceptions. There is **no rigid line length limit**, but Uber suggests a soft limit of 99 characters. Break by semantics, not length — refactor rather than just wrap.

> Read [references/FORMATTING.md](references/FORMATTING.md) when configuring gofmt, deciding on line breaks, applying MixedCaps rules, or resolving local consistency questions.

---

## Reduce Nesting

Handle error cases and special conditions first. Return early or continue the loop to keep the "happy path" unindented.

```go
// Bad: Deeply nested
for _, v := range data {
    if v.F1 == 1 {
        v = process(v)
        if err := v.Call(); err == nil {
            v.Send()
        } else {
            return err
        }
    } else {
        log.Printf("Invalid v: %v", v)
    }
}

// Good: Flat structure with early returns
for _, v := range data {
    if v.F1 != 1 {
        log.Printf("Invalid v: %v", v)
        continue
    }

    v = process(v)
    if err := v.Call(); err != nil {
        return err
    }
    v.Send()
}
```

### Unnecessary Else

If a variable is set in both branches of an if, use default + override pattern.

```go
// Bad: Setting in both branches
var a int
if b {
    a = 100
} else {
    a = 10
}

// Good: Default + override
a := 10
if b {
    a = 100
}
```

---

## Naked Returns

A `return` statement without arguments returns the named return values. This is
known as a "naked" return.

```go
func split(sum int) (x, y int) {
    x = sum * 4 / 9
    y = sum - x
    return // returns x, y
}
```

### Guidelines for Naked Returns

- **OK in small functions**: Naked returns are fine in functions that are just a
  handful of lines
- **Be explicit in medium+ functions**: Once a function grows to medium size, be
  explicit with return values for clarity
- **Don't name results just for naked returns**: Clarity of documentation is
  always more important than saving a line or two

```go
// Good: Small function, naked return is clear
func minMax(a, b int) (min, max int) {
    if a < b {
        min, max = a, b
    } else {
        min, max = b, a
    }
    return
}

// Good: Larger function, explicit return
func processData(data []byte) (result []byte, err error) {
    result = make([]byte, 0, len(data))

    for _, b := range data {
        if b == 0 {
            return nil, errors.New("null byte in data")
        }
        result = append(result, transform(b))
    }

    return result, nil // explicit: clearer in longer functions
}
```

See **go-documentation** for guidance on Named Result Parameters.

---

## Semicolons

Go's lexer automatically inserts semicolons after any line whose last token is
an identifier, literal, or one of: `break continue fallthrough return ++ -- ) }`.

This means **opening braces must be on the same line** as the control structure:

```go
// Good: brace on same line
if i < f() {
    g()
}

// Bad: brace on next line — lexer inserts semicolon after f()
if i < f()  // wrong!
{           // wrong!
    g()
}
```

Idiomatic Go only has explicit semicolons in `for` loop clauses and to separate
multiple statements on a single line.

---

## Quick Reference

| Principle | Key Question |
|-----------|--------------|
| Clarity | Can a reader understand what and why? |
| Simplicity | Is this the simplest approach? |
| Concision | Is the signal-to-noise ratio high? |
| Maintainability | Can this be safely modified later? |
| Consistency | Does this match surrounding code? |

## Related Skills

- **Naming conventions**: See [go-naming](../go-naming/SKILL.md) when applying MixedCaps, choosing identifier names, or resolving naming debates
- **Error flow**: See [go-error-handling](../go-error-handling/SKILL.md) when structuring error-first guard clauses or reducing nesting via early returns
- **Documentation**: See [go-documentation](../go-documentation/SKILL.md) when writing doc comments, named return parameters, or package-level docs
- **Linting enforcement**: See [go-linting](../go-linting/SKILL.md) when automating style checks with golangci-lint or configuring CI
- **Code review**: See [go-code-review](../go-code-review/SKILL.md) when applying style principles during a systematic code review
- **Logging style**: See [go-logging](../go-logging/SKILL.md) when reviewing logging practices, choosing between log and slog, or structuring log output
