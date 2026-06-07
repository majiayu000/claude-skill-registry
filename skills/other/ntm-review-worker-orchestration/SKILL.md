---
name: ntm-review-worker-orchestration
description: |-
  Use when operating an NTM review or analysis worker with bounded inputs and evidence-backed output.
  Triggers:
practices:
- pragmatic-programmer
skill_api_version: 1
user-invocable: false
hexagonal_role: supporting
context:
  window: inherit
  intent:
    mode: task
  intel_scope: topic
metadata:
  tier: orchestration
  stability: stable
  dependencies:
  - ntm
output_contract: 'A reviewed worker run: mission card, NTM pane assignment, input bundle, evidence-backed findings, validation result, and durable handoff.'
---

# NTM Review Worker Orchestration

Use this skill when a named analysis or review worker should run through NTM
instead of as an in-session aside. The worker is a role, not a proprietary
persona: give it a mission, inputs, constraints, and an output contract that a
separate controller can verify.

## Fit

Use this skill when the work needs one or more of these properties:

- A persistent pane the operator can inspect, nudge, or restart.
- A named review role with a stable mission across multiple prompts.
- Cross-model or multi-pane review where findings must be compared.
- Evidence-backed critique, risk review, incident analysis, or hypothesis audit.
- A handoff that another operator can resume from NTM state and written output.

Do not use this for a simple one-shot answer, deterministic JSON-only fan-out, or
private persona emulation. Use plain skills or structured workflows for those.

## Mission Card

Before sending anything to NTM, write a mission card:

```markdown
## Review worker mission
- Worker name: <short role name>
- Session/project: <NTM session or project>
- Mission: <one sentence outcome>
- Inputs: <files, logs, tickets, diffs, URLs, prior findings>
- Non-goals: <what the worker must not investigate or edit>
- Output path: <where findings must be written or reported>
- Validation: <commands, checks, source rereads, or independent reviewer>
- Handoff: <mail thread, issue, note path, or final message target>
```

The mission must be self-contained. Do not rely on conversation context, hidden
persona lore, or "as discussed" references.

## Workflow

1. Discover the live NTM contract.
   Run `ntm --robot-capabilities` before any unfamiliar action. Prefer robot
   surfaces for automation and avoid TUI-only commands.

2. Snapshot the current swarm.
   Capture `ntm --robot-snapshot` and note the target session, panes, attention
   cursor, active work, locks, degraded sources, and whether the operator pane is
   excluded from sends.

3. Assign the worker role.
   Pick the smallest pane set that can perform the review. If no suitable pane
   exists, launch or request one through the normal NTM spawn path. Name the role
   by function, such as `security-reviewer`, `incident-analyst`, or
   `architecture-critic`.

4. Send the mission.
   Dispatch the mission card plus the input bundle. Include expected output
   format, citation requirements, validation checks, and the stop condition.
   Avoid broad `--all` sends unless the user pane inclusion is intentional.

5. Monitor by evidence, not optimism.
   Use attention, tail, events, and the worker's written artifacts to confirm
   progress. If the pane stalls, diagnose before interrupting or restarting.

6. Validate the findings.
   The controller must verify the worker's result independently. Re-read cited
   files, run the named checks, compare with another pane when needed, and mark
   findings as confirmed, unsupported, or unresolved.

7. Handoff cleanly.
   Summarize what happened, where outputs live, what was validated, what remains
   open, and which NTM cursor/session/pane state the next operator should inspect.
   Release or renew any coordination locks you opened.

## Prompt Template

```text
You are the <worker name> review worker for <project/session>.

Mission:
<one sentence outcome>

Inputs:
- <path or source>: <why it matters>

Constraints:
- Do not edit files unless explicitly authorized.
- Do not rely on uncited claims.
- Stay inside the stated scope and report scope escapes separately.

Required output:
- Findings ordered by severity or confidence.
- Evidence for each finding: file paths, commands, log lines, or observed NTM events.
- Validation suggestions for the controller.
- Open questions and handoff notes.

Stop when:
<clear completion condition>
```

## Output Spec

Every completed run must produce:

- `mission`: the mission card or a faithful summary of it.
- `pane`: session name, pane identifier, and worker role.
- `inputs`: files, commands, logs, issues, or other material inspected.
- `findings`: evidence-backed conclusions with unsupported claims removed.
- `validation`: checks the controller ran and their result.
- `handoff`: next steps, residual risk, locks/mail/issue references, and resume
  instructions.

## Validation Rules

- The live NTM contract was discovered before state-changing actions.
- Worker prompts were self-contained and role-based, not persona-based.
- Inputs and non-goals were explicit.
- Findings cite evidence the controller can inspect.
- A separate validation step checked the worker's output.
- The handoff names concrete artifacts and NTM state.

## Failure Handling

If NTM state is degraded, record the degraded source and continue only with
evidence you can observe. If a pane is stale or mis-scoped, interrupt or restart
only after a liveness proof. If the worker reports unsupported claims, return the
run for revision or mark the claims unresolved in the handoff.
