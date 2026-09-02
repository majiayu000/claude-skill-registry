---
name: watch-until
description: 'Use when asked to poll a named changing job, log, or artifact until a supplied completion predicate holds. Returns a terminal verdict: predicate-holds, non-converged, or blocked. Not for source or remote-system changes. Not for continuous anomaly monitoring: use watch-for.'
---

# Watch until

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User wants to poll a changing job, log, or artifact until a supplied completion predicate becomes true and a terminal completion verdict is returned. Not for continuous anomaly monitoring: use watch-for. |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | Local reads of the named changing job, log, or artifact only. |
| Done | The supplied completion predicate has become true (`predicate-holds`), or the declared watch bound (deadline or maximum poll count) is reached without convergence (`non-converged`), or an unreadable or ambiguous condition stops the watch (`blocked`). |

## Inputs

- Target (required): the path, handle, or identifier of the changing job, log, or artifact to poll.
- Completion predicate (required): a falsifiable condition evaluated against the current observed state of the target each poll.
- Poll interval (optional): time between reads. If absent, use a sensible default for the target type.
- Deadline or maximum poll count (required): bounds the watch. The watch stops at whichever comes first. Without a bound, the watch cannot start.

## Procedure

1. Confirm the target is readable and the completion predicate is unambiguous. If either is missing or unclear, stop and report the problem: do not guess. Done when: the target is confirmed readable and the predicate is unambiguous, or the problem is reported.
2. Read the target surface. Do not write, modify, restart, or trigger anything. Done when: the current state is observed without mutation.
3. Evaluate the completion predicate against the current observed state. Done when: the predicate is evaluated to true or false.
4. If the predicate holds, stop and report `predicate-holds` with the final observed state. Done when: the terminal classification is emitted.
5. If the predicate does not hold, wait the poll interval and repeat from step 2. Done when: the poll interval has elapsed and the loop re-enters step 2.
6. Stop and report the terminal classification if any failure class in the next section is reached. Done when: the failure class is named and the terminal classification is emitted.

## Failure and recovery
- Target unreadable or disappeared: stop. Report `blocked` with the read failure and the last known state. Do not restart or recreate the target.
- Predicate unparseable or ambiguous: stop. Report `blocked` with the ambiguity. Do not infer a different predicate.
- Deadline or maximum poll count reached: stop. Report `non-converged` with the last observed state and the number of polls performed.
- Target state oscillates without satisfying the predicate: stop. Report `non-converged` with the oscillation pattern, the last observed state, and the oscillation count. Oscillation is detected when the same two or more distinct states repeat in a cycle of 3 consecutive polls without the predicate holding.
- No partial result is ever reported as success. The done predicate either holds or it does not.

## Output
One terminal classification: `predicate-holds` (with final observed state), `non-converged` (with last observed state, poll count, and the failure class that stopped it), or `blocked` (with the failure reason and last known state).
