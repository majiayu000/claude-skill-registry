---
name: shipping
description: 'Use when deploying to production, planning a feature release, setting up launch safeguards, or running a canary release to promote or roll back with evidence. Branches on mode: plan-only produces a verified deployment plan; execute-rollout drives the staged rollout with health-signal gating and automatic halt on degradation. Not for local dev deploys or deploys without a confirmed rollback plan.'
disable-model-invocation: true
---

# Shipping

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User needs to safely deploy a change to production or plan its release safeguards. |
| Authority | Human-only: require explicit human invocation and confirmation before any irreversible deployment action. |
| Side effect | Drives the deployment or rollout sequence and verification; no durable files of its own. |
| Done | Plan mode: a verified deployment plan is produced. Execute mode: a completed rollout with all thresholds green, or a stopped and rolled-back deployment. |

## Inputs

- Deployment target (required): the environment, host, or platform being deployed to.
- Change scope (required): the artifact, commit, image, or changeset being shipped.
- Rollback plan (required): the documented procedure to revert the change. Must be executable without external tooling that may be unavailable during an incident.
- Health signal metrics (required): the metrics and alert thresholds active during rollout. Each metric must have a healthy band and an unhealthy threshold.
- Mode (required): plan-only or execute-rollout.
- Rollout strategy (optional): the staged rollout percentage or canary schedule. In plan mode, this is part of the plan output.

## Procedure

1. Determine mode: plan-only or execute-rollout. Done when: the mode is confirmed by the human.
2. Validate the rollback plan and verify the deployment artifact. Confirm the rollback plan's first step is independently executable. Confirm the artifact is present, named, and its integrity can be verified. Done when: the rollback plan is validated and the artifact is verified.
3. **Plan mode**: produce the deployment plan containing the change scope, rollback procedure, rollout strategy with staged thresholds, health signal metrics with thresholds, and the halt conditions. Done when: the plan is produced and verified.
4. **Execute mode**: present the full change scope and the irreversible consequences to the human before any deployment action. Done when: the human confirms after seeing the scope and consequences.
5. **Execute mode**: drive the staged rollout. Do not advance to the next threshold without confirmed health signals. For a canary strategy: deploy the canary revision at the supplied traffic slice, watch the named metrics over the watch window, classify against thresholds (healthy if every metric stays within its healthy band for the whole window; unhealthy if any metric crosses its unhealthy threshold), and promote or roll back with the collected metric evidence. Done when: all staged thresholds are confirmed green.
6. **Execute mode**: automatically halt and surface a named failure at the first non-green health signal. Do not proceed past a failure. On rollback trigger or human request, execute the documented rollback procedure verbatim. Done when: the failure is named and the rollout is stopped, or the rollback is executed.
7. Report the final state: successful rollout with thresholds verified, rollback completed, or the verified deployment plan. Done when: the final state is reported.

## Failure and recovery

- Rollback plan invalid: stop. Do not deploy. Return "rollback plan not confirmed" with the specific defect.
- Artifact missing: stop. Return "artifact not available" with the target identifier.
- Human rejects preview: stop. No deployment action occurs. Return "preview rejected".
- Health signal degradation during rollout: stop rollout. Do not advance. Return "rollout stopped: unhealthy signal" with the signal name and value. Execute rollback if the human requests it.
- Indeterminate metrics at window end (canary): do not promote. Record the indeterminate classification and evidence. Require a human decision before promote or rollback.
- Metric source unavailable during watch window: do not promote on absent data. Roll back to the previous stable revision and record that the decision was forced by unavailable checks.
- Partial result: never report done when rollout is incomplete or rollback is not confirmed.

## Output

A deployment state report: `rolled out` (all staged thresholds confirmed green, rollback plan verified), `rolled back` (rollback executed, prior state confirmed or explicitly accepted by human), `blocked` (named failure reason, no state change occurred), or `plan produced` (plan mode: the verified deployment plan with change scope, rollback procedure, rollout strategy, and health signal thresholds).
