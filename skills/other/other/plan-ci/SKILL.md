---
name: plan-ci
description: "[Planning] Analyze Github Actions logs and provide a plan to fix the issues"
argument-hint: [github-actions-url]
infer: true
---

Activate `plan` skill.

> **CRITICAL:** Do NOT use `EnterPlanMode` tool — it blocks Write/Edit/Task tools needed for plan creation. Follow the workflow below.
> **Planning is collaborative:** Validate plan, ask user to confirm, surface decision questions with recommendations.

## Github Actions URL
 $ARGUMENTS

Use the `planner` subagent to read the github actions logs, analyze and find the root causes of the issues, then provide a detailed plan for implementing the fixes.

**Plan File Specification:**
- Every `plan.md` MUST start with YAML frontmatter:
  ```yaml
  ---
  title: "{Brief title}"
  description: "{One sentence for card preview}"
  status: pending
  priority: P1
  effort: {estimated fix time}
  branch: {current git branch}
  tags: [ci, bugfix]
  created: {YYYY-MM-DD}
  ---
  ```

**Output:**
Provide at least 2 implementation approaches with clear trade-offs, and explain the pros and cons of each approach, and provide a recommended approach.

## MANDATORY: Plan Collaboration Protocol (READ THIS)

- **Do NOT use `EnterPlanMode` tool** — it blocks Write/Edit/Task tools needed to create plan files and launch subagents
- **Do NOT start implementing** — plan only, wait for user approval
- **ALWAYS validate:** After plan creation, execute `/plan-review` to validate the plan
- **ALWAYS confirm:** Ask user to review and approve the plan using `AskUserQuestion` with a recommendation
- **ALWAYS surface decisions:** Use `AskUserQuestion` with recommended options for key architectural/design decisions
- **Planning = Collaboration:** The plan is shaped by user input — never treat it as a unilateral output
- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end
- Sacrifice grammar for concision. List unresolved questions at the end
