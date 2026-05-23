---
name: plan-hard
version: 1.0.0
description: '[Planning] Research, analyze, and create an implementation plan'
disable-model-invocation: false
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` before executing.

- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)
- `docs/test-specs/` — Test specifications by module (read existing TCs to include test strategy in plan)

> **Phase Quality:** **MUST READ** `.claude/skills/shared/iterative-phase-quality-protocol.md`.
> Each phase file MUST satisfy: ≤5 files per phase, ≤3h effort, clear success criteria, mapped test cases.

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

## Quick Summary

**Goal:** Research, analyze the codebase, and create a detailed phased implementation plan with user collaboration.

**Workflow:**

1. **Pre-Check** — Detect active/suggested plan or create new directory
2. **Research** — Parallel researcher subagents explore different aspects (max 5 tool calls each)
3. **Codebase Analysis** — Read backend-patterns-reference.md, frontend-patterns-reference.md, project-structure-reference.md; scout if needed
4. **Plan Creation** — Planner subagent creates plan.md + phase-XX files with full sections
5. **Post-Validation** — Optionally interview user to confirm decisions via /plan-validate

**Key Rules:**

- PLANNING ONLY: do NOT implement or execute code changes
- Always run /plan-review after plan creation
- Ask user to confirm before any next step
- **MANDATORY IMPORTANT MUST** detect new tech/lib in plan and create validation task (see New Tech/Lib Gate below)

## New Tech/Lib Gate (MANDATORY for all plans)

**MANDATORY IMPORTANT MUST** after plan creation, detect new tech/packages/libraries not in the project. If found: `TaskCreate` per lib → WebSearch top 3 alternatives → compare (fit, size, community, learning curve, license) → recommend with confidence % → `AskUserQuestion` to confirm. **Skip if** plan uses only existing dependencies.

## Greenfield Mode

> **Auto-detected:** If no existing codebase is found (no code directories like `src/`, `app/`, `lib/`, `server/`, `packages/`, etc., no manifest files like `package.json`/`*.sln`/`go.mod`, no populated `project-config.json`), this skill switches to greenfield mode automatically. Planning artifacts (docs/, plans/, .claude/) don't count — the project must have actual code directories with content.

**When greenfield is detected:**

1. Skip codebase analysis phase (researcher subagents that grep code)
2. **Replace with:** market research + business evaluation phase using WebSearch + WebFetch
3. Delegate architecture decisions to `solution-architect` agent
4. Output: `plans/{id}/plan.md` with greenfield-specific phases (domain model, tech stack, project structure)
5. Skip "MUST READ project-structure-reference.md" (won't exist)
6. Enable broad web research for tech landscape, best practices, framework comparisons
7. Every decision point requires AskUserQuestion with 2-4 options + confidence %
8. **[CRITICAL] Business-First Protocol:** Tech stack decisions come AFTER full business analysis. Do NOT ask user to pick a tech stack upfront. Instead: complete business evaluation → derive technical requirements → research current market options → produce comparison report → present to user for decision. See `solution-architect` agent for the full tech stack research methodology.

- Research reports <=150 lines; plan.md <=80 lines
- **External Memory**: Write all research and analysis to `.ai/workspace/analysis/{task-name}.analysis.md`. Re-read ENTIRE analysis file before generating plan.

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

Activate `planning` skill.

## Scaffolding-First Protocol (Conditional)

**Activation conditions (ALL must be true):**

1. Active workflow is `greenfield-init` OR `big-feature`
2. AI MUST self-investigate for existing base/foundational abstractions using these patterns:
    - Abstract/base classes: `abstract class.*Base|Base[A-Z]\w+|Abstract[A-Z]\w+`
    - Generic interfaces: `interface I\w+<|IGeneric|IBase`
    - Infrastructure abstractions: `IRepository|IUnitOfWork|IService|IHandler`
    - Utility/extension layers: `Extensions|Helpers|Utils|Common` (directories or classes)
    - Frontend foundations: `base.*component|base.*service|base.*store|abstract.*component` (case-insensitive)
    - DI/IoC registration: `AddScoped|AddSingleton|providers:|NgModule|@Injectable`
3. If existing scaffolding found → **SKIP.** Log: "Existing scaffolding detected at {file:line}. Skipping Phase 1 scaffolding."
4. If NO foundational abstractions found → **PROCEED** with scaffolding phase.

**When activated:**

Phase 1 of the plan MUST be **Architecture Scaffolding** — all base abstract classes, generic interfaces, infrastructure abstractions, and DI registration with OOP/SOLID principles. Runs BEFORE feature stories. AI self-investigates what base classes the tech stack needs. All infrastructure behind interfaces with at least one concrete implementation (Dependency Inversion).

**When skipped:** Plan proceeds normally — feature stories build on existing base classes.

## PLANNING-ONLY — Collaboration Required

> **DO NOT** use the `EnterPlanMode` tool — you are ALREADY in a planning workflow.
> **DO NOT** implement or execute any code changes.
> **COLLABORATE** with the user: ask decision questions, present options with recommendations.
> After plan creation, ALWAYS run `/plan-review` to validate the plan.
> ASK user to confirm the plan before any next step.

## Your mission

<task>
$ARGUMENTS
</task>

## Pre-Creation Check (Active vs Suggested Plan)

Check the `## Plan Context` section in the injected context:

- If "Plan:" shows a path -> Active plan exists. Ask user: "Continue with this? [Y/n]"
- If "Suggested:" shows a path -> Branch-matched hint only. Ask if they want to activate or create new.
- If "Plan: none" -> Create new plan using naming from `## Naming` section.

## Workflow

1. If creating new: Create directory using `Plan dir:` from `## Naming` section, then run `node .claude/scripts/set-active-plan.cjs {plan-dir}`
   If reusing: Use the active plan path from Plan Context.
   Make sure you pass the directory path to every subagent during the process.
2. Follow strictly to the "Plan Creation & Organization" rules of `planning` skill.
3. Use multiple `researcher` agents (max 2 agents) in parallel to research for this task:
   Each agent research for a different aspect of the task and are allowed to perform max 5 tool calls.
4. Analyze the codebase by reading `backend-patterns-reference.md`, `frontend-patterns-reference.md`, and `project-structure-reference.md` file.
   **ONLY PERFORM THIS FOLLOWING STEP IF reference docs are placeholders or older than 3 days**: Use `/scout <instructions>` slash command to search the codebase for files needed to complete the task.
5. Main agent gathers all research and scout report filepaths, and pass them to `planner` subagent with the prompt to create an implementation plan of this task.
6. Main agent receives the implementation plan from `planner` subagent, and ask user to review the plan

## Post-Plan Validation (Optional)

After plan creation, offer validation interview to confirm decisions before implementation.

**Check `## Plan Context` -> `Validation: mode=X, questions=MIN-MAX`:**

| Mode     | Behavior                                                                         |
| -------- | -------------------------------------------------------------------------------- |
| `prompt` | Ask user: "Validate this plan with a brief interview?" -> Yes (Recommended) / No |
| `auto`   | Automatically execute `/plan-validate {plan-path}`                               |
| `off`    | Skip validation step entirely                                                    |

**If mode is `prompt`:** Use `AskUserQuestion` tool with options above.
**If user chooses validation or mode is `auto`:** Execute `/plan-validate {plan-path}` SlashCommand.

## Output Requirements

**Plan Directory Structure** (use `Plan dir:` from `## Naming` section)

```
{plan-dir}/
├── research/
│   ├── researcher-XX-report.md
│   └── ...
├── reports/
│   ├── XX-report.md
│   └── ...
├── scout/
│   ├── scout-XX-report.md
│   └── ...
├── plan.md
├── phase-XX-phase-name-here.md
└── ...
```

**Research Output Requirements**

- Ensure every research markdown report remains concise (<=150 lines) while covering all requested topics and citations.

**Plan File Specification**

- Every `plan.md` MUST start with YAML frontmatter:

    ```yaml
    ---
    title: '{Brief title}'
    description: '{One sentence for card preview}'
    status: pending
    priority: P2
    effort: { sum of phases, e.g., 4h }
    story_points: { sum of phase SPs, e.g., 8 }
    branch: { current git branch }
    tags: [relevant, tags]
    created: { YYYY-MM-DD }
    ---
    ```

- Save overview at `{plan-dir}/plan.md` (<80 lines): list each phase with status, progress, and links to phase files.
- For each phase, create `{plan-dir}/phase-XX-phase-name-here.md` with sections: Context links, Overview, Key Insights, Requirements, **Alternatives Considered** (minimum 2 approaches with pros/cons), **Design Rationale** (WHY chosen approach), Architecture, **UI Layout** (see below), Related code files, Implementation Steps, Todo list, Success Criteria, Risk Assessment, Security Considerations, Next steps.
- **UI Layout**: For frontend-facing phases, include ASCII wireframe per `.claude/skills/shared/ui-wireframe-protocol.md`. Classify components by tier (common/domain-shared/page-app). For backend-only phases: `## UI Layout` → `N/A — Backend-only change.`

## **IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using `TaskCreate`
- Always add a final review todo task to verify work quality and identify fixes/enhancements
- **MANDATORY FINAL TASKS:** After creating all planning todo tasks, ALWAYS add these two final tasks:
    1. **Task: "Run /plan-validate"** — Trigger `/plan-validate` skill to interview the user with critical questions and validate plan assumptions
    2. **Task: "Run /plan-review"** — Trigger `/plan-review` skill to auto-review plan for validity, correctness, and best practices

## Important Notes

**IMPORTANT:** Analyze the skills catalog and activate the skills that are needed for the task during the process.
**IMPORTANT:** Ensure token efficiency while maintaining high quality.
**IMPORTANT:** Sacrifice grammar for the sake of concision when writing reports.
**IMPORTANT:** In reports, list any unresolved questions at the end, if any.

## REMINDER — Planning-Only Command

> **DO NOT** use `EnterPlanMode` tool.
> **DO NOT** start implementing.
> **ALWAYS** validate with `/plan-review` after plan creation.
> **ASK** user to confirm the plan before any implementation begins.
> **ASK** user decision questions with your recommendations when multiple approaches exist.

---

## Standalone Review Gate (Non-Workflow Only)

> **MANDATORY IMPORTANT MUST:** If this skill is called **outside a workflow** (standalone `/plan-hard`), the generated plan MUST include `/review-changes` as a **final phase/task** in the plan. This ensures all implementation changes get reviewed before commit even without a workflow enforcing it.
>
> If already running inside a workflow (e.g., `feature`, `bugfix`), skip this — the workflow sequence handles `/review-changes` at the appropriate step.

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/plan-review (Recommended)"** — Validate plan before implementation
- **"/plan-validate"** — Interview user to confirm plan decisions
- **"Skip, continue manually"** — user decides

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
