---
name: size-the-run
description: 'Use when a run could be over- or under-powered, before dispatching a subagent, or when the user asks how hard to think about a task. Recommends one capability tier and one effort level on a neutral two-dial scale, without pinning a vendor model.'
---

# Size the run

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks how hard a run should be ('how hard should I think about this', 'is this worth a deep run', 'size this task') or a subagent dispatch is about to launch. |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | One advisory recommendation in chat; no config, execution, or model change. |
| Done | The report names exactly one capability tier plus one effort level (the cheapest sufficient pair), the move-up/move-down triggers, and the proof surface. |

## Inputs

- Task description (required): the work being sized: a concrete unit of work, not a vague goal.
- Context (optional): domain constraints, risk factors, or prior sizing history that affect the judgment.

## Procedure

1. **Frame the unit.** Name the exact work being sized. Done when: the unit of work is named in one sentence.
2. **Score once.** Assess risk and complexity across ownership boundaries, reversibility and blast radius, safety or privacy risk, ambiguity and synthesis load, need for research or adversarial review, and the cost of a wrong answer. Done when: all six risk dimensions are assessed.
3. **Read off tier.** Choose the cheapest tier whose ceiling covers the judgment and risk. Risk beats size: one high-risk file can want `frontier`, while a broad mechanical rename can stay `fast`.
   - `fast`: local, mechanical, reversible work with cheap, complete verification.
   - `standard`: ordinary repo-grounded reasoning, multi-step drafting, normal coding and docs.
   - `frontier`: architecture, high ambiguity, safety or security risk, release-critical review, or work where one wrong assumption wastes a large run.
   Done when: one tier is chosen with its rationale.
4. **Read off effort.** Default to the effort that tracks the tier. Raise it for ambiguity or long multi-step reasoning; lower it for a bounded task under a strong model. Effort buys deliberation, never capability.
   - `glance`: minimal deliberation, the direct path.
   - `measured`: ordinary, everyday deliberation.
   - `thorough`: deliberate extra: alternatives and assumptions checked.
   - `exhaustive`: maximal deliberation, the search exhausted and re-checked.
   Tier and effort move together by default (`fast`→`glance`, `standard`→`measured`, `frontier`→`thorough`, reserving `exhaustive` for the hardest stakes), then part where deliberation-hunger and capability-need diverge.
   Done when: one effort level is chosen with its rationale.
5. **Report both coordinates.** Give one shared rationale, `move up if` and `move down if` triggers for each dial, and the proof surface the work still needs regardless of tier or effort. Done when: both dials, their triggers, and the proof surface are stated.
6. **Stop.** Do not execute the sized task, change config, or switch models. Done when: no execution action is taken; the recommendation is the sole output.

## Failure and recovery
- Ambiguous task boundary: refuse to size; ask the user to name the unit of work before proceeding.
- Insufficient risk signal: default to `standard`/`measured` and state the assumption explicitly; do not guess.
- Partial result: if the task cannot be fully assessed, return the best-effort sizing with the uncertainty named; never silently default.
- Non-convergent: if repeated re-assessment yields different tiers without new evidence, report the last stable pair and the oscillation.
- No rollback applies: this skill is read-only and advisory.

## Output
A report naming exactly one capability tier (`fast`/`standard`/`frontier`), one effort level (`glance`/`measured`/`thorough`/`exhaustive`), a shared rationale, move-up and move-down triggers per dial, and the proof surface — no routing, vendor, or orchestration claim.

Machine-readable block:

```text
recommended_tier: fast|standard|frontier
recommended_effort: glance|measured|thorough|exhaustive
rationale: <one sentence, covering both dials>
move_up_if: <signals that would justify a stronger tier or higher effort>
move_down_if: <signals that would justify a cheaper tier or lower effort>
proof_surface: <verification still required>
```
