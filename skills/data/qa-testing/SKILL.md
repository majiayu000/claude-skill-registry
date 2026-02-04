---
name: qa-testing
version: "2.0"
description: Ensure data integrity, stability, and basic security for a personal productivity app. Focus on preventing data loss, memory leaks, and sync failures during daily 8-hour usage sessions. Skip enterprise-grade testing. Use when testing, verifying, validating, checking features, running tests, or before claiming anything is "done" or "fixed".
triggers:
  - "test task persistence"
  - "verify offline sync"
  - "check for memory leaks"
  - "test data integrity"
  - "run QA checklist"
  - "verify backup restore"
  - "test Supabase RLS"
  - "check Pomodoro timer accuracy"
  - "before marking features complete"
  - "test canvas geometry"
  - "run geometry tests"
  - "test sync behavior"
  - "verify smart group"
  - "canvas invariants"
  - "check position stability"
---

# QA Testing Skill for Personal Productivity App

**Version:** 2.0
**Last Updated:** January 2026
**App Stack:** Vue 3 + Supabase (auth + sync) + SQLite local backup
**Views:** Pomodoro timer, Kanban board, Calendar, Canvas (node-based)
**Target:** Desktop browser only, single-user personal use

---

## Purpose

Ensure data integrity, stability, and basic security for a personal productivity app. Focus on preventing data loss, memory leaks, and sync failures during daily 8-hour usage sessions. **Skip enterprise-grade testing** (multi-user, compliance, cross-browser).

---

## Triggers (When to Apply This Skill)

Claude should apply this QA skill automatically when:

- "Test task persistence after refresh"
- "Verify offline sync works"
- "Check for memory leaks"
- "Test data integrity"
- "Run QA checklist"
- "Verify backup restore"
- "Test Supabase RLS"
- "Check Pomodoro timer accuracy"
- Modifying any data operations (create/edit/delete tasks)
- Adding new views or components
- Changing sync logic or offline handling
- **Before marking features complete**

---

## Core Testing Principles

### ALWAYS Test Before Marking Work Complete

**Data Persistence (Non-negotiable):**
- Create/edit/delete operations MUST survive page refresh
- All state changes MUST sync to Supabase within 2 seconds
- Local SQLite backup MUST mirror Supabase data (matching row counts)

**Memory Stability:**
- App MUST stay under 150MB during 8-hour workday
- View transitions MUST NOT leak memory (< 30MB growth per 50 transitions)
- NO detached DOM nodes after component unmount

**Offline Resilience:**
- Tasks created offline MUST sync when online without data loss or duplicates
- Multiple offline edits MUST preserve latest version only (timestamp wins)
- Sync status MUST be visible to user

---

## Test Requirements by Feature Type

### When Adding/Modifying Task Management Features

**MUST test (in order):**

1. **Persistence Test:**
   - Create task → wait 2 seconds → F5 refresh → task still visible
   - Edit task → wait 2 seconds → F5 refresh → changes saved
   - Delete task → wait 2 seconds → F5 refresh → task gone
   - Mark complete → refresh → status preserved

2. **Database Verification:**
```javascript
// Run in browser console after creating task
const { data } = await supabase
  .from('tasks')
  .select('*')
  .order('created_at', { ascending: false })
  .limit(1);
console.log('Last task:', data); // Verify matches UI
```

3. **SQLite Sync Check:**
   - Compare Supabase task count with local SQLite count
   - Verify `updated_at` timestamps match
   - Check `synced` flag is true for all tasks

4. **Offline Scenario:**
```javascript
// In Playwright test
await page.context().setOffline(true);
// Create 3 tasks offline
await page.context().setOffline(false);
await page.waitForTimeout(2000); // Allow sync
// Verify all 3 tasks in Supabase, no duplicates
```

5. **Conflict Resolution:**
   - Edit same task offline (Device A) and online (Device B)
   - Expected: Latest timestamp wins, no data corruption

**Console verification script (copy-paste ready):**
```javascript
// After any data operation, verify sync status
const { data: tasks, count } = await supabase
  .from('tasks')
  .select('*', { count: 'exact' });
console.log(`Total tasks in Supabase: ${count}`);
console.log('Last 5 tasks:', tasks.slice(-5));

// Check for unsynced (if using sync flag)
const { data: unsynced } = await supabase
  .from('tasks')
  .select('*')
  .eq('synced', false);
console.log(`Unsynced tasks: ${unsynced?.length || 0}`);
```

---

### When Adding/Modifying Views (Kanban, Calendar, Canvas)

**MUST test:**

1. **Memory Leak Check:**
   - Open Chrome DevTools → Shift+Esc (Task Manager)
   - Record initial memory (e.g., 80MB)
   - Navigate: Kanban → Calendar → Canvas → repeat 10 times
   - Check final memory: should be < 110MB (< 30MB growth)

2. **Data Display Accuracy:**
   - Create 5 tasks in Kanban → switch to Calendar → verify all 5 visible
   - Edit task in Calendar → switch to Kanban → verify change appears
   - Delete in Canvas → switch to other views → verify gone everywhere

3. **State Persistence:**
   - Apply filter in Kanban → switch to Calendar → return to Kanban → filter still applied
   - Canvas: create nodes → save → refresh → positions restored

4. **Performance:**
   - Load 100 tasks → switch between views → each transition < 500ms
   - No visible jank or lag during animations

**Memory profiling (Chrome DevTools):**
```
1. DevTools → Memory tab → Take heap snapshot (Snapshot 1)
2. Perform 10 view transitions
3. Take heap snapshot (Snapshot 2)
4. Click "Comparison" → compare Snapshot 2 to Snapshot 1
5. Check "Detached DOM tree" count → should be 0
6. Check memory delta → should be < 10MB
```

---

### When Modifying Pomodoro Timer

**MUST test:**

1. **Accuracy Test (25 minutes):**
   - Start timer → use phone stopwatch in parallel
   - After 25 minutes, compare: timer MUST be within ±1 second

2. **Pause/Resume:**
   - Start → run 5 minutes → pause
   - Wait 2 minutes (paused)
   - Resume → verify continues from 5-minute mark exactly

3. **Background Tab:**
   - Start timer → switch to another browser tab for 5 minutes
   - Return to app → timer should have progressed 5 minutes

4. **Page Refresh:**
   - Start timer → wait 3 minutes → refresh page
   - Expected: Timer recovers state OR warns user of lost session

5. **Completion Trigger:**
   - Run full 25-minute session
   - Verify notification/sound triggers (if implemented)

**Quick accuracy test (console):**
```javascript
// Start timer, then run this:
const start = Date.now();
setTimeout(() => {
  const elapsed = Date.now() - start;
  const error = Math.abs(elapsed - 60000); // 60 seconds
  console.log(`Expected: 60000ms, Actual: ${elapsed}ms, Error: ${error}ms`);
  if (error > 1000) console.error('Timer drift > 1 second');
  else console.log('Timer accurate');
}, 60000);
```

---

### When Adding Offline Capabilities

**MUST test all these scenarios:**

1. **Offline Create (5 tasks):**
   - DevTools → Network → Offline
   - Create "Task 1", "Task 2", "Task 3", "Task 4", "Task 5"
   - DevTools → Online
   - Wait 5 seconds → verify all 5 in Supabase
   - Verify NO duplicates

2. **Offline Edit:**
   - Go offline
   - Create task → edit same task 2 times (3 versions total)
   - Go online
   - Expected: Only latest version exists, not 3 separate tasks

3. **Offline Delete:**
   - Create task online
   - Go offline → delete task
   - Go online
   - Expected: Task stays deleted (not restored)

4. **Sync Status Visibility:**
   - User MUST see "Syncing...", "Synced", or "Sync Failed" indicator
   - Never silent failure

5. **Long Offline Period:**
   - Work offline for 10 minutes (create/edit/delete multiple tasks)
   - Go online
   - All changes sync successfully without data loss

**Offline test pattern (Playwright):**
```javascript
test('Offline sync preserves all changes', async ({ page }) => {
  await page.goto('http://localhost:5546');

  // Go offline
  await page.context().setOffline(true);

  // Create 5 tasks
  for (let i = 1; i <= 5; i++) {
    await page.fill('input[placeholder*="task"]', `Offline Task ${i}`);
    await page.click('button:has-text("Add")');
    await page.waitForTimeout(300);
  }

  // Verify locally visible
  const localCount = await page.locator('[data-testid="task-item"]').count();
  expect(localCount).toBe(5);

  // Go online
  await page.context().setOffline(false);
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(3000); // Allow sync

  // Verify in Supabase (run in browser context)
  const supabaseCount = await page.evaluate(async () => {
    const { count } = await window.supabase
      .from('tasks')
      .select('*', { count: 'exact', head: true });
    return count;
  });

  expect(supabaseCount).toBe(5);
});
```

---

## Memory Leak Prevention

### Common Vue 3 Leak Sources

**1. Event Listeners (CRITICAL):**
```vue
<script setup>
import { onMounted, onBeforeUnmount } from 'vue';

onMounted(() => {
  window.addEventListener('resize', handleResize);
});

onBeforeUnmount(() => {
  // CRITICAL: Must cleanup
  window.removeEventListener('resize', handleResize);
});
</script>
```

**2. Timers (CRITICAL):**
```javascript
const intervalId = setInterval(() => {
  // Pomodoro countdown logic
}, 1000);

onBeforeUnmount(() => {
  // CRITICAL: Must cleanup
  clearInterval(intervalId);
});
```

**3. WebSocket/Supabase Subscriptions:**
```javascript
const subscription = supabase
  .channel('tasks')
  .on('postgres_changes', { event: '*', schema: 'public', table: 'tasks' }, handleChange)
  .subscribe();

onBeforeUnmount(() => {
  subscription.unsubscribe();
});
```

**4. Third-Party Libraries:**
- Canvas/node editor instances: call `.destroy()` or `.dispose()` in `onBeforeUnmount`
- Chart libraries: clean up chart instances
- Date pickers: destroy picker instances

### Memory Testing Baseline

| State | Target | Failure Threshold |
|-------|--------|-------------------|
| Initial load (no tasks) | < 50MB | > 80MB |
| With 100 tasks | < 120MB | > 180MB |
| After 50 view transitions | < 80MB | > 150MB |
| Idle 30 mins | ±5MB change | > 20MB growth |

**How to Measure:**

**Method 1: Chrome Task Manager (Easiest)**
1. Shift+Esc → find your app tab
2. Watch "Memory" column during test
3. Record before/after values

**Method 2: Console API**
```javascript
// Run before and after test
const mb = (performance.memory.usedJSHeapSize / 1048576).toFixed(2);
console.log(`Memory: ${mb} MB`);
```

**Method 3: DevTools Memory Profiler (Most Detailed)**
1. DevTools → Memory tab
2. Take snapshot before test
3. Perform 50 view transitions
4. Force garbage collection (trash icon)
5. Take snapshot after test
6. Compare → check for:
   - Detached DOM nodes (should be 0)
   - Event listeners count (should not grow)
   - Total heap size growth (< 30MB)

---

## Data Integrity Checklist

### Before Every Commit Involving Data Operations

**Run this 5-minute checklist:**

- [ ] Create → Refresh: Task visible after refresh
- [ ] Edit → Refresh: Changes persisted
- [ ] Delete → Refresh: Task gone
- [ ] Complete → Refresh: Status saved
- [ ] Supabase Console: Data matches UI
- [ ] SQLite Count: Matches Supabase count
- [ ] Console Errors: No red errors during test
- [ ] Sync Status: "Synced" indicator visible after operations

### Edge Cases to Always Consider

**Sync Conflicts:**
- Scenario: Same task edited offline and online simultaneously
- Expected: Latest `updated_at` timestamp wins, no duplicate tasks
- Test: Edit in two browser windows (one offline)

**Browser Storage Limits:**
- Scenario: localStorage quota exceeded (5-10MB limit)
- Expected: App shows error message, suggests clearing old data
- Test: Fill localStorage with dummy data, then try to create task

**Tab Closed During Sync:**
- Scenario: User closes browser tab while sync in progress
- Expected: Reopening app recovers unsaved changes from SQLite backup
- Test: Create 5 tasks, immediately close tab, reopen, verify all 5 exist

**Corrupted Local Database:**
- Scenario: local DB file corrupted
- Expected: App detects corruption, restores from backup, syncs with Supabase
- Test: Corrupt DB file manually, restart app, verify recovery

---

## Backup & Recovery Requirements

### Backup File Validation

**On every app start, verify:**
- `local_data.db` exists and is readable (non-zero size)
- Backup file exists (< 24 hours old)
- If primary DB corrupted, restore from backup automatically
- If both missing, create new DB and sync from Supabase

### Recovery Scenarios

| Scenario | Expected Behavior | How to Test |
|----------|-------------------|-------------|
| Local DB deleted | Restore from backup file | `rm local_data.db` → restart |
| Backup also deleted | Create new DB, sync from Supabase | Delete both → restart |
| Supabase unreachable | Use local DB, queue syncs | DevTools → Offline mode |
| Both DBs empty | Start fresh | Clean install |
| Sync fails 3x | Show error, retry with backoff | Mock API failure |

---

## Security Testing (Personal App Scope)

### Supabase RLS Enforcement

**MUST verify these:**

1. **Anonymous Access Blocked:**
```javascript
// In browser console (logged out)
const { data, error } = await supabase.from('tasks').select('*');
console.log('Error code:', error?.code); // Should be PGRST301 or 401
```

2. **RLS Enabled on All Tables:**
```sql
-- In Supabase SQL Editor
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public';
-- All should show rowsecurity = true
```

3. **User Can Only See Own Data:**
```sql
-- As logged-in user
SELECT * FROM tasks;
-- Should return only tasks where user_id = auth.uid()

-- Check no orphaned records
SELECT * FROM tasks WHERE user_id IS NULL;
-- Should return 0 rows
```

### Input Validation (XSS Prevention)

| Input | Expected Behavior |
|-------|-------------------|
| `<script>alert('xss')</script>` | Rendered as plain text, no alert |
| `<img src=x onerror=alert(1)>` | Rendered as plain text, no execution |
| `'; DROP TABLE tasks; --` | Stored as literal string |
| Task name > 1000 chars | Truncated or rejected with error |

**Test in UI:**
1. Create task with name: `<script>alert('XSS')</script>`
2. Check UI: Should display literal text
3. Check DOM: Should be escaped (`&lt;script&gt;`)

### Auth Edge Cases

| Test | Steps | Expected |
|------|-------|----------|
| Sign up | Create new account | Auto-logged in, redirected |
| Sign in | Valid credentials | Session token stored |
| Wrong password | Invalid credentials | Error message, NOT logged in |
| Session persistence | Login → refresh | Still logged in |
| Logout | Click logout → refresh | Session cleared |
| Expired token | Wait 1 hour (or mock) | Auto-logout OR silent refresh |

---

## Performance Targets

### Acceptable Response Times

| Operation | Target | Max Acceptable |
|-----------|--------|----------------|
| Page load (TTI) | < 2s | < 4s |
| Add task (render) | < 300ms | < 800ms |
| Sync to Supabase | < 2s | < 5s |
| View transition | < 200ms | < 500ms |
| Render 100 tasks | < 1.5s | < 3s |
| Canvas 50 nodes | < 1s | < 2s |

### Stress Testing Baselines

**Task Volume:**
- 50 tasks: Must be smooth, no lag
- 100 tasks: Slight lag acceptable (< 2s render)
- 250 tasks: Still usable, document as soft limit
- 500+ tasks: Warn user if approaching

**Long-Running Session:**
- 1 hour: No memory growth, app responsive
- 4 hours: < 50MB memory growth acceptable
- 8 hours (full workday): < 100MB growth, no crashes

---

## Testing Workflow Integration

### Before Committing Code

**Quick Check (2 minutes):**
- [ ] Run app, perform changed operation
- [ ] Refresh page → verify persistence
- [ ] Check console for errors
- [ ] Chrome Task Manager → verify no memory spike

**Standard Check (10 minutes):**
- [ ] Quick check (above)
- [ ] Test offline → online sync (create 3 tasks)
- [ ] Supabase console → verify data matches UI
- [ ] Switch between all 3 views
- [ ] Run unit tests: `npm run test:unit`

**Full Check (30 minutes, before release):**
- [ ] Standard check (above)
- [ ] Create 100 tasks → verify render time < 2s
- [ ] Navigate views 20 times → memory growth < 20MB
- [ ] Leave app idle 5 mins → verify no memory leak
- [ ] Test backup restore
- [ ] Verify RLS (logged out access blocked)

### When to Run Each Level

| Level | When | Time |
|-------|------|------|
| Quick check | Every commit | 2 min |
| Standard check | Before pushing to main | 10 min |
| Full check | Before deploying, after major features | 30 min |

---

## Common Failures & Fixes

### Issue: Tasks disappear after refresh

**Likely Cause:** Sync not completing before refresh
**Fix:** Add `await` to database operations, show loading state

```javascript
// Bad: Fire-and-forget
const createTask = async (name) => {
  supabase.from('tasks').insert({ name });
};

// Good: Wait for sync
const createTask = async (name) => {
  const { data, error } = await supabase.from('tasks').insert({ name });
  if (error) console.error('Sync failed:', error);
  else console.log('Task synced:', data);
};
```

### Issue: Memory grows continuously

**Likely Cause:** Event listeners not cleaned up
**Fix:** Check all `addEventListener` have matching `removeEventListener`
**Debug:** DevTools → Memory → Compare snapshots → Look for "Detached DOM tree"

### Issue: Offline changes lost

**Likely Cause:** No local queue for pending syncs
**Fix:** Implement sync queue in IndexedDB/localStorage, retry on online event

### Issue: Sync conflicts create duplicates

**Likely Cause:** No deduplication logic
**Fix:** Use `upsert` with unique constraint

```javascript
const { data, error } = await supabase
  .from('tasks')
  .upsert({ id: taskId, ...updates }, { onConflict: 'id' });
```

### Issue: Pomodoro timer drifts over 25 minutes

**Likely Cause:** Using `setInterval` which compounds lag
**Fix:** Store start timestamp, calculate remaining time on each tick

```javascript
// Bad: setInterval compounds lag
let seconds = 1500;
setInterval(() => { seconds--; }, 1000);

// Good: Timestamp-based calculation
const startTime = Date.now();
const duration = 25 * 60 * 1000;

setInterval(() => {
  const elapsed = Date.now() - startTime;
  const remaining = duration - elapsed;
  const seconds = Math.ceil(remaining / 1000);
}, 100);
```

---

## What NOT to Test (Overkill for Personal App)

**Skip these (enterprise-only concerns):**
- Cross-browser testing → Just use Chrome/Brave
- Mobile responsiveness → Desktop-only
- Multi-user conflict resolution → Single-user app
- Load testing 1000+ concurrent users → Only you use it
- WCAG accessibility compliance → Personal tool
- GDPR/compliance audits → Your own data
- Penetration testing → Not exposed publicly

**Do test these (personal app essentials):**
- Data integrity → No disappearing tasks (deal-breaker)
- Memory leaks → Must work 8 hours (your workday)
- Offline resilience → Common personal use case
- Backup recovery → Single point of failure
- Basic security (RLS) → Prevents accidents

---

## Sign-Off Checklist (Before Daily Use)

**Must pass ALL these before considering app ready for personal daily use:**

- [ ] Create/edit/delete tasks survive F5 refresh
- [ ] Supabase and SQLite data counts match
- [ ] Offline → online sync works for 5+ tasks without duplicates
- [ ] Memory stable after 30-minute usage session (< 50MB growth)
- [ ] Can handle 100+ tasks without lag (< 2s render time)
- [ ] Pomodoro timer accurate to ±1 second over 25 minutes
- [ ] Backup restores successfully when local DB deleted
- [ ] RLS blocks unauthenticated access (test in console)
- [ ] No console errors during normal usage
- [ ] All 3 views (Kanban/Calendar/Canvas) render correctly

---

## Example 10-Minute Test Session

**Goal: Verify app is stable for daily use**

```
1. [2 min] Data Integrity
   - Create "Test Task 1" → refresh → verify visible
   - Edit to "Test Task 1 Updated" → refresh → verify change
   - Delete → refresh → verify gone

2. [3 min] Offline Sync
   - DevTools → Offline
   - Create "Offline Task 1", "Offline Task 2", "Offline Task 3"
   - DevTools → Online
   - Wait 5 seconds → verify all 3 in Supabase console

3. [2 min] View Transitions
   - Kanban → Calendar → Canvas → Kanban → Calendar → Canvas
   - Chrome Task Manager: memory < 100MB

4. [2 min] Pomodoro
   - Start timer → wait 10 seconds → verify countdown accurate
   - Pause → wait 5 seconds → verify time frozen
   - Resume → verify continues from pause point

5. [1 min] Console Check
   - No red errors in console
   - No "401 Unauthorized" messages
   - Sync status shows "Synced"

Pass Criteria: All steps complete without errors, memory < 100MB
```

---

## Refusal & Escalation

**Refuse to skip these critical tests:**
- Data persistence (create/edit/delete → refresh)
- Offline sync verification
- Memory leak checks after adding components/features

**Escalate to human review if:**
- Test failures persist after 3 attempts to fix
- Memory leak source unclear after profiling
- Sync conflicts creating data corruption

---

## Mandatory User Verification

**CRITICAL**: Before claiming ANY issue is "fixed", "resolved", or "complete":

1. Run all relevant tests (build, type-check, unit tests)
2. Verify no console errors
3. Take screenshots/evidence of the fix
4. **Use AskUserQuestion to explicitly ask the user to verify**
5. **DO NOT mark tasks as completed without user confirmation**

**The user is the final authority on whether something is fixed. No exceptions.**

---

## Canvas Geometry Invariant Tests (TASK-256)

### Critical Canvas Stability Tests

The canvas system has automated tests protecting the three most fragile parts. **Run these tests when modifying any canvas-related code:**

```bash
# Run all geometry/sync/smartgroup tests
npm test -- --run tests/unit/geometry-invariants.test.ts tests/unit/sync-readonly.test.ts tests/unit/smartgroup-metadata.test.ts
```

### Test Files

| File | Purpose | When to Run |
|------|---------|-------------|
| `tests/unit/geometry-invariants.test.ts` | Verify single-writer rule: only drag handlers change positions | Modifying drag/drop, position updates |
| `tests/unit/sync-readonly.test.ts` | Verify sync is read-only: never mutates stores | Modifying useCanvasSync, sync logic |
| `tests/unit/smartgroup-metadata.test.ts` | Verify Smart-Groups only change metadata, not geometry | Modifying power keywords, overdue collector |

### Key Invariants Being Tested

**1. Geometry Single-Writer Rule:**
- Only `useCanvasInteractions.ts` drag handlers can modify:
  - Task: `parentId`, `canvasPosition`
  - Group: `parentGroupId`, `position`
- All other code must be READ-ONLY for these fields

**2. Sync Read-Only Behavior:**
- `syncStoreToCanvas` reads from stores, writes only to Vue Flow nodes
- NEVER calls `updateTask` or `updateGroup` from sync
- Position mismatches log warnings but don't mutate store

**3. Smart-Group Metadata-Only:**
- Power keywords (Today, Friday, High Priority) update metadata only
- `applySmartGroupProperties` returns only metadata fields (dueDate, status, priority)
- Never changes parentId or canvasPosition

### Test Helpers Location

```
tests/unit/helpers/geometry-test-helpers.ts
```

Key helpers:
- `changedTaskGeometryFields(before, after)` - Detect geometry changes
- `changedGroupGeometryFields(before, after)` - Detect group geometry changes
- `assertNoTaskGeometryChanged(beforeMap, afterMap)` - Bulk assertion
- `createTestTask()`, `createTestGroup()` - Fixtures

### When to Run These Tests

**ALWAYS run before:**
- Modifying `useCanvasInteractions.ts` (drag handlers)
- Modifying `useCanvasSync.ts` (sync logic)
- Modifying `usePowerKeywords.ts` or `useCanvasOverdueCollector.ts`
- Modifying `useCanvasSectionProperties.ts`
- Any changes to task/group position or parent fields

**Quick validation command:**
```bash
npm test -- --run tests/unit/geometry
```

### Expected Output

```
✓ tests/unit/geometry-invariants.test.ts (20 tests)
✓ tests/unit/sync-readonly.test.ts (12 tests)
✓ tests/unit/smartgroup-metadata.test.ts (26 tests)

Test Files  3 passed
Tests       58 passed
```

### If Tests Fail

**Geometry invariant failure:**
- Check if your code accidentally mutates `parentId`, `canvasPosition`, `parentGroupId`, or `position`
- Ensure only drag handlers call position-changing methods

**Sync read-only failure:**
- Remove any `updateTask`/`updateGroup` calls from sync functions
- Sync should only call `setNodes` (Vue Flow display layer)

**Smart-Group failure:**
- Ensure `applySmartGroupProperties` only returns metadata fields
- Check `ENABLE_SMART_GROUP_REPARENTING` flag is false

---

---

## Integration with Stress Testing (TASK-338)

For comprehensive stress testing beyond the standard QA checklist, use the `stress-tester` skill:

```bash
# Full stress test suite
npm run test:stress:full

# Quick stress tests
npm run test:stress:quick

# Generate stress test report
npm run test:stress:report
```

**When to use stress-tester instead of qa-testing:**
- Before major releases
- After significant refactoring
- When investigating reliability issues
- Security audits
- Performance regression testing

**Skill chaining:**
```
qa-testing → stress-tester (for deeper testing)
stress-tester → dev-debugging (for fixes)
dev-debugging → qa-testing (to verify fix)
```

See `.claude/skills/stress-tester/SKILL.md` for full documentation.

---

**Version History:**
- v1.0 (Jan 2026): Original functional testing skill
- v2.0 (Jan 2026): Enhanced with data integrity, memory testing, offline sync, backup verification, and security testing for personal app use
- v2.1 (Jan 2026): Added Canvas Geometry Invariant Tests (TASK-256)
- v2.2 (Jan 2026): Integration with stress-tester skill (TASK-338)

---

## Automatic Skill Chaining

**IMPORTANT**: After QA testing, Claude should automatically invoke related skills based on findings:

1. **If tests fail due to bugs** → Use `Skill(dev-debugging)` to investigate and fix
2. **If canvas geometry issues** → Use `Skill(vue-flow-debug)` for specialized debugging
3. **If planning needed for fixes** → Use `Skill(chief-architect)` to break down complex work
4. **If UI/UX issues found** → Use `Skill(dev-implement-ui-ux)` for design fixes

**Mandatory Pre-Success Chain**:
Before claiming ANY feature is "done", "fixed", or "complete":
```
1. Run relevant tests (this skill)
2. If tests pass → Ask user to verify
3. Only after user confirms → Mark as complete
```

**This skill is automatically invoked by other skills after:**
- Bug fixes (dev-debugging chains to qa-testing)
- Feature implementation (chief-architect chains to qa-testing)
- UI changes (dev-implement-ui-ux chains to qa-testing)
