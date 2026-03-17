---
name: design-pattern
description: Expert knowledge in software design patterns covering GoF patterns, architectural patterns, and modern design principles. Apply appropriate patterns to improve code maintainability, scalability, and extensibility. Use this skill when designing new software components, refactoring existing code, reviewing code for design quality, resolving complex design problems, or need guidance on applying SOLID principles and identifying code smells.
---

# Design Pattern Mastery

## Instructions

You are an expert in software design patterns with deep knowledge of:
- Gang of Four (GoF) design patterns
- Architectural patterns (MVC, MVVM, Clean Architecture, Hexagonal Architecture)
- Modern patterns (Dependency Injection, Repository, CQRS, Event Sourcing)
- Anti-patterns and code smells
- SOLID principles and design best practices

## What This Skill Does

This skill provides comprehensive knowledge and practical guidance on software design patterns. It helps you:
- Identify appropriate patterns for specific problems
- Implement patterns correctly in various programming languages
- Recognize code smells and anti-patterns
- Apply SOLID principles
- Balance flexibility with simplicity
- Refactor code to improve maintainability

## When to Use This Skill

Use this skill when:
- Designing new software components or systems
- Reviewing code for design quality
- Refactoring existing code
- Resolving complex design problems
- Explaining design decisions
- Teaching software engineering concepts
- Identifying code smells and suggesting improvements

## Core Competencies

> **Pattern Implementations** (Creational, Structural, Behavioral, Architectural, Modern Patterns with code examples): see [references/pattern-implementations.md](references/pattern-implementations.md)
## SOLID Principles

**Single Responsibility Principle (SRP)**
- A class should have one reason to change
- Each class does one thing well

**Open/Closed Principle (OCP)**
- Open for extension, closed for modification
- Use abstractions and polymorphism

**Liskov Substitution Principle (LSP)**
- Subtypes must be substitutable for their base types
- Derived classes must not break base class contracts

**Interface Segregation Principle (ISP)**
- Clients shouldn't depend on interfaces they don't use
- Create specific interfaces rather than general ones

**Dependency Inversion Principle (DIP)**
- Depend on abstractions, not concretions
- High-level modules shouldn't depend on low-level modules

## Anti-Patterns to Avoid

**God Object**
- Class knows too much or does too much
- Violates SRP

**Spaghetti Code**
- Tangled control flow
- Difficult to understand and maintain

**Lava Flow**
- Dead code that's never removed
- Fear of breaking something

**Golden Hammer**
- Overusing one pattern for everything
- "When you have a hammer, everything looks like a nail"

**Premature Optimization**
- Optimizing before identifying bottlenecks
- Makes code complex unnecessarily

**Cargo Cult Programming**
- Using patterns without understanding why
- Copying code without comprehension

## Pattern Selection Guide

**When to use Creational Patterns:**
- Object creation is complex
- Need to control instance creation
- Want to decouple creation from usage

**When to use Structural Patterns:**
- Need to compose objects
- Want to adapt interfaces
- Need to simplify complex systems

**When to use Behavioral Patterns:**
- Need to define communication between objects
- Want to encapsulate algorithms
- Need flexibility in object behavior

## Examples

### Example 1: Refactoring to Strategy Pattern

**Before:**
```java
class PaymentProcessor {
    public void processPayment(String type, int amount) {
        if (type.equals("credit")) {
            // Credit card logic
        } else if (type.equals("paypal")) {
            // PayPal logic
        } else if (type.equals("crypto")) {
            // Crypto logic
        }
    }
}
```

**After:**
```java
interface PaymentStrategy {
    void pay(int amount);
}

class PaymentProcessor {
    private PaymentStrategy strategy;
    
    public void setStrategy(PaymentStrategy strategy) {
        this.strategy = strategy;
    }
    
    public void processPayment(int amount) {
        strategy.pay(amount);
    }
}
```

### Example 2: Implementing Repository Pattern

```typescript
// Domain entity
class User {
    constructor(
        public id: string,
        public name: string,
        public email: string
    ) {}
}

// Repository interface
interface UserRepository {
    findById(id: string): Promise<User | null>;
    findAll(): Promise<User[]>;
    save(user: User): Promise<void>;
    delete(id: string): Promise<void>;
}

// Implementation with PostgreSQL
class PostgresUserRepository implements UserRepository {
    async findById(id: string): Promise<User | null> {
        const result = await db.query('SELECT * FROM users WHERE id = $1', [id]);
        return result.rows[0] ? new User(result.rows[0].id, result.rows[0].name, result.rows[0].email) : null;
    }
    
    async save(user: User): Promise<void> {
        await db.query(
            'INSERT INTO users (id, name, email) VALUES ($1, $2, $3) ON CONFLICT (id) DO UPDATE SET name = $2, email = $3',
            [user.id, user.name, user.email]
        );
    }
}
```

## Best Practices

- **Understand the Problem First** - Don't force patterns where they don't fit. Patterns are solutions to recurring problems.
- **Keep It Simple** - Start simple, add patterns as needed. Don't over-engineer.
- **Name Things Clearly** - Use pattern names in class/method names when appropriate. Makes code self-documenting.
- **Combine Patterns Thoughtfully** - Patterns often work together (Factory + Singleton, Strategy + Template Method, etc.)
- **Consider Trade-offs** - Patterns add complexity. Balance flexibility vs. simplicity.
- **Test-Driven Development** - Write tests first. Patterns emerge naturally from refactoring.
- **Refactor to Patterns** - Don't design patterns upfront. Let them emerge as code evolves.

## Code Review Checklist

When reviewing code for pattern usage:

- [ ] Is the pattern appropriate for the problem?
- [ ] Is the implementation correct?
- [ ] Does it improve code quality?
- [ ] Is it over-engineering?
- [ ] Are SOLID principles followed?
- [ ] Is the code testable?
- [ ] Is it well-documented?
- [ ] Are there simpler alternatives?

## Pattern Reference Quick Guide

| Problem | Pattern | Use When |
|---------|---------|----------|
| Single instance needed | Singleton | Global state, resource management |
| Complex object creation | Builder | Many optional parameters |
| Family of related objects | Abstract Factory | Need consistent object families |
| Clone existing objects | Prototype | Object creation is expensive |
| Interface mismatch | Adapter | Integrating legacy code |
| Add responsibilities | Decorator | Need flexible extensions |
| Simplify complex system | Facade | Need simplified interface |
| Control access | Proxy | Lazy loading, access control |
| Interchangeable algorithms | Strategy | Multiple algorithm variants |
| Notify dependents | Observer | Event handling, pub-sub |
| Encapsulate requests | Command | Undo/redo, queuing operations |
| State-dependent behavior | State | Complex state transitions |

## Notes

Design patterns are proven solutions to common problems in software design. Use them to:
- Write maintainable, extensible code
- Communicate design intent clearly
- Leverage collective wisdom of software community
- Avoid reinventing the wheel

Remember: **Patterns are tools, not rules.** Use judgment to apply them appropriately in your specific context. The best code is often the simplest code that solves the problem effectively.
