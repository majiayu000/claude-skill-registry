---
name: kotlin-testing
description: Kotlin testing with JUnit 5, MockK, Spring test slices, and Testcontainers. Provides mocking patterns, test slice selection, and TDD workflow for Spring Boot + Kotlin. Use when writing tests for Kotlin/Spring code, setting up test infrastructure, or debugging test failures.
---

# Kotlin Testing

Testing patterns for Spring Boot 4 + Kotlin 2 projects.

## When to Use

- Writing unit tests for services/repositories
- Setting up integration tests with Testcontainers
- Mocking dependencies with MockK
- Selecting appropriate Spring test slices
- Debugging flaky or failing tests

## MCP Workflow

```kotlin
# 1. Find existing test patterns
serena.search_for_pattern("@Test|@MockK|@SpringBootTest", relative_path="src/test/")

# 2. Check test utilities
serena.get_symbols_overview(relative_path="src/test/kotlin/.../support/")

# 3. Find test slice usage
jetbrains.search_in_files_by_text("@DataJpaTest|@WebMvcTest", fileMask="*Test.kt")

# 4. Spring testing docs
context7.get-library-docs("/spring/spring-boot", "testing")
```

## Test Slice Selection

| Slice | Use When | Loads |
|-------|----------|-------|
| `@SpringBootTest` | Full integration | Everything |
| `@WebMvcTest` | Controller only | Web layer |
| `@DataJpaTest` | Repository only | JPA + DB |
| `@MockMvcTest` | REST endpoints | MockMvc |
| None (unit test) | Service/domain logic | Nothing |

**Rule**: Start with unit tests (no slice), add slices only when testing integration points.

## MockK Patterns

### Basic Mocking

```kotlin
@ExtendWith(MockKExtension::class)
class PipelineServiceTest {
    @MockK
    private lateinit var repository: PipelineRepositoryJpa

    @InjectMockKs
    private lateinit var service: PipelineService

    @Test
    fun `should create pipeline`() {
        // Arrange
        val command = CreatePipelineCommand(name = "test")
        val entity = PipelineEntity(id = 1, name = "test")
        every { repository.save(any()) } returns entity

        // Act
        val result = service.create(command)

        // Assert
        assertThat(result.name).isEqualTo("test")
        verify(exactly = 1) { repository.save(any()) }
    }
}
```

### Relaxed Mocks (Stubs)

```kotlin
@MockK(relaxed = true)  // Returns sensible defaults
private lateinit var logger: Logger

// Or inline
val mockRepo = mockk<Repository>(relaxed = true)
```

### Capturing Arguments

```kotlin
val slot = slot<PipelineEntity>()
every { repository.save(capture(slot)) } returns mockEntity

service.create(command)

assertThat(slot.captured.name).isEqualTo("test")
```

### Coroutines (coEvery/coVerify)

```kotlin
coEvery { asyncService.process(any()) } returns Result.success()
coVerify { asyncService.process(match { it.id == 1L }) }
```

## Spring Test Patterns

### @DataJpaTest (Repository Testing)

```kotlin
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@Testcontainers
class UserRepositoryTest {
    companion object {
        @Container
        val mysql = MySQLContainer("mysql:8.0")
            .withDatabaseName("test")

        @DynamicPropertySource
        @JvmStatic
        fun properties(registry: DynamicPropertyRegistry) {
            registry.add("spring.datasource.url", mysql::getJdbcUrl)
            registry.add("spring.datasource.username", mysql::getUsername)
            registry.add("spring.datasource.password", mysql::getPassword)
        }
    }

    @Autowired
    private lateinit var repository: UserRepositoryJpaSpringData

    @Test
    fun `should find by email`() {
        val user = UserEntity(email = "test@example.com")
        repository.save(user)

        val found = repository.findByEmail("test@example.com")

        assertThat(found?.email).isEqualTo("test@example.com")
    }
}
```

### @WebMvcTest (Controller Testing)

```kotlin
@WebMvcTest(PipelineController::class)
class PipelineControllerTest {
    @Autowired
    private lateinit var mockMvc: MockMvc

    @MockkBean
    private lateinit var pipelineService: PipelineService

    @Test
    fun `should return pipeline by id`() {
        every { pipelineService.findById(1L) } returns PipelineDto(id = 1, name = "test")

        mockMvc.get("/api/pipelines/1")
            .andExpect {
                status { isOk() }
                jsonPath("$.name") { value("test") }
            }
    }
}
```

## TDD Workflow for Kotlin

### 1. RED: Write Failing Test

```kotlin
@Test
fun `should reject duplicate pipeline names`() {
    every { repository.existsByName("existing") } returns true

    assertThrows<DuplicateNameException> {
        service.create(CreatePipelineCommand(name = "existing"))
    }
}
```

### 2. GREEN: Implement

```kotlin
fun create(command: CreatePipelineCommand): PipelineDto {
    if (repository.existsByName(command.name)) {
        throw DuplicateNameException("Pipeline '${command.name}' exists")
    }
    return repository.save(command.toEntity()).toDto()
}
```

### 3. REFACTOR: Improve

- Extract validation to domain
- Add more edge case tests
- Verify exception messages

## Anti-Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| `@SpringBootTest` for unit tests | Slow, loads everything | Remove annotation |
| `every { } returns` without verify | Mock unused | Add `verify` or use `relaxed` |
| Testing private methods | Brittle tests | Test through public API |
| `Thread.sleep()` in tests | Flaky | Use `awaitility` or latch |
| Mocking data classes | Unnecessary | Use real instances |

## Quality Checklist

- [ ] Unit tests use no Spring context (fast)
- [ ] Integration tests use appropriate slice
- [ ] Mocks verified with `verify` blocks
- [ ] Testcontainers for database tests
- [ ] No `Thread.sleep()` (use awaitility)
- [ ] Tests follow AAA pattern (Arrange-Act-Assert)
- [ ] Test names describe behavior: `should X when Y`
