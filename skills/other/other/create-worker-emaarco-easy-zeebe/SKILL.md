---
name: create-worker
argument-hint: "[<path-to-ProcessApi-or-BPMN-file>] [task-type-constant]"
allowed-tools: Read, Write, Glob
description: Create or update a `@JobWorker` class (inbound Zeebe adapter) for a BPMN service task. Use when the user says "create a worker", "generate a job worker", or "scaffold an inbound Zeebe adapter". Accepts a ProcessApi file, a BPMN model, or a plain description; supports both Kotlin and Java; updates existing workers if one already exists.
---

# Skill: create-worker

Generates one `@Component` `@JobWorker` (inbound adapter) class for the specified service task — the boundary where the
process engine calls into your application. See [`references/about.md`](references/about.md) for background.
To generate workers for multiple service tasks, invoke this skill once per task.

## Pattern

```kotlin
@Component
class YourWorker(private val useCase: YourUseCase) {
    private val log = KotlinLogging.logger {}

    @JobWorker(type = TaskTypes.CONSTANT)
    fun handle(@Variable id: UUID): Map<String, Any> {
        useCase.execute(DomainType(id))
        return mapOf(Variables.OUTPUT to value)
    }
}
```

See `references/worker-template.kt` for all variants (void, return, dynamic output).

## IMPORTANT

- `@JobWorker(type = ...)` must reference `ProcessApi.TaskTypes.CONSTANT` — not a hardcoded string
- Inject the use-case interface as the only constructor parameter
- Never depend on the Camunda SDK in the constructor
- Use `@Variable` by default to get process variables
- Switch to `@VariableAsType` only when many variables are needed

## Instructions

### Step 1 – Load Required Files

The goal of this step is to locate and read both the BPMN process model and the ProcessApi file.
Do not extract any content yet — just load the files.

Based on `$ARGUMENTS`:

- If a `.bpmn` file path is provided: read it as the process model. Then search for the ProcessApi file in the same
  service module (`Glob **/adapter/process/*ProcessApi.{kt,java}`).
- If a ProcessApi (`.kt` or `.java`) file path is provided: read it directly. Then search for the BPMN file in the same
  service module (`Glob **/bpmn/*.bpmn`).
- If a task type constant or plain description is provided: search for BPMN files (`Glob **/bpmn/*.bpmn`) and ProcessApi
  files (`Glob **/adapter/process/*ProcessApi.{kt,java}`). Match by name where possible; otherwise list results and ask
  the user to pick.
- If no arguments are provided: Glob `**/bpmn/*.bpmn` and `**/adapter/process/*ProcessApi.*` across the codebase. List
  results and ask the user to select.

**Interrupt if:**

- Neither the BPMN file nor the ProcessApi can be found — ask the user to provide the missing path manually.
- Multiple candidates are found without a clear match — list them and ask the user to select one.

### Step 2 – Identify the Task

The goal of this step is to identify the exact task and its input/output parameters.
The **BPMN is the source of truth** for task type values and variable mappings; the ProcessApi is used only to resolve
the matching Kotlin constant for code generation.

**From the BPMN (source of truth):**

- List all service tasks that have a `<zeebe:taskDefinition>` element.
- If a task type was provided in `$ARGUMENTS`, select the matching service task. Otherwise present the list and ask the
  user to select one.
- From the selected service task extract:
    - The task type string value from `<zeebe:taskDefinition type="...">` — this is the authoritative task type
    - `<zeebe:input>` mappings → the task's **input parameters** (will become `@Variable` parameters)
    - `<zeebe:output>` mappings → the task's **output parameters** (drive the return type and `mapOf(...)` keys)

**From the ProcessApi (for code generation only):**

- Extract the package name, object/class name, and the file extension (`.kt` → Kotlin, `.java` → Java).
- Find the `TaskTypes.*` constant whose value matches the task type string extracted from the BPMN — this constant is
  used in the `@JobWorker(type = ...)` annotation.
- Extract all `Variables.*` constants (used when referencing output variable names in code).

### Step 3 – Determine Worker Location

- Convert the task type string to PascalCase and append `Worker` to derive the class name (e.g.
  `NEWSLETTER_SEND_WELCOME_MAIL` → `SendWelcomeMailWorker`).
- Derive the base package from the ProcessApi package (e.g. `io.miragon.example.adapter.process` →
  `io.miragon.example`):
    - Worker package: `<base>.adapter.inbound.zeebe`
    - Source root: derived from the ProcessApi file path (e.g. `services/example-service/src/main/kotlin/`)
    - Expected target file: `<source-root>/<package-path>/<WorkerName>.kt`
- Check whether the file exists at the expected path. If not found there, Glob `**/<WorkerName>.kt` within the same
  service module to check whether it exists elsewhere.

### Step 4 – Identify Use Case

Search `**/application/port/in/**/*UseCase.kt` (or `.java`) for an interface whose name matches the selected task type.

- If exactly one match is found, use it.
- If multiple matches are found, list them and ask the user to select.
- If no match is found, interrupt and ask the user to provide the use-case interface name manually.

### Step 5 – Generate or Update Worker

Pick the reference template based on the language detected in Step 1:

- **Kotlin** → `references/worker-template.kt`
- **Java** → `references/worker-template.java`

**If the file does not exist — generate:**

- `@Component` class with the constructor parameter for the use-case resolved in Step 4
- `@JobWorker(type = TaskTypes.THE_CONSTANT)` on the `handle` method
- `@Variable` parameters derived from the BPMN input mappings identified in Step 2; use `@VariableAsType` only when a
  typed class already exists or many variables are needed — both from `io.camunda.client.annotation`
- Logger: `KotlinLogging.logger {}` (Kotlin) / `LoggerFactory.getLogger(WorkerName.class)` (Java)
- Scan `**/domain/` for an existing value object matching each input variable (e.g. `NEWSLETTER_ID` → `NewsletterId`).
  **Never** leave a `TODO` for domain-type substitution — resolve or create the type.
- **Return type rule**: if the BPMN output mappings from Step 2 are non-empty, use `Map<String, Any>` and
  `return mapOf(Variables.CONSTANT to value)`. Otherwise omit the return type (`Unit` / `void`). Use the dynamic-output
  variant from the template when the map contents depend on the use-case result.

**If the file already exists — update:**

Read the existing file. Compare it against the expected structure. Apply only what is missing or outdated:

- correct the `@JobWorker` type reference if stale
- align variable injection with the BPMN input mappings
- preserve any existing use-case delegation logic

### Step 6 – Report

Report the file created, updated, or skipped (if nothing changed) and remind the developer to:

1. Verify the worker package is within the Spring component-scan base package (automatic if it is under the
   application's base package)
2. Run `/test-worker` to generate a unit test for the worker
3. Call `/create-worker` again for any remaining service tasks
