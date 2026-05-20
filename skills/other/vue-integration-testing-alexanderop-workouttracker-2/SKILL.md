---
name: vue-integration-testing
description: Write Vue 3 integration tests using Vitest Browser Mode and Page Objects. Use proactively whenever adding tests for views, components with routing, user flows, or features that span multiple components. Triggers include "add tests", "write tests", "test this", "needs tests", "integration tests", "test the feature", "test user flow", or any task involving testing UI interactions, navigation, dialogs, forms, or multi-step workflows.
---

# Vue Integration Testing

Write integration tests that verify complete user flows using Vitest Browser Mode (Playwright) with the `createTestApp` helper and Page Objects.

## Test Infrastructure

- **Framework**: Vitest 4 with Playwright browser mode (real browser, not jsdom)
- **Database**: `fake-indexeddb` polyfill for IndexedDB
- **Queries**: Vitest Browser locators with automatic retry

**Commands:**
```bash
pnpm test              # Run all tests
pnpm test:watch        # Watch mode
pnpm test:headed       # Visible browser (debugging)
pnpm test:coverage     # With coverage
```

## Test File Structure

Place integration tests in `src/__tests__/integration/`:

```typescript
import { page, userEvent } from 'vitest/browser'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { createTestApp } from '../helpers/createTestApp'
import { cleanupIntegrationTest, setupIntegrationTest } from '../helpers/integrationSetup'

describe('Feature Name', () => {
  beforeEach(setupIntegrationTest)
  afterEach(cleanupIntegrationTest)

  it('describes the user journey being tested', async () => {
    const app = await createTestApp()

    // Use page objects for interactions
    await app.builder.navigateTo()
    await app.builder.addStrengthBlock('Squats')
    await app.builder.startWorkout()

    // Assert outcomes
    await expect.poll(() => app.router.currentRoute.value.path).toMatch(/^\/workout\/active/)

    app.cleanup()
  })
})
```

## Test Isolation

Tests share `fake-indexeddb`. Always use the provided setup/cleanup helpers:

- `setupIntegrationTest()` - Resets workout state, benchmark state, timers, and database
- `cleanupIntegrationTest()` - Clears state and DOM after each test

## createTestApp API

Returns a `TestApp` object with:

### Core Properties
| Property | Type | Purpose |
|----------|------|---------|
| `router` | `Router` | Vue Router instance for navigation/assertions |
| `container` | `Element` | Rendered DOM container |

### Page Objects
Pre-instantiated helpers for domain-specific UI workflows:

| Property | Purpose |
|----------|---------|
| `common` | Shared UI: dialogs, navigation, exercise selection |
| `builder` | Workout builder operations |
| `workout` | Active workout view (sets, timers, menus) |
| `queue` | Workout queue dialog |
| `benchmarks` | Benchmarks list view |
| `benchmarkForm` | Benchmark creation form |
| `benchmarkDetail` | Benchmark detail view |
| `logPastWorkout` | Past workout logging flow |

### Query Methods
Vitest Browser locators with automatic retry:
- `getByRole(role, options?)` - Query by ARIA role
- `getByText(text, options?)` - Query by text content
- `getByTestId(testId)` - Query by data-testid

### Helper Methods
- `navigateTo(route)` - Programmatic navigation
- `cleanup()` - Unmount the app

### Options
```typescript
const app = await createTestApp({ initialRoute: '/workout/active' })
```

## Page Object Design Principles

Following Martin Fowler's Page Object pattern:

1. **No assertions in POs** - Return predicates/values, let tests assert
2. **Return value objects** - Not raw DOM elements (use SetRowPO instead of HTMLInputElement)
3. **Encapsulate async** - POs handle `flushPromises()`, waits internally
4. **Use data attributes** - Prefer `data-set-state="active"` over CSS class selectors

## Page Object Reference

### CommonPO (Base)
Shared across all page objects:

```typescript
await app.common.waitForDialog()           // Wait for dialog to appear
await app.common.waitForDialogClose()      // Wait for dialog + overlay removal
const button = app.common.getDialogButton('Confirm')  // Find button in dialog
app.common.isDialogOpen()                  // Returns boolean (use in assertions)
await app.common.selectExercise('Squats')  // Search and select exercise
await app.common.waitForRoute(/^\/workout/)  // Wait for route match

// In tests, assert dialog state with:
expect(app.common.isDialogOpen()).toBe(false)
```

### ActiveWorkoutPO
Active workout view interactions:

```typescript
// Wait for UI
await app.workout.waitForTableVisible()

// Set interactions via SetRowPO (preferred - abstracts DOM)
const setRow = app.workout.getSet(0)           // Get SetRowPO by index
const activeSet = await app.workout.getActiveSet()  // Get active SetRowPO
const values = await setRow.getValues()        // { weight, reps, rir }
await setRow.fill({ kg: 100, reps: 8, rir: 2 })
await setRow.complete()
await setRow.isCompleted()                     // Returns boolean

// High-level operations
await app.workout.fillCardSetAndComplete({ weight: '60', reps: '12', rir: '3' })
await app.workout.endWorkoutAndNavigateToSummary()

// UI queries
const menu = await app.workout.getMenuTrigger()
const nextBtn = await app.workout.getFooterButton('next')
await app.workout.isSetCompleted(0)  // Check set completion
```

### SetRowPO
Encapsulates a single set row (returned by `workout.getSet()` or `workout.getActiveSet()`):

```typescript
const setRow = app.workout.getSet(0)

// Get current values as strings (not raw DOM)
const { weight, reps, rir } = await setRow.getValues()

// Fill values
await setRow.fill({ kg: 100, reps: 8, rir: 2 })

// Complete the set
await setRow.complete()

// Or fill and complete in one call
await setRow.fillAndComplete({ weight: '100', reps: '8', rir: '2' })

// Check state (returns boolean for test assertions)
await setRow.isCompleted()
await setRow.isActive()
```

### BuilderPO
Workout builder operations:

```typescript
await app.builder.clickStartNewWorkout()          // Click home page button
await app.builder.navigateTo()                    // Alias for clickStartNewWorkout
await app.builder.openAddBlockDialog()            // Open add block dialog
await app.builder.addStrengthBlock('Squats')      // Full flow to add block
await app.builder.addTimedBlock('AMRAP')          // Add timed block
await app.builder.startWorkout()                  // Start the workout
```

### QueuePO
Workout queue dialog:

```typescript
await app.queue.open()
const items = app.queue.getItems()       // Get all queue items
const active = app.queue.getActiveItem() // Get active item
```

## Query & Assertion Patterns

### Vitest Browser Locators (Preferred)
Locators have built-in retry, pass them directly to userEvent:

```typescript
import { page, userEvent } from 'vitest/browser'

// Click with locator (retries automatically)
await userEvent.click(page.getByRole('button', { name: /submit/i }))

// Fill input
await userEvent.fill(page.getByRole('textbox', { name: /email/i }), 'test@example.com')

// Click directly on locator
await page.getByRole('button', { name: /save/i }).click()
```

### DOM Assertions
Use `expect.element()` for DOM element assertions:

```typescript
await expect.element(page.getByRole('dialog')).toBeVisible()
await expect.element(page.getByRole('button')).toBeDisabled()
await expect.element(page.getByRole('button')).toHaveClass('opacity-0')
await expect.element(page.getByText('Success')).not.toBeInTheDocument()
```

### State/Async Assertions
Use `expect.poll()` for non-DOM state or async values:

```typescript
// Router state
await expect.poll(() => app.router.currentRoute.value.path).toBe('/workout')

// Database queries
await expect.poll(async () => {
  const workout = await db.workouts.get('id')
  return workout?.name
}).toBe('My Workout')

// With custom timeout
await expect.element(page.getByText('Loaded'), { timeout: 5000 }).toBeVisible()
```

### When to Use .element()
Only use `.element()` when you need the actual DOM element:

```typescript
// Need DOM properties
const input = await page.getByRole('textbox').element()
const value = input.value

// DON'T pass .element() to userEvent (loses retry)
// BAD: await userEvent.click(await button.element())
// GOOD: await userEvent.click(button)
```

## Interaction Patterns

### Dialog Flow
```typescript
await userEvent.click(page.getByRole('button', { name: /open/i }))
await app.common.waitForDialog()
await userEvent.click(app.common.getDialogButton('Confirm'))
await app.common.waitForDialogClose()
```

### Dropdown Menu
```typescript
const menuTrigger = await app.workout.getMenuTrigger()
await userEvent.click(menuTrigger)
await expect.element(page.getByRole('menuitem', { name: /end workout/i })).toBeVisible()
await userEvent.click(page.getByRole('menuitem', { name: /end workout/i }))
```

### Complete Workout Flow Example
```typescript
it('completes a strength workout', async () => {
  const app = await createTestApp()

  // Build workout
  await app.builder.navigateTo()
  await app.builder.addStrengthBlock('Squats')
  await app.builder.startWorkout()

  // Wait for table and complete sets
  await app.workout.waitForTableVisible()
  await app.workout.fillCardSetAndComplete({ weight: '100', reps: '5', rir: '2' })

  // Verify prefilled values in next set using SetRowPO
  const activeSet = await app.workout.getActiveSet()
  const values = await activeSet!.getValues()
  expect(values.weight).toBe('100')

  // Complete remaining sets
  await app.workout.fillCardSetAndComplete({ weight: '100', reps: '5', rir: '2' })

  // End workout
  await app.workout.endWorkoutAndNavigateToSummary()

  // Verify
  await expect.element(page.getByText(/workout complete/i)).toBeVisible()

  app.cleanup()
})
```

## Query Selection Guide

| Need | Query |
|------|-------|
| Button by label | `page.getByRole('button', { name: /label/i })` |
| Link | `page.getByRole('link', { name: /text/i })` |
| Heading | `page.getByRole('heading', { name: /title/i })` |
| Text input | `page.getByRole('textbox', { name: /label/i })` |
| Checkbox | `page.getByRole('checkbox', { name: /label/i })` |
| Menu item | `page.getByRole('menuitem', { name: /text/i })` |
| Toggle button | `page.getByRole('button', { pressed: true })` |
| Any text | `page.getByText(/partial text/i)` |
| Test ID | `page.getByTestId('my-element')` |

Use case-insensitive regex (`/text/i`) for resilience.

## Factory Usage

### In-Memory Factories (composable tests)
```typescript
import { workoutBuilder } from '@/__tests__/factories'

const workout = workoutBuilder()
  .withName('Leg Day')
  .withStrengthBlock({ name: 'Squats' })
  .build()
```

### Database Factories (integration tests)
```typescript
import { dbWorkoutBuilder } from '@/__tests__/factories'

const workout = await dbWorkoutBuilder()
  .withName('Test Workout')
  .withStrengthBlock()
  .withDuration(3600)
  .build()

await db.workouts.add(workout)
```

See `src/__tests__/factories/` for available factories.

## Common Gotchas

| Problem | Solution |
|---------|----------|
| Dialog blocks clicks after close | Use `waitForDialogClose()` - waits for dialog AND overlay |
| Number inputs not updating | Page objects use `setInputValueDirectly()` with native setter |
| Animations prevent assertions | Wait for animation or use `.not.toHaveClass('opacity-0')` |
| State leaks between tests | Always use `beforeEach(setupIntegrationTest)` |
| Multiple elements match text | Use specific role query: `getByRole('heading', { name: /title/i })` |
| SVG vs HTML element type | Use `ensureHTMLElement()` helper from `domHelpers.ts` |
| Need to check dialog state | Use `expect(common.isDialogOpen()).toBe(false)` - POs return predicates |
| Accessing input values | Use `setRow.getValues()` not raw `.value` - POs return value objects |
| CSS class selectors brittle | Components use `data-set-state` attributes for testability |
| UI button navigation flaky | Use `navigateTo('/path')` instead of clicking nav buttons |

## Navigation Reliability

**Prefer direct router navigation over UI button clicks** when moving between pages in tests.

UI button clicks for navigation can be flaky in Vitest Browser Mode due to timing issues with button visibility, element overlays, and Vue Router transitions.

```typescript
// ❌ FLAKY - clicking UI buttons for navigation
await userEvent.click(page.getByRole('button', { name: /go back/i }))
await expect.element(page.getByRole('button', { name: /resume workout/i })).toBeVisible()

// ✅ RELIABLE - direct router navigation
await navigateTo('/exercises')
await expect.element(page.getByRole('button', { name: /some button/i })).toBeVisible()
```

**When to use direct navigation:**
- Moving between pages to test a global component (e.g., FAB visibility)
- Setting up test preconditions (navigating to a specific starting route)
- Any navigation that isn't the primary behavior being tested

**When to use UI navigation:**
- Testing the navigation behavior itself (e.g., "clicking Submit navigates to success page")
- User flow tests where the navigation is part of what's being verified
