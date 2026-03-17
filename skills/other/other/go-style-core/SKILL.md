---
name: go-style-core
description: Core Go style principles and formatting guidelines from Google and Uber style guides. Use when writing any Go code to ensure clarity, simplicity, and consistency. This is the foundational skill - other Go style skills build on these principles.
---

# Go Style Core Principles

> **Normative**: This guidance is required per Google's canonical Go style
> guide.

## Style Principles (Priority Order)

When writing readable Go code, apply these principles in order of importance:

### 1. Clarity

The code's purpose and rationale must be clear to the reader.

- **What**: Use descriptive names, helpful comments, and efficient organization
- **Why**: Add commentary explaining rationale, especially for nuances
- View clarity through the reader's lens, not the author's
- Code should be easy to read, not easy to write

```go
// Good: Clear purpose
func (c *Config) WriteTo(w io.Writer) (int64, error)

// Bad: Unclear, repeats receiver
func (c *Config) WriteConfigTo(w io.Writer) (int64, error)
```

### 2. Simplicity

Code should accomplish goals in the simplest way possible.

Simple code:
- Is easy to read top to bottom
- Does not assume prior knowledge
- Has no unnecessary abstraction levels
- Has comments explaining "why", not "what"
- May be mutually exclusive with "clever" code

**Least Mechanism Principle**: Prefer standard tools:
1. Core language constructs (channel, slice, map, loop, struct)
2. Standard library tools (http client, template engine)
3. Core libraries before new dependencies

### 3. Concision

Code should have high signal-to-noise ratio.

- Avoid repetitive code
- Avoid extraneous syntax
- Avoid unnecessary abstraction
- Use table-driven tests to factor out common code

```go
// Good: Common idiom, high signal
if err := doSomething(); err != nil {
    return err
}

// Good: Signal boost for unusual case
if err := doSomething(); err == nil { // if NO error
    // ...
}
```

### 4. Maintainability

Code is edited many more times than written.

Maintainable code:
- Is easy for future programmers to modify correctly
- Has APIs that grow gracefully
- Uses predictable names (same concept = same name)
- Minimizes dependencies
- Has comprehensive tests with clear diagnostics

```go
// Bad: Critical detail hidden
if user, err = db.UserByID(userID); err != nil { // = vs :=

// Good: Explicit and clear
u, err := db.UserByID(userID)
if err != nil {
    return fmt.Errorf("invalid origin user: %s", err)
}
user = u
```

### 5. Consistency

Code should look and behave like similar code in the codebase.

- Package-level consistency is most important
- When ties occur, break in favor of consistency
- Never override documented style principles for consistency

---

## Formatting

### gofmt is Required

All Go source files **must** conform to `gofmt` output. No exceptions.

```bash
# Format a file
gofmt -w myfile.go

# Format all files in directory
gofmt -w .
```

### Parentheses

> **Source**: Effective Go

Go needs fewer parentheses than C and Java. Control structures (`if`, `for`, `switch`) don't have parentheses in their syntax. The operator precedence hierarchy is shorter and clearer, so `x<<8 + y<<16` means what the spacing suggests—unlike in other languages.

### MixedCaps (Camel Case)

Go uses `MixedCaps` or `mixedCaps`, never underscores:

```go
// Good
MaxLength    // exported constant
maxLength    // unexported constant
userID       // variable

// Bad
MAX_LENGTH   // no snake_case
max_length   // no underscores
```

Exceptions:
- Test function names may use underscores: `TestFoo_Bar`
- Generated code interoperating with OS/cgo

### Line Length

There is **no rigid line length limit** in Go, but avoid uncomfortably long
lines. Uber suggests a soft limit of 99 characters.

> **Combined**: Google + Uber + Go Wiki CodeReviewComments guidance

Guidelines:
- If a line feels too long, **refactor** rather than just wrap
- Don't split before indentation changes (function declarations, conditionals)
- Don't split long strings (URLs) into multiple lines
- When splitting, put all arguments on their own lines
- If it's already as short as practical, let it remain long

**Break by semantics, not length**:

> **Advisory**: Go Wiki CodeReviewComments

Don't add line breaks just to keep lines short when they are more readable long
(e.g., repetitive lines). Break lines because of what you're writing, not
because of line length.

Long lines often correlate with long names. If you find lines are too long,
consider whether the names could be shorter. Getting rid of long names often
helps more than wrapping lines.

This advice applies equally to function length—there's no rule "never have a
function more than N lines", but there is such a thing as too long. The solution
is to change where function boundaries are, not to count lines.

```go
// Bad: Arbitrary mid-line break
func (s *Store) GetUser(ctx context.Context,
    id string) (*User, error) {

// Good: All arguments on own lines
func (s *Store) GetUser(
    ctx context.Context,
    id string,
) (*User, error) {
```

### Local Consistency

When the style guide is silent, be consistent with nearby code:

**Valid** local choices:
- `%s` vs `%v` for error formatting
- Buffered channels vs mutexes

**Invalid** local overrides:
- Line length restrictions
- Assertion-based testing libraries

---

## Reduce Nesting

> **Source**: Uber Go Style Guide

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

> **Source**: Uber Go Style Guide

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

> **Advisory**: Go Wiki CodeReviewComments

A `return` statement without arguments returns the named return values. This is
known as a "naked" return.

```go
func split(sum int) (x, y int) {
    x = sum * 4 / 9
    y = sum - x
    return  // returns x, y
}
```

### Guidelines for Naked Returns

- **OK in small functions**: Naked returns are fine in functions that are just a
  handful of lines
- **Be explicit in medium+ functions**: Once a function grows to medium size, be
  explicit with return values for clarity
- **Don't name results just for naked returns**: Clarity of documentation is
  always more important than saving a line or two. Don't name result parameters
  just because it enables naked returns

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

    return result, nil  // explicit: clearer in longer functions
}
```

See **go-documentation** for guidance on Named Result Parameters.

---

## Quick Reference

| Principle | Key Question |
|-----------|--------------|
| Clarity | Can a reader understand what and why? |
| Simplicity | Is this the simplest approach? |
| Concision | Is the signal-to-noise ratio high? |
| Maintainability | Can this be safely modified later? |
| Consistency | Does this match surrounding code? |

## See Also

- For naming conventions: `go-naming`
- For error handling patterns: `go-error-handling`
- For documentation guidelines: `go-documentation`
- For testing best practices: `go-testing`
- For defensive programming: `go-defensive`
- For performance optimization: `go-performance`
- For linting and static analysis: `go-linting`
