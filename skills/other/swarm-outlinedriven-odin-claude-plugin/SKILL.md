---
name: swarm
description: 'Use when asked to run partitioned parallel coverage or races across isolated workers. Don''t use for remote, credential, publish, deploy, or irreversible changes.'
---

# Swarm

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Run partitioned parallel coverage or races. |
| Authority | Reversible local: writes only named local artifacts; rollback is version control or undo. No remote mutation. |
| Side effect | Spawns isolated cloud workers. Workers run session-scoped; nothing published. |
| Done | Consolidated evidence table with gaps and dropouts returned. |

## Inputs

Must supply:
- **Partition strategy or count.** A partition count (integer, minimum 2) or a custom strategy that assigns disjoint work slices to each worker.
- **Test target or scope.** The exact test suite, file set, coverage mode, or race condition to run in each partition.

Optional:
- **Concurrency cap.** Defaults to 3. Cap concurrency even when more partitions are independent. Workers do not automatically scale up unbounded.
- **Session label.** A string to prefix each worker session name for traceability.

## Refusal

- No concrete target or partition count: stop. Do not infer or extend the target.
- Partial failure (some workers failed, at least one produced evidence): return the consolidated partial evidence with the non-converged result. List the failed partitions by ID.
- Complete failure (all workers failed): return a blank table with the non-converged result. Name the failure class and the request that caused it.
- Non-converged: use `non-converged` when all workers fail, a batch produces broad unplanned edits, or the evidence cannot be consolidated.

## Procedure

1. **Bound the scope.** Accept only the partition strategy and the test target. Done when: a concrete target and partition count are confirmed.
2. **Derive partitions.** Convert the partition strategy into N disjoint work slices, where N equals the partition count or the number of slices the strategy produces. Each slice must be independently runnable with no shared state. Done when: N disjoint slices are enumerated.
3. **Cap concurrency.** If concurrency cap is not supplied, default to 3. Do not spawn more than the cap simultaneously even if more partitions are available. Done when: the concurrency cap is set.
4. **Spawn isolated workers.** Spawn each worker in a fresh, isolated session. Each worker receives exactly one slice and runs the test target against that slice only. Workers do not coordinate; no shared state is assumed. Done when: every worker is dispatched.
5. **Run to completion.** Wait for each worker to finish. Each worker produces a local evidence artifact scoped to its slice: pass/fail per test, coverage percentage, and any dropouts (skipped, timed out, panicked). Done when: every worker has returned or failed.
6. **Consolidate evidence.** Collect every worker artifact. Merge into one table with one row per partition: partition ID, tests run, tests passed, coverage delta, dropouts. Add a summary row: combined tests, combined coverage, total dropouts. Done when: the consolidated table is assembled.
7. **Report gaps and dropouts.** Name every partition that produced a dropout or coverage below the expected threshold. For each gap, give the partition ID, symptom, and affected slice. Done when: every gap is named.
8. **Stop, do not widen.** Return the consolidated table and the gap report. Do not trigger additional workers, re-run failed partitions, or mutate the original source. Done when: the table and gap report are returned.

## Output

Consolidated evidence table (partition ID, tests run, tests passed, coverage delta, dropouts; one summary row) plus a gap report naming every partition with a dropout or sub-threshold coverage by partition ID, symptom, and affected slice.
