---
name: Spring Boot Testing
description: Standards for unit, integration, and slice testing in Spring Boot 3
metadata:
  labels: [spring-boot, testing, junit, testcontainers]
  triggers:
    files: ['**/*Test.java']
    keywords: [webmvctest, datajpatest, testcontainers, assertj]
---

# Spring Boot Testing Standards

## **Priority: P0**

## Implementation Guidelines

### TDD Workflow

1.  **Red**: Write a failing test (e.g., `returns 404`).
2.  **Green**: Implement minimal code to pass.
3.  **Refactor**: Clean up while keeping tests green.
4.  **Coverage**: Verify with JaCoCo.

### Best Practices

- **Real Infrastructure**: Use **Testcontainers** for DB/Queues. See [Integration Template](references/testing-template.md).
- **Slice Testing**: See [Slice Test Templates](references/testing-template.md#slice-tests) for `@WebMvcTest` / `@DataJpaTest`.

### Best Practices

- **Real Infrastructure**: Use **Testcontainers** for DB/Queues. Avoid H2/Embedded.
- **Assertions**: Use **AssertJ** (`assertThat`) over JUnit assertions.
- **Isolation**: Use `@MockBean` for downstream dependencies in Slice Tests.

## Anti-Patterns

- **Context Reloading**: `**No Dirty Contexts**: Avoid @MockBean in base classes.`
- **External Calls**: `**No network I/O**: Use WireMock.`
- **System Out**: `**No System.out**: Use assertions.`

## References

- [Implementation Examples](references/implementation.md)
