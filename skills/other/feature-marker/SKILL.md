---
name: feature-marker
description: >
  Skill-first run-through feature workflow for Claude, Codex, and Gemini.
  Use when the user asks to implement a feature through PRD, TechSpec, Tasks,
  verification, local commit, and branch handoff. The npm package installs
  skill files only; the LLM skill performs the workflow.
---

# feature-marker

Use this skill when the user asks to implement, plan, test, or hand off a
feature with Feature Marker.

The normal invocation is a plain LLM prompt:

```text
Use feature-marker to implement <feature-slug>.
```

Run through the feature by default. Do not use an interactive menu, old CLI
workflow commands, checkpoint JSON, or a JavaScript workflow engine. The package
installer only installs this skill.

## Run-Through Procedure

1. Identify the feature slug from the prompt. If the slug is missing, derive a
   short kebab-case slug from the feature request.
2. Read repo state: current branch, base branch, git status, project files, and
   any existing `tasks/{slug}/prd.md`, `tasks/{slug}/techspec.md`, and
   `tasks/{slug}/tasks.md`.
3. Stop before implementation only when:
   - the feature request is too ambiguous to produce useful artifacts;
   - the checkout has unrelated uncommitted work and the user has not approved
     a worktree or cleanup path;
   - required verification or project setup is blocked.
4. Use branch-first isolation. If the current branch is `main`, `master`,
   `develop`, or `trunk`, create `feature-marker/{slug}` unless the user gave a
   branch name. Use a git worktree only when the checkout is dirty or the user
   asks for one.
5. Create or reuse artifacts in `tasks/{slug}/` using the bundled templates:
   - `templates/prd-template.md` -> `tasks/{slug}/prd.md`
   - `templates/techspec-template.md` -> `tasks/{slug}/techspec.md`
   - `templates/tasks-template.md` -> `tasks/{slug}/tasks.md`
   Replace `{slug}` and `{feature_title}`, fill every relevant section, and do
   not leave unresolved template placeholders in committed artifacts.
6. Run an implementation grill pass before coding. Challenge the artifacts for
   missing acceptance criteria, weak task order, risky files, data/migration
   impact, missing tests, unclear edge cases, and handoff gaps.
7. Resolve grill findings in `tasks/{slug}/` before implementation. Ask the
   user only when a finding changes scope or requires a product decision.
   Otherwise continue without a generic artifact approval gate.
8. Implement only the tasks in `tasks/{slug}/tasks.md`. Keep changes scoped to
   the feature and preserve unrelated local edits.
9. Run project-appropriate verification. If a command fails, fix the issue when
   it is in scope; otherwise report the exact blocker and stop.
10. Commit the feature locally when implementation and verification are complete,
   unless the user prohibited commits. Do not push or open a PR automatically.
11. Print the branch handoff with exact commands:

```bash
git push -u origin <branch>
gh pr create --base <base-branch> --head <branch>
```

## Artifact State

The canonical state is user-facing markdown:

```text
tasks/{slug}/
  prd.md
  techspec.md
  tasks.md
```

Optional verification notes may also live under `tasks/{slug}/` when they help
future continuation, but checkpoint JSON is not the source of truth.

## Prompt Intents

There are no CLI workflow modes. Treat these as prompt intents:

- `full`: run the complete PRD -> TechSpec -> Tasks -> implementation grill ->
  implementation -> tests -> branch handoff flow.
- `tasks-only`: use existing artifacts and implement the task list.
- `test-only`: run verification on the current feature branch and report
  results.
- `prd-only`: create or revise only `tasks/{slug}/prd.md`.

`spec-driven` and `ralph-loop` are out of scope for this skill-first v1 unless
they are rebuilt as explicit skill instructions.
