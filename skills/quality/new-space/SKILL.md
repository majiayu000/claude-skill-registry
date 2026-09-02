---
name: new-space
description: 'Use when a user starts a new work session and asks to split human decisions from agent execution. Writes a contract-bound brief under run/<session-id>/ and runs spawn, work, review, and human-gate phases to completion. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# New space

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User starts a new work session and asks to split human decisions from agent execution. |
| Authority | Write only under `run/<session-id>/` and execute only the approved spawn target. Human sign-off remains external to this skill. |
| Side effect | Five artifacts under `run/<session-id>/`: brief, spawn evidence, work record, review artifact, and human-gate record. |
| Done | All five artifacts exist under `run/<session-id>/`: the brief is approved, spawn output is captured with exit status, the work record reflects actual execution, the review artifact states conformance and verification items, and the human-gate record carries the decision, timestamp, and conditions. |

## Inputs

- Approved brief (required): human-authored statement of work goal and constraints. State what is optional and what must be supplied.
- Session id (required): caller-supplied, filesystem-safe, unique under `run/`. Reject if missing, not filesystem-safe, or collides with an existing directory.
- Spawn command or agent target (required): the command or agent to launch, what it may read, what outputs it must produce, and what it must not change.
- Review criteria (required): the standard the work is checked against.
- Context (optional): current directory, project layout, open issues, or prior session artifacts.

## Procedure

1. Validate the session id and approved brief. Confirm the session id is filesystem-safe and unique under `run/`. Confirm the user approves the brief. Halt if the intent is ambiguous, the brief is unapproved, or the session id is missing or colliding. Done when: the session id is validated and the brief is approved.
2. Write the brief to `run/<session-id>/brief.md`. Include the work goal, scope, constraints, and done criteria. Done when: `brief.md` exists at the stated path.
3. Execute the spawn target. Capture stdout, stderr, and the exit code. Write the spawn evidence to `run/<session-id>/spawn.md`. Done when: spawn output is captured with exit status recorded in `spawn.md`.
4. Record the work phase. Document the agent's actual execution path, outputs, and any deviations from the brief in `run/<session-id>/work.md`. Done when: the work record reflects the actual execution path and deviations.
5. Record the review artifact. Write what was produced, whether it meets the brief, and what the human must verify to `run/<session-id>/review.md`. Present it to the user. Await explicit sign-off or revision request. Done when: the review artifact states production status, brief conformance, and human verification items, and the user signs off or requests revision.
6. Collect and record the human gate. On sign-off, write `run/<session-id>/human-gate.md` with the decision, timestamp, and any conditions. Done when: the human-gate record is written with decision, timestamp, and conditions.

## Failure and recovery

- Missing or colliding session id: stop. Ask the user for a filesystem-safe, unique session id before proceeding.
- Unapproved brief: stop. Ask the user for a concrete work goal. Do not invent scope.
- Spawn failure: attempt one retry with a corrected spawn definition. Record the failure and retry count in `spawn.md`. Stop if the second attempt fails.
- Review incomplete: present the divergence to the user. Do not proceed until the user resolves or approves.
- Human gate withheld: the session is not done. Record the last state and stop.
- Partial-result rule: if any phase halts midstream, all durable artifacts written up to that point remain. No automatic rollback.

## Output

One workspace directory (`run/<session-id>/`) containing `brief.md`, `spawn.md`, `work.md`, `review.md`, and `human-gate.md` in that order. The session is executed, not merely prepared: spawn evidence and the final human-gate state are both present.
