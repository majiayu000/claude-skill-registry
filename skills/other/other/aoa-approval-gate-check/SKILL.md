---
name: aoa-approval-gate-check
scope: risk
status: evaluated
summary: Classify whether a requested action should proceed, wait for explicit approval, or be refused at the current authority level.
invocation_mode: explicit-only
technique_dependencies:
  - AOA-T-PENDING-APPROVAL-GATE-CHECK
---

# aoa-approval-gate-check

## Intent

Use this skill to determine whether a task crosses an approval boundary and what should happen before any execution proceeds.

## Trigger boundary

Use this skill when:
- a task may be destructive, operationally sensitive, or security-relevant
- the current authority level is unclear
- the agent needs to classify whether the next step is safe, explicit-only, or out of bounds

Do not use this skill when:
- the task is clearly low-risk and already bounded by an ordinary workflow
- no meaningful approval boundary exists in the current context
- the authority is already clear and the main need is choosing a preview path before execution; use `aoa-dry-run-first`
- the task is only about preparing a public-safe artifact for sharing; use `aoa-sanitized-share`

## Inputs

- requested action
- touched surfaces
- known approval state
- risk signals
- possible fallback or inspect-only path

## Outputs

- classification of the action: safe to proceed, explicit approval required, or do not execute
- note on whether explicit approval is needed
- bounded next-step recommendation
- report of unresolved authority assumptions

## Procedure

1. identify the requested action and touched surfaces
2. assess whether the action could be destructive, sensitive, or authority-gated
3. classify the action as safe to proceed, explicit-approval required, or not appropriate to execute
4. prefer inspect-only or bounded alternatives when authority is insufficient
5. report the classification and the reason for it

## Contracts

- unclear authority should not be silently interpreted as permission
- classification should be explicit and reviewable
- safer bounded alternatives should be preferred when possible
- the result should reduce accidental overreach

## Risks and anti-patterns

- assuming approval because a task sounds routine
- collapsing several risk levels into a single vague warning
- using approval logic to avoid useful bounded analysis
- hiding destructive steps behind innocent labels

## Verification

- confirm the touched surfaces were identified
- confirm the approval need was classified explicitly rather than as a vague warning
- confirm the next step fits the stated authority level
- confirm uncertainty was not masked as permission

## Technique traceability

Manifest-backed techniques:
- AOA-T-PENDING-APPROVAL-GATE-CHECK from `8Dionysus/aoa-techniques` at `TBD` using path `TBD` and sections: Intent, When to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

Future project overlays may add:
- local authority models
- local risk categories
- approval examples
- repository-specific explicit-only rules
