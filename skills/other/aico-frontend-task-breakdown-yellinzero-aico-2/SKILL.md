---
name: aico-frontend-task-breakdown
description: |
  Break down PM story into organized tasks in a single file following UI DEVELOPMENT order: Setup → Static UI → Dynamic Logic → Interactions → Testing.

  UNIQUE VALUE: Creates single task file (story-{name}.md) containing all tasks for a story. Tasks are ordered by UI development layers.

  Use this skill when:
  - Running /frontend.tasks command
  - User asks to "break down story", "create frontend tasks", "split into tasks"
  - Have story at docs/reference/pm/stories/ and need organized task breakdown
  - Need tasks ordered by UI development layers (not random order)
  - Starting frontend work and want organized task list

  Task order is CRITICAL: Setup → Static UI → Dynamic → Interactions → Tests
  Output: Create single file docs/reference/frontend/tasks/story-{name}.md with all tasks
---

# Task Breakdown

## ⚠️ CRITICAL RULES - READ FIRST

**BEFORE doing anything, you MUST:**

1. **CHECK EXISTING TASK FILE FIRST**:
   - ALWAYS check if `story-{story-name}.md` already exists in `docs/reference/frontend/tasks/`
   - If exists: READ it and continue from current progress (add new tasks or update existing ones)
   - If not exists: Create new task breakdown file
   - **NEVER re-break down existing tasks**

2. **FILE NAMING**:
   - Pattern: `story-{story-name}.md` (single file per story)
   - Example: `story-user-profile.md`
   - All tasks for this story go into this ONE file
   - Tasks are separated by `---` dividers

3. **MULTIPLE TASKS IN ONE FILE**:
   - One file contains ALL tasks for the story
   - Each task = independently testable section
   - Clear scope and acceptance criteria per task
   - Tasks numbered sequentially (Task 1, Task 2, etc.)

4. **ALWAYS SAVE TO CORRECT PATH**:
   - Path: `docs/reference/frontend/tasks/story-{story-name}.md`
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
8. **Generate single file**: Create `story-{story-name}.md` with all tasks in sections
9. **Update Story file**: Add "Related Tasks" section to story file with link to task file
10. **Summary**: Show created file and next steps

## Task File Format

See [Task File Template](references/task-file-template.md) for complete structure.

**Key points:**

- Single file contains all tasks for the story
- Tasks numbered sequentially (Task 1, Task 2, etc.)
- Each task has: Description, Context, Acceptance Criteria, Scope, Implementation Steps
- Progress section at the end tracks completion
- Both story-based and standalone use the same format (only filename differs)

## Updating Story File

After generating the task file, **ALWAYS** update the story file to add the "Related Tasks" section:

```markdown
## Related Tasks

### Frontend Tasks

Task breakdown: [docs/reference/frontend/tasks/story-user-profile.md](../frontend/tasks/story-user-profile.md)

**Progress**: 0/5 tasks completed

- [ ] Task 1: Setup Component
- [ ] Task 2: Implement Header
- [ ] Task 3: Implement Avatar
- [ ] Task 4: Implement Bio
- [ ] Task 5: Add Tests
```

**Key points:**

- Add this section at the end of the story file (before any existing notes)
- Include link to the task file
- Use `- [ ]` checkboxes for each task (will be checked when task completes)
- List tasks in execution order (Setup → UI → Logic → Tests)
- Keep the section organized by frontend/backend if both exist
- Include progress counter (X/Y tasks completed)

## Output Example

After breaking down "user-profile" story:

```
Created task file for story 'user-profile':

✓ docs/reference/frontend/tasks/story-user-profile.md

Task breakdown includes:
- Task 1: Setup Component Structure (setup)
- Task 2: Implement Header Section (feature)
- Task 3: Implement Avatar Component (feature)
- Task 4: Implement Bio Section (feature)
- Task 5: Add Comprehensive Tests (testing)

Total: 5 tasks

Next steps:
1. Review task breakdown in story-user-profile.md
2. Use /frontend.plan to add detailed steps to specific tasks
3. Use /frontend.implement to start executing tasks
```

## Key Rules

- ALWAYS create a single file containing all tasks for the story
- MUST use `story-{story-name}.md` naming (NOT multiple files)
- ALWAYS include test tasks at the end
- MUST note dependencies between tasks (in each task's metadata)
- Keep tasks focused - not too big, not too small
- Each task section is self-contained with clear acceptance criteria
- Separate tasks with `---` dividers
- Include Story Progress section at the end of file

## Common Mistakes

- ❌ Tasks too large (full page) → ✅ Break into sections
- ❌ Tasks too small (add one button) → ✅ Group related work
- ❌ Skip dependencies → ✅ Note which tasks depend on others
- ❌ Forget testing → ✅ Always include test tasks
- ❌ Create multiple files → ✅ Use single file with multiple task sections
