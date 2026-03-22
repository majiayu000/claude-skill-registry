---
name: aoa-port-adapter-refactor
scope: core
status: evaluated
summary: Refactor code toward clearer ports and adapters so reusable logic is less entangled with infrastructure details.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-PENDING-PORT-ADAPTER-REFACTOR
---

# aoa-port-adapter-refactor

## Intent

Use this skill to separate domain or application logic from concrete infrastructure details by introducing or clarifying ports and adapters.

## Trigger boundary

Use this skill when:
- business or domain logic is tightly coupled to a concrete dependency
- tests are hard to write because external concerns leak into the core logic
- the same dependency pattern is beginning to repeat across modules
- a module needs a clearer seam before further change

Do not use this skill when:
- the task is a tiny local fix with no architectural pressure
- there is no meaningful boundary to clarify yet
- the code would become more ceremonial than useful after extraction
- the main problem is deciding whether logic belongs in the core or at the edge; use `aoa-core-logic-boundary` first
- the main problem is clarifying repository docs or source-of-truth ownership; use `aoa-source-of-truth-check` first

## Inputs

- target module or slice
- concrete dependency that currently leaks into the core logic
- desired scope of refactor
- validation expectations

## Outputs

- clearer boundary between logic and infrastructure
- proposed or implemented port shape
- proposed or implemented adapter shape
- verification summary

## Procedure

1. identify the concrete dependency that is making change or testing harder
2. isolate the reusable logic from the infrastructure-specific behavior
3. define a narrow port around what the core actually needs
4. move infrastructure-specific behavior behind an adapter or equivalent seam
5. keep the refactor bounded and avoid unrelated cleanup
6. verify that the new boundary improves clarity and does not silently change behavior

## Contracts

- the extracted boundary should reduce coupling, not add decorative abstraction
- the port should stay narrow and purpose-shaped
- the refactor should not widen into a hidden rewrite
- the final result should remain understandable to another human or agent

## Risks and anti-patterns

- introducing empty abstractions with no real boundary value
- extracting a port that mirrors an overgrown concrete dependency instead of narrowing it
- using the refactor as a pretext for unrelated architectural churn
- making tests more indirect without improving clarity

## Verification

- confirm the concrete dependency pressure was real
- confirm the new boundary is narrower and clearer than before
- confirm behavior did not drift silently
- confirm the refactor stayed inside the declared scope

## Technique traceability

Manifest-backed techniques:
- AOA-T-PENDING-PORT-ADAPTER-REFACTOR from `8Dionysus/aoa-techniques` at `TBD` using path `TBD` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

Future project overlays may add:
- local architecture conventions
- preferred adapter locations
- local test commands
- repository-specific review rules
