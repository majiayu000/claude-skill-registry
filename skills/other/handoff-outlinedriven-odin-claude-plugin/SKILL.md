---
name: handoff
description: 'Use when substantive work reaches a session boundary, resumes after interruption, completes, or must move to another session, agent, harness, directory, or repository. Maintains ignored local continuity state and emits a bounded portable brief without launching its receiver.'
---

# Session continuity and handoff

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Substantive work starts, reaches a significant boundary, resumes after interruption, completes, or must move to another session, agent, harness, directory, repository, or person. An explicit handoff request selects the packaging branch. |
| Authority | Reversible writes to ignored repository-local continuity files and, on explicit handoff, one portable brief or stdout. No receiver launch, remote mutation, credentials, paid actions, publication, deployment, data-at-rest changes outside these artifacts, bulk mutation, or irreversible effects. |
| Side effect | Continuity files under `.handoff/continuity/` and portable briefs under `.handoff/handoffs/` written to disk. |
| Done | Continuity status (`fresh`, `resumed`, `interrupted`, or `completed`) with the death-point path. On explicit handoff, one compliant brief path or stdout result. |

## Inputs

- Current repository identity, session handle, goal, scope, active files, and current time.
- Current tasks, decisions with rationale, blockers, evidence, and next action.
- Existing continuity artifacts, when present.
- For explicit handoff: an optional source handle, destination path, and project exclude list.

Use `.handoff/continuity/` for `notes.md`, `graph.md`, and `death-point.md`. Use `.handoff/handoffs/` for portable briefs. Before the first write, prove `.handoff/` is ignored. If it is not, add the repository-local exclusion and prove it again. Do not stage these files.

## Procedure

1. **Choose resume or fresh.** Follow [resume.md](references/resume.md). Resume only from the complete, readable, unfinished continuity set whose recorded repository identity matches the current repository. Start fresh when it is absent, completed, corrupt, stale, incomplete, or belongs to another project. A minimal emergency death point starts a fresh record with its available context. Preserve unusable files and report why they were rejected.

2. **Initialize continuity state.** In fresh mode, write `death-point.md` first with the available goal, repository identity, session handle, timestamp, status `active`, and next action `initialize continuity state`. Flush that minimal death point before creating `notes.md` and `graph.md`. Then write the goal, scope, repository identity, session handle, and initial rationale to `notes.md`; create a directed graph of task, decision, and blocker nodes with dependency, sequence, and resolution edges; and replace the death point with the last completed action, next action, blockers, timestamp, and status `active`. In resume mode, append a timestamped resumption record, mark the prior death-point node `resumed`, and reconcile current facts without rewriting prior rationale.

3. **Maintain one live record.** At each decision, discovery that changes the plan, task-state transition, blocker change, phase boundary, interruption risk, or scope change, update the rationale notes, graph, and death point before continuing. Record the changed fact and why it matters; omit tool chatter and intermediate noise. Flush all three artifacts after the update.

4. **Mark the ending.** On interruption or ordinary session exit, set the death point to `interrupted` with the last completed action, exact next action, active blockers, and timestamp. On goal completion, append the achieved result and residual work to the notes, resolve or classify every open graph node, and set the death point to `completed`. A later session always starts fresh after a `completed` marker.

5. **Package only on explicit handoff.** Resolve the requested source by exact handle when supplied; otherwise use the current live state. Reject ambiguity and wrong-project matches. Before reading source content into the package, apply the exclude list to the canonical project identity and every candidate path. Refuse the package if any source is excluded; a stale index does not override the current exclude list.

6. **Print the source receipt.** Show session or harness kind, canonical project identity, short session handle, source timestamp, and computed age. Treat future or invalid timestamps as unknown age. For work older than seven days, print a warning with its age before continuing. If policy withholds newer matching work, disclose that this is the newest visible source.

7. **Build one UTF-8 brief of at most 6,144 bytes.** Include typed sections for source receipt, goal and scope, active files, task/decision/blocker graph, decisions with rationale, evidence, next action, and `Where it stopped`. Filter raw transcript, tool output, command dumps, JSON or CLI walls, system reminders, repeated material, and long token runs. Preserve conclusions in order. Reserve at least one quarter of the budget for `Where it stopped`, containing the final substantive, noise-filtered exchanges or the death-point facts. When truncation is required, end that section with `[cut for handoff budget]`; do not leave an empty heading or append content after the marker.

8. **Emit and stop.** Write the brief under `.handoff/handoffs/` or emit it to stdout. End with: `Continue from this compact context; do not re-derive completed work.` Report the path or stdout result and current continuity status. Never launch or instruct tooling to launch the receiver.

## Failure and recovery

- Unusable prior state: preserve it, name `corrupt`, `stale`, `incomplete`, `completed`, or `wrong project`, and start fresh.
- Unverified ignore rule: stop before writing continuity state and name the failed ignore check.
- Ambiguous or absent handoff source: stop packaging and request an exact handle; keep maintaining current continuity state.
- Excluded source: name the matched project or path and emit no brief.
- Budget failure: emit no complete brief until its UTF-8 byte count is at most 6,144 and every required section is nonempty.
- Partial write: preserve every complete artifact and report the failed file. A complete minimal `death-point.md` is an emergency recovery marker: the next session starts fresh from its available goal and timestamp, then rebuilds notes and graph from current evidence. Any other partial set is not a usable resume point.

## Output

During work, output the ignored local continuity status: `fresh`, `resumed`, `interrupted`, or `completed`, with the death-point path. On resume, also name any rejected continuity set and its reason. On explicit handoff, output the source receipt, any age or visibility warning, and one compliant brief path or stdout result. The procedure ends there; no receiver is launched.
