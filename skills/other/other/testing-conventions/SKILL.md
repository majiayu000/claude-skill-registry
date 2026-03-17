---
name: testing-conventions
description: Vitest 4 + Playwright testing conventions: query priority (getByRole > getByText > getByTestId), seed-resilient patterns, realistic user flows (happy path & early finish), virtualized lists, fake-indexeddb isolation, factories, and gotchas (database reset, userEvent, expect.poll). Triggers: "query priority", "getByRole", "getByTestId", "getByLabelText", "querySelector", "seed data", "test invariants", "test isolation", "fake-indexeddb", "database reset", "expect.poll", "expect.element", "assertion", "userEvent", "realistic flows", "early finish", "virtualized list", "virtual scroll", "scoped query", "animation test", "visual state", "factory", "workoutBuilder", "flaky test", "navigation test", "exercise selection", "data attribute query", "test cleanup", "test gotchas".
---

# Testing Conventions

Complements the `vue-integration-testing` skill with project-specific conventions.

## Stack

**Framework**: Vitest 4 with Playwright browser mode (NOT jsdom)

**Test isolation**: `fake-indexeddb` (NOT real IndexedDB)

## Query Priority

Use `page` from `vitest/browser`:

1. `page.getByRole` (best) - Accessible queries
2. `page.getByLabelText` - Form fields
3. `page.getByText` - Non-interactive elements
4. `page.getByTestId` (last resort)

```ts
import { page } from 'vitest/browser'

// GOOD
page.getByRole('button', { name: /start workout/i })

// LAST RESORT
page.getByTestId('workout-timer')
```

### When querySelector Is Acceptable

Vitest 4.x lacks `locators.extend()`. Use `querySelector` with eslint-disable for:

**1. CSS class assertions (animation/visual state):**
```ts
await expect.poll(() => {
  // eslint-disable-next-line no-restricted-syntax -- Testing animation class
  return document.querySelector('.animate-ping') !== null
}).toBe(true)
```

**2. Scoped queries within located elements:**
```ts
// PREFERRED: Chained locator
const card = page.getByRole('article', { name: 'Bench Press' })
const removeBtn = card.getByRole('button', { name: /remove/i })

// ACCEPTABLE: When card is already a DOM element
// eslint-disable-next-line no-restricted-syntax -- Scoped query within card
const removeBtn = card.querySelector('button[aria-label*="remove" i]')
```

**3. Raw DOM element tests (video, hidden file inputs):**
```ts
// eslint-disable-next-line no-restricted-syntax -- Raw DOM test
expect(document.querySelector('video')).toBeTruthy()
```

**4. Data attribute queries:**
```ts
// eslint-disable-next-line no-restricted-syntax -- Data attribute query
const completedSets = dialog.querySelectorAll('[data-set-state="completed"]')
```

## Assertions

```ts
// DOM visibility - use expect.element()
await expect.element(page.getByText(/block 1/i)).toBeVisible()

// Non-DOM state - use expect.poll()
await expect.poll(() => app.router.currentRoute.value.path).toBe('/workout')

// Database - use expect.poll() with async
await expect.poll(async () => {
  const template = await db.templates.get('id')
  return template?.name
}).toBe('My Template')
```

## Seed Data Resilience (IMPORTANT)

Seed data evolves. Tests that assume specific seed data break unexpectedly.

### Pattern: Test Invariants, Not Specific Data

```ts
// FRAGILE - assumes exactly 1 "Deadlift" exists
const matches = buttons.filter(btn => btn.textContent?.includes('Deadlift'))
expect(matches.length).toBe(1)

// RESILIENT - tests the invariant (no duplicates)
const names = buttons.map(btn => btn.textContent?.trim())
const uniqueNames = new Set(names)
expect(names.length).toBe(uniqueNames.size)
```

### Pattern: Create Controlled Test Data

```ts
// FRAGILE - depends on seed data
await userEvent.fill(searchInput, 'Deadlift')
expect(results.length).toBe(1)

// RESILIENT - create unique test data
await db.exercises.add({
  id: 'test-unique-exercise',
  name: 'Zzzz Unique Test Exercise',
  muscle: 'chest',
  equipment: 'barbell',
})
await userEvent.fill(searchInput, 'Zzzz Unique')
await expect.element(page.getByText('Zzzz Unique Test Exercise')).toBeVisible()
```

### Pattern: Test Behavior, Not Implementation

```ts
// FRAGILE - count changes with seed data
expect(exercises.length).toBe(134)

// RESILIENT - tests behavior
expect(exercises.length).toBeGreaterThan(0)
expect(exercises.every(e => e.name && e.muscle)).toBe(true)
```

### Pattern: Use Exact Matches When Filtering

```ts
// FRAGILE - partial match catches unexpected exercises
const deadlifts = exercises.filter(e => e.name.includes('Deadlift'))

// RESILIENT - exact match
const deadlift = exercises.find(e => e.name === 'Deadlift')
```

## Exercise Selection in Tests

The exercise list has 130+ items and is virtualized. Tests can break when:
- **Partial name matching**: "Squat" might match "Belt Squat Machine" before "Bodyweight Squat"
- **Virtualized lists**: Exercises may scroll off-screen

```ts
// BAD - partial names are fragile
await userEvent.click(common.getDialogButton('Squat'))

// GOOD - use full exact names
await userEvent.click(common.getDialogButton('Bodyweight Squat'))

// GOOD - use exercises at START of alphabet (A-B visible without scrolling)
await expect.element(page.getByText('Assisted Pull-up Machine')).toBeVisible()
```

## Test Realistic User Flows

Don't just test happy paths. Real users often finish early.

```ts
// HAPPY PATH ONLY - user completes all sets
await workout.completeMultipleSets(3, { weight: '80', reps: '10', rir: '2' })

// REALISTIC - user enters data but finishes early via menu
const setRow = workout.getSet(0)
await setRow.fill({ kg: 80, reps: 10, rir: 2 })  // Enter data, DON'T click complete
await workout.openMenu()
await page.getByRole('menuitem', { name: /end workout/i }).click()
```

**Key flows to test:**
1. Complete all sets → finish (happy path)
2. Enter data → finish early via menu (realistic)
3. No data entered → finish early (edge case)

## Navigation Reliability

UI button clicks for navigation can be flaky. Prefer direct router navigation:

```ts
// FLAKY - clicking UI buttons for navigation
await userEvent.click(page.getByRole('button', { name: /go back/i }))

// RELIABLE - direct router navigation
await navigateTo('/exercises')
```

Use UI navigation only when testing the navigation behavior itself.

## Factory Usage

```ts
// In-memory workout (composable tests)
import { workoutBuilder } from '@/__tests__/factories/workout.builder'
const workout = workoutBuilder()
  .withStrengthBlock({ exerciseName: 'Squat' })
  .build()

// Database workout (integration tests)
import { dbWorkoutBuilder } from '@/__tests__/factories/dbWorkout.factory'
const dbWorkout = await dbWorkoutBuilder()
  .withExercise('Deadlift', 3)
  .build()
```

## Core Gotchas

1. **Always reset database**: `await resetDatabase()` in `beforeEach`
2. **Always cleanup**: `app.cleanup()` at end of test
3. **Use userEvent**: NOT fireEvent
4. **Locators work directly**: Don't use `.element()` for userEvent clicks
