---
name: aico-backend-implement
description: |
  Execute backend task implementation with TDD. Read task file, execute steps, verify each, update status.

  Use this skill when:
  - User asks to "implement task/plan", "start implementation", "execute plan", or "start coding"
  - Have task file (story-* or standalone-*) ready to execute
  - User asks to "use TDD", "write test first", or "test-driven"
  - User asks to "write tests", "add tests", "create tests"
  - Fixing bugs (write failing test first)

  TDD Iron Law: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
  TDD Cycle: RED (failing test) → Verify fails → GREEN (minimal code) → Verify passes → REFACTOR

  Prerequisites:
  - Task file in docs/reference/backend/tasks/ (story-* or standalone-*)
  - Read constraints.md and design spec before coding

  Flow: Read Task → Read Constraints → Execute Steps → Verify → Test → Update Status
---

# Implement

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

0. **Read task file** (MANDATORY):
   - Look for task file in `docs/reference/backend/tasks/`
   - Accept either:
     - **Story-based**: `story-{story-name}.md` with task number
     - **Standalone**: `standalone-{task-name}.md` with task number
   - User must specify task number (e.g., "implement story-user-api Task 1" or "implement standalone-fix-auth Task 1")
   - Both formats contain multiple tasks, just different naming
   - If NOT exists or task number not specified → STOP and ask user which task to implement

1. **Read constraints FIRST** (before any code):
   - `docs/reference/backend/design-system.md` - Colors, typography, spacing
   - `docs/reference/backend/constraints.md` - Tech stack, patterns
   - If task references design: `docs/reference/backend/designs/{name}.md`

2. **Execute implementation steps**:
   - Read "Implementation Steps" section from task
   - Execute each step in order
   - Run verification command after each step
   - If fail → fix before proceeding
   - If pass → continue to next step

3. **After all steps**:
   - Run unit tests
   - Run build check

4. **Update task status**:
   - Update the specific task section in the file
   - Mark acceptance criteria checkboxes: `- [ ]` → `- [x]`
   - Change Status from `pending` to `completed`
   - Update "Progress" section at bottom of file
   - Both story-based and standalone files use the same format

5. **Notify completion**:
   - Show task file path and task number
   - Show completion status
   - **Check related Story** (story-based only):
     - Read `> **Story**:` field from file header
     - If Story exists, check story file at `docs/reference/pm/stories/`
     - Update Story's Related Tasks section: mark this task as `- [x]`
     - Count total vs completed tasks
     - If all tasks completed, show: "✅ All tasks completed! Story {story-name} is ready for acceptance."
     - If partial completion, show: "⏳ Progress: X/Y tasks completed"

## Task File Format

See [Task File Template](../task-breakdown/references/task-file-template.md) for complete structure.

Both story-based and standalone tasks use the same file structure - the only difference is the filename:

- **Story-based**: `story-{story-name}.md` (from PM story breakdown)
- **Standalone**: `standalone-{task-name}.md` (from plan/ad-hoc requirements)

**Usage Examples:**

- `implement story-user-api Task 1`
- `implement standalone-fix-auth Task 1`

## Execution Flow

```
Read Task File
     ↓
Read Constraints (design-system.md, constraints.md, designs/)
     ↓
Execute Step 1 → Verify → Pass? → Continue
                      ↓
                     Fail → Fix → Retry
     ↓
Execute Step 2 → Verify → Pass? → Continue
     ↓
     ...
     ↓
Run Unit Tests
     ↓
Run Build Check
     ↓
Update Task File (mark AC completed, update status)
     ↓
Show Completion Summary
```

## Step Execution Rules

### Rule 1: Follow Constraints Exactly

```tsx
// ❌ Wrong: Ignore design system
<button className="bg-blue-500 text-white">

// ✅ Right: Use design tokens
<button className="bg-primary text-primary-foreground">
```

### Rule 2: Verify Before Proceeding

Each step has a Verify section - MUST run it and confirm expected output before moving on.

### Rule 3: No Skipping

- Execute ALL steps in order
- Do NOT combine steps
- Do NOT skip verification

## Post-Implementation Checklist

1. **Run tests**: `npm test [component]`
2. **Run build**: `npm run build`
3. **Update task file**:
   - Mark AC checkboxes: `- [x]`
   - Update Status: `completed`
4. **Show completion summary** to user

## Error Handling

| Error Type           | Action                                 |
| -------------------- | -------------------------------------- |
| TypeScript error     | Fix type issues, re-verify             |
| Test failure         | Debug test, fix implementation or test |
| Build failure        | Check imports, fix errors              |
| Constraint violation | Re-read constraints, align code        |

## Updating Task File

After successful implementation, update the task file. Both story-based and standalone files use the same format, so the update process is identical:

**1. Mark Task's Acceptance Criteria as Completed**

```markdown
## Task 1: Define Types

> **Status**: completed ← Changed from pending

### Acceptance Criteria

- [x] Types defined correctly ← Changed from [ ]
- [x] Exported from index ← Changed from [ ]
- [x] No type errors ← Changed from [ ]
```

**2. Update Progress Section**

```markdown
## Progress

- Total tasks: 6
- Completed: 1 ← Changed from 0
- In progress: 0
- Pending: 5 ← Changed from 6

**Next task**: Task 2: Database Schema ← Update this
```

**3. Update Story File Checkboxes (story-based only)**

If this is a story-based task, update the PM story file at `docs/reference/pm/stories/`:

```markdown
### Backend Tasks

- [x] Task 1: Define Types ← Changed from [ ]
- [ ] Task 2: Database Schema
- [ ] Task 3: Repository Layer
```

## Key Rules

- ALWAYS read task file first
- ALWAYS read all constraint files before writing any code
- MUST run verification command for each step
- ALWAYS run tests before marking task complete
- MUST update task file (mark AC, update status)

## Common Mistakes

- ❌ Start without reading task file → ✅ ALWAYS read task file first
- ❌ Skip reading constraints → ✅ ALWAYS read before coding
- ❌ Skip verification → ✅ Run verify command for each step
- ❌ Skip tests → ✅ Run tests before marking complete
- ❌ Forget to update task file → ✅ Update AC and status

---

## TDD Deep Dive

### The TDD Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? **Delete it. Start over.**

### Red-Green-Refactor Cycle

```
RED → Verify Fails → GREEN → Verify Passes → REFACTOR → Repeat
```

#### 1. RED - Write Failing Test

```typescript
test('Button shows loading state when clicked', async () => {
  render(<SubmitButton onClick={mockSubmit} />)
  await userEvent.click(screen.getByRole('button'))
  expect(screen.getByRole('button')).toBeDisabled()
  expect(screen.getByTestId('spinner')).toBeInTheDocument()
})
```

#### 2. Verify RED - Watch It Fail

```bash
npm test -- --watch ComponentName
```

#### 3. GREEN - Write Minimal Code

Write simplest code to pass the test. Don't add features not in test.

#### 4. Verify GREEN - Watch It Pass

#### 5. REFACTOR - Clean Up

Only after green. Keep tests passing.

### Testing Library Query Priority

1. `getByRole` - accessible by everyone
2. `getByLabelText` - form fields
3. `getByText` - non-interactive elements
4. `getByTestId` - last resort

### Test Coverage Requirements

| Component Type | Required Tests                   |
| -------------- | -------------------------------- |
| UI Component   | Render, props, variants          |
| Form           | Validation, submit, error states |
| Interactive    | User events, callbacks           |
| Data Display   | Loading, error, empty states     |

### TDD Red Flags - STOP and Start Over

- Code before test
- Test passes immediately
- Testing implementation details
- `querySelector` everywhere

---

## Example Workflow

```bash
# User: "Implement story-user-profile-2-header"

1. ✓ Read task: docs/reference/backend/tasks/story-user-profile-2-header.md
2. ✓ Read constraints:
   - design-system.md
   - constraints.md
   - designs/user-profile.md

3. ✓ Execute Step 1: Create component file
   → Run: npm run typecheck
   → ✓ Pass

4. ✓ Execute Step 2: Implement header layout
   → Run: npm run dev
   → ✓ Pass

5. ✓ Execute Step 3: Add responsive styles
   → Run: npm run dev (test at different breakpoints)
   → ✓ Pass

6. ✓ Execute Step 4: Add unit tests
   → Run: npm test LoginHeader
   → ✓ 3 tests passed

7. ✓ Run full test suite
   → Run: npm test
   → ✓ All tests passed

8. ✓ Run build
   → Run: npm run build
   → ✓ Build successful

9. ✓ Update task file:
   - Marked all AC as completed
   - Status: completed

10. ✓ Task completed!
```

## Iron Law

**NO CODE WITHOUT TASK FILE**

This rule is non-negotiable. Before writing code:

1. Task file must exist
2. Acceptance criteria must be defined
3. Implementation steps must be clear

### Rationalization Defense

| Excuse                         | Reality                                     |
| ------------------------------ | ------------------------------------------- |
| "It's a simple change"         | Simple changes often have hidden complexity |
| "I'll document after coding"   | Post-hoc documentation is always incomplete |
| "Tests can wait until later"   | Untested code is broken code                |
| "I know what needs to be done" | Assumptions without validation cause bugs   |
