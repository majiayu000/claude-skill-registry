---
name: java-create
description: Interactive wizard for creating Java components with standards compliance
user-invocable: true
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
---

# Java Core Skill

**REFERENCE MODE**: This skill provides reference material. Load specific standards on-demand based on current task.

Core Java development standards for general Java projects. This skill covers fundamental patterns, modern Java features, performance optimization, and implementation verification.

## Prerequisites

This skill applies to Java 17+ projects with no CUI-specific dependencies.

## Workflow

### Step 1: Load Core Patterns

**CRITICAL**: Load this standard for any Java implementation work.

```
Read: standards/java-core-patterns.md
```

This provides foundational rules for:
- Package and class structure
- Method design and command-query separation
- Parameter objects and method complexity
- Code organization principles

### Step 2: Load Additional Standards (As Needed)

**Modern Java Features** (load for new code):
```
Read: standards/java-modern-features.md
```

Use when: Writing new code or modernizing existing code. Covers records, pattern matching, sealed classes, and text blocks.

**Performance Patterns** (load for optimization work):
```
Read: standards/java-performance-patterns.md
```

Use when: Optimizing code or designing high-performance components.

**Build Precondition Pattern** (load for validation logic):
```
Read: standards/build-precondition-pattern.md
```

Use when: Implementing validation logic or precondition checking.

**Implementation Verification** (load for code review):
```
Read: standards/implementation-verification.md
```

Use when: Reviewing implementations or verifying code quality.

## Key Rules Summary

### Package Structure
```java
// CORRECT - Feature-based organization
de.example.portal.authentication     // Authentication feature
de.example.portal.configuration      // Configuration feature
de.example.portal.user.management    // User management feature
```

### Command-Query Separation
```java
// Query - returns value, no side effects
public boolean isValid() {
    return status == Status.VALID;
}

// Command - modifies state, returns void
public void markAsInvalid() {
    this.status = Status.INVALID;
}
```

### Parameter Objects (3+ parameters)
```java
// CORRECT - Multiple related parameters grouped
public record ValidationRequest(
    String tokenId,
    Set<String> expectedScopes,
    Duration maxAge,
    String issuer
) {}

public boolean validate(ValidationRequest request) {
    // Clear, organized parameters
}
```

## Related Skills

- `pm-dev-java:java-null-safety` - JSpecify null annotations
- `pm-dev-java:java-lombok` - Lombok patterns
- `pm-dev-java:junit-core` - JUnit 5 testing patterns
- `pm-dev-java:javadoc` - JavaDoc documentation standards

## Standards Reference

| Standard | Purpose |
|----------|---------|
| java-core-patterns.md | Code organization and design principles |
| java-modern-features.md | Records, pattern matching, sealed classes |
| java-performance-patterns.md | Performance optimization patterns |
| build-precondition-pattern.md | Validation logic patterns |
| implementation-verification.md | Code review and verification |
