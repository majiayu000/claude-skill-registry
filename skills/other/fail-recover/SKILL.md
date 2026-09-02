---
name: fail-recover
description: 'Use when the user needs to restore service from a specific known failure by applying a single prescribed recovery operation. Verifies the symptom, validates the prescription against its authority source, records the rollback path, applies the operation, and confirms restoration via a health signal. Not for design-time failure definition or open-ended debugging.'
---

# Fail recover

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User needs to restore service from a specific known failure using a prescribed recovery operation. |
| Authority | Reversible local writes only. State and follow the rollback path before mutating. Write only the named local target. |
| Side effect | The single prescribed recovery operation applied to the local configuration target. No scope widening, no retry with a different action. |
| Done | The recovery operation is applied to the target artifact and the health signal confirms service restoration. |

## Inputs

Required:

- The known failure symptom: the observable condition that identifies the failure (error message, metric threshold, health-check output).
- The prescribed recovery operation: the single bounded action to apply.
- The authority source for the prescription: where the recovery operation is documented (a runbook, an incident postmortem, a vendor advisory, a playbook entry). Named explicitly so the operation can be validated.
- The target configuration artifact: the local file, setting, or service the operation changes.

Optional:

- An explicit rollback path. If absent, derive and record one before any mutation.
- A health signal or verification mechanism: the command, endpoint, or metric that confirms restoration. If absent, ask the user to name one before applying the operation.

## Procedure

1. Verify the observed symptom matches the known failure. Compare the observed condition against the documented symptom. If they do not match, stop. Done when: the symptom matches the known failure, or the skill stops with the mismatch reported.
2. Validate the prescribed recovery operation against the named authority source. Confirm the operation is the one documented for this failure and that it targets only the named local artifact. If the authority source does not prescribe this operation for this symptom, stop. Done when: the operation is validated as prescribed and scoped to the named target.
3. Record the explicit rollback path that reverses the recovery operation. If the user did not supply one, derive it from the operation's inverse and record it before any mutation. Done when: the rollback path is recorded.
4. Apply the recovery operation to the named local target only. Done when: the recovery operation is applied to the named target.
5. Verify restoration using the specified health signal or verification mechanism. Run the health check, query the endpoint, or read the metric. Done when: the health signal confirms service restoration, or the check fails and rollback is triggered.

## Failure and recovery

- Symptom mismatch: the observed condition does not match the known failure. Stop; apply no recovery operation.
- Invalid prescription: the authority source does not document this operation for this symptom, or the operation targets something other than the named artifact. Stop; apply nothing.
- Health check fails after application: reverse the named local change via the recorded rollback path. Report the remaining symptom, the action taken, and the rollback result. Do not retry with a widened scope or an unvalidated action.
- Missing health signal: if no verification mechanism is named and the user cannot supply one, stop before applying the operation. Restoration cannot be confirmed without a health signal.
- Partial result: no partial application is reported as done. Report what was applied and the remaining failure.
- Rollback: reverse the named local change via the recorded rollback path. Never swallow errors or assert the done predicate when it does not hold.

## Output

Terminal classification: `restored` or `not-restored`. Include the recovery operation applied, the authority source cited, the named local target changed, the rollback path, the health signal used, and the remaining symptom when not restored.
