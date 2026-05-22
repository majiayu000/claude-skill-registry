---
name: golang-idiomatic-go
description: Idiomatic Go patterns review. Use when checking Go-specific idioms, interface design, or pointer usage. Ensures code follows Go conventions and best practices.
license: MIT
metadata:
  author: saifoelloh
  version: "2.0.0"
  parent_skill: golang-best-practices
  sources:
    - "Learning Go: An Idiomatic Approach (Jon Bodner)"
    - "Effective Go"
  last_updated: "2026-01-22"
---

# Golang Idiomatic Patterns

Expert-level review for idiomatic Go patterns. Ensures code follows Go conventions, proper interface design, and appropriate pointer usage.

## When to Apply

Use this skill when:
- Ensuring code follows Go idioms
- Reviewing interface design patterns
- Checking pointer vs value usage
- Verifying "Accept interfaces, return structs" pattern
- Auditing usecase complexity
- Ensuring small, focused interfaces

## Rule Categories by Priority

| Priority | Count | Focus |
|----------|-------|-------|
| High | 1 | Method receivers |
| Medium | 5 | Go idioms and patterns |

## Rules Covered (6 total)

### High-Impact Patterns (1)

- `high-pointer-receiver` - Use pointer receivers for mutations

### Medium Improvements (5)

- `medium-interface-pollution` - Keep interfaces small (<5 methods)
- `medium-accept-interface-return-struct` - API flexibility pattern
- `medium-pointer-overuse` - Don't overuse pointers for small types
- `medium-usecase-complexity` - Move business logic to domain entities
- `medium-interface-in-implementation` - Define interfaces where used

## Common Idiomatic Patterns

### Accept Interfaces, Return Structs
```go
// ✅ GOOD: Accept interface, return struct
func Process(r io.Reader) (*Result, error) {
    // ...
    return &Result{}, nil
}
```

### Small Interfaces
```go
// ✅ GOOD: Small, focused interface
type Reader interface {
    Read(p []byte) (n int, err error)
}
```

### Pointer Receivers for Mutations
```go
// ✅ GOOD: Pointer receiver modifies state
func (u *User) UpdateEmail(email string) {
    u.Email = email
}
```

## Trigger Phrases

This skill activates when you say:
- "Is this idiomatic Go?"
- "Review Go style"
- "Check interface design"
- "Verify pointer usage"
- "Review Go conventions"
- "Check for Go anti-patterns"

## How to Use

### For Idiomatic Review

1. Check method receivers (pointer vs value)
2. Verify interface sizes and locations
3. Review pointer usage appropriateness
4. Check "accept interfaces, return structs" pattern

## Output Format

```
## Idiomatic Go Improvements: X

### [Rule Name] (Line Y)
**Pattern**: Interface Design / Pointer Usage / Method Receiver
**Issue**: Violates Go idiom
**Fix**: Suggested correction
**Example**:
```go
// Idiomatic Go code
```

## Related Skills

- [golang-clean-architecture](../clean-architecture/SKILL.md) - For interface segregation
- [golang-design-patterns](../design-patterns/SKILL.md) - For usecase complexity

## Philosophy

Based on "Learning Go" and Effective Go:

- **Simplicity over cleverness** - Boring code is good code
- **Interfaces are satisfied implicitly** - Define where used
- **Composition over inheritance** - Embed types, don't extend
- **Clear is better than clever** - Readability wins

## Notes

- Focus on Go-specific patterns
- Not general programming practices
- Emphasizes Go conventions and idioms
- Based on Effective Go and community standards
