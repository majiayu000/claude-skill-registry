---
name: testing-patterns
description: Testing patterns and principles. Unit, integration, mocking strategies.
category: security
version: 4.1.0-fractal
layer: master-skill
---

# Testing Patterns

> Principles for reliable test suites.

---

## 1. Testing Pyramid

```
        /\          E2E (Few)
       /  \         Critical flows
      /----\
     /      \       Integration (Some)
    /--------\      API, DB queries
   /          \
  /------------\    Unit (Many)
                    Functions, classes
```

---

## 2. AAA Pattern

| Step | Purpose |
|------|---------|
| **Arrange** | Set up test data |
| **Act** | Execute code under test |
| **Assert** | Verify outcome |

---

## 3. Test Type Selection

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [When to Use Each](./sub-skills/when-to-use-each.md)
### 2. [Good Unit Tests](./sub-skills/good-unit-tests.md)
### 3. [What to Unit Test](./sub-skills/what-to-unit-test.md)
### 4. [What to Test](./sub-skills/what-to-test.md)
### 5. [Setup/Teardown](./sub-skills/setupteardown.md)
### 6. [When to Mock](./sub-skills/when-to-mock.md)
### 7. [Mock Types](./sub-skills/mock-types.md)
### 8. [Naming](./sub-skills/naming.md)
### 9. [Grouping](./sub-skills/grouping.md)
### 10. [Strategies](./sub-skills/strategies.md)
### 11. [Principles](./sub-skills/principles.md)
