---
name: applying-effective-go
description: "Apply Go best practices, idioms, and conventions from golang.org/doc/effective_go. Use when writing, reviewing, or refactoring Go code to ensure idiomatic, clean, and efficient implementations."
---

# Applying Effective Go

Apply best practices and conventions from the official [Effective Go guide](https://go.dev/doc/effective_go) to write clean, idiomatic Go code.

## When to Apply

Use this skill automatically when:
- Writing new Go code
- Reviewing Go code
- Refactoring existing Go implementations

## Key Reminders

Follow the conventions and patterns documented at https://go.dev/doc/effective_go, with particular attention to:

- **Formatting**: Always use `gofmt` - this is non-negotiable
- **Naming**: No underscores, use MixedCaps for exported names, mixedCaps for unexported
- **Error handling**: Always check errors; return them, don't panic
- **Concurrency**: Share memory by communicating (use channels)
- **Interfaces**: Keep small (1-3 methods ideal); accept interfaces, return concrete types
- **Documentation**: Document all exported symbols, starting with the symbol name

## References

- Official Guide: https://go.dev/doc/effective_go
- Code Review Comments: https://github.com/golang/go/wiki/CodeReviewComments
- Standard Library: Use as reference for idiomatic patterns
