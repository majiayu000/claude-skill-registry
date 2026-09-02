---
name: converge
description: 'Use when the user wants to collapse an open decision field to one decision and record its rationale locally. Not for multi-lens pressure testing. No remote or irreversible changes.'
---

# Converge

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User wants to collapse an open decision field to one decision and record its rationale. |
| Authority | Reversible local write to exactly one named local decision record file. No code, VCS, credential, paid, published, deployed, or remote mutation. Rollback is deleting or reverting that record file. |
| Side effect | A decision and rationale written to one local decision record file; the open field is marked collapsed. |
| Done | The decision field is collapsed to one decision with a distinguishing rationale recorded in the local decision file. |

## Inputs

- The open decision field: the set of considered options, recorded human opinions, agent doubts, and obvious assumptions. Required.
- The human's chosen option. Required; if not supplied, prompt the human to select one.
- The decision record path. Optional; defaults to `docs/decisions/YYYYMMDD-decision.md` where YYYYMMDD is today's date.

## Decision record format

```markdown
# Decision: <one-line summary>

Date: YYYY-MM-DD

## Chosen option

<the selected option>

## Rationale

<why this option won>

## Rejected options

- <option>: <why it was rejected>
- <option>: <why it was rejected>
```

## Procedure

1. Read the open decision field and enumerate every considered option, recorded human opinion, agent doubt, and obvious assumption. If no field exists, stop: there is nothing to collapse. Done when: every option, opinion, doubt, and assumption in the field is enumerated, or the absence of a field is reported.
2. If the human's chosen option was not supplied, prompt the human to select one option from the field. Do not select on the human's behalf. Done when: the human has selected one option from the field.
3. State the rationale that distinguishes the chosen option from each rejected option: why it won and why each other did not. If the rationale holds equally for a rejected option, ask the human to sharpen it before recording. Done when: a distinguishing rationale is stated for the chosen option against every rejected option.
4. Write the chosen option and its distinguishing rationale to the decision record file at the determined path using the format above. Create the parent directory if needed. Mark the field collapsed. Done when: exactly one decision is recorded with rationale and the field is marked collapsed.

## Failure and recovery

- Empty field: no options to collapse. Stop and report "no decision field to collapse". Do not invent options.
- No human selection: the human did not choose. Stop and report "awaiting human selection". Do not pick a default.
- Ambiguous rationale: the rationale holds equally for a rejected option. Ask the human to sharpen it before recording. Do not record a non-distinguishing rationale.
- Partial-result rule: a partially written record is not a decision. Revert the record file to its prior state and report the block.
- Rollback: delete or revert the local decision record file. No other artifact is touched.

## Output

A local decision record file at `docs/decisions/YYYYMMDD-decision.md` (or the supplied path) containing the chosen option and its distinguishing rationale against every rejected option, with the field marked collapsed.
