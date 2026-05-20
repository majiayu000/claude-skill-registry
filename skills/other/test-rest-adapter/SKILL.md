---
name: test-rest-adapter
argument-hint: "<path-to-controller-file>"
allowed-tools: Read, Write, Edit, Glob, Bash(./gradlew *)
description: Generate Kotlin tests using `@WebMvcTest`, `MockMvc`, and `@MockkBean` for a Spring REST controller. Use when the user asks to "write tests for a REST controller", "add MockMvc tests", "generate a @WebMvcTest", "fix an existing @WebMvcTest", or "update the controller test".
---

# Skill: test-rest-adapter

Generate or fix a test for a REST controller using `@WebMvcTest` with `MockMvc` and `@MockkBean`.

## Pattern

`@WebMvcTest` loads only the web layer (no full Spring context, no JPA, no Zeebe).
Use-case dependencies are replaced with `@MockkBean` from `com.ninjasquad.springmockk`.

```kotlin
@WebMvcTest(YourController::class)
class YourControllerTest {
    @Autowired
    private lateinit var mockMvc: MockMvc

    @MockkBean
    private lateinit var useCase: YourUseCase
    private val mapper = ObjectMapper()

    @Test
    fun `user performs action`() {
        // given: valid request body and stubbed use case
        every { useCase.method(any()) } returns resultId
        // when: the request is performed
        val response = mockMvc.perform(
            post("/api/path")
                .contentType(APPLICATION_JSON).content(mapper.writeValueAsString(input))
        ).andReturn()
        // then: the use case is called with the exact command and the response is correct
        verify { useCase.method(expectedCommand) }
        confirmVerified(useCase)
    }
    // Path-variable variant: stub just Runs, no mapper, verify exact domain-id object
}
```

See `references/rest-controller-test-template.kt` for the full annotated example.

## IMPORTANT

- `@WebMvcTest(ControllerClass::class)` — web slice only; no JPA, no Zeebe
- `@MockkBean` for every use-case / adapter dependency
- `private val mapper = ObjectMapper()` — serialize request bodies via ObjectMapper, not inline strings
- **Test method names are business-oriented**: describe what the user/use-case achieves
  (e.g. `` `user subscribes to newsletter` ``), never HTTP mechanics
- Structure each test with `// given: <what is set up>`, `// when: <the action>`, `// then: <what is verified>`
  sections; omit the section comment when that phase is a single line
- Stub use-case with `any()` in `every { … }`, then verify the **exact command object** in `verify { … }`
- Use `andReturn()` and assert on `response.response.status` and `response.response.contentAsString` with AssertJ
- `confirmVerified(useCase)` — detect unexpected calls
- Value-type IDs with a `String` secondary constructor (e.g. `SubscriptionId("uuid-string")`) can be used directly
- One test per endpoint — happy path only unless error behaviour is explicit in the controller

## Instructions

### Step 1 – Read and identify

Read the controller file at `$ARGUMENTS` and extract:

- Controller class name, base `@RequestMapping` path, and each endpoint (`@GetMapping`, `@PostMapping`, etc.)
- For each endpoint: HTTP method, sub-path, `@RequestBody` / `@PathVariable` / `@RequestParam` parameters,
  return type
- Injected use-case / adapter dependencies (constructor parameters)

If `$ARGUMENTS` is empty or the file cannot be read, stop and ask the user to provide the controller path.

### Step 2 – Locate the test file

- Derive the test file path by replacing `src/main/kotlin` with `src/test/kotlin` in the controller file path.
- Keep the same package structure and class name, but append `Test` as a suffix (e.g. `NewsletterController` →
  `NewsletterControllerTest`).
- If the test file already exists at that path, open it and switch to fix mode.
- If it does not exist, proceed to generate a new file in Step 4.

### Step 3 – Determine required test cases

- Write one happy-path test per endpoint.
- Add an error-case test only when the controller explicitly handles a failure scenario (e.g. returns a specific status
  code on failure).
- If additional cases apply, list them and ask the user for permission before writing more than one test per endpoint.

### Step 4 – Generate or fix the test file

- Use `references/rest-controller-test-template.kt` as a starting point
- Stub use-case with `any()` in `every { }`, verify the **exact** command object in `verify { }`
- Fixed UUID strings for deterministic test data

### Step 5 – Write, run, and report

- Write the file to the located path
- Run all tests in the class via an appropriate Gradle command;
- Report the created or updated file path and a brief summary.
