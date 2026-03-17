---
name: kotlin-testing
description: Kotlin testing with JUnit 5, MockK, Spring test slices, and fast feedback commands. Provides single test execution, incremental builds, and JetBrains MCP integration for rapid TDD cycles. Use when writing tests for Kotlin/Spring code, running specific tests, or debugging test failures.
---

# Kotlin Testing

## 🚀 MANDATORY: Fast Feedback Workflow

> **이 워크플로우를 반드시 따르세요. 개발 속도가 10배 이상 빨라집니다.**

### 개발 사이클 (매 코드 수정마다 반복)

```
1. 코드 수정
2. IDE 검사 (0-2초)     → jetbrains.get_file_problems(...)
3. 단일 테스트 (5-10초)  → ./gradlew :module:test --tests "*Test"
4. 반복
5. 기능 완료 후 (1회만)  → ./gradlew build
```

### ⚠️ 금지 패턴 (절대 사용 금지)

```bash
# ❌ 개발 중 절대 금지
./gradlew clean build        # 60-120초 낭비!
./gradlew test               # 전체 테스트 금지!
./gradlew clean              # clean 불필요!

# ✅ 올바른 사용
./gradlew :module-core-domain:test --tests "*ServiceTest"      # 5-10초
./gradlew :module-server-api:test --tests "*ControllerTest"    # 5-10초
```

### JetBrains MCP 먼저 사용 (STEP 1)

코드 수정 후 **항상** IDE 검사 먼저 실행:

```python
# 필수: 코드 수정 후 즉시 에러 확인 (0-2초)
jetbrains.get_file_problems(
    filePath="module-core-domain/src/main/kotlin/.../Service.kt",
    errorsOnly=True
)

# 에러 없으면 단일 테스트 실행
jetbrains.execute_terminal_command(
    command="./gradlew :module-core-domain:test --tests '*ServiceTest'",
    timeout=60000
)
```

---

## When to Use

- Writing unit tests for services/repositories
- **Running single tests during TDD** (fast feedback)
- Setting up integration tests with Testcontainers
- Mocking dependencies with MockK
- Debugging flaky or failing tests

---

## Fast Feedback Commands Reference

> **Never use `./gradlew clean build` during development iterations!**

### Command Selection Guide

| Situation | Command | Time |
|-----------|---------|------|
| **Single test class** | `./gradlew :module:test --tests "*ServiceTest"` | ~5-10s |
| **Single test method** | `./gradlew :module:test --tests "*ServiceTest.should*"` | ~5-10s |
| **Module tests only** | `./gradlew :module:test` | ~15-30s |
| **Compile check only** | `./gradlew :module:compileKotlin` | ~3-5s |
| **Full build (CI only)** | `./gradlew clean build` | ~60-120s |

### Module Names Reference

```bash
# project-basecamp-server modules
:module-core-common:test      # Utilities
:module-core-domain:test      # Domain services, entities
:module-core-infra:test       # Repository impls, external clients
:module-server-api:test       # Controllers
```

### Single Test Patterns

```bash
# Run single test class
./gradlew :module-core-domain:test --tests "*PipelineServiceTest"

# Run single test method (partial match)
./gradlew :module-core-domain:test --tests "*PipelineServiceTest.should create*"

# Run tests matching pattern
./gradlew :module-core-domain:test --tests "*Service*"

# Run with console output (for debugging)
./gradlew :module-core-domain:test --tests "*ServiceTest" --info

# Re-run only failed tests
./gradlew :module-core-domain:test --tests "*ServiceTest" --rerun
```

### Incremental Build (NO clean!)

```bash
# Compile only (fastest check for syntax errors)
./gradlew :module-core-domain:compileKotlin

# Compile + test single class (fast TDD cycle)
./gradlew :module-core-domain:compileKotlin && \
./gradlew :module-core-domain:test --tests "*ServiceTest"

# Module build (no clean)
./gradlew :module-core-domain:build

# Full build WITHOUT clean (uses cache)
./gradlew build
```

### JetBrains MCP Integration (Fastest)

```python
# Option 1: Quick compile check via IDE inspection
jetbrains.get_file_problems(
    filePath="module-core-domain/src/main/kotlin/.../Service.kt",
    errorsOnly=True,
    timeout=5000
)

# Option 2: Run test via terminal
jetbrains.execute_terminal_command(
    command="./gradlew :module-core-domain:test --tests '*ServiceTest'",
    timeout=60000,
    maxLinesCount=200
)

# Option 3: Use existing run configuration
jetbrains.get_run_configurations()  # List available
jetbrains.execute_run_configuration(
    configurationName="ServiceTest",
    timeout=30000
)
```

---

## TDD Fast Feedback Loop

### 1. Write Test (RED)

```kotlin
@Test
fun `should reject duplicate names`() {
    every { repository.existsByName("existing") } returns true

    assertThrows<DuplicateNameException> {
        service.create(CreateCommand(name = "existing"))
    }
}
```

### 2. Quick Compile Check

```bash
# Fastest: IDE inspection (0-2s)
jetbrains.get_file_problems(filePath="...", errorsOnly=True)

# Or: Gradle compile (3-5s)
./gradlew :module-core-domain:compileKotlin
```

### 3. Run Single Test (GREEN)

```bash
# Single test class (~5-10s)
./gradlew :module-core-domain:test --tests "*ServiceTest"

# Or via JetBrains
jetbrains.execute_terminal_command(
    command="./gradlew :module-core-domain:test --tests '*ServiceTest'",
    timeout=60000
)
```

### 4. Refactor

Repeat steps 2-3 until passing, then refactor.

### 5. Final Module Verification

```bash
# After TDD cycle complete, verify module (~15-30s)
./gradlew :module-core-domain:test

# Only use full build for final CI check
./gradlew build  # NO clean unless cache issues!
```

---

## MCP Workflow

```python
# 1. Check file for compile errors (FAST - no build)
jetbrains.get_file_problems(
    filePath="module-core-domain/src/test/kotlin/.../ServiceTest.kt",
    errorsOnly=True
)

# 2. Find existing test patterns
serena.search_for_pattern(
    "@Test|@MockK|@SpringBootTest",
    relative_path="project-basecamp-server/src/test/",
    context_lines_after=1,
    max_answer_chars=3000
)

# 3. Run specific test via JetBrains
jetbrains.execute_terminal_command(
    command="./gradlew :module-core-domain:test --tests '*ServiceTest' --info",
    timeout=60000
)

# 4. Spring testing docs
context7.get-library-docs("/spring/spring-boot", "testing")
```

---

## Test Slice Selection

| Slice | Use When | Loads | Time |
|-------|----------|-------|------|
| None (unit test) | Service/domain logic | Nothing | ~1s |
| `@WebMvcTest` | Controller only | Web layer | ~3-5s |
| `@DataJpaTest` | Repository only | JPA + DB | ~5-10s |
| `@SpringBootTest` | Full integration | Everything | ~10-30s |

**Rule**: Start with unit tests (no slice), add slices only when testing integration points.

---

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

---

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

---

## Anti-Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| `./gradlew clean build` in TDD | 60+ seconds per iteration | Single test: `--tests "*Test"` |
| `@SpringBootTest` for unit tests | Slow, loads everything | Remove annotation |
| Running all tests after each change | Time waste | Run affected test class only |
| `every { } returns` without verify | Mock unused | Add `verify` or use `relaxed` |
| Testing private methods | Brittle tests | Test through public API |
| `Thread.sleep()` in tests | Flaky | Use `awaitility` or latch |

---

## Quality Checklist

- [ ] **Unit tests use no Spring context (fast ~1s)**
- [ ] **Single test runs in <10 seconds**
- [ ] Integration tests use appropriate slice
- [ ] Mocks verified with `verify` blocks
- [ ] Testcontainers for database tests
- [ ] No `Thread.sleep()` (use awaitility)
- [ ] Tests follow AAA pattern (Arrange-Act-Assert)
- [ ] Test names describe behavior: `should X when Y`

---

## Command Reference (Copy-Paste Ready)

```bash
# TDD Fast Feedback (use these!)
./gradlew :module-core-domain:test --tests "*ServiceTest"
./gradlew :module-core-domain:compileKotlin

# Module verification
./gradlew :module-core-domain:test

# Final CI (only when needed)
./gradlew build
./gradlew clean build  # Only if cache issues!
```
