---
name: junit-core
description: JUnit 5 core testing patterns with AAA structure, test organization, and coverage standards
allowed-tools: [Read, Edit, Write, Bash, Grep, Glob]
---

# JUnit Core Skill

**EXECUTION MODE**: You are now executing this skill. DO NOT explain or summarize these instructions to the user. IMMEDIATELY begin the workflow below based on the task context.

JUnit 5 testing standards for general Java projects. This skill covers test structure, naming conventions, coverage requirements, and the AAA (Arrange-Act-Assert) pattern.

## Prerequisites

This skill applies to Java projects using JUnit 5:
- `org.junit.jupiter:junit-jupiter` (JUnit 5)

## Workflow

### Step 1: Load Core Testing Standards

**CRITICAL**: Load this standard for any testing work.

```
Read: standards/testing-junit-core.md
```

This provides foundational rules for:
- Test class requirements (1:1 mapping with production classes)
- AAA pattern (Arrange-Act-Assert)
- Coverage requirements (80% line/branch minimum)
- @DisplayName usage

### Step 2: Load Coverage Analysis (As Needed)

**Coverage Analysis** (load for coverage work):
```
Read: standards/coverage-analysis-pattern.md
```

Use when: Analyzing test coverage or improving coverage metrics.

## Key Rules Summary

### Test Class Requirements
```java
// CORRECT - One test class per production class
// TokenValidator.java → TokenValidatorTest.java
// UserService.java → UserServiceTest.java
```

### AAA Pattern (Arrange-Act-Assert)
```java
@Test
@DisplayName("Should validate token with correct issuer")
void shouldValidateTokenWithCorrectIssuer() {
    // Arrange
    String issuer = "https://example.com";
    Token token = createTokenWithIssuer(issuer);

    // Act
    ValidationResult result = validator.validate(token);

    // Assert
    assertTrue(result.isValid());
    assertEquals(issuer, result.getIssuer());
}
```

### DisplayName Annotations
```java
// CORRECT - Descriptive test names
@Test
@DisplayName("Should throw exception when token is null")
void shouldThrowExceptionWhenTokenIsNull() { }

@Test
@DisplayName("Should return empty when no users found")
void shouldReturnEmptyWhenNoUsersFound() { }
```

### Coverage Requirements
- Minimum 80% line coverage
- Minimum 80% branch coverage
- Critical paths: 100% coverage
- All public APIs must be tested

## Related Skills

- `pm-dev-java:junit-integration` - Maven integration testing
- `pm-dev-java-cui:cui-testing` - CUI test generator framework
- `pm-dev-java:java-core` - Core Java patterns

## Standards Reference

| Standard | Purpose |
|----------|---------|
| testing-junit-core.md | Test structure, AAA pattern, naming |
| coverage-analysis-pattern.md | Coverage analysis and improvement |
