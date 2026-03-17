---
name: aico-backend-task-breakdown
description: |
  Break down PM story into organized tasks in a single file following LAYERED ARCHITECTURE order: Types → Database → Repository → Service → API → Tests.

  UNIQUE VALUE: Creates single task file (story-{name}.md) containing all tasks for a story. Tasks are ordered by backend architecture layers.

  Use this skill when:
  - Running /backend.tasks command
  - User asks to "break down story", "create backend tasks", "split into tasks"
  - Have story at docs/reference/pm/stories/ and need organized task breakdown
  - Need tasks ordered by backend architecture layers (not random order)
  - Starting backend work and want organized task list

  Task order is CRITICAL: Setup → Static UI → Dynamic → Interactions → Tests
  Output: Create single file docs/reference/backend/tasks/story-{name}.md with all tasks
---

# Task Breakdown

## ⚠️ CRITICAL RULES - READ FIRST

**BEFORE doing anything, you MUST:**

1. **CHECK EXISTING TASK FILE FIRST**:
   - ALWAYS check if `story-{story-name}.md` already exists in `docs/reference/backend/tasks/`
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
   - Path: `docs/reference/backend/tasks/story-{story-name}.md`
   - NO exceptions, NO other locations

5. **READ CONTEXT FIRST**:
   - Read story from `docs/reference/pm/stories/`
   - Read design from `docs/reference/backend/designs/` if exists
   - Read design system from `docs/reference/backend/design-system.md`
   - Read constraints from `docs/reference/backend/constraints.md`

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Read story/PRD**: Load from `docs/reference/pm/stories/` or `docs/reference/pm/versions/`
2. **Read design** (if exists): Load from `docs/reference/backend/designs/`
3. **Read constraints**: Load design system and technical constraints
4. **Identify components**: What backend layers are needed
5. **Identify interactions**: What APIs and data flows are needed
6. **Break into tasks**: Independently testable, single responsibility, by architecture layer
7. **Order by dependencies**: Types → DB → Repository → Service → API → Tests
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
- Backend tasks ordered by architecture layers: Types → DB → Repository → Service → API → Tests

## Updating Story File

After generating the task file, **ALWAYS** update the story file to add the "Related Tasks" section:

```markdown
## Related Tasks

### Backend Tasks

Task breakdown: [docs/reference/backend/tasks/story-user-profile.md](../backend/tasks/story-user-profile.md)

**Progress**: 0/6 tasks completed

- [ ] Task 1: Define Types
- [ ] Task 2: Database Schema
- [ ] Task 3: Repository Layer
- [ ] Task 4: Service Layer
- [ ] Task 5: API Endpoints
- [ ] Task 6: Add Tests
```

**Key points:**

- Add this section at the end of the story file (before any existing notes)
- Include link to the task file
- Use `- [ ]` checkboxes for each task (will be checked when task completes)
- List tasks in execution order (Types → DB → Repository → Service → API → Tests)
- Keep the section organized by frontend/backend if both exist
- Include progress counter (X/Y tasks completed)

## Output Example

After breaking down "user-profile" story:

```
Created task file for story 'user-profile':

✓ docs/reference/backend/tasks/story-user-profile.md

Task breakdown includes:
- Task 1: Define Types (setup)
- Task 2: Database Schema (feature)
- Task 3: Repository Layer (feature)
- Task 4: Service Layer (feature)
- Task 5: API Endpoints (feature)
- Task 6: Add Tests (testing)

Total: 6 tasks

Next steps:
1. Review task breakdown in story-user-profile.md
2. Use /backend.plan to add detailed steps to specific tasks
3. Use /backend.implement to start executing tasks
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

- ❌ Tasks too large (full feature) → ✅ Break into layers
- ❌ Tasks too small (add one field) → ✅ Group related work
- ❌ Skip dependencies → ✅ Note which tasks depend on others
- ❌ Forget testing → ✅ Always include test tasks
- ❌ Create multiple files → ✅ Use single file with multiple task sections
