---
name: codex-workflow-autopilot
description: Generate execution workflows from confirmed intent using behavioral modes, BMAD phases, checkpoints, and Phase X verification. Route build, fix, review, debug, and docs tasks into ordered steps with exit criteria.
load_priority: on-demand
---

## TL;DR
Route tasks by complexity: complex -> Thinking Partner + Devil's Advocate, teaching -> Teaching Mode + explain_code.py, simple -> direct execution. Map intent to workflow (build/fix/review/debug/docs). Use BMAD 4-phase for complex. Always end with Phase X quality gate.

# Workflow Autopilot

## Activation

1. Activate after intent analysis is confirmed.
2. Activate on explicit `$codex-workflow-autopilot`.
3. Activate teaching mode on `$teach`, "explain", or "walk me through".

## Behavioral Protocol Decision Tree

```
Task complexity?
    |- Complex (architecture/design/multi-file) -> activate Thinking Partner mode
    |   `- Before presenting solution -> activate Devil's Advocate mode
    |
    |- Teaching request -> activate Teaching Mode + explain_code.py
    |
    `- Simple (single file fix) -> direct execution
```

## Behavioral Modes

| Signals | Mode | Behavior |
| --- | --- | --- |
| what if, ideas, options | brainstorm | ask clarifying questions and present alternatives, no code |
| think with me, compare options, help me decide | thinking-partner | co-think with tradeoff-first framing and explicit decision criteria |
| build, create, implement | implement | execute quickly with production-focused output |
| error, bug, broken | debug | reproduce, isolate, root-cause, fix, regression-test |
| review, audit, check | review | inspect and report findings by severity |
| challenge this, poke holes, red team, counterargument | devils-advocate | stress-test assumptions, expose risks, and propose mitigations |
| explain, teach, learn | teach | explain progressively with examples |
| deploy, release, ship | ship | prioritize stability and complete checks |

## Thinking-Partner Trigger

Trigger this mode when user asks for collaborative reasoning rather than immediate implementation.

- Signal examples: "think with me", "compare options", "which approach is better", "help me decide".
- Load and apply: `references/thinking-partner-mode.md`.
- Ask focused clarifying questions before proposing workflow.
- Present option matrix with tradeoffs, risks, and recommended path.
- Convert selected path back to workflow steps and exit criteria.

## Devil's Advocate Trigger

Trigger this mode when user asks for challenge, risk probing, or plan hardening.

- Signal examples: "be critical", "find blind spots", "red team this plan", "play devil's advocate".
- Load and apply: `references/devils-advocate-mode.md`.
- Attack assumptions explicitly and rank findings by impact/likelihood.
- Provide mitigation actions and clear stop/ship criteria.
- Return to normal workflow mode only after key risks are addressed or explicitly accepted.

## Teaching Mode Trigger

Trigger this mode when user asks to understand project code, not to modify it.

- Signal examples: `$teach`, "explain this", "teach me", "how does this work", "walk me through".
- Load and apply: `references/teaching-mode-spec.md`.
- Prefer project-specific explanation over generic language/framework theory.
- Use `scripts/explain_code.py` as optional context helper for functions/imports/imported-by mapping.
- Output in four layers: what, how, why, connections, then gotchas.
- Keep scope tight to user request (function/file/module) and avoid unnecessary full-file dumps.

## Intent to Workflow

| Intent | Steps | Exit Criteria |
| --- | --- | --- |
| build | analyze -> plan -> implement -> test -> docs -> gate | tests pass, docs checked, gate pass |
| fix | reproduce -> isolate -> root-cause -> fix -> regression-test -> docs -> gate | root cause identified, regression test pass, gate pass |
| review | inspect -> categorize findings -> recommend actions | findings documented with severity |
| debug | reproduce -> hypotheses -> verify/eliminate -> fix -> regression-test -> gate | verified fix with evidence, gate pass |
| docs | scope change -> update docs -> verify links/accuracy -> gate | docs updated and verified |

## BMAD for Complex Requests

Use BMAD when intent analysis marks `complexity: complex`.

### Phase 1: Analysis (no code)

- confirm requirements and constraints
- inspect existing patterns
- capture key decisions

### Phase 2: Planning (no code)

- create plan via `$codex-plan-writer`
- define task-level input/output/verify

Checkpoint: wait for explicit user approval before Phase 3.

### Phase 3: Solutioning (no code)

- finalize architecture and data flow decisions
- identify cross-file impacts

### Phase 4: Implementation (code)

- implement task by task
- run tests/docs as workflow requires

### Phase X: Verification (always last)

1. Run `$codex-execution-quality-gate`.
2. If gate fails, fix blockers and rerun.
3. Do not declare completion before gate decision.

## Reference Files

- `references/thinking-partner-mode.md`: use only when collaborative option analysis is requested.
- `references/devils-advocate-mode.md`: use only when explicit challenge/risk probing is requested.
- `references/teaching-mode-spec.md`: use when user asks for code walkthrough, explanation, or teaching.
- `references/workflow-create.md`: execution template for new feature workflows.
- `references/workflow-debug.md`: execution template for debugging workflows.
- `references/workflow-review.md`: execution template for review workflows.
- `references/workflow-refactor.md`: execution template for refactoring workflows.
- `references/workflow-deploy.md`: execution template for deployment workflows.
- `references/workflow-handoff.md`: execution template for session handoff workflows.

## Helper Script

- `scripts/explain_code.py`:
  - Windows:
    `python "$env:USERPROFILE\.codex\skills\codex-workflow-autopilot\scripts\explain_code.py" --project-root <path> --file <relative-or-absolute-file>`
  - macOS/Linux:
    `python "$HOME/.codex/skills/codex-workflow-autopilot/scripts/explain_code.py" --project-root <path> --file <relative-or-absolute-file>`

## Script Invocation Discipline

1. Always run `--help` before invoking a script.
2. Treat scripts as black-box helpers and prefer direct execution over source inspection.
3. Read script source only when customization or bug fixing is required.

## Overrides

- "skip test": remove test step and warn quality confidence is reduced.
- "no docs": remove docs step and warn maintainability confidence is reduced.
- "just do it": default to build workflow and still show brief step plan.
- "skip plan": allow for simple scope; for complex scope warn and reconfirm.

## Scope Heuristic

- small: 1-3 files, single concern
- medium: 4-10 files, multiple concerns
- large: 10+ files or architectural impact

## Output Contract

Return fenced JSON in conversation:

```json
{
  "mode": "brainstorm | thinking-partner | implement | debug | review | devils-advocate | teach | ship",
  "workflow_type": "build | fix | review | debug | docs | refactor | deploy | handoff",
  "steps": ["step1", "step2"],
  "exit_criteria": ["criterion1"],
  "estimated_scope": "small | medium | large",
  "phase": "analysis | planning | solutioning | implementation | verification"
}
```

Execution remains sequential for MVP.
