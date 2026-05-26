---
name: plan-flow
description: "Analyze repository-level duplicate/redundant design first, then build and execute a strict step-test-update plan in docs/plan. Use for deep architecture review, convergence planning, and traceable one-step-at-a-time delivery."
---

# Plan Flow

## Overview

Use this skill when the user needs:
- A complete analysis of duplicated/redundant design in a codebase.
- A detailed TODO plan with explicit file-level steps.
- Strict execution evidence: change one step, test it, then update plan status.

This skill is repository-agnostic. It defines how to analyze and plan, not only what was done in one specific repo.

## Core Workflow (Analyze -> Plan -> Execute)

1. Establish scope and constraints.
- Confirm target directories/modules and out-of-scope areas.
- Capture compatibility requirement, risk tolerance, and testing expectations.
- Record baseline (`git status --short`, current branch, known blockers).

2. Run structured redundancy analysis first.
- Build an inventory of architecture anchors:
  - Domain models and schemas
  - Factory/registry entry points
  - HTTP/storage/cache/logging abstractions
  - Route/service/provider adapters
- Identify duplicate/redundant candidates with evidence:
  - Same concept, multiple conflicting definitions
  - Same responsibility, parallel implementations
  - Exported but unconnected modules
  - Dead/legacy paths still affecting readability
- For each finding, record:
  - Exact files and symbols
  - Call path or usage evidence
  - Risk if changed
- See `references/analysis-playbook.md`.

3. Prioritize and convert analysis into executable plan.
- Score each finding by impact/effort/risk/confidence.
- Group into phases (`P0`, `P1`, `P2`) and sequence low-risk/high-signal steps first.
- Create or update `plan/<task>.md` from `references/plan-template.md`.
- Keep exactly one step in `in_progress`.
- Use statuses: `pending` / `in_progress` / `completed` / `blocked`.
- See `references/risk-impact-scoring.md`.

4. Execute with strict step-test-update loop.
- Implement only the current step and only in listed files.
- Run step-level tests immediately, then project health checks.
- Update plan status and execution log before touching next step.
- On failure, record root cause and run fix loop before continuing.

5. Close with phase/final verification.
- Run phase matrix checks and final regression set.
- Report residual risks, deferred work, and explicit coverage gaps.

## Quality Gates

- No finding enters the plan without file-level evidence.
- No step is `completed` without test command evidence.
- No next step starts before plan status/log update is written.
- If full regression is unavailable, record exact reason and nearest fallback checks.

## Reference Map

- `references/analysis-playbook.md`
  - How to detect duplicate/redundant design with reproducible evidence.
- `references/risk-impact-scoring.md`
  - How to prioritize findings into phases and step order.
- `references/plan-template.md`
  - Reusable plan skeleton including analysis table, step template, and log format.
- `references/plan-accomplishments.md`
  - One completed real example (for style and granularity only, not as mandatory scope).

## Scripts

- `scripts/redundancy_scan.sh <target_dir>`
  - Fast first-pass scan for duplicate symbol names, parallel factory/builders, and legacy/dead-code hints.
- `scripts/findings_to_plan.py --target-dir src --output plan/<name>.md`
  - Convert scan findings into a draft execution plan with scoring and phased order (`P0/P1/P2`).
- `scripts/plan_lint.py <plan/file.md>`
  - Validate plan state machine, test evidence, and execution-log completeness for completed steps.

## Trigger Cues

Trigger this skill when user asks for:
- "分析这个库有哪些重复设计/冗余设计"
- "做一个非常完整详细的 todolist/执行计划"
- "每改一处就测试并更新计划状态"
- "按步骤推进并可追踪"

## Execution Rules

- Prefer small, reversible steps over large refactors.
- Keep plan language specific to file paths, symbols, and commands.
- Avoid mixing analysis conclusions with unverified assumptions.
- If new evidence contradicts earlier assumptions, revise plan before coding.
