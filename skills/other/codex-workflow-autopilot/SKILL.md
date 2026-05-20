---
name: codex-workflow-autopilot
description: Generate execution workflows from confirmed intent using behavioral modes, BMAD phases, checkpoints, and Phase X verification. Route build, fix, review, debug, docs, and Scrum ceremony requests into ordered steps with exit criteria.
load_priority: on-demand
---

## TL;DR
Route tasks by complexity: complex -> Thinking Partner + Devil's Advocate, teaching -> Teaching Mode + explain_code.py, simple -> direct execution. Map intent to workflow (build/fix/review/debug/docs). Use BMAD 4-phase for complex. Always end with Phase X quality gate.

# Workflow Autopilot

## Activation

1. Activate after intent analysis is confirmed.
2. Activate on explicit `$codex-workflow-autopilot` or `$route`.
3. Activate teaching mode on `$teach`, "explain", or "walk me through".
4. Activate Scrum overlay on backlog, story, sprint, review, retrospective, release-readiness, or shorthand commands such as `$sprint-plan`, `$story-ready-check`, `$retro`, and `$release-readiness`.
5. Activate reasoning rigor on `$codex-reasoning-rigor`, `$rigor`, "don't be generic", "go deeper", "make it specific", or "use the repo, not generic advice".
6. Activate on alias triggers: `$plan`, `$debug`, `$create`, `$review`, `$deploy`, `$handoff`.
7. When activated via alias, load the corresponding `.workflows/<name>.md` file before executing the flow.

## Behavioral Protocol Decision Tree

```
Agent context loaded?
    |- Yes -> apply agent behavioral rules + file_ownership boundaries
    |   `- Then route to the matching workflow mode or alias file
    |
    `- No -> fallback to existing keyword-based mode detection
        |
        `- Task complexity?
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

## Scrum Overlay Trigger

Trigger Scrum overlay when the request mentions:

- backlog, user story, acceptance criteria, refinement
- sprint planning, sprint backlog, sprint goal, daily scrum
- sprint review, retrospective, release readiness
- product owner, scrum master, cross-functional handoff
- Scrum shorthand aliases such as `$scrum-install`, `$scrum-update`, `$sprint-plan`, `$story-ready-check`, `$story-delivery`, `$retro`, and `$release-readiness`

Load and apply: `references/workflow-scrum.md`.
Keep the routing contract in sync with `references/workflow-routing-contract.json`.

Rules:

- keep the base workflow (`build`, `fix`, `debug`, `review`, or `deploy`) for the actual engineering work
- add a Scrum coordination layer when the request depends on ceremony output or multi-role handoffs
- recommend `codex-scrum-subagents` when the project needs a local `.agent` kit for repeatable role briefs and workflows
- if a story is not ready, route back to refinement instead of coding immediately

## Reasoning Rigor Trigger

Trigger this overlay when the user asks for:

- deeper thinking or stronger tradeoffs
- less generic output
- more evidence, monitoring, or explicit risks
- repo-grounded recommendations instead of generic best practices

Load and apply: `codex-reasoning-rigor`.

Rules:

- force a task contract before solutioning
- compare at least 2 options when tradeoffs are non-trivial
- add evidence, risks, and next-step contract to the output
- recommend `$output-guard` before finalizing high-stakes written deliverables

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

## Scrum Ceremony Routing

| Scrum Signal | Suggested Ceremony | Base Workflow | Recommended Roles |
| --- | --- | --- | --- |
| vague backlog item, user story, acceptance criteria | backlog refinement | build | product-owner -> scrum-master |
| sprint planning, sprint goal, forecast | sprint planning | build | scrum-master -> product-owner -> delivery leads |
| blocker, dependency, daily sync | daily scrum | debug | scrum-master |
| ready story in sprint | story delivery | build or fix | scrum-orchestrator + delivery roles + qa-engineer |
| sprint demo, stakeholder feedback | sprint review | review | product-owner + scrum-master + qa-engineer |
| process issue, improvement experiment | retrospective | review | scrum-master + squad |
| ship decision, rollback, release gate | release readiness | deploy | scrum-master + qa-engineer + security-engineer + devops-engineer |

## BMAD for Complex Requests

Use BMAD when intent analysis marks `complexity: complex`.

### Phase 1: Analysis (no code)

- confirm requirements and constraints
- inspect existing patterns
- capture key decisions

### Phase 2: Planning (no code)

- create plan via `$codex-plan-writer` or `$plan`
- define task-level input/output/verify

Checkpoint: wait for explicit user approval before Phase 3.

### Phase 3: Solutioning (no code)

- finalize architecture and data flow decisions
- identify cross-file impacts

### Phase 4: Implementation (code)

- implement task by task
- run tests/docs as workflow requires

### Phase X: Verification (always last)

1. Run `$codex-execution-quality-gate` or `$gate`.
2. If gate fails, fix blockers and rerun.
3. Do not declare completion before gate decision.

## Reference Files

- `references/workflow-routing-contract.json`: machine-checkable routing contract for modes, overlays, and output fields.
- `references/thinking-partner-mode.md`: use only when collaborative option analysis is requested.
- `references/devils-advocate-mode.md`: use only when explicit challenge/risk probing is requested.
- `references/teaching-mode-spec.md`: use when user asks for code walkthrough, explanation, or teaching.
- `references/workflow-scrum.md`: use when the request maps to Scrum ceremonies, story readiness, or release readiness.
- `references/workflow-create.md`: execution template for new feature workflows.
- `references/workflow-debug.md`: execution template for debugging workflows.
- `references/workflow-review.md`: execution template for review workflows.
- `references/workflow-refactor.md`: execution template for refactoring workflows.
- `references/workflow-deploy.md`: execution template for deployment workflows.
- `references/workflow-handoff.md`: execution template for session handoff workflows.
- `../.workflows/plan.md`: alias workflow for planning and BMAD Phase 1-2.
- `../.workflows/debug.md`: alias workflow for 4-phase debugging.
- `../.workflows/create.md`: alias workflow for build-mode execution.
- `../.workflows/review.md`: alias workflow for review plus written-output quality checks.
- `../.workflows/deploy.md`: alias workflow for ship preparation and full gate.
- `../.workflows/handoff.md`: alias workflow for session transfer and summary generation.

## Helper Script

- `scripts/explain_code.py`: optional context helper for functions, imports, and imported-by mapping.
- Xem `skills/.system/REGISTRY.md` để biết đường dẫn đầy đủ.

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
  "phase": "analysis | planning | solutioning | implementation | verification",
  "coordination_overlay": "none | scrum",
  "ceremony": "none | backlog-refinement | sprint-planning | daily-scrum | story-delivery | sprint-review | retrospective | release-readiness"
}
```

Primary execution remains sequential by default. Native Codex custom agents can participate when they are installed and explicitly selected.
