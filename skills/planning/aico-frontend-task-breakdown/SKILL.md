---
name: aico-frontend-task-breakdown
description: |
  Break down PM story into independent frontend task files following UI DEVELOPMENT order: Setup → Static UI → Dynamic Logic → Interactions → Testing.

  UNIQUE VALUE: Creates independent task files (story-{name}-{n}-{task}.md) for each task. Tasks are ordered by UI development layers.

  Use this skill when:
  - Running /frontend.tasks command
  - User asks to "break down story", "create frontend tasks", "split into tasks"
  - Have story at docs/reference/pm/stories/ and need organized task files
  - Need tasks ordered by UI development layers (not random order)
  - Starting frontend work and want organized task list

  Task order is CRITICAL: Setup → Static UI → Dynamic → Interactions → Tests
  Output: Create multiple files in docs/reference/frontend/tasks/ with story- prefix
---

# Task Breakdown

## ⚠️ CRITICAL RULES - READ FIRST

**BEFORE doing anything, you MUST:**

1. **CHECK EXISTING TASKS FIRST**:
   - ALWAYS check if task files with `story-{story-name}-*` already exist
   - If exists: READ them and continue from current progress
   - If not exists: Create new task breakdown
   - **NEVER re-break down existing tasks**

2. **FILE NAMING**:
   - Pattern: `story-{story-name}-{number}-{task-name}.md`
   - Example: `story-user-profile-1-setup-component.md`
   - `{number}`: Sequential number (1, 2, 3...)
   - `{task-name}`: Short kebab-case description

3. **ONE TASK PER FILE**:
   - Each file = one complete task
   - Each task = independently testable
   - Clear scope and acceptance criteria

4. **ALWAYS SAVE TO CORRECT PATH**:
   - Path: `docs/reference/frontend/tasks/story-{story-name}-{n}-{task}.md`
   - NO exceptions, NO other locations

5. **READ CONTEXT FIRST**:
   - Read story from `docs/reference/pm/stories/`
   - Read design from `docs/reference/frontend/designs/` if exists
   - Read design system from `docs/reference/frontend/design-system.md`
   - Read constraints from `docs/reference/frontend/constraints.md`

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Read story/PRD**: Load from `docs/reference/pm/stories/` or `docs/reference/pm/versions/`
2. **Read design** (if exists): Load from `docs/reference/frontend/designs/`
3. **Read constraints**: Load design system and technical constraints
4. **Identify components**: What UI elements are needed
5. **Identify interactions**: What logic and events are needed
6. **Break into tasks**: Independently testable, single responsibility
7. **Order by dependencies**: Setup → Static UI → Dynamic → Tests
8. **Generate files**: Create one file per task with story- prefix
9. **Update Story file**: Add "Related Tasks" section to story file with task list
10. **Summary**: Show created files and next steps

## Task File Format

```markdown
# Task: [Task Name]

> **File**: `story-{story-name}-{number}-{task-name}.md`
> **Type**: feature | improvement
> **Source**: story:{story-name}
> **Story**: docs/reference/pm/stories/{story-id}.md
> **Design**: docs/reference/frontend/designs/{design-name}.md
> **Created**: YYYY-MM-DD
> **Status**: pending

## Description

[Clear description of what this task achieves]

## Context

- Part of [Story Name] story
- Depends on: [Previous task if any]
- Design reference: [Link to design if applicable]
- Should follow design system tokens

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Scope

**Files to create/modify:**

- Create: `src/components/...`
- Modify: `src/pages/...`

**Key components:**

- Component A
- Component B

## Implementation Steps

> Note: Detailed steps can be added using `/frontend.plan` command

### Step 1: [Brief description]

**Files**: ...
**Action**: ...
**Verify**: ...

---

## Notes

[Any additional notes, considerations, or technical decisions]

## Related Tasks

- Depends on: story-{story-name}-{prev-number}-{prev-task}
- Blocks: story-{story-name}-{next-number}-{next-task}
```

## Task Types

| Type        | Examples                                |
| ----------- | --------------------------------------- |
| Setup       | Create component structure, setup state |
| UI          | Implement section/component layout      |
| Logic       | Add form validation, API integration    |
| Interaction | Implement hover, click, animations      |
| Testing     | Unit tests, integration tests           |

## Granularity Rules

- Each task = independently testable
- Each task = single responsibility
- Each task = clear scope (not too big, not too small)
- Each task = 1-4 hours of work

## Ordering Rules

1. **Setup tasks first** - Component structure, routing
2. **Static UI before dynamic** - Layout before logic
3. **Core functionality before edge cases** - Happy path first
4. **Tests after implementation** - Each feature gets tests

## Updating Story File

After generating task files, **ALWAYS** update the story file to add the "Related Tasks" section:

```markdown
## Related Tasks

### Frontend Tasks

- [ ] docs/reference/frontend/tasks/story-user-profile-1-setup-component.md
- [ ] docs/reference/frontend/tasks/story-user-profile-2-implement-header.md
- [ ] docs/reference/frontend/tasks/story-user-profile-3-implement-avatar.md
- [ ] docs/reference/frontend/tasks/story-user-profile-4-implement-bio.md
- [ ] docs/reference/frontend/tasks/story-user-profile-5-add-tests.md
```

**Key points:**

- Add this section at the end of the story file (before any existing notes)
- Use `- [ ]` checkboxes for all tasks (they will be checked when tasks complete)
- List tasks in execution order (Setup → UI → Logic → Tests)
- Keep the section organized by frontend/backend if both exist

## Output Example

After breaking down "user-profile" story:

```
Created 5 task files:

✓ docs/reference/frontend/tasks/story-user-profile-1-setup-component.md
✓ docs/reference/frontend/tasks/story-user-profile-2-implement-header.md
✓ docs/reference/frontend/tasks/story-user-profile-3-implement-avatar.md
✓ docs/reference/frontend/tasks/story-user-profile-4-implement-bio.md
✓ docs/reference/frontend/tasks/story-user-profile-5-add-tests.md

Next steps:
1. Review task files
2. Use /frontend.plan to add detailed steps to each task
3. Use aico-frontend-implement to execute tasks
```

## Key Rules

- ALWAYS create separate files for each task
- MUST use `story-{story-name}-{number}-{task-name}.md` naming
- ALWAYS include test tasks at the end
- MUST note dependencies between tasks
- Keep tasks focused - not too big, not too small
- Each task file is self-contained and complete

## Common Mistakes

- ❌ Tasks too large (full page) → ✅ Break into sections
- ❌ Tasks too small (add one button) → ✅ Group related work
- ❌ Skip dependencies → ✅ Note which tasks depend on others
- ❌ Forget testing → ✅ Always include test tasks
- ❌ Vague task names → ✅ Use descriptive names in filename
