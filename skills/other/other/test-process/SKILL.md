---
name: test-process
argument-hint: "<process-name-or-bpmn-path>"
allowed-tools: Read, Write, Glob, Grep, Bash(./gradlew *), AskUserQuestion
description: Generate `@CamundaSpringProcessTest` integration tests for a Zeebe BPMN process, with one `@Test` method per selected process path. Use when the user asks to "write process tests", "generate integration tests for a process", or "test the newsletter process". Analyzes all testable paths (happy path, gateway branches, timer expiry, message events, boundary events), lets the user select which to generate, and supports update mode to append tests to an existing class.
---

# Skill: test-process

Generates a `@CamundaSpringProcessTest` integration test class for a Zeebe BPMN process.
The test class contains one `@Test` method per selected process path.
Such a path could be happy path, gateway branches or boundary events.

To add paths to an existing test class, invoke this skill again.
It will switch to update mode and only append the new test methods.

## IMPORTANT:

- One `@Test` method per distinct process path (happy path, each timer expiry, each message branch, each boundary event)
- Use `@MockkBean` for every use-case interface that a worker injects — these are the collaborators
- Set up all mocks in `@BeforeEach` with `every { useCase.method(any()) } just Runs`
- Use fixed UUID strings for deterministic, reproducible test data — use different UUIDs per test to avoid correlation
  conflicts
- Drive the process via the process adapter (`processPort.*`) not via `camundaClient` directly, except when using
  `startBeforeElement` for mid-process scenarios
- Use `ProcessInstanceSelectors.byKey(instanceKey)` to create the selector for assertions
- Always end each test with `confirmVerified(...)` across all mocked use cases to catch unexpected interactions
- Use `verify { useCase wasNot Called }` for negative assertions (not `verify(exactly = 0) { ... }`)

## Pattern

```kotlin
@CamundaSpringProcessTest
@SpringBootTest
@Import(TestProcessEngineConfiguration::class)
class NewsletterProcessTest {

    @Autowired
    lateinit var processPort: NewsletterSubscriptionProcess

    @MockkBean
    lateinit var subscribeUseCase: SubscribeToNewsletterUseCase

    @BeforeEach
    fun setUp() {
        every { subscribeUseCase.execute(any()) } just Runs
    }

    @Test
    fun `happy path - subscription confirmed`() {
        val instanceKey = processPort.startNewsletterSubscription(NewsletterSubscriptionId("uuid-1"))
        val selector = ProcessInstanceSelectors.byKey(instanceKey)

        CamundaAssert.assertThat(selector).hasCompletedElement("serviceTask_Subscribe")
        verify { subscribeUseCase.execute(any()) }
        confirmVerified(subscribeUseCase)
    }
}
```

See `references/process-test-template.kt` for all variants (timer, message, mid-process start).

## SDK Context

This project uses:

- **Test runtime**: `io.camunda:camunda-process-test-spring` — `@CamundaSpringProcessTest`, `CamundaAssert`,
  `CamundaProcessTestContext`, `ProcessInstanceSelectors` from `io.camunda.process.test.api`
- **Mocking**: `com.ninjasquad.springmockk.MockkBean` (Spring-aware mockk bean replacement)
- **Engine wrapper**: `TestProcessEngineConfiguration` from `io.miragon.common.test.config`

If you encounter imports or usage patterns not covered by this skill, ask the user before proceeding.

## Instructions

### Step 1 – Locate and read the BPMN file

If `$ARGUMENTS` is a file path, read it directly.
If it is a process name, search for `*$ARGUMENTS*.bpmn` in `src/main/resources/bpmn/`.

Read the full BPMN XML and extract **all** the following:

- Process ID (`<bpmn:process id="...">`)
- All service tasks: element ID + `zeebe:taskDefinition type` attribute
- All receive tasks and intermediate message catch events: element ID + referenced message name
- All message definitions: name + correlation key expression
- All timer definitions: element ID, whether boundary or intermediate catch event, attached activity (if boundary),
  duration/cycle expression (e.g. `PT60S`, `R3/PT60S`)
- All exclusive/parallel/inclusive gateways: element ID + outgoing sequence flows with their condition expressions
- All boundary events (error, escalation, non-timer): element ID + `attachedToRef` activity + event type
- All end events: element ID + type (none, error, terminate, escalation) and which gateway branch leads to them

If you cannot find the bpmn-file ask the user to provide a path to it.

### Step 2 – Analyze process paths

Using the data collected in Step 1, derive every distinct testable path in the process.
Do **not** show this analysis to the user. Keep it as an internal working set.

For each path, record:

- **Label** — short display name (e.g. "Happy path", "Timer: registration expires")
- **Description** — which BPMN elements are exercised and what the outcome is
- **Technique** — recommended test technique: `full-start`, `startBeforeElement`, `increaseTime`, `sendMessage`

Derive paths using these four categories:

- **Happy path** — always present; the primary successful flow from start event to the successful end event
- **Gateway branch** — one path per outgoing branch of each exclusive or inclusive gateway that is not already covered
  by the happy path; note the condition that triggers the branch and the resulting end event
- **Boundary event** — one path per boundary event regardless of type (timer, message, error, escalation) and
  regardless of whether it is interrupting or non-interrupting; note the attached activity and where the flow goes
- **Event subprocess** — one path per event subprocess; note the triggering event type and the subprocess end event

### Step 3 – Ask user which paths to test

Present the paths derived in Step 2 to the user using `AskUserQuestion` with `multiSelect: true`.

- Always list "Happy path" first and mark it as "(Recommended)" in its description
- For each other path, include the dominant BPMN element names and the test technique in the description so the user
  understands what will be generated
- Store the selected paths — only generate test methods for these in Step 6

### Step 4 – Read supporting files

#### 4.1 – ProcessApi

- Search for `adapter/process/*ProcessApi.kt` in the same module as the BPMN file.
- If not found, use `AskUserQuestion` to ask the user to provide the path, then read it.
- Extract: `PROCESS_ID`, and all constants under `TaskTypes`, `Messages`, `Variables`, `Elements`.

#### 4.2 – Process adapter

- Search for `adapter/outbound/zeebe/*ProcessAdapter.kt` in the same module.
- If not found, use `AskUserQuestion` to ask the user to provide the path, then read it.
- Note the class name and all public methods (start-process and message-send methods).

#### 4.3 – Workers

- Search for all files matching `adapter/inbound/zeebe/*Worker.kt` in the same module.
- If none are found, that is valid — note the absence and continue.
- For each worker found, note the injected use-case interface (constructor parameter) and any `@Variable` parameters.

#### 4.4 – TestProcessEngineConfiguration

- Search for `TestProcessEngineConfiguration.kt` in the test source tree of the module.
- If not found, stop immediately and inform the user: "TestProcessEngineConfiguration could not be found. This class is required for the `@Import` annotation. Please ensure `common-zeebe-test` is on the test classpath and correct the setup before proceeding."
- If found, note its fully qualified class name for the `@Import` annotation.

### Step 5 – Determine the test file location

Mirror the source layout:

- Module root: derive from the BPMN file path (e.g. `services/example-service/`)
- Test file: `src/test/kotlin/<package-path>/<ProcessName>ProcessTest.kt`
- Package: same as the process adapter package (e.g. `io.miragon.example.adapter.process`)

If a file with that name already exists, switch to **update mode**: add only the new test methods for the paths the
user selected in Step 3, leaving existing methods untouched.

### Step 6 – Generate the test class

Use `references/process-test-template.kt` as your starting point. Generate **only** the test methods for the paths
selected in Step 3. Apply these rules when adapting the template:

- **Happy path** → use the full-start variant; call `processPort.<startMethod>` and optionally
  `processPort.<sendMessageMethod>` if the happy path includes a message
- **Message path** → include the message-send section; use a distinct UUID to avoid correlation conflicts with other
  tests
- **Timer path** → include `processTestContext.increaseTime(Duration.of...)` with the correct duration; start at
  the appropriate element via `startProcessAt` if skipping earlier tasks is needed
- **Mid-process / boundary event path** → use `startProcessAt` with the correct element ID from `ProcessApi.Elements`
- **`startProcessAt` helper** → include the private helper only if at least one selected path uses it
- **`camundaClient` and `processTestContext` fields** → include only when at least one selected path needs them

### Step 7 – Write the test file

Write the generated class to the location determined in Step 5.

### Step 8 – Verify

Run the generated tests using the appropriate Gradle command. Derive the module path from the file location:

```
./gradlew :<module-path>:test --tests "*<ProcessName>ProcessTest*"
```

If tests fail, diagnose the root cause (missing mock setup, wrong element ID, incorrect timer duration) and fix
before reporting.

### Step 9 – Report

Give a short report about which file you have created or updated,
as well as how many test-cases were affected.