---
name: frontend-testing
description: Generate Vitest + React Testing Library tests for Desktop Ethereal frontend components, hooks, and utilities. Triggers on testing, spec files, coverage, Vitest, RTL, unit tests, integration tests, or write/review test requests.
---

# Desktop Ethereal Frontend Testing Skill

This skill enables Claude to generate high-quality, comprehensive frontend tests for the Desktop Ethereal project following established conventions and best practices.

> **⚠️ Authoritative Source**: This skill is derived from general testing best practices with adaptations for Tauri/React desktop applications. Use Vitest mock/timer APIs (`vi.*`).

## When to Apply This Skill

Apply this skill when the user:

- Asks to **write tests** for a component, hook, or utility
- Asks to **review existing tests** for completeness
- Mentions **Vitest**, **React Testing Library**, **RTL**, or **spec files**
- Requests **test coverage** improvement
- Mentions **testing**, **unit tests**, or **integration tests** for frontend code

**Do NOT apply** when:

- User is asking about backend/Rust tests
- User is asking about E2E tests (Playwright/Cypress)
- User is only asking conceptual questions without code context

## Quick Reference

### Tech Stack

| Tool | Version | Purpose |
| ------ | --------- | --------- |
| Vitest | ^3.0.4 | Test runner |
| React Testing Library | ^16.2.0 | Component testing |
| jsdom | ^26.0.0 | Test environment |
| TypeScript | ^5.9.3 | Type safety |

### Key Commands

```bash
# Run all tests
pnpm test

# Watch mode
pnpm test:watch

# Run specific file
pnpm test path/to/file.spec.tsx

# Generate coverage report
pnpm test:coverage
```

### File Naming

- Test files: `ComponentName.test.tsx` (same directory as component)
- Integration tests: `src/test/integration/` directory

## Test Structure Template

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import Component from './index'

// ✅ Import real project components (DO NOT mock these)
// import Sprite from '@/components/Sprite'
// import { useEtherealState } from '@/hooks/useEtherealState'

// ✅ Mock external dependencies and Tauri APIs only
vi.mock('@tauri-apps/api/event', () => ({
  listen: vi.fn().mockResolvedValue({ unlisten: vi.fn() }),
}))

vi.mock('@tauri-apps/api/core', () => ({
  invoke: vi.fn(),
}))

// Shared state for mocks (if needed)
let mockSharedState = false

describe('ComponentName', () => {
  beforeEach(() => {
    vi.clearAllMocks()  // ✅ Reset mocks BEFORE each test
    mockSharedState = false  // ✅ Reset shared state
  })

  // Rendering tests (REQUIRED)
  describe('Rendering', () => {
    it('should render without crashing', () => {
      // Arrange
      const props = { title: 'Test' }

      // Act
      render(<Component {...props} />)

      // Assert
      expect(screen.getByText('Test')).toBeInTheDocument()
    })
  })

  // Props tests (REQUIRED)
  describe('Props', () => {
    it('should apply custom className', () => {
      render(<Component className="custom" />)
      expect(screen.getByRole('button')).toHaveClass('custom')
    })
  })

  // User Interactions
  describe('User Interactions', () => {
    it('should handle click events', () => {
      const handleClick = vi.fn()
      render(<Component onClick={handleClick} />)

      fireEvent.click(screen.getByRole('button'))

      expect(handleClick).toHaveBeenCalledTimes(1)
    })
  })

  // Edge Cases (REQUIRED)
  describe('Edge Cases', () => {
    it('should handle null data', () => {
      render(<Component data={null} />)
      expect(screen.getByText(/no data/i)).toBeInTheDocument()
    })

    it('should handle empty array', () => {
      render(<Component items={[]} />)
      expect(screen.getByText(/empty/i)).toBeInTheDocument()
    })
  })
})
```

## Testing Workflow (CRITICAL)

### ⚠️ Incremental Approach Required

**NEVER generate all test files at once.** For complex components or multi-file directories:

1. **Analyze & Plan**: List all files, order by complexity (simple → complex)
1. **Process ONE at a time**: Write test → Run test → Fix if needed → Next
1. **Verify before proceeding**: Do NOT continue to next file until current passes

```
For each file:
  ┌────────────────────────────────────────┐
  │ 1. Write test                          │
  │ 2. Run: pnpm test <file>.test.tsx      │
  │ 3. PASS? → Mark complete, next file    │
  │    FAIL? → Fix first, then continue    │
  │ 4. Check coverage                      │
  └────────────────────────────────────────┘
```

### Complexity-Based Order

Process in this order for multi-file testing:

1. 🟢 Utility functions (simplest)
1. 🟢 Custom hooks
1. 🟡 Simple components (presentational)
1. 🟡 Medium components (state, effects)
1. 🔴 Complex components (API, routing)
1. 🔴 Integration tests (App component - last)

### When to Refactor First

- **Complexity > 50**: Break into smaller pieces before testing
- **500+ lines**: Consider splitting before testing
- **Many dependencies**: Extract logic into hooks first

> 📖 See references/workflow.md for complete workflow details and todo list format.

## Testing Strategy

### Path-Level Testing (Directory Testing)

When assigned to test a directory/path, test **ALL content** within that path:

- Test all components, hooks, utilities in the directory (not just `index` file)
- Use incremental approach: one file at a time, verify each before proceeding
- Goal: 100% coverage of ALL files in the directory

### Integration Testing First

**Prefer integration testing** when writing tests for a directory:

- ✅ **Import real project components** directly (including base components and siblings)
- ✅ **Only mock**: Tauri APIs (`@/tauri-apps/api/*`), external services
- ❌ **DO NOT mock** project components unless absolutely necessary
- ❌ **DO NOT mock** sibling/child components in the same directory

> See [Test Structure Template](#test-structure-template) for correct import/mock patterns.

## Core Principles

### 1. AAA Pattern (Arrange-Act-Assert)

Every test should clearly separate:

- **Arrange**: Setup test data and render component
- **Act**: Perform user actions
- **Assert**: Verify expected outcomes

### 2. Black-Box Testing

- Test observable behavior, not implementation details
- Use semantic queries (getByRole, getByLabelText)
- Avoid testing internal state directly
- **Prefer pattern matching over hardcoded strings** in assertions:

```typescript
// ❌ Avoid: hardcoded text assertions
expect(screen.getByText('Loading...')).toBeInTheDocument()

// ✅ Better: role-based queries
expect(screen.getByRole('status')).toBeInTheDocument()

// ✅ Better: pattern matching
expect(screen.getByText(/loading/i)).toBeInTheDocument()
```

### 3. Single Behavior Per Test

Each test verifies ONE user-observable behavior:

```typescript
// ✅ Good: One behavior
it('should disable button when loading', () => {
  render(<Button loading />)
  expect(screen.getByRole('button')).toBeDisabled()
})

// ❌ Bad: Multiple behaviors
it('should handle loading state', () => {
  render(<Button loading />)
  expect(screen.getByRole('button')).toBeDisabled()
  expect(screen.getByText('Loading...')).toBeInTheDocument()
  expect(screen.getByRole('button')).toHaveClass('loading')
})
```

### 4. Semantic Naming

Use `should <behavior> when <condition>`:

```typescript
it('should show error message when validation fails')
it('should call onSubmit when form is valid')
it('should disable input when isReadOnly is true')
```

## Required Test Scenarios

### Always Required (All Components)

1. **Rendering**: Component renders without crashing
1. **Props**: Required props, optional props, default values
1. **Edge Cases**: null, undefined, empty values, boundary conditions

### Conditional (When Present)

| Feature | Test Focus |
| --------- | ----------- |
| `useState` | Initial state, transitions, cleanup |
| `useEffect` | Execution, dependencies, cleanup |
| Event handlers | All onClick, onChange, onSubmit, keyboard |
| Tauri IPC calls | Loading, success, error states |
| `useCallback`/`useMemo` | Referential equality |
| Context | Provider values, consumer behavior |
| Forms | Validation, submission, error display |

## Coverage Goals (Per File)

For each test file generated, aim for:

- ✅ **100%** function coverage
- ✅ **100%** statement coverage
- ✅ **>95%** branch coverage
- ✅ **>95%** line coverage

> **Note**: For multi-file directories, process one file at a time with full coverage each. See `references/workflow.md`.

## Tauri-Specific Considerations

### Mocking Tauri APIs

Always mock Tauri APIs in tests:

```typescript
// Mock Tauri event system
vi.mock('@tauri-apps/api/event', () => ({
  listen: vi.fn().mockImplementation((event, callback) => {
    // Simulate event emission for testing
    return Promise.resolve({ unlisten: vi.fn() })
  }),
}))

// Mock Tauri command invocations
vi.mock('@tauri-apps/api/core', () => ({
  invoke: vi.fn().mockResolvedValue('mock result'),
}))
```

### Testing Event-Driven Components

For components that respond to Tauri events:

```typescript
it('should update state when gpu-update event is received', async () => {
  // Mock the listen function to immediately call the callback
  const mockListen = vi.mocked(listen)
  mockListen.mockImplementation((event, callback) => {
    if (event === 'gpu-update') {
      callback({ payload: { temperature: 85 } })
    }
    return Promise.resolve({ unlisten: vi.fn() })
  })

  render(<EtherealStatusBar />)

  // Wait for state update
  await waitFor(() => {
    expect(screen.getByText('OVERHEATING')).toBeInTheDocument()
  })
})
```

## Detailed Guides

For more detailed information, refer to:

- `references/workflow.md` - **Incremental testing workflow** (MUST READ for multi-file testing)
- `references/mocking.md` - Mock patterns and best practices
- `references/async-testing.md` - Async operations and API calls
- `references/common-patterns.md` - Frequently used testing patterns
- `references/checklist.md` - Test generation checklist and validation steps

## Authoritative References

### Primary Specification (MUST follow)

- **`docs/testing.md`** - The canonical testing specification for Desktop Ethereal.

### Reference Examples in Codebase

- `src/hooks/useEtherealState.test.ts` - Custom hook tests
- `src/components/Sprite.test.tsx` - Component tests (to be created)
- `src/test/setup.ts` - Global test setup

### Project Configuration

- `vitest.config.ts` - Vitest configuration
- `src/test/setup.ts` - Test environment setup
