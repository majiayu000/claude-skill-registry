---
name: cook
version: 1.0.0
description: '[Implementation] Implement a feature [step by step]'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` before executing.

- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)
- `docs/test-specs/` — Test specifications by module (read existing TCs; generate/update test specs via `/tdd-spec` after implementation)

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

> **Process Discipline:** MUST READ `.claude/skills/shared/rationalization-prevention-protocol.md` (anti-evasion) AND `.claude/skills/shared/red-flag-stop-conditions-protocol.md` (when to STOP and reassess).

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

## Quick Summary

**Goal:** Implement a feature step-by-step with research, planning, execution, and verification.

**Workflow:**

1. **Question** — Clarify requirements via AskUserQuestion; challenge assumptions
2. **Research** — Use researcher subagents in parallel; scout codebase for patterns
3. **Plan** — Create implementation plan, get user approval
4. **Implement** — Execute with skill activation, code-simplifier, review-changes

**Key Rules:**

- Parent skill for all cook-\* variants (cook-auto, cook-fast, cook-hard, cook-parallel)
- Write research findings to `.ai/workspace/analysis/` for context preservation
- Always activate relevant skills from catalog during implementation
- Break work into small todo tasks; add final review task

### Frontend/UI Context (if applicable)

When this task involves frontend or UI changes, **MUST READ** `.claude/skills/shared/ui-system-context.md` and the following docs:

- Component patterns: `docs/project-reference/frontend-patterns-reference.md`
- Styling/BEM guide: `docs/project-reference/scss-styling-guide.md`
- Design system tokens: `docs/project-reference/design-system/README.md`

<HARD-GATE>
Do NOT start coding until you have a plan (approved or self-created) and have searched
the codebase for 3+ similar implementations. This applies to EVERY feature regardless
of perceived simplicity. "Simple" features have hidden complexity.
</HARD-GATE>

## Per-Phase Quality Cycle (MANDATORY)

<HARD-GATE>
Follow `.claude/skills/shared/iterative-phase-quality-protocol.md`:
Each plan phase = one quality cycle (plan→implement→review→fix→verify).
DO NOT start next phase until current phase passes VERIFY.
After each phase: re-assess remaining phases for scope changes.
</HARD-GATE>

## Greenfield Mode

> **Auto-detected:** If no existing codebase is found (no code directories like `src/`, `app/`, `lib/`, `server/`, `packages/`, etc., no manifest files like `package.json`/`*.sln`/`go.mod`, no populated `project-config.json`), this skill switches to greenfield mode automatically. Planning artifacts (docs/, plans/, .claude/) don't count — the project must have actual code directories with content.

**When greenfield is detected:**

1. If an **approved plan exists** in `plans/`: scaffold project structure from the plan
2. If **no approved plan**: redirect to `/plan` first — "No approved plan found. Run /plan first to create a greenfield project plan."
3. Generate: folder layout, starter files, build config, CI skeleton, CLAUDE.md
4. Skip codebase pattern search (no patterns exist yet)
5. Use plan's tech stack decisions to generate project scaffold
6. After scaffolding, run `/project-config` to populate project configuration

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

## Variant Decision Guide

| If implementation needs...  | Use                   | Why                                     |
| --------------------------- | --------------------- | --------------------------------------- |
| Quick, straightforward      | `/cook-fast`          | Skip deep research, minimal planning    |
| Complex, multi-layer        | `/cook-hard`          | Maximum verification, subagent research |
| Backend + frontend parallel | `/cook-parallel`      | Parallel fullstack-developer agents     |
| Full autonomous execution   | `/cook-auto`          | Minimal user interaction                |
| Fast autonomous             | `/cook-auto-fast`     | Auto + skip deep research               |
| Parallel autonomous         | `/cook-auto-parallel` | Auto + parallel agents                  |
| General/interactive         | `/cook` (this skill)  | Step-by-step with user collaboration    |

Think harder to plan & start working on these tasks:
<tasks>$ARGUMENTS</tasks>

---

## Your Approach

1. **Question Everything**: Use `AskUserQuestion` tool to fully understand the request, constraints, and true objectives. Don't assume — clarify until certain.
2. **Brutal Honesty**: Provide frank feedback. If something is unrealistic or over-engineered, say so directly. Prevent costly mistakes.
3. **Explore Alternatives**: Consider multiple approaches. Present 2-3 viable solutions with clear pros/cons.
4. **Challenge Assumptions**: Question the initial approach. Often the best solution differs from what was originally envisioned.
5. **Consider All Stakeholders**: Evaluate impact on end users, developers, operations team, and business objectives.

---

## Workflow

**IMPORTANT:** Analyze the skills catalog at `.claude/skills/*` and activate needed skills during the process.

### Research

- Use multiple `researcher` subagents in parallel to explore the request, validate ideas, and find best solutions.
- Keep research reports concise (≤150 lines) with citations.
- Use `/scout-ext` (preferred) or `/scout` (fallback) to search the codebase.
- **External Memory**: Write all research findings to `.ai/workspace/analysis/{task-name}.analysis.md`. Re-read ENTIRE file before planning.

### Plan

- Use `planner` subagent to create an implementation plan using progressive disclosure structure.
- Create directory using plan naming pattern, save overview at `plan.md` (under 80 lines).
- For each phase: `phase-XX-name.md` with Context, Overview (date/priority/status), Key Insights, Requirements, Architecture, Related Code Files, Implementation Steps, Todo List, Success Criteria, Risk Assessment, Security Considerations, Next Steps.

### Implementation

- Use `/code` slash command to implement the plan step by step.
- Use `ui-ux-designer` subagent for frontend work per `./docs/design-guidelines.md`.
- For product UIs (dashboards, admin panels, SaaS apps), activate `/interface-design` for craft-driven design guidance.
- For marketing pages, landing pages, creative UIs, or screenshot replication, activate `/frontend-design` for distinctive design with bold aesthetics.
- Run type checking and compile to verify no syntax errors.

**Subagent Context Discipline:**

- **Provide full task text** — paste task content into subagent prompt; don't make subagent read plan file
- **"Ask questions before starting"** — subagent should surface uncertainties before implementing
- **Self-review before reporting** — subagent checks completeness, quality, YAGNI before returning results

### Batch Checkpoint (Large Plans)

For plans with 10+ tasks, execute in batches with human review:

1. **Execute batch** — Complete next 3 tasks (or user-specified batch size)
2. **Report** — Show what was implemented, verification output, any concerns
3. **Wait** — Say "Ready for feedback" and STOP. Do NOT continue automatically.
4. **Apply feedback** — Incorporate changes, then execute next batch
5. **Repeat** until all tasks complete

<HARD-GATE>
For plans with 10+ tasks, do NOT execute all tasks continuously without checkpoint.
Stop after every batch for human review. This prevents runaway execution where early
mistakes compound through later tasks.
</HARD-GATE>

### Testing

- Write real tests covering happy path, edge cases, and error cases.
- Use `tester` subagent to run tests. If failures: use `debugger` subagent to find root cause, fix, re-run.
- Repeat until all tests pass. Do not use fake data, mocks, or temporary solutions just to pass the build.

### Code Review

- **Two-stage review** (see `.claude/skills/shared/two-stage-task-review-protocol.md`):
    1. First: dispatch `spec-compliance-reviewer` to verify implementation matches spec
    2. Only after spec passes: dispatch `code-reviewer` for quality review
- If critical issues: fix and re-run `tester`.
- Repeat until all tests pass and code is reviewed.
- Report summary to user and ask for approval.

### Project Management & Documentation

**If user approves:** Use `project-manager` and `docs-manager` subagents in parallel to update progress and documentation.
**If user rejects:** Ask user to explain issues, fix, and repeat.

### Onboarding

- Instruct user on getting started (API keys, env vars, config) if needed.
- Help configure step by step, one question at a time.

### Final Report

- Summary of changes with next steps.
- Ask user if they want to commit and push via `git-manager` subagent.

## Red Flags — STOP (Implementation-Specific)

If you're thinking:

- "This is too simple to need a plan" — Simple tasks have hidden complexity. Plan anyway.
- "I already know how to do this" — Check codebase patterns first. Your assumptions may be wrong.
- "Let me just code it, then test" — TDD. Write the test first. Or at minimum, verify after each change.
- "The plan is close enough, I'll adapt" — Follow the plan exactly or raise concerns. Drift compounds.
- "I'll commit after I finish everything" — Commit after each task. Frequent commits prevent loss.
- "This refactor will make it better" — Only refactor what's in scope. YAGNI.
- "I can skip the review, it's obvious" — Reviews catch what authors miss. Never skip.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements

---

## Workflow Recommendation

> **IMPORTANT MUST:** If you are NOT already in a workflow, use `AskUserQuestion` to ask the user:
>
> 1. **Activate `feature` workflow** (Recommended) — scout → investigate → plan → cook → review → sre-review → test → docs
> 2. **Execute `/cook` directly** — run this skill standalone

---

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/code-simplifier (Recommended)"** — Simplify and clean up implementation
- **"/review-changes"** — Review changes before commit
- **"Skip, continue manually"** — user decides

## Standalone Review Gate (Non-Workflow Only)

> **MANDATORY IMPORTANT MUST:** If this skill is called **outside a workflow** (standalone `/cook`), you MUST create a `TaskCreate` todo task for `/review-changes` as the **last task** in your task list. This ensures all changes are reviewed before commit even without a workflow enforcing it.
>
> If already running inside a workflow (e.g., `feature`, `bugfix`), skip this — the workflow sequence handles `/review-changes` at the appropriate step.

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
