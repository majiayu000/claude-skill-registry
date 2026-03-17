---
name: aico-frontend-plan
description: |
  Create or enhance frontend tasks with detailed implementation steps. Supports TWO modes:

  MODE A: Enhance existing task (add detailed steps to task in file)
  MODE B: Create new standalone task file (can contain single or multiple tasks)

  IMPORTANT: This skill creates MICRO-LEVEL atomic steps, NOT macro architecture plans.
  For architecture planning or feature scoping, use EnterPlanMode instead.

  Use this skill when:
  - Running /frontend.plan command
  - User asks for "atomic steps", "step-by-step plan with verification"
  - Have a specific task and need implementation steps
  - User wants to create a standalone task file (not from story)
  - Need granular steps: Setup (create files) → Implementation (write code) → Test (verify)

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
   - If input looks like `story-user-profile Task 1` or `standalone-fix-login Task 2`: **MODE A**
   - If input is a new requirement (e.g., "Fix login button hover"): **MODE B**

2. **MODE A - Enhance Existing Task**:
   - Read the task file from `docs/reference/frontend/tasks/`
   - User must specify task number (e.g., "Task 1", "Task 2")
   - Add or update the "Implementation Steps" section for that specific task
   - Keep all other sections intact
   - Save back to the same file

3. **MODE B - Create Standalone Task File**:
   - Analyze the requirement - is it simple (1 task) or complex (multiple tasks)?
   - If complex, break into multiple tasks (like task-breakdown does)
   - Use filename: `standalone-{requirement-name}.md` (kebab-case)
   - Save to `docs/reference/frontend/tasks/`
   - File format: same as story-based (multiple task sections)

4. **READ CONSTRAINTS FIRST**:
   - Must read `docs/reference/frontend/design-system.md` for design tokens
   - Must read `docs/reference/frontend/constraints.md` for tech stack
   - If task references a design, read from `docs/reference/frontend/designs/`

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## MODE A: Enhance Existing Task

### Process

1. **Read task file**: Get file from `docs/reference/frontend/tasks/{filename}.md` (story-_ or standalone-_)
2. **Extract specific task**: Find the task section by number (e.g., "Task 1", "Task 2")
3. **Read related files** (if referenced): Load design from `docs/reference/frontend/designs/`
4. **Read design system**: Load `docs/reference/frontend/design-system.md` for design tokens
5. **Read constraints**: Load `docs/reference/frontend/constraints.md`
6. **Break into atomic steps**:
   - Start with file creation/setup
   - One section/feature per step
   - Include verification for each step
   - Do NOT include commit step (that happens during execution)
7. **Keep steps atomic**: One action per step
8. **Update task section**: Add/replace "Implementation Steps" in the specific task
9. **Present summary**: Show what was added

### Example

```bash
# Input: User runs /frontend.plan story-user-profile Task 2

# Output:
✓ Read file: docs/reference/frontend/tasks/story-user-profile.md
✓ Found Task 2: Implement Header Section
✓ Added 4 implementation steps

Steps added:
1. Create header component file
2. Implement header layout
3. Add responsive styles
4. Add unit tests

Task ready for implementation. Use /frontend.implement to execute.
```

## MODE B: Create Standalone Task File

### Process

1. **Analyze requirement**:
   - Is this a simple task (single responsibility) or complex (multiple steps)?
   - If complex, break down into multiple independent tasks

2. **Ask user for details** (optional):
   - Auto-generate task name from description
   - Ask for confirmation

3. **Read constraints**:
   - Read design system and technical constraints
   - If user mentions a component, check existing code

4. **Generate task file** (unified format):
   - File header with metadata
   - If simple: 1 task section with detailed steps
   - If complex: Multiple task sections (Task 1, Task 2, etc.)
   - Each task has: Description, Context, AC, Scope, Implementation Steps
   - Progress section at end

5. **Save task file**: Write to `docs/reference/frontend/tasks/standalone-{name}.md`

6. **Present summary**: Show created file and next steps

### Example - Simple Requirement

```bash
# Input: User runs /frontend.plan "Fix login button hover state"

# Output:
✓ Created standalone task: standalone-fix-login-button-hover.md

File contains:
- 1 task: Fix Button Hover
- 3 implementation steps
- Test verification included

Next: Use /frontend.implement standalone-fix-login-button-hover Task 1
```

### Example - Complex Requirement

```bash
# Input: User runs /frontend.plan "Add user profile page with avatar, bio, and settings"

# Output:
✓ Created standalone task: standalone-user-profile-page.md

File contains:
- Task 1: Setup Profile Page Component
- Task 2: Implement Avatar Section
- Task 3: Implement Bio Section
- Task 4: Implement Settings Section
- Task 5: Add Tests

Total: 5 tasks

Next: Use /frontend.implement standalone-user-profile-page Task 1
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
- MUST save to docs/reference/frontend/tasks/ directory
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
