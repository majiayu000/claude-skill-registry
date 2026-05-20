---
name: aoa-dry-run-first
scope: risk
status: evaluated
summary: Prefer simulation, inspection, or preview paths before real execution for changes that can have meaningful operational consequences.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-PENDING-DRY-RUN-FIRST
  - AOA-T-0004
---

# aoa-dry-run-first

## Intent

Use this skill to force a preview-first mindset before executing changes that may be destructive, irreversible, or operationally meaningful.

## Trigger boundary

Use this skill when:
- the task can be simulated, previewed, or inspected before real execution
- the action may delete, restore, migrate, reconfigure, or otherwise alter a live surface
- the cost of a mistaken execution is meaningfully higher than the cost of a preview step

Do not use this skill when:
- no meaningful dry-run or preview path exists and the task is already clearly bounded and harmless
- the task is purely analytical and does not approach execution at all
- the central question is whether execution is authorized at all rather than how to preview it; use `aoa-approval-gate-check`
- the task is only about preparing a sanitized artifact for sharing; use `aoa-sanitized-share`

## Inputs

- requested action
- available preview or dry-run mechanisms
- touched surfaces
- known limits of the preview path

## Outputs

- dry-run or preview recommendation
- bounded preview result or plan
- note on what the preview does and does not prove
- recommendation for next step

## Procedure

1. identify whether a preview, simulation, inspect-only, or dry-run path exists
2. prefer the safest bounded preview path before real execution
3. make explicit what the preview covers and what it cannot guarantee
4. avoid treating dry-run output as proof of total safety
5. recommend the next step only after the preview has been interpreted

## Contracts

- dry-run should reduce uncertainty before execution
- preview results should not be overstated
- lack of a dry-run path should be named as a risk, not hidden
- real execution should not be smuggled into a preview step

## Risks and anti-patterns

- treating a preview as complete validation
- skipping preview because the real change looks small
- using a fake or weak preview path that does not touch the real risk surface
- blurring inspect-only and execute behavior

## Verification

- confirm a preview or dry-run path was considered first
- confirm the preview scope was named honestly
- confirm unresolved risk after preview was not hidden
- confirm the preview step did not silently perform the real action
- confirm the recommended next step matches the preview confidence

## Technique traceability

Manifest-backed techniques:
- AOA-T-PENDING-DRY-RUN-FIRST from `8Dionysus/aoa-techniques` at `TBD` using path `TBD` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation
- AOA-T-0004 from `8Dionysus/aoa-techniques` at `fe7df9aba3937435b431489ed0f9c5d52690a37c` using path `techniques/agent-workflows/intent-plan-dry-run-contract-chain/TECHNIQUE.md` and sections: Intent, When to use, Outputs, Core procedure, Validation

## Adaptation points

Future project overlays may add:
- local preview commands
- dry-run limitations
- restore or recovery expectations
- project-specific inspect-only patterns
