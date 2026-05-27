---
name: create-process-adapter
argument-hint: "[<path-to-ProcessApi-or-BPMN-file>]"
allowed-tools: Read, Write, Glob
description: Create or update a Zeebe process out-adapter (outbound adapter) that calls the process engine via `startProcess`, `sendMessage`, and `sendSignal`. Use when the user asks to "create a process adapter", "generate the outbound Zeebe adapter", "wire up the process port", or "add a process out-adapter for a BPMN process". Accepts a ProcessApi file, a BPMN model, or a plain description; updates existing adapters by adding missing methods and correcting stale constant references.
---

# Skill: create-process-adapter

Generates or updates one process out-adapter class in `adapter/outbound/zeebe/` — the **outbound adapter** where your
application calls the process engine (start process, send message, trigger signal). See [
`references/about.md`](references/about.md) for background.

Generated/updated methods cover:

- `startProcess` (using `PROCESS_ID`)
- methods per message in `Messages.*` (using `sendMessage`)
- methods per signal in `Signals.*` (using `sendSignal`), if present

If the adapter file already exists, the skill compares it to the ProcessApi and adds any missing methods or corrects
outdated constant references.

## IMPORTANT

- All string constants must come from the ProcessApi — never use raw string literals
- `startProcess(processId = ...)` must reference `ProcessApi.PROCESS_ID`
- `sendMessage(messageName = ...)` must reference `ProcessApi.Messages.CONSTANT`
- always pass `correlationId` to correlate the message with the right process instance
- Variable keys in `startProcess` must reference `ProcessApi.Variables.CONSTANT`
- Method names come from the outbound port interface
- Method signatures must accept **domain types** (not raw `String` or `UUID`). Inside the method body, extract
  the primitive with `.value.toString()` (or `.value`) before passing to `engineApi`.

## Pattern

```kotlin
@Component
class YourProcessAdapter(private val engineApi: ProcessEngineApi) : YourProcess {

    override fun startSomething(id: YourId) {
        engineApi.startProcess(
            processId = ProcessApi.PROCESS_ID,
            variables = mapOf("test" to id.value.toString())
        )
    }

    override fun sendSomething(id: YourId) {
        engineApi.sendMessage(
            messageName = ProcessApi.Messages.CONSTANT,
            correlationId = id.value.toString()
        )
    }
}
```

See `references/process-adapter-template.kt` for the full annotated example.

## Instructions

### Step 1 – Resolve the input source

Determine where the process constants come from based on `$ARGUMENTS`:

- **ProcessApi file (`.kt`)**: read it directly. Extract: package name, object name, `PROCESS_ID`, all `Messages.*`
  constants, all `Signals.*` constants (if present), all `Variables.*` constants.
- **BPMN file (`.bpmn`)**: search the same service module for a `*ProcessApi.kt` file
  (Glob `**/adapter/process/*ProcessApi.kt`). If found, read it as above. If not found, ask the user whether to
  continue without type-safe constants.
- **No argument / plain description**: search the whole codebase for `*ProcessApi.kt` files
  (Glob `**/adapter/process/*ProcessApi.kt`). List them and ask the user which one to use.

### Step 2 – Determine the target package and source root

Derive the base package from the ProcessApi package (e.g. `io.miragon.example.adapter.process` → base:
`io.miragon.example`). Adapter package: `<base>.adapter.outbound.zeebe`.

Determine the source root path from the ProcessApi file path (e.g. `services/example-service/src/main/kotlin/`).

### Step 3 – Generate or update the process out-adapter

Derive the adapter class name from the ProcessApi object name (e.g.
`NewsletterSubscriptionProcessApi` → `NewsletterSubscriptionProcessAdapter`).

Check whether a file with that name already exists at the target location.

**If the file does not exist — generate:**

- Use `references/process-adapter-template.kt` as a starting point
- Method signatures accept domain types;
- extract `.value.toString()` for the variables map
- Wire in the outbound port interface once one exists

**If the file already exists — update:**

Read the existing file. Compare each public method against the ProcessApi constants.

Add methods for any `Messages.*` not yet represented.
Correct any constant references that are stale or use raw strings.
Preserve existing method bodies and any added behavior.

### Step 4 – Report

List each file created, updated, or skipped (if nothing changed) and remind the developer to:

1. Wire in the outbound port interface if one exists (add `: ProcessNameProcess` and `override` to each method)
2. Run `/test-process-adapter` to generate unit tests for the adapter

If anything is unclear — for example, multiple ProcessApi files are found or no outbound port interface exists — ask the
user before generating any file.
