---
name: definition.story_map
phase: definition
roles:
  - Product Designer
  - Product Manager
description: Generate a structured user story map to visualize workflows, user goals, and release slices.
variables:
  required:
    - name: persona
      description: Persona or user type represented in the journey.
    - name: primary_goal
      description: Core job-to-be-done or outcome for the persona.
  optional:
    - name: stages
      description: Ordered list of journey stages or activities.
    - name: constraints
      description: Notable constraints or assumptions guiding scope.
outputs:
  - Story map with activities, tasks, and release slices.
  - Narrative summary capturing insights and alignment considerations.
  - Export-friendly table for backlog tooling.
---

# Purpose
Support cross-functional alignment on scope by visualizing how users progress through key activities and what increments deliver value.

# Pre-run Checklist
- ✅ Review discovery insights to confirm persona and goal accuracy.
- ✅ Align with engineering on technical constraints or dependencies.
- ✅ Gather any existing journey maps or service blueprints for reference.

# Invocation Guidance
```bash
codex run --skill definition.story_map \
  --vars "persona={{persona}}" \
         "primary_goal={{primary_goal}}" \
         "stages={{stages}}" \
         "constraints={{constraints}}"
```

# Recommended Input Attachments
- Screens or prototypes covering the journey.
- Notes from field studies or shadowing sessions.

# Claude Workflow Outline
1. Outline the persona, goal, and context.
2. Create a story map table with columns for stages, activities, tasks, and candidate releases.
3. Highlight assumptions, dependencies, and instrumentation needs per slice.
4. Provide a narrative summary and collaboration checkpoints.
5. Suggest export steps for tools like FigJam, Miro, or backlog systems.

# Output Template
```
## Story Map Overview
Persona: {{persona}}
Goal: {{primary_goal}}

## Story Map
| Stage | User Activity | Tasks | Release Slice | Notes |
| --- | --- | --- | --- | --- |

## Alignment Notes
- Assumptions:
- Dependencies:
- Instrumentation:
```

# Follow-up Actions
- Review the map with design, engineering, and product marketing for feedback.
- Break down release slices into backlog items with acceptance criteria.
- Track updates in the squad planning workspace.
