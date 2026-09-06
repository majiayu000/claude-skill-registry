---
name: diverge
description: 'Use when the user wants to expand a decision field with additional options and dimensions. Not for selecting or applying an option: use decide. No source or remote-system changes.'
---

# Diverge

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User wants to expand a decision field. |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | Chat output: an expanded decision field. |
| Done | The decision field is expanded with additional options and dimensions. |

## Inputs

- A decision question or statement (required): the choice the user is weighing.
- Known options (optional): candidate choices already on the table.
- Known dimensions (optional): criteria or axes already being considered.
- Constraints or context (optional): bounds, preferences, or stakes that shape the field.

## Procedure

1. Restate the decision question in one sentence and confirm it names a choice between alternatives, not a task to execute. If it does not name a choice, stop and ask the user to restate it. **Done when:** a choice between alternatives is confirmed or the skill stops to ask.
2. List the known options and known dimensions the user supplied; mark any that are absent as empty. **Done when:** the known sets are listed or marked empty.
3. Generate additional options the user has not named, including opposites, hybrids, deferrals, and status-quo variants. Each option is one phrase plus a one-line rationale. **Done when:** new options are generated without duplicates.
4. Generate additional dimensions the user has not named: criteria or axes along which any option could be evaluated. Each dimension is one phrase plus a one-line description of what it measures. **Done when:** new dimensions are generated without duplicates.
5. Tag every option and dimension as known or new so the expansion is visible. **Done when:** every entry is tagged.
6. Return the expanded field as a structured list: decision question, options (known then new), dimensions (known then new). **Done when:** the ordered structured list is returned.

## Failure and recovery
- Vague decision question: ask the user to restate it as a choice between alternatives before expanding; do not invent the question.
- No known options or dimensions supplied: proceed with an empty known set and generate the field from the question alone; note that the starting set was empty.
- Expansion produces no new options or dimensions: report that the field appears saturated and return the known set unchanged rather than padding with redundant entries.
- Partial result: return whatever options and dimensions were generated, label the set as partial, and state that generation stopped early; never claim the field is complete.

## Output
A chat report containing the decision question, options (known then new), and dimensions (known then new), each tagged, ordered restate → inventory → expand-options → expand-dimensions → tag → return; no file is written and no decision is made.
