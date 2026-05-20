---
name: project-planner
description: Produce deterministic, execution-ready project plans from ambiguous or detailed requests. Covers scope definition, milestone planning, work breakdown structure (WBS), dependency mapping, critical path identification, effort and timeline estimation, risk planning, roadmap sequencing, and acceptance criteria. Use when users ask for project planning, delivery plans, implementation roadmaps, milestone plans, task breakdowns, dependency-aware schedules, resourcing plans, tradeoff planning, or replanning after scope changes.
---

# Project Planner

## Overview
Use this skill to transform project intent into a decision-ready execution plan with explicit scope, milestones, dependencies, estimates, risks, and done criteria.
The workflow is assistant-agnostic and should be followed by any coding assistant or agent.

## Trigger Hints
Use this skill when prompts include terms such as:
- "project plan", "delivery plan", "implementation plan"
- "roadmap", "milestones", "WBS", "task breakdown"
- "dependencies", "critical path", "estimate timeline"
- "replan", "scope change", "risk mitigation plan"

## Workflow
1. Resolve planning scope and planning horizon.
2. Define success criteria and constraints from verified inputs.
3. Identify deliverables and map milestone sequence.
4. Build a task-level WBS with explicit done criteria.
5. Map dependencies and determine critical path.
6. Estimate effort, duration, and confidence.
7. Document risks, assumptions, mitigations, and ownership cadence.
8. Produce the output contract in a stable markdown schema.
9. Run verification gates before returning the final plan.

## 0) Resolve Planning Scope (required)
- Confirm planning target (project/program/feature/release) and time horizon.
- If mission-critical inputs are missing (deadline, team capacity, non-negotiable constraints), ask focused clarification questions.
- If unanswered, proceed with explicit assumptions and mark them in the output.

## 1) Define Success and Constraints
- Define objective in one sentence and measurable success criteria.
- Separate hard constraints (fixed deadline, compliance, staffing limits) from soft preferences.
- Prefer verifiable constraints from provided facts; do not invent policy, staffing, or budget details.

## 2) Identify Deliverables and Milestones
- List concrete deliverables and map them to milestone checkpoints.
- Ensure each milestone has a clear validation gate and owner role.
- Sequence milestones in dependency-aware order, not just chronological order.

## 3) Create Work Breakdown Structure
- Decompose each deliverable into actionable tasks.
- Task sizing guideline:
  - Target each task to about 0.5 to 2 working days.
  - Split tasks larger than 2 days into smaller outcome-oriented tasks.
  - Merge tasks smaller than 0.5 day only when they share owner and done criteria.
- Every task must include done criteria that is testable or reviewable.

## 4) Map Dependencies and Critical Path
- Use dependency notation `Task A -> Task B`.
- Record blocking dependencies explicitly in the task table.
- Identify the critical path as the longest chain of blocking tasks that determines minimum delivery time.
- Flag dependency bottlenecks where one task blocks multiple downstream tasks.

## 5) Estimate Effort and Timeline
- Provide effort estimates per task and milestone-level rollups.
- Include confidence markers for each major estimate: `low`, `medium`, or `high`.
- Apply explicit schedule buffer when confidence is low or unknowns are high.
- If deadline is infeasible, propose tradeoff options: reduce scope, add capacity, or shift timeline.

## 6) Risks, Assumptions, and Mitigations
- Track top risks with probability/impact and mitigation action.
- Keep assumptions explicit and falsifiable.
- Maintain an open-questions list for unresolved decisions that materially affect schedule or scope.

## 7) Ownership, Cadence, and Tracking
- Assign owner role for milestones and major workstreams.
- Define tracking cadence (for example, daily execution check and weekly milestone review).
- Include first 3 to 5 immediate next actions to start execution.

## Output Contract
Return the plan using this exact section order and schema:

1. `## Project Summary`
- Goal
- Timeline
- Team/Capacity
- Constraints

2. `## Milestones`
- Markdown table: `Milestone | Target Date | Owner | Validation Gate`

3. `## Work Breakdown`
- Markdown table: `Task | Effort | Owner | Depends On | Done Criteria`

4. `## Dependency Graph and Critical Path`
- Dependency list using `A -> B` notation
- One explicit critical path statement

5. `## Risks and Mitigations`
- Markdown table: `Risk | Probability | Impact | Mitigation | Owner`

6. `## Assumptions and Open Questions`
- Assumptions list
- Open questions list

7. `## Immediate Next Actions`
- Numbered list of first 3 to 5 execution tasks

Required rules:
- If required inputs are missing, ask clarifying questions first.
- If proceeding without answers, mark assumptions clearly and include confidence markers on estimates.
- Do not produce vague output; every milestone and task must be actionable.

## Verification Gates
Before returning the plan, verify:
- Output section order exactly matches the Output Contract.
- Every milestone has an owner and validation gate.
- Every task row has effort, owner, dependency state, and done criteria.
- Critical path is explicitly stated as one dependency chain.
- Estimate confidence markers are present for major estimates.
- Missing mission-critical inputs are represented as either clarifying questions or explicit assumptions.
