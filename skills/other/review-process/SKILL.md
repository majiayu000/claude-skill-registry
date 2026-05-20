---
name: review-process
user-invocable: false
allowed-tools: Read, Glob, Grep
description: Audit a Zeebe BPMN process and its glue-code (workers, process adapter, tests) for consistency and coverage, producing a structured report written to `.claude/temp/`. Use when the user asks to "review the newsletter process", "audit a BPMN process", "check process consistency", or "use the review-process subagent". Checks task-type coverage, message coverage, ProcessApi consistency, variable coverage, test coverage, and BPMN styleguide compliance.
---

# Skill: review-process

Review a BPMN process model and its glue-code for consistency, coverage, and correctness.
Produce a structured consistency report and write it to a file at the end.

## IMPORTANT

- You are a read-only agent, only reviewing processes.
- Never write anything to a source-file - other than your report
- Write your output to the temp-folder `.claude/temp` in a file `review-<process>.md`
- If the bpmn-model to review could not be found ask the user to provide a concrete path

## Instructions

To perform the review of a process, execute the following steps in order:

### Step 1 – Locate and read the BPMN file

Search for the `.bpmn` file in `src/main/resources/bpmn/` matching the process name given. If you cannot find a file,
ask the user to provide a path to it.

If you found a matching file, read the file and extract:

- **Service task types** (`zeebe:taskDefinition type` attribute values)
- **Message names** (`<bpmn:message name="...">` values)
- **Process variables** referenced in expressions or I/O mappings
- **Process ID** (`<bpmn:process id="...">`)
- **Element IDs** for all service tasks, events, and gateways
- **Timer definitions** and boundary event types

### Step 1b – Read the BPMN styleguide

Read `docs/bpmn-styleguide/styleguide.md`. Extract the conventions for:

- **Element ID format**: `Type_Name` in CamelCase (e.g. `serviceTask_SendWelcomeMail`)
- **Message ID format**: `<serviceName>.<state>` — both parts CamelCase (e.g. `newsletter.subscriptionConfirmed`)
- **Type ID format**: `<serviceName>.<elementIdWithoutTypePrefix>` — both parts CamelCase (e.g.
  `newsletter.sendWelcomeMail`)
- **Naming rules**: tasks (verb + noun), events (noun + past tense), gateways (short question)

If the styleguide does not exist, quit with an according error-message

### Step 2 – Read the ProcessApi file

Locate the ProcessApi file (typically in `adapter/process/`). Read and extract:

- `PROCESS_ID` constant
- All `TaskTypes.*` constants
- All `Messages.*` constants
- All `Variables.*` constants
- All `Elements.*` constants

If you cannot find a ProcessApi, ask the user to provide a path.

### Step 3 – Discover and read workers and tests

Locate all files in `adapter/inbound/zeebe/`. For each worker, identify:

- The `@JobWorker(type = ...)` value and which ProcessApi constant it references
- The `@Variable` parameters used

If none are found this can be a valid output either.
However, mark this in your final report, in case the processModel defines serviceTasks.
In this case, it should be reviewed by the user.

### Step 4 – Read the process out-adapter and tests

Locate the process out-adapter in `adapter/outbound/zeebe/`. For each public method, identify:

- Whether it calls `startProcess` or `sendMessage`
- Which `processId` and `messageName` constants it uses

If none are found this can be a valid output either.
However, mark this in your final report, in case the processModel defines messages.
In this case, it should be reviewed by the user.

### Step 5 – Read the process test

Locate the process integration test (typically in `test/.../adapter/process/`). Identify:

- Which process paths are tested (happy path, timer expiry, abort, etc.)
- Which elements are asserted with `hasCompletedElement`

### Step 6 – Produce the consistency report

Output a structured report with these sections:

**Task Type Coverage**: For each service task in the BPMN, report whether a worker exists. Flag BPMN tasks without a
worker and workers without a BPMN task.

**Message Coverage**: For each message in the BPMN, report whether the process adapter has a corresponding method. Flag
gaps.

**ProcessApi Consistency**: Compare ProcessApi constants against actual BPMN values. Flag mismatches and warn about raw
string literals in workers or adapters.

**Variable Coverage**: List variables used in workers and adapters. Verify they appear in `Variables.*` in the
ProcessApi.

**Test Coverage**: For each identified process path, report whether a test exists that covers it. Also report whether
each worker and process-adapter are covered as well

**Styleguide Compliance**: Check the BPMN model against the conventions loaded in Step 1b:

- For each service task, event, and gateway: verify the element ID matches the `Type_Name` CamelCase pattern
- For each message: verify the message name matches the `<serviceName>.<state>` CamelCase pattern
- For each task type (job type): verify it matches the `<serviceName>.<elementIdWithoutTypePrefix>` pattern
- Flag element IDs that use auto-generated values (e.g. `Activity_0xf83kz`) or that deviate from the convention
- Flag task/event names that do not follow verb+noun (tasks) or noun+past-tense (events) conventions

**Summary**: Overall assessment — ✅ consistent / ⚠️ minor gaps / ❌ significant issues — with actionable next steps.

### Step 7 – Write the report to a file

Determine the output file path as `.claude/temp/<processName>-review.md`, where
`<processName>` is the kebab-case process name derived from the process ID
(e.g. process ID `newsletter-subscription` → file `docs/newsletter-process-review.md`).

Prepend a metadata header to the report:

- `**Date:**` set to today's date
- `**Process file:**` set to the relative BPMN path
- `**Process ID:**` set to the process ID

Write the complete report (header and all sections from Step 6) to the output file.
Confirm the file path to the user.
