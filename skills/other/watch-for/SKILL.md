---
name: watch-for
description: 'Use when the user wants to monitor a file, log, endpoint, or stateful artifact for drift, errors, or unexpected changes and receive a per-tick anomaly verdict. Samples at a fixed cadence, compares each sample against a baseline, and emits normal, anomalous, or error judgments until a stop condition is met. Not for tasks that require source or remote-system changes, and not for polling a completion predicate: use watch-until.'
---

# Watch for

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User wants to observe a changing surface and receive a judgment on anomalies. |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | Local reads of the bounded changing surface at each sampling interval. |
| Done | The stop condition is met and a final summary is emitted. |

## Inputs

1. **Surface address** (required): the file, URL, log, or artifact to observe. Declare its path or address once; do not widen scope during the watch.
2. **Anomaly criteria** (required): the condition, pattern, threshold, or structural rule that classifies a sampled state as anomalous. State it in falsifiable terms.
3. **Sampling interval** (required): the cadence between reads. A number of seconds, a cron expression, or an event-driven trigger name.
4. **Stop condition** (required): a predicate that ends the watch automatically, or an explicit tick count after which the watch stops.

## Procedure

1. Bound the surface. Record the surface address, anomaly criteria, and sampling interval. Refuse to observe anything outside this declared scope. Done when: surface address, anomaly criteria, and sampling interval are recorded.
2. Capture the initial state as the baseline snapshot. Read the surface once. Done when: the baseline snapshot is recorded.
3. Wait the sampling interval, then sample the surface. If the surface is unreadable, emit an error judgment and wait for the next interval rather than widening scope. Done when: a sample is read or an error judgment is emitted.
4. Compare the current sample against the baseline using the anomaly criteria. Classify the sample as normal, anomalous, or error. Done when: the sample is classified.
5. Emit judgment. If anomalous, emit a judgment containing: surface address, timestamp, what changed, why it matches the anomaly criteria, and severity derived from the anomaly criteria (the criteria itself defines what counts as critical versus informational). If normal, emit a brief no-anomaly confirmation. If error, emit the read failure reason. Update the baseline to the current sample. Done when: judgment is emitted and baseline is updated.
6. Check the stop condition. If met, end the watch and emit a final summary: total ticks, anomalies found, error count, and final surface state. Otherwise, repeat from step 3. Done when: stop condition is met and final summary is emitted.

## Failure and recovery
| Failure class | Behavior |
|---|---|
| Surface unreadable | Emit an error judgment naming the surface and failure reason. Wait for the next interval. Do not widen scope or invent data. |
| Stale sample | Mark the judgment as stale-data. Continue watching. Do not suppress the tick. |
| Scope-widening requested | Refuse. The surface was bounded at step 1. Report the refusal and continue on the declared surface. |
| Stop condition unreachable | If the stop condition depends on an external system that fails, emit a warning and continue until manual stop. |

No failure class causes the watcher to pretend the done predicate holds. Every tick produces a judgment or an explicit error.

## Output
A stream of per-tick judgments (surface address, timestamp, classification: normal/anomalous/error/stale, what changed or why the read failed, severity if anomalous), with a final summary on stop: total ticks, anomaly count, error count, and final surface state.
