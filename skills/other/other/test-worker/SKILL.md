---
name: test-worker
argument-hint: "<path-to-worker-file>"
allowed-tools: Read, Write, Glob, Bash(./gradlew *)
description: Generate a unit test for a Zeebe `@JobWorker` class using mockk (Kotlin) or Mockito (Java), without any Spring context or Camunda test runtime. Use when the user asks to "write tests for a job worker", "generate tests for a worker", or "test a @JobWorker".
---

# Skill: test-worker

Generate a new unit test or update an existing one for a Zeebe job worker class.
This skill follows the project's established test patterns.

## IMPORTANT

- No Spring context, no Camunda test runtime in worker unit tests
- Mirror the test to the package-path of the worker file
- **Kotlin**: use `mockk` / `io.mockk.*`; always call `confirmVerified(useCase)` after every `verify` block
- **Java**: use Mockito (`@ExtendWith(MockitoExtension.class)`, `@Mock`, `@InjectMocks`); call
  `verifyNoMoreInteractions(useCase)` after every `verify`
- By default, write only **one** test case; ask for permission before writing more
- Structure each test with `// Given`, `// When`, `// Then` section comments; omit the comment when that phase is a
  single line

## Pattern

```kotlin
class YourWorkerTest {
    private val useCase = mockk<YourUseCase>()
    private val underTest = YourWorker(useCase)

    @Test
    fun `should perform action when job is received`() {
        // Given
        val variableId = UUID.fromString("123e4567-e89b-12d3-a456-426614174000")
        every { useCase.method(DomainType(variableId)) } just Runs
        // When
        underTest.handle(variableId)
        // Then
        verify(exactly = 1) { useCase.method(DomainType(variableId)) }
        confirmVerified(useCase)
    }
}
```

### Output-variable worker

Use this variant when `handle` returns `Map<String, Any>`.
Capture the result and assert the map entries:

```kotlin
    @Test
fun `should return output variable when job is received`() {
    // Given
    val variableId = UUID.fromString("123e4567-e89b-12d3-a456-426614174000")
    every { useCase.method(DomainType(variableId)) } returns expectedValue
    // When
    val result = underTest.handle(variableId)
    // Then
    verify(exactly = 1) { useCase.method(DomainType(variableId)) }
    confirmVerified(useCase)
    assertThat(result).containsExactly(entry(Variables.CONSTANT, expectedValue))
}
```

See `references/worker-test-template.kt` for the full annotated example.

## SDK Context

This project uses:

- **Production**: `io.camunda:camunda-spring-boot-starter` — annotations from `io.camunda.client.annotation` (
  `@JobWorker`, `@Variable`, `@VariableAsType`)
- **Testing**: `io.camunda:camunda-process-test-spring` — test utilities from `io.camunda.process.test.api` (used in
  process integration tests, not in worker unit tests)

Worker unit tests use `io.mockk` only — no Camunda test runtime is needed.
If you encounter imports or usage patterns not covered by this skill,
ask the user before proceeding how to handle it and whether to add it to the skill.

## Instructions

### Step 1 – Read and identify

Read the worker file at `$ARGUMENTS` and extract:

- **Language**: derive from the file extension — `.kt` → Kotlin (mockk), `.java` → Java (Mockito)
- Worker class name & use-case to be called by the worker
- Variable injection style:
    - **`@Variable param: Type`** — injects one variable by name; the test calls `handle(value)` with the raw value
    - **`@VariableAsType variables: MyVarsClass`** — injects all variables as a typed object; the test instantiates
      the class and passes it, e.g. `handle(MyVarsClass(subscriptionId = subscriptionId))`
- The `@JobWorker`-annotated `handle` method signature
- The **return type** of `handle`:
    - `Unit` (or no explicit return type) → **void worker**: no result assertion needed
    - `Map<String, Any>` → **output-variable worker**: capture `val result = underTest.handle(...)` and assert the
      returned map in the Then block
- The use-case method called inside `handle` and its parameter types
- Domain wrapper types used (e.g. `SubscriptionId`)
- Error Handling: If the file at `$ARGUMENTS` cannot be read, stop immediately and ask the user for the correct path.

### Step 2 – Locate the use-case interface

Every worker must delegate to a use-case:

- Derive the interface name from the constructor parameter identified in Step 1
- Glob for `**/<InterfaceName>.kt` (Kotlin) or `**/<InterfaceName>.java` (Java) under the `src/main` source tree
- If found, read it to confirm the method signature matches what Step 1 identified
- If not found, search more broadly (`**/*UseCase.kt` / `**/*UseCase.java`) and present the user with a numbered
  list of candidates
- If no use-case can be found at all, **stop** and ask the user to provide the path manually before continuing

### Step 3 – Locate the test file

- Mirror the path: replace `src/main/kotlin` → `src/test/kotlin` (Kotlin) or `src/main/java` → `src/test/java` (
  Java), keeping the same package structure
- Append `Test` to the class name (e.g. `FooWorker` → `FooWorkerTest`)
- If the file already exists, open it and switch to fix mode; if not, proceed to generate a new file

### Step 4 – Determine required test cases

Normally one test per distinct happy-path behavior.

- If the worker calls the use case conditionally or has multiple code paths, list the cases and ask for permission
  before writing more than one.

### Step 5 – Generate or fix the test file

- Pick the reference template based on the language detected in Step 1
- **Kotlin** → `references/worker-test-template.kt` (mockk)
- **Java** → `references/worker-test-template.java` (Mockito)
- Write the test case(s) based on the template
- In both cases, don't use tests with spring-context and use fixed uuid strings

### Step 6 – Write, run, and report

- Write the test file to the located path
- Run all tests in the class via an appropriate Gradle command
- Report the created or updated file path and a brief summary