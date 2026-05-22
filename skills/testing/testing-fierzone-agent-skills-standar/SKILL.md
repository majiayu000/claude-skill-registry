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

### Test Strategy

- **Unit First**: Prioritize pure unit tests (Mockito) over Context tests.
- **Slice Testing**: Use `@WebMvcTest` (Controllers) and `@DataJpaTest` (Repos) to reduce build time.
- **Integration**: Use `@SpringBootTest` only for critical end-to-end flows.

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
