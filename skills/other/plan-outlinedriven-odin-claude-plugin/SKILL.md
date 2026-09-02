---
name: plan
description: 'Use when a user commits to a direction and asks to plan, brief, research, or operationalize it. Classifies type and tier, researches read-only, and writes to plans/ after acknowledgment. Not for scoring — use planning; not for codebase audit — use plan-review.'
---

# Knowledge plan

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User commits to a direction and asks to plan, brief, structure, research, or operationalize it. |
| Authority | Reversible local: write only named local plan artifacts; state the rollback path. |
| Side effect | Runs read-only parallel research and writes plans/{type}-{descriptive-name}.md, adding a date on collision. |
| Done | Type and tier are classified; prior work, knowledge, live data, external facts when needed, and origin tensions are checked; user acknowledges the context brief; the file leads with the type-correct answer and includes sourced metrics, questions, and references. |

## Inputs

- Required: user commitment to a direction and a descriptive name for the plan.
- Optional: stated type/tier preference; any pinned evidence or references the user supplies.

## Procedure

1. **Classify type.** Map the user's ask to one of: Product Plan, Technical Plan, Research Brief, Operational Plan. Map the tier to one of: Exploration, Proposal, Execution, Audit. Done when: type and tier are classified.
2. **Research prior work.** Read every file under plans/ relevant to the direction. Record what already exists and what gaps remain. Done when: existing plans under plans/ are read and gaps recorded.
3. **Research knowledge base.** Query available context (memories, session notes, codebase knowledge) for relevant facts, constraints, and prior decisions. Done when: relevant facts, constraints, and prior decisions are queried.
4. **Research live data.** When the plan requires measurable or factual grounding, fetch current evidence: live search, API lookups, or tool calls that read current state. Done when: current evidence is fetched when the plan requires it.
5. **Surface origin tensions.** Flag any contradictions between prior work, stated knowledge, and live data. List them as open questions in the plan. Done when: contradictions are listed as open questions.
6. **Draft the context brief.** Write one paragraph summarizing the direction, the classified type and tier, and the key tensions surfaced. Present it to the user. Done when: one paragraph covering direction, type, tier, and tensions is presented.
7. **Await acknowledgment.** Do not proceed to file write until the user confirms the context brief is accurate. Done when: the user confirms the context brief.
8. **Write the plan artifact.** Write plans/{type}-{descriptive-name}.md. If a file at that path already exists, append a date stamp to the filename before writing. Done when: the file is written at the correct path (date-stamped on collision).
9. **Lead with the type-correct answer.** Open the file with the answer, conclusion, or verdict first, before any background or rationale. Done when: the file opens with the answer before any background.
10. **Include sourced metrics, questions, and references.** Every factual claim in the plan carries a source or a citation marker. Open questions are listed explicitly. Done when: every factual claim carries a source and open questions are listed.
11. **Declare done.** Report the written file path and confirm that type, tier, research checks, acknowledgment, leading answer, and sourced references are all present. Done when: the file path is reported and all checks confirmed present.

## Failure and recovery
- No direction or name supplied. Skill stops. No plan is written.
- Research read failure. Log the failure. Continue with remaining research streams. If all streams fail, write the plan with an explicit "unverified" section listing every failed check.
- File write failure. Do not write a partial file. Report the error and the rollback: no artifact is left behind.
- User withholds acknowledgment. Skill stops. No file is written. Report the blocked state.
- No research findings. Write the plan with a "Sparse" marker and an explicit list of what was checked and found empty.

## Output
A file at `plans/{type}-{descriptive-name}.md` (or `-{date}.md` on collision) containing the type-correct answer first, then classified type and tier, sourced metrics, open questions, and references — not done until the user acknowledges the context brief.
