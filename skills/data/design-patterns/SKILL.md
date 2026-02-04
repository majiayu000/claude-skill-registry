---
name: golang-design-patterns
description: Go design patterns and refactoring skill. Use when refactoring complex code, reducing technical debt, or applying design patterns. Detects code smells and suggests pattern-based solutions.
license: MIT
metadata:
  author: saifoelloh
  version: "2.0.0"
  parent_skill: golang-best-practices
  sources:
    - "Refactoring (Martin Fowler)"
    - "Design Patterns (Gang of Four)"
    - "Refactoring.Guru"
  last_updated: "2026-01-22"
---

# Golang Design Patterns & Refactoring

Expert-level code refactoring and design pattern application for Go. Detects code smells, suggests refactoring strategies, and applies proven design patterns to improve maintainability.

## When to Apply

Use this skill when:
- Refactoring complex or legacy code
- Reducing technical debt
- Extracting reusable patterns
- Simplifying large functions (God Objects)
- Improving code maintainability
- Applying Gang of Four patterns to Go

## Rule Categories by Priority

| Priority | Count | Focus |
|----------|-------|-------|
| High | 2 | Critical refactoring needs |
| Medium | 11 | Code quality improvements |

## Rules Covered (13 total)

### High-Impact Patterns (2)

- `high-god-object` - Extract logic from 300+ line functions
- `high-extract-method` - Name complex code blocks with descriptive methods

### Medium Improvements (11)

- `medium-primitive-obsession` - Replace primitives with value objects
- `medium-long-parameter-list` - Use parameter objects for >5 params
- `medium-data-clumps` - Extract repeated parameter groups
- `medium-feature-envy` - Move logic closer to data
- `medium-magic-constants` - Replace magic numbers with named constants
- `medium-builder-pattern` - Fluent API for complex construction
- `medium-factory-constructor` - Validated object creation
- `medium-introduce-parameter-object` - Group related parameters
- `medium-switch-to-strategy` - Replace type switches with interfaces
- `medium-middleware-decorator` - Decorator pattern for http.Handler
- `medium-law-of-demeter` - Reduce coupling, avoid message chains

## Common Refactoring Patterns

### God Object → Extracted Methods
```go
// ❌ 500 line function
func (u *Usecase) Process() { ... }

// ✅ Extracted methods
func (u *Usecase) Process() {
    u.validate()
    u.transform()
    u.persist()
}
```

### Primitive Obsession → Value Object
```go
// ❌ Primitive types
func CreateUser(email string) { ... }

// ✅ Value object
type Email struct { value string }
func CreateUser(email Email) { ... }
```

### Type Switch → Strategy Pattern
```go
// ❌ Type switch
switch v := val.(type) { ... }

// ✅ Strategy pattern
type Processor interface { Process() }
```

## Trigger Phrases

This skill activates when you say:
- "Refactor this code"
- "Reduce complexity"
- "Extract methods from large function"
- "Apply design patterns"
- "Improve maintainability"
- "Simplify this usecase"
- "Find code smells"

## How to Use

### For Code Refactoring

1. Identify code smells (God Objects, long parameter lists, etc.)
2. Apply appropriate refactoring pattern
3. Verify tests still pass
4. Check for improved readability

### For Pattern Application

1. Identify appropriate pattern for use case
2. Apply pattern incrementally
3. Ensure pattern improves, not complicates code

## Output Format

```
## High Priority Refactoring: X

### [Rule Name] (Line Y)
**Code Smell**: God Object / Long Parameter List / Primitive Obsession
**Impact**: Hard to maintain / Test / Understand
**Refactoring**: Extract Method / Introduce Parameter Object / Create Value Object
**Example**:
```go
// Refactored code
```

## Related Skills

- [golang-clean-architecture](../clean-architecture/SKILL.md) - For usecase complexity patterns
- [golang-idiomatic-go](../idiomatic-go/SKILL.md) - For interface design

## Philosophy

Based on Martin Fowler's Refactoring:

- **Code smells indicate problems** - Detect and address systematically
- **Refactor incrementally** - Small, safe steps
- **Patterns are solutions** - Apply when appropriate, not dogmatically
- **Maintainability matters** - Code is read more than written

## Notes

- Focus on common Go refactoring patterns
- All patterns adapted for Go idioms
- Emphasizes readability and maintainability
- Includes Gang of Four patterns applicable to Go
