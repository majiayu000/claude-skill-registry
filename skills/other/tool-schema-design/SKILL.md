---
name: tool-schema-design
description: Design and validate model-facing tool definitions with clear names, action-oriented descriptions, bounded JSON Schema parameters, explicit side effects, safe defaults, idempotency, errors, and realistic tests. Use when creating function-calling tools, MCP tools, agent actions, structured tool inputs, or when a model selects the wrong tool, invents arguments, or causes unsafe side effects.
---

# Tool Schema Design

Make the safe, intended call easier for a model to choose than an ambiguous or destructive alternative.

## Use when

- Add or revise a function-calling, MCP, plugin, or internal agent tool.
- Split an overloaded API operation into model-usable actions.
- Reduce wrong-tool selection, malformed arguments, or fabricated fields.
- Document authorization, confirmation, idempotency, and error behavior.

## Inputs

Collect supported user intents, backend operation semantics, required credentials, actor and tenant scope, side effects, reversibility, latency, rate limits, failure modes, and provider-specific schema constraints. Obtain representative valid and invalid requests.

## Output contract

Produce:

1. A tool-boundary decision and overlap analysis.
2. A model-facing name and description with explicit use and non-use conditions.
3. A valid parameter schema with constraints, examples, and unknown-field policy.
4. Side-effect, confirmation, authorization, idempotency, timeout, and error contracts.
5. Positive, boundary, adversarial, and tool-selection tests.
6. Validation results and any provider-specific limitations.

## Workflow

1. Define one coherent user intent per tool. Split tools whose modes have different permissions, side effects, or required fields; avoid tiny tool sets with indistinguishable names.
2. Choose a stable verb-led name. Write the description to say what the tool does, when to call it, when not to call it, and what state it changes.
3. Design parameters from user intent rather than mirroring a backend SDK. Require only indispensable fields, use enums for closed choices, set numeric and length bounds, and describe formats and units. Read [schema-patterns.md](references/schema-patterns.md) for composition and mutation patterns.
4. Reject unknown fields when the runtime supports it. Represent conditional shapes with separate tools or explicit schema branches instead of prose-only dependencies.
5. Keep actor identity, authorization scope, and trusted tenant context server-side. Do not ask the model to supply secrets or claims the runtime already knows.
6. Define execution semantics outside the JSON shape: read-only versus mutating, confirmation level, idempotency key, retry safety, timeout, partial success, and compensating action.
7. Return compact structured results and stable machine-readable error codes. Distinguish invalid input, denied authorization, confirmation required, conflict, rate limit, dependency failure, and unknown failure.
8. Test tool selection against neighboring tools and test execution with valid, omitted, extra, boundary, malicious, and stale inputs.

Use `python3 scripts/validate_tool_schema.py tool.json --strict` before wiring the schema into a runtime. Structural errors always fail. Strict mode also fails on review findings such as free-form command execution, caller-controlled privilege flags, credential parameters, arbitrary URL/path surfaces, permissive unknown fields, and useful missing bounds. `structurally_valid` describes JSON shape only; even `strict_pass: true` is not a semantic safety, authorization, sandbox, provider-compatibility, or implementation certification.

## Safety and permissions

- Enforce authorization in the tool implementation; never rely on the model description as a security boundary.
- Require explicit confirmation for purchases, messages, deployments, deletion, permission changes, or other consequential mutations.
- Do not expose secret parameters, raw credentials, unrestricted shell commands, or arbitrary URLs and file paths unless the use case and sandbox require them.
- Prefer allowlists, scoped identifiers, dry runs, idempotency keys, and reversible operations.
- Treat tool output as untrusted input before placing it back into model context.

## Verification

- Parse and validate the schema with the target provider, not only the bundled structural/heuristic validator or a generic JSON Schema validator.
- Confirm every required field is declared, every enum is reachable, arrays define item shapes, and unknown-field handling matches the implementation.
- Run contrastive prompts that should choose this tool, a neighboring tool, or no tool.
- Verify denied and confirmation-required calls do not perform side effects.
- Compare implementation behavior, returned errors, and documentation for drift.

## Failure handling

- If provider schema features differ, reduce to the supported subset and record the lost constraint in runtime validation.
- If tool selection is ambiguous, sharpen names and descriptions or merge indistinguishable tools; do not depend on prompt ordering.
- If malformed calls persist, simplify nesting, remove redundant fields, and add schema bounds plus server-side validation.
- If a mutation times out, query operation status by idempotency key before retrying.
- If backend behavior conflicts with the contract, fail closed on consequential actions and fix the adapter before release.

## Example

For “let an assistant reschedule a calendar event,” separate event lookup from mutation; name the mutation `reschedule_calendar_event`; require an opaque event ID, timezone-aware start and end timestamps, and an idempotency key; keep account identity server-side; reject unknown fields; require confirmation when attendees will be notified; return a preview or updated event plus a stable status; and test missing timezone, end-before-start, stale event, unauthorized calendar, duplicate retry, and nearby “create event” prompts.
