---
name: tdd-assessor
description: Evaluate if TDD is beneficial for current task and set up test-first approach. Use after plan and split strategy are decided.
---

# TDD Assessor

Evaluates Test-Driven Development fit for an implementation plan and sets up the TDD approach if appropriate.

## Prerequisites

- `plan.md` exists in `runs/{ticket-id}/`
- Plan approved and PR strategy decided

## Workflow

### 1. Load Context

Read `plan.md` from the current ticket's run directory and identify:

- What's being built
- Complexity level
- Type of change (feature, bug fix, refactor, config)

### 2. Evaluate TDD Fit

Score these factors:

| Factor                             | Score |
| ---------------------------------- | ----- |
| Clear specifications?              | +1    |
| New feature or bug fix?            | +1    |
| Complex logic?                     | +1    |
| Has acceptance criteria?           | +1    |
| Pure functions involved?           | +1    |
| Exploratory/uncertain scope?       | -1    |
| Heavy UI without clear assertions? | -1    |
| Simple config/typo fix?            | -2    |

**TDD Score interpretation:**

- 3-5: Strongly recommend TDD
- 1-2: TDD optional, suggest hybrid
- 0 or below: Skip TDD, write tests after

### 3. Research Testing Patterns

If TDD recommended, research the codebase:

```bash
# Find similar tests
find src -name "*.test.ts" | xargs grep -l "{relevant-keyword}" | head -5

# Read testing docs (if available)
cat docs/testing/README.md 2>/dev/null || echo "No testing README found"
cat docs/testing/unit-testing.md 2>/dev/null || echo "No unit testing docs found"
```

Identify:

- Test file location patterns (colocated: `*.test.ts` next to source)
- Mocking approaches used
- Setup helpers and fixtures

### 4. Generate TDD Plan

If TDD recommended, produce this structure:

```markdown
# TDD Approach for {Ticket}

## Assessment

- TDD Score: {X}/5
- Recommendation: TDD / Hybrid / Write tests after

## Testing Strategy

### Unit Tests

- **Location:** `src/{path}/*.test.ts` (colocated)
- **Framework:** Vitest
- **Pattern:** {based on research}

### Test Cases to Write First

1. **Test: {description}**
   - File: `src/{path}/{feature}.test.ts`
   - Verifies: {what behavior}
   - Setup: {any mocking needed}

2. **Test: {description}**
   - File: `src/{path}/{feature}.test.ts`
   - Verifies: {what behavior}

### Mocking Strategy

- {What to mock and how}
- Reference: {path to similar test file}

### E2E Tests (if applicable)

- **Location:** `browser_tests/{feature}.spec.ts`
- **Scenarios:** {list}

## TDD Workflow

For each feature:

1. Write test in `{file}.test.ts`
2. Run: `pnpm test:unit -- {file}.test.ts`
3. Verify test fails (RED)
4. Implement minimum code
5. Verify test passes (GREEN)
6. Refactor if needed
7. Commit: tests + implementation together
```

### 5. Present Decision

```
TDD Assessment Score: {X}/5

Recommendation: {TDD / Hybrid / Write tests after}

Rationale: {why}

Options:
A) Accept - Use TDD approach
B) Skip TDD - Write tests after implementation
C) Hybrid - TDD for core logic, tests after for UI

Your choice:
```

### 6. Update Plan

After user decision:

- Append TDD section to `plan.md`
- Update `status.json` with `tdd_approach` field

### 7. Output

- Confirm chosen approach
- If TDD: Print the first test to write with full code skeleton
- Prompt to continue to implementation

## Testing Reference

Check the target repository's AGENTS.md or testing documentation for project-specific patterns.

### Common Test Structure

- **Unit tests:** Colocated `*.test.ts` files
- **Component tests:** `MyComponent.test.ts` next to component file
- **Store tests:** `src/stores/*.test.ts`
- **E2E tests:** `tests/**/*.spec.ts` or `e2e/**/*.spec.ts`

### Common Commands

```bash
pnpm test:unit                          # Run all unit tests
pnpm test:unit -- src/path/file.test.ts # Run specific test
pnpm test:unit -- --watch               # Watch mode
```

Check AGENTS.md or package.json for project-specific test commands.

### Testing Principles

- No change detector tests
- Behavioral coverage
- Don't mock what you don't own
- Don't just test mocks

## When TDD Doesn't Fit

For these cases, recommend writing tests after:

- Exploratory prototyping
- UI tweaks with unclear final state
- Simple config changes
- Highly integrated changes where test setup is complex

For bug fixes, always recommend writing a test that reproduces the bug first (this is TDD).
