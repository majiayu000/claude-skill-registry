---
name: backend-testing
description: Write and review backend tests with JUnit5, MockMvc, and Spring Boot Test. Use for writing controller tests, service tests, and integration tests.
---

# Backend Testing Skill

## When to Use

- Writing unit tests for services or repositories
- Writing controller tests with MockMvc
- Writing integration tests
- Reviewing test coverage or test quality

---

## Stack

- JUnit5 + Spring Boot Test
- MockMvc for controller tests
- (Optional) Testcontainers for integration tests

---

## Minimum Requirements

Each endpoint requires:
- At least 1 success test
- At least 1 failure test

Document important endpoints with Spring REST Docs.

---

## What to Test

1. **Validation errors** - Invalid input handling
2. **Authorization errors** - If applicable
3. **Idempotency behaviors** - Duplicate request handling
4. **TTL expiry behaviors** - Session/token expiration

---

## Test Organization

```
src/test/java/
├── controller/
│   └── {Feature}ControllerTest.java
├── service/
│   └── {Feature}ServiceTest.java
└── integration/
    └── {Feature}IntegrationTest.java
```

---

## Test Naming Convention

```java
@Test
void should_ReturnSuccess_When_ValidInput() { }

@Test
void should_ThrowException_When_InvalidInput() { }
```
