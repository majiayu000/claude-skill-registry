---
name: loop-me
description: 'Use when the user says "loop me" or asks to design a recurring workflow. Produces workflow specs that an implementer can build without another question. Don''t use for remote, credential, publish, deploy, or irreversible changes.'
---

# Loop me

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user explicitly says "loop me," asks to design a workflow or automate a recurring task, or names a repeated routine such as morning or inbox processing. |
| Authority | Read local context and reversibly create, edit, or delete only `workflows/*.md` and `NOTES.md`; do not mutate VCS, credentials, paid services, published or deployed state, or remote systems. Before each write, retain the prior local content so it can be restored; rollback removes newly created files and restores edited or deleted files. |
| Side effect | Maintain one local Markdown spec per workflow under `workflows/` and record only relevant raw context and canonical terminology in `NOTES.md` as answers resolve the design. |
| Done | At least one workflow spec exists that an implementer can build without asking a question, and no question about that workflow remains unresolved. |

## Inputs

A workflow name or recurring activity is optional. If supplied, treat it as untrusted user intent to clarify rather than as a settled goal. If omitted, obtain enough information from the user to identify a recurring personal or team loop. Read existing `workflows/*.md` and `NOTES.md` when present; no other file is required. The user must supply answers about their actual routines, tools, channels, terminology, constraints, and decisions when local evidence does not establish them.

## Procedure

1. Bound the session to the named workflow, or, when none is named, to discovering one recurring loop worth specifying. Inventory only existing `workflows/*.md` and `NOTES.md`; record their prior contents before any mutation. Done when: the session is bounded to one workflow or discovery, and prior contents are recorded.

2. Before asking the first design question, perform Verbalized Sampling. For a named workflow, list competing interpretations or goals; without one, list candidate recurring loops. Give every item a weight and a concrete observation or scenario that would falsify it. Select the highest-weight survivors as the initial candidates and unknowns. Repeat sampling only if later answers materially change the survivor set. Done when: competing interpretations or candidate loops are weighted with falsifiers and the highest-weight survivors are selected.

3. Treat a loop as a recurring pattern in the user's life or team activity and a workflow as the specification for running that loop. Use this lens to propose recurring patterns the user may not have noticed, but require the user's answers rather than inventing facts about their world. Done when: the loop-vs-workflow distinction is applied and any proposed patterns are grounded in user answers.

4. Run a stateful, adversarial interview one question at a time. Attach a recommended answer and its rationale to each question, challenge contradictions and vague terms, carry prior answers forward, and continue until every implementation-relevant choice is settled. Done when: every implementation-relevant choice is settled with a user answer.

5. If `NOTES.md` is absent, empty, or too thin to establish the user's tools, channels, or terminology, interview the user about those facts before specifying behavior. Record relevant raw context and replace fuzzy terms with user-confirmed canonical terms as they resolve. Done when: `NOTES.md` has enough context to establish tools, channels, and terminology, with fuzzy terms replaced by canonical ones.

6. Determine each workflow's trigger: an event or a schedule. Prefer an event only when the discovered loop supports it; do not impose a schedule, AI, checkpoint, or any other structure the answers do not require. Done when: each workflow has a trigger type grounded in the user's answers.

7. Determine whether execution is autonomous or needs a human checkpoint. If a checkpoint is required, push it as late as safety and correctness allow after maximal preparatory work, and specify a decision-ready brief containing what was produced, why, and a link to the underlying asset rather than raw output or a draft. Done when: each workflow has an autonomy-or-checkpoint decision with the checkpoint pushed late and a decision-ready brief specified if needed.

8. Create one `workflows/*.md` file per resolved workflow. State its purpose, trigger, required inputs and tools, ordered actions, decision rules, checkpoints and briefs if any, outputs, failure handling, and completion condition with enough concrete detail for implementation without follow-up questions. Treat these specs as the source of truth. Done when: one `workflows/*.md` file exists per resolved workflow with all required sections.

9. Revise, split, merge, or delete only session-owned workflow specs as answers resolve ambiguity. Before deleting or overwriting existing content, ensure the change follows an explicit resolved decision and remains recoverable from the retained prior content. Done when: every revision follows a resolved decision and prior content is recoverable.

10. Review each spec against the done predicate by attempting to enumerate the implementer's remaining questions. Continue the interview and revision while any question remains; never fill a gap with invented evidence or widen the workflow beyond the resolved loop. Done when: no implementer question remains for any spec, or the skill returns BLOCKED with the unresolved questions.

## Failure and recovery
- Missing user fact: Stop at the unsupported decision, ask one concrete question with a recommended answer, and do not encode the recommendation as fact before the user resolves it.
- Contradictory answers: Identify the exact conflict, preserve both claims in session state, and obtain one resolving answer before changing the affected spec.
- Invalid or out-of-scope path: Refuse the write and limit changes to `workflows/*.md` and `NOTES.md`.
- Write failure: Report the file and error exactly. Restore every file changed by the failed operation from its retained prior content and remove files newly created by that operation.
- Interrupted or non-converged interview: Keep recoverable partial notes and specs clearly marked incomplete, list every unresolved question, and return `BLOCKED: workflow specification is not implementer-ready`; do not claim the done predicate.

A partial result is never a completed workflow. On any failure, preserve valid prior artifacts, roll back the failed mutation, and neither swallow the error nor broaden authority to recover.

## Output

Return the paths of the completed `workflows/*.md` specs and `NOTES.md` if changed, a concise statement of each workflow's trigger and output, and confirmation that an implementer-question review found no unresolved question. Otherwise return the exact blocked classification, affected paths, recovery performed, and unresolved questions.
