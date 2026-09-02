---
name: backlog
description: 'Use when asked to park an undecided idea without representing it as decided or active work. Creates or updates one reversible local backlog entry with evidence and a readiness threshold. Not for decided or active work — use the project task system.'
---

# Backlog

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User wants to park an undecided idea without representing it as decided or active work. |
| Authority | Reversible local write only: create or update one backlog entry file. No VCS commit, no remote call, no credential use, no published artifact. |
| Side effect | One backlog entry as a reversible local state change with recorded evidence. |
| Done | The idea is parked in the backlog and ready to be promoted when it meets the readiness threshold. |

## Inputs

- Idea statement (required): one or two sentences naming the idea and the problem it would address.
- Undecided reason (required): the specific missing input that blocks a decision now — an unverified assumption, absent evidence, an open question, or a competing alternative.
- Readiness threshold (required): the concrete, falsifiable condition that, when met, would make the idea promotable (a measurement, a resolved question, or a confirmed constraint that yields a yes/no).
- Existing evidence (optional): links, measurements, or notes already in hand that bear on the idea.
- Backlog location (optional): path to the backlog file or directory; default is a `backlog.md` file in the current workspace.

## Procedure

1. Validate the inputs: confirm the idea statement is a single coherent proposal, the undecided reason names a concrete missing input, and the readiness threshold is falsifiable. A human or tool must be able to test it and get a yes/no result. Done when: all three required inputs are validated as coherent, concrete, and falsifiable.
2. Bound scope: this skill only parks the idea. Do not evaluate, rank, or promote it. Do not create tasks, requirements, or tickets. Done when: scope is bounded to parking only with no evaluation, ranking, or promotion.
3. Locate or create the backlog store. If a backlog file exists, append to it; otherwise create one with a header marking it as undecided-parking only. Done when: the backlog store is located or created.
4. Write one entry with the idea statement, undecided reason, readiness threshold, any supplied evidence, timestamp, and a stable identifier. Derive the identifier from the idea statement as a kebab-case slug (lowercase words joined by hyphens, with non-alphanumerics dropped); on collision with an existing identifier, append `-2`, `-3`, and so on. Mark the entry status `parked`. Done when: the entry is written with all fields and marked `parked`.
5. Record the entry as a reversible local state change: the file write is the only mutation. No commit, push, or remote call occurs. Done when: the entry is recorded as the only mutation with no commit, push, or remote call.
6. Confirm the done predicate: the entry exists, is marked `parked`, and carries its readiness threshold so a later promotion step can test it. Done when: the entry is confirmed present, parked, and threshold-carrying.

## Failure and recovery
- Non-falsifiable threshold: if the readiness threshold cannot be checked with a yes/no outcome, stop and ask the user to restate it as a testable condition. Do not park an entry whose promotion trigger is subjective.
- Idea already decided or active: if the idea is already represented as a task, requirement, or in-progress work, stop. The backlog is for undecided ideas only; parking a decided item duplicates state.
- Write failure: if the backlog file cannot be written, do not mutate any other file. Report the write error and the intended entry content so the user can retry or relocate.
- Partial result: no partial state is valid. Either the full entry is written or nothing is written. A failed write leaves the backlog unchanged.

## Output
One backlog entry in the local backlog store, marked `parked`, carrying its idea statement, undecided reason, readiness threshold, evidence, and timestamp — ready to be promoted by a later decision step that tests the threshold.
