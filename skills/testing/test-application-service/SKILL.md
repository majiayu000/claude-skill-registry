---
name: test-application-service
argument-hint: "<path-to-service-file>"
allowed-tools: Read, Write, Glob, Bash(./gradlew *)
description: Generate a pure mockk unit test (no Spring context) for an application-layer use-case service. Use when the user asks to "write tests for an application service", "test a use case", or "generate unit tests for a service". Follows the project's given/when/then pattern with `confirmVerified` after every verify block; uses domain test builders and fixed UUIDs; no Spring context required.
---

# Skill: test-application-service

Generate a unit test for an application service (use case) following the project's established test patterns.

## Pattern

Application service tests are pure unit tests using mockk. No Spring context required.

```kotlin
class YourServiceTest {
    private val port = mockk<SomePort>()
    private val underTest = YourService(port = port)

    @Test
    fun `describe behaviour`() {
        // given: valid input and mocked port behaviour
        every { port.method(any()) } returns value   // or: just Runs
        // when: the use case is executed
        underTest.execute(command)
        // then: the port is called with the expected arguments
        verify { port.method(expected) }
        confirmVerified(port)
    }
}
```

See `references/service-test-template.kt` for the full annotated example (slot capture, multiple mocks).

## IMPORTANT

- Mirror the class from the production-code with just a suffix `Test`
- Instantiate the service directly — no Spring context
- `mockk<Interface>()` for each constructor dependency
- `confirmVerified(mock)` inline at the end of **each** test — not in `@AfterEach`
- Stub Unit-returning methods with `just Runs`; use `returns value` otherwise
- One `@Test` per distinct behaviour (happy path + exception if the service throws)
- Use test builders from `domain/TestObjectBuilder.kt` (e.g. `testNewsletterSubscription()`)
- Fixed UUID strings for deterministic test data
- Structure each test with `// given: <what is set up>`, `// when: <the action>`, `// then: <what is verified>`
  sections; omit the section comment when that phase is a single line
- Backtick test names

## Instructions

### Step 1 – Read and identify

Read the service file at `$ARGUMENTS` and extract:

- Service class name and the use-case interface it implements
- Constructor dependencies (repository interfaces, outbound ports)
- Each public method: signature, what it calls, what it returns or throws
- Domain value types used (e.g. `SubscriptionId`, `NewsletterSubscription`)

If no matching service was found, pause the execution and, ask the user to provide the path to the service

Also locate test builders. Look for functions in the test module and its `domain` package that build objects that are
used in the service.
If none exists, pause the execution as well.
Ask the user to provide or link to the builder(s)

### Step 2 – Locate the test file

- Derive the test file path by replacing `src/main/kotlin` with `src/test/kotlin` in the service file path.
- Keep the same package structure and class name, but append `Test` as a suffix (e.g. `SubscribeToNewsletterService` → `SubscribeToNewsletterServiceTest`).
- If the test file already exists at that path, open it and switch to fix mode.
- If it does not exist, proceed to generate a new file in Step 4.

### Step 3 – Determine required test cases

- Write one happy-path test for each public method of the service.
- Add an exception test only when the service explicitly throws (e.g. `NoSuchElementException`).
- Keep the total number of tests to three or fewer.
- If more scenarios are applicable, list them and ask the user for permission before writing additional tests.

### Step 4 – Generate or fix the test file

- Use `references/service-test-template.kt` as a starting point
- Use test builders from `domain/TestObjectBuilder.kt`; fixed UUID strings
- Backtick test names

### Step 5 – Write, run, and report

- Write the file to the located path;
- Run all tests in the class via an appropriate Gradle command;
- Report the created or updated file path and a brief summary.
