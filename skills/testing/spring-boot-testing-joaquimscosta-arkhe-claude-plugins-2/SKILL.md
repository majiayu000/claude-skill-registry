---
name: spring-boot-testing
description: Spring Boot 4 testing strategies and patterns. Use when writing unit tests, slice tests (@WebMvcTest, @DataJpaTest), integration tests, Testcontainers with @ServiceConnection, security testing (@WithMockUser, JWT), or Modulith event testing with Scenario API. Covers the critical @MockitoBean migration from @MockBean.
---

# Spring Boot 4 Testing

Comprehensive testing patterns including slice tests, Testcontainers, security testing, and Modulith Scenario API.

## Critical Breaking Change

| Old (Boot 3.x) | New (Boot 4.x) | Notes |
|----------------|----------------|-------|
| `@MockBean` | `@MockitoBean` | **Required migration** |
| `@SpyBean` | `@MockitoSpyBean` | **Required migration** |
| `MockMvc` (procedural) | `MockMvcTester` (fluent) | **New AssertJ-style API** |
| Implicit `@AutoConfigureMockMvc` | Explicit annotation required | Add to `@SpringBootTest` |

## MockMvcTester (Spring Boot 4)

New fluent, AssertJ-style API for controller testing:

```java
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvcTester mvc;  // NEW: Fluent API

    @Test
    void getUser_returnsUser() {
        mvc.get().uri("/users/{id}", 1)
            .exchange()
            .assertThat()
            .hasStatusOk()
            .bodyJson()
            .extractingPath("$.name")
            .isEqualTo("John");
    }
}
```

**Key Benefits**: Fluent assertions, better error messages, AssertJ integration.

## Test Annotation Selection

| Test Type | Annotation | Use When |
|-----------|------------|----------|
| Controller | `@WebMvcTest` | Testing request/response, validation |
| Repository | `@DataJpaTest` | Testing queries, entity mapping |
| JSON | `@JsonTest` | Testing serialization/deserialization |
| REST Client | `@RestClientTest` | Testing external API clients |
| Full Integration | `@SpringBootTest` | End-to-end, with real dependencies |
| Module | `@ApplicationModuleTest` | Testing bounded context in isolation |

## Core Workflow

1. **Choose test slice** → Minimal context for fast tests
2. **Mock dependencies** → `@MockitoBean` for external services
3. **Use Testcontainers** → `@ServiceConnection` for databases
4. **Assert thoroughly** → Use AssertJ, `MockMvcTester` (new), `RestTestClient` (new), WebTestClient
5. **Test security** → `@WithMockUser`, JWT mocking

## Quick Patterns

See [EXAMPLES.md](EXAMPLES.md) for complete working examples including:
- **@WebMvcTest** with `MockMvcTester` and `@MockitoBean` (Java + Kotlin)
- **@DataJpaTest** with `TestEntityManager` for lazy loading verification
- **Testcontainers** with `@ServiceConnection` for PostgreSQL/Redis
- **Security Testing** with `@WithMockUser` for role-based access
- **Modulith Event Testing** with `Scenario` API

## Detailed References

- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for complete working code examples
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and Boot 4 migration
- **Slice Tests**: See [references/SLICE-TESTS.md](references/SLICE-TESTS.md) for @WebMvcTest, @DataJpaTest, @JsonTest patterns
- **Testcontainers**: See [references/TESTCONTAINERS.md](references/TESTCONTAINERS.md) for @ServiceConnection, container reuse
- **Security Testing**: See [references/SECURITY-TESTING.md](references/SECURITY-TESTING.md) for @WithMockUser, JWT mocking
- **Modulith Testing**: See [references/MODULITH-TESTING.md](references/MODULITH-TESTING.md) for Scenario API, event verification

## Anti-Pattern Checklist

| Anti-Pattern | Fix |
|--------------|-----|
| Using `@MockBean` in Boot 4 | Replace with `@MockitoBean` |
| `@SpringBootTest` for unit tests | Use appropriate slice annotation |
| Missing `entityManager.clear()` | Add to verify lazy loading |
| High-cardinality test data | Use minimal, focused fixtures |
| Shared mutable test state | Use `@DirtiesContext` or fresh containers |
| No security tests | Add `@WithMockUser` tests for endpoints |

## Critical Reminders

1. **@MockitoBean is mandatory** — `@MockBean` removed in Boot 4
2. **Slice tests are fast** — Use them for focused testing
3. **Clear EntityManager** — Required to test lazy loading behavior
4. **@ServiceConnection simplifies Testcontainers** — No more `@DynamicPropertySource`
5. **Test security explicitly** — Don't rely on disabled security
