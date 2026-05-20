---
name: test-process-adapter
argument-hint: "<path-to-adapter-file>"
allowed-tools: Read, Write, Glob, Bash(./gradlew *)
description: Generate mockk-based unit tests for Zeebe process out-adapters covering `startProcess`, `sendMessage`, and `sendSignal` methods. Use when the user asks to "write tests for a process adapter", "test the outbound Zeebe adapter", or "generate unit tests for a process adapter".
---

# Skill: test-process-adapter

Generate a unit test for a Zeebe process out-adapter following the project's established test patterns.

## SDK Context

This project uses:

- **Production**: `io.camunda:camunda-spring-boot-starter`
- **Wrapper** — `ProcessEngineApi` from `io.miragon.common.zeebe.engine`
- **Testing**: adapter unit tests use `io.mockk` only; no Camunda test runtime needed

If you encounter imports or usage patterns not covered by this skill,
ask the user before proceeding how to handle it and whether to add it to the skill.

## Reference Pattern

```kotlin
class YourProcessAdapterTest {
    private val engineApi = mockk<ProcessEngineApi>()
    private val underTest = YourProcessAdapter(engineApi = engineApi)

    @Test
    fun `starts process`() {
        // given: engine stubbed to return a process instance key
        every { engineApi.startProcess(any(), any()) } returns 42L
        // when: the adapter initiates the process
        val result = underTest.startSomething(id)
        // then: engine called with the correct processId and variables
        verify { engineApi.startProcess(ProcessApi.PROCESS_ID, mapOf(...)) }
        assertThat(result).isEqualTo(42L)
        confirmVerified(engineApi)
    }

    @Test
    fun `sends message`() {
        // given: engine stubbed for message correlation
        every { engineApi.sendMessage(any(), any(), any()) } just Runs
        // when: the adapter sends the message
        underTest.sendSomething(id)
        // then: engine called with the correct messageName and correlationId
        verify { engineApi.sendMessage(ProcessApi.Messages.CONSTANT, id.value.toString(), emptyMap()) }
        confirmVerified(engineApi)
    }
}
```

See `references/process-adapter-test-template.kt` for the full annotated example.

## IMPORTANT

- Structure each test with `// given: <what is set up>`, `// when: <the action>`, `// then: <what is verified>`
  sections; omit the section comment when that phase is a single line
- Use `io.mockk.*` for mocking `ProcessEngineApi`
- Use `org.assertj.core.api.Assertions.assertThat` for return-value assertions
- Use `confirmVerified(engineApi)` at the end of every test to catch unexpected calls
- Import the exact ProcessApi class used in the adapter under test
- All string constants (processId, messageName, variable keys) must come from the ProcessApi object — no raw literals

## Instructions

### Step 1 – Read and identify

Read the adapter file at `$ARGUMENTS` and extract:

- Adapter class name and the outbound port interface it implements (if any)
- The ProcessApi object imported (e.g. `NewsletterSubscriptionProcessApi`)
- Each public method: name, parameters, return type
- Which `ProcessEngineApi` methods are called (`startProcess`, `sendMessage`, etc.)
- Which ProcessApi constants are referenced (PROCESS_ID, Messages.*, Variables.*, etc.)

Then read the ProcessApi file to confirm the exact constant names and nested object structure.

### Step 2 – Locate the test file

Mirror `src/main/kotlin` → `src/test/kotlin`, same package path, append `Test` to the class name.
If the file already exists, open it and switch to fix mode. If not, proceed to generate a new file.

### Step 3 – Determine required test cases

One test per public adapter method.
If a method has multiple code paths, list them and ask for
permission before writing more than one test for that method.

### Step 4 – Generate or fix the test file

- Use `references/process-adapter-test-template.kt` as a starting point
- All string constants from ProcessApi — no raw literals
- Fixed UUID strings for deterministic test data
- Use named parameters for parameters of method calls

### Step 5 – Write, run, and report

- Write the file to the located path;
- Run all tests in the class via an appropriate Gradle command;
- Report the created or updated file path and a brief summary.
