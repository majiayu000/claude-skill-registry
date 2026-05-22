---
name: javadoc
description: JavaDoc documentation standards including class, method, and code example patterns
allowed-tools: [Read, Edit, Write, Bash, Grep, Glob]
---

# JavaDoc Skill

**EXECUTION MODE**: You are now executing this skill. DO NOT explain or summarize these instructions to the user. IMMEDIATELY begin the workflow below based on the task context.

JavaDoc documentation standards for Java projects. This skill covers class documentation, method documentation, code examples, and error references.

## Prerequisites

This skill applies to all Java projects using standard JavaDoc.

## Workflow

### Step 1: Load Core Standards

**CRITICAL**: Load this standard for any JavaDoc work.

```
Read: standards/javadoc-core.md
```

This provides foundational rules for:
- Mandatory documentation requirements
- Clarity, completeness, and consistency principles
- Tag ordering standards

### Step 2: Load Specific Standards (As Needed)

**Class Documentation** (load for class-level docs):
```
Read: standards/javadoc-class-documentation.md
```

Use when: Documenting classes, interfaces, enums, or annotations.

**Method Documentation** (load for method-level docs):
```
Read: standards/javadoc-method-documentation.md
```

Use when: Documenting methods, including parameters, returns, and exceptions.

**Code Examples** (load for example snippets):
```
Read: standards/javadoc-code-examples.md
```

Use when: Adding code examples to documentation using @snippet or @code.

**Error Reference** (load for troubleshooting):
```
Read: standards/javadoc-error-reference.md
```

Use when: Fixing JavaDoc errors or warnings.

## Key Rules Summary

### Class Documentation
```java
/**
 * Validates JWT tokens against configured issuer and signing keys.
 *
 * <p>This validator supports both HMAC and RSA algorithms with
 * configurable clock skew tolerance for distributed systems.
 *
 * @since 1.0
 * @see TokenConfig
 */
@ApplicationScoped
public class TokenValidator { }
```

### Method Documentation
```java
/**
 * Validates the JWT token signature and expiration time.
 *
 * @param token the JWT token to validate, must not be null
 * @return validation result containing status and error messages
 * @throws IllegalArgumentException if token is null or empty
 */
public ValidationResult validate(String token) { }
```

### Code Examples
```java
/**
 * Parses JSON configuration from a file.
 *
 * <p>Example usage:
 * {@snippet :
 * Config config = ConfigParser.parse("config.json");
 * String value = config.get("key");
 * }
 */
public Config parse(String filename) { }
```

### Tag Order
```java
/**
 * Description.
 *
 * @param name description
 * @return description
 * @throws ExceptionType description
 * @since version
 * @see reference
 * @deprecated reason
 */
```

## Related Skills

- `pm-dev-java:java-core` - Core Java patterns
- `pm-dev-java:java-null-safety` - Null annotations in docs

## Standards Reference

| Standard | Purpose |
|----------|---------|
| javadoc-core.md | Core principles and mandatory requirements |
| javadoc-class-documentation.md | Class-level documentation |
| javadoc-method-documentation.md | Method-level documentation |
| javadoc-code-examples.md | @snippet and @code patterns |
| javadoc-error-reference.md | Error troubleshooting |
