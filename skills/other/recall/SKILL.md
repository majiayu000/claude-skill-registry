---
name: recall
description: 'Use when asked to recover prior work and current status before resuming. Returns a status-tagged capsule and one concrete next move. Not for handoff snapshots — use handoff. Not for tasks that require source or remote-system changes.'
---

# Recall

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Recover prior work and current status before resuming. |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | Chat-output only. No file, credential, paid, published, deployed, or remote mutation. |
| Done | Status-tagged capsule and one concrete next move. |

## Refusals

- Fabricating state: rejected. If no session file is found, return `session-not-found`. Do not invent artifacts or actions.
- Suppressing divergences: rejected. Verified records with divergence flags are returned; divergences are not hidden to satisfy the done predicate.
- Source or remote-system changes: rejected. This skill is read-only throughout.

## Inputs

- Session identifier (required): the active session ID or session directory path to recover.
- Current working directory (required): the directory the agent was operating in when the session ended.
- Optional scope hint: a specific file, module, or task tag to narrow recovery. Omit to recover the full capsule.

## Procedure

1. Identify the session source. Locate the session state file or transcript corresponding to the supplied session identifier. If no session file is found, return `session-not-found`. **Done when**: the session file is located or `session-not-found` is returned.
2. Extract the transcript. Parse the session transcript. If parsing fails, return `transcript-parse-failure`. **Done when**: the transcript is parsed or `transcript-parse-failure` is returned.
3. Mine the transcript for work state. Collect all completed actions, emitted artifacts, tool results, and navigation events. Extract each as a discrete record with its outcome. **Done when**: every work record is extracted with its outcome.
4. Verify against live repository state. For each file, artifact, and VCS-tracked target mentioned in the transcript, read the live filesystem and confirm the record matches current state. Flag each mismatch as a `divergence`. **Done when**: every record is verified or flagged as divergent.
5. Tag the capsule. Assign each recovered record one of: `completed`, `in-progress`, `blocked`, or `diverged`. **Done when**: every record has a status tag.
6. Identify the concrete next move. From the in-progress and blocked records, select the highest-priority actionable item that is not blocked by an unresolved divergence. State it as one concrete next move. **Done when**: one concrete next move is stated.
7. Emit the capsule. Return a structured capsule containing all tagged records, the concrete next move, and a summary of divergences. **Done when**: the capsule is returned.

## Failure and recovery

- `session-not-found`: return with the identifier. Do not fabricate state.
- `transcript-parse-failure`: return with the parse error. Do not continue with partial data.
- `no-recoverable-state`: return when the transcript contains no identifiable work records. Do not invent artifacts or actions.

If some records verify and others diverge, return the verified records with divergence flags. This skill performs no mutations; no rollback is required.

## Output

A structured capsule with `session_id`, `records` (each with action, outcome, status, divergence_note), `next_move`, and `divergences`, ordered as listed.
