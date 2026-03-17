---
name: Java Best Practices
description: Core engineering principles inspired by Effective Java and Clean Code.
metadata:
  labels: [java, best-practices, effective-java, clean-code]
  triggers:
    files: ['**/*.java']
    keywords: [refactor, clean code, smells, patterns, design]
---

# Java Best Practices

## **Priority: P1 (HIGH)**

Core engineering principles for robust, maintainable Java systems.

## Implementation Guidelines

- **Immutability**: Prefer immutable objects (`final` fields, unmodifiable collections).
- **Access Modifiers**: Minimize visibility. Default to **package-private** (no modifier). Use `private` for all fields. Only `public` for API contracts.
- **Composition > Inheritance**: Favor `Has-A` over `Is-A`. Avoid deep hierarchies.
- **Constructors**: Use Static Factory Methods (`User.of()`) over complex constructors.
- **Builder Pattern**: Use for objects with 4+ parameters.
- **Exceptions**: Use Checked vs Unchecked wisely. Recoverable -> Checked; Programming Error -> Unchecked.
- **Fail Fast**: Validate parameters (`Objects.requireNonNull`) at the method start.
- **Interfaces**: Code to interfaces (`List`, `Map`), not implementations (`ArrayList`, `HashMap`).
- **Dependency Injection**: Invert control. Inject dependencies via constructor.
- **Method References**: Use `String::toUpperCase` over `s -> s.toUpperCase()` where readable.

## Anti-Patterns

- **Return Null**: Returns empty `Optional` or Collection instead.
- **Empty Catch**: Never swallow exceptions. Log or rethrow.
- **God Class**: Single Responsibility Principle. Break it down.
- **Magic Numbers**: Extract constants with meaningful names.
- **Mutable Statics**: Avoid `public static` fields (Global state).

## Code

```java
// Static Factory + Builder (Implicit via Library or Manual)
public class Pizza {
  private final int size;
  private final boolean cheese;

  private Pizza(Builder b) { ... }

  public static Pizza of(int size) {
    return new Pizza(size, false);
  }
}

// Composition
public class Service {
  private final Repository repo; // Injected

  public Service(Repository repo) {
    this.repo = Objects.requireNonNull(repo);
  }
}
```

## Related Topics

language | concurrency | tooling
