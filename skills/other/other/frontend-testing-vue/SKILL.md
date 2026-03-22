---
name: frontend-testing-vue
description: Generate Vitest + Vue Test Utils tests for Nuxt 4 components, composables, stores, and server routes. Triggers on testing, spec files, coverage, Vitest, Vue Test Utils, unit tests, integration tests, or write/review test requests.
---

# Vue 3 / Nuxt 4 Frontend Testing Skill

This skill enables Claude to generate high-quality, comprehensive frontend tests for Vue 3/Nuxt 4 projects following established conventions and best practices.

## When to Apply This Skill

Apply this skill when the user:

- Asks to **write tests** for a component, composable, store, or server route
- Asks to **review existing tests** for completeness
- Mentions **Vitest**, **Vue Test Utils**, or **test files**
- Requests **test coverage** improvement
- Mentions **testing**, **unit tests**, or **integration tests** for frontend code
- Wants to understand **testing patterns** in a Vue/Nuxt codebase

**Do NOT apply** when:

- User is asking about E2E tests (Playwright) - separate skill
- User is only asking conceptual questions without code context

## Design for Testability

⚠️ **Tests assume code is designed for testability. If testing is difficult:**

1. Review `docs/development/CODE_DESIGN_PRINCIPLES.md`
2. Extract business logic to composables (testable without DOM)
3. Use typed props/emits for clear contracts
4. Minimize component dependencies

**Signs code needs refactoring:**
- Can't test logic without rendering entire component tree
- Test setup requires 20+ lines of mocks
- Tests fail when unrelated UI changes
- Can't test in isolation

## Quick Reference

### Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Vitest | 3.x | Test runner |
| Vue Test Utils | 2.4.x | Component testing |
| jsdom | - | Unit test environment |
| node | - | Integration test environment |
| Pinia Testing | 1.x | Store testing |
| TypeScript | 5.x | Type safety |

### Key Commands

```bash
# Run all unit tests
pnpm test:unit

# Watch mode
pnpm test:unit:watch

# Run specific file
pnpm test:unit path/to/file.test.ts

# Generate coverage report
pnpm test:coverage

# Run integration tests
pnpm test:integration

# Quick test (changed files only)
pnpm test:quick
```

### File Naming

- Unit tests: `*.test.ts` (co-located or in `tests/` directory)
- E2E tests: `*.spec.ts` (in `tests/e2e/`)
- Integration tests: `tests/integration/`

## Test Structure Template

```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import ComponentName from '~/components/ComponentName.vue'

// ✅ Mock external dependencies only
vi.mock('~/composables/useApi', () => ({
  useApi: vi.fn(() => ({
    data: ref(null),
    pending: ref(false),
    error: ref(null),
  })),
}))

describe('ComponentName', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  // Rendering tests (REQUIRED)
  describe('Rendering', () => {
    it('should render without crashing', () => {
      const wrapper = mount(ComponentName, {
        props: { title: 'Test' },
      })
      
      expect(wrapper.text()).toContain('Test')
    })
  })

  // Props tests (REQUIRED)
  describe('Props', () => {
    it('should apply custom class', () => {
      const wrapper = mount(ComponentName, {
        props: { class: 'custom' },
      })
      
      expect(wrapper.classes()).toContain('custom')
    })
  })

  // User Interactions
  describe('User Interactions', () => {
    it('should emit click event', async () => {
      const wrapper = mount(ComponentName)
      
      await wrapper.find('button').trigger('click')
      
      expect(wrapper.emitted('click')).toHaveLength(1)
    })
  })

  // Edge Cases (REQUIRED)
  describe('Edge Cases', () => {
    it('should handle null data', () => {
      const wrapper = mount(ComponentName, {
        props: { data: null },
      })
      
      expect(wrapper.text()).toContain('No data')
    })
  })
})
```

## Testing Workflow (CRITICAL)

### ⚠️ Incremental Approach Required

**NEVER generate all test files at once.** For complex components or multi-file directories:

1. **Analyze & Plan**: List all files, order by complexity (simple → complex)
2. **Process ONE at a time**: Write test → Run test → Fix if needed → Next
3. **Verify before proceeding**: Do NOT continue to next file until current passes

```
For each file:
  ┌─────────────────────────────────────────┐
  │ 1. Write test                           │
  │ 2. Run: pnpm test:unit <file>.test.ts   │
  │ 3. PASS? → Mark complete, next file     │
  │    FAIL? → Fix first, then continue     │
  └─────────────────────────────────────────┘
```

### Complexity-Based Order

Process in this order for multi-file testing:

1. 🟢 Utility functions (simplest)
2. 🟢 Composables (isolated logic)
3. 🟢 Pinia stores
4. 🟡 Simple components (presentational)
5. 🟡 Medium components (state, effects)
6. 🔴 Complex components (API, routing)
7. 🔴 Server routes
8. 🔴 Integration tests (last)

> 📖 See `references/workflow.md` for complete workflow details.

## Testing Strategy

### Dynamic Import Pattern (CRITICAL for Nuxt)

Because Nuxt auto-imports composables, **always use dynamic imports after mocking**:

```typescript
// ✅ CORRECT: Mock BEFORE dynamic import
vi.mock('vue-router', () => ({
  useRouter: vi.fn(() => ({ push: vi.fn() })),
  useRoute: vi.fn(() => ({ params: {} })),
}))

const { useMyComposable } = await import('~/composables/useMyComposable')

// ❌ WRONG: Static import with mocks
import { useMyComposable } from '~/composables/useMyComposable' // Mocks won't work!
```

### What to Mock vs Import Real

| Category | Action |
|----------|--------|
| Nuxt composables (`useRoute`, `useFetch`) | Mock via globals |
| Pinia stores | Use real with `setActivePinia()` |
| UI components (Reka UI, shadcn) | Import real |
| API calls (`$fetch`) | Mock via `vi.stubGlobal` |
| Supabase client | Mock |
| i18n (`useI18n`) | Mock via globals |

## Core Principles

### 1. AAA Pattern (Arrange-Act-Assert)

```typescript
it('should filter products by category', () => {
  // Arrange
  const wrapper = mount(ProductList, {
    props: { products: mockProducts },
  })
  
  // Act
  await wrapper.find('[data-testid="category-filter"]').setValue('electronics')
  
  // Assert
  expect(wrapper.findAll('.product-item')).toHaveLength(3)
})
```

### 2. Test Observable Behavior

```typescript
// ✅ Good: Test what user sees
expect(wrapper.text()).toContain('Loading...')

// ❌ Bad: Test internal state
expect(wrapper.vm.isLoading).toBe(true)
```

### 3. Single Behavior Per Test

```typescript
// ✅ Good: One behavior
it('should disable button when loading', () => {
  const wrapper = mount(Button, { props: { loading: true } })
  expect(wrapper.find('button').attributes('disabled')).toBeDefined()
})

// ❌ Bad: Multiple behaviors
it('should handle loading state', () => {
  const wrapper = mount(Button, { props: { loading: true } })
  expect(wrapper.find('button').attributes('disabled')).toBeDefined()
  expect(wrapper.text()).toContain('Loading...')
  expect(wrapper.classes()).toContain('loading')
})
```

### 4. Semantic Naming

Use `should <behavior> when <condition>`:

```typescript
it('should show error message when validation fails')
it('should emit submit when form is valid')
it('should disable input when isReadOnly is true')
```

## Required Test Scenarios

### Always Required (All Components)

1. **Rendering**: Component renders without crashing
2. **Props**: Required props, optional props, default values
3. **Edge Cases**: null, undefined, empty values, boundary conditions

### Conditional (When Present)

| Feature | Test Focus |
|---------|-----------|
| `ref`/`reactive` | Initial state, transitions |
| `watch`/`watchEffect` | Trigger conditions, cleanup |
| Event handlers | `@click`, `@input`, `@submit`, keyboard |
| API calls | Loading, success, error states |
| Routing | Navigation, params, query strings |
| `computed` | Derived values |
| Pinia stores | State, getters, actions |
| `emit` | Event emission with payloads |

## Coverage Goals

Current project thresholds (from `vitest.config.ts`):

- ✅ **≥70%** branch coverage (currently ~75%)
- ✅ **≥55%** function coverage (currently ~60%)
- ✅ Lines/statements: Uses negative threshold (-145000 uncovered max) to prevent regression

Note: Negative thresholds mean "maximum uncovered lines allowed" - this prevents regressions while allowing incremental improvement.

## Detailed Guides

For more detailed information, refer to:

- `references/workflow.md` - Incremental testing workflow
- `references/mocking.md` - Mock patterns for Nuxt/Vue
- `references/async-testing.md` - Async operations and API calls
- `references/composables.md` - Composable testing patterns
- `references/stores.md` - Pinia store testing
- `references/server-routes.md` - API route testing
- `references/common-patterns.md` - Frequently used patterns
- `references/checklist.md` - Test generation checklist

## Project-Specific Configuration

### Alias Resolution

Tests use these path aliases (from `vitest.config.ts`):

```typescript
'~': './'                                              // Nuxt alias
'@': './'                                              // Alternative root alias
'~~': './'                                             // Nuxt double-tilde alias
'@@': './'                                             // Alternative double alias
'#app': './.nuxt'                                      // Nuxt app directory
'#imports': './tests/setup/nuxt-imports-mock.ts'       // Auto-imports mock
'vue-i18n': './tests/setup/vue-i18n-mock.ts'           // i18n mock
'pinia': './node_modules/pinia'                        // Real Pinia
'#supabase/server': './tests/server/utils/mocks/...'   // Server Supabase mock
'#nitro': './tests/server/utils/mocks/nitro.mock.ts'   // Nitro mock
'h3': './tests/server/utils/mocks/h3.mock.ts'          // H3 utilities mock
```

### Global Mocks (Auto-loaded)

These are mocked globally in `tests/setup/vitest.setup.ts`:

- `useI18n` - Returns key with parameter interpolation
- `useRoute` / `useRouter` - Basic routing mocks
- `useLocalePath` - Returns path with locale
- `navigateTo` - Navigation mock
- `useCookie` - Cookie storage mock
- `import.meta.client` - Set to `true`
