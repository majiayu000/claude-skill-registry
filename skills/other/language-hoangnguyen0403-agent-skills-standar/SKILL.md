---
name: Java Language Patterns
description: Modern Java standards (21+) including Records, Pattern Matching, and Virtual Threads.
metadata:
  labels: [java, language, jdk21, modern-java]
  triggers:
    files: ['**/*.java', 'pom.xml', 'build.gradle']
    keywords: [record, switch, sealed, var, virtual thread, stream, optional]
---

# Java Language Patterns

## **Priority: P0 (CRITICAL)**

Modern Java (21+) standards for concise, immutable, and expressive code.

## Implementation Guidelines

- **Records**: Use `record` for DTOs/Value Objects. Avoid Lombok `@Data` where possible.
- **Local Variables**: Use `var` for clear, inferred types. Explicit types for interfaces.
- **Switch**: Use Switch Expressions `->` and Pattern Matching over `if/else` chains.
- **Text Blocks**: Use `"""` for JSON/SQL strings. Avoid concatenation `+`.
- **Pattern Matching**: Use `instanceof` with binding: `if (obj instanceof String s)`.
- **Sealed Classes**: Use `sealed interface/class` for restricted hierarchies (Domain Models).
- **Collections**: Use `List.of()`, `Map.of()`, `Set.of()` for unmodifiable collections.
- **Streams**: Use `stream()` for transformations. Prefer `toList()` (Java 16+) over `collect(Collectors.toList())`.
- **Optional**: Return `Optional<T>` over `null`. Use `map`, `filter`, `ifPresent`. Never use `Optional` fields/params.
- **Virtual Threads**: Prefer `Executors.newVirtualThreadPerTaskExecutor()` for high-throughput I/O.

## Anti-Patterns

- **No `null`**: `**No Nulls**: Return Optional or empty collections; avoid null parameters.`
- **No Raw Types**: `**Use Generics**: Never use raw types like List.`
- **No Old Switch**: `**No Fall-through**: Use Switch Expressions ->.`
- **Boilerplate**: `**No manual get/set**: Use Records or value objects.`
- **Blocking**: `**No synchronized**: Use java.util.concurrent utilities or Virtual Threads.`

## Code

```java
// Record + Pattern Matching
public record User(String id, String name) {}

public String handle(Object obj) {
  return switch (obj) {
    case User(var id, var name) -> "User: " + name; // Record Patterns (Java 21)
    case String s when s.length() > 5 -> "Long String: " + s;
    case null -> "It's null";
    default -> "Unknown";
  };
}

// Virtual Threads (Loom)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var userDetails = scope.fork(() -> fetchUser());
    var orders = scope.fork(() -> fetchOrders());
    scope.join().throwIfFailed(); // Wait for both
}
```

## Related Topics

best-practices | concurrency | testing
