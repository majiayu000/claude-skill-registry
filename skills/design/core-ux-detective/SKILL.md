---
name: core-ux-detective
description: >
  Discover, define and canonicalize the core user tasks and user paths of the application.
  Use when (1) mapping what users can actually do in the app, (2) defining canonical user
  journeys/flows, (3) creating the AI-readable user model (core-user-model.json),
  (4) reviewing whether a new feature introduces a new core path, (5) other skills
  (help, marketing, onboarding) need authoritative task/path definitions to consume.
  Triggers: "core tasks", "user paths", "user journeys", "UX model", "what can users do",
  "core flows", "user model", "canonical tasks", file types: core-user-model.json.
---

# Core UX Detective

Discover and canonicalize the TRUE core user tasks and user paths.

This skill is the **single source of truth** for what users can do in the application.
Other skills (help, marketing, onboarding) MUST consume this output and MUST NOT redefine
core tasks or paths independently.

## Authority

- ONLY this skill identifies core user actions
- ONLY this skill defines user paths
- ONLY this skill names steps canonically
- ONLY this skill decides primary vs secondary flow

## Workflow

### 1. Gather Inputs

Collect from any available source:
- **Codebase**: Routes, pages, components, hooks (especially `src/pages/`, `src/components/`)
- **PRD**: `Docs/01-PRD.md`
- **Feature lists**: `Docs/context/packages-map.md`, `Docs/context/repo-structure.md`
- **Existing model**: `Docs/ai/core-user-model.json` (if it exists)
- **UI screenshots or verbal descriptions** from user

### 2. Identify Core User Tasks

Extract user-facing actions. Rules:
- **User-facing only** — not technical internals (no "hydrate cache", "run migration")
- **Clear, neutral language** — no marketing ("revolutionary") or help tone ("click here")
- **Finnish labels** — this is a Finnish-first app; use Finnish for `label`
- **Conservative** — fewer well-defined tasks > many vague tasks

Each task needs:
```json
{
  "id": "snake_case_stable_id",
  "label": "Finnish label",
  "intent": "Why the user does this (English)",
  "appears_in": ["page_or_context_ids"],
  "draft": false
}
```

Mark `"draft": true` if uncertain about the task's scope or permanence.

### 3. Define User Paths

Group tasks into meaningful journeys. Each path:
- Has a clear user intent
- Has ordered steps (referencing task IDs)
- Has a beginning and an end
- Is explicitly defined (overlapping steps between paths is fine)

```json
{
  "id": "path_snake_case",
  "label": "Finnish path label",
  "intent": "What the user accomplishes (English)",
  "primary": true,
  "steps": ["task_id_1", "task_id_2", "task_id_3"]
}
```

- `primary: true` = core journey most users follow
- `primary: false` = secondary/power-user flow

### 4. Output Schema

Save to `Docs/ai/core-user-model.json`:

```json
{
  "$schema": "core-user-model-v1",
  "updated": "YYYY-MM-DD",
  "core_tasks": [ ... ],
  "user_paths": [ ... ]
}
```

### 5. Validate

After writing the model:
- Every step in `user_paths[].steps` must reference a valid `core_tasks[].id`
- No orphan tasks (every task appears in at least one path, or is marked `draft`)
- No duplicate IDs
- Labels are Finnish, intents are English

## Rules

- **Conservative**: fewer paths > many vague paths
- **Clarity over completeness**: a well-defined subset beats a fuzzy comprehensive list
- **Stable IDs**: once an ID is published, do not rename it (add new, deprecate old)
- **No marketing or instructional text** in the model
- **Draft flag**: if unsure, set `"draft": true` — other skills skip draft items

## Discovery Strategy

When analyzing the codebase to find core tasks:

1. **Routes** — each route = potential user task or context
2. **Page components** — what actions does each page enable?
3. **Hooks with user state** — `useAuth`, `useReelDraft`, `useBookmarks` etc. reveal capabilities
4. **UI action buttons** — buttons/links with Finnish labels reveal user-facing actions
5. **Database tables with `user_id`** — each user-owned table hints at a core task

For detailed discovery patterns, see [references/discovery-patterns.md](references/discovery-patterns.md).

## Consuming the Model

Other skills read `Docs/ai/core-user-model.json` and:
- Use `core_tasks[].id` as canonical references
- Use `core_tasks[].label` for Finnish UI text
- Use `user_paths` for onboarding flows, help guides, marketing funnels
- Never redefine or rename tasks — request changes via this skill
