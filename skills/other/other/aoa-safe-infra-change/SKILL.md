---
name: aoa-safe-infra-change
scope: risk
status: evaluated
summary: Make bounded infrastructure or configuration changes with explicit risk framing, verification, and reversible execution discipline.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-PENDING-SAFE-INFRA-CHANGE
  - AOA-T-0001
---

# aoa-safe-infra-change

## Intent

Use this skill to shape infrastructure, service, configuration, or operational changes into a safer bounded workflow.

## Trigger boundary

Use this skill when:
- the task changes infrastructure, services, configuration, orchestration, or operational surfaces
- the change has runtime, safety, or deployment implications
- the task needs stronger verification and rollback thinking than a normal code edit

Do not use this skill when:
- the task is a purely local code change with no operational implications
- a more specific risk skill should be used instead
- the operator has not provided enough authority for the requested action
- the main question is whether authority exists at all; use `aoa-approval-gate-check`
- the main need is to prefer or interpret a preview path before execution; use `aoa-dry-run-first`

## Inputs

- target change
- touched operational surfaces
- stated authority or approval state
- validation path
- rollback idea

## Outputs

- explicit risk-aware plan
- bounded infrastructure or config change, or bounded execution recommendation
- verification result
- report with remaining risk notes

## Procedure

1. identify the operational surface and main risk
2. confirm whether the change belongs to a high-risk or explicit-only category
3. keep the change small and reviewable
4. avoid unrelated cleanup or hidden expansion of scope
5. verify the result using the strongest practical bounded checks available
6. report what changed, what was verified, and what remains risky or deferred

## Contracts

- infrastructure changes should stay explicit and reviewable
- risk should be named before apply, not after failure
- verification should be stronger than symbolic confidence
- rollback thinking should exist before execution

## Risks and anti-patterns

- treating infra edits like ordinary code edits
- making broad config or orchestration changes under a narrow task label
- relying on weak verification for changes with real runtime impact
- skipping explicit risk framing because the diff looks small

## Verification

- confirm the operational surface was named clearly
- confirm the change stayed bounded
- confirm verification was explicit and proportional to the risk
- confirm rollback or recovery thinking was present before execution or recommendation
- confirm the report includes unresolved risk or recovery notes

## Technique traceability

Manifest-backed techniques:
- AOA-T-PENDING-SAFE-INFRA-CHANGE from `8Dionysus/aoa-techniques` at `TBD` using path `TBD` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0001 from `8Dionysus/aoa-techniques` at `ea49abf4f7e96506feed56eb87a9052cbe4408a5` using path `techniques/agent-workflows/plan-diff-apply-verify-report/TECHNIQUE.md` and sections: Intent, Outputs, Contracts, Risks, Validation

## Adaptation points

Future project overlays may add:
- local risk classifications
- approval rules
- preferred validation commands
- rollback or recovery expectations
