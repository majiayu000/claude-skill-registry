---
name: go-interfaces
description: Use when defining or implementing Go interfaces, designing abstractions, creating mockable boundaries for testing, or composing types through embedding. Also use when deciding whether to accept an interface or return a concrete type, or using type assertions or type switches, even if the user doesn't explicitly mention interfaces. Does not cover generics-based polymorphism (see go-generics).
license: Apache-2.0
metadata:
  sources: "Effective Go, Google Style Guide, Uber Style Guide"
allowed-tools: Bash(bash:*)
---

# Go Interfaces and Composition

## Available Scripts

- **`scripts/check-interface-compliance.sh`** — Finds exported interfaces missing compile-time compliance checks (`var _ I = (*T)(nil)`). Run `bash scripts/check-interface-compliance.sh --help` for options.

---

## Accept Interfaces, Return Concrete Types

Interfaces belong in the package that **consumes** values, not the package that
**implements** them. Return concrete (usually pointer or struct) types from
constructors so new methods can be added without refactoring.

```go
// Good: consumer defines the interface it needs
package consumer

type Thinger interface { Thing() bool }

func Foo(t Thinger) string { ... }
```

```go
// Good: producer returns concrete type
package producer

type Thinger struct{ ... }
func (t Thinger) Thing() bool { ... }
func NewThinger() Thinger { return Thinger{ ... } }
```

```go
// Bad: producer defines and returns its own interface
package producer

type Thinger interface { Thing() bool }
type defaultThinger struct{ ... }
func NewThinger() Thinger { return defaultThinger{ ... } }
```

**Do not define interfaces before they are used.** Without a realistic example
of usage, it is too difficult to see whether an interface is even necessary.

---

## Generality: Hide Implementation, Expose Interface

If a type exists only to implement an interface with no exported methods beyond
that interface, return the interface from constructors to hide the implementation:

```go
func NewHash() hash.Hash32 {
    return &myHash{}  // unexported type
}
```

Benefits: implementation can change without affecting callers, substituting
algorithms requires only changing the constructor call.

---

## Type Assertions: Comma-Ok Idiom

Without checking, a failed assertion causes a runtime panic. Always use the
comma-ok idiom to test safely:

```go
str, ok := value.(string)
if ok {
    fmt.Printf("string value is: %q\n", str)
}
```

To check if a value implements an interface:

```go
if _, ok := val.(json.Marshaler); ok {
    fmt.Printf("value %v implements json.Marshaler\n", val)
}
```

---

## Type Switch

It's idiomatic to reuse the variable name (`t := t.(type)`) — the variable has
the correct type in each case branch. When a case lists multiple types
(`case int, int64:`), the variable has the interface type.

---

## Embedding

Avoid embedding types in public structs — the inner type's full method set
becomes part of your public API. Use unexported fields instead.

> Read [references/EMBEDDING.md](references/EMBEDDING.md) when using struct embedding for composition, overriding embedded methods, resolving name conflicts, applying the HandlerFunc adapter pattern, or deciding whether to embed in public API types.

---

## Interface Satisfaction Checks

Use a blank identifier assignment to verify a type implements an interface at
compile time:

```go
var _ json.Marshaler = (*RawMessage)(nil)
```

This causes a compile error if `*RawMessage` doesn't implement `json.Marshaler`.

Use this pattern when:
- There are no static conversions that would verify the interface automatically
- The type must satisfy an interface for correct behavior (e.g., custom JSON
  marshaling)
- Interface changes should break compilation, not silently degrade

**Don't** add these checks for every interface — only when no other static
conversion would catch the error.

> **Validation**: After defining interfaces or implementations, run `bash scripts/check-interface-compliance.sh` to verify all concrete types have compile-time `var _ I = (*T)(nil)` checks.

---

## Receiver Type

If in doubt, use a pointer receiver. Don't mix receiver types on a single
type — if any method needs a pointer, use pointers for all methods. Use value
receivers only for small, immutable types (`Point`, `time.Time`) or basic types.

> Read [references/RECEIVER-TYPE.md](references/RECEIVER-TYPE.md) when deciding between pointer and value receivers for a new type, especially for types with sync primitives or large structs.

---

## Quick Reference

| Concept | Pattern | Notes |
|---------|---------|-------|
| Consumer owns interface | Define interfaces where used | Not in the implementing package |
| Safe type assertion | `v, ok := x.(Type)` | Returns zero value + false |
| Type switch | `switch v := x.(type)` | Variable has correct type per case |
| Interface embedding | `type RW interface { Reader; Writer }` | Union of methods |
| Struct embedding | `type S struct { *T }` | Promotes T's methods |
| Interface check | `var _ I = (*T)(nil)` | Compile-time verification |
| Generality | Return interface from constructor | Hide implementation |

---

## Related Skills

- **Interface naming**: See [go-naming](../go-naming/SKILL.md) when naming interfaces (the `-er` suffix convention) or choosing receiver names
- **Error types**: See [go-error-handling](../go-error-handling/SKILL.md) when implementing the `error` interface, custom error types, or `errors.As` matching
- **Generics vs interfaces**: See [go-generics](../go-generics/SKILL.md) when deciding whether generics are needed or an interface already suffices
- **Functional options**: See [go-functional-options](../go-functional-options/SKILL.md) when using an interface-based Option pattern for flexible constructors
- **Compile-time checks**: See [go-defensive](../go-defensive/SKILL.md) when adding `var _ I = (*T)(nil)` satisfaction checks at API boundaries
