---
name: aico-backend-implement
description: |
  Execute backend task implementation with TDD. Read task file, execute implementation steps, verify each step, update status.

  Use this skill when:
  - User asks to "implement this task", "implement the plan", "start implementation", "execute plan"
  - Have a task file (story- or standalone- prefix) ready to execute
  - User says "start coding", "write the code", "begin implementation"
  - User asks to "use TDD", "write test first", "test-driven" for backend code
  - User asks to "write tests", "add tests", "create tests"
  - Fixing UI bugs (write failing test that reproduces bug first)

  TDD Iron Law: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
  TDD Cycle: RED (write failing test) → Verify fails → GREEN (minimal code) → Verify passes → REFACTOR

  Prerequisites:
  - MUST have task file in docs/reference/backend/tasks/ (story- or standalone- prefix)
  - MUST read design-system.md, constraints.md, and design spec before writing any code

  Flow: Read Task File → Read Constraints → Execute Steps → Verify Each → Test → Update Task Status
---

# Implement

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

0. **Read task file** (MANDATORY):
   - Look for task file in `docs/reference/backend/tasks/`
   - Accept either:
     - `story-{story-name}-{number}-{task-name}.md`
     - `standalone-{task-name}.md`
   - If NOT exists → STOP and ask user which task to implement

1. **Read constraints FIRST** (before any code):
   - `docs/reference/backend/design-system.md` - Colors, typography, spacing
   - `docs/reference/backend/constraints.md` - Tech stack, patterns
   - If task references design: `docs/reference/backend/designs/{name}.md`

2. **Execute implementation steps**:
   - Read "Implementation Steps" section from task file
   - Execute each step in order
   - Run verification command after each step
   - If fail → fix before proceeding
   - If pass → continue to next step

3. **After all steps**:
   - Run unit tests
   - Run build check

4. **Update task status**:
   - Mark acceptance criteria checkboxes: `- [ ]` → `- [x]`
   - Change Status from `pending` to `completed`

5. **Notify completion**:
   - Show task file path
   - Show completion status
   - **Check related Story** (if task is from story breakdown):
     - Read `> **Story**:` field from task file
     - If Story exists, check story file at `docs/reference/pm/stories/`
     - Update Story's Related Tasks section: mark this task as `- [x]`
     - Count total vs completed tasks for this story
     - If all story tasks completed, show: "✅ All tasks completed! Story {story-name} is ready for acceptance. Please notify PM to verify."
     - If partial completion, show: "⏳ Story {story-name} progress: X/Y tasks completed"

## Task File Format

The implement skill reads task files in this format:

```markdown
# Task: [Task Name]

> **File**: `story-{name}-{n}-{task}.md` or `standalone-{task}.md`
> **Status**: pending | in_progress | completed

## Description

...

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Implementation Steps

### Step 1: [Action]

**Files**: ...
**Action**: ...
**Verify**: ...

### Step 2: [Action]

...
```

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

After successful implementation, update the task file:

### 1. Mark Acceptance Criteria as Completed

```markdown
## Acceptance Criteria

- [x] Logo displays correctly ← Changed from [ ]
- [x] Title uses correct typography ← Changed from [ ]
- [x] Header is responsive ← Changed from [ ]
- [x] Tests pass ← Changed from [ ]
```

### 2. Update Status

```markdown
> **Status**: completed ← Changed from pending
```

### 3. Add Completion Notes (optional)

```markdown
## Notes

- Implemented on YYYY-MM-DD
- All tests passing
- Used design tokens from design-system.md
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
