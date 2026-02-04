---
name: writing-plans
description: Use when design is complete and you need detailed implementation tasks for engineers with zero codebase context - creates comprehensive implementation plans with exact file paths, complete code examples, and verification steps assuming engineer has minimal domain knowledge
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

---

## Google-Engineer Production Standards (MANDATORY)

**Every plan MUST address these concerns before writing code:**

### 1. Research Phase (Before Planning)
- **Search for best practices** using WebSearch for the specific tech stack
- **Find authoritative sources** (official docs, respected blogs, GitHub discussions)
- **Document research sources** in the plan header with links

### 2. Code Quality Checklist
Every plan must include solutions for:

| Concern | Required Solution |
|---------|-------------------|
| **DRY Violations** | Centralized config modules for any value used in 2+ places |
| **Error Handling** | Error boundaries (React), try-catch with proper logging, graceful degradation |
| **Loading States** | Skeleton loaders that match content structure (not spinners) |
| **User Feedback** | Toast/notification for all mutations (success AND failure) |
| **Optimistic Updates** | TanStack Query pattern with snapshot/rollback for instant UX |
| **Mobile UX** | Min 44px touch targets, responsive grids, thumb-zone placement |
| **Type Safety** | Strict TypeScript, Zod validation at boundaries, no `any` |
| **Testing** | E2E tests for critical paths, unit tests for business logic |
| **Accessibility** | ARIA labels, keyboard navigation, color contrast |
| **Performance** | Lazy loading, code splitting, memoization where needed |

### 3. Defensive Programming Patterns
```
- Validate inputs at system boundaries (API routes, form submissions)
- Never trust client data on the server
- Use TypeScript strict mode
- Prefer immutable updates
- Handle null/undefined explicitly
- Log errors with context (not just the error message)
```

### 4. Self-Roast Before Shipping
After drafting the plan, review each component and ask:
- "What happens if this crashes?"
- "What happens on slow network?"
- "What happens on mobile?"
- "Is this hardcoded anywhere else?"
- "Where are the tests?"
- "Would a user know if this succeeded or failed?"

Fix any issues found before presenting the plan.

---

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Research Sources:**
- [Link 1](url) - What was learned
- [Link 2](url) - What was learned

**Production Checklist:**
- [ ] Centralized config (no magic strings/numbers in 2+ places)
- [ ] Error boundaries around risky components
- [ ] Skeleton loading states
- [ ] Toast notifications for mutations
- [ ] Optimistic updates where applicable
- [ ] Mobile-friendly touch targets (44px+)
- [ ] E2E tests for critical paths
- [ ] Accessibility basics (ARIA, keyboard nav)

---
```

## Task Structure

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## Advanced Patterns Reference

### Error Boundaries (React)
```typescript
import { ErrorBoundary } from 'react-error-boundary';

<ErrorBoundary
  FallbackComponent={ErrorFallback}
  onReset={() => queryClient.invalidateQueries()}
  onError={(error, info) => logToService(error, info)}
>
  <RiskyComponent />
</ErrorBoundary>
```

### Optimistic Updates (TanStack Query v5)
```typescript
useMutation({
  mutationFn: updateTodo,
  onMutate: async (newTodo) => {
    await queryClient.cancelQueries({ queryKey: ['todos'] });
    const previous = queryClient.getQueryData(['todos']);
    queryClient.setQueryData(['todos'], (old) => [...old, newTodo]);
    return { previous };
  },
  onError: (err, newTodo, context) => {
    queryClient.setQueryData(['todos'], context.previous);
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});
```

### Skeleton That Matches Content
```typescript
// BAD: Generic spinner
if (isLoading) return <Spinner />;

// GOOD: Skeleton matching actual content structure
if (isLoading) return (
  <Card>
    <CardHeader>
      <Skeleton className="h-6 w-32" />
    </CardHeader>
    <CardContent>
      <Skeleton className="h-10 w-20 mb-2" />
      <Skeleton className="h-2 w-full" />
    </CardContent>
  </Card>
);
```

### Mobile Touch Targets
```typescript
// BAD: Tiny buttons
<Button size="sm" className="p-1">+</Button>

// GOOD: Thumb-friendly
<Button size="lg" className="h-12 w-12 min-h-[44px] min-w-[44px]">+</Button>
```

## Remember
- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, TDD, frequent commits
- **Research before planning**
- **Self-roast before shipping**
- **Every mutation needs feedback**
- **Every async operation needs loading + error states**

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:subagent-driven-development
- Stay in this session
- Fresh subagent per task + code review

**If Parallel Session chosen:**
- Guide them to open new session in worktree
- **REQUIRED SUB-SKILL:** New session uses superpowers:executing-plans
