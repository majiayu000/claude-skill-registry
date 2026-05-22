---
name: e2e
description: E2E testing patterns for kspec web UI. Use when writing Playwright tests, debugging hydration issues, or working with daemon fixtures.
---

# E2E Testing Skill

Learnings and patterns from completed E2E work (tasks.spec.ts, items.spec.ts).

## Quick Reference

| Scenario | Pattern | Example |
|----------|---------|---------|
| Isolated daemon | `import { test } from '../fixtures/test-base'` | Every E2E test |
| Select dropdown (bits-ui) | Click trigger → `getByRole('option')` or `locator('[data-slot="select-item"]')` | Filter tests |
| Text input | `pressSequentially()` with delay | Tag filter |
| Wait for API | `waitForRequest()` | Action tests |
| Wait for URL | `waitForURL(/pattern/)` | Navigation tests |
| Scoped selectors | `.locator('> div').first().getByTestId()` | Tree nav |
| Content check | `toContainText()` not just `toBeVisible()` | All tests |

## Fixture Architecture

### Test-base.ts Pattern

The `test-base.ts` fixture creates a completely isolated environment per test:

```typescript
// Key steps performed automatically:
1. Kill any existing daemon on port 3456
2. Create temp dir with .kspec/ subdirectory
3. Copy E2E fixtures from packages/web-ui/tests/fixtures/
4. Initialize git repo with test user config
5. Create fake shadow worktree structure:
   - .git/worktrees/-kspec/ directory
   - .kspec/.git file with "gitdir:" pointer
6. Start daemon: kspec serve start --daemon --port 3456
7. Set WEB_UI_DIR for static serving
8. Wait 2 seconds for daemon readiness
9. Provide isolated fixture to test
10. Cleanup: stop daemon, remove temp directory
```

**Key file locations:**
- `packages/web-ui/tests/fixtures/` - E2E YAML fixtures
- `packages/web-ui/tests/fixtures/test-base.ts` - Fixture setup
- `packages/web-ui/tests/e2e/*.spec.ts` - Test files

### Fixture Isolation is Non-Negotiable

E2E fixtures MUST be separate from unit test fixtures:

```
tests/fixtures/           ← Unit test fixtures (shared)
packages/web-ui/tests/fixtures/  ← E2E fixtures (isolated)
```

**Why:** E2E daemon mutations affect fixtures. Unit tests need stable data.

## ULID Format Requirements

**Critical:** ULIDs use Crockford base32 which **excludes I, L, O, U**.

```typescript
// INVALID ULIDs - contain forbidden characters
'01TASK100...'   // I is invalid
'01MODULE0...'   // O and U are invalid
'01TRAIT10...'   // I is invalid

// VALID ULIDs - only 0-9, A-H, J-K, M-N, P-T, V-Z
'01TASK0000...'  // T, A, S, K are all valid
'01TRATT100...'  // No I, L, O, U
```

**Recommendation:** Use `testUlid()` helper from `tests/helpers/cli.ts`:

```typescript
import { testUlid, testUlids } from '../../helpers/cli';

const taskId = testUlid('TASK');     // '01TASK00000000000000000000'
const traitId = testUlid('TRAIT');   // '01TRAJT0000000000000000000' (I auto-replaced)
const [id1, id2, id3] = testUlids('TASK', 3);
```

## Svelte 5 SSR/Hydration Gotchas

### Problem: $state Variables Don't React After Hydration

**Symptom:** Detail panel state updates correctly but UI doesn't re-render.

**Root cause:** `adapter-static` pre-renders pages. After hydration, reactive subscriptions with `$state` can disconnect.

**Solution 1 (Preferred):** Disable SSR for interactive pages

```typescript
// +page.ts
export const ssr = false;
```

**Solution 2:** Use $state object pattern with flushSync

```typescript
let panel = $state<{ open: boolean; task: Task | null }>({
  open: false,
  task: null
});

// When updating, use flushSync for synchronous DOM update
import { flushSync } from 'svelte';

flushSync(() => {
  panel.task = task;
  panel.open = true;
});
```

### Problem: URL Param Changes Don't Trigger Reactivity

**Symptom:** Clicking navigation that uses `goto()` doesn't reload data.

**Root cause:** Client-side navigation bypasses component mount.

**Solution:** Use reactive `$:` blocks instead of `onMount`:

```typescript
// BAD - only runs once
onMount(() => {
  loadItem(ref);
});

// GOOD - reacts to URL changes
$: if (ref && open) {
  loadItem(ref);
}
```

### Problem: bits-ui Select Returns Array

**Symptom:** Selecting "in_progress" produces `['i', 'n', '_', 'p', 'r', 'o', 'g', 'r', 'e', 's', 's', 'in_progress']`

**Solution:** Take last element if array:

### bits-ui Select E2E Selectors

bits-ui Select components use **both** standard ARIA roles and `data-slot` attributes. Either selector approach works:

```typescript
// Open dropdown
await page.getByTestId('my-select-trigger').click();

// Option 1: Standard ARIA role (recommended - more semantic)
await page.getByRole('option', { name: 'Option Name' }).click();

// Option 2: data-slot attribute (alternative)
const dropdown = page.locator('[data-slot="select-content"]');
await dropdown.locator('[data-slot="select-item"]').filter({ hasText: 'Option Name' }).click();
```

**Note:** Each select item element has both `role="option"` and `data-slot="select-item"` attributes.

```typescript
function updateFilter(key: string, value: string | string[] | undefined) {
  let actualValue: string | undefined;
  if (Array.isArray(value)) {
    actualValue = value.length > 0 ? value[value.length - 1] : undefined;
  } else {
    actualValue = value;
  }
  // ... rest of filter logic
}
```

## Common Test Patterns

### Filter Testing

```typescript
// Select dropdown - both role="option" and data-slot work
const filterStatus = page.getByTestId('filter-status');
await filterStatus.click();

// Click option using ARIA role (recommended)
await page.getByRole('option', { name: 'Pending', exact: true }).click();
await page.waitForURL(/status=pending/);

// Text input - use pressSequentially, not fill()
const filterTag = page.getByTestId('filter-tag');
await filterTag.click();
await filterTag.pressSequentially('e2e', { delay: 50 });
await page.waitForURL(/tag=e2e/);
```

### Detail Panel Testing

```typescript
// Open panel
const item = page.getByTestId('list-item').first();
await item.click();

// Verify panel content
const panel = page.getByTestId('detail-panel');
await expect(panel).toBeVisible();
await expect(panel.getByTestId('title')).toContainText('Expected Title');
```

### API Request Verification

```typescript
// Verify API call was made, not just UI state
const requestPromise = page.waitForRequest((req) =>
  req.url().includes('/api/tasks/') && req.url().includes('/start')
);
await startButton.click();
const request = await requestPromise;
expect(request.method()).toBe('POST');
```

### Tree/Hierarchy Navigation

```typescript
// Get module node
const specTree = page.getByTestId('spec-tree').first();
const moduleNode = specTree.locator('[data-testid*="tree-node-module"]').first();

// Expand module (expand toggle is sibling to node-title)
const expandToggle = moduleNode.locator('> div').first().getByTestId('expand-toggle');
await expandToggle.click();

// Find child feature after expansion
const childContainer = moduleNode.getByTestId('tree-node-child');
const featureNode = childContainer.locator('[data-testid*="tree-node-feature"]').first();
await expect(featureNode).toBeVisible();
```

### Navigation Verification

```typescript
// Verify navigation occurred
const link = page.getByTestId('spec-ref-link');
await link.click();
await page.waitForURL(/\/items\?ref=/);

// Verify content loaded after navigation
const detail = page.getByTestId('item-detail');
await expect(detail).toBeVisible();
```

## data-testid Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Lists | `{entity}-list` | `task-list`, `spec-tree` |
| List items | `{entity}-list-item` or `tree-node-{type}` | `task-list-item`, `tree-node-module` |
| Detail panels | `{entity}-detail-panel` | `task-detail-panel`, `spec-detail-panel` |
| Filters | `filter-{name}` | `filter-status`, `filter-tag` |
| Badges | `{entity}-{field}` | `task-status-badge`, `task-priority` |
| Buttons | `{action}-{entity}-button` or `{action}-button` | `start-task-button`, `expand-toggle` |
| Counts | `{entity}-count-{status}` | `task-count-ready`, `task-count-blocked` |

## WebSocket Testing

### Current Limitation

Daemon WebSocket in E2E tests returns 200 instead of 101 for upgrade handshake.

**Impact:** WebSocket connection tests fail in E2E environment.

### Workaround Options

1. **Skip with documentation:**
   ```typescript
   test.skip('counts animate on WebSocket update', async ({ page }) => {
     // Skipped: Daemon WebSocket upgrade returns 200 in E2E environment
     // See: AGENTS.md "CI Limitations" section
   });
   ```

2. **Test API triggers instead:** Verify API calls that would trigger WebSocket events:
   ```typescript
   test('task update triggers refetch', async ({ page, daemon }) => {
     // Trigger update via API
     const response = await fetch(`${daemon.url}/api/tasks/${id}/start`, {
       method: 'POST'
     });
     expect(response.ok).toBe(true);

     // Verify UI updates (without WebSocket, need page reload)
     await page.reload();
     await expect(page.getByTestId('task-status')).toContainText('In Progress');
   });
   ```

### When WebSocket Works

Full test pattern for future:
```typescript
test('counts animate on update', async ({ page, daemon }) => {
  await page.goto('/');

  // Get initial count
  const countEl = page.getByTestId('task-count-in_progress');
  const initialCount = await countEl.textContent();

  // Trigger task start via API
  await fetch(`${daemon.url}/api/tasks/${taskId}/start`, { method: 'POST' });

  // Wait for animation class
  await expect(countEl).toHaveClass(/animate-pulse/);

  // Verify count changed
  await expect(countEl).not.toContainText(initialCount!);
});
```

## New E2E Test Checklist

Before writing a new E2E test:

- [ ] Fixtures have required data (tasks, items, meta with variety)
- [ ] ULIDs are valid Crockford base32 (no I, L, O, U)
- [ ] Import from `../fixtures/test-base` (not Playwright direct)
- [ ] Use `daemon` fixture parameter for isolated environment
- [ ] Components have data-testid attributes for selectors
- [ ] Use scoped selectors with `.first()` for ambiguous queries
- [ ] Verify API calls with `waitForRequest()`, not just UI
- [ ] Check URL params with `waitForURL()` for navigation tests
- [ ] Test content with `toContainText()`, not just visibility
- [ ] Include variety: happy path, edge cases, responsive

## Fixture Data Requirements

### Task Status Variety

Fixtures should include tasks with all statuses:
- `pending` (ready - no unmet dependencies)
- `in_progress` (started)
- `pending_review` (code done, awaiting merge)
- `blocked` (has unmet dependencies)
- `completed` (done)

### Hierarchy for Tree Tests

```yaml
modules:
  - _ulid: 01M0DULE00000000000000000
    type: module
    features:
      - _ulid: 01FEATURE0000000000000000
        type: feature
        requirements:
          - _ulid: 01REQVREMENT000000000000
            type: requirement
```

### Linked Data

- Tasks with `spec_ref` pointing to spec items
- Items with `traits` array referencing trait items
- Observations with `spec_ref` or `task_ref` links

## Debugging Tips

### Test Passes Locally, Fails in CI

1. **Check file watchers:** CI containers don't support recursive `fs.watch`. Tests using watchers are skipped in CI.
2. **Check port conflicts:** E2E uses port 3456. Previous daemon may not have cleaned up.
3. **Check fixture paths:** CI paths may differ. Use relative paths in fixtures.

### Element Not Found

1. **SSR timing:** Add `{ timeout: 5000 }` to assertions
2. **Scope correctly:** Use `element.getByTestId()` not `page.getByTestId()`
3. **Wait for load:** `await page.waitForLoadState('networkidle')`

### State Not Updating

1. **Check SSR:** Add `export const ssr = false` to page
2. **Check reactivity:** Use `$:` blocks for URL-driven state
3. **Check flushSync:** For synchronous DOM updates

## Anti-Patterns

### Don't: Conditional Assertions

```typescript
// BAD - hides failures
if (await element.isVisible()) {
  await expect(element).toContainText('value');
}

// GOOD - fails clearly
await expect(element).toBeVisible();
await expect(element).toContainText('value');
```

### Don't: Share Fixtures with Unit Tests

```typescript
// BAD - mutations affect unit tests
await copyFixtures('../../tests/fixtures/');

// GOOD - isolated E2E fixtures
await copyFixtures('../fixtures/');  // packages/web-ui/tests/fixtures/
```

### Don't: Test UI State Only

```typescript
// BAD - doesn't verify API call
await startButton.click();
await expect(statusBadge).toContainText('In Progress');

// GOOD - verifies both
const req = await page.waitForRequest(r => r.url().includes('/start'));
expect(req.method()).toBe('POST');
await expect(statusBadge).toContainText('In Progress');
```

## Related Skills

- `/svelte-5` - Svelte 5 patterns, SSR, reactivity
- `/local-review` - Pre-PR quality checks
- `/task-work` - Task lifecycle workflow
