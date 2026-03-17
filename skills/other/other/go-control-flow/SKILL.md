---
name: go-control-flow
description: Go control flow idioms from Effective Go. Covers if with initialization, omitting else for early returns, for loop forms, range, switch without fallthrough, type switch, and blank identifier patterns. Use when writing conditionals, loops, or switch statements in Go.
---

# Go Control Flow

> **Source**: Effective Go. Go's control structures are related to C but differ
> in important ways. Understanding these differences is essential for writing
> idiomatic Go code.

Go has no `do` or `while` loop—only a generalized `for`. There are no
parentheses around conditions, and bodies must always be brace-delimited.

---

## If Statements

### Basic Form

Go's `if` requires braces and has no parentheses around the condition:

```go
if x > 0 {
    return y
}
```

### If with Initialization

`if` and `switch` accept an optional initialization statement. This is common
for scoping variables to the conditional block:

```go
// Good: err scoped to if block
if err := file.Chmod(0664); err != nil {
    log.Print(err)
    return err
}
```

### Omit Else for Early Returns

When an `if` body ends with `break`, `continue`, `goto`, or `return`, omit the
unnecessary `else`. This keeps the success path unindented:

```go
// Good: no else, success path at left margin
f, err := os.Open(name)
if err != nil {
    return err
}
codeUsing(f)
```

```go
// Bad: else clause buries normal flow
f, err := os.Open(name)
if err != nil {
    return err
} else {
    codeUsing(f)  // unnecessarily indented
}
```

### Guard Clauses for Error Handling

Code reads well when the success path flows down the page, eliminating errors as
they arise:

```go
// Good: guard clauses eliminate errors early
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

---

## Redeclaration and Reassignment

The `:=` short declaration allows redeclaring variables in the same scope under
specific conditions:

```go
f, err := os.Open(name)  // declares f and err
// ...
d, err := f.Stat()       // declares d, reassigns err (not a new err)
```

A variable `v` may appear in a `:=` declaration even if already declared,
provided:

1. The declaration is in the **same scope** as the existing `v`
2. The value is **assignable** to `v`
3. At least **one other variable** is newly created by the declaration

This pragmatic rule makes it easy to reuse a single `err` variable through a
chain of operations.

```go
// Good: err reused across multiple calls
data, err := fetchData()
if err != nil {
    return err
}
result, err := processData(data)  // err reassigned, result declared
if err != nil {
    return err
}
```

**Warning**: If `v` is declared in an outer scope, `:=` creates a **new**
variable that shadows it:

```go
// Bad: accidental shadowing
var err error
if condition {
    x, err := someFunc()  // this err shadows the outer err!
    // outer err remains nil
}
```

---

## For Loops

Go unifies `for` and `while` into a single construct with three forms:

```go
// C-style for (only form with semicolons)
for init; condition; post { }

// While-style (condition only)
for condition { }

// Infinite loop
for { }
```

### Range Clause

Use `range` to iterate over arrays, slices, strings, maps, and channels:

```go
// Iterate with key and value
for key, value := range oldMap {
    newMap[key] = value
}

// Key/index only (drop the second variable)
for key := range m {
    if key.expired() {
        delete(m, key)
    }
}

// Value only (use blank identifier for index)
for _, value := range array {
    sum += value
}
```

### Range Over Strings

For strings, `range` iterates over UTF-8 encoded runes (not bytes), handling
multi-byte characters automatically.

### Parallel Assignment in For

Go has no comma operator. Use parallel assignment for multiple loop variables:

```go
// Reverse a slice
for i, j := 0, len(a)-1; i < j; i, j = i+1, j-1 {
    a[i], a[j] = a[j], a[i]
}
```

Note: `++` and `--` are statements, not expressions, so they cannot be used in
parallel assignment.

---

## Switch

Go's `switch` is more flexible than C's:

- Expressions need not be constants or integers
- Cases are evaluated top to bottom until a match
- **No automatic fall through** (no need for `break` in each case)

### Expression-less Switch

If the `switch` has no expression, it switches on `true`. This is idiomatic for
writing clean `if-else-if` chains:

```go
// Good: expression-less switch for ranges
func unhex(c byte) byte {
    switch {
    case '0' <= c && c <= '9':
        return c - '0'
    case 'a' <= c && c <= 'f':
        return c - 'a' + 10
    case 'A' <= c && c <= 'F':
        return c - 'A' + 10
    }
    return 0
}
```

### Comma-Separated Cases

Multiple cases can be combined with commas (no fall through needed):

```go
func shouldEscape(c byte) bool {
    switch c {
    case ' ', '?', '&', '=', '#', '+', '%':
        return true
    }
    return false
}
```

### Break with Labels

`break` terminates the switch by default. To break out of an enclosing loop, use
a label:

```go
Loop:
    for n := 0; n < len(src); n += size {
        switch {
        case src[n] < sizeOne:
            break        // breaks switch only
        case src[n] < sizeTwo:
            if n+1 >= len(src) {
                break Loop   // breaks out of for loop
            }
        }
    }
```

---

## Type Switch

A type switch discovers the dynamic type of an interface value using
`.(type)`:

```go
switch v := value.(type) {
case nil:
    fmt.Println("value is nil")
case int:
    fmt.Printf("integer: %d\n", v)      // v is int
case string:
    fmt.Printf("string: %q\n", v)       // v is string
case bool:
    fmt.Printf("boolean: %t\n", v)      // v is bool
default:
    fmt.Printf("unexpected type %T\n", v)
}
```

It's idiomatic to reuse the variable name (`v := value.(type)`) since the
variable has a different type in each case clause.

When a case lists multiple types (`case int, int64:`), the variable has the
interface type.

---

## The Blank Identifier

The blank identifier `_` discards values. It's like writing to `/dev/null`.

### Multiple Assignment

Discard unwanted values from multi-value expressions:

```go
// Only need the error
if _, err := os.Stat(path); os.IsNotExist(err) {
    fmt.Printf("%s does not exist\n", path)
}

// Only need the value (discard ok)
value := cache[key]  // simpler: just use single-value form
_, present := cache[key]  // when you only need presence check
```

**Never discard errors carelessly**:

```go
// Bad: ignoring error will crash if path doesn't exist
fi, _ := os.Stat(path)
if fi.IsDir() {  // nil pointer dereference if path doesn't exist
    // ...
}
```

### Unused Imports and Variables During Development

Silence compiler errors temporarily during active development:

```go
import (
    "fmt"
    "io"
)

var _ = fmt.Printf  // silence unused import (remove before committing)
var _ io.Reader

func main() {
    fd, _ := os.Open("test.go")
    _ = fd  // silence unused variable
}
```

### Import for Side Effect

Import a package only for its `init()` side effects:

```go
import _ "net/http/pprof"  // registers HTTP handlers
import _ "image/png"       // registers PNG decoder
```

This makes clear the package is imported only for side effects—it has no usable
name in this file.

### Interface Compliance Check

Verify at compile time that a type implements an interface:

```go
// Verify that *MyType implements io.Writer
var _ io.Writer = (*MyType)(nil)

// Verify that MyHandler implements http.Handler
var _ http.Handler = MyHandler{}
```

This fails at compile time if the type doesn't implement the interface, catching
errors early.

---

## Quick Reference

| Pattern | Go Idiom |
|---------|----------|
| If initialization | `if err := f(); err != nil { }` |
| Early return | Omit `else` when if body returns |
| Redeclaration | `:=` reassigns if same scope + new var |
| C-style for | `for i := 0; i < n; i++ { }` |
| While-style | `for condition { }` |
| Infinite loop | `for { }` |
| Range with key+value | `for k, v := range m { }` |
| Range value only | `for _, v := range slice { }` |
| Range key only | `for k := range m { }` |
| Parallel assignment | `i, j = i+1, j-1` |
| Expression-less switch | `switch { case cond: }` |
| Comma cases | `case 'a', 'b', 'c':` |
| No fallthrough | Default behavior (explicit `fallthrough` if needed) |
| Break from loop in switch | `break Label` |
| Type switch | `switch v := x.(type) { }` |
| Discard value | `_, err := f()` |
| Side-effect import | `import _ "pkg"` |
| Interface check | `var _ Interface = (*Type)(nil)` |

---

## See Also

- **go-style-core**: Core Go style principles and formatting
- **go-error-handling**: Error handling patterns including guard clauses
- **go-naming**: Naming conventions for loop variables and labels
- **go-concurrency**: Goroutines, channels, and select statements
- **go-defensive**: Defensive programming patterns
