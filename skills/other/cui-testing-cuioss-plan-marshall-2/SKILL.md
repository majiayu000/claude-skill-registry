---
name: cui-testing
description: CUI test library standards for test data generation, value object contracts, and JUL log testing
user-invocable: false
allowed-tools: Read, Grep, Glob
---

# CUI Testing Skill

**REFERENCE MODE**: This skill provides reference material. Load specific standards on-demand based on current task.

CUI-specific testing standards for projects using CUI test libraries. This skill covers the mandatory test data generator framework, value object contract testing, and JUL log testing utilities.

## Prerequisites

This skill requires CUI test library dependencies:
- `de.cuioss.test:cui-test-generator` (Generators, TypedGenerator)
- `de.cuioss.test:cui-test-value-objects` (ShouldHandleObjectContracts)
- `de.cuioss.test:cui-test-juli` (EnableTestLogger, LogAsserts)

## Workflow

### Step 1: Load Test Generator Framework

**CRITICAL**: Load this standard for any test implementation work.

```
Read: standards/test-generator-framework.md
```

This provides the foundational rules:
- MANDATORY use of `Generators.*` for ALL test data
- FORBIDDEN: Manual test data, Random, Faker
- REQUIRED: `@EnableGeneratorController` annotation

### Step 2: Load Additional Standards (As Needed)

**Value Object Testing** (load for domain object tests):
```
Read: standards/testing-value-objects.md
```

Use when: Testing value objects, implementing equals/hashCode contracts, or using `ShouldHandleObjectContracts<T>`.

**JUL Log Testing** (load for log verification tests):
```
Read: standards/testing-juli-logger.md
```

Use when: Testing code that uses CUI logging and needs to verify log output with `@EnableTestLogger` and `LogAsserts`.

## Key Rules Summary

### Test Data Generation
```java
// CORRECT - Use Generators
@EnableGeneratorController
class MyServiceTest {
    @Test
    void shouldProcess() {
        String input = Generators.nonEmptyStrings().next();
        // ...
    }
}

// FORBIDDEN - Never use manual data or Random
String input = "test"; // WRONG
String input = UUID.randomUUID().toString(); // WRONG
```

### Parameterized Tests
```java
// CORRECT - Use @GeneratorsSource
@ParameterizedTest
@GeneratorsSource(EmailGenerator.class)
void shouldValidateEmail(String email) {
    // Test with generated emails
}
```

### Value Object Contracts
```java
// Implements automatic contract testing
class PersonTest implements ShouldHandleObjectContracts<Person> {
    @Override
    public Person getUnderTest() {
        return new PersonGenerator().next();
    }
}
```

### Log Testing
```java
@EnableTestLogger
class MyServiceTest {
    @Test
    void shouldLogWarning() {
        // Execute code that logs
        service.processWithWarning();

        // Verify log output
        LogAsserts.assertLogContains(TestLogLevel.WARN, "expected message");
    }
}
```

## Related Skills

- `pm-dev-java:junit-core` - General JUnit 5 patterns (no CUI dependencies)
- `pm-dev-java-cui:cui-logging` - CUI logging standards (use with cui-testing for log tests)

## Standards Reference

| Standard | Purpose |
|----------|---------|
| test-generator-framework.md | Mandatory test data generation |
| testing-value-objects.md | Contract testing for value objects |
| testing-juli-logger.md | JUL log testing with LogAsserts |
