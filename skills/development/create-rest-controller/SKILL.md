---
name: create-rest-controller
argument-hint: "[<path-to-UseCase-port-file>] [http-verb] [path]"
allowed-tools: Read, Write, Glob
description: Scaffold or update a Spring `@RestController` (inbound adapter) with nested request/response DTOs and a `toCommand()` mapping function. Use when the user asks to "create a REST controller", "add an endpoint", "generate an inbound adapter", or "scaffold a controller". Accepts a use-case port file or a plain description; infers HTTP verb and path from the use-case name; updates existing controllers if one already exists.
---

# Skill: create-rest-controller

Generates or updates one `@RestController` (inbound adapter) for a specific use case in `adapter/inbound/rest/`,
including:

- Nested request and response `data class` DTOs
- A private `toCommand()` extension function for request-to-command mapping

To generate controllers for multiple use cases, invoke this skill once per use case.
If the file already exists, the skill compares it to the expected structure and applies only what is missing or stale.

## Pattern

```kotlin
@RestController
@RequestMapping("/api/resource")
class DoSomethingController(private val useCase: DoSomethingUseCase) {

    @PostMapping("/action")
    fun doSomething(@RequestBody input: Form): ResponseEntity<Response> {
        ...
    }

    data class Form(val field: String)
    data class Response(val id: String)

    private fun Form.toCommand() = DoSomethingUseCase.Command(DomainType(field))
}
```

See `references/rest-controller-template.kt` for the full annotated example.

## IMPORTANT

- One endpoint aka method per controller-class.
- Inject the use-case interface as the **only** constructor parameter
- Wrap all request fields in domain value objects inside `toCommand()` before passing to the use case;
- Always return `ResponseEntity<T>`: use `ResponseEntity<Response>` when the use case returns a value,
  `ResponseEntity<Void>` when it returns `Unit`
- Request/response DTOs are `data class` types nested inside the controller class
- Before writing the controller, scan the `domain/` package for value objects matching each request field.
  Use them in `toCommand()` directly. If a required value object does not exist, ask the user whether you should create
  it first.

## Instructions

### Step 1 – Resolve the input source

Determine which use-case interface to target based on `$ARGUMENTS`:

- **Use-case port file (`.kt`)**: Read it directly and extract the package name, interface name, method signature(s),
  `Command` nested class fields (if present), and return type.

If no argument is passed:

- Search the whole codebase for use-case port files using a Glob `**/application/port/inbound/*UseCase.kt`.
- List the results and ask the user which one to use before continuing.

### Step 2 – Analyze the use-case and controller

Derive the base package from the use-case port package
(e.g. `io.miragon.example.application.port.inbound` → base: `io.miragon.example`).
Controller package: `<base>.adapter.inbound.rest`.

Determine the source root path from the port file path
(e.g. `services/example-service/src/main/kotlin/`).

### Step 3 – Determine the HTTP verb and path

If `$ARGUMENTS` contains a verb and path, use them.

Otherwise, infer defaults from the use-case name:

- Name starts with `Create`, `Subscribe`, `Register`, `Add` → `POST`
- Name starts with `Update`, `Confirm`, `Change` → `POST` (or `PUT` — ask)
- Name starts with `Delete`, `Remove`, `Cancel`, `Abort` → `DELETE` (or `POST` — ask)
- Name starts with `Get`, `Find`, `Search`, `List` → `GET`

Derive a sensible URL path from the use-case name and the domain noun (e.g.
`SubscribeToNewsletterUseCase` → `POST /api/subscriptions/subscribe`).

Ask the user to confirm or adjust the verb and path before generating.

### Step 4 – Generate or update the controller

Derive the controller class name from the use-case interface name by replacing `UseCase` with `Controller`
(e.g. `SubscribeToNewsletterUseCase` → `SubscribeToNewsletterController`).

Check whether a file with that name already exists at the target location.

**If the file does not exist — generate:**

- Use `references/rest-controller-template.kt` as a starting point
- Scan `domain/` for value objects; create missing ones before writing
- Never leave a TODO for domain-type substitution

**If the file already exists — update:**

Read the existing file. Compare it against the use-case interface signature.
Apply only what is missing or outdated:
add missing fields to the request form, update the return type, correct the `toCommand()` mapping.
Preserve any existing logic.

### Step 5 – Report

Report the file created, updated, or skipped (if nothing changed) and remind the developer to:

1. Verify the base path in `@RequestMapping` is consistent with the existing API structure
2. Run `/test-rest-adapter` to generate a unit test for the controller
3. Call `/create-rest-controller` again for any remaining use cases
