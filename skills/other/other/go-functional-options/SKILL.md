---
name: go-functional-options
description: Use when designing a Go constructor or factory function with optional configuration — especially with 3+ optional parameters or extensible APIs. Also use when building a New* function that takes many settings, even if they don't mention "functional options" by name. Does not cover general function design (see go-functions).
license: Apache-2.0
metadata:
  sources: "Uber Style Guide"
---

# Functional Options Pattern

Functional options is a pattern where you declare an opaque `Option` type that records information in an internal struct. The constructor accepts a variadic number of these options and applies them to configure the result.

## When to Use

Use functional options when:

- **3+ optional arguments** on constructors or public APIs
- **Extensible APIs** that may gain new options over time
- **Clean caller experience** is important (no need to pass defaults)

## The Pattern

### Core Components

1. **Unexported `options` struct** - holds all configuration
2. **Exported `Option` interface** - with unexported `apply` method
3. **Option types** - implement the interface
4. **`With*` constructors** - create options

### Option Interface

```go
type Option interface {
    apply(*options)
}
```

The unexported `apply` method ensures only options from this package can be used.

## Complete Implementation

```go
package db

import "go.uber.org/zap"

// options holds all configuration for opening a connection.
type options struct {
    cache  bool
    logger *zap.Logger
}

// Option configures how we open the connection.
type Option interface {
    apply(*options)
}

// cacheOption implements Option for cache setting (simple type alias).
type cacheOption bool

func (c cacheOption) apply(opts *options) {
    opts.cache = bool(c)
}

// WithCache enables or disables caching.
func WithCache(c bool) Option {
    return cacheOption(c)
}

// loggerOption implements Option for logger setting (struct for pointers).
type loggerOption struct {
    Log *zap.Logger
}

func (l loggerOption) apply(opts *options) {
    opts.logger = l.Log
}

// WithLogger sets the logger for the connection.
func WithLogger(log *zap.Logger) Option {
    return loggerOption{Log: log}
}

// Open creates a connection.
func Open(addr string, opts ...Option) (*Connection, error) {
    // Start with defaults
    options := options{
        cache:  defaultCache,
        logger: zap.NewNop(),
    }

    // Apply all provided options
    for _, o := range opts {
        o.apply(&options)
    }

    // Use options.cache and options.logger...
    return &Connection{}, nil
}
```

## Usage Examples

### Without Functional Options (Bad)

```go
// Caller must always provide all parameters, even defaults
db.Open(addr, db.DefaultCache, zap.NewNop())
db.Open(addr, db.DefaultCache, log)
db.Open(addr, false /* cache */, zap.NewNop())
db.Open(addr, false /* cache */, log)
```

### With Functional Options (Good)

```go
// Only provide options when needed
db.Open(addr)
db.Open(addr, db.WithLogger(log))
db.Open(addr, db.WithCache(false))
db.Open(
    addr,
    db.WithCache(false),
    db.WithLogger(log),
)
```

## Comparison: Functional Options vs Config Struct

| Aspect | Functional Options | Config Struct |
|--------|-------------------|---------------|
| **Extensibility** | Add new `With*` functions | Add new fields (may break) |
| **Defaults** | Built into constructor | Zero values or separate defaults |
| **Caller experience** | Only specify what differs | Must construct entire struct |
| **Testability** | Options are comparable | Struct comparison |
| **Complexity** | More boilerplate | Simpler setup |

**Prefer Config Struct when**: Fewer than 3 options, options rarely change, all options usually specified together, or internal APIs only.

> Read [references/OPTIONS-VS-STRUCTS.md](references/OPTIONS-VS-STRUCTS.md) when deciding between functional options and config structs, designing a config struct API with proper defaults, or evaluating the hybrid approach for complex constructors.

## Why Not Closures?

An alternative implementation uses closures:

```go
// Closure approach (not recommended)
type Option func(*options)

func WithCache(c bool) Option {
    return func(o *options) { o.cache = c }
}
```

The interface approach is preferred because:

1. **Testability** - Options can be compared in tests and mocks
2. **Debuggability** - Options can implement `fmt.Stringer`
3. **Flexibility** - Options can implement additional interfaces
4. **Visibility** - Option types are visible in documentation

## Quick Reference

```go
// 1. Unexported options struct with defaults
type options struct {
    field1 Type1
    field2 Type2
}

// 2. Exported Option interface, unexported method
type Option interface {
    apply(*options)
}

// 3. Option type + apply + With* constructor
type field1Option Type1

func (o field1Option) apply(opts *options) { opts.field1 = Type1(o) }
func WithField1(v Type1) Option            { return field1Option(v) }

// 4. Constructor applies options over defaults
func New(required string, opts ...Option) (*Thing, error) {
    o := options{field1: defaultField1, field2: defaultField2}
    for _, opt := range opts {
        opt.apply(&o)
    }
    // ...
}
```

### Checklist

- [ ] `options` struct is unexported
- [ ] `Option` interface has unexported `apply` method
- [ ] Each option has a `With*` constructor
- [ ] Defaults are set before applying options
- [ ] Required parameters are separate from `...Option`

## Related Skills

- **Interface design**: See [go-interfaces](../go-interfaces/SKILL.md) when designing the `Option` interface or choosing between interface and closure approaches
- **Naming conventions**: See [go-naming](../go-naming/SKILL.md) when naming `With*` constructors, option types, or the unexported options struct
- **Function design**: See [go-functions](../go-functions/SKILL.md) when organizing constructors within a file or formatting variadic signatures
- **Documentation**: See [go-documentation](../go-documentation/SKILL.md) when documenting `Option` types, `With*` functions, or constructor behavior

### External Resources

- [Self-referential functions and the design of options](https://commandcenter.blogspot.com/2014/01/self-referential-functions-and-design.html) - Rob Pike
- [Functional options for friendly APIs](https://dave.cheney.net/2014/10/17/functional-options-for-friendly-apis) - Dave Cheney
