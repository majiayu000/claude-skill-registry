---
name: aico-backend-plan
description: |
  Create or enhance backend tasks with detailed implementation steps. Supports TWO modes:

  MODE A: Enhance existing task (add detailed steps to task in file)
  MODE B: Create new standalone task file (can contain single or multiple tasks)

  IMPORTANT: This skill creates MICRO-LEVEL atomic steps, NOT macro architecture plans.
  For architecture planning or feature scoping, use EnterPlanMode instead.

  Use this skill when:
  - Running /backend.plan command
  - User asks for "atomic steps", "step-by-step plan with verification"
  - Have a specific task and need implementation steps
  - User wants to create a standalone task file (not from story)
  - Need granular steps: Types → DB → Repository → Service → API → Tests

  DO NOT use for:
  - Architecture planning (use EnterPlanMode)
  - General development planning
  - Feature scoping or estimation

  Output:
  - MODE A: Update specific task section in file with Implementation Steps
  - MODE B: Create new standalone-{name}.md file with one or multiple tasks
---

# Plan

## ⚠️ CRITICAL RULES - READ FIRST

1. **DETECT MODE**: Determine if input is an existing task reference or a new requirement description
   - If input looks like `story-user-api Task 1` or `standalone-fix-auth Task 2`: **MODE A**
   - If input is a new requirement (e.g., "Add user authentication"): **MODE B**

2. **MODE A - Enhance Existing Task**:
   - Read the task file from `docs/reference/backend/tasks/`
   - User must specify task number (e.g., "Task 1", "Task 2")
   - Add or update the "Implementation Steps" section for that specific task
   - Keep all other sections intact
   - Save back to the same file

3. **MODE B - Create Standalone Task File**:
   - Analyze the requirement - is it simple (1 task) or complex (multiple tasks)?
   - If complex, break into multiple tasks (like task-breakdown does)
   - Use filename: `standalone-{requirement-name}.md` (kebab-case)
   - Save to `docs/reference/backend/tasks/`
   - File format: same as story-based (multiple task sections)

4. **READ CONSTRAINTS FIRST**:
   - Must read `docs/reference/backend/design-system.md` for design tokens
   - Must read `docs/reference/backend/constraints.md` for tech stack
   - If task references a design, read from `docs/reference/backend/designs/`

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## MODE A: Enhance Existing Task

### Process

1. **Read task file**: Get task details from `docs/reference/backend/tasks/{task-file}.md`
2. **Read design** (if referenced): Load related design from `docs/reference/backend/designs/`
3. **Read design system**: Load `docs/reference/backend/design-system.md` for design tokens
4. **Read constraints**: Load `docs/reference/backend/constraints.md`
5. **Break into atomic steps**:
   - Start with file creation/setup
   - One section/feature per step
   - Include verification for each step
   - Do NOT include commit step (that happens during execution)
6. **Keep steps atomic**: One action per step
7. **Update task file**: Add/replace "Implementation Steps" section
8. **Present summary**: Show file location and what was added

### Example

```bash
# Input: User runs /backend.plan story-user-profile-2-header

# Output:
✓ Read task: docs/reference/backend/tasks/story-user-profile-2-header.md
✓ Added 4 implementation steps to task file

Steps added:
1. Create component file
2. Implement header layout
3. Add responsive styles
4. Add unit tests

Task ready for implementation. Use aico-backend-implement to execute.
```

## MODE B: Create Standalone Task

### Process

1. **Ask user for details**:
   - Task type: feature | bugfix | improvement
   - Confirm task name (auto-generate from description)

2. **Read constraints**:
   - Read design system and technical constraints
   - If user mentions a component, check existing code

3. **Generate complete task file**:
   - All metadata (type, source, created, status)
   - Description
   - Context
   - Acceptance Criteria
   - Scope
   - Implementation Steps (detailed, atomic)
   - Notes

4. **Save task file**: Write to `docs/reference/backend/tasks/standalone-{task-name}.md`

5. **Present summary**: Show created file and next steps

### Example

```bash
# Input: User runs /backend.plan "Fix login button hover state"

# Interactive:
# Type: [feature | bugfix | improvement] → bugfix
# Task name: fix-login-button-hover (auto-generated, confirm?)

# Output:
✓ Created standalone task: standalone-fix-login-button-hover.md

Task includes:
- Description and context
- 2 acceptance criteria
- 3 implementation steps
- Test verification

Next: Use aico-backend-implement to execute this task
```

## Implementation Steps Format

Both modes use the same step format:

````markdown
## Implementation Steps

### Step 1: [Action]

**Files**:

- Create: `src/components/[Name].tsx`
- Modify: `src/pages/[Page].tsx:L10-L20`

**Action**:
[Exact code or action to take]

**Verify**:

```bash
[verification command]
```
````

Expected: [expected output]

---

### Step 2: [Next Action]

...

````

## Step Granularity

Each step = ONE atomic action:

| Good Steps | Bad Steps |
|------------|-----------|
| Create component file with imports | Create component with all logic |
| Add component skeleton (empty return) | Implement entire component |
| Implement single section | Implement all sections |
| Write one test case | Write all tests |

## Step Types

### Setup Step
```markdown
**Files**: Create: `src/components/ProfileCard.tsx`
**Action**: Create file with basic structure
**Verify**: `npx tsc --noEmit` → No errors
````

### Implementation Step

```markdown
**Files**: Modify: `src/components/ProfileCard.tsx:L8-L10`
**Action**: Implement header section with Avatar and name
**Verify**: `npm run dev` → Component renders correctly
```

### Test Step

```markdown
**Files**: Create: `src/components/__tests__/ProfileCard.test.tsx`
**Action**: Write unit test for profile name rendering
**Verify**: `npm test ProfileCard` → 1 test passed
```

## Standalone Task File Template

For MODE B, see [Task File Template](../task-breakdown/references/task-file-template.md) for complete structure.

Use the same format as story-based tasks, just with:

- Filename: `standalone-{requirement-name}.md`
- Header: `# Standalone Tasks: [Requirement Name]`
- No `> **Story**: ...` line

**Note**: For simple requirements, file may contain only 1 task. For complex requirements, break into multiple tasks.

## Key Rules

- ALWAYS include verification command for each step
- MUST keep steps to 2-5 minutes of work
- MUST save to docs/reference/backend/tasks/ directory
- NEVER combine multiple actions into one step
- Do NOT include commit step in plan (commits happen during execution)
- MODE A: Preserve all existing content, only add/update steps
- MODE B: Generate complete, self-contained task file

## Common Mistakes

- ❌ Steps too large → ✅ One action per step
- ❌ Skip verification → ✅ Every step has verify command
- ❌ Vague actions → ✅ Include exact code
- ❌ Not saving to file → ✅ Always save task file
- ❌ Including commit in steps → ✅ Commits happen during execution, not planning
- ❌ MODE A: Overwriting existing content → ✅ Only update Implementation Steps section
- ❌ MODE B: Missing metadata → ✅ Include all template sections
