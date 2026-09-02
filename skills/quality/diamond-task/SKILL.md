---
name: diamond-task
description: 'Use when one issue or PR is too large for a worker and partitions into disjoint write sets. Builds a task DAG, composes a reviewed result, or names the falsified node or split. Not for independent parallel tasks — use parallel-launch. No remote or irreversible changes.'
---

# Diamond task

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Use when one issue or pull request is too large or too entangled for one worker and its complete writable surface can be partitioned into disjoint write sets. |
| Authority | Reversibly write only the named local run artifacts and declared target write sets. Preserve a pre-run checkpoint and restore it on terminal failure. This is the sole production task-DAG generator. |
| Side effect | Run isolated workers and apply their returned diffs by mechanical union within their declared write sets; the composer authors no content and changes nothing outside those sets. |
| Done | Produce one result that reproduces every worker diff byte-for-byte within disjoint declared write sets and has approval from a fresh isolated reviewer who was neither a worker nor the composer, or stop with no partial composition and identify the falsified worker node or split. |

## Inputs

Required inputs are one issue or pull request with its acceptance criteria, the local target workspace, the checks each worker and the composed result must satisfy, and named local locations for the checkpoint, isolated composition, and run report. Supply any fixed ordering constraints between units of work; otherwise the partition determines independent worker nodes. The target's current bytes and metadata are the composition base. The production task DAG is derived from the supplied units of work and their declared ordering constraints only.

## Procedure

1. Capture the exact target base in the named checkpoint. Enumerate every target byte the task may create, replace, or delete, including integration edits, formatting changes, and generated output that the final result requires. **Done when:** the checkpoint captures the exact base and the complete writable surface is enumerated.

2. Design the production task DAG by partitioning that complete writable surface into worker nodes with pairwise-disjoint write sets. Define each set by canonical target paths and, when a path is shared, non-overlapping byte regions or insertion boundaries. Give each node its task, allowed write set, required checks, required proof, and only the inputs it needs. Every content byte the composer might otherwise need to author must belong to a worker node. Stop before worker execution if coverage is incomplete, any sets overlap, or isolation cannot be provided. **Done when:** the DAG partitions the surface into disjoint covering write sets with every content byte owned by a node, or the skill stops on incomplete coverage, overlap, or missing isolation.

3. Run every ready node in an isolated copy of the base. Each worker may change only its declared write set and must return its exact diff, check results, and proof. A worker may not approve either its own result or the composition. **Done when:** every ready node runs in isolation and returns its diff, check results, and proof.

4. Validate each returned diff against its node contract before composition. An overlap, an out-of-set byte, or a failing check falsifies the responsible node. Re-run only that node in fresh isolation, then repeat validation. If the failure spans write sets or exposes missing partition coverage, falsify the split instead. **Done when:** every returned diff is validated in-set with checks passing, or a node or split is falsified.

5. Recreate the isolated composition from the checkpoint and mechanically union the validated worker diffs. Reproduce every diff byte-for-byte, make no change outside the declared write sets, and author no content to reconcile, improve, format, or complete the result. Verify the composed bytes against every returned diff and run the declared composed-result checks. **Done when:** the composition reproduces every diff byte-for-byte within the write sets and the composed-result checks pass.

6. Attribute any composition mismatch or failing check to exactly one worker node and re-run only that node, then rebuild the composition from the checkpoint and repeat downstream validation. If attribution spans write sets, falsify the split. **Done when:** the mismatch or failing check is attributed to one node and re-run, or the split is falsified.

7. Give the validated composition and all proofs to a fresh isolated reviewer who was neither a worker nor the composer. A review finding falsifies exactly one worker node; re-run only that node, rebuild from the checkpoint, and repeat composition, checks, and fresh review. A finding that spans write sets falsifies the split. Only the fresh reviewer may approve the result. **Done when:** the fresh reviewer approves the result, or a node or split is falsified.

8. After approval, apply the reviewed mechanical union to the named target and verify its bytes equal the approved composition. Record the node contracts, diffs, proofs, composed checks, reviewer identity and verdict, and final byte comparison in the run report. **Done when:** the approved composition is applied, bytes match, and the run report is recorded.

## Failure and recovery
Return `blocked` without target mutation when required input, a checkpoint, isolation, or a required check is unavailable. Return `split-falsified` when the surface cannot be partitioned into disjoint covering write sets, an overlap or uncovered byte appears, or a failure or finding spans write sets. Return `node-falsified` when one node repeats an equivalent out-of-set change, check failure, composition mismatch, or review finding after its isolated re-run. For every terminal failure, discard isolated compositions, restore the named target from the checkpoint if application began, retain the returned diffs and proof as evidence, and emit no partial composition. Never report approval unless the composed checks, byte comparison, and fresh-review verdict all pass in the same replay.

## Output
On success, return `approved` with the applied composed local result and a run report containing the complete partition, worker diffs and proofs, composed check results, byte-for-byte comparison, and fresh-review approval; on a clean stop, return `blocked`, `split-falsified`, or `node-falsified` with the unchanged or restored target, no partial composition, the responsible node or split, and the falsifying evidence, ordered checkpoint → partition → run → validate → compose → attribute → review → apply.
