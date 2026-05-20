---
name: design-patterns
version: 1.0.0
description: "Guidance on when and how to apply design patterns. Use when: (1) asking which pattern to use, (2) refactoring code, (3) discussing code smells, (4) need to decouple components, (5) building extensible systems."
license: MIT
model: claude-opus-4-5-20251101
metadata:
  domains: [design-patterns, architecture, refactoring, oop]
  source: https://refactoring.guru/design-patterns/catalog
  language: typescript
---

# Design Patterns

Expert guidance on applying Gang of Four design patterns to solve common software design problems. This skill helps you identify code smells, match them to appropriate patterns, and implement solutions effectively.

## Triggers

- `which pattern should I use` - Pattern selection guidance
- `refactor this code` - Identify and apply patterns to improve existing code
- `how to decouple` - Find patterns to reduce coupling
- `design pattern for` - Specific pattern recommendations
- `code smells` - Identify problems that patterns can solve

## Quick Reference

| Input | Output | Duration |
|-------|--------|----------|
| Code problem/smell | Pattern recommendation + implementation guide | 2-5 min |
| Existing code | Refactoring plan with pattern | 5-10 min |
| Pattern name | Implementation example + guidance | 1-2 min |

## Agent Behavior Contract

1. **Analyze first** - Always examine existing code before recommending patterns
2. **Identify the problem** - Clearly state the code smell or design issue
3. **Don't over-engineer** - Apply patterns only when they solve real problems
4. **Explain trade-offs** - Discuss pros and cons of each pattern
5. **Prefer simplicity** - If a simpler solution exists, recommend it
6. **Show examples** - Provide TypeScript code examples
7. **Consider alternatives** - Mention related or alternative patterns

## Pattern Selection Decision Tree

### Object Creation Problems?

```
├─ Need to create objects without specifying concrete classes?
│  └─→ Factory Method
│
├─ Need families of related objects to work together?
│  └─→ Abstract Factory
│
├─ Complex object with many optional parameters?
│  └─→ Builder
│
└─ Need exactly one instance with global access?
   └─→ Singleton (⚠️ use sparingly)
```

### Behavior/Algorithm Problems?

```
├─ Need to swap algorithms at runtime?
│  └─→ Strategy
│
├─ Behavior changes based on internal state?
│  └─→ State
│
├─ Need to notify multiple objects of changes?
│  └─→ Observer
│
├─ Want to queue, log, or undo operations?
│  └─→ Command
│
├─ Need to save/restore object state (undo/redo, snapshots)?
│  └─→ Memento
│
└─ Define algorithm skeleton, let subclasses override steps?
   └─→ Template Method
```

### Structure/Interface Problems?

```
├─ Incompatible interfaces need to work together?
│  └─→ Adapter
│
├─ Need to add responsibilities without subclassing?
│  └─→ Decorator
│
└─ Want to simplify complex subsystem?
   └─→ Facade
```

## Process

### Phase 1: Identify the Problem

Analyze the code to identify specific issues.

1. **Read the code** - Understand current implementation
2. **Identify code smells** - Look for:
   - Tight coupling between classes
   - Large constructors or parameter lists
   - Conditional logic that changes frequently
   - Duplicate code across similar classes
   - Global state or singletons everywhere
   - Classes with too many responsibilities

**Verification:** You can clearly articulate the specific problem or limitation.

### Phase 2: Match Problem to Pattern

Select the most appropriate pattern.

1. **Use decision tree** - Navigate the decision tree above
2. **Consult reference files** - Read detailed pattern documentation:
   - `references/creational.md` - Factory Method, Abstract Factory, Builder, Singleton
   - `references/structural.md` - Adapter, Decorator, Facade
   - `references/behavioral.md` - Observer, Strategy, Command, State, Template Method
3. **Consider alternatives** - Evaluate 2-3 patterns if multiple fit
4. **Explain trade-offs** - Discuss pros/cons of recommended approach

**Verification:** The pattern directly addresses the identified problem.

### Phase 3: Implement Solution

Guide implementation with concrete examples.

1. **Show structure** - Explain key participants (interfaces, classes, relationships)
2. **Provide example** - Write TypeScript code demonstrating the pattern
3. **Explain flow** - Walk through how components interact
4. **Point out gotchas** - Warn about common mistakes

**Verification:** Implementation follows pattern principles and solves the original problem.

## Common Scenarios → Patterns

| Scenario | Pattern | Why |
|----------|---------|-----|
| Multiple button types trigger save, but implementation differs | Strategy | Swap save algorithms at runtime |
| UI needs to update when data changes | Observer | Automatic notification system |
| Need to add logging, validation to existing objects | Decorator | Add behavior without modifying originals |
| Working with legacy API that doesn't match your interface | Adapter | Bridge incompatible interfaces |
| Complex library with 50 classes, just need simple operations | Facade | Simplified interface to subsystem |
| Creating game characters with many customization options | Builder | Step-by-step construction |
| Document editor with undo/redo | Command | Encapsulate operations as objects |
| Connection states: disconnected, connecting, connected | State | Behavior changes with state |
| Need to save object snapshots for rollback | Memento | Capture and restore state without breaking encapsulation |

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Pattern for pattern's sake | Adds unnecessary complexity | Identify actual problem first |
| Singleton everywhere | Hidden dependencies, hard to test | Dependency injection |
| Deep decorator chains | Debugging nightmare | Consider composition or other patterns |
| Premature abstraction | YAGNI violation | Wait for clear pattern of repetition |
| Factory for single product | Over-engineering | Direct instantiation is fine |
| Observer for everything | Memory leaks, performance issues | Use only when truly needed |

## Verification

After applying a pattern:

- [ ] The original problem is solved
- [ ] Code is more maintainable, not more complex
- [ ] Pattern participants have clear responsibilities
- [ ] Tests pass and cover new structure
- [ ] Team members understand the pattern choice
- [ ] No unnecessary abstraction layers added

## Extension Points

1. **Custom patterns**: Document your own domain-specific patterns based on these fundamentals
2. **Pattern combinations**: Some problems benefit from combining multiple patterns
3. **Refactoring catalog**: Build a library of before/after refactorings for your codebase

## References

- [Creational Patterns](references/creational.md) - Factory Method, Abstract Factory, Builder, Singleton
- [Structural Patterns](references/structural.md) - Adapter, Decorator, Facade
- [Behavioral Patterns](references/behavioral.md) - Observer, Strategy, Command, State, Template Method, Memento
- [Refactoring.Guru](https://refactoring.guru/design-patterns/catalog) - Complete catalog with examples

---

**Note**: Pattern selection requires judgment. When in doubt, prefer simpler solutions over pattern application.
