---
name: go
description: Go (Golang) with goroutines, channels, interfaces, and idiomatic patterns. Use for .go files.
---

# Go

A simple, fast, and concurrent language developed by Google.

## When to Use

- Microservices / Cloud-native apps
- Network tools (servers, proxies)
- High-performance systems
- CLIs

## Quick Start

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")

    ch := make(chan string)
    go func() {
        ch <- "from goroutine"
    }()

    msg := <-ch
    fmt.Println(msg)
}
```

## Core Concepts

### Goroutines

Lightweight threads managed by the Go runtime.

```go
go doSomething()
```

### Channels

Typed conduits for communication between goroutines.

### Interfaces

Implicitly implemented. If a struct has the methods, it implements the interface.

## Best Practices

**Do**:

- Handle errors explicitly (check `if err != nil`)
- Use `gofmt` to format code
- Keep extensive comments for public APIs
- Use context for cancellation and timeouts

**Don't**:

- Ignore errors (using `_`) blindly
- Use panic/recover for normal error handling
- Create large interfaces (keep them small)

## References

- [Go Documentation](https://go.dev/doc/)
- [Effective Go](https://go.dev/doc/effective_go)
