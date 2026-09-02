---
name: autoplan
description: 'Use when the user runs /autoplan on a plan or idea. Runs CEO, design, DX, and engineering review phases over the idea, amends the plan, derives deterministic task IDs into a task JSONL ledger, and waits at a final human approval gate. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Autoplan

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user runs `/autoplan` on a plan or idea. |
| Authority | Reversible local write: write only the amended plan, the task JSONL ledger at `tasks/autoplan-ledger.jsonl`, and TODO updates. Recover by discarding those local artifacts. |
| Side effect | Writes the amended plan, appends tasks to `tasks/autoplan-ledger.jsonl`, and updates TODOs. |
| Done | The final approval gate presents an amended plan and aggregated implementation tasks with stable IDs. |

## Inputs

Required: a plan or idea to develop, supplied as a file path or inline text.

Optional: an existing `tasks/autoplan-ledger.jsonl` to extend. If absent, create one.

## Ledger destination and overwrite policy

The task ledger lives at `tasks/autoplan-ledger.jsonl`. When the file does not exist, create it. When it exists, append new tasks to the end; never overwrite or truncate existing entries. Each run appends only the tasks it produces. This preserves prior runs and makes the ledger append-only across invocations.

## Task ID generation

Each task gets a deterministic ID formed from the reviewing phase prefix and a zero-padded sequence number within that phase:

- CEO review: `CEO-01`, `CEO-02`, ...
- Design review: `DES-01`, `DES-02`, ...
- DX review: `DX-01`, `DX-02`, ...
- Engineering review: `ENG-01`, `ENG-02`, ...

Sequence numbers start at `01` within each phase and increment in the order tasks are identified. IDs are stable within a run: the same plan evaluated the same way produces the same IDs. If a phase produces no tasks, its prefix is unused.

Each ledger line is a JSON object with `id`, `description`, and `phase` keys.

## Procedure

1. Read the supplied plan or idea. If it is a path, read the file; if inline text, use it directly. Stop if no plan or idea is supplied. Done when: the plan or idea is read or the absence is reported.
2. Run the four review phases (CEO, design, DX, engineering), each evaluating the idea against a six-principle decision register (clarity, impact, audience, risk, sequencing, reversibility). Record each phase's decisions in the register. If a phase cannot reach a decision, record the open question and continue the remaining phases. Done when: all four phases have recorded their decisions or open questions in the register.
3. Amend the plan with the consolidated decisions from all four phases. Done when: the plan is amended with consolidated decisions.
4. Derive implementation tasks from the four phases. Assign deterministic IDs per the task ID generation rules above. Construct the task ledger by appending one JSON line per task to `tasks/autoplan-ledger.jsonl`, creating the file if absent. Update TODOs to reflect the aggregated tasks. Done when: the ledger is appended with one task per line, each carrying a stable ID, description, and phase, and TODOs reflect the aggregated tasks.
5. Present the amended plan and aggregated tasks at a final approval gate. Stop and wait for the human decision; do not proceed to execution. Done when: the approval gate is presented and the skill stops for the human decision.

## Failure and recovery

- Missing input: stop before any write; report that no plan or idea was supplied.
- A review phase cannot reach a decision: record the open question in the decision register, continue the remaining phases, and surface the open question at the approval gate.
- Ledger write fails: discard the partial append; do not present a done state; report the blocked result with the phase reached.
- Rollback: all effects are local artifacts (amended plan, task JSONL ledger, TODO updates); discard them to recover the pre-run state.
- Non-converged: if the approval gate is not reached, the result is blocked, not done; never claim the done predicate holds.

## Output
An amended plan, a task JSONL ledger at `tasks/autoplan-ledger.jsonl` with deterministic IDs, updated TODOs, and a final approval gate presenting both the amended plan and the aggregated tasks for the human decision.
