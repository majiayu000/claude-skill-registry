---
name: ax-audit
description: 'Use when asked to audit an agent or AI feature for agentic-experience quality. Assesses target source or described behavior against Architecture and Agentic-experience rubrics, records findings with locators or logical bounds, and returns a severity-tiered report with a PASS/FAIL/INCOMPLETE verdict. Not for source or remote-system changes.'
---

# AX audit

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Human asks for an agentic experience audit, an AX review, whether something is agent-native, a critique of an AI feature, or whether it earns user trust |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation |
| Side effect | Chat output only: a read-only severity-tiered report with a ship-readiness verdict and an AX Relationship Summary |
| Done | Delivered findings with locators (file:line for source, logical bounds for described behavior), an AX Relationship Summary, and a PASS/FAIL/INCOMPLETE verdict |

## Inputs

- Target agent system or AI feature under audit: source path, repository, or described behavior. Required.
- Scope boundary: which files, modules, or interaction surfaces are in scope. Required.
- Specific concern or focus area the human wants prioritized. Optional.

## Procedure

1. Read the target source or described behavior within the stated scope. Do not mutate anything. Done when: the target is read within the scope boundary.
2. Evaluate the target against two audit axes, each with four rule families. Record every finding with a locator: `file:line` for source-backed targets, or logical bounds (described behavior, interaction surface, or module name) for behavior-only targets.

   Architecture axis (rules-arch):
   - Communication: approval gate present where the agent should act autonomously; completion signal missing or ambiguous; progress not visible to the user during long work.
   - Context: no checkpoint or resume across sessions; context injection absent or brittle; context starvation where the agent lacks information it needs to act.
   - Granularity: static API mapping where tools mirror raw endpoints instead of workflow-shaped actions; tools too coarse or too fine for the task shape.
   - Parity: CRUD coverage incomplete; tool or UI parity gaps where an action exists in one surface but not the other; orphaned UI actions with no backing tool.

   Agentic-experience axis (rules-ax):
   - Communication: no generative momentum where the agent stalls instead of producing; no intent handshake where the agent does not confirm or negotiate intent; no progress signal during execution.
   - Context: memory not visible to the user; no adaptive canvas that reshapes around the work; agent operates under-contextual, missing situational awareness.
   - Control: no approval gate where one is needed for irreversible actions; no escape hatch to interrupt or redirect; control buried under conversational friction.
   - Trust: no confidence cues where the agent asserts without signaling certainty; no escalation path when the agent is stuck or uncertain; no uncertainty markers on outputs.

   Done when: every rule family across both axes is evaluated and findings are recorded with locators or marked INCOMPLETE.
3. Assign each finding a severity: Critical (blocks ship), Major (degrades trust or correctness), Minor (polish). Done when: every finding has its severity assigned.
4. Write the AX Relationship Summary. In one paragraph, state how the agent and user relate across control, trust, context, and communication. Classify the relationship as human-led, agent-led, or collaborative, and explain where it breaks down. Done when: the relationship summary paragraph is written with its classification.
5. Issue the ship-readiness verdict:
   - PASS: no Critical findings; Major findings are acknowledged and acceptable.
   - FAIL: one or more Critical findings.
   - INCOMPLETE: scope or target was insufficient to evaluate one or more rule families.
   Done when: the verdict is issued with its reason.

## Failure and recovery

- Insufficient target: if the source or described behavior does not expose enough to evaluate a rule family, mark that family INCOMPLETE rather than guessing. Do not invent findings.
- Scope too narrow: state which rule families could not be evaluated and why. Do not widen scope without the human's explicit request.
- No mutation on failure: the audit is read-only; there is nothing to roll back. Re-run with expanded scope or additional source if the human provides it.

## Output

A chat report ordered: severity-tiered findings (each with file:line or logical-bound locator, rule family, severity, explanation), AX Relationship Summary paragraph, ship-readiness verdict (PASS/FAIL/INCOMPLETE with reason).
