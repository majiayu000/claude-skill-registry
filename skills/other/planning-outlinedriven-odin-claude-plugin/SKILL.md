---
name: planning
description: 'Use when a plan must be stress-tested, iteratively improved, and scored against a 5/5 quality bar across six dimensions. Drafts, scores with a deterministic rubric, and revises up to a fixed iteration limit. Not for a committed-direction brief; use plan. Not for task breakdown; use planning-and-task-breakdown.'
---

# Planning

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user says stress-test this plan, get this plan to 5/5, review and score my plan, or asks to iteratively improve a plan against a quality bar. |
| Authority | Reversible-local: write only the named plan file and review report. Rollback by discarding uncommitted files. |
| Side effect | Writes a plan file and a review report. May ask clarifying questions before the first draft. |
| Done | The plan scores 5/5 on all six dimensions (completeness, feasibility, scope, testability, risk, assumptions) with checkable claims, or a named blocker is recorded that the plan cannot resolve. |

## Inputs

- Feature description or existing plan text (required): supplied by the user or session context.
- Scope, appetite, or constraint signals (optional): any constraints the user supplies.

## Procedure

1. Gather requirements and bound scope. If the user supplied a feature description, extract the stated goal, constraints, and known dependencies. If information is missing, ask one precise clarifying question before proceeding. Do not assume scope. Done when: goal, constraints, and dependencies are extracted or a clarifying question is asked.
2. Draft the initial plan. Structure it as: goal (one-sentence desired outcome), scope (included and explicitly excluded), steps (numbered, ordered, each stating who does what and what evidence proves it done), feasibility check, assumptions, risk (named with mitigation), and testability. Done when: the draft contains all seven structural parts.
3. Score the plan against six dimensions using a deterministic 1-5 rubric:
   - Completeness: does the plan cover the full goal with no gaps in steps or evidence?
   - Feasibility: can each step be executed with the stated authority and inputs?
   - Scope: is the boundary between included and excluded explicit and non-contradictory?
   - Testability: does each step name evidence that proves it done?
   - Risk: is every risk named with a mitigation?
   - Assumptions: is every assumption stated and checkable?
   Score 5 only when the dimension is fully satisfied. Score below 5 when a specific gap exists, and name the gap. Done when: every dimension has a numeric score and named gaps.
4. Iteratively revise the plan to close gaps, up to a maximum of 5 loops. Each revision addresses the specific named gaps from the prior score. Re-score after each revision. If a revision introduces a new gap in a previously-scored dimension, revert to the last fully-scored state and name the new gap. Stop when every dimension scores 5, a named blocker outside reversible-local authority is identified, or the iteration limit is reached. Done when: every dimension scores 5, a named blocker is recorded, or 5 iterations are completed.
5. Deliver the final plan file and review report. The review report states each dimension score, what was changed in each iteration, any named blockers, and the final verdict. Done when: the plan file and review report are written with per-dimension scores and the iteration log.

## Failure and recovery

| Failure | Recovery |
|---|---|
| User provides no feature description and declines to answer clarifying questions | Stop. Output "no plan written: feature description required." Do not assume scope. |
| Iteration limit reached without 5/5 | Output the plan with current scores. Name every dimension that did not reach 5. State "plan did not reach 5/5" in the review report. |
| Named blocker identified outside reversible-local authority | Name the blocker in the review report. State the plan is incomplete and what resolution is needed. Do not pretend the plan is done. |
| Revision introduces a new gap in a previously-scored dimension | Revert to the last fully-scored state. Name the new gap. Do not widen scope. |

## Output

A plan file (`PLAN.md` or user-named) with goal, scope, steps, feasibility, assumptions, risks, and testability notes, plus a review report with six-dimension scores, iteration changes, named blockers, and the final verdict. Or a one-sentence refusal naming the missing input when no plan is written.
