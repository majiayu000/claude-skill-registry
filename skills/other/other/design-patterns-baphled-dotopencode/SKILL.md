---
name: design-patterns
description: Recognise and apply design patterns appropriately
category: Code Quality
---

# Skill: design-patterns

## What I do

I teach design patterns: recognising situations where patterns apply, knowing why each pattern solves a specific problem, and applying them without over-engineering. Patterns should emerge naturally, not be forced.

## When to use me

- Refactoring code and recognising opportunities for patterns
- Reviewing code to spot missing structure
- Designing new components or systems
- Teaching junior engineers why patterns matter
- Choosing between multiple design approaches

## Core principles

1. **Pattern solves a problem** - Never apply pattern "just because"
2. **Name the problem first** - Understand what you're solving before choosing pattern
3. **Simplest pattern wins** - Don't reach for complex patterns when simple works
4. **Language matters** - Some patterns are idiomatic in some languages, not others
5. **Patterns evolve** - Modern Go patterns differ from classic Gang of Four

## Patterns & examples

**Common patterns and when to use them:**

| Pattern | Problem | Example |
|---------|---------|---------|
| Factory | Creating complex objects | Database connection pooling |
| Strategy | Different algorithms for same task | Multiple sorting strategies |
| Observer | Decoupling event producers from consumers | Event handlers, webhooks |
| Adapter | Using incompatible interfaces together | Wrapping third-party libraries |
| Decorator | Adding behaviour without modifying original | Middleware, logging wrappers |

**Pattern recognition example:**

Problem: "I have multiple types of notifications (email, SMS, Slack) and need to send them"

❌ Wrong approach: Write if/else for each type
✅ Right approach: Strategy pattern

```go
// ✅ Correct: Strategy pattern
type NotificationStrategy interface {
  Send(message string) error
}

type EmailNotifier struct{ ... }
func (e *EmailNotifier) Send(msg string) error { ... }

type SlackNotifier struct{ ... }
func (s *SlackNotifier) Send(msg string) error { ... }

// Consumer doesn't care which strategy
func SendAlert(n NotificationStrategy, msg string) error {
  return n.Send(msg)
}
```

**Language-specific patterns:**

Go: Composition over inheritance, interface-driven design, table-driven tests
Ruby: Metaprogramming, DSLs, ActiveRecord patterns
JavaScript: Closures, promises/async-await, dependency injection

## Anti-patterns to avoid

- ❌ Applying pattern before understanding the problem
- ❌ Using complex patterns when simple code suffices
- ❌ Forcing patterns across language boundaries (don't use Java patterns in Go)
- ❌ Treating patterns as dogma instead of guidelines
- ❌ Over-engineering for "future flexibility"

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Code-Quality/Design Patterns.md`

## Related skills

- `clean-code` - Apply patterns to improve readability
- `refactor` - Recognise when patterns would help
- `architecture` - Patterns as building blocks for larger systems
- `modular-design` - Patterns that enable testability (Strategy, DI, Adapter as seams)
